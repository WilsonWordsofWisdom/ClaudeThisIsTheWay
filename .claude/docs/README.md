# docs/ scaffold

Reusable template for a project's `docs/` folder. On a new project, copy these files into `<project>/docs/` and fill them in as each lifecycle stage is reached.

They are **living documents** — created early and updated across the whole lifecycle (see `~/.claude/CLAUDE.md` §5 and `~/.claude/sop/`).

| File | Standard SOP | When it's created |
|------|--------------|-------------------|
| `PRD.md` | `sop/PRODUCT_BRIEF.md` | Discovery — first |
| `decisions.md` | `sop/PRODUCT_BRIEF.md` + `sop/ARCHITECTURE.md` | Appended throughout |
| `design.md` | `sop/DESIGN_GUIDE.md` | When UI work starts |
| `architecture.md` | `sop/ARCHITECTURE.md` | Before multi-part build |
| `tests/*.feature` | `sop/TESTING.md` | Per PRD journey |

**Not templated here** (produced on demand, not standing docs): the security gap-analysis (`sop/SECURITY_ASSESSMENT.md`, after each major release) and the product-analytics page (`sop/ANALYTICS.md`, after first release).

**Traceability:** PRD journeys → `tests/` → E2E coverage; PRD north star → analytics.
