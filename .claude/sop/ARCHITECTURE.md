# ARCHITECTURE.md

**Stage:** Architecture — after design, before implementing anything multi-part.
**Purpose:** Standards for sound system and data design, and for keeping the design visible.

## Principles

1. **Simplicity.** The best architecture is the simplest one that meets the requirements.
2. **Clear boundaries & single responsibility.** Each module does one thing, behind a well-defined interface.
3. **One-way data flow.** Predictable direction beats clever bidirectional coupling.
4. **Avoid one-way doors.** Prefer reversible decisions; flag the irreversible ones explicitly.

## Gate — propose and diagram before building

**Before building, present the best architecture approach(es) to the human operator with trade-offs and a recommendation, and show a diagram of the proposed end-state solution.** Get alignment before writing code.

**Cloud reference architecture.** Based on the operator's preferred cloud from the PRD's *Technical requirements* (AWS / GCP / Azure), research the relevant reference architecture and Well-Architected guidance for that provider, then **propose the specific cloud resources needed to build the product** (compute, storage, database, networking, auth, etc.) with rough cost/scaling implications. Get sign-off before provisioning.

## The architecture doc lives at `docs/architecture.md`

Keep a current architecture diagram in `docs/architecture.md`. Use **Mermaid** (text-based, versionable, easy to regenerate). **Update the diagram as the product is refined and enhanced** so it never goes stale.

## Checklist — before implementation

- [ ] **Model the data first** — entities, relationships, ownership, lifecycle.
- [ ] **Module boundaries & dependencies** — what each unit does, how they talk, who depends on whom.
- [ ] **State ownership** — where each piece of state lives and who mutates it.
- [ ] **Failure-handling strategy** — how errors, retries, and partial failures are handled.
- [ ] **Elasticity & scalability** — size for the load and growth the PRD implies (traffic, data volume, concurrency, peak vs. baseline); scale to the requirement, no more, no less.
- [ ] **Justify external dependencies** — each new dep earns its place; prefer platform-native.
- [ ] **No premature abstraction** — build for today's requirements, not imagined ones.
- [ ] **Record key decisions** — append ADR-lite entries (decision, why, alternatives) to the shared `docs/decisions.md`, not inline in the diagram doc.

## Defers to

Use `plan-eng-review` / `writing-plans` for detailed implementation planning; this SOP governs the shape of the system and the diagram that documents it.
