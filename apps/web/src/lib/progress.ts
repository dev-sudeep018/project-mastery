import { z } from "zod";
import { allItems as catalog } from "./curriculum";

export const LEARNING_KEY = "mastery:learning:v1";
export const draftKey = (id: string, version: number) =>
  `mastery:draft:${id}:v${version}`;
export const completionKey = (id: string, version: number) =>
  `mastery:progress:${id}:v${version}`;
const recordSchema = z.strictObject({
  updatedAt: z.number().int().nonnegative().max(8_640_000_000_000_000),
  completed: z.boolean(),
  attempts: z.number().int().nonnegative().max(1_000_000),
});
const stateSchema = z.record(
  z.string().regex(/^[mdep][0-9]{2,5}:v[1-9][0-9]*$/),
  recordSchema,
);
export type LearningState = z.infer<typeof stateSchema>;
const keyFor = (id: string, version: number) => `${id}:v${version}`;
export function completed(state: LearningState, id: string) {
  const item = catalog.find((item) => item.id === id);
  return !!(item && state[keyFor(id, item.version)]?.completed);
}
export function readProgress(): LearningState {
  try {
    const parsed = stateSchema.safeParse(
      JSON.parse(localStorage.getItem(LEARNING_KEY) ?? "{}"),
    );
    const state = parsed.success ? parsed.data : {};
    for (const item of catalog) {
      const key = keyFor(item.id, item.version);
      if (
        localStorage.getItem(completionKey(item.id, item.version)) ===
        "complete"
      )
        state[key] = {
          ...(state[key] ?? { updatedAt: 0, attempts: 0 }),
          completed: true,
        };
    }
    return state;
  } catch {
    return {};
  }
}
export function recordVisit(id: string, version: number, result?: boolean) {
  const state = readProgress(),
    key = keyFor(id, version),
    previous = state[key];
  state[key] = {
    updatedAt: Date.now(),
    completed: !!previous?.completed || result === true,
    attempts: Math.min(
      1_000_000,
      (previous?.attempts ?? 0) + (result === undefined ? 0 : 1),
    ),
  };
  localStorage.setItem(LEARNING_KEY, JSON.stringify(state));
  if (state[key].completed)
    localStorage.setItem(completionKey(id, version), "complete");
  window.dispatchEvent(new Event("mastery-progress"));
}
export function mergeProgress(
  current: LearningState,
  incoming: LearningState,
): LearningState {
  const merged = { ...current };
  for (const item of catalog) {
    const key = keyFor(item.id, item.version),
      next = incoming[key],
      prev = merged[key];
    if (next)
      merged[key] = {
        updatedAt: Math.max(prev?.updatedAt ?? 0, next.updatedAt),
        completed: !!prev?.completed || next.completed,
        attempts: Math.max(prev?.attempts ?? 0, next.attempts),
      };
  }
  return merged;
}
export const BackupSchema = z.strictObject({
  format: z.literal("project-mastery-backup"),
  version: z.literal(1),
  progress: stateSchema,
  drafts: z.record(
    z.string().regex(/^mastery:draft:[mdep][0-9]{2,5}:v[1-9][0-9]*$/),
    z.string().max(32_000),
  ),
});
export type Backup = z.infer<typeof BackupSchema>;
export function exportBackup(): Backup {
  const drafts: Record<string, string> = {};
  for (const item of catalog) {
    const key = draftKey(item.id, item.version);
    try {
      const value = JSON.parse(localStorage.getItem(key) ?? "null");
      if (
        value?.version === 1 &&
        typeof value.code === "string" &&
        value.code.length <= 32_000
      )
        drafts[key] = value.code;
    } catch {
      /* A corrupt draft must not prevent the remaining export. */
    }
  }
  return {
    format: "project-mastery-backup",
    version: 1,
    progress: readProgress(),
    drafts,
  };
}
export function importBackup(backup: Backup) {
  const valid = BackupSchema.parse(backup);
  localStorage.setItem(
    LEARNING_KEY,
    JSON.stringify(mergeProgress(readProgress(), valid.progress)),
  );
  for (const item of catalog) {
    const key = draftKey(item.id, item.version);
    if (valid.drafts[key] !== undefined && localStorage.getItem(key) === null)
      localStorage.setItem(
        key,
        JSON.stringify({ version: 1, code: valid.drafts[key] }),
      );
  }
  window.dispatchEvent(new Event("mastery-progress"));
}
