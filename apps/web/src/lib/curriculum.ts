import catalogData from "../generated/catalog.json";
import type { Problem } from "@mastery/problem-schema";

export const allItems = catalogData as unknown as Problem[];
export const catalog = allItems
  .filter((item) => item.kind !== "project")
  .sort((a, b) => {
    const order = ["foundations", "deep-learning", "engineering"];
    return (
      order.indexOf(a.domain) - order.indexOf(b.domain) ||
      a.id.localeCompare(b.id)
    );
  });
export const domains: Record<Problem["domain"], string> = {
  foundations: "Mathematics & ML",
  "deep-learning": "Deep learning",
  engineering: "AI engineering",
};
export const paths = [
  {
    slug: "mathematics-to-ml",
    title: "Mathematics to Machine Learning",
    description:
      "Connect vectors, probabilities, gradients, preprocessing, and evaluation to the behavior of a model.",
    outcome:
      "Explain model updates, avoid preprocessing leakage, and compare decision thresholds.",
    items: ["m01", "m02", "m03", "m04", "m05", "m06", "m07"],
  },
  {
    slug: "deep-learning",
    title: "Deep Learning from First Principles",
    description:
      "Check derivatives, trace activation gradients, and inspect the operations and controls used in neural networks.",
    outcome:
      "Trace forward and backward signals and explain dropout and gradient clipping.",
    items: ["d01", "d02", "d05", "d06", "d07", "d03", "d04"],
  },
  {
    slug: "ai-engineering",
    title: "Practical AI Engineering",
    description:
      "Turn documents into retrieval vectors, combine and diversify results, then evaluate relevance and ranking quality.",
    outcome:
      "Build a retrieval pipeline and explain its relevance, diversity, and evaluation tradeoffs.",
    items: ["e01", "e02", "e05", "e03", "e04", "e06", "e07"],
  },
];
export function itemById(id: string) {
  return allItems.find((item) => item.id === id);
}
export function itemHref(id: string) {
  return `/problems/${itemById(id)?.slug ?? ""}/`;
}
export function pathFor(id: string) {
  return paths.find((path) => path.items.includes(id));
}
