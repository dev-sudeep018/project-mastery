import { test, expect } from "@playwright/test";
import { readFileSync } from "node:fs";

test("BM25 explanations follow the query, document and parameters", async ({
  page,
}) => {
  await page.goto("/projects/mini-retrieval/");
  await page
    .getByRole("combobox", { name: "Inspect a query" })
    .selectOption("1");
  await page
    .getByRole("combobox", { name: "Explain this document" })
    .selectOption("hybrid");
  const summary = page.locator(".score-summary");
  const before = await summary.textContent();
  const contributions = page.getByRole("region", {
    name: "BM25 term contributions",
  });
  await expect(
    contributions.getByRole("rowheader", { name: "search", exact: true }),
  ).toBeVisible();
  await page.getByRole("slider", { name: "BM25 k1", exact: true }).press("End");
  await expect(summary).not.toHaveText(before!);
  await page
    .getByRole("combobox", { name: "Explain this document" })
    .selectOption("privacy");
  await expect(
    page.getByText(
      "No query terms match this document. Its BM25 score is zero.",
    ),
  ).toBeVisible();
  await page
    .getByRole("combobox", { name: "Inspect a query" })
    .selectOption("3");
  await expect(
    page.getByRole("combobox", { name: "Explain this document" }),
  ).toHaveValue("privacy");
  await expect(
    contributions.getByRole("rowheader", { name: "private", exact: true }),
  ).toBeVisible();
});

test("evidence handles no fit, whole sources, and reproducible export", async ({
  page,
}) => {
  await page.goto("/projects/mini-retrieval/");
  const budget = page.getByRole("slider", { name: "Source-word budget" });
  await budget.press("Home");
  await expect(
    page.getByText(
      "No documents fit. Increase the word budget or choose another ranking.",
    ),
  ).toBeVisible();
  await expect(page.locator(".evidence-decisions .warning-text")).toHaveCount(
    2,
  );
  await page
    .getByRole("combobox", { name: "Inspect a query" })
    .selectOption("2");
  await page
    .getByRole("combobox", { name: "Evidence ranking" })
    .selectOption("bm25");
  await page
    .getByRole("combobox", { name: "Hybrid text method" })
    .selectOption("lexical");
  await page.getByRole("slider", { name: "BM25 b", exact: true }).press("Home");
  await budget.press("End");
  await expect(page.locator(".evidence-decisions .success-text")).toHaveCount(
    2,
  );
  await expect(page.locator(".evidence-context h4")).toHaveCount(2);
  const download = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export experiment report" }).click();
  const file = await download;
  const result = JSON.parse(readFileSync((await file.path())!, "utf8"));
  expect(result.version).toBe(2);
  expect(result.dataset).toEqual(
    JSON.parse(
      readFileSync("content/projects/mini-retrieval/dataset.json", "utf8"),
    ),
  );
  expect(result.experiment).toMatchObject({
    k: 2,
    vectorWeight: 0.5,
    lexicalMethod: "lexical",
    rankConstant: 60,
    bm25Settings: { k1: 1.2, b: 0 },
  });
  expect(result.experiment.rows).toHaveLength(4);
  expect(result.evidence).toMatchObject({
    query: "evaluation",
    method: "bm25",
    budget: 220,
    selectedIds: result.experiment.rows[2].bm25.slice(0, 2),
  });
  const sources = result.evidence.selectedIds.map((id: string) =>
    result.dataset.documents.find((doc: { id: string }) => doc.id === id),
  );
  const used = sources.reduce(
    (total: number, doc: { text: string }) =>
      total + doc.text.trim().split(/\s+/).length,
    0,
  );
  expect(result.evidence.used).toBe(used);
  expect(result.evidence.remaining).toBe(220 - used);
  expect(result.evidence.context).toBe(
    sources
      .map((doc: { id: string; text: string }) => `[${doc.id}] ${doc.text}`)
      .join("\n\n"),
  );
  expect(result.evidence.decisions).toHaveLength(2);
  expect(result.evidence.selectedIds).toContain("metrics");
  expect(result.evidence.context).toContain("[metrics]");
});

test("score table and evidence remain usable at a narrow width", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/projects/mini-retrieval/");
  await page.getByText("How text becomes a score", { exact: true }).click();
  await page.getByRole("slider", { name: "Results per query" }).press("End");
  await page.getByRole("slider", { name: "Source-word budget" }).press("End");
  await expect(page.locator(".evidence-context h4")).toHaveCount(6);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  const table = page.getByRole("region", { name: "BM25 term contributions" });
  await table.focus();
  await expect(table).toBeFocused();
  await page
    .getByRole("link", { name: "Implement selection under a context budget" })
    .click();
  await expect(page).toHaveURL(/\/problems\/context-budget-selection\/$/);
});
