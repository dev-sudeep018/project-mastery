import { Github } from "lucide-react";
import { Shell } from "@/components/shell";
export default function About() {
  return (
    <Shell active="about">
      <header className="topbar">
        <span>About Project Mastery</span>
        <span className="free-label">Built in the open</span>
      </header>
      <div className="page-content about-copy">
        <h1>AI skills should be accessible.</h1>
        <p className="page-lead">
          Project Mastery is a free, open-source learning project for Python
          programmers who want to understand and build AI systems.
        </p>
        <h2>Learn, build, understand.</h2>
        <p>
          We connect explanations, small coding challenges, and increasingly
          complete projects. The goal is useful engineering ability, supported
          by clear feedback and reproducible work.
        </p>
        <h2>What works today</h2>
        <ul>
          <li>One original challenge: Numerically Stable Softmax.</li>
          <li>A Python editor with example runs and 13 public checks.</li>
          <li>
            On-device execution with NumPy, saved drafts, and recovery from
            failed runs.
          </li>
        </ul>
        <h2>Free means free to learn.</h2>
        <p>
          The introductory experience requires no paid API keys, GPU
          subscription, or account. Original software is Apache-2.0; original
          educational writing is CC BY-SA 4.0. The project is at its first
          development milestone.
        </p>
        <h2>Be honest about progress.</h2>
        <p>
          Local completion is practice feedback. It is not an independently
          verified credential, and completing exercises does not guarantee
          employment. The full 12-challenge curriculum and account
          synchronization are future work.
        </p>
        <a
          className="primary"
          href="https://github.com/dev-sudeep018/project-mastery"
          target="_blank"
          rel="noreferrer"
        >
          <Github size={16} />
          Explore the repository
        </a>
      </div>
    </Shell>
  );
}
