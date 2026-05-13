# Record Schema

## Purpose
定义 self-improvement memory records 的统一 frontmatter 和状态机。
records/ 是低频证据池，不是 active rules。

## Required Frontmatter

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

## Type Values
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

## Source Values
- hook
- self-improvement-review
- auto-memory-compact
- user
- manual
- session-transcript

## Status Values
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

## Freshness Values
- current
- stale
- historical

## Hard Requirements
- default_load must be false for all records.
- promotion candidates must set promote_requires_user_approval: true.
- records must not be treated as active rules.
- writing to global or project CLAUDE.md requires a separate explicit user approval step.

## Directory Mapping
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