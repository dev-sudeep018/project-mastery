"use client";
import dynamic from "next/dynamic";
import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import type { OnMount } from "@monaco-editor/react";
import {
  ArrowLeft,
  ArrowRight,
  Check,
  CheckCircle2,
  ChevronRight,
  Circle,
  Clock3,
  Code2,
  Copy,
  Expand,
  Lightbulb,
  LoaderCircle,
  Play,
  RotateCcw,
  ShieldCheck,
  Square,
  Terminal,
  XCircle,
} from "lucide-react";
import { MAX_SOURCE_LENGTH } from "@mastery/runner-protocol";
import data from "@/generated/problem.json";
import { DRAFT_KEY, PROGRESS_KEY, readDraft } from "@/lib/draft";
import { useRunner } from "@/lib/use-runner";
import { Shell } from "./shell";

const Editor = dynamic(() => import("./python-editor"), {
  ssr: false,
  loading: () => <div className="editor-loading">Loading code editor…</div>,
});
const resourceTabs = ["description", "hints", "solution"] as const;
const samples = [
  {
    name: "Ordinary scores",
    input: "[1.0, 2.0, 3.0]",
    output: "[0.090031, 0.244728, 0.665241]",
  },
  {
    name: "Large positive scores",
    input: "[1000.0, 1001.0, 1002.0]",
    output: "[0.090031, 0.244728, 0.665241]",
  },
  {
    name: "Equal scores",
    input: "[7.0, 7.0, 7.0, 7.0]",
    output: "[0.25, 0.25, 0.25, 0.25]",
  },
];
export function Workspace() {
  const [tab, setTab] = useState<"description" | "hints" | "solution">(
    "description",
  );
  const [code, setCode] = useState(data.starter);
  const [hydrated, setHydrated] = useState(false);
  const [saveState, setSaveState] = useState("Saved on this device");
  const [complete, setComplete] = useState(false);
  const [pendingReplacement, setPendingReplacement] = useState<
    "starter" | "reference" | null
  >(null);
  const [copied, setCopied] = useState(false);
  const [focus, setFocus] = useState(false);
  const [split, setSplit] = useState(44);
  const [mobileEditor, setMobileEditor] = useState(false);
  const runner = useRunner();
  const splitRef = useRef<HTMLDivElement>(null);
  const runRef = useRef<() => void>(() => {});
  const busy = runner.phase !== "idle";

  useEffect(() => {
    try {
      setCode(readDraft(localStorage.getItem(DRAFT_KEY), data.starter));
      setComplete(localStorage.getItem(PROGRESS_KEY) === "complete");
    } catch {
      setSaveState("Storage unavailable. Copy your code before leaving.");
    }
    setHydrated(true);
  }, []);
  useEffect(() => {
    if (!hydrated) return;
    if (code.length > MAX_SOURCE_LENGTH) {
      setSaveState("Draft too large to save. Copy your code before leaving.");
      return;
    }
    try {
      localStorage.setItem(DRAFT_KEY, JSON.stringify({ version: 1, code }));
      setSaveState("Saved on this device");
    } catch {
      setSaveState("Could not save. Copy your code before leaving.");
    }
  }, [code, hydrated]);
  useEffect(() => {
    if (runner.result?.status === "passed" && runner.mode === "all") {
      setComplete(true);
      try {
        localStorage.setItem(PROGRESS_KEY, "complete");
      } catch {
        /* Saving status is handled by the draft notice. */
      }
    }
  }, [runner.result, runner.mode]);
  const checkSolution = useCallback(() => {
    if (!busy && code.length <= MAX_SOURCE_LENGTH) runner.run(code, "all");
  }, [busy, code, runner]);
  useEffect(() => {
    runRef.current = checkSolution;
  }, [checkSolution]);
  useEffect(() => {
    const handle = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        event.preventDefault();
        runRef.current();
      }
      if (event.key === "Escape") setFocus(false);
    };
    addEventListener("keydown", handle);
    return () => removeEventListener("keydown", handle);
  }, []);
  const mountEditor: OnMount = (editor, monaco) => {
    monaco.editor.defineTheme("mastery", {
      base: "vs-dark",
      inherit: true,
      rules: [
        { token: "comment", foreground: "84988B", fontStyle: "italic" },
        { token: "keyword", foreground: "C4B5FD" },
        { token: "string", foreground: "B3D69B" },
        { token: "number", foreground: "E2BF88" },
      ],
      colors: {
        "editor.background": "#111715",
        "editor.foreground": "#DCE5DF",
        "editorLineNumber.foreground": "#667A6E",
        "editorLineNumber.activeForeground": "#C9D9CF",
        "editor.lineHighlightBackground": "#19221D",
        "editor.selectionBackground": "#294C3A",
        "editorCursor.foreground": "#9DDFB1",
        "editorIndentGuide.background1": "#27342C",
      },
    });
    monaco.editor.setTheme("mastery");
    editor.addAction({
      id: "mastery-check",
      label: "Check solution",
      keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter],
      run: () => runRef.current(),
    });
  };
  const passed = runner.result?.tests.filter((t) => t.passed).length ?? 0;
  function resize(clientX: number) {
    const box = splitRef.current?.getBoundingClientRect();
    if (box)
      setSplit(
        Math.min(62, Math.max(30, ((clientX - box.left) / box.width) * 100)),
      );
  }
  async function copyCode() {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      setSaveState("Copy unavailable. Select the code and press Ctrl+C.");
    }
  }

  return (
    <Shell workspace>
      <header className="topbar">
        <div className="breadcrumb">
          <Link href="/problems/">Practice</Link>
          <ChevronRight size={14} />
          <span>Foundations</span>
        </div>
        <span className="free-label">
          <ShieldCheck size={15} />
          Free & open source
        </span>
      </header>
      <div className="problem-header">
        <div>
          <Link className="back-link" href="/problems/">
            <ArrowLeft size={14} />
            All problems
          </Link>
          <h1>Numerically Stable Softmax</h1>
          <div className="problem-meta">
            <span className="difficulty">Beginner</span>
            <span>
              <Clock3 size={14} />
              20 min
            </span>
            <span>NumPy</span>
            <span className={complete ? "complete-label" : ""}>
              {complete ? (
                <>
                  <CheckCircle2 size={14} />
                  Completed on this device
                </>
              ) : (
                "M02 · Foundations"
              )}
            </span>
          </div>
        </div>
        <Link className="path-link" href="/paths/">
          Your learning path
          <ArrowRight size={16} />
        </Link>
      </div>
      <div className="mobile-switch" role="group" aria-label="Workspace view">
        <button
          className={!mobileEditor ? "selected" : ""}
          onClick={() => setMobileEditor(false)}
        >
          Read exercise
        </button>
        <button
          className={mobileEditor ? "selected" : ""}
          onClick={() => setMobileEditor(true)}
        >
          Write Python
        </button>
      </div>
      <div
        ref={splitRef}
        className={`workbench ${focus ? "editor-focused" : ""} ${mobileEditor ? "mobile-code" : ""}`}
        style={{ "--split": `${split}%` } as React.CSSProperties}
      >
        <section className="problem-panel" aria-label="Problem information">
          <div className="tabbar" role="tablist" aria-label="Problem resources">
            {resourceTabs.map((t, index) => (
              <button
                key={t}
                id={`tab-${t}`}
                role="tab"
                aria-selected={tab === t}
                aria-controls={`panel-${t}`}
                tabIndex={tab === t ? 0 : -1}
                onKeyDown={(event) => {
                  const next =
                    event.key === "Home"
                      ? 0
                      : event.key === "End"
                        ? resourceTabs.length - 1
                        : event.key === "ArrowRight"
                          ? (index + 1) % resourceTabs.length
                          : event.key === "ArrowLeft"
                            ? (index + resourceTabs.length - 1) %
                              resourceTabs.length
                            : null;
                  if (next === null) return;
                  event.preventDefault();
                  setTab(resourceTabs[next]);
                  document.getElementById(`tab-${resourceTabs[next]}`)?.focus();
                }}
                onClick={() => setTab(t)}
              >
                {t === "hints" && <Lightbulb size={15} />}
                {
                  {
                    description: "Description",
                    hints: "Hints",
                    solution: "Solution",
                  }[t]
                }
              </button>
            ))}
          </div>
          <div
            className="problem-content"
            role="tabpanel"
            id={`panel-${tab}`}
            aria-labelledby={`tab-${tab}`}
          >
            {tab === "description" && (
              <>
                <h2>Small function. Essential idea.</h2>
                <p>
                  Turn raw model scores into probabilities. Softmax sits at the
                  heart of classifiers and attention, but a direct
                  implementation can break on large numbers.
                </p>
                <h3>Your task</h3>
                <p>
                  Implement <code>softmax(x)</code> for a one-dimensional array
                  of finite numbers. Return a NumPy array of probabilities
                  without changing the input.
                </p>
                <div
                  className="formula"
                  aria-label="Softmax of x i equals exponential of x i minus max x, divided by the sum of exponential of x j minus max x"
                >
                  <span>
                    softmax(x)<sub>i</sub> ={" "}
                  </span>
                  <span className="fraction">
                    <span>
                      exp(x<sub>i</sub> − max(x))
                    </span>
                    <span>
                      Σ<sub>j</sub> exp(x<sub>j</sub> − max(x))
                    </span>
                  </span>
                </div>
                <h3>See it in numbers</h3>
                <div className="example-block">
                  <div>
                    <span>Input</span>
                    <code>[1.0, 2.0, 3.0]</code>
                  </div>
                  <div>
                    <span>Output</span>
                    <code>[0.090031, 0.244728, 0.665241]</code>
                  </div>
                  <div
                    className="probability-chart"
                    aria-label="Probability distribution: score 1 is 9.0 percent, score 2 is 24.5 percent, score 3 is 66.5 percent"
                  >
                    {[9, 24.5, 66.5].map((value, index) => (
                      <div key={value}>
                        <span>Score {index + 1}</span>
                        <div className="bar-track">
                          <i style={{ width: `${value}%` }} />
                        </div>
                        <span>{value}%</span>
                      </div>
                    ))}
                  </div>
                </div>
                <h3>The catch</h3>
                <p>
                  <code>[1000, 1001, 1002]</code> should give the same
                  probabilities. Directly computing <code>exp(1000)</code>{" "}
                  overflows. Subtracting the largest score keeps the calculation
                  stable.
                </p>
                <h3>Requirements</h3>
                <ul className="requirements">
                  <li>Accept a numeric list or a one-dimensional array.</li>
                  <li>Return finite, nonnegative values that sum to one.</li>
                  <li>
                    Raise <code>ValueError</code> for empty, non-finite, or
                    non-1D input.
                  </li>
                  <li>Leave the original input unchanged.</li>
                </ul>
                <p className="muted small">
                  Absolute tolerance: 1e-7 · Relative tolerance: 1e-6
                </p>
                <div className="knowledge">
                  <h3>Before you begin</h3>
                  <p>Python functions · NumPy arrays · Exponentials</p>
                </div>
              </>
            )}
            {tab === "hints" && (
              <>
                <h2>A nudge, when you need it.</h2>
                <p>
                  Open one hint at a time. Try the next step in your code before
                  continuing.
                </p>
                {[
                  [
                    "Start with the contract",
                    "Convert x with np.asarray(x, dtype=np.float64). Check x.ndim, x.size, and np.isfinite(x) before doing any math.",
                  ],
                  [
                    "Keep the exponentials small",
                    "Subtract np.max(x) from every score. This creates a new array and makes the largest shifted score zero.",
                  ],
                  [
                    "Normalize the weights",
                    "Compute np.exp(shifted), then divide by its sum. At least one weight is one, so the normalizer is positive.",
                  ],
                ].map(([title, body], i) => (
                  <details className="hint" key={title}>
                    <summary>
                      Hint {i + 1}: {title}
                    </summary>
                    <p>{body}</p>
                  </details>
                ))}
                <p className="muted small">
                  Extremely small probabilities may underflow to zero. That is
                  acceptable for this exercise.
                </p>
              </>
            )}
            {tab === "solution" && (
              <>
                <h2>Understand the reference.</h2>
                <p>
                  Compare the steps with your approach. The important idea is
                  subtracting the maximum before exponentiation.
                </p>
                <pre className="reference-code">{data.solution}</pre>
                <button
                  className="secondary"
                  onClick={() => {
                    setPendingReplacement("reference");
                    setMobileEditor(true);
                  }}
                >
                  <Code2 size={15} />
                  Use reference in editor
                </button>
                <h3>Why this works</h3>
                <p>
                  Subtracting one value from every score multiplies every
                  exponential by the same factor. That factor cancels during
                  normalization, so the probabilities stay the same.
                </p>
                <p className="muted small">
                  All evaluation tests are public. Completion is local practice
                  feedback.
                </p>
              </>
            )}
          </div>
        </section>
        <div
          className="resize-handle"
          role="separator"
          aria-label="Resize problem and code panels"
          aria-orientation="vertical"
          aria-valuenow={Math.round(split)}
          aria-valuemin={30}
          aria-valuemax={62}
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
              e.preventDefault();
              setSplit((s) =>
                Math.min(
                  62,
                  Math.max(30, s + (e.key === "ArrowRight" ? 2 : -2)),
                ),
              );
            }
          }}
          onPointerDown={(e) => {
            e.currentTarget.setPointerCapture(e.pointerId);
          }}
          onPointerMove={(e) => {
            if (e.currentTarget.hasPointerCapture(e.pointerId))
              resize(e.clientX);
          }}
          onPointerUp={(e) =>
            e.currentTarget.releasePointerCapture(e.pointerId)
          }
        >
          <span />
        </div>
        <section className="coding-panel" aria-label="Python workspace">
          <div className="editor-toolbar">
            <span className="filename">
              <Code2 size={16} />
              solution.py
            </span>
            <div>
              <span className="runtime-label">Python · NumPy</span>
              <button
                className="icon-button"
                aria-label={copied ? "Code copied" : "Copy code"}
                title="Copy code"
                onClick={copyCode}
              >
                {copied ? <Check size={16} /> : <Copy size={16} />}
              </button>
              <button
                className="icon-button"
                aria-label="Reset starter code"
                title="Reset starter code"
                onClick={() => setPendingReplacement("starter")}
              >
                <RotateCcw size={16} />
              </button>
              <button
                className="icon-button focus-button"
                aria-label={focus ? "Exit focus mode" : "Focus on editor"}
                title="Focus on editor"
                onClick={() => setFocus((f) => !f)}
              >
                <Expand size={16} />
              </button>
            </div>
          </div>
          {pendingReplacement && (
            <div className="inline-confirm" role="status">
              <span>
                Replace your current code with{" "}
                {pendingReplacement === "reference"
                  ? "the reference solution"
                  : "the starter"}
                ?
              </span>
              <button
                onClick={() => {
                  setCode(
                    pendingReplacement === "reference"
                      ? data.solution
                      : data.starter,
                  );
                  setPendingReplacement(null);
                }}
              >
                Replace code
              </button>
              <button onClick={() => setPendingReplacement(null)}>
                Keep my code
              </button>
            </div>
          )}
          <div className="editor-container">
            {hydrated && (
              <Editor
                height="100%"
                language="python"
                path="solution.py"
                value={code}
                onChange={(value) => {
                  setCode(value ?? "");
                  setSaveState("Saving…");
                }}
                onMount={mountEditor}
                theme="vs-dark"
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                  lineHeight: 24,
                  fontFamily: 'Consolas, "Liberation Mono", monospace',
                  padding: { top: 20, bottom: 20 },
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                  tabSize: 4,
                  wordWrap: "on",
                  renderLineHighlight: "line",
                  lineNumbersMinChars: 3,
                  glyphMargin: false,
                  folding: false,
                  ariaLabel: "Python code editor",
                  accessibilitySupport: "on",
                }}
              />
            )}
          </div>
          <div className="editor-status">
            <span>{saveState}</span>
            <span>
              UTF-8<span className="status-divider">·</span>4 spaces
            </span>
          </div>
          <div className="run-toolbar">
            <span className="shortcut">
              <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to check
            </span>
            <div>
              {busy ? (
                <button className="secondary" onClick={runner.cancel}>
                  <Square size={13} />
                  Stop run
                </button>
              ) : (
                <button
                  className="secondary"
                  disabled={!runner.ready || code.length > MAX_SOURCE_LENGTH}
                  onClick={() => runner.run(code, "sample")}
                >
                  <Play size={14} />
                  Run examples
                </button>
              )}
              <button
                className="primary"
                disabled={
                  !runner.ready || busy || code.length > MAX_SOURCE_LENGTH
                }
                onClick={checkSolution}
              >
                {busy ? (
                  <LoaderCircle className="spin" size={16} />
                ) : (
                  <Check size={17} />
                )}
                Check solution
              </button>
            </div>
          </div>
          {code.length > MAX_SOURCE_LENGTH && (
            <p className="error-notice" role="alert">
              Code exceeds 32,000 characters. Shorten it before running.
            </p>
          )}
          <div className="results-panel">
            <div className="results-heading">
              <span>
                <Terminal size={16} />
                Test results
              </span>
              <span
                className={
                  runner.result?.status === "passed" ? "success-text" : "muted"
                }
                aria-live="polite"
              >
                {busy
                  ? runner.phase === "loading"
                    ? "Loading Python…"
                    : "Running tests…"
                  : runner.result
                    ? `${passed}/${runner.result.tests.length} passed`
                    : "Ready for your first run"}
              </span>
            </div>
            <div
              className="results-body"
              aria-live="polite"
              aria-atomic="false"
            >
              {runner.connectionError ? (
                <div className="run-notice error">
                  <XCircle size={20} />
                  <div>
                    <strong>Runner unavailable</strong>
                    <p>{runner.connectionError}</p>
                    <button className="secondary" onClick={runner.reconnect}>
                      Reconnect
                    </button>
                  </div>
                </div>
              ) : busy ? (
                <div className="run-notice">
                  <LoaderCircle className="spin" size={22} />
                  <div>
                    <strong>
                      {runner.phase === "loading"
                        ? "Preparing Python and NumPy"
                        : "Checking your implementation"}
                    </strong>
                    <p>
                      {runner.phase === "loading"
                        ? "The first run takes a little longer. Your code stays on this device."
                        : "Each run uses a fresh Python environment."}
                    </p>
                  </div>
                </div>
              ) : runner.result ? (
                <>
                  <div
                    className={`result-summary ${runner.result.status === "passed" ? "success" : "failure"}`}
                  >
                    {runner.result.status === "passed" ? (
                      <CheckCircle2 size={19} />
                    ) : (
                      <XCircle size={19} />
                    )}
                    <div>
                      <strong>
                        {runner.result.status === "passed"
                          ? runner.mode === "all"
                            ? "All checks passed. Nicely done."
                            : "Examples passed. Try the full checks next."
                          : runner.result.status === "timeout"
                            ? "Time limit reached"
                            : runner.result.status === "cancelled"
                              ? "Run stopped"
                              : runner.result.status === "error"
                                ? "Python needs a fix"
                                : "Keep going. Here’s what to check."}
                      </strong>
                      <span>
                        {runner.result.durationMs} ms ·{" "}
                        {runner.mode === "all"
                          ? "Full public test suite"
                          : "Example tests"}
                      </span>
                    </div>
                  </div>
                  {runner.result.error && (
                    <pre className="error-output">{runner.result.error}</pre>
                  )}
                  {runner.result.tests.map((test) => (
                    <details
                      className={`test-row ${test.passed ? "passed" : "failed"}`}
                      key={test.name}
                    >
                      <summary>
                        {test.passed ? (
                          <CheckCircle2 size={15} />
                        ) : (
                          <XCircle size={15} />
                        )}
                        <span>{test.name}</span>
                        <span>{test.passed ? "Passed" : "Failed"}</span>
                        <ChevronRight size={13} />
                      </summary>
                      <p>{test.message}</p>
                    </details>
                  ))}
                  {runner.result.output && (
                    <>
                      <h3 className="output-label">Console output</h3>
                      <pre className="console-output">
                        {runner.result.output}
                      </pre>
                    </>
                  )}
                </>
              ) : (
                <div className="sample-tests">
                  {samples.map((sample, i) => (
                    <details className="test-row" key={sample.name}>
                      <summary>
                        <Circle size={14} />
                        <span>
                          Example {i + 1}: {sample.name}
                        </span>
                        <ChevronRight size={13} />
                      </summary>
                      <p>
                        Input: <code>{sample.input}</code>
                        <br />
                        Expected: <code>{sample.output}</code>
                      </p>
                    </details>
                  ))}
                  <p className="test-help">
                    Run examples to explore. Check solution to test all 13
                    cases.
                  </p>
                </div>
              )}
            </div>
          </div>
          <div className="privacy-note">
            <ShieldCheck size={13} />
            Runs on your device. Results are practice feedback.
          </div>
        </section>
      </div>
      {runner.origin && (
        <iframe
          ref={runner.frame}
          key={runner.frameKey}
          src={runner.origin}
          onLoad={runner.hello}
          title="Isolated Python execution"
          sandbox="allow-scripts allow-same-origin"
          referrerPolicy="no-referrer"
          className="runner-frame"
          aria-hidden="true"
          tabIndex={-1}
        />
      )}
    </Shell>
  );
}
