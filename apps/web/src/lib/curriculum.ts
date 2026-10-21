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
      "Connect vectors, probabilities, gradients, and loss to the behavior of a model.",
    outcome: "Explain what a model measures and how its parameters improve.",
    items: ["m01", "m02", "m03", "m04"],
  },
  {
    slug: "deep-learning",
    title: "Deep Learning from First Principles",
    description:
      "Check derivatives, propagate gradients, and construct the operations inside a transformer.",
    outcome:
      "Trace a signal through linear layers, normalization, and attention.",
    items: ["d01", "d02", "d03", "d04"],
  },
  {
    slug: "ai-engineering",
    title: "Practical AI Engineering",
    description:
      "Turn documents into a retrieval system, then measure where it works and where it misses.",
    outcome: "Build and evaluate a small retrieval pipeline.",
    items: ["e01", "e02", "e03", "e04"],
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
