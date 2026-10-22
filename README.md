# Project Mastery

Free, open-source AI learning for Python programmers. Follow connected paths, investigate interactive experiments, or start with a retrieval project and learn the concepts as you build.

The current curriculum contains 21 original lessons, 4 interactive experiments, and a retrieval project with a Python integration checkpoint. Two lessons begin with deliberately flawed code to investigate and repair. The [2,000-problem curriculum plan](docs/curriculum.md) separates the expansion target from published content.

![Connected learning home in black and light grey](docs/images/learning-home.jpg)

The screenshot records the connected-learning home. Coding lessons start with incomplete code or a clearly labelled debugging investigation. The current interface keeps the black/grey base and uses semantic colors for feedback and Python syntax.

![Semantic feedback and Python syntax colors](docs/images/semantic-workspace.jpg)

This workspace screenshot shows an existing reference draft passing three example cases. Example-only runs do not record completion.

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

The project is in development. See [verification](docs/verification.md) for what has actually been verified and [architecture](docs/architecture.md) for the execution boundary and limits. Browser results are practice feedback, not tamper-resistant certification.

For fast content iteration, use `pnpm content:check m05 d06 e07` (omit IDs for all packages). See the [free-resource survey and batch workflow](docs/source-research.md) and its [source registry](content/sources.json).

## Contributing and maintenance

Start with [CONTRIBUTING.md](CONTRIBUTING.md). Use a branch and pull request; GitHub Actions checks content, reference solutions, types, formatting, lint, builds, and Chromium/Firefox/WebKit behavior. Dependabot proposes weekly dependency and Actions updates. Report vulnerabilities privately using the repository's Security tab.

The [design record](DESIGN.md) describes the implemented palette, layout, controls, and responsive behavior. The [roadmap](docs/roadmap.md) tracks the remaining curriculum, account, and deployment work.

## Structure

- `apps/web`: Next.js learning workspace.
- `apps/runner`: sandbox frame and disposable Python workers on an isolated origin.
- `packages`: versioned problem schema and validated message protocol.
- `content/problems`: original problem statements, starter code, tests, and reference solutions.
- `scripts`: validation, runtime preparation, and local development servers.
- `tests`: schema, evaluator, browser, and isolation checks.

Original software and Python examples: Apache-2.0. Original educational prose: CC BY-SA 4.0. Third-party dependencies retain their own licenses. See LICENSE and content/LICENSE.
