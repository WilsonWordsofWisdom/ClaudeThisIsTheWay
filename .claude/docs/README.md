# docs/

The project's living documents. Each is governed by an SOP and maintained across the whole
lifecycle rather than written once (see `~/.claude/CLAUDE.md` §5).

| File | Governed by | Holds |
|------|-------------|-------|
| `PRD.md` | `sop/PRODUCT_BRIEF.md` | Problem, users, critical journeys, success metrics + north star, non-goals, data classification |
| `decisions.md` | `sop/PRODUCT_BRIEF.md` (business) · `sop/ARCHITECTURE.md` (technical) | Append-only dated record of what was decided, and why |
| `design.md` | `sop/DESIGN_GUIDE.md` | Current layouts, key screens, visual language |
| `architecture.md` | `sop/ARCHITECTURE.md` | Current Mermaid diagram of the system |
| `troubleshooting.md` | `sop/ENGINEERING.md` | Problems that recur: symptom, cause, fix, dead ends |
| `tests/*.feature` | `sop/TESTING.md` | Gherkin scenarios, one file per PRD journey |
| `ArchitectureDiagram.drawio` | `docs/ArchitectureDiagram.drawio` | Detailed architecture diagram used alongside architecture.md |

`PRD.md`, `design.md`, and `architecture.md` each carry a **Status** — `Authored`,
`Reconstructed`, or `Draft`. `Reconstructed` means the document was inferred from existing
code: it describes what the system *is*, not what was decided, and its judgement-based
sections are unverified until the operator confirms them.

Produced on demand rather than kept as standing documents: the security gap analysis
(`sop/SECURITY_ASSESSMENT.md`) and the product-analytics page (`sop/ANALYTICS.md`).

**Traceability:** PRD journeys → `tests/` → E2E coverage; PRD north star → analytics.
