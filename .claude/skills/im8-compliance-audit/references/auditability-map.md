# Domain auditability map

This file tells the audit which of the 15 IM8 control domains can be meaningfully
checked from a code repository, which need partial external evidence, and which
cannot be assessed from a repo at all. Use it to sort every in-scope control into
one of three buckets: **Compliant**, **Gap**, or **Not assessable from repo**.

The guiding principle: a repository contains source code, config-as-code, pipeline
definitions, and documentation. It does **not** contain running infrastructure
state, cloud-provider settings, organisational records, or contracts. Absence of
evidence in a repo is only a gap for controls that *should* leave a repo artefact.
For everything else, absence is expected and must be reported as "not assessable"
rather than "non-compliant" — otherwise the audit produces false positives.

## Repo-auditable domains (evidence usually present in-repo)

These domains leave concrete, checkable artefacts in a typical application repo.
A missing artefact here is a genuine gap.

### Software Supply Chain (SC)
- SC-1 Code repository with version control → the repo itself; check it is Git.
- SC-3 Peer review before merge → branch protection / CODEOWNERS / required reviewers.
- SC-4 Dependency version pinning → lockfiles (package-lock.json, Pipfile.lock, go.sum, etc.).
- SC-5 Consistent build/release process → CI/CD config, IaC, release scripts.
- SC-6 Install only pinned versions on deploy → `npm ci`, `pipenv sync` in pipeline.
- SC-2 Commit signing (L2) → repo setting; partially visible via signed commits in history.
- SC-7/SC-8 Artefact signing & verification (L2) → cosign/sigstore steps in pipeline.
- SC-9 InnerSource (L2) → org/process; only weak repo signal.

### Secure Development (SD)
- SD-1 Push protection for secrets → repo/platform setting + config files.
- SD-2 Default branch push protection → branch protection rules.
- SD-3 CI tests required before merge (L2) → branch protection + CI config.
- SD-4 Static analysis in pipeline → SAST/IaC scanner job in CI config.
- SD-5 Dependency scanning → SCA job (Dependabot, Trivy, Snyk, etc.) in CI config.
- SD-6 Secret detection → gitleaks/trufflehog/secret-scanning job in CI config.
- SD-7 CI env-var secret masking → CI config (masked/protected variables).
- SD-8 Prod/non-prod environment segregation → IaC / pipeline environment definitions.

### Container Security (CS) — only if the system is containerised
- CS-1 Unique base image tags (L2) → Dockerfile FROM lines.
- CS-2 Minimal base images (L2) → Dockerfile FROM lines.
- CS-3 Runtime secrets, not build-time → Dockerfile / compose / k8s manifests.
- CS-4 Non-root container user → Dockerfile USER instruction.
- CS-5 Dockerfile linting (L2) → hadolint job in CI config.
- CS-6 Read-only root filesystem (L2) → k8s securityContext / compose config.
- CS-7 Image scanning → scanner job in CI / registry config.
- CS-9 Orchestrator API not public → k8s/IaC config (partial; runtime confirms).
- CS-10 Workload segmentation → k8s namespaces / network policies in manifests.
- CS-8 Private registry (L2), CS-11 runtime protection (L2) → partial; mostly runtime.

### Application Security (AS) — partial
- AS-1 Input validation, AS-2 parameterised queries, AS-3 output sanitisation,
  AS-7 access-control checks, AS-9 CSP headers, AS-13 no internal detail leakage,
  AS-14 secure crypto libraries → all visible in source code, though completeness
  requires judgement (you can find evidence of the pattern, not prove exhaustive use).
- AS-8 Secrets management → check for hardcoded secrets + use of a secrets solution.
- AS-5/AS-6/AS-11 password & session params → code may show the logic, but the
  configured *values* must be checked against the agency's chosen parameters.

### Infrastructure Security (IS) — only the Infrastructure-as-Code parts
- IS-2 patch management, IS-4 least functionality, IS-5 host hardening,
  IS-9 EOS assets → visible only if the repo contains IaC / golden-image definitions.
  If infra is click-ops in the console, these become not-assessable.

## Partially-auditable domains (repo gives hints, runtime confirms)

Report findings here as provisional and always pair them with a "needs runtime/cloud
evidence to confirm" note.

- Network Security (NS) — only if IaC (Terraform/CloudFormation) is in the repo;
  otherwise the live VPC/security-group/WAF state is the source of truth.
- Data Protection (DP) — encryption settings may appear in IaC; data residency
  (DP-1, an L0 control) and central tenant management are cloud-account facts.
- Logging & Monitoring (LM) — log-shipping config may be in IaC, but retention,
  alerting, and central forwarding to GCSOC are runtime/operational facts.
- Cryptography & Key Management (CK) — library choice is in code; key rotation
  and establishment are KMS/runtime facts.

## Not assessable from a repo (do not flag as gaps)

State clearly that these require evidence the agency must supply separately. Listing
them is itself valuable — it tells the agency where the audit is blind.

- Access Control (AC) — IAM policies, MFA enforcement, account inventories, access
  reviews, credential rotation all live in the cloud provider / IdP, not the repo.
- Backup & Recovery (BR) — backup existence, retention immutability, and recovery
  testing are operational records.
- Security Programme Management (PM) — SSP, risk assessment, residual-risk approval,
  incident plan, documentation are governance documents (note: all L0 PM controls
  fall here).
- Third Party Management (TP) — contracts, offshore arrangements, attestation reports.
- Datacentre (DC) — physical facility controls.
- Several Infrastructure Security (IS) controls — management agents, malware
  protection, EDR, remote admin tooling, time sync, domain registration, SMS Sender
  ID — are runtime/operational/central-registry facts.

## Important reminders

- Container Security only applies if the system actually uses containers. If it does
  not, mark the whole CS domain "not applicable" rather than "gap".
- Public-facing-only controls (ST-3 public VDP, IS-11/13/14 domain & SMS registration,
  AC-7 Singpass/Corppass) are not applicable to internal-only systems.
- SaaS / offshore controls (TP-1, TP-3, TP-5, and SaaS handling in BR-1/ST-1/ST-4)
  apply only if the system uses SaaS or offshore development.
- When uncertain whether a finding is a real gap or just an artefact living outside
  the repo, default to "not assessable" and explain what evidence would settle it.
  Over-reporting gaps erodes trust in the audit more than under-reporting does.
