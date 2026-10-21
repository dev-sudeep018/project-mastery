import { test, expect } from "@playwright/test";
import { readFileSync } from "node:fs";
import { DRAFT_KEY } from "../../apps/web/src/lib/draft";
const reference = readFileSync(
  "content/problems/m02-stable-softmax/solution.py",
  "utf8",
);

test("runner has restrictive headers and cannot read the parent origin", async ({
  page,
  request,
}) => {
  const response = await request.get("http://127.0.0.1:4174/worker.js");
  const policy = response.headers()["content-security-policy"];
  expect(policy).toContain("connect-src 'self'");
  expect(policy).toContain("worker-src 'self'");
  expect(policy).not.toContain("'unsafe-eval'");
  expect(response.headers()["access-control-allow-origin"]).toBeUndefined();
  expect((await request.post("http://127.0.0.1:4174/")).status()).toBe(405);
  await page.goto("/problems/stable-softmax/");
  await expect(
    page.getByRole("button", { name: "Check solution", exact: true }),
  ).toBeEnabled();
  const frame = page
    .frames()
    .find((frame) => frame.url().startsWith("http://127.0.0.1:4174"))!;
  expect(
    await frame.evaluate(() => {
      try {
        return parent.document.cookie;
      } catch {
        return "BLOCKED";
      }
    }),
  ).toBe("BLOCKED");
});
test("learner Python cannot request application or external network resources", async ({
  page,
}) => {
  const probe =
    `import js
from pyodide.ffi import JsException
for url in ["http://localhost:3000/", "https://example.com/"]:
    try:
        xhr = js.XMLHttpRequest.new()
        xhr.open("GET", url, False)
        xhr.send(None)
        raise AssertionError("NETWORK WAS NOT BLOCKED")
    except JsException:
        print("NETWORK_BLOCKED")
assert not hasattr(js.globalThis, "document")
assert not hasattr(js.globalThis, "localStorage")
print("NO_APP_STORAGE")
` + reference;
  await page.addInitScript(
    ({ key, code }) =>
      localStorage.setItem(key, JSON.stringify({ version: 1, code })),
    { key: DRAFT_KEY, code: probe },
  );
  await page.goto("/problems/stable-softmax/");
  await page
    .getByRole("button", { name: "Check solution", exact: true })
    .click();
  await expect(page.getByText("All checks passed. Nicely done.")).toBeVisible({
    timeout: 50_000,
  });
  await expect(page.locator(".console-output")).toContainText(
    "NETWORK_BLOCKED",
  );
  await expect(page.locator(".console-output")).toContainText("NO_APP_STORAGE");
});
test("forged parent messages and malformed run requests are ignored", async ({
  page,
}) => {
  await page.goto("/problems/stable-softmax/");
  await expect(
    page.getByRole("button", { name: "Check solution", exact: true }),
  ).toBeEnabled();
  await page.evaluate(() =>
    window.postMessage(
      { kind: "result", protocol: 1, status: "passed", tests: [] },
      "*",
    ),
  );
  await expect(page.getByText("All checks passed. Nicely done.")).toHaveCount(
    0,
  );
  const count = await page.evaluate(async () => {
    let messages = 0;
    const listener = (event: MessageEvent) => {
      if (event.data?.kind === "status" || event.data?.kind === "result")
        messages++;
    };
    addEventListener("message", listener);
    document.querySelector("iframe")?.contentWindow?.postMessage(
      {
        kind: "run",
        protocol: 1,
        requestId: crypto.randomUUID(),
        problemId: "m02",
        problemVersion: 1,
        sourceCode: "x".repeat(32001),
        mode: "all",
      },
      "http://127.0.0.1:4174",
    );
    await new Promise((resolve) => setTimeout(resolve, 300));
    removeEventListener("message", listener);
    return messages;
  });
  expect(count).toBe(0);
});

test("runner rejects unpublished items and unavailable versions before execution", async ({
  page,
}) => {
  await page.goto("/problems/stable-softmax/");
  await expect(
    page.getByRole("button", { name: "Check solution", exact: true }),
  ).toBeEnabled();
  const results = await page.evaluate(async () => {
    const frame = document.querySelector("iframe")!.contentWindow!;
    const requests = [
      { problemId: "m99999", problemVersion: 1 },
      { problemId: "m02", problemVersion: 999 },
    ];
    return Promise.all(
      requests.map(
        (item) =>
          new Promise<{ status: string; error: string; tests: unknown[] }>(
            (resolve, reject) => {
              const requestId = crypto.randomUUID();
              const timer = setTimeout(() => {
                removeEventListener("message", listener);
                reject(new Error("No rejection received"));
              }, 5000);
              function listener(event: MessageEvent) {
                if (
                  event.source !== frame ||
                  event.origin !== "http://127.0.0.1:4174" ||
                  event.data?.requestId !== requestId ||
                  event.data?.kind !== "result"
                )
                  return;
                clearTimeout(timer);
                removeEventListener("message", listener);
                resolve(event.data);
              }
              addEventListener("message", listener);
              frame.postMessage(
                {
                  kind: "run",
                  protocol: 1,
                  requestId,
                  ...item,
                  sourceCode: 'raise Exception("SHOULD NOT EXECUTE")',
                  mode: "all",
                },
                "http://127.0.0.1:4174",
              );
            },
          ),
      ),
    );
  });
  for (const result of results) {
    expect(result.status).toBe("error");
    expect(result.error).toContain("lesson version is unavailable");
    expect(result.tests).toEqual([]);
  }
});
