import dataset from "../../../../content/projects/mini-retrieval/dataset.json";
export { dataset };
export function cosine(a: number[], b: number[]) {
  const norm = (x: number[]) => Math.hypot(...x);
  const denominator = norm(a) * norm(b);
  return denominator ? a.reduce((n, x, i) => n + x * b[i], 0) / denominator : 0;
}
export function chunks(text: string, size: number, overlap: number) {
  if (
    !Number.isInteger(size) ||
    size < 1 ||
    !Number.isInteger(overlap) ||
    overlap < 0 ||
    overlap >= size
  )
    throw new Error("Invalid chunk settings");
  const words = text.trim().split(/\s+/).filter(Boolean),
    result: string[] = [];
  for (let i = 0; i < words.length; i += size - overlap) {
    result.push(words.slice(i, i + size).join(" "));
    if (i + size >= words.length) break;
  }
  return result;
}
export function metrics(rankings: string[][], relevant: string[][], k: number) {
  let recall = 0,
    mrr = 0;
  rankings.forEach((ranking, i) => {
    const labels = new Set(relevant[i]),
      top = [...new Set(ranking)].slice(0, k);
    if (labels.size) {
      recall += top.filter((id) => labels.has(id)).length / labels.size;
      const rank = top.findIndex((id) => labels.has(id));
      mrr += rank >= 0 ? 1 / (rank + 1) : 0;
    }
  });
  return {
    recall: rankings.length ? recall / rankings.length : 0,
    mrr: rankings.length ? mrr / rankings.length : 0,
  };
}
export function fuse(rankings: string[][], weights: number[], constant = 60) {
  const scores = new Map<string, number>();
  rankings.forEach((ranking, i) =>
    [...new Set(ranking)].forEach((id, rank) =>
      scores.set(
        id,
        (scores.get(id) ?? 0) + weights[i] / (constant + rank + 1),
      ),
    ),
  );
  return [...scores.keys()].sort(
    (a, b) => scores.get(b)! - scores.get(a)! || (a < b ? -1 : a > b ? 1 : 0),
  );
}
const stop = new Set(
  "a an the to and or how do i can on in of its is with before those when".split(
    " ",
  ),
);
export const retrievalTokenizer = {
  pattern: "[a-z]+",
  lowercase: true,
  stopWords: [...stop],
  queryTerms: "distinct",
  stemming: false,
} as const;
export const tokenize = (text: string) =>
  (text.toLowerCase().match(/[a-z]+/g) ?? []).filter((word) => !stop.has(word));
const byId = (a: string, b: string) => (a < b ? -1 : a > b ? 1 : 0);
export type RetrievalMethod = "vector" | "lexical" | "bm25" | "hybrid";
export type LexicalMethod = "lexical" | "bm25";
export const methodLabels: Record<RetrievalMethod, string> = {
  vector: "Vector",
  lexical: "Keyword",
  bm25: "BM25",
  hybrid: "Hybrid",
};
export const retrievalMethods = [
  "vector",
  "lexical",
  "bm25",
  "hybrid",
] as const;

/** Positive IDF and the conventional (k1 + 1) numerator, as in E09. */
export function bm25(
  documents: { id: string; text: string }[],
  query: string,
  k1 = 1.2,
  b = 0.75,
) {
  if (!Number.isFinite(k1) || k1 <= 0 || !Number.isFinite(b) || b < 0 || b > 1)
    throw new Error("Invalid BM25 settings");
  if (new Set(documents.map((doc) => doc.id)).size !== documents.length)
    throw new Error("Document IDs must be unique");
  const corpus = documents.map((doc) => tokenize(doc.text));
  const averageLength = corpus.length
    ? corpus.reduce((total, terms) => total + terms.length, 0) / corpus.length
    : 0;
  const terms = [...new Set(tokenize(query))].sort();
  const frequencies = terms.map(
    (term) => corpus.filter((doc) => doc.includes(term)).length,
  );
  return {
    averageLength,
    documentCount: documents.length,
    terms,
    documents: documents.map((doc, index) => {
      const length = corpus[index].length;
      const contributions = terms.map((term, i) => {
        const frequency = corpus[index].filter((word) => word === term).length;
        const documentFrequency = frequencies[i];
        const idf = Math.log(
          1 +
            (documents.length - documentFrequency + 0.5) /
              (documentFrequency + 0.5),
        );
        const normalization =
          1 - b + b * (averageLength ? length / averageLength : 0);
        const score = frequency
          ? (idf * frequency * (k1 + 1)) / (frequency + k1 * normalization)
          : 0;
        return { term, frequency, documentFrequency, idf, score };
      });
      return {
        id: doc.id,
        length,
        score: contributions.reduce((sum, term) => sum + term.score, 0),
        contributions,
      };
    }),
  };
}

