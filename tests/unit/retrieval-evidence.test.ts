import { describe, expect, it } from "vitest";
import {
  bm25,
  dataset,
  evaluateProject,
  selectEvidence,
  tokenize,
} from "../../apps/web/src/lib/retrieval";

describe("inspectable BM25", () => {
  it("uses lowercase English terms, fixed stop words, and no stemming", () => {
    expect(tokenize("The DOCUMENT, documents; 42 vector-vector!")).toEqual([
      "document",
      "documents",
      "vector",
      "vector",
    ]);
  });
  it("matches hand-calculated saturation, IDF, and length normalization", () => {
    const result = bm25(
      [
        { id: "a", text: "cat cat dog" },
        { id: "b", text: "dog" },
      ],
      "cat cat missing",
      1,
      1,
    );
    // Average length 2; cat appears in 1/2 documents. Duplicate query terms count once.
    expect(result.averageLength).toBe(2);
    expect(result.documents[0].score).toBeCloseTo((Math.log(2) * 4) / 3.5, 12);
    expect(result.documents[1].score).toBe(0);
    expect(result.documents[0].contributions).toEqual([
      {
        term: "cat",
        frequency: 2,
        documentFrequency: 1,
        idf: Math.log(2),
        score: expect.closeTo((Math.log(2) * 4) / 3.5, 12),
      },
      {
        term: "missing",
        frequency: 0,
        documentFrequency: 0,
        idf: Math.log(6),
        score: 0,
      },
    ]);
  });
  it("includes empty documents in the mean and handles an entirely empty index", () => {
    const result = bm25(
      [
        { id: "a", text: "cat" },
        { id: "b", text: "the" },
      ],
      "cat",
      1,
      1,
    );
    expect(result.averageLength).toBe(0.5);
    expect(result.documents[0].score).toBeCloseTo((Math.log(2) * 2) / 3, 12);
    expect(bm25([{ id: "a", text: "" }], "cat").documents[0].score).toBe(0);
    expect(bm25([], "cat").documents).toEqual([]);
    expect(
      bm25([{ id: "a", text: "cat" }], "the").documents[0].contributions,
    ).toEqual([]);
  });
  it("disables length normalization at b=0 without disabling frequency saturation", () => {
    const docs = [
      { id: "a", text: "cat" },
      { id: "b", text: "cat dog dog dog" },
    ];
    const unnormalized = bm25(docs, "cat", 1.2, 0).documents;
    expect(unnormalized[0].score).toBeCloseTo(unnormalized[1].score, 12);
    const normalized = bm25(docs, "cat", 1.2, 1).documents;
    expect(normalized[0].score).toBeGreaterThan(normalized[1].score);
  });
  it("rejects nonfinite or out-of-range settings and duplicate identities", () => {
    for (const [k1, b] of [
      [0, 0.75],
      [-1, 0.75],
      [Infinity, 0.75],
      [1, NaN],
      [1, -0.1],
      [1, 1.1],
    ])
      expect(() => bm25([], "cat", k1, b)).toThrow();
    expect(() =>
      bm25(
        [
          { id: "a", text: "" },
          { id: "a", text: "cat" },
        ],
        "cat",
      ),
    ).toThrow();
  });
  it("keeps score explanations, metrics and hybrid ranks consistent", () => {
    const report = evaluateProject(6, 0, "bm25");
    expect(report.bm25.recall).toBe(1);
    for (const row of report.rows) {
      expect(row.hybrid).toEqual(row.bm25);
      for (const score of row.scores) {
        const explanation = row.explanation.documents.find(
          (doc) => doc.id === score.id,
        )!;
        expect(score.bm25).toBe(
          explanation.contributions.reduce((sum, term) => sum + term.score, 0),
        );
      }
      const zeros = row.scores
        .filter((doc) => doc.bm25 === 0)
        .map((doc) => doc.id)
        .sort();
      expect(row.bm25.filter((id) => zeros.includes(id))).toEqual(zeros);
    }
    expect(
      evaluateProject(2, 1, "bm25").rows.every(
        (row) => row.hybrid.join() === row.vector.join(),
      ),
    ).toBe(true);
    expect(report.rows[1].bm25[0]).toBe("hybrid");
    expect(
      evaluateProject(2, 0, "lexical").rows.every(
        (row) => row.hybrid.join() === row.lexical.join(),
      ),
    ).toBe(true);
  });
});

describe("evidence selection", () => {
  const docs = [
    { id: "long", title: "Long", text: "one two three four five" },
    { id: "short", title: "Short", text: "six\nseven" },
    { id: "last", title: "Last", text: "eight" },
    { id: "empty", title: "Empty", text: "  " },
  ];
  it("skips oversized documents, continues down the ranking, and includes exact fits", () => {
    const result = selectEvidence(docs, ["long", "short", "last"], 3);
    expect(result.selectedIds).toEqual(["short", "last"]);
    expect(result.used).toBe(3);
    expect(result.remaining).toBe(0);
    expect(result.decisions.map((doc) => doc.remaining)).toEqual([3, 1, 0]);
    expect(result.context).toBe("[short] six\nseven\n\n[last] eight");
    expect(result.decisions[0].reason).toBe("over-budget");
  });
  it("keeps ranking order, never duplicates sources, and does not select empty text", () => {
    expect(
      selectEvidence(docs, ["last", "last", "empty", "short"], 10).selectedIds,
    ).toEqual(["last", "short"]);
    expect(selectEvidence(docs, ["empty"], 0).decisions[0].reason).toBe(
      "empty",
    );
    expect(selectEvidence(docs, ["long", "short"], 0).context).toBe("");
    expect(selectEvidence(docs, [], 10).remaining).toBe(10);
  });
  it("never exceeds a budget over every teaching query, method and cutoff", () => {
    for (const row of evaluateProject(6, 0.5, "bm25").rows)
      for (const method of ["lexical", "vector", "bm25", "hybrid"] as const)
        for (let k = 1; k <= 6; k++)
          for (let budget = 0; budget <= 220; budget++) {
            const result = selectEvidence(
              dataset.documents,
              row[method].slice(0, k),
              budget,
            );
            expect(result.used).toBeLessThanOrEqual(budget);
            expect(result.used + result.remaining).toBe(budget);
            expect(result.used).toBe(
              result.decisions
                .filter((doc) => doc.included)
                .reduce((sum, doc) => sum + doc.words, 0),
            );
          }
  });
  it("rejects ambiguous or invalid inputs instead of silently dropping evidence", () => {
    for (const budget of [-1, 0.5, NaN, Infinity])
      expect(() => selectEvidence(docs, [], budget)).toThrow();
    expect(() => selectEvidence(docs, ["missing"], 10)).toThrow();
    expect(() => selectEvidence([docs[0], docs[0]], [], 10)).toThrow();
  });
});
