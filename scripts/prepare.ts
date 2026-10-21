import { cp, mkdir, readFile, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { createRequire } from "node:module";
import path from "node:path";
import { build } from "esbuild";
import { loadContent, root } from "./content";
import { validateCatalog } from "../packages/problem-schema/src/index";

const require = createRequire(import.meta.url);
const entries = (await loadContent()).filter(
  (entry) => entry.problem.status === "validated",
);
validateCatalog(entries.map((entry) => entry.problem));
const runner = path.join(root, "apps/runner/public");
const runtime = path.join(runner, "runtime");
const generated = path.join(root, "apps/web/src/generated");
await Promise.all([
  mkdir(runtime, { recursive: true }),
  mkdir(generated, { recursive: true }),
  mkdir(path.join(generated, "items"), { recursive: true }),
  mkdir(path.join(root, "apps/runner/src/generated"), { recursive: true }),
  mkdir(path.join(runner, "generated"), { recursive: true }),
]);
const pyodideDir = path.dirname(require.resolve("pyodide"));
const pyodidePackage = JSON.parse(
  await readFile(path.join(pyodideDir, "package.json"), "utf8"),
);
const runtimeMarker = path.join(runtime, ".version");
let preparedVersion = "";
try {
  preparedVersion = await readFile(runtimeMarker, "utf8");
} catch {
  /* First setup. */
}
if (preparedVersion !== pyodidePackage.version) {
  await cp(pyodideDir, runtime, { recursive: true });
  await writeFile(runtimeMarker, pyodidePackage.version);
}
const lock = JSON.parse(
  await readFile(path.join(runtime, "pyodide-lock.json"), "utf8"),
);
const needed = new Set<string>();
function collect(name: string) {
  if (needed.has(name)) return;
  const pkg = lock.packages[name];
  if (!pkg) throw new Error(`No package ${name} in the pinned runtime.`);
  needed.add(name);
  for (const dependency of pkg.depends ?? []) collect(dependency);
}
collect("numpy");
for (const name of needed) {
  const pkg = lock.packages[name];
  const target = path.join(runtime, pkg.file_name);
  let bytes: Buffer | undefined;
  try {
    bytes = await readFile(target);
  } catch {
    /* Download below. */
  }
  if (bytes && createHash("sha256").update(bytes).digest("hex") === pkg.sha256)
    continue;
  console.log(`Downloading verified runtime package: ${name}`);
  const response = await fetch(
    `https://cdn.jsdelivr.net/pyodide/v${pyodidePackage.version}/full/${pkg.file_name}`,
  );
  if (!response.ok)
    throw new Error(`Package download failed: ${response.status}`);
  bytes = Buffer.from(await response.arrayBuffer());
  if (createHash("sha256").update(bytes).digest("hex") !== pkg.sha256)
    throw new Error(`Checksum mismatch for ${name}`);
  await writeFile(target, bytes);
}
const webRequire = createRequire(path.join(root, "apps/web/package.json"));
const monacoWorker = webRequire.resolve(
  "monaco-editor/editor/editor.worker.js",
);
await build({
  entryPoints: [monacoWorker],
  outfile: path.join(root, "apps/web/public/editor.worker.js"),
  bundle: true,
  format: "esm",
  target: "es2022",
  minify: true,
});
const helpers = await readFile(
  path.join(root, "content/evaluator_helpers.py"),
  "utf8",
);
await writeFile(
  path.join(generated, "catalog.json"),
  JSON.stringify(entries.map((e) => e.problem)),
);
const manifest = entries.map(({ problem }) => ({
  id: problem.id,
  version: problem.version,
  evaluator: `/generated/${problem.id}-v${problem.version}.py`,
}));
await writeFile(
  path.join(root, "apps/runner/src/generated/manifest.json"),
  JSON.stringify(manifest),
);
for (const entry of entries) {
  const { problem, lesson, starter, solution } = entry;
  await writeFile(
    path.join(generated, "items", `${problem.slug}.json`),
    JSON.stringify({ problem, lesson, starter, solution }),
  );
  await writeFile(
    path.join(runner, `generated/${problem.id}-v${problem.version}.py`),
    helpers + "\n" + entry.tests,
  );
}
await build({
  entryPoints: [
    path.join(root, "apps/runner/src/bridge.ts"),
    path.join(root, "apps/runner/src/worker.ts"),
  ],
  outdir: runner,
  bundle: true,
  format: "esm",
  target: "es2022",
  minify: true,
  external: ["/runtime/*"],
  define: {
    __APP_ORIGIN__: JSON.stringify(
      process.env.APP_ORIGIN ?? "http://localhost:3000",
    ),
  },
});
console.log(
  "Content, local Monaco assets, and isolated Python runner are ready.",
);
