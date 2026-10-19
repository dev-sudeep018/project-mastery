# Verification record

First workspace milestone, checked on 20 October 2026 (Asia/Kolkata). The implementation is tracked in [pull request #1](https://github.com/dev-sudeep018/project-mastery/pull/1); its required GitHub checks are the authoritative CI results for each revision.

## Recorded local results

Environment: Windows, Node.js 24.13.0, pnpm 11.25.0, Python 3.14.5, NumPy 2.4.5, Playwright 1.64.1.

| Check                                                        | Result                                                                                  |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| Content schema, prerequisite graph, and reference validation | Passed for the one published exercise                                                   |
| TypeScript, ESLint, Prettier                                 | Passed                                                                                  |
| Vitest contracts and draft recovery                          | 8 tests passed                                                                          |
| Python evaluator and numerical properties                    | 3 tests passed                                                                          |
| Next.js production static export                             | Passed                                                                                  |
| Chromium browser and isolation suite                         | 10 tests passed                                                                         |
| WebKit browser and isolation suite                           | 10 tests passed                                                                         |
| Production dependency audit                                  | No known vulnerabilities reported at verification time                                  |
| Manual desktop/mobile review                                 | 1440 x 900 and 390 x 844 inspected; mobile replacement fix received `disposition: ship` |
| In-app browser console                                       | No errors reported in the final inspected preview                                       |

The reference implementation passes all 13 public exercise cases in both local Python and browser Python. The evaluator rejects incomplete and plausible incorrect solutions. Additional numerical checks cover invariance under adding a constant and preservation of the input.

Browser tests exercise starter failures, reference success, saved edits after reload, example-only runs, syntax errors, literal HTML output, cancellation, infinite-loop termination, fresh state between runs, navigation, search, keyboard tab/panel controls, and the mobile replacement prompt. Isolation probes check response CSP, blocked parent-document access, blocked application/external network requests from learner code, and rejection of forged or malformed messages.

## GitHub verification and maintenance

[GitHub Actions](https://github.com/dev-sudeep018/project-mastery/actions) performs clean Linux installs and runs four required jobs: content/types/lint/format/unit tests/build, plus one browser/isolation job for each of Chromium, Firefox, and WebKit. Use the checks on the pull request to inspect the precise tested commit and any retry. Failure artifacts retain screenshots and traces for seven days.

The `main` branch requires an up-to-date pull request with those four checks and resolved conversations, including for administrators. Force pushes and deletion are disabled. Private vulnerability reporting is enabled. Dependabot configuration becomes active when merged into the default branch.

## Verification limits

The locally downloaded Firefox executable could not launch on this Windows host (`spawn UNKNOWN`), including after reinstalling the official Playwright binary. The GitHub Firefox job tests Linux independently; Windows Firefox is not claimed as verified.

Playwright WebKit is not a real Safari/iPhone device test. Mobile verification uses a narrow browser viewport. A full screen-reader review, actual mobile-device testing, production hosting/header verification, load testing, and an independent security audit remain future work. Browser workers do not provide a hard memory quota; completion is local, mutable practice feedback.

Automated editor replacement dispatches a synthetic paste payload through Monaco's DOM handler and verifies the saved code exactly. It covers editor changes and persistence, not operating-system clipboard permissions or integration.

The product contains one complete exercise. Other curriculum entries are visibly marked as planned. No account synchronization or public production deployment is included in this milestone.

## Visual provenance

`images/workspace.jpg` is an original screenshot of the locally built application, captured during a reference-solution run. The interface uses authored CSS, Lucide icons, native UI/code fonts, and actual numerical example bars. There are no generated photographs or invented commercial claims.

## Reproduction

```sh
pnpm install --frozen-lockfile
python -m pip install numpy==2.4.5
pnpm check
pnpm exec playwright install chromium firefox webkit
pnpm test:e2e
pnpm audit --prod
```

On Linux, install browser OS dependencies with `pnpm exec playwright install --with-deps`. GitHub uses this path. The browser suite starts the two-origin preview server automatically when needed.
