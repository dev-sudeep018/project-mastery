# Verification record

## Connected learning and monochrome palette — 21–22 October 2026

The current release connects three guided paths, four interactive experiments, a searchable lesson library, and a retrieval project. It contains 12 published lessons plus one Python integration checkpoint, with 161 public cases. The 2,000-item curriculum allocation is a target, not an authored-content count.

Local content validation, TypeScript, ESLint, formatting, 15 Vitest tests, five Python test methods, and the 25-page production export pass. Native validation checks every reference and rejects every incomplete starter and a trivial incorrect implementation. Independent numerical checks cover softmax shift invariance, finite-difference gradients, and attention masking.

The browser suite now contains 28 tests per engine. It covers all 13 published references, connected navigation, filters, experiment controls, retrieval metrics/report export, progress backup merges, preservation of existing drafts, cross-tab completion, mobile navigation, and the existing editor/isolation regressions. An additional manifest test verifies that unknown items and unsupported versions are rejected before execution. All 84 browser tests passed in the clean Linux runs for revision `500b672`; final per-engine results for later revisions are recorded on [pull request #12](https://github.com/dev-sudeep018/project-mastery/pull/12).

Local Chromium and WebKit runs covered the complete suite. Two backup-test assertions incorrectly read Monaco's input element instead of its rendered code; after correcting that test, all 14 focused checks passed across both engines, including backup import and cross-tab completion. The final editor palette adjustments were also inspected in the rendered browser.

The finish review inspected ten desktop/mobile captures and sampled the implementation. It found one missing accessibility state on the mobile reading/editor switch. The corrected buttons expose complementary pressed states, and the existing mobile flow test passes in local Chromium and WebKit. The reviewer scored that fix resolved with `disposition: ship`; this verdict covers the listed fix. The initial reviewer attempt was replaced after a quota interruption. The design records were rechecked after the correction and remain accurate. The final production export, focused lint, formatting, and type checks pass.

The black/light-grey palette uses shared CSS tokens in the site and Monaco editor. Measured text contrast is at least 5.58:1 for the checked subtle-text/hover pair; primary action text is 12.84:1. The strong control boundary has 3.48:1 contrast against the hover surface. Diagnostic labels and icons distinguish passed and failed states without hue. These checks are not a complete accessibility audit.

The 2,000-ID prerequisite-graph test validates metadata capacity only. It does not establish the build performance, editorial quality, or runtime load characteristics of 2,000 authored packages. No production account synchronization or public production deployment is included.

## Prior workspace milestone — 20 October 2026

The first workspace milestone is tracked in [pull request #1](https://github.com/dev-sudeep018/project-mastery/pull/1), now merged. The results below describe that earlier revision; the required GitHub checks are authoritative for each tested commit.

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

The `main` branch requires an up-to-date pull request with those four checks and resolved conversations, including for administrators. Force pushes and deletion are disabled. Private vulnerability reporting is enabled. Dependabot configuration is present on the default branch.

## Verification limits

The locally downloaded Firefox executable could not launch on this Windows host (`spawn UNKNOWN`), including after reinstalling the official Playwright binary. The GitHub Firefox job tests Linux independently; Windows Firefox is not claimed as verified.

Playwright WebKit is not a real Safari/iPhone device test. Mobile verification uses a narrow browser viewport. A full screen-reader review, actual mobile-device testing, production hosting/header verification, load testing, and an independent security audit remain future work. Browser workers do not provide a hard memory quota; completion is local, mutable practice feedback.

Automated editor replacement dispatches a synthetic paste payload through Monaco's DOM handler and verifies the saved code exactly. It covers editor changes and persistence, not operating-system clipboard permissions or integration.

The first milestone contained one complete exercise. The connected-learning release expands it to the counts recorded above.

## Visual provenance

`images/workspace.jpg` records the first milestone during a reference-solution run. `images/learning-home.jpg` records the connected-learning home with the user's black/light-grey palette. Both are original screenshots of the locally built application. The interface uses authored CSS, Lucide icons, native UI/code fonts, and actual numerical example bars. There are no generated photographs or invented commercial claims.

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
