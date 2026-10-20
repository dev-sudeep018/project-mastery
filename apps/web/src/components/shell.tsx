import Link from "next/link";
import {
  ArrowUpRight,
  BookOpen,
  Braces,
  Github,
  Layers3,
  Route,
  Sparkles,
} from "lucide-react";

export function Shell({
  children,
  active = "practice",
  workspace = false,
}: {
  children: React.ReactNode;
  active?: "practice" | "paths" | "about";
  workspace?: boolean;
}) {
  return (
    <div className={`app-shell ${workspace ? "workspace-shell" : ""}`}>
      <aside className="sidebar">
        <Link className="brand" href="/">
          <span className="brand-mark">
            <Layers3 size={23} />
          </span>
          <span>
            Project
            <br />
            <strong>Mastery</strong>
          </span>
        </Link>
        <div className="sidebar-body">
          <p className="nav-label">Your learning space</p>
          <nav aria-label="Main navigation">
            <Link
              href="/problems/"
              aria-current={active === "practice" ? "page" : undefined}
            >
              <Braces size={18} />
              Practice
            </Link>
            <Link
              href="/paths/"
              aria-current={active === "paths" ? "page" : undefined}
            >
              <Route size={18} />
              Learning paths
            </Link>
            <Link
              href="/about/"
              aria-current={active === "about" ? "page" : undefined}
            >
              <BookOpen size={18} />
              About the project
            </Link>
          </nav>
          <div className="sidebar-note">
            <Sparkles size={18} />
            <p>
              Understanding comes
              <br />
              from building.
            </p>
            <span>
              One concept. One experiment.
              <br />
              One step further.
            </span>
          </div>
        </div>
        <a
          className="github-link"
          href="https://github.com/dev-sudeep018/project-mastery"
          target="_blank"
          rel="noreferrer"
        >
          <Github size={18} />
          Build with us
          <ArrowUpRight size={14} />
        </a>
        <div className="sidebar-footer">Free to learn. Open to everyone.</div>
      </aside>
      <main id="main-content" className="main-area">
        {children}
      </main>
    </div>
  );
}
