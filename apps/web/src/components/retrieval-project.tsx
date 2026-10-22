"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { ArrowRight, ChevronRight, Download } from "lucide-react";
import { dataset, chunks, evaluateProject } from "@/lib/retrieval";
import { itemHref } from "@/lib/curriculum";
import { downloadJson } from "./learning";

const NOTES_KEY = "mastery:project:mini-retrieval:v1";
export function RetrievalProject() {
  const [k, setK] = useState(2),
    [weight, setWeight] = useState(0.5),
    [query, setQuery] = useState(0);
  const [size, setSize] = useState(16),
    [overlap, setOverlap] = useState(4);
  const [notes, setNotes] = useState(""),
    [hydrated, setHydrated] = useState(false),
    [notice, setNotice] = useState("");
  const [noticeTone, setNoticeTone] = useState("info");
  const report = evaluateProject(k, weight),
    selected = report.rows[query];
  useEffect(() => {
    try {
      const saved = localStorage.getItem(NOTES_KEY);
      if (saved && saved.length <= 8000) setNotes(saved);
    } catch {
      setNoticeTone("warning");
      setNotice("Storage is unavailable. Export your report before leaving.");
    }
    setHydrated(true);
  }, []);
  useEffect(() => {
    if (!hydrated) return;
    try {
      localStorage.setItem(NOTES_KEY, notes);
    } catch {
      setNoticeTone("warning");
      setNotice("Could not save notes. Export your report before leaving.");
    }
  }, [notes, hydrated]);
  return (
    <>
      <h1>Build a small retrieval system.</h1>
      <p className="page-lead">
        Turn a collection of documents into ranked evidence. Investigate a
        baseline, combine retrieval methods, and explain what improved—or did
        not.
      </p>
      <div className="project-start">
        <p>
          Six original documents. Four labelled queries. No API key. The vectors
          are manually assigned teaching data, so the experiment makes no claim
          about real embedding-model quality.
        </p>
        <Link className="primary" href="/problems/retrieval-pipeline/">
          Build the Python pipeline
          <ArrowRight size={16} />
        </Link>
      </div>
      <section className="project-section">
        <h2>1. Inspect the material</h2>
        <p>
          Chunk boundaries affect the passages an index would store. This
          workbench ranks whole documents with supplied vectors; changing the
          chunk controls below previews preprocessing and does not re-embed or
          change the ranking.
        </p>
        <div className="experiment-controls">
          <label>
            Words per chunk: {size}
            <input
              aria-label="Project chunk size"
              type="range"
              min="8"
              max="32"
              value={size}
              onChange={(e) => {
                const n = Number(e.target.value);
                setSize(n);
                setOverlap(Math.min(overlap, n - 1));
              }}
            />
          </label>
          <label>
            Overlap: {overlap}
            <input
              aria-label="Project overlap"
              type="range"
              min="0"
              max={size - 1}
              value={overlap}
              onChange={(e) => setOverlap(Number(e.target.value))}
            />
          </label>
        </div>
        <div className="document-list">
          {dataset.documents.map((doc) => (
            <details key={doc.id}>
              <summary>
                <ChevronRight size={16} />
                {doc.title}
                <span className="muted small">
                  {chunks(doc.text, size, overlap).length} chunks
                </span>
              </summary>
              <p>{doc.text}</p>
              <p className="small muted">
                Teaching vector: [{doc.vector.join(", ")}]
              </p>
              <ol className="chunk-list">
                {chunks(doc.text, size, overlap).map((chunk, i) => (
                  <li key={i}>{chunk}</li>
                ))}
              </ol>
            </details>
          ))}
        </div>
        <Link className="text-link" href={itemHref("e01")}>
          Build the chunking operation
          <ArrowRight size={15} />
        </Link>
      </section>
      <section className="project-section">
        <h2>2. Compare retrieval methods</h2>
        <p>
          Vector search uses cosine similarity. The keyword baseline counts
          distinct shared words after removing a small fixed stop-word list.
          Hybrid search uses reciprocal rank fusion with constant 60. Equal
          scores use document ID order.
        </p>
        <div className="experiment-controls">
          <label>
            Results per query: {k}
            <input
              aria-label="Results per query"
              type="range"
              min="1"
              max="6"
              value={k}
              onChange={(e) => setK(Number(e.target.value))}
            />
          </label>
          <label>
            Vector weight: {weight.toFixed(1)} · keyword:{" "}
            {(1 - weight).toFixed(1)}
            <input
              aria-label="Vector weight"
              type="range"
              min="0"
              max="1"
              step=".1"
              value={weight}
              onChange={(e) => setWeight(Number(e.target.value))}
            />
          </label>
        </div>
        <div className="table-scroll">
          <table>
            <caption>Mean scores across all four teaching queries</caption>
            <thead>
              <tr>
                <th>Method</th>
                <th>Recall@{k}</th>
                <th>MRR@{k}</th>
              </tr>
            </thead>
            <tbody>
              {(["vector", "lexical", "hybrid"] as const).map((method) => (
                <tr key={method}>
                  <th>
                    {method === "lexical"
                      ? "Keyword"
                      : method === "vector"
                        ? "Vector"
                        : "Hybrid"}
                  </th>
                  <td>{report[method].recall.toFixed(3)}</td>
                  <td>{report[method].mrr.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <label className="query-select">
          Inspect a query
          <select
            value={query}
            onChange={(e) => setQuery(Number(e.target.value))}
          >
            {dataset.queries.map((q, i) => (
              <option value={i} key={q.id}>
                {q.text}
              </option>
            ))}
          </select>
        </label>
        <p className="muted small">
          Relevant IDs: {dataset.queries[query].relevant.join(", ")}. Relevance
          is a fixed teaching label, not an automatic judgement.
        </p>
        <div className="rank-comparison">
          {(["vector", "lexical", "hybrid"] as const).map((method) => (
            <div key={method}>
              <h3>
                {method === "lexical"
                  ? "Keyword"
                  : method === "vector"
                    ? "Vector"
                    : "Hybrid"}
              </h3>
              <ol>
                {selected[method].slice(0, k).map((id) => (
                  <li key={id}>
                    <span>
                      {dataset.documents.find((doc) => doc.id === id)?.title}
                    </span>
                    {dataset.queries[query].relevant.includes(id) && (
                      <span className="relevant-label">Relevant</span>
                    )}
                  </li>
                ))}
              </ol>
            </div>
          ))}
        </div>
        <div className="button-row">
          <Link className="text-link" href={itemHref("e02")}>
            Implement retrieval
          </Link>
          <Link className="text-link" href={itemHref("e03")}>
            Understand the metrics
          </Link>
          <Link className="text-link" href={itemHref("e04")}>
            Build rank fusion
          </Link>
        </div>
      </section>
      <section className="project-section">
        <h2>3. Record the evidence</h2>
        <p>
          Which query changed when you adjusted the weights? Did recall and MRR
          tell the same story? What would you need to test before trusting this
          on a larger collection?
        </p>
        <label className="reflection-label">
          Your findings
          <textarea
            maxLength={8000}
            rows={6}
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Record a prediction, an observation, and a limitation…"
            disabled={!hydrated}
          />
        </label>
        <div className="button-row">
          <button
            className="primary"
            onClick={() => {
              downloadJson("mini-retrieval-report.json", {
                format: "project-mastery-retrieval-report",
                version: 1,
                provenance: dataset.provenance,
                experiment: report,
                preprocessing: {
                  size,
                  overlap,
                  scope: "preview-only; rankings use whole-document vectors",
                },
                findings: notes,
              });
              setNoticeTone("success");
              setNotice(
                "Report exported with the current settings, rankings, metrics, and findings.",
              );
            }}
          >
            <Download size={16} />
            Export experiment report
          </button>
          <button
            className="secondary"
            onClick={() => downloadJson("mini-retrieval-dataset.json", dataset)}
          >
            Download dataset
          </button>
        </div>
        <p role="status" className={`${noticeTone}-text`}>
          {notice}
        </p>
        <p className="muted small">
          The workbench calculates its reference results in your browser.
          Implement the Python pipeline to check your own ranking, fusion, and
          evaluation code.
        </p>
      </section>
    </>
  );
}
