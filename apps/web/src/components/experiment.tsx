"use client";
import { useState } from "react";

export function Experiment({
  itemId,
  compact = false,
}: {
  itemId: string;
  compact?: boolean;
}) {
  const [temperature, setTemperature] = useState(1);
  const [shift, setShift] = useState(0);
  const [angle, setAngle] = useState(45);
  const [step, setStep] = useState(-2);
  const [size, setSize] = useState(6);
  const [overlap, setOverlap] = useState(2);
  const kind = ["m01", "e02"].includes(itemId)
    ? "vectors"
    : ["m02", "m04", "d04"].includes(itemId)
      ? "softmax"
      : ["m03", "d01", "d02"].includes(itemId)
        ? "gradient"
        : itemId === "e01"
          ? "chunks"
          : null;
  if (!kind) return null;
  const logits = [1, 2, 3].map((x) => (x + shift) / temperature);
  const weights = logits.map((x) => Math.exp(x - Math.max(...logits)));
  const probabilities = weights.map(
    (x) => x / weights.reduce((a, b) => a + b, 0),
  );
  const h = 10 ** step;
  const derivative = ((2 + h) ** 3 - (2 - h) ** 3) / (2 * h);
  const words =
    "A retrieval system finds useful passages before a language model writes an answer using the evidence it found".split(
      " ",
    );
  const chunks: string[] = [];
  for (let start = 0; start < words.length; start += size - overlap) {
    chunks.push(words.slice(start, start + size).join(" "));
    if (start + size >= words.length) break;
  }
  return (
    <section
      className={`experiment ${compact ? "compact" : ""}`}
      aria-label="Interactive experiment"
    >
      <h3>
        {kind === "vectors"
          ? "Change the angle"
          : kind === "softmax"
            ? "Change the distribution"
            : kind === "gradient"
              ? "Try a gradient check"
              : "Move the chunk boundaries"}
      </h3>
      <p className="muted">
        Predict the change, move a control, then explain what you observe.
      </p>
      {kind === "vectors" && (
        <>
          <label>
            Angle between vectors: <output>{angle}°</output>
            <input
              aria-label="Angle between vectors"
              type="range"
              min="0"
              max="180"
              value={angle}
              onChange={(e) => setAngle(Number(e.target.value))}
            />
          </label>
          <svg
            className="vector-diagram"
            viewBox="0 0 300 160"
            role="img"
            aria-label={`Two unit vectors at ${angle} degrees, cosine similarity ${Math.cos((angle * Math.PI) / 180).toFixed(3)}`}
          >
            <path
              d="M20 140H280M150 150V10"
              fill="none"
              stroke="var(--border)"
            />
            <line
              x1="150"
              y1="140"
              x2="270"
              y2="140"
              stroke="var(--muted)"
              strokeWidth="3"
            />
            <line
              x1="150"
              y1="140"
              x2={150 + 120 * Math.cos((angle * Math.PI) / 180)}
              y2={140 - 120 * Math.sin((angle * Math.PI) / 180)}
              stroke="var(--accent)"
              strokeWidth="3"
            />
          </svg>
          <p>
            Cosine similarity{" "}
            <strong className="measurement">
              {Math.cos((angle * Math.PI) / 180).toFixed(3)}
            </strong>
          </p>
          <p className="small muted">
            Length stays fixed. Direction alone changes the score.
          </p>
        </>
      )}
      {kind === "softmax" && (
        <>
          <label>
            Temperature: <output>{temperature.toFixed(1)}</output>
            <input
              aria-label="Temperature"
              type="range"
              min=".2"
              max="4"
              step=".1"
              value={temperature}
              onChange={(e) => setTemperature(Number(e.target.value))}
            />
          </label>
          <label>
            Add to every score: <output>{shift}</output>
            <input
              aria-label="Score shift"
              type="range"
              min="0"
              max="1000"
              step="100"
              value={shift}
              onChange={(e) => setShift(Number(e.target.value))}
            />
          </label>
          <div className="probability-chart">
            {probabilities.map((p, i) => (
              <div key={i}>
                <span>{i + 1 + shift}</span>
                <div className="bar-track">
                  <i style={{ width: `${p * 100}%` }} />
                </div>
                <span>{(p * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
          <p className="small muted">
            Scores [1, 2, 3] use softmax(score / temperature). A shared shift
            preserves the probabilities; a lower temperature concentrates them.
          </p>
        </>
      )}
      {kind === "gradient" && (
        <>
          <label>
            Step size h: <output>{h.toExponential(0)}</output>
            <input
              aria-label="Derivative step exponent"
              type="range"
              min="-12"
              max="0"
              value={step}
              onChange={(e) => setStep(Number(e.target.value))}
            />
          </label>
          <p>
            For f(x) = x³ at x = 2, the exact derivative is <strong>12</strong>.
          </p>
          <dl className="experiment-values">
            <div>
              <dt>Central difference</dt>
              <dd>{derivative.toFixed(8)}</dd>
            </div>
            <div>
              <dt>Absolute error</dt>
              <dd>{Math.abs(derivative - 12).toExponential(3)}</dd>
            </div>
          </dl>
          <p className="small muted">
            Find the region with the smallest error. Why does shrinking the step
            eventually stop helping?
          </p>
        </>
      )}
      {kind === "chunks" && (
        <>
          <label>
            Words per chunk: <output>{size}</output>
            <input
              aria-label="Words per chunk"
              type="range"
              min="3"
              max="12"
              value={size}
              onChange={(e) => {
                const next = Number(e.target.value);
                setSize(next);
                setOverlap(Math.min(overlap, next - 1));
              }}
            />
          </label>
          <label>
            Overlap: <output>{overlap}</output>
            <input
              aria-label="Word overlap"
              type="range"
              min="0"
              max={size - 1}
              value={overlap}
              onChange={(e) => setOverlap(Number(e.target.value))}
            />
          </label>
          <ol className="chunk-list">
            {chunks.map((chunk, i) => (
              <li key={i}>{chunk}</li>
            ))}
          </ol>
          <p className="small muted">
            {chunks.length} chunks ·{" "}
            {chunks.reduce((n, c) => n + c.split(" ").length, 0)} indexed words
            from {words.length} source words. More overlap repeats more context.
          </p>
        </>
      )}
    </section>
  );
}
