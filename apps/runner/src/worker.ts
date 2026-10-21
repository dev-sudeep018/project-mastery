import {
  PROTOCOL_VERSION,
  RunRequestSchema,
} from "../../../packages/runner-protocol/src/index";
import manifest from "./generated/manifest.json";

// Kept external by esbuild and served exclusively from the runner origin.
// @ts-expect-error This module is supplied by the pinned, locally copied runtime.
import { loadPyodide } from "/runtime/pyodide.mjs";

const workerScope = globalThis as unknown as {
  postMessage: (data: unknown) => void;
  onmessage: ((event: MessageEvent) => void) | null;
};
const pyodide = await loadPyodide({ indexURL: `${location.origin}/runtime/` });
await pyodide.loadPackage("numpy");
const parameters = new URL(location.href).searchParams;
const item = manifest.find(
  (item) =>
    item.id === parameters.get("item") &&
    String(item.version) === parameters.get("version"),
);
if (!item) throw new Error("Unknown lesson version.");
const evaluatorResponse = await fetch(item.evaluator);
if (!evaluatorResponse.ok) throw new Error("Evaluator is unavailable.");
const evaluator = await evaluatorResponse.text();
workerScope.onmessage = async (event: MessageEvent) => {
  const parsed = RunRequestSchema.safeParse(event.data);
  if (!parsed.success) return;
  workerScope.onmessage = null;
  const request = parsed.data;
  if (request.problemId !== item.id || request.problemVersion !== item.version)
    return;
  const started = performance.now();
  let output = "";
  const append = (line: string) => {
    output = (output + line + "\n").slice(0, 4096);
  };
  pyodide.setStdout({ batched: append });
  pyodide.setStderr({ batched: append });
  pyodide.globals.set("__submission", request.sourceCode);
  pyodide.globals.set("__mode", request.mode);
  try {
    await pyodide.runPythonAsync(evaluator);
    const json = await pyodide.runPythonAsync(`
import json as _json
_learner = {"__name__": "__main__"}
exec(compile(__submission, "solution.py", "exec"), _learner)
_json.dumps(run_tests(_learner, __mode))
`);
    const tests = JSON.parse(json as string);
    workerScope.postMessage({
      kind: "result",
      protocol: PROTOCOL_VERSION,
      requestId: request.requestId,
      status: tests.every((t: { passed: boolean }) => t.passed)
        ? "passed"
        : "failed",
      tests,
      output,
      error: "",
      durationMs: Math.round(performance.now() - started),
    });
  } catch (error) {
    workerScope.postMessage({
      kind: "result",
      protocol: PROTOCOL_VERSION,
      requestId: request.requestId,
      status: "error",
      tests: [],
      output,
      error: String(error).slice(-2048),
      durationMs: Math.round(performance.now() - started),
    });
  }
};
workerScope.postMessage({ kind: "prepared" });
