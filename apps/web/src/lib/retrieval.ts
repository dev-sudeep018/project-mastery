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
const tokens = (text: string) =>
  new Set(
    (text.toLowerCase().match(/[a-z]+/g) ?? []).filter(
      (word) => !stop.has(word),
    ),
  );
export function evaluateProject(k: number, vectorWeight: number) {
  if (
    !Number.isInteger(k) ||
    k < 1 ||
    k > dataset.documents.length ||
    !Number.isFinite(vectorWeight) ||
    vectorWeight < 0 ||
    vectorWeight > 1
  )
    throw new Error("Invalid experiment settings");
  const rows = dataset.queries.map((query) => {
    const terms = tokens(query.text);
    const scores = dataset.documents.map((document) => ({
      id: document.id,
      vector: cosine(query.vector, document.vector),
      lexical: [...tokens(document.text)].filter((term) => terms.has(term))
        .length,
    }));
    const rank = (field: "vector" | "lexical") =>
      [...scores]
        .sort((a, b) => b[field] - a[field] || (a.id < b.id ? -1 : 1))
        .map((row) => row.id);
    const vector = rank("vector"),
      lexical = rank("lexical"),
      hybrid = fuse([vector, lexical], [vectorWeight, 1 - vectorWeight]);
    return { query: query.id, vector, lexical, hybrid, scores };
  });
  const labels = dataset.queries.map((query) => query.relevant);
  return {
    datasetVersion: dataset.version,
    k,
    vectorWeight,
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
  };
}
