import { spawnSync } from "node:child_process";
import { loadContent, root } from "./content";
const entries = await loadContent();
const python = process.env.PYTHON ?? "python";
const result = spawnSync(
  python,
  ["-m", "unittest", "discover", "-s", "tests/python", "-v"],
  { cwd: root, stdio: "inherit" },
);
if (result.error) throw result.error;
if (result.status !== 0) process.exit(result.status ?? 1);
console.log(
  `Validated ${entries.length} problem package(s), prerequisite graph, and reference evaluator.`,
);
