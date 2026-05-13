# Compact Retention Policy

## Purpose
定义 memory 内容治理、保留、归档、摘要和 raw 文件移动策略。

## v0.2 Target Structure
写明：
~/.claude/memory/
├── MEMORY.md
├── SELF_IMPROVEMENT_DASHBOARD.md
├── inbox/
├── records/
│   ├── errors/
│   ├── reviews/
│   ├── patterns/
│   ├── candidates/
│   │   ├── promotions/
│   │   ├── skills/
│   │   └── capabilities/
│   ├── rejected/
│   └── resolved/
├── compact/
│   ├── COMPACT_POLICY.md
│   ├── plans/
│   └── reports/
└── archive/
    ├── summaries/
    └── raw/

## Retention Classes
- active-evidence
- resolved-evidence
- test-noise
- legacy-raw
- summary-only
- archive-raw
- stale-review
- superseded-report

## Keep Active
- latest formal review
- latest hooks overall acceptance
- latest alignment report
- latest completion report
- latest cleanup/compact report
- unresolved promotion candidates
- active patterns
- representative real safety evidence

## Archive
- old dry-run reports
- old install plans
- superseded acceptance reports
- hook test noise
- smoke test noise
- synthetic failures
- legacy GLOBAL files
- old workflow drafts

## Summary First
在移动大量 raw 文件前必须创建 summary。
summary 放 archive/summaries/
raw 放 archive/raw/

## Never Delete By Default
默认不删除 .md 文件。
删除必须是单独明确请求。