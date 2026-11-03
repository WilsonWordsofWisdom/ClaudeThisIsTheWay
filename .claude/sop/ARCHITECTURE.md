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

**Preserve before/after, don't overwrite in place.** When an approved architecture decision changes the diagram, keep the prior version visible: a "Before (baseline)" section and an "After (to-be)" section, each with its own Mermaid diagram (Mermaid-in-markdown can't render two diagrams side by side, so this is sequential). In the "After" diagram, use `classDef`/`class` to color new components distinctly (e.g. `fill:#d5e8d4,stroke:#82b366` — green) from modified components (e.g. `fill:#fff2cc,stroke:#d6b656` — amber) and unchanged ones, with a one-line legend. For cases where a true side-by-side view matters (e.g. presenting to a client), maintain a companion `.drawio` file with a two-column layout, row-per-layer, the same highlight colors, and a legend.


## Reconstructing a diagram from existing code

When the diagram was never produced, derive it from what's there. Read the code before drawing: entry points, module boundaries and their dependencies, data stores, external services called, and whatever deployment surface appears in config.

Draw it in layers, going only as deep as the project warrants:

1. **Context** — the system as a single box, the people (users, operators) who use it, and the external systems it talks to (third-party APIs, identity providers, payment, email), with a short label on each relationship. No internal detail; a non-technical reader should understand it at a glance.
2. **Container** — inside the system boundary: each separately running or deployable unit (web app, API, worker, database, queue, cache, file store), its technology, and how containers communicate (protocol, sync vs. async). A "container" is a process or data store, not a Docker container.
3. **Component** — inside one container (usually the main application): its modules or major building blocks (controllers, services, repositories, adapters), what each is responsible for, and who depends on whom. Show the direction of dependency and the external calls each component makes.
4. **Code** — inside a single component: its classes, interfaces, functions and types, how they relate (inheritance, composition, calls), and the data shapes that cross its boundary. Draw it only for components that are complex, critical or risky, never for the whole system.

### Keeping the layer sheets current in the `.drawio` file

The companion `.drawio` file has one sheet (page) per layer — Context, Container, Component, Code — in addition to the side-by-side overview. Treat the sheets as living documents that move with the code:

- **Update in the same change that causes the drift.** When a PR adds, removes, renames or re-wires something a layer shows, update that layer's sheet (and the matching Mermaid diagram in `docs/architecture.md`) before merge. Don't batch diagram updates for later.
- **Know which sheet a change touches:**

  | Change | Sheet(s) to update |
  |--------|--------------------|
  | New/removed user type or external system or third-party API | Context (and Container if a new integration point appears) |
  | New/removed service, worker, datastore, queue, or a changed protocol between them | Container |
  | New/removed/split/merged module in a container, or a changed dependency direction | Component |
  | Changed classes, interfaces or data shapes inside a component that has a Code sheet | Code |

  A change at a lower layer usually leaves the layers above untouched; a change at a higher layer almost always requires checking the layers below it.
- **Only add a Code sheet when warranted.** Create one per complex, critical or risky component, named after it (e.g. `Code – Auth`). Don't create empty or placeholder Code sheets.
- **Keep sheets consistent with each other.** A box that appears on more than one sheet must have the same name everywhere, and each sheet should reference the one above and below it (e.g. a label such as "see Component sheet") so the hierarchy stays navigable.
- **Apply the before/after convention per sheet.** Use the same colors (green = new, amber = modified, unchanged = default) and legend on every sheet touched by an approved decision; reset to the new baseline once the change is merged and released.
- **Edit the existing sheet, don't recreate it.** Preserve the operator's layout, styles and any manual positioning; change only the elements affected. Keep the `.drawio` XML valid (unique cell ids, edges pointing at existing cells) and confirm the file still opens.
- **Flag mismatches.** If a sheet and the code disagree and the intent is unclear, ask the operator which is right rather than silently "fixing" either, and log any resulting decision in `docs/decisions.md`.

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
