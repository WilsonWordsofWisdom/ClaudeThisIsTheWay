# SSP parameter documentation guide

Every parameterised control requires the agency to explicitly choose and record a
value in its System Security Plan. The catalog intentionally ships these blank — the
blanks are obligations, not oversights. This file classifies all 30 parameterised
controls by how the audit should handle each parameter, and provides guidance values
where authoritative sources exist.

## Parameter classes

**Repo-inferable (R)** — the value is visible in source code or pipeline config.
The audit reports the found value; the agency must confirm it is acceptable and
document it in the SSP.

**Operational threshold (O)** — the agency chooses the value; it is implemented in
infrastructure, operations, or process. The repo has no signal. The audit flags the
obligation and suggests a reference range.

**Governance/people (G)** — inherently organisational: a named person, team, service,
or location. Never present in source code. The audit flags the obligation.

**Choice (C)** — a selection from a fixed list defined in the catalog. If the
mechanism is found in the repo, the audit can often infer the correct choice.

---

## Application Security

### AS-5 Password Requirements | low-L1, medium-L1
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| as-5_prm_1 | R | Minimum password length (characters) | NIST SP 800-63B: minimum 8 chars for user-set passwords; Singapore government practice typically 12+. Check the validation logic. |
| as-5_prm_2 | R | Password policy (e.g. "not a commonly used password") | Check what the code enforces (blocklist, complexity rules, etc.). NIST 800-63B recommends length over complexity. |

If the system uses OTP/passwordless auth exclusively, mark AS-5 as N/A and record
the rationale in the SSP — the control explicitly carves out SSO/passwordless.

### AS-11 Session Management | low-L1, medium-L1
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| as-11_prm_1 | R | Maximum session duration (hours) | NIST SP 800-63B: 12h or 30-min inactivity for AAL2; 12h or 15-min inactivity for AAL3. A 30-day session for Restricted data is very likely non-compliant — flag explicitly. |

---

## Security Testing

### ST-1 Vulnerability Assessment | low-L1, medium-L0
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| st-1_prm_1 | G | Type of VA scanning (agent-based / network-based) | Agency chooses based on architecture. |
| st-1_prm_2 | O | Frequency (days) | GovTech WOG VMS guidance: at least every 30 days for internet-facing systems. |

### ST-3 Public Vulnerability Disclosure Programme | low-L1, medium-L0
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| st-3_prm_1 | G+C | Channel type (security.txt / HackerOne / email) | Agency chooses. security.txt standard (RFC 9116) is the simplest. Check for `public/.well-known/security.txt` in the repo. |

### ST-4 Security Testing Programme | low-L1, medium-L0
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| st-4_prm_1 | G | Type (penetration test / bug bounty / red team) | WOG Security Testing Guidelines recommend penetration test as default. |
| st-4_prm_2 | O | Frequency (days) | Typically 365 days (annually) or after major changes. |

### ST-5 Vulnerability Management | low-L1, medium-L1
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| st-5_prm_1 | O | Critical remediation SLA (days) | CISA KEV guidance + SG gov practice: 7 days. |
| st-5_prm_2 | O | High remediation SLA (days) | Typical: 30 days. |
| st-5_prm_3 | O | Medium remediation SLA (days) | Typical: 90 days. |
| st-5_prm_4 | O | Low remediation SLA (days) | Typical: 180 days. |

---

## Backup and Recovery

### BR-1 Backup | low-L1, medium-L0
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| br-1_prm_1 | O | Backup frequency (days) | Typical for production: 1 day (daily). Check cloud backup service config. |

### BR-2 Recovery Testing | low-L2, medium-L1
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| br-2_prm_1 | O | Recovery test frequency (days) | Typical: 180 days (semi-annually) or 365 days (annually). |

### BR-3 Backup Retention | low-L1, medium-L1
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| br-3_prm_1 | O | Retention period (days) | Minimum 90 days is common; align with agency data retention policy. Check S3 Object Lock / Azure immutability config. |

---

## Data Protection

### DP-1 Data Residency | low-L1, medium-L0
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| dp-1_prm_1 | G | Country | Must be Singapore for government data. Confirm the cloud region in infra config or cloud console. |

---

## Logging and Monitoring

### LM-8 Security Log Retention | low-L1, medium-L1
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| lm-8_prm_1 | O | Retention period (days) | NIST SP 800-92 and Singapore PDPA practice: 365 days (1 year) minimum. Check log lifecycle / S3 retention policy config. |

### LM-12 Central Security Log Management | low-L0, medium-L0
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| lm-12_prm_1 | G | Central SIEM/monitoring service name | For GCC tenants: GCSOC. Agency must name the service — "GCSOC" is the default for GCC-hosted systems. |

---

## Access Control

### AC-3 Inactive and Expired Accounts | low-L1, medium-L0
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| ac-3_prm_1 | O | Days after last authorised use before disabling | Typical: 30 days. |
| ac-3_prm_2 | O | Days of inactivity before disabling | Typical: 90 days. |
| ac-3_prm_3 | G | Account type in scope (privileged / all / IAM) | Agency defines which account types this applies to. |

### AC-4 Access Review | low-L1, medium-L1
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| ac-4_prm_1 | O | Review frequency (e.g. "quarterly") | Typical: quarterly or semi-annually. |
| ac-4_prm_2 | O | Days to remove access after review identifies it as unnecessary | Typical: 7–14 days. |

### AC-8 Automated Account Lifecycle Management | low-L1, medium-L1
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| ac-8_prm_1 | G | Process to automate (provisioning / deprovisioning / both) | Agency defines scope. |
| ac-8_prm_2 | G | Tool name (e.g. SCIM, WOG AAD, Okta) | Agency names the specific tool. |

