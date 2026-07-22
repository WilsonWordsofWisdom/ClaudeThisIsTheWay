# ENGINEERING.md

**Stage:** Build — during implementation.
**Purpose:** Coding, commit, and PR standards that keep code reviewable, traceable, and secure.

## Principles

1. **Match existing style.** Consistency with the codebase beats personal preference.
2. **Surgical changes.** Every changed line traces to the request. Don't refactor what isn't broken.
3. **YAGNI.** Minimum code that solves the problem; nothing speculative.
4. **DRY — don't repeat yourself.** Extract shared logic into reusable functions/components; the same change should never need to be made in two places.
5. **No hardcoded values.** Use named constants, config, and environment variables instead of magic literals. Structure code so values and behaviors likely to change are easy to change — dynamic where it removes duplication or eases maintenance, without speculative over-engineering (balance with YAGNI).
6. **Secure by default.** Security is part of writing the code, not a later phase.

## Coding checklist

- [ ] **Lint & format (mandatory)** — code must pass the linter and be auto-formatted to the project's style before committing; always format for human readability.
- [ ] **Consistent naming & component patterns** — follow the same conventions throughout the project.
- [ ] **Small, focused units** — a function/file does one thing; large files signal too many responsibilities.
- [ ] **Clear inline comments** — explain each function and any non-obvious line, so review and traceability are seamless. Comments say *why*, not *what*.
- [ ] **Secure coding** — validate input at boundaries, encode output, parameterize queries, least privilege, safe defaults. (See `SECURITY_ASSESSMENT.md`.)
- [ ] **No secrets in code** — use environment variables/secret stores.
- [ ] **No silent failures** — handle or surface errors; never swallow them.
- [ ] **No orphaned dead code** — remove imports/vars/functions *your* change made unused; leave pre-existing dead code unless asked.

## Commit & PR standard

- **Commit messages:** imperative, scoped, and specific — *what* changed and *why*. Small, coherent commits over one giant blob.
- **Branch, don't commit to main.** Never force-push or amend shared history without asking.
- **PR summary must include:**
  - **Key features built** — what this PR delivers.
  - **Why** the key code changes were made.
  - **Bugs fixed** (if any).
  - **Tests done** — including results (see `TESTING.md`).
  - **What the operator should review** — the risky or judgment-call areas to focus on, with specific **`file:line` references** pointing to where each key feature was built.

## Defers to

Use `test-driven-development` for the write-tests-first loop and `review` / `code-review` before landing; this SOP defines the code, commit, and PR quality bar.
