import { spawnSync } from "node:child_process";
import { loadContent, root } from "./content";

// Fast authoring loop; the complete release gate remains `pnpm check` and CI.
const entries = await loadContent();
const ids = new Set(process.argv.slice(2));
for (const id of ids) {
  if (!entries.some((entry) => entry.problem.id === id)) {
    throw new Error(
      `Unknown lesson ID: ${id}. Use IDs such as m05 d06 e07, or omit IDs for all packages.`,
    );
  }
}
const selected = entries.filter(
  (entry) => !ids.size || ids.has(entry.problem.id),
);
if (!selected.length) throw new Error("No content packages selected");

// A review signal only: this detects identical task text with changed numbers,
// not semantic plagiarism or whether two objectives teach the same concept.
const tasks = new Map<string, string[]>();
for (const entry of entries) {
  const key = entry.lesson.task
    .toLowerCase()
    .replace(/\d+(?:\.\d+)?/g, "#")
    .replace(/\s+/g, " ")
    .trim();
  tasks.set(key, [...(tasks.get(key) ?? []), entry.problem.id]);
}
for (const group of tasks.values()) {
  if (
    group.length > 1 &&
    group.some((id) => selected.some((entry) => entry.problem.id === id))
  ) {
    console.warn(`Review possible duplicate task wording: ${group.join(", ")}`);
  }
}
const start = performance.now();
const result = spawnSync(
  process.env.PYTHON ?? "python",
  [
    "-m",
    "unittest",
    "discover",
    "-s",
    "tests/python",
    "-p",
    "test_content.py",
    "-k",
    "test_every_reference_passes",
    "-v",
  ],
  {
    cwd: root,
    stdio: "inherit",
    env: {
      ...process.env,
      MASTERY_CONTENT_FOLDERS: JSON.stringify(
        selected.map((entry) => entry.folder),
      ),
    },
  },
);
if (result.error) throw result.error;
if (result.status !== 0) process.exit(result.status ?? 1);
console.log(
  `Checked ${selected.length} packages / ${selected.reduce((sum, entry) => sum + entry.lesson.test_count, 0)} public cases in ${((performance.now() - start) / 1000).toFixed(1)}s of native execution. References, starters, sample counts and trivial wrong answers checked. Browser execution and editorial review still required.`,
);