### AC-13 Static Credential Rotation | low-L2, medium-L2
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| ac-13_prm_1 | O | Rotation period (days) | Typical: 90 days. Prefer short-lived tokens (AWS STS, etc.) over rotation where possible. |

---

## Container Security

### CS-7 Container Image Scanning | low-L1, medium-L1
| Param | Class | Label | Choices | Guidance |
|-------|-------|-------|---------|----------|
| cs-7_prm_1 | R+C | Scanning location | CI/CD pipeline, container registry | If a scanner job exists in CI config → "CI/CD pipeline". If only registry scanning → "container registry". Repo-inferable. |

---

## Security Programme Management

### PM-2 Risk Assessment | low-L1, medium-L1
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| pm-2_prm_1 | G | System owner name/role | Named in the SSP. |
| pm-2_prm_2 | G | Risk assessment approver name/role | Named in the SSP. |
| pm-2_prm_3 | G+C | Use case | SaaS subscription / initial full release | Agency selects which applies. |
| pm-2_prm_4 | O | Review frequency (days) | Typical: 365 days (annually) or when major changes. |

### PM-4 Approval of Residual Risks | low-L0, medium-L0
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| pm-4_prm_1 | G | Approving authority (IDSC / agency CIO / CISO) | L0 control — this value must be set. Cannot be left blank. |

### PM-7 SaaS Certification | (SaaS systems only)
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| pm-7_prm_1 | G | Required certifications (e.g. ISO 27001, SOC 2 Type II) | Agency specifies which certifications are required from the SaaS provider. |

### PM-8 SaaS Whitelisting | (SaaS systems only)
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| pm-8_prm_1 | G | Whitelisting authority | Agency names the body that maintains the approved SaaS list. |

---

## Infrastructure Security

### IS-9 End-of-Support Assets | low-L1, medium-L1
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| is-9_prm_1 | G | Asset type (software / hardware / OS / all) | Agency defines scope. Check dependency manifests and container base images for EOS versions. |

---

## Secure Development

### SD-4 Static Analysis | low-L1, medium-L1
| Param | Class | Label | Choices | Guidance |
|-------|-------|-------|---------|----------|
| sd-4_prm_1 | R+C | SAST location | CI/CD pipeline, static analysis platform | Check CI config for a SAST job (CodeQL, Semgrep, etc.). Repo-inferable. |

### SD-5 Dependency Scanning | low-L1, medium-L1
| Param | Class | Label | Choices | Guidance |
|-------|-------|-------|---------|----------|
| sd-5_prm_1 | R+O | Scan frequency (days) | — | Check CI config or Dependabot schedule. Typical: 7 days. Repo-inferable if scheduled. |
| sd-5_prm_2 | R+C | Scan location | CI/CD pipeline, code repository, dependency scanning platform | Repo-inferable from CI/Dependabot config. |

### SD-6 Secret Detection | low-L1, medium-L1
| Param | Class | Label | Choices | Guidance |
|-------|-------|-------|---------|----------|
| sd-6_prm_1 | R+C | Detection location | CI/CD pipeline, code repository, secret detection platform | Check for gitleaks/trufflehog/platform push-protection in CI. Repo-inferable. |
| sd-6_prm_2 | O | Remediation SLA (days) | — | Typical: 1–3 days for exposed credentials; document in SSP. |

---

## Third Party Management

### TP-2 Third Party Audit | (applicable systems only)
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| tp-2_prm_1 | G | Audit type (SOC 2 / ISO 27001 / penetration test) | Agency specifies. |
| tp-2_prm_2 | O | Frequency (days) | Typical: 365 days. |

### TP-4 Attestation Report Review | (applicable systems only)
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| tp-4_prm_1 | G | Attestation type (SOC 2 Type II / ISO 27001) | Agency specifies. |
| tp-4_prm_2 | O | Review frequency (days) | Typical: 365 days (each time a new report is issued). |

### TP-5 Qualified Offshore Development Centre | (offshore dev only)
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| tp-5_prm_1 | G | ODC type | Agency specifies the engagement model. |

### TP-6 Supplier Assessments and Reviews | (applicable systems only)
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| tp-6_prm_1 | G | Assessing party (agency / GovTech / third-party auditor) | Agency names who conducts the assessment. |

---

## Cryptography

### CK-2 Cryptographic Key Rotation | low-L2, medium-L1
| Param | Class | Label | Guidance |
|-------|-------|-------|----------|
| ck-2_prm_1 | O | Rotation period (days) | NIST SP 800-57: context-dependent; typical for symmetric keys: 365 days. AWS KMS / Azure Key Vault support automatic rotation. |

---

## Summary counts
- Total parameterised controls in catalog: 30
- Total individual parameters: 47
- Repo-inferable (R or R+C): as-5 (×2), as-11, cs-7, sd-4, sd-5 (×2), sd-6 (×2) = **9 params**
- Governance/people (G): pm-2 (×3), pm-4, pm-7, pm-8, ac-8 (×2), ac-3_prm_3, dp-1, lm-12, tp-2_prm_1, tp-4_prm_1, tp-5, tp-6, is-9, st-1_prm_1, st-3, st-4_prm_1 = **17 params**
- Operational thresholds (O): st-1_prm_2, st-4_prm_2, st-5 (×4), br-1, br-2, br-3, lm-8, ac-3 (×2), ac-4 (×2), ac-13, ck-2, pm-2_prm_4, sd-5_prm_1, sd-6_prm_2 = **21 params**
