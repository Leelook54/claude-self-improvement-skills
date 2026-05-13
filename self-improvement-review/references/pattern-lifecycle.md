# Pattern Lifecycle

## 目的
定义 repeated friction patterns 的识别、更新、解决、关闭和重新打开规则。

## Pattern File
每个 pattern 一个 topic file，路径：
records/patterns/<pattern_key>.md

## Pattern Index
records/patterns/PATTERN_INDEX.md

## Pattern Frontmatter
字段：
---
type: friction_pattern
pattern_key:
title:
status:
first_seen:
last_seen:
recurrence_count:
severity:
default_load: false
promote_requires_user_approval: true
---

## Status Lifecycle
- needs_evidence：只有一次证据，尚不足以形成 pattern
- active：重复出现，需要处理
- resolved：已有处理方案
- stale：长时间未再出现
- superseded：被新 pattern 或 policy 取代
- rejected：误判或低价值

## Recurrence Rules
- 同一 pattern 出现新证据时更新 recurrence_count
- 更新 last_seen
- 追加 evidence_paths
- 不重复创建新 pattern

## Reopen Rules
- resolved pattern 如果再次出现同类证据，重新标记 active
- stale pattern 如果再次出现，更新 last_seen 并重新评估

## Evidence Quotes
每个 pattern 最多保留 1–3 条短 evidence quotes。
不复制完整 transcript。