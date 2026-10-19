export const DRAFT_KEY = "mastery:draft:m02:v1";
export const PROGRESS_KEY = "mastery:progress:m02:v1";
export function readDraft(value: string | null, starter: string) {
  if (!value) return starter;
  try {
    const draft = JSON.parse(value);
    return draft.version === 1 &&
      typeof draft.code === "string" &&
      draft.code.length <= 32_000
      ? draft.code
      : starter;
  } catch {
    return starter;
  }
}
