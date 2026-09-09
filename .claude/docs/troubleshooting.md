# Troubleshooting Log

> Living document. Problems that **can recur**, and what actually fixed them.
> Standard: `~/.claude/sop/ENGINEERING.md`
> Searched before investigating any error; appended after any fix that took more than one attempt.

**What belongs here:** environment and tooling quirks, non-obvious root causes, and
**dead ends** — the attempts that didn't work and why. Dead ends are the most valuable
entries and the ones most often lost.

**What doesn't:** a fixed code bug. It can't recur, and the fix plus its reasoning are
already in git history. Logging it here only buries the entries that matter.

**Pruning:** when the cause is permanently gone, delete the entry outright. Git remembers.

---

## <short symptom title>

**Symptom:** `<the exact error string, as it appears>`
**Cause:** <what was actually wrong — often not what the error pointed at>
**Fix:** <the specific thing that worked>
**Dead ends:** <what was tried and failed, and why it failed>
**Logged:** YYYY-MM-DD
