# PRODUCT_BRIEF.md

**Stage:** Discovery — the first thing to do on any new project or feature.
**Purpose:** Force clarity on *what* we're building and *why* before any design or code.

## Principles

1. **No code without a brief.** If we can't state the problem and who has it, we're not ready to build.
2. **Non-goals matter as much as goals.** What we deliberately won't do prevents scope creep.
3. **The brief is a living document, not a one-time gate.** It evolves as we learn.
4. **Smallest valuable slice wins.** Ship the thinnest thing that delivers real value, then iterate.

## Trigger — check state, not stage

`docs/PRD.md` is required by *existence*. Check for it rather than trying to recognise the moment:

| State | What to do |
|-------|-----------|
| Missing, project is new | Principle 1 applies — no code without a brief. Run the discovery dialogue. |
| Missing, code already exists | Offer to reconstruct it from the codebase, marked `Status: Reconstructed`. |
| Present | Read it; it is the input every later stage depends on. |

**A reconstructed PRD is weaker than an authored one, and must say so.** Read from code, you can describe what the system does and infer its journeys. You cannot recover what was decided, what was rejected, or why. Two sections are especially unreliable and should be marked as such until the operator confirms them:

- **Non-goals** — from code these collapse into "things it happens not to do", which is not the same as a deliberate exclusion and constrains nothing.
- **Success metrics & north star** — chosen after the fact, these drift toward whatever the existing instrumentation can already measure rather than what matters.

Ask the operator to fill both. Once they have, change the status to `Authored` and log what they tell you in `docs/decisions.md` — that conversation is often the only surviving record of the original reasoning.

## The PRD lives at `docs/PRD.md`

Every project maintains a Product Requirements Doc at `docs/PRD.md`. Create it up front, then **keep updating it through the whole lifecycle** as requirements, scope, and enhancements evolve. It is the single source of truth that downstream stages depend on.

**Companion log — `docs/decisions.md`:** significant business *and* technical decisions (and *why*) are recorded in a separate, append-only decisions log at `docs/decisions.md` — not inline in the PRD. Other SOPs (e.g. `ARCHITECTURE.md`) append to and reference the same file. Keep entries dated.

## Checklist — a complete brief covers

- [ ] **Problem statement** — the real problem, in one or two sentences.
- [ ] **Target user & job-to-be-done** — who has this problem and what they're trying to accomplish.
- [ ] **Critical user journeys & workflows** — the key end-to-end paths a user takes. These later drive the test cases (see `TESTING.md`).
- [ ] **Success metrics & north star** — how we'll know it worked; the one metric that matters most. These later drive the analytics page (see `ANALYTICS.md`).
- [ ] **In scope** — what this delivers.
- [ ] **Non-goals** — what it explicitly does not do (this release).
- [ ] **Constraints** — time, budget, compliance, and other hard limits.
- [ ] **Data classification & regulatory regime** — the most sensitive data the system will hold, and any regime that follows from it. This is a business decision only the operator can make, and later stages depend on it (see `SECURITY_ASSESSMENT.md`). Default to *none* for personal projects.
- [ ] **Technical requirements** — preferred stack, cloud/hosting environment, and any technologies to bootstrap on or build with; note if greenfield/open.
- [ ] **Assumptions & risks** — what we're betting on, and what could go wrong.
- [ ] **Smallest valuable slice** — the first shippable increment.

> Significant decisions are logged in `docs/decisions.md`, not in this checklist.

## Fill-in template

```md
# <Project> — Product Requirements

## Problem
## Target user & job-to-be-done
## Critical user journeys
1.
## Success metrics & north star
- North star:
- Supporting metrics:
## In scope
## Non-goals
## Constraints
## Data classification & regulatory regime
## Technical requirements
- Preferred stack / cloud / hosting:
- Technologies to bootstrap on or build with:
## Assumptions & risks
## Smallest valuable slice
```

> Decisions are logged separately in `docs/decisions.md` (append-only, dated: `YYYY-MM-DD — <decision> — <why>`).

## Defers to

Use the `brainstorming` skill to run the discovery dialogue; this SOP defines what the resulting brief must contain.
