import Link from "next/link";
import {
  ArrowUpRight,
  BookOpen,
  Braces,
  Github,
  Layers3,
  Route,
  Sparkles,
  House,
  FlaskConical,
  FolderOpen,
  NotebookPen,
} from "lucide-react";

export function Shell({
  children,
  active = "practice",
  workspace = false,
}: {
  children: React.ReactNode;
  active?:
    | "home"
    | "practice"
    | "paths"
    | "explore"
    | "projects"
    | "progress"
    | "about";
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
            <strong>ZeroShot</strong>
          </span>
        </Link>
        <div className="sidebar-body">
          <p className="nav-label">Your learning space</p>
          <nav aria-label="Main navigation">
            <Link
              href="/"
              aria-current={active === "home" ? "page" : undefined}
            >
              <House size={18} />
              Learning home
            </Link>
            <Link
              href="/problems/"
              aria-current={active === "practice" ? "page" : undefined}
            >
              <Braces size={18} />
              Lesson library
            </Link>
            <Link
              href="/paths/"
              aria-current={active === "paths" ? "page" : undefined}
            >
              <Route size={18} />
              Guided paths
            </Link>
            <Link
              href="/projects/mini-retrieval/"
              aria-current={active === "projects" ? "page" : undefined}
            >
              <FolderOpen size={18} />
              Projects
            </Link>
            <Link
              href="/explore/"
              aria-current={active === "explore" ? "page" : undefined}
            >
              <FlaskConical size={18} />
              Open lab
            </Link>
            <Link
              href="/progress/"
              aria-current={active === "progress" ? "page" : undefined}
            >
              <NotebookPen size={18} />
              Your progress
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
          href="https://github.com/dev-sudeep018/zeroshot"
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
