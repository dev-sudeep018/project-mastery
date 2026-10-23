# Retrieval: from scores to evidence

The mini retrieval project connects the engineering lessons to a complete
investigation: inspect the original corpus, compare rankings, explain scores,
select source text, and export the evidence behind a finding. It runs locally in
the browser without a model service or API key. This extends the existing project;
it does not add to the published lesson count.

## An investigation to try

1. Choose “How do I combine keyword and vector search?” and retrieve one result.
   Compare the Vector, Keyword, BM25 and Hybrid rankings with the fixed relevance
   label. These vectors are manually assigned teaching data.
2. Set vector weight to zero, then one. Hybrid should reproduce the chosen text
   ranking at zero and the vector ranking at one. Switch its text method between
   Keyword and BM25 while keeping other settings fixed.
3. Inspect the `hybrid` document's BM25 score. Its repeated `search` term shows
   saturation. Change k₁ and b, and distinguish a changed score from a changed
   ranking. A score change need not improve recall or MRR.
4. Choose an evidence ranking, then reduce the source-word budget to zero. No
   source should be included. Increase the budget and inspect each inclusion and
   skip. The first k results are candidates; the selector does not reach beyond
   that cutoff to fill remaining space.
5. Record a prediction, an observation and a limitation, then export the report.
   Separate retrieval relevance from the correctness of a future generated answer.

The Python pipeline checkpoint P01 still accepts supplied text rankings, performs
cosine ranking and reciprocal rank fusion, and computes metrics. It does not
require implementing a tokenizer or BM25. E08 (document-term counts), E09 (BM25),
and E13 (context budgeting) provide the operations for extending that pipeline.
The project links those lessons at the point where they are used.

## Scoring and selection conventions

Keyword and BM25 both lowercase text, extract `[a-z]+` sequences, and remove the
same fixed stop-word list. There is no stemming or learned tokenizer. Keyword
counts distinct shared terms. BM25 counts document term frequencies, using each
distinct query term once. Empty documents contribute to average corpus length.

BM25 uses `ln(1 + (N - df + 0.5) / (df + 0.5))` and the conventional
`tf * (k1 + 1)` numerator, matching lesson E09. Defaults are k₁ = 1.2 and b = 0.75.
The [Apache Lucene BM25 reference](https://lucene.apache.org/core/9_12_1/core/org/apache/lucene/search/similarities/BM25Similarity.html)
documents the positive IDF and parameter meanings; this is an original teaching
implementation, not a Lucene compatibility layer. Term contributions sum to each
document's score. Scores are rounded only for display. Equal scores use document
ID order. Hybrid fuses full rankings with RRF constant 60 before applying k.

Evidence selection consumes the chosen top-k ranking in order. It includes a
whole document only when its source text fits, skips an oversized document, then
continues to the next candidate. Empty sources are skipped and duplicate IDs
count once. This is a greedy policy, not a knapsack optimizer.

The budget counts whitespace-separated **source words**, including stop words.
It excludes added source labels. It is deliberately distinct from BM25 indexed
terms and from model tokens. A model integration would need its actual tokenizer,
prompt overhead and output allowance. Chunk controls remain a preprocessing
preview; all four methods and the evidence selector operate on whole documents.

## Report format

`mini-retrieval-report.json` now uses format `project-mastery-retrieval-report`,
version **2**. It contains:

- The complete teaching dataset and provenance, including synthetic vectors and
  relevance labels.
- All four queries' rankings, raw scores, BM25 term explanations and mean metrics.
- k, vector weight, the hybrid text method, BM25 parameters, tokenizer conventions
  and RRF constant.
- The selected evidence query and method, word budget, each candidate's cost and
  decision, remaining budget after each decision, selected source IDs and exact
  context text.
- Chunk-preview settings with their scope, and the learner's findings.

Existing findings remain stored under the original notes key. Controls reset on
reload; export captures their current values. Reports are downloadable records,
not importable project backups. No external text or credentials are transmitted.

## Verification scope

Unit checks compare BM25 with independent hand calculations, cover empty corpora
and query terms, normalization, tie ordering, invalid inputs and hybrid weight
endpoints. Evidence checks cover exact fits, oversized skips, duplicate and empty
sources, and budget bounds across every teaching query, method and cutoff.

Browser tests exercise parameter-dependent score explanations, query changes,
zero/full budgets, source text, downloadable reproducible reports, narrow-screen
overflow, keyboard access to the score table and related lesson navigation.
See [the verification record](verification.md) for executed results and limits.
