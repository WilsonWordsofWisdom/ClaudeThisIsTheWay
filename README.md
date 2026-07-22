# ClaudeThisIsTheWay
Setup for Claude Code for a great and standardized vibe coding experience

## Claude Code Development Lifecycle & SOPs

| # | Stage | SOP file | Purpose | CLAUDE.md would trigger it... |
|---|-------|----------|---------|-------------------------------|
| 1 | Discovery | PRODUCT_BRIEF.md | Problem, users, success metrics, scope & non-goals | Before starting any new feature/project |
| 2 | Design | DESIGN_GUIDE.md | UX/UI standards, visual language, a11y, component patterns | When building or changing UI |
| 3 | Architecture | ARCHITECTURE.md | System/data design, tech selection, module boundaries | Before implementing anything multi-part |
| 4 | Build | ENGINEERING.md | Coding standards, patterns, error handling, git hygiene | During implementation |
| 5 | Verify | TESTING.md | Test strategy, TDD, what "verified" means | Writing/running tests before claiming done |
| 6 | Harden | SECURITY_ASSESSMENT.md | Threat modeling, secrets, authn/z, injection, deps | Before merge — esp. auth/payments/user input |
| 7 | Measure | ANALYTICS.md | Instrumentation, events, metrics, post-launch review | When adding tracking / after launch |

## This Is The Way Forward
When you start the next project, CLAUDE.md §5 fires stage by stage and I scaffold this docs/ tree:

your-next-project/
├─ CLAUDE.md              ← project-specific overrides (stack, ports, conventions)
└─ docs/
   ├─ PRD.md              ← created first (PRODUCT_BRIEF.md → problem, journeys, north star, tech reqs)
   ├─ decisions.md        ← append-only, dated business + technical decisions
   ├─ design.md           ← created when UI work starts (Material Design default; mockup offered first)
   ├─ architecture.md     ← created before multi-part build (Mermaid + cloud reference architecture)
   └─ tests/
      └─ *.feature        ← Gherkin, one per PRD journey → drives E2E coverage

## May the force be with Claude
The development lifecycle loop it enforces:

PRODUCT_BRIEF → DESIGN → ARCHITECTURE → ENGINEERING → TESTING → SECURITY → ANALYTICS
     │ PRD          │ mockup    │ diagram +    │ DRY/secure   │ Gherkin    │ OWASP/    │ HEART +
     │ + journeys   │ gate      │ cloud arch   │ + PR file:ln │ E2E        │ ATLAS/    │ SLO dash
     │              │           │              │              │            │ NIST      │
     └──────────────┴───────────┴──── docs/decisions.md (updated throughout) ──────────┘
                    PRD journeys → tests ;  PRD north star → analytics  (traceability)


## Installation

These files live in your **global** Claude config at `~/.claude/`. The install
**merges** them in — it replaces your `CLAUDE.md` and adds `sop/` + `docs/`,
while leaving your existing skills, plugins, settings, and auth untouched.

### Recommended (safe merge)

```bash
# 1. Back up your current global Claude setup
cp -R ~/.claude "$HOME/.claude.backup.$(date +%Y%m%d%H%M%S)"

# 2. Clone this repo to a temp folder
git clone https://github.com/WilsonWordsofWisdom/ClaudeThisIsTheWay.git /tmp/claude-tiw

# 3. Merge the standards into ~/.claude (creates it if missing)
mkdir -p ~/.claude
cp -R /tmp/claude-tiw/.claude/. ~/.claude/

# 4. Clean up
rm -rf /tmp/claude-tiw
```

Your global `CLAUDE.md` is now replaced with this one, and `~/.claude/sop/`
and `~/.claude/docs/` are added. Restore anytime from the backup folder.

### Brand-new users (no existing ~/.claude)

```bash
git clone https://github.com/WilsonWordsofWisdom/ClaudeThisIsTheWay.git /tmp/claude-tiw
mkdir -p ~/.claude && cp -R /tmp/claude-tiw/.claude/. ~/.claude/ && rm -rf /tmp/claude-tiw
```

### Per-project docs scaffold

When starting a new project, copy the living-doc templates into it:

```bash
cp -R ~/.claude/docs <your-project>/docs
```

> ⚠️ **Do not** `rm -rf ~/.claude` to "replace" your setup — that deletes your
> installed skills, plugins, MCP servers, settings, and sign-in. The merge
> above is all you need.