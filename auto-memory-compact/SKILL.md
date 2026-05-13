---
name: auto-memory-compact
description: Review and compact Claude Code auto memory and local self-improvement memory records. Use when the user asks to clean, summarize, deduplicate, compact, prune, or remove low-value memory; when MEMORY.md is too long; or when cache hygiene and prompt-prefix stability need review.
---

# Auto Memory Compact

## Purpose

- Compact Claude Code auto memory safely
- Keep MEMORY.md as a short index
- Move detail to topic files or archive
- Remove duplicate, stale, contradicted, or low-value memory
- Generate review reports and cache hygiene checks
- Do not promote anything into CLAUDE.md without explicit user approval

## PreCompact Snapshot Support

Supports PreCompact hook for lightweight session state snapshots before context compression.

- Policy: `references/precompact-policy.md`
- Script: `scripts/precompact_snapshot.py`
- Output: `~/.claude/memory/compact/precompact/`
- Hook is NOT installed by default (v0.2 observation period)

Snapshot ≠ compact execution. Snapshot only records payload fields; it does not run full review.

## Safety Rules

- Do not write to global `~/.claude/CLAUDE.md`
- Do not rewrite Claude Code auto MEMORY.md without a compact plan
- Do not delete memory records by default; archive first
- Do not treat records/ as active rules
- Do not promote anything without explicit user approval
- Do not merge topic files back into MEMORY.md
- Do not scan records/ during normal work

## Workflow

1. Identify target memory paths
2. Inspect MEMORY.md and topic files
3. Classify entries
4. Produce compact plan
5. Ask for approval before applying modifications to Claude Code auto memory
6. Apply only minimal safe changes after approval
7. Generate compact report

## References

- `references/auto-memory-safety.md` — Safety rules for modifying Claude Code auto memory
- `references/compact-classification.md` — Entry classification taxonomy
- `references/cache-hygiene.md` — Cache stability and prompt-prefix checks
- `references/output-formats.md` — Compact plan and report output formats
- `references/compact-retention-policy.md` — Content governance, retention, and archive strategy
- `references/dashboard-policy.md` — Dashboard content, line count, and update rules

## Scripts

- `scripts/inspect_memory.py` — Inspect memory structure (supports v0.2 checks)
- `scripts/generate_dashboard.py` — Generate dashboard markdown (dry-run by default)
- `scripts/retention_audit.py` — Read-only audit for file accumulation and overwrite risk
