# SECURITY_ASSESSMENT.md

**Stage:** Harden — before merge, and on a recurring cadence.
**Purpose:** Keep the product secure without breaking what works.

## Principles

1. **Security by design (shift-left).** Consider security from discovery onward — build it in, don't bolt it on at the end.
2. **Defense in depth.** Layer controls so no single safeguard is a single point of failure.
3. **Minimize attack surface.** Expose only the endpoints, features, data, and permissions actually needed.
4. **Least privilege.** Grant the minimum access needed, everywhere.
5. **Never trust input.** Validate and encode all data crossing a boundary.
6. **Secrets out of code.** Environment variables / secret stores only.

## Reference standards

Anchor assessments to established frameworks — pick what fits the product:

- **OWASP Top 10** — most critical web application risks.
- **OWASP ASVS** — application security verification requirements; use as a depth guide.
- **OWASP Top 10 for LLM Applications** — risks specific to LLM/AI features.
- **MITRE ATLAS** — adversarial threats & techniques against AI/ML systems.
- **MITRE ATT&CK** — adversary tactics & techniques for threat modeling.
- **NIST SSDF (SP 800-218)** — secure software development practices.
- **NIST CSF** — organizational cyber-risk framework.
- **CIS Benchmarks** — hardening baselines for cloud, OS, and services.

## Baseline review checklist (every change)

- [ ] **Authn/authz on every protected path** — no missing access checks.
- [ ] **Input validation & output encoding** — guard against injection and XSS.
- [ ] **Secrets in env**, never committed.
- [ ] **Dependency risk** — new/updated deps checked for known vulnerabilities.
- [ ] **PII / sensitive data handling** — minimize, protect, don't log.
- [ ] **Safe defaults** — deny by default; fail closed.
- [ ] **Errors don't leak** — no stack traces, secrets, or internals in responses.
- [ ] **Audit sensitive actions** — log security-relevant events.

## Recommended tooling (by coverage)

| Coverage | Recommended tools |
|----------|-------------------|
| SAST (static analysis) | Semgrep, CodeQL, SonarQube |
| Dependency / SCA | `npm audit`, Snyk, Dependabot, OWASP Dependency-Check |
| Secret scanning | gitleaks, TruffleHog, provider secret-scanning |
| DAST (dynamic) | OWASP ZAP, Burp Suite |
| Container / IaC | Trivy, Checkov, tfsec |
| LLM / AI security | garak, prompt-injection & jailbreak test suites (map to MITRE ATLAS) |

Pick tools matching the project's language, framework, and cloud.

## Cadence — mandatory triggers

- **Every PR (automated):** secret-scanning and dependency audit must run and pass in CI — block merge on any new secret or high-severity vulnerability.
- **Every 3 PRs:** run static code analysis (SAST). **Inform the operator first**, then run it and report findings.
- **After each major release:** run a full security audit **on a new branch** and present a **gap analysis** to the operator:
  - Critical security bugs found.
  - **Priorities** (severity + likelihood).
  - An **implementation plan** to fix them.
- **Also trigger immediately** for any change touching auth, payments, or user input.

## Regulated work — IM8 (conditional)

**Only when `docs/PRD.md` declares a government data classification.** Projects with no
classification — personal work included — skip this section entirely; nothing here changes
their flow.

- **Additional, not instead of.** The baseline checklist above still applies. IM8 is a control
  list, not an application-security review; it does not phrase most app-layer bugs as findings.
- **Invoke the `im8-compliance-audit` skill.** It takes the PRD's classification, derives the risk
  band, and reports gaps. **If the skill is unavailable, say so and stop — never improvise IM8
  controls from memory.** Invented control IDs are worse than no audit, and the reader cannot
  tell the difference.
- **Run it early, then before each release.** L0 gaps are hard blockers with no deviation
  permitted, so a first pass at architecture sign-off makes them a design constraint rather than
  late rework. Per-PR is the wrong cadence — the audit needs human input (classification,
  containerised, public-facing, offshore) and cannot be a CI gate.
- **It is not certification.** The audit finds repo-visible gaps. It does not replace the SSP
  process or IDSC/CISO sign-off, and a large share of controls are *not assessable from a repo* by
  design. Say this whenever reporting results — "3 gaps found" reads as a clean bill of health on
  everything else, especially to a non-technical reader.
- **The report is sensitive.** It is a ranked list of weaknesses in a government system. It follows
  the repository's visibility: never write it into a public repo, and when in doubt keep it out of
  version control.
- **Check the catalog's freshness.** The skill reports when the control catalog was last verified.
  Carry that date into whatever you hand over — a stale catalog can misreport a control's level,
  and a missed L1 → L0 promotion tells the agency it may deviate where it may not.

## Data compliance & privacy

- **Flag PII / sensitive data wherever it appears** — names, emails, phone numbers, government IDs, financial, health, biometric, precise location, credentials.
- **Check against applicable regimes** — GDPR, PDPA, and any others relevant to the product's users/region.
- **Recommend fixes to the operator** — data masking, tokenization, encoding, encryption (at rest *and* in transit), data minimization, retention limits, and consent capture where required.
- Never log or expose sensitive data; confirm a lawful basis before collecting it.

## Fix safety

Every security fix must **not break the working product** and must be **rollback-safe** — verify behavior after the fix and ensure a clean revert path if it fails.

## Applying fixes — commit/branch discipline

**One branch, one commit per finding — not a separate branch per fix.** The feature being reviewed needs to be committed first, as the stable "before fixes" base the fix commits sit on top of. Fixes for one bounded feature typically touch the same small set of files, so separate branches would just conflict with each other on merge — and the feature and its fixes are one logical change; main should receive them together, not the feature without its fixes or the fixes without the feature. Separate commits already give most of what separate branches would: each fix is independently readable and revertible (`git revert`), and the PR diff shows a clear list of what changed, without the branch-management overhead.

**Sequence:**

1. Commit the feature as-is (the stable base).
2. Resolve any findings that are policy questions, not code bugs (see below) first, recording the decision in `docs/decisions.md` — other fixes may depend on that answer.
3. Fix remaining findings one at a time. Run the test suite after each. Commit message includes the finding number, e.g. `Fix #3: keep data module out of client bundle`.
4. Restart to a clean state and re-run the scenario-driven Verify pass (see `TESTING.md`) against the acceptance-criteria file.
5. Update the handover doc (e.g. `docs/HANDOVER.md`).
6. Open one PR to `main` listing which findings were fixed and which were accepted (deliberately not fixed, with reasoning). Merge only after review.

**Not every finding is a code defect.** Some are ambiguities the review surfaces that Discovery/Design never fully pinned down — e.g. "is this access restriction actually intended, or is that itself the gap?" Those need a decision, recorded in `docs/decisions.md`, not a code fix — and because other findings' fixes can depend on that decision, resolving policy questions comes before writing bug fixes, not after.

## Defers to

Use `cso` / `security-review` for deep assessment; this SOP defines the baseline checklist, the cadence, and the fix-safety rules.

**Scope split:** this SOP secures the *product* (application security). The *agent workflow itself* — no secrets in prompts, prompt-injection resistance, steering-file integrity, dependency verification, and the human approval gate — is governed by `AGENT_SECURITY.md`, which is always on.
