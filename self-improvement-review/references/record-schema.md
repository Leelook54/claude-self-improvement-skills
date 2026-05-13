# Record Schema

## 目的
定义 self-improvement memory records 的统一 frontmatter 和状态机。
records/ 是低频证据池，不是 active rules。

## 必填 frontmatter

统一字段：
---
type:
source:
default_load: false
status:
created_at:
last_reviewed_at:
review_count:
freshness:
verify_before_use:
promote_requires_user_approval: true
---

## type 值

- correction_candidate
- tool_error
- safety_block
- review
- friction_pattern
- promotion_candidate
- skill_candidate
- capability_request
- rejected
- resolved_issue

## source 值

- hook
- self-improvement-review
- auto-memory-compact
- user
- manual
- session-transcript

## status 值

- unreviewed
- proposed
- needs_evidence
- accepted_into_skill_policy
- accepted_into_project_policy
- resolved
- rejected
- stale
- superseded
- archived

## freshness 值

- current
- stale
- historical

## 硬性要求

- 所有 records 的 `default_load` 必须为 false
- promotion candidates 必须设置 `promote_requires_user_approval: true`
- records 不得作为 active rules
- 写入全局或项目 CLAUDE.md 需要单独的、明确的用户批准步骤

## 目录映射

写明 v0.2 目标映射：
- inbox/：unreviewed correction candidates
- records/errors/：tool_error / safety_block
- records/reviews/：review and audit reports
- records/patterns/：friction_pattern topic files
- records/candidates/promotions/：promotion_candidate
- records/candidates/skills/：skill_candidate
- records/candidates/capabilities/：capability_request
- records/rejected/：rejected
- records/resolved/：resolved_issue