#!/usr/bin/env python3
"""
IM8 catalog freshness check and conditional refresh.

Compares the last-modified date embedded in the local snapshot against the
live GovTechSG/tech-standards repo. If the repo is newer, downloads the full
catalog and profiles, diffs them against the snapshot, updates the snapshot,
and reports what changed.

Usage (from the skill root directory):
    python scripts/refresh_catalog.py

Output: JSON to stdout. The calling agent reads this to decide which catalog
to use and whether to surface a change log to the user.

Exit codes:
    0 — snapshot is current, or was successfully updated
    1 — fetch failed (network unavailable or rate-limited); snapshot is still usable
"""

import json
import sys
from datetime import datetime, timezone
import urllib.request
import urllib.error
from pathlib import Path

SKILL_ROOT = Path(__file__).parent.parent
SNAPSHOT_PATH = SKILL_ROOT / "references" / "catalog-snapshot.json"
LAST_CHECKED_PATH = SKILL_ROOT / "references" / "last-checked.json"

CATALOG_URL = (
    "https://raw.githubusercontent.com/GovTechSG/tech-standards/master"
    "/catalogs/im8-reform.json"
)
PROFILES_BASE = (
    "https://raw.githubusercontent.com/GovTechSG/tech-standards/master/profiles"
)
PROFILE_FILES = [
    "low-risk-level-0.json",
    "low-risk-level-1.json",
    "low-risk-level-2.json",
    "medium-risk-level-0.json",
    "medium-risk-level-1.json",
    "medium-risk-level-2.json",
]
TIMEOUT = 10  # seconds per request
# Range request: the last-modified field appears within the first 600 bytes
FRESHNESS_RANGE = "bytes=0-600"


