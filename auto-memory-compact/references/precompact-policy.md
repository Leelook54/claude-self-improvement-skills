# PreCompact Snapshot Policy

## Purpose

PreCompact snapshot 用于在 Claude Code 上下文压缩前采集会话状态快照，为后续回顾和决策提供轻量级 handoff 信息。

Snapshot 由 PreCompact hook 触发，仅做只读数据采集，不执行任何修改操作。

## Why Not Run Full Review / Compact

完整 review / compact 会触发较多扫描、报告写入和维护噪声，不适合放在 PreCompact hook 自动执行。Hook 应在毫秒内完成，静默执行，不产生额外开销。

Snapshot 采集后，由 user 或 self-improvement-review 选择性读取，不自动加载。

## Runtime Output

| Item | Path |
|------|------|
| Directory | `~/.claude/memory/compact/precompact/` |
| Naming | `YYYYMMDD_HHMMSS_precompact-snapshot.md` |

## Frontmatter Standard

```yaml
---
name: precompact-{timestamp}
type: precompact_snapshot
source: hook
default_load: false
status: unreviewed
promote_requires_user_approval: true
---
```

## Content Fields

| Field | Source | Note |
|-------|--------|------|
| transcript_path | hook payload | if present in hook payload |
| session_id | hook payload | if present in hook payload |
| session_start | hook payload | if present in hook payload |
| context_percent | hook payload | if present in hook payload |
| compact_trigger | hook payload | if present in hook payload |
| model | hook payload | if present in hook payload |
| effort_level | hook payload | if present in hook payload |
| cwd | hook payload | if present in hook payload |
| input_tokens | hook payload | if present in hook payload |
| output_tokens | hook payload | if present in hook payload |
| cache_creation_tokens | hook payload | if present in hook payload |
| cache_read_tokens | hook payload | if present in hook payload |

**Constraint**: Only record fields present in hook payload. If not present, write `not provided`. Do not read transcript to fill missing data.

**Line Limit**: Content ≤80 lines (excluding frontmatter).

## Forbidden Behavior

- Do not write to `~/.claude/CLAUDE.md`
- Do not modify `MEMORY.md` or any memory index files
- Do not read transcript file content
- Do not delete files
- Do not move files
- Do not create records/ or errors/
- Do not send external network requests
- Do not write to stdout
- Do not commit to git

## Failure Behavior

- **Silent by default**: No output on failure
- **If necessary**: Only single-line short stderr (max 1 line, error type only like `err:io`), no stack trace
- **Non-blocking**: Compact process continues regardless of hook success/failure

## Validation Checklist

- [ ] Directory created at `~/.claude/memory/compact/precompact/`
- [ ] File naming format: `YYYYMMDD_HHMMSS_precompact-snapshot.md`
- [ ] Frontmatter includes required fields
- [ ] Content lines ≤80
- [ ] No stdout output (except `--dry-run`)
- [ ] Short stderr on failure (when not silent)
- [ ] Compact continues after hook execution