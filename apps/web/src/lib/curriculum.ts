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
      "Build and evaluate numerical models, inspect feature geometry, and preserve training/evaluation boundaries.",
    items: [
      "m01",
      "m02",
      "m03",
      "m04",
      "m05",
      "m06",
      "m07",
      "m08",
      "m09",
      "m10",
      "m11",
      "m12",
      "m13",
      "m14",
      "m15",
      "m16",
      "m17",
    ],
  },
  {
    slug: "deep-learning",
    title: "Deep Learning from First Principles",
    description:
      "Check derivatives, trace activation gradients, and inspect the operations and controls used in neural networks.",
    outcome:
      "Trace neural-network operations and gradients, update optimizer state, and prepare sequence representations.",
    items: [
      "d01",
      "d02",
      "d05",
      "d06",
      "d07",
      "d03",
      "d04",
      "d08",
      "d09",
      "d10",
      "d11",
      "d12",
      "d13",
      "d14",
      "d15",
      "d16",
      "d17",
    ],
  },
  {
    slug: "ai-engineering",
    title: "Practical AI Engineering",
    description:
      "Turn documents into retrieval vectors, combine and diversify results, then evaluate relevance and ranking quality.",
    outcome:
      "Represent text, rank and select evidence, inspect tokenization, and evaluate predictions and probabilities.",
    items: [
      "e01",
      "e02",
      "e05",
      "e03",
      "e04",
      "e06",
      "e07",
      "e08",
      "e09",
      "e10",
      "e11",
      "e12",
      "e13",
      "e14",
      "e15",
      "e16",
      "e17",
    ],
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