def fetch(url, headers=None, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def get_repo_date():
    """
    Fetch just the first 600 bytes of the live catalog to extract the
    last-modified date — avoids downloading the full 300 KB.
    Returns the date string or None on failure.
    """
    try:
        chunk = fetch(CATALOG_URL, headers={"Range": FRESHNESS_RANGE})
        import re
        m = re.search(r'"last-modified"\s*:\s*"([^"]+)"', chunk)
        return m.group(1) if m else None
    except Exception:
        return None


def load_snapshot():
    with open(SNAPSHOT_PATH) as f:
        return json.load(f)


def build_snapshot_from_live():
    """Download the full catalog and all profiles, return a new snapshot dict."""
    raw = json.loads(fetch(CATALOG_URL))
    catalog = raw["catalog"]
    meta = catalog["metadata"]

    controls = {}
    for g in catalog["groups"]:
        for ctrl in g.get("controls", []):
            stmt = next(
                (p["prose"] for p in ctrl.get("parts", []) if p["name"] == "statement"),
                "",
            )
            guidance = next(
                (p["prose"] for p in ctrl.get("parts", []) if p["name"] == "guidance"),
                "",
            )
            params = [
                {"id": p["id"], "label": p.get("label", "")}
                for p in ctrl.get("params", [])
            ]
            controls[ctrl["id"]] = {
                "title": ctrl["title"],
                "group": g["title"],
                "statement": stmt,
                "guidance": guidance,
                "params": params,
            }

    profile_levels = {}
    for fname in PROFILE_FILES:
        raw_p = json.loads(fetch(f"{PROFILES_BASE}/{fname}"))
        props = {
            pr["name"]: pr["value"]
            for pr in raw_p["profile"]["metadata"].get("props", [])
        }
        band = props.get("risk", "").replace("-risk", "")
        level = int(props.get("level", -1))

        for imp in raw_p["profile"].get("imports", []):
            for ic in imp.get("include-controls", []):
                for cid in ic.get("with-ids", []):
                    if cid not in profile_levels:
                        profile_levels[cid] = {}
                    if band not in profile_levels[cid]:
                        profile_levels[cid][band] = level
                    else:
                        profile_levels[cid][band] = min(
                            profile_levels[cid][band], level
                        )

    return {
        "metadata": {
            "last_modified": meta["last-modified"],
            "version": meta["version"],
            "oscal_version": meta["oscal-version"],
        },
        "groups": [g["title"] for g in catalog["groups"]],
        "controls": controls,
        "profile_levels": profile_levels,
    }


def diff_snapshots(old, new):
    """
    Compare two snapshot dicts. Returns a list of human-readable change strings
    grouped by type, ordered from most to least significant.
    """
    changes = []
    old_ctrl = old.get("controls", {})
    new_ctrl = new.get("controls", {})
    old_levels = old.get("profile_levels", {})
    new_levels = new.get("profile_levels", {})

    # --- Profile level changes (most operationally significant) ---
    for cid in set(old_levels) | set(new_levels):
        o = old_levels.get(cid, {})
        n = new_levels.get(cid, {})
        title = new_ctrl.get(cid, old_ctrl.get(cid, {})).get("title", cid)
        for band in set(o) | set(n):
            ol = o.get(band)
            nl = n.get(band)
            if ol != nl:
                if ol is None:
                    changes.append(
                        f"[LEVEL] {cid} ({title}): added to {band}-risk at L{nl}"
                    )
                elif nl is None:
                    changes.append(
                        f"[LEVEL] {cid} ({title}): removed from {band}-risk"
                    )
                else:
                    direction = "promoted" if nl < ol else "demoted"
                    changes.append(
                        f"[LEVEL] {cid} ({title}): {band}-risk {direction} "
                        f"L{ol} → L{nl}"
                    )

    # --- New / removed controls ---
    added = set(new_ctrl) - set(old_ctrl)
    removed = set(old_ctrl) - set(new_ctrl)
    for cid in sorted(added):
        changes.append(
            f"[NEW]   {cid}: {new_ctrl[cid]['title']} "
            f"({new_ctrl[cid]['group']})"
        )
    for cid in sorted(removed):
        changes.append(
            f"[REMOVED] {cid}: {old_ctrl[cid]['title']} "
            f"({old_ctrl[cid]['group']})"
        )

    # --- Statement changes on existing controls ---
    for cid in sorted(set(old_ctrl) & set(new_ctrl)):
        o_stmt = old_ctrl[cid].get("statement", "")
        n_stmt = new_ctrl[cid].get("statement", "")
        o_title = old_ctrl[cid].get("title", "")
        n_title = new_ctrl[cid].get("title", "")
        if n_title != o_title:
            changes.append(
                f"[TITLE] {cid}: '{o_title}' → '{n_title}'"
            )
        if n_stmt != o_stmt:
            # Summarise: show first 120 chars of new statement
            preview = n_stmt[:120].replace("\n", " ")
            changes.append(
                f"[STATEMENT] {cid} ({n_title}): statement changed. "
                f"New: '{preview}…'"
            )

    # --- Domain (group) changes ---
    old_groups = set(old.get("groups", []))
    new_groups = set(new.get("groups", []))
    for g in sorted(new_groups - old_groups):
        changes.append(f"[DOMAIN] New domain added: '{g}'")
    for g in sorted(old_groups - new_groups):
        changes.append(f"[DOMAIN] Domain removed: '{g}'")

    return changes


def read_last_checked():
    """
    When this machine last successfully reached the live catalog.

    Kept separate from the snapshot (and out of git) because it answers a
    per-machine question: "have *we* verified this recently?" A snapshot's
    own last_modified date only says when GovTech last changed the catalog —
    it cannot distinguish "unchanged since then" from "never checked since
    then", which is the distinction that matters when a check fails.
    """
    try:
        with open(LAST_CHECKED_PATH) as f:
            return json.load(f).get("checked_at")
    except (OSError, ValueError):
        return None


def record_check(repo_date):
    """Stamp a successful reach of the live catalog. Best-effort."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        with open(LAST_CHECKED_PATH, "w") as f:
            json.dump({"checked_at": now, "catalog_date_seen": repo_date}, f, indent=1)
    except OSError:
        pass
    return now


def days_since(iso_ts):
    if not iso_ts:
        return None
    try:
        then = datetime.fromisoformat(iso_ts)
        if then.tzinfo is None:
            then = then.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - then).days
    except ValueError:
        return None


def main():
    snapshot = load_snapshot()
    snapshot_date = snapshot["metadata"]["last_modified"]

    repo_date = get_repo_date()

    if repo_date is None:
        # Network unavailable or rate-limited — fall back to snapshot
        last_checked = read_last_checked()
        age = days_since(last_checked)
        if last_checked is None:
            staleness = (
                "This machine has never successfully verified the catalog, so the "
                "snapshot's age is unknown — it may or may not still be current."
            )
        else:
            staleness = f"Last verified {age} day(s) ago ({last_checked})."
        result = {
            "status": "fetch_failed",
            "snapshot_date": snapshot_date,
            "repo_date": None,
            "checked_at": last_checked,
            "days_since_check": age,
            "catalog_path": str(SNAPSHOT_PATH),
            "changes": [],
            "message": (
                "Could not reach GitHub to check for catalog updates. "
                "Using local snapshot dated "
                + snapshot_date
                + ". "
                + staleness
                + " Re-run when network is available."
            ),
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    if repo_date == snapshot_date:
        checked_at = record_check(repo_date)
        result = {
            "status": "current",
            "snapshot_date": snapshot_date,
            "repo_date": repo_date,
            "checked_at": checked_at,
            "days_since_check": 0,
            "catalog_path": str(SNAPSHOT_PATH),
            "changes": [],
            "message": (
                f"Snapshot is current (last modified: {snapshot_date}; "
                f"verified {checked_at})."
            ),
        }
        print(json.dumps(result, indent=2))
        sys.exit(0)

    # Repo is newer — download, diff, update snapshot
    try:
        new_snapshot = build_snapshot_from_live()
    except Exception as e:
        last_checked = read_last_checked()
        result = {
            "status": "fetch_failed",
            "snapshot_date": snapshot_date,
            "repo_date": repo_date,
            "checked_at": last_checked,
            "days_since_check": days_since(last_checked),
            "catalog_path": str(SNAPSHOT_PATH),
            "changes": [],
            "message": (
                f"Repo is newer ({repo_date} vs snapshot {snapshot_date}) "
                f"but full download failed: {e}. Using existing snapshot."
            ),
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    changes = diff_snapshots(snapshot, new_snapshot)

    # Write updated snapshot
    with open(SNAPSHOT_PATH, "w") as f:
        json.dump(new_snapshot, f, indent=1)

    checked_at = record_check(repo_date)

    result = {
        "status": "updated",
        "snapshot_date": snapshot_date,
        "repo_date": repo_date,
        "checked_at": checked_at,
        "days_since_check": 0,
        "catalog_path": str(SNAPSHOT_PATH),
        "changes": changes,
        "message": (
            f"Catalog updated from {snapshot_date} to {repo_date}. "
            f"{len(changes)} change(s) detected — see 'changes' list."
        ),
    }
    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
