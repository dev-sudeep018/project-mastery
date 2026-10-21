import { describe, expect, it } from "vitest";
import {
  BackupSchema,
  mergeProgress,
  draftKey,
} from "../../apps/web/src/lib/progress";
import {
  chunks,
  metrics,
  fuse,
  evaluateProject,
} from "../../apps/web/src/lib/retrieval";
import {
  ProblemSchema,
  validateCatalog,
} from "../../packages/problem-schema/src/index";
import { loadContent } from "../../scripts/content";

describe("portable progress", () => {
  it("preserves completion and the newer timestamp without inventing added attempts", () => {
    expect(
      mergeProgress(
        { "m02:v1": { updatedAt: 40, completed: true, attempts: 3 } },
        {
          "m02:v1": { updatedAt: 20, completed: false, attempts: 1 },
          "m99999:v1": { updatedAt: 100, completed: true, attempts: 4 },
        },
      ),
    ).toEqual({ "m02:v1": { updatedAt: 40, completed: true, attempts: 3 } });
    expect(draftKey("m02", 1)).not.toBe(draftKey("e02", 1));
    expect(draftKey("m02", 1)).not.toBe(draftKey("m02", 2));
  });
  it("rejects unsupported and malformed backups", () => {
    const backup = {
      format: "project-mastery-backup",
      version: 1,
      progress: {},
      drafts: {},
    };
    expect(BackupSchema.safeParse(backup).success).toBe(true);
    for (const patch of [
      { version: 2 },
      { drafts: { "../../token": "text" } },
      {
        progress: {
          "m02:v1": { updatedAt: 1, completed: "true", attempts: 0 },
        },
      },
      { drafts: { "mastery:draft:m02:v1": "x".repeat(32001) } },
    ])
      expect(BackupSchema.safeParse({ ...backup, ...patch }).success).toBe(
        false,
      );
  });
});
describe("retrieval workbench", () => {
  it("does not emit redundant trailing chunks", () => {
    expect(chunks("a b c d", 3, 2)).toEqual(["a b c", "b c d"]);
    expect(chunks(" ", 3, 1)).toEqual([]);
    expect(() => chunks("a", 2, 2)).toThrow();
  });
  it("distinguishes recall from reciprocal rank and deduplicates before cutoff", () => {
    expect(metrics([["x", "x", "a"]], [["a", "b"]], 2)).toEqual({
      recall: 0.5,
      mrr: 0.5,
    });
    expect(metrics([], [], 2)).toEqual({ recall: 0, mrr: 0 });
    expect(metrics([["a"], ["a"]], [[], ["a"]], 1)).toEqual({
      recall: 0.5,
      mrr: 0.5,
    });
  });
  it("fuses independent ranks and resolves exact ties reproducibly", () => {
    expect(
      fuse(
        [
          ["a", "b"],
          ["b", "c"],
        ],
        [1, 1],
        1,
      ),
    ).toEqual(["b", "a", "c"]);
    expect(fuse([["b"], ["a"]], [1, 1])).toEqual(["a", "b"]);
    expect(fuse([["a"], ["b"]], [0, 1])).toEqual(["b", "a"]);
  });
  it("computes score changes from the selected experiment", () => {
    const one = evaluateProject(1, 1),
      all = evaluateProject(6, 1);
    expect(all.vector.recall).toBe(1);
    expect(one.vector.recall).toBeLessThan(all.vector.recall);
    expect(
      evaluateProject(1, 0).rows.every(
        (row) => row.hybrid[0] === row.lexical[0],
      ),
    ).toBe(true);
    expect(() => evaluateProject(0, 0.5)).toThrow();
  });
});
describe("content capacity", () => {
  it("accepts 2,000 distinct IDs and validates their prerequisite graph", async () => {
    const [entry] = await loadContent();
    const items = Array.from({ length: 2000 }, (_, i) =>
      ProblemSchema.parse({
        ...entry.problem,
        id: `m${String(i + 1).padStart(2, "0")}`,
        slug: `capacity-${i}`,
        prerequisites: i ? [`m${String(i).padStart(2, "0")}`] : [],
      }),
    );
    expect(() => validateCatalog(items)).not.toThrow();
  });
});
