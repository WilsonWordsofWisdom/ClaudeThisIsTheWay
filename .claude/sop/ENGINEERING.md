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

## Library dependency selection

Before adding a new library, compare it against the alternatives — including "write it ourselves" and "use the platform/stdlib" — on total lifecycle cost, not just lines of code saved today.

- **Problem fit & footprint** — Solves the actual problem cleanly, at the smallest size that does so. Prefer stdlib/platform first; don't pull in a large abstraction for something a few lines would handle — and don't hand-roll complex, security-sensitive functionality just to dodge a dependency.
- **Maintenance health** — Recent commits/releases, responsive maintainers, a track record of fixing bugs and security issues promptly. Stars/downloads are a signal, not proof of quality — for critical functionality, read the implementation.
- **Security & supply chain** — Vulnerability history, scanning support, and the size/trustworthiness of its transitive dependency tree. Watch for install scripts, native binaries, or build steps that need extra trust.
- **API stability & exit cost** — Mature, semver'd, predictable upgrades. Keep third-party types out of our public/internal interfaces so replacing the library later stays cheap.
- **License compatibility** — Its license and its transitive deps' licenses fit our project's distribution/commercial requirements.
- **Necessity (YAGNI)** — Every dependency needs a concrete justification; no adding libraries for speculative future needs.

**For non-trivial dependencies, answer before adding:**
1. Why can't stdlib/platform solve this?
2. What's its security/vulnerability track record, and what transitive deps does it pull in?
3. How costly would it be to remove later?
4. Are its licenses compatible?
Prefer dependencies that are boring, mature, well-understood, and easy to upgrade or remove.

## Troubleshooting log — `docs/troubleshooting.md`

Debugging the same problem twice is pure waste, and across sessions it is invisible waste — nobody
notices the second investigation was avoidable. The log exists to make that cost visible and cheap.

- **Read first.** Before investigating any error, grep the log for the symptom. The lookup has to be
  cheaper than the investigation for this to pay, so entries lead with the **literal error string**.
- **Write when it cost something.** Append after any fix that took more than one attempt. Solved
  first try means it wasn't expensive and won't be next time either.
- **Write it in the same edit as the fix.** A separate step doesn't happen.
- **Record dead ends.** "Tried X, failed because Y" is what stops the re-tread — it is the highest-value
  entry and the one always lost.
- **Only what recurs.** Environment quirks, tooling, non-obvious causes. Not fixed code bugs: those
  can't happen again and git already holds the reasoning.
- **Prune.** When the cause is permanently gone, delete the entry. Git remembers.

This covers repeat investigation *across* sessions. It does nothing for a single session that thrashes
on one problem — there, stop and re-read the error rather than trying another variation.

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
