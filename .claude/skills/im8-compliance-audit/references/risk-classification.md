# Risk classification and control resolution

## How data classification maps to risk band

IM8 does not define risk bands inside the GitHub repo — the band is determined by
the highest **government data classification / sensitivity level** the system
handles. The public portal makes the mapping explicit in each SSP's "System
Characteristics":

| Data sensitivity of the system                     | Risk band   | Repo profile prefix |
| -------------------------------------------------- | ----------- | ------------------- |
| Up to **Restricted**, **Sensitive (Normal)**       | Low-risk    | `low-risk-*`        |
| **Confidential**, **Sensitive (High)**             | Medium-risk | `medium-risk-*`     |
| Critical Information Infrastructure (**CII**)/higher| High-risk   | *(not in repo yet)* |

So the audit's first job is to ask the user for the system's data classification,
then derive the band:

- "Official (Open)" / "Restricted" / "Sensitive Normal" → **low-risk**
- "Confidential" / "Sensitive High" → **medium-risk**
- "Secret" / "Top Secret" / CII → **high-risk** → the OSCAL profiles do NOT exist
  in this repo. Tell the user the repo only covers low- and medium-risk cloud, point
  them to the portal (https://info.standards.tech.gov.sg/ssp/high-risk-cloud/), and
  offer to audit against the medium-risk baseline as a *floor* with a clear caveat
  that high-risk adds controls not captured here.

If the user is unsure of their classification, ask what the most sensitive single
piece of data in the system is (e.g. citizen NRIC + financial records → likely
Confidential; published public information → likely Restricted/Open). Do not guess
silently — the band drives the entire audit.

## Profile levels (what each level means for a finding's severity)

Each band has three cumulative levels. Pull the controls for every level up to and
including the one the user wants assessed (default: assess L0 + L1, and surface L2
as best-practice opportunities — this matches the default SSP templates).

- **Level 0 — cardinal, mandatory. No deviation permitted.** A gap here is a hard
  blocker. Report at highest severity.
- **Level 1 — basic hygiene baseline.** A gap is significant but may be covered by a
  documented, IDSC-approved deviation in the agency's SSP. Report as a gap that needs
  either remediation or a recorded deviation.
- **Level 2 — best-practice enhancements.** Report as an opportunity, not a failure.

## Loading controls for the audit

The canonical source of truth is `references/catalog-snapshot.json`, kept fresh by
`scripts/refresh_catalog.py`. Always run the freshness check (Step 3 in the audit
flow) before loading controls.

### Snapshot format

The snapshot contains three relevant fields:

```json
{
  "metadata": {
    "last_modified": "2025-05-13T18:00:00+08:00",
    "version": "2025.05.13",
    "oscal_version": "1.1.2"
  },
  "controls": {
    "ac-2": {
      "title": "Multi-Factor Authentication (MFA)",
      "group": "Access Control",
      "statement": "Require MFA for privileged accounts at login.",
      "guidance": "...",
      "params": [...]
    }
  },
  "profile_levels": {
    "ac-2": { "low": 1, "medium": 0 },
    "lm-20": { "low": 2 }
  }
}
```

`profile_levels[control_id][band]` is the **lowest level** the control appears at
in that band — i.e. the level at which it first becomes required. `"medium": 0` means
it is a mandatory (L0) control for medium-risk systems.

### Building the in-scope control set

```python
# Example: low-risk system, assess L0+L1 (target_level = 1)
band = "low"
target_level = 1

with open("references/catalog-snapshot.json") as f:
    snapshot = json.load(f)

in_scope = {
    cid: snapshot["controls"][cid]
    for cid, levels in snapshot["profile_levels"].items()
    if band in levels and levels[band] <= target_level
    and cid in snapshot["controls"]
}
# in_scope maps control_id -> {title, group, statement, guidance, params}
```

### Manual refresh (if the script can't reach GitHub)

If the network is unavailable, the snapshot remains usable. To manually update it
when connectivity is restored, run:

```bash
python scripts/refresh_catalog.py
```

Or to fetch the raw files yourself:
```
https://raw.githubusercontent.com/GovTechSG/tech-standards/master/catalogs/im8-reform.json
https://raw.githubusercontent.com/GovTechSG/tech-standards/master/profiles/{band}-level-{0,1,2}.json
```
Build `profile_levels` by reading each profile's `imports[].include-controls[].with-ids`
and recording the minimum level at which each control ID appears per band.

## Parameters are intentionally blank

All 47 parameterised controls (e.g. AS-5 password length, BR-1 backup frequency,
ST-5 remediation SLAs, LM-8 log retention) ship with labels but **no values**. The
agency sets these in its own SSP. The audit therefore cannot judge whether a
threshold "meets policy" unless the user supplies the agency's chosen values. For
any parameterised control, check whether the mechanism exists in the repo, and flag
that the specific value still needs to be verified against the agency's SSP.
