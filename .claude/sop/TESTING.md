# TESTING.md

**Stage:** Verify — alongside and after building, before claiming done.
**Purpose:** Test standards driven by the PRD, so we test what actually matters to users.

## Principles

1. **Test behavior, not implementation.** Tests should survive refactors.
2. **Failing test first.** For a feature or bug, write the test that fails, then make it pass.
3. **Evidence before claims.** "Done" requires seeing verification output — never assert success unseen.

## PRD-driven test cases

- **Generate test cases from the latest `docs/PRD.md` critical user journeys and workflows.**
- **Share the generated cases with the human operator for review and refinement.**
- **Collaborate to find and add missing cases** — edge cases, error paths, and journeys that were overlooked.

## Test levels & tooling

Cover all levels appropriate to the change:

- **Unit** — individual functions/components in isolation.
- **Integration** — modules working together (e.g. API + data, component + state).
- **End-to-end (E2E)** — full user journeys through the running app.
- **Regression** — existing behavior still works after a change.

Pick tools by the project's language/framework — e.g. **Playwright** or **Cypress** for browser E2E of user journeys, and **Jest** (or the framework's native runner) for unit/integration and synthetic journey checks.

**Baseline: every critical user journey in the PRD must have E2E coverage.**

## Gherkin syntax

Write test cases in **Gherkin** so they map cleanly to user journeys and stay readable to non-engineers. Store the `.feature` files under `docs/tests/` so they trace back to the PRD:

```gherkin
Feature: <capability from a PRD journey>
  Scenario: <specific case>
    Given <initial context>
    When <action>
    Then <expected outcome>
```

## Verification checklist

- [ ] **Reproduce bugs with a test first**, then fix.
- [ ] **Cover happy / edge / error paths** for each journey.
- [ ] **Deterministic** — no flakiness, no time/order dependence.
- [ ] **Run the full suite** plus typecheck and lint; read the output.
- [ ] **Exercise the actual change** in the running app, not just unit tests.
- [ ] **Regression before merge** — run the regression suite before or upon merging the working branch into `main`; it must be green.
- [ ] **Report real results** — including failures — and **include test results in the PR summary/comments** (see `ENGINEERING.md`).

## Defers to

Use `test-driven-development` for the red-green loop and `verification-before-completion` before any "it works" claim; this SOP defines where test cases come from and how they're written.
