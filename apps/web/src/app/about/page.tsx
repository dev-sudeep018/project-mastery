import { Github } from "lucide-react";
import { Shell } from "@/components/shell";
import { catalog, paths } from "@/lib/curriculum";
export default function About() {
  return (
    <Shell active="about">
      <header className="topbar">
        <span>About ZeroShot</span>
        <span className="free-label">Built in the open</span>
      </header>
      <div className="page-content about-copy">
        <h1>AI skills should be accessible.</h1>
        <p className="page-lead">
          ZeroShot is a free, open-source learning project for Python
          programmers who want to understand and build AI systems.
        </p>
        <h2>Learn, build, understand.</h2>
        <p>
          We connect guided lessons, open experiments, and projects. The goal is
          useful engineering ability, supported by clear feedback and
          reproducible work.
        </p>
        <h2>What works today</h2>
        <ul>
          <li>
            {catalog.length} original lessons across {paths.length} connected
            learning paths.
          </li>
          <li>
            Four interactive experiments and a retrieval project with a Python
            implementation checkpoint.
          </li>
          <li>
            A Python editor with public examples, edge-case checks, hints, and
            references.
          </li>
          <li>
            On-device execution with NumPy, saved drafts, and recovery from
            failed runs.
          </li>
        </ul>
        <h2>Free means free to learn.</h2>
        <p>
          The introductory experience requires no paid API keys, GPU
          subscription, or account. Original software is Apache-2.0; original
          educational writing is CC BY-SA 4.0.
        </p>
        <h2>Be honest about progress.</h2>
        <p>
          Local completion is practice feedback. It is not an independently
          verified credential, and completing exercises does not guarantee
          employment. The curriculum target is 2,000 learning problems.
          Published counts reflect working content; the remaining curriculum and
          account synchronization are still being built. You can export and
          import your local progress and drafts today.
        </p>
        <a
          className="primary"
          href="https://github.com/dev-sudeep018/zeroshot"
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
