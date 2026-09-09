---
name: im8-compliance-audit
description: Audit a code repository against the Singapore Government's IM8 (ICT&SS Policy Reform) security controls to surface compliance gaps. Use this whenever the user wants to check, audit, assess, or review a repo for IM8 compliance, IM8 controls, GovTech tech-standards, Singapore government security standards, or asks "is this repo IM8-compliant" / "what IM8 gaps does this codebase have". Trigger even if the user only mentions "the security standards" in a Singapore government context, or names a data classification (Restricted, Confidential, Sensitive) alongside a repo. The skill takes the system's data classification as input, derives the risk band, pulls the matching controls from the GovTechSG/tech-standards GitHub repo, and reports what is covered, what the gaps are, and what cannot be assessed from a repo alone.
---

# IM8 Compliance Audit

This skill audits a repository against Singapore's IM8 ICT&SS controls and produces
a gap report. The point is not to claim full compliance certification — it is to
honestly show the agency three things: what the repo demonstrably covers, where the
gaps are, and which controls a repo simply cannot speak to. That third category
matters as much as the first two; reporting a control as "failed" when it just lives
outside the repo (in the cloud console, in a contract, in a governance document)
produces false alarms and erodes trust in the audit.

## The audit flow

Work through these steps in order. Don't skip the classification step — the entire
control set depends on it.

### 1. Establish data classification → risk band

The risk band is *not* something you can read from the code. It comes from the
highest government data classification the system handles. Ask the user for it if
they haven't given it. Read `references/risk-classification.md` for the exact mapping;
in short:

- Restricted / Sensitive (Normal) / Open → **low-risk**
- Confidential / Sensitive (High) → **medium-risk**
- Secret / CII and above → **high-risk** (not in the repo — handle per the reference file)

If the user is unsure, help them classify by asking what the most sensitive single
data element in the system is, rather than guessing. State the derived band back to
them before proceeding so they can correct it.

### 2. Establish scope-affecting system characteristics