/** Consume whole documents in rank order, skipping those that do not fit. */
export function selectEvidence(
  documents: { id: string; title: string; text: string }[],
  ranking: string[],
  budget: number,
) {
  if (!Number.isSafeInteger(budget) || budget < 0)
    throw new Error("Budget must be a non-negative integer");
  const lookup = new Map(documents.map((doc) => [doc.id, doc]));
  if (lookup.size !== documents.length)
    throw new Error("Document IDs must be unique");
  let used = 0;
  const decisions = [...new Set(ranking)].map((id, index) => {
    const doc = lookup.get(id);
    if (!doc) throw new Error(`Unknown document: ${id}`);
    const words = doc.text.trim().split(/\s+/).filter(Boolean).length;
    const included = words > 0 && used + words <= budget;
    if (included) used += words;
    return {
      ...doc,
      rank: index + 1,
      words,
      included,
      reason: included ? "included" : words ? "over-budget" : "empty",
      remaining: budget - used,
    };
  });
  const selected = decisions.filter((doc) => doc.included);
  return {
    budget,
    unit: "whitespace-separated source words; source labels excluded",
    policy: "rank-order greedy; skip oversized documents; no truncation",
    used,
    remaining: budget - used,
    selectedIds: selected.map((doc) => doc.id),
    decisions,
    context: selected.map((doc) => `[${doc.id}] ${doc.text}`).join("\n\n"),
  };
}

export function evaluateProject(
  k: number,
  vectorWeight: number,
  lexicalMethod: LexicalMethod = "lexical",
  k1 = 1.2,
  b = 0.75,
) {
  if (
    !Number.isInteger(k) ||
    k < 1 ||
    k > dataset.documents.length ||
    !Number.isFinite(vectorWeight) ||
    vectorWeight < 0 ||
    vectorWeight > 1 ||
    !["lexical", "bm25"].includes(lexicalMethod)
  )
    throw new Error("Invalid experiment settings");
  const rows = dataset.queries.map((query) => {
    const terms = new Set(tokenize(query.text));
    const explanation = bm25(dataset.documents, query.text, k1, b);
    const scores = dataset.documents.map((document, i) => ({
      id: document.id,
      vector: cosine(query.vector, document.vector),
      lexical: [...new Set(tokenize(document.text))].filter((term) =>
        terms.has(term),
      ).length,
      bm25: explanation.documents[i].score,
    }));
    const rank = (field: "vector" | "lexical" | "bm25") =>
      [...scores]
        .sort((a, b) => b[field] - a[field] || byId(a.id, b.id))
        .map((row) => row.id);
    const vector = rank("vector"),
      lexical = rank("lexical"),
      bm25Ranking = rank("bm25"),
      hybrid = fuse(
        [vector, lexicalMethod === "bm25" ? bm25Ranking : lexical],
        [vectorWeight, 1 - vectorWeight],
      );
    return {
      query: query.id,
      vector,
      lexical,
      bm25: bm25Ranking,
      hybrid,
      scores,
      explanation,
    };
  });
  const labels = dataset.queries.map((query) => query.relevant);
  return {
    datasetVersion: dataset.version,
    k,
    vectorWeight,
    lexicalMethod,
    bm25Settings: {
      k1,
      b,
      idf: "log(1 + (N - df + 0.5) / (df + 0.5))",
      numerator: "tf * (k1 + 1)",
    },
    tokenizer: retrievalTokenizer,
    rankConstant: 60,
    rows,
    vector: metrics(
      rows.map((row) => row.vector),
      labels,
      k,
    ),
    lexical: metrics(
      rows.map((row) => row.lexical),
      labels,
      k,
    ),
    hybrid: metrics(
      rows.map((row) => row.hybrid),
      labels,
      k,
    ),
    bm25: metrics(
      rows.map((row) => row.bm25),
      labels,
      k,
    ),
  };
}
