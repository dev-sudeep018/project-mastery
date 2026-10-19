"use client";
import Link from "next/link";
import { useState } from "react";
import { ArrowRight, Search, Sprout } from "lucide-react";
import { Shell } from "./shell";
import data from "@/generated/problem.json";
export function Catalog() {
  const [query, setQuery] = useState("");
  const found =
    `${data.problem.title} ${data.problem.skills.join(" ")} foundations beginner`
      .toLowerCase()
      .includes(query.toLowerCase().trim());
  return (
    <Shell>
      <header className="topbar">
        <span>Practice</span>
        <span className="free-label">No account needed</span>
      </header>
      <div className="page-content">
        <h1>Build your understanding.</h1>
        <p className="page-lead">
          Small implementations. Real understanding. Start with a core AI idea
          and learn by making it work.
        </p>
        <div className="catalog-toolbar">
          <label className="search-field">
            <Search size={16} />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search problems or skills"
              aria-label="Search problems or skills"
            />
          </label>
          <span>
            {found ? 1 : 0} available {found ? "problem" : "problems"}
          </span>
        </div>
        {found ? (
          <article className="problem-card">
            <span className="problem-number">M02</span>
            <div>
              <h2>{data.problem.title}</h2>
              <p>{data.problem.summary}</p>
              <div className="problem-meta">
                <span className="difficulty">Beginner</span>
                <span>20 min</span>
                <span>NumPy</span>
                <span>Foundations</span>
              </div>
            </div>
            <Link className="primary" href="/problems/stable-softmax/">
              Open problem
              <ArrowRight size={15} />
            </Link>
          </article>
        ) : (
          <div className="empty-message">
            <h2>No matching problems</h2>
            <p>Try “softmax”, “NumPy”, or “foundations”.</p>
          </div>
        )}
        <div className="quiet-note">
          <Sprout size={19} />
          <p>
            We’re starting with one carefully tested exercise. The founding plan
            grows to 12 challenges, three learning paths, and one integrated
            project.
          </p>
        </div>
      </div>
    </Shell>
  );
}
