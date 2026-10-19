# Project Mastery

Free, open-source AI practice for Python programmers. This repository is the first working milestone: one carefully tested exercise, a real Python editor, isolated browser execution, and useful feedback.

## Local setup

Requires Node.js 22+, pnpm 11.25.0, and Python 3.13+ with NumPy.

```sh
npm install -g pnpm@11.25.0
pnpm install
python -m pip install numpy
pnpm dev
```

Open http://localhost:3000. The separate runner uses http://127.0.0.1:4174. Keep both addresses distinct. The first setup downloads the pinned Python runtime and NumPy package; subsequent runs reuse them.

## Checks

```sh
pnpm check
pnpm exec playwright install chromium firefox webkit
pnpm test:e2e
```

The project is in development. See docs/verification.md for what has actually been verified and docs/architecture.md for the execution boundary and limits. Browser results are practice feedback, not tamper-resistant certification.

## Structure

- `apps/web`: Next.js learning workspace.
- `apps/runner`: sandbox frame and disposable Python workers on an isolated origin.
- `packages`: versioned problem schema and validated message protocol.
- `content/problems`: original problem statements, starter code, tests, and reference solutions.
- `scripts`: validation, runtime preparation, and local development servers.
- `tests`: schema, evaluator, browser, and isolation checks.

Original software and Python examples: Apache-2.0. Original educational prose: CC BY-SA 4.0. Third-party dependencies retain their own licenses. See LICENSE and content/LICENSE.
