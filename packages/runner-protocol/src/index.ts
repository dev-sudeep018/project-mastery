import { z } from "zod";

export const PROTOCOL_VERSION = 1;
export const MAX_SOURCE_LENGTH = 32_000;
export const EXECUTION_TIMEOUT_MS = 3_000;
export const BOOT_TIMEOUT_MS = 45_000;
const id = z.string().uuid();
export const RunRequestSchema = z.strictObject({
  kind: z.literal("run"),
  protocol: z.literal(PROTOCOL_VERSION),
  requestId: id,
  problemId: z.string().regex(/^[mdep][0-9]{2,5}$/),
  problemVersion: z.number().int().positive(),
  sourceCode: z.string().max(MAX_SOURCE_LENGTH),
  mode: z.enum(["sample", "all"]),
});
export const HostMessageSchema = z.discriminatedUnion("kind", [
  RunRequestSchema,
  z.strictObject({
    kind: z.literal("hello"),
    protocol: z.literal(PROTOCOL_VERSION),
  }),
  z.strictObject({
    kind: z.literal("cancel"),
    protocol: z.literal(PROTOCOL_VERSION),
    requestId: id,
  }),
]);
export const TestResultSchema = z.strictObject({
  name: z.string().max(120),
  passed: z.boolean(),
  message: z.string().max(600),
});
export const RunResultSchema = z.strictObject({
  kind: z.literal("result"),
  protocol: z.literal(PROTOCOL_VERSION),
  requestId: id,
  status: z.enum(["passed", "failed", "error", "timeout", "cancelled"]),
  tests: z.array(TestResultSchema).max(40),
  output: z.string().max(4096),
  error: z.string().max(2048),
  durationMs: z.number().finite().nonnegative().max(300_000),
});
export const RunnerMessageSchema = z.discriminatedUnion("kind", [
  z.strictObject({
    kind: z.literal("ready"),
    protocol: z.literal(PROTOCOL_VERSION),
  }),
  z.strictObject({
    kind: z.literal("status"),
    protocol: z.literal(PROTOCOL_VERSION),
    requestId: id,
    phase: z.enum(["loading", "running"]),
  }),
  RunResultSchema,
]);
export type RunRequest = z.infer<typeof RunRequestSchema>;
export type RunResult = z.infer<typeof RunResultSchema>;

export function assertSeparateOrigin(appOrigin: string, runnerOrigin: string) {
  const app = new URL(appOrigin);
  const runner = new URL(runnerOrigin);
  if (
    !["http:", "https:"].includes(runner.protocol) ||
    runner.origin === app.origin ||
    runner.username ||
    runner.password ||
    runner.pathname !== "/" ||
    runner.search ||
    runner.hash
  ) {
    throw new Error(
      "Python runner must use a separate HTTP(S) origin without credentials or a path.",
    );
  }
  return runner.origin;
}