A few domains are conditional. Confirm (briefly — infer from the repo where you can,
ask only what you can't determine):

- Is the system **containerised**? (If not, the Container Security domain is *not
  applicable*, not a gap.)
- Is it **public-facing** or internal-only? (Affects public VDP, domain/SMS
  registration, Singpass/Corppass controls.)
- Does it use **SaaS** components or **offshore development**? (Affects Third Party
  Management and some SaaS-specific control variants.)
- Which **target level** to assess? Default to L0 + L1 as pass/fail and surface L2
  as best-practice opportunities (this matches the default SSP templates).

### 3. Pull the IM8 controls

Before loading controls, run the freshness check from the skill root:

```bash
python scripts/refresh_catalog.py
```

Read the JSON output and act on `status`:

- **`current`** — snapshot is up-to-date. Load from `references/catalog-snapshot.json`.
  Include the `snapshot_date` and `checked_at` in the audit summary table.
- **`updated`** — the script has downloaded the live catalog, diffed it, and written
  the updated snapshot. Load from `references/catalog-snapshot.json`. **Surface the
  `changes` list to the user before the audit findings** — a level promotion (e.g. a
  control moving from L1 to L0) or a new control may change the severity of findings
  in this very audit.
- **`fetch_failed`** — network unavailable or rate-limited. Load the snapshot anyway,
  note the `message` in the audit summary, and flag that the catalog version may be
  out of date. Full manual refresh instructions are in `references/risk-classification.md`.

  Report the freshness honestly using `checked_at` / `days_since_check`. A snapshot's
  own `snapshot_date` only says when GovTech last *changed* the catalog — on its own it
  cannot distinguish "unchanged since then" from "not checked since then". If
  `checked_at` is `null`, this machine has never verified the catalog: say so plainly,
  because a level promotion missed here (a control moving L1 → L0) turns a finding the
  agency believes it can deviate from into one it cannot.

Then build the in-scope control set: from the snapshot's `profile_levels` field,
collect all control IDs where the band (e.g. `"low"`) has a level value ≤ target
level (e.g. 1 for L0+L1). Resolve each ID against `controls` for title, statement,
and params. Details in `references/risk-classification.md`.

### 4. Evaluate the repository against each in-scope control

For every control in scope, classify it into exactly one of three buckets. Use
`references/auditability-map.md` — it lists, domain by domain, which controls leave
repo artefacts and which don't. This is the heart of avoiding false positives.

- **Compliant** — concrete evidence in the repo satisfies the control. Cite the
  evidence (file path, config block, pipeline step, branch-protection setting).
- **Gap** — the control *should* leave a repo artefact and that artefact is missing
  or misconfigured. Cite what's missing and what would fix it.
- **Not assessable from repo** — the control's evidence lives outside a repository
  (cloud console, IAM, contracts, governance docs, physical facility). Do not call
  this a gap. Name what evidence the agency would need to supply to close the
  assessment.

Tag each Gap with its level-derived severity: L0 gaps are hard blockers (no deviation
allowed), L1 gaps need remediation or a documented IDSC-approved deviation, L2 items
are opportunities.

**Parameterised controls require separate handling.** The catalog intentionally ships
all 47 parameters blank — the blanks are obligations, not omissions. For every in-scope
parameterised control, consult `references/parameter-guide.md` which classifies each
parameter into one of three types:

- **Repo-inferable (R)** — value is visible in source code or config. Read it, report
  it, and flag whether it looks acceptable against guidance values in the reference.
  The agency must still explicitly document it in their SSP.
- **Operational threshold (O)** — agency-chosen value implemented in infrastructure
  or process; nothing in the repo can confirm it. Flag as an SSP documentation
  obligation and include the guidance range from the reference.
- **Governance/people (G)** — a named person, team, service, or location. Never in
  source code. Flag as an SSP documentation obligation.

All three types feed into the **SSP parameter checklist** section of the report — not
just the repo-visible ones. A parameter that sits in the not-assessable domain still
requires the agency to document it. Losing it in the not-assessable section means the
agency walks away not knowing they have an unfilled SSP obligation.

### 5. Produce the report

Use the structure below exactly. All sections that list control IDs use tables —
they are easier to scan and act on than prose lists.

## Report structure

```
# IM8 Compliance Audit — [repo name]

## Summary

| Field                  | Value |
|------------------------|-------|
| Data classification    | [what the user gave] |
| Derived risk band      | [low / medium / high] |
| Catalog version        | [last-modified field from im8-reform.json metadata] |
| Catalog last verified  | [checked_at, or "never verified on this machine"] |
| Levels assessed        | [e.g. L0 + L1 as pass/fail; L2 as opportunities] |
| System characteristics | [containerised? public-facing? SaaS? offshore?] |
| Controls in scope      | [exact count — never approximate] |
| Compliant              | [exact count] |
| Gaps (L0+L1)           | [exact count] |
| Platform-unconfirmed   | [exact count] |
| Not assessable         | [exact count] |
| Not applicable         | [exact count] |

> This audit measures the repo against the published baseline. It does not replace
> the formal SSP process or IDSC/CISO sign-off. Some apparent gaps may already be
> covered by an approved deviation in the agency's SSP.

## ⚠️ Pre-audit flags
[Any issues that affect the audit's own validity — e.g. contradictions between the
user-supplied classification and something found in the repo (a doc calling itself
medium-risk when the user said low-risk), version mismatches, or scope ambiguities.
These must be resolved before the findings can be relied upon. If there are none,
omit this section.]

## Critical gaps (Level 0 — mandatory, no deviation permitted)

| Control | Title | What's missing | How to fix |
|---------|-------|---------------|------------|
| [id]    | ...   | ...           | ...        |

[If none: state plainly "No L0 repo-auditable gaps found." Then note which L0
controls exist in-scope but are not assessable from a repo (they appear in the
Not assessable section) — L0 controls that live outside the repo still require
confirmation in the SSP.]

## Significant gaps (Level 1 — remediate or record an approved deviation)

| Control | Title | Evidence of gap | Remediation |
|---------|-------|-----------------|-------------|
| [id]    | ...   | ...             | ...         |

## Unconfirmed platform settings
[Controls whose evidence lives in a platform/cloud console setting rather than the
repo itself — e.g. branch protection, push protection, environment segregation in
the CI/CD platform. The repo contains no artefact to confirm or deny these. They
are not "gaps" (the setting may well be on) but they cannot be called "compliant"
either. The agency should screenshot or export the relevant settings and attach them
to the SSP.]

| Control | Title | Setting to confirm | Where to check |
|---------|-------|--------------------|----------------|
| [id]    | ...   | ...                | ...            |

## Best-practice opportunities (Level 2)

| Control | Title | Suggestion |
|---------|-------|------------|
| [id]    | ...   | ...        |

## Covered controls

| Control | Title | Status | Evidence |
|---------|-------|--------|----------|
| [id]    | ...   | Compliant / Partial | [file path or config reference] |

[Use "Partial" when the mechanism exists but coverage cannot be proven exhaustive
from the repo — e.g. input validation is present but not demonstrably applied to
every input. Add a brief note for Partial entries.]

## Not applicable

| Control | Title | Reason |
|---------|-------|--------|
| [id]    | ...   | [e.g. No containers — CS domain N/A; internal-only — ST-3 N/A] |

## Not assessable from this repository
[Open with a paragraph explaining that a repo audit is structurally blind to
evidence that lives in the cloud account, IAM/IdP, backup systems, contracts, and
governance documents. Absence here is expected, not a finding.]

| Domain | Controls | Evidence the agency must supply |
|--------|----------|----------------------------------|
| [name] | [id list]| [specific artefact or record] |

## SSP parameter checklist

Parameters are mandatory SSP documentation obligations — the catalog ships them blank
intentionally. This section covers ALL in-scope parameterised controls regardless of
whether a repo artefact exists. Consult `references/parameter-guide.md` for
classification, guidance values, and authoritative sources.

### Parameters found in repo — confirm value and document in SSP

| Control | Title | Parameter | Found value | Acceptable? | SSP action |
|---------|-------|-----------|-------------|-------------|------------|
| [id]    | ...   | [param id]| [file:line] | [yes/flag]  | Document this value |

### Parameters requiring SSP documentation (no repo signal)

Operational thresholds and governance/people parameters that the agency must set and
record in the SSP. These are not gaps in the repo — they are obligations that must be
met in the SSP regardless of what the repo contains.

| Control | Level | Title | Parameter | Type | Guidance value |
|---------|-------|-------|-----------|------|----------------|
| [id]    | L0/L1/L2 | ... | [param id + label] | O/G | [from parameter-guide.md] |

## Security observations beyond the control list
[Anything substantive found during the audit that doesn't map cleanly to a single
control — stale dangerous comments, conditional security code paths, dependency
version anomalies, undocumented fallbacks. These are not IM8 findings but they
matter. If there is nothing to report, omit this section.]
```

## Important guidance

- **Count controls precisely.** The summary table shows exact numbers. "~14
  compliant" is not acceptable — resolve ambiguities before reporting.
- **Record the catalog version and when it was last verified.** The `im8-reform.json`
  metadata has a `last-modified` date; the freshness check reports `checked_at`. Include
  both — the first makes the audit reproducible, the second tells the reader how much to
  trust it. An old `last-modified` with a recent `checked_at` is fine; an unknown
  `checked_at` is not.
- **Four buckets, not three.** Gap / Compliant / Not assessable are the three
  inherited buckets; add **Unconfirmed platform settings** as a fourth for controls
  whose evidence lives in a console UI rather than the repo. This prevents both
  false positives (calling it a gap when the setting may be on) and false negatives
  (calling it compliant when you can't see it).
- **Not applicable is its own category.** N/A controls (no containers → CS domain
  N/A; OTP-only auth → AS-5 N/A) belong in the N/A table, not buried in parameters
  or silently omitted.
- **Default to "not assessable" over "gap" when uncertain.** A false gap sends the
  agency chasing a non-problem and erodes trust in the rest of the report.
- **Cite evidence for every Compliant and Gap finding.** "SC-4 satisfied" is weak;
  "SC-4 satisfied — package-lock.json present with pinned versions" is auditable.
- **Don't claim completeness on source-code controls.** You can find evidence that
  input validation exists (AS-1); you can't prove it's applied to every input. Use
  "Partial" status and a brief note.
- **Surface security observations that fall outside the control list.** The most
  valuable audit findings sometimes aren't a named IM8 control — a stale TLS-bypass
  comment, a conditional DB connection that skips encryption, an undocumented
  fallback. Capture them in the final section.
- **The repo is the published reference, not the agency's SSP.** It gives control
  definitions without the agency's chosen parameter values or approved deviations.
  Frame findings as "gaps relative to the published baseline" and note that approved
  deviations in the agency's SSP may already cover some of them.
