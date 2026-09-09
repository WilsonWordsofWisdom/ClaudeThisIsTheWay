# ARCHITECTURE.md

**Stage:** Architecture — after design, before implementing anything multi-part.
**Purpose:** Standards for sound system and data design, and for keeping the design visible.

## Principles

1. **Simplicity.** The best architecture is the simplest one that meets the requirements.
2. **Clear boundaries & single responsibility.** Each module does one thing, behind a well-defined interface.
3. **One-way data flow.** Predictable direction beats clever bidirectional coupling.
4. **Avoid one-way doors.** Prefer reversible decisions; flag the irreversible ones explicitly.

## Trigger — check state, not stage

`docs/architecture.md` is required by *existence*. Check for it rather than trying to recognise the moment — the moment is missed on every project that adopted these standards after it started, which is most of them.

| State | What to do |
|-------|-----------|
| Missing, project is new | The gate below applies — propose and diagram *before* building. |
| Missing, code already exists | Offer to reconstruct it from the codebase (see below), marked `Status: Reconstructed`. |
| Present | Read it. If the code has moved past it, offer to refresh it and show what changed. |

## Gate — propose and diagram before building

**Before building, present the best architecture approach(es) to the human operator with trade-offs and a recommendation, and show a diagram of the proposed end-state solution.** Get alignment before writing code.

**Cloud reference architecture.** Based on the operator's preferred cloud from the PRD's *Technical requirements* (AWS / GCP / Azure), research the relevant reference architecture and Well-Architected guidance for that provider, then **propose the specific cloud resources needed to build the product** (compute, storage, database, networking, auth, etc.) with rough cost/scaling implications. Get sign-off before provisioning.

## The architecture doc lives at `docs/architecture.md`

Keep a current architecture diagram in `docs/architecture.md`. Use **Mermaid** (text-based, versionable, easy to regenerate). **Update the diagram as the product is refined and enhanced** so it never goes stale.

## Reconstructing a diagram from existing code

When the diagram was never produced, derive it from what's there. Read the code before drawing: entry points, module boundaries and their dependencies, data stores, external services called, and whatever deployment surface appears in config.

Draw it in layers, going only as deep as the project warrants:

1. **Context** — the system and the external things it talks to.
2. **Container** — the services, processes, and data stores inside it.
3. **Component** — modules within the main application, and who depends on whom.

For an architecture review, also mark **trust boundaries** and the **data flows** that cross them.

**Name what a repository cannot show.** Cloud topology, network boundaries, IAM and roles, scaling and failover configuration, and anything set in a console leave no trace in the code. List these as *not visible from the repository* rather than omitting them — silent omission reads as absence of risk. The same applies to any module whose behaviour you inferred rather than confirmed: say which is which.

A reconstructed diagram records what the system **is**, not what anyone decided — which is precisely what makes it useful for an audit, since the gap between it and an older intended diagram is itself a finding. Ask the operator to correct it; once they have, change its status to `Authored` and log any decisions their corrections reveal in `docs/decisions.md`.

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
