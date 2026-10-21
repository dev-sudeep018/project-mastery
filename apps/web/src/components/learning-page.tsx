import { Shell } from "./shell";
export function LearningPage({
  title,
  active,
  children,
}: {
  title: string;
  active: "home" | "practice" | "paths" | "explore" | "projects" | "progress";
  children: React.ReactNode;
}) {
  return (
    <Shell active={active}>
      <header className="topbar">
        <span>{title}</span>
        <span className="free-label">Free & open source</span>
      </header>
      <div className="page-content learning-content">{children}</div>
    </Shell>
  );
}
