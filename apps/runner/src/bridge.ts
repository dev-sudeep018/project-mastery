import {
  BOOT_TIMEOUT_MS,
  EXECUTION_TIMEOUT_MS,
  HostMessageSchema,
  PROTOCOL_VERSION,
  RunResultSchema,
  type RunRequest,
  type RunResult,
} from "../../../packages/runner-protocol/src/index";
import manifest from "./generated/manifest.json";

declare const __APP_ORIGIN__: string;
const appOrigin = __APP_ORIGIN__;
if (location.origin === appOrigin || parent === window)
  throw new Error("Runner requires a separate parent origin.");
let active: {
  request: RunRequest;
  worker: Worker;
  timer: ReturnType<typeof setTimeout>;
  started: number;
} | null = null;
const send = (message: unknown) => parent.postMessage(message, appOrigin);

function finish(status: RunResult["status"], error = "") {
  if (!active) return;
  const { request, worker, timer, started } = active;
  clearTimeout(timer);
  worker.terminate();
  active = null;
  send({
    kind: "result",
    protocol: PROTOCOL_VERSION,
    requestId: request.requestId,
    status,
    tests: [],
    output: "",
    error: error.slice(0, 2048),
    durationMs: Math.round(performance.now() - started),
  });
}

addEventListener("message", (event: MessageEvent) => {
  if (event.source !== parent || event.origin !== appOrigin) return;
  const parsed = HostMessageSchema.safeParse(event.data);
  if (!parsed.success) return;
  const message = parsed.data;
  if (message.kind === "hello") {
    send({ kind: "ready", protocol: PROTOCOL_VERSION });
    return;
  }
  if (message.kind === "cancel") {
    if (active?.request.requestId === message.requestId)
      finish("cancelled", "Run stopped. Your code is saved.");
    return;
  }
  if (active) return;
  const item = manifest.find(
    (item) =>
      item.id === message.problemId && item.version === message.problemVersion,
  );
  if (!item) {
    send({
      kind: "result",
      protocol: PROTOCOL_VERSION,
      requestId: message.requestId,
      status: "error",
      tests: [],
      output: "",
      error: "This lesson version is unavailable. Reload the page.",
      durationMs: 0,
    });
    return;
  }
  const worker = new Worker(
    `/worker.js?item=${item.id}&version=${item.version}`,
    { type: "module" },
  );
  const started = performance.now();
  const timer = setTimeout(
    () =>
      finish(
        "error",
        "Python could not load in time. Check the runner and try again.",
      ),
    BOOT_TIMEOUT_MS,
  );
  active = { request: message, worker, started, timer };
  send({
    kind: "status",
    protocol: PROTOCOL_VERSION,
    requestId: message.requestId,
    phase: "loading",
  });
  let executing = false;
  worker.onmessage = (event: MessageEvent) => {
    if (active?.worker !== worker) return;
    if (!executing && event.data?.kind === "prepared") {
      executing = true;
      clearTimeout(active.timer);
      active.timer = setTimeout(
        () =>
          finish(
            "timeout",
            "Execution exceeded 3 seconds. Look for an infinite loop or reduce the work.",
          ),
        EXECUTION_TIMEOUT_MS,
      );
      send({
        kind: "status",
        protocol: PROTOCOL_VERSION,
        requestId: message.requestId,
        phase: "running",
      });
      worker.postMessage(message);
      return;
    }
    const parsed = RunResultSchema.safeParse(event.data);
    if (!parsed.success || parsed.data.requestId !== message.requestId) return;
    clearTimeout(active.timer);
    worker.terminate();
    active = null;
    send(parsed.data);
  };
  worker.onerror = () =>
    finish(
      "error",
      "The Python worker stopped unexpectedly. Try again; each run starts fresh.",
    );
  worker.onmessageerror = () =>
    finish("error", "The runner returned unreadable output. Try again.");
});
send({ kind: "ready", protocol: PROTOCOL_VERSION });
