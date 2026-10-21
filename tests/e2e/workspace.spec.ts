import { test, expect, type Page } from "@playwright/test";
import { readFileSync } from "node:fs";
import { DRAFT_KEY, PROGRESS_KEY } from "../../apps/web/src/lib/draft";
const reference = readFileSync(
  "content/problems/m02-stable-softmax/solution.py",
  "utf8",
);

async function pasteCode(page: Page, code: string) {
  const editor = page.getByRole("textbox", { name: "Python code editor" });
  await editor.focus();
  // Monaco follows the browser's platform, including WebKit's Mac emulation.
  const isMac = await page.evaluate(() =>
    navigator.userAgent.includes("Macintosh"),
  );
  await page.keyboard.press(isMac ? "Meta+A" : "Control+A");
  // Exercise Monaco's paste handler and onChange rather than its model API.
  // Firefox strips untrusted DataTransfer payloads, so supply the clipboard
  // event data explicitly. This does not claim OS clipboard integration coverage.
  await editor.evaluate((element, text) => {
    const event = new ClipboardEvent("paste", {
      bubbles: true,
      cancelable: true,
    });
    Object.defineProperty(event, "clipboardData", {
      value: {
        types: ["text/plain"],
        files: [],
        items: [],
        getData: (type: string) => (type === "text/plain" ? text : ""),
      },
    });
    element.dispatchEvent(event);
  }, code);
  await expect
    .poll(async () => {
      const raw = await page.evaluate(
        (key) => localStorage.getItem(key),
        DRAFT_KEY,
      );
      return raw ? JSON.parse(raw).code : null;
    })
    .toBe(code);
}

async function openCode(page: Page, code: string) {
  await page.addInitScript(
    ({ key, value }) =>
      localStorage.setItem(key, JSON.stringify({ version: 1, code: value })),
    { key: DRAFT_KEY, value: code },
  );
  await page.goto("/problems/stable-softmax/");
  await expect(
    page.getByRole("button", { name: "Check solution", exact: true }),
  ).toBeEnabled();
}
test("starter fails usefully, reference passes all tests and records local progress", async ({
  page,
}) => {
  await page.goto("/problems/stable-softmax/");
  await page
    .getByRole("button", { name: "Check solution", exact: true })
    .click();
  await expect(page.getByText("Keep going. Here’s what to check.")).toBeVisible(
    { timeout: 50_000 },
  );
  await page.getByRole("tab", { name: "Solution", exact: true }).click();
  await page.getByRole("button", { name: "Use reference in editor" }).click();
  await page.getByRole("button", { name: "Replace code", exact: true }).click();
  await page
    .getByRole("button", { name: "Check solution", exact: true })
    .click();
  await expect(page.getByText("All checks passed. Nicely done.")).toBeVisible({
    timeout: 50_000,
  });
  await expect(page.getByText("13/13 passed")).toBeVisible();
  expect(
    await page.evaluate((key) => localStorage.getItem(key), PROGRESS_KEY),
  ).toBe("complete");
  await page.reload();
  await expect(page.getByText("Completed on this device")).toBeVisible();
});
test("real editor changes survive refresh and example mode does not mark complete", async ({
  page,
}) => {
  await page.goto("/problems/stable-softmax/");
  await pasteCode(page, reference);
  await page.reload();
  await page.getByRole("button", { name: "Run examples" }).click();
  await expect(
    page.getByText("Examples passed. Try the full checks next."),
  ).toBeVisible({ timeout: 50_000 });
  await expect(page.getByText("3/3 passed")).toBeVisible();
  expect(
    await page.evaluate((key) => localStorage.getItem(key), PROGRESS_KEY),
  ).toBeNull();
});
test("syntax errors are readable and HTML output remains plain text", async ({
  page,
}) => {
  await openCode(page, "def softmax(:\n    pass");
  await page
    .getByRole("button", { name: "Check solution", exact: true })
    .click();
  await expect(page.getByText("Python needs a fix")).toBeVisible({
    timeout: 50_000,
  });
  await expect(page.locator(".error-output")).toContainText("SyntaxError");
  await pasteCode(page, 'print("<img src=x onerror=alert(1)>")\n' + reference);
  await page
    .getByRole("button", { name: "Check solution", exact: true })
    .click();
  await expect(page.getByText("All checks passed. Nicely done.")).toBeVisible({
    timeout: 50_000,
  });
  await expect(page.locator(".console-output")).toContainText(
    "<img src=x onerror=alert(1)>",
  );
  await expect(page.locator(".results-body img")).toHaveCount(0);
});
test("infinite loops time out and the next run gets a fresh environment", async ({
  page,
}) => {
  await openCode(page, "while True:\n    pass");
  await page
    .getByRole("button", { name: "Check solution", exact: true })
    .click();
  await expect(page.getByText("Time limit reached")).toBeVisible({
    timeout: 50_000,
  });
  await pasteCode(
    page,
    'assert "_old" not in globals()\n_old = True\n' + reference,
  );
  for (let run = 0; run < 2; run++) {
    await page
      .getByRole("button", { name: "Check solution", exact: true })
      .click();
    await expect(page.getByText("All checks passed. Nicely done.")).toBeVisible(
      { timeout: 50_000 },
    );
  }
});
test("a run can be stopped without losing the draft", async ({ page }) => {
  await openCode(page, "while True:\n    pass");
  await page
    .getByRole("button", { name: "Check solution", exact: true })
    .click();
  await page.getByRole("button", { name: "Stop run" }).click();
  await expect(page.getByText("Run stopped", { exact: true })).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Check solution", exact: true }),
  ).toBeEnabled();
});
test("navigation, filtering, hints and panel resizing work", async ({
  page,
}) => {
  await page.goto("/problems/");
  await page
    .getByRole("textbox", { name: "Search lessons" })
    .fill("not-a-problem");
  await expect(page.getByText("No matching lessons yet.")).toBeVisible();
  await page
    .getByRole("textbox", { name: "Search lessons" })
    .fill("stable softmax");
  await page.getByRole("link", { name: /Numerically Stable Softmax/ }).click();
  await page.getByRole("tab", { name: "Hints" }).click();
  await page.getByRole("tab", { name: "Hints" }).press("ArrowRight");
  await expect(
    page.getByRole("tab", { name: "Solution", exact: true }),
  ).toBeFocused();
  await page
    .getByRole("tab", { name: "Solution", exact: true })
    .press("ArrowLeft");
  await page.getByText("Hint 1: Start with the contract").click();
  await expect(
    page.getByText("Convert x with np.asarray", { exact: false }),
  ).toBeVisible();
  const divider = page.getByRole("separator");
  await divider.focus();
  await page.keyboard.press("ArrowRight");
  await expect(divider).toHaveAttribute("aria-valuenow", "46");
  await page.getByRole("link", { name: "Guided paths", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "One idea builds on the next." }),
  ).toBeVisible();
});
test("mobile reading and editing fit the viewport", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/problems/stable-softmax/");
  await expect(
    page.getByRole("heading", { name: "Numerically Stable Softmax" }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  await page.getByRole("tab", { name: "Solution", exact: true }).click();
  await page.getByRole("button", { name: "Use reference in editor" }).click();
  await expect(
    page.getByText("Replace your current code with the reference solution?"),
  ).toBeVisible();
  await page.getByRole("button", { name: "Replace code", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Check solution", exact: true }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
});
