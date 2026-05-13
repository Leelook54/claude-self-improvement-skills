# Claude Self-Improvement Skills

**Version**: v0.1.0
**Date**: 2026-05-13

---

## Purpose

This repository maintains two Claude Code skills for a local self-improvement memory system.

These skills enable:
- Periodic review of self-improvement evidence (user corrections, tool errors)
- Memory compaction and cache hygiene management
- Promotion candidate identification without auto-application
- Alignment reporting and smoke testing

---

## Skills

### auto-memory-compact

Reviews memory structure, generates compact plans, checks cache hygiene, and handles archived notes.

**Location**: `auto-memory-compact/`

**Key Files**:
- `SKILL.md` - Skill definition and safety rules
- `references/` - Policy and taxonomy documents
- `scripts/inspect_memory.py` - Memory inspection script
- `scripts/collect_records.py` - Records collection script (shared with self-improvement-review)

### self-improvement-review

Reviews correction/error evidence, detects repeated friction patterns, identifies promotion candidates and skill candidates.

**Location**: `self-improvement-review/`

**Key Files**:
- `SKILL.md` - Skill definition and safety rules
- `references/` - Policy and taxonomy documents
- `scripts/collect_records.py` - Records collection script (shared with auto-memory-compact)

---

## Boundaries

- **Skill definitions only**: This repository contains skill definitions only. Runtime evidence lives outside the repository under `~/.claude/memory/`.
- **No auto-write**: These skills do not automatically write to global or project `CLAUDE.md`.
- **User approval required**: Promotion candidates require explicit user approval before any higher-priority placement.
- **Evidence isolation**: Do not commit `records/`, `archive/`, `inbox/`, `compact/`, `settings.json`, or `CLAUDE.md`.
- **No runtime artifacts**: Do not commit hook logs, test noise, or memory evidence.

---

## Architecture

```
~/.claude/
├── skills/
│   ├── auto-memory-compact/    ← This repo
│   └── self-improvement-review/ ← This repo
├── memory/
│   ├── MEMORY.md               ← Lightweight index
│   ├── records/                ← Evidence (NOT in repo)
│   ├── archive/                ← Historical (NOT in repo)
│   └── inbox/                  ← Captured (NOT in repo)
└── hooks/
    ├── capture_user_correction.py   (H1)
    ├── capture_tool_failure.py      (H2)
    └── pretool_safety_guard.py     (H3)
```

---

## Install

Copy or sync the skill directories into your Claude Code skills directory:

```bash
# Option 1: Clone and copy
git clone <repo-url> ~/tmp/claude-self-improvement-skills
cp -r ~/tmp/claude-self-improvement-skills/auto-memory-compact ~/.claude/skills/
cp -r ~/tmp/claude-self-improvement-skills/self-improvement-review ~/.claude/skills/

# Option 2: Git submodule (advanced)
git submodule add <repo-url> ~/.claude/skills/auto-memory-compact
git submodule add <repo-url> ~/.claude/skills/self-improvement-review
```

After installation, the skills will be available via Claude Code's skill system.

---

## Versioning

Use semantic versioning for stable snapshots:
- `v0.1.0` - Initial v0.1 release (2026-05-13)

---

## Maintenance

- Review skills periodically after system updates
- Update references/ documents when policies change
- Tag releases for significant changes
- Do not commit runtime evidence or memory artifacts

---

## License

Private. For personal use with Claude Code.
