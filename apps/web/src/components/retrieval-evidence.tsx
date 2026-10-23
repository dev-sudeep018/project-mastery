"use client";
import Link from "next/link";
import { useState } from "react";
import { Check, CircleAlert } from "lucide-react";
import {
  dataset,
  methodLabels,
  retrievalMethods,
  retrievalTokenizer,
  type evaluateProject,
  type RetrievalMethod,
  type selectEvidence,
} from "@/lib/retrieval";
import { itemHref } from "@/lib/curriculum";

type Row = ReturnType<typeof evaluateProject>["rows"][number];

export function ScoreInspector({ row }: { row: Row }) {
  const [documentId, setDocumentId] = useState(row.bm25[0]);
  const score = row.explanation.documents.find((doc) => doc.id === documentId)!;
  return (
    <section className="project-section" aria-labelledby="score-heading">
      <h2 id="score-heading">3. Explain a BM25 score</h2>
      <p>
        BM25 rewards matching terms, with diminishing returns for repetition and
        an adjustment for document length. It uses the actual source text.
        Compare a highly ranked document with one that shares fewer query terms.
      </p>
      <p className="muted small">
        Query: {dataset.queries.find((query) => query.id === row.query)!.text}
      </p>
      <label className="query-select">
        Explain this document
        <select
          value={documentId}
          onChange={(e) => setDocumentId(e.target.value)}
        >
          {row.bm25.map((id, i) => (
            <option key={id} value={id}>
              {i + 1}. {dataset.documents.find((doc) => doc.id === id)!.title}
            </option>
          ))}
        </select>
      </label>
      <p className="score-summary">
        BM25 score <strong>{score.score.toFixed(4)}</strong> · {score.length}{" "}
        indexed terms · corpus average{" "}
        {row.explanation.averageLength.toFixed(2)}
      </p>
      <div
        className="table-scroll"
        role="region"
        aria-label="BM25 term contributions"
        tabIndex={0}
      >
        <table>
          <caption>
            Each distinct query term contributes to the total score.
          </caption>
          <thead>
            <tr>
              <th scope="col">Term</th>
              <th scope="col">Occurrences</th>
              <th scope="col">Documents containing term</th>
              <th scope="col">IDF</th>
              <th scope="col">Contribution</th>
            </tr>
          </thead>
          <tbody>
            {score.contributions.map((term) => (
              <tr key={term.term}>
                <th scope="row">{term.term}</th>
                <td>{term.frequency}</td>
                <td>
                  {term.documentFrequency} of {row.explanation.documentCount}
                </td>
                <td>{term.idf.toFixed(4)}</td>
                <td>{term.score.toFixed(4)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="score-table-hint muted small">
        Scroll the table horizontally to see each term’s contribution.
      </p>
      {score.score === 0 && (
        <p className="info-text">
          No query terms match this document. Its BM25 score is zero.
        </p>
      )}
      <details className="retrieval-conventions">
        <summary>How text becomes a score</summary>
        <p>
          Lowercase English letter sequences are counted; punctuation and digits
          separate terms. The fixed stop words below are removed. There is no
          stemming: “document” and “documents” are different terms. Query terms
          count once; repeated document terms increase term frequency.
        </p>
        <p className="small muted">
          Stop words: {retrievalTokenizer.stopWords.join(", ")}
        </p>
        <p className="retrieval-formula">
          IDF = ln(1 + (N − df + 0.5) / (df + 0.5))
        </p>
        <p className="retrieval-formula">
          Contribution = IDF × tf × (k₁ + 1) / (tf + k₁ × (1 − b + b × length /
          average length))
        </p>
        <p>
          N is the document count; df counts documents containing the term; tf
          counts occurrences in this document. Length counts indexed terms after
          stop-word removal. Displayed values are rounded; calculations use full
          precision.
        </p>
      </details>
      <div className="button-row">
        <Link className="text-link" href={itemHref("e08")}>
          Build document-term counts
        </Link>
        <Link className="text-link" href={itemHref("e09")}>
          Implement BM25 scoring
        </Link>
      </div>
    </section>
  );
}

export function EvidenceBuilder({
  evidence,
  method,
  setMethod,
  budget,
  setBudget,
  queryText,
  k,
}: {
  evidence: ReturnType<typeof selectEvidence>;
  method: RetrievalMethod;
  setMethod: (method: RetrievalMethod) => void;
  budget: number;
  setBudget: (budget: number) => void;
  queryText: string;
  k: number;
}) {
  return (
    <section className="project-section" aria-labelledby="evidence-heading">
      <h2 id="evidence-heading">4. Assemble the evidence</h2>
      <p>
        Use the first {k} results for “{queryText}”. Work through them in rank
        order, keeping whole documents that fit and skipping those that do not.
        This greedy policy can leave space unused; it does not find an optimal
        combination.
      </p>
      <div className="experiment-controls evidence-controls">
        <label className="query-select">
          Evidence ranking
          <select
            value={method}
            onChange={(e) => setMethod(e.target.value as RetrievalMethod)}
          >
            {retrievalMethods.map((key) => (
              <option value={key} key={key}>
                {methodLabels[key]}
              </option>
            ))}
          </select>
        </label>
        <label>
          Source-word budget: {budget}
          <input
            type="range"
            min="0"
            max="220"
            value={budget}
            aria-label="Source-word budget"
            onChange={(e) => setBudget(Number(e.target.value))}
          />
        </label>
      </div>
      <p className="muted small">
        Budget counts whitespace-separated words in the source text, before
        stop-word removal. Source labels are excluded. This is a teaching
        budget, not a model token limit. Chunk previews do not change these
        whole-document candidates.
      </p>
      <p className="evidence-summary" role="status">
        {evidence.selectedIds.length} documents selected · {evidence.used} /{" "}
        {budget} source words · {evidence.remaining} remaining
      </p>
      <ol className="evidence-decisions">
        {evidence.decisions.map((doc) => (
          <li key={doc.id}>
            <div>
              <strong>{doc.title}</strong>
              <span className="small muted">
                {doc.words} words · source [{doc.id}]
              </span>
            </div>
            <span className={doc.included ? "success-text" : "warning-text"}>
              {doc.included ? (
                <Check size={16} aria-hidden="true" />
              ) : (
                <CircleAlert size={16} aria-hidden="true" />
              )}
              {doc.included
                ? "Included"
                : doc.reason === "empty"
                  ? "Skipped: empty"
                  : "Skipped: exceeds remaining budget"}
            </span>
          </li>
        ))}
      </ol>
      <h3>Selected source text</h3>
      {evidence.selectedIds.length ? (
        <div className="evidence-context">
          {evidence.decisions
            .filter((doc) => doc.included)
            .map((doc) => (
              <div key={doc.id}>
                <h4>
                  [{doc.id}] {doc.title}
                </h4>
                <p>{doc.text}</p>
              </div>
            ))}
        </div>
      ) : (
        <p className="info-text">
          No documents fit. Increase the word budget or choose another ranking.
        </p>
      )}
      <p className="muted small">
        These are retrieved sources, not a generated answer. Inclusion does not
        prove relevance or factual correctness. The report exports this exact
        selection and every skip decision.
      </p>
      <Link className="text-link" href={itemHref("e13")}>
        Implement selection under a context budget
      </Link>
    </section>
  );
}
