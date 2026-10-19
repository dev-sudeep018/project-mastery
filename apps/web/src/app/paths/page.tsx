import Link from "next/link";
import { ArrowRight, Circle, CircleDot, Route } from "lucide-react";
import { Shell } from "@/components/shell";
export default function Paths() {
  return (
    <Shell active="paths">
      <header className="topbar">
        <span>Learning paths</span>
        <span className="free-label">A connected way to practice</span>
      </header>
      <div className="page-content">
        <h1>One idea builds on the next.</h1>
        <p className="page-lead">
          Our first path connects numerical computing to the operations behind
          machine learning. Start with the available exercise; the rest is our
          content roadmap.
        </p>
        <div className="path-intro">
          <Route size={26} />
          <div>
            <h2>Mathematics to Machine Learning</h2>
            <p>For programmers comfortable with Python functions and arrays.</p>
          </div>
        </div>
        <ol className="path-list">
          {[
            [
              "Vector operations & cosine similarity",
              "Understand similarity between vectors.",
              false,
            ],
            [
              "Numerically Stable Softmax",
              "Turn model scores into a probability distribution.",
              true,
            ],
            [
              "Linear regression gradients",
              "Find how each parameter changes the loss.",
              false,
            ],
            [
              "Binary cross-entropy",
              "Measure the cost of confident, incorrect predictions.",
              false,
            ],
          ].map(([title, body, available]) => (
            <li key={String(title)} className={available ? "available" : ""}>
              {available ? (
                <CircleDot className="step-icon" size={18} />
              ) : (
                <Circle className="step-icon" size={18} />
              )}
              <div>
                <h3>
                  {title}
                  {!available && <span className="planned">Planned</span>}
                </h3>
                <p>{body}</p>
                {available && (
                  <Link href="/problems/stable-softmax/">
                    Practice this concept
                    <ArrowRight size={14} />
                  </Link>
                )}
              </div>
            </li>
          ))}
        </ol>
        <p className="roadmap-note muted">
          Deep Learning from First Principles and Practical AI Engineering are
          planned next. Content is never locked behind payment.
        </p>
      </div>
    </Shell>
  );
}
