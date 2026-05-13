# Compact Retention Policy

## 目的
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

---

## Long-term Retention Policy

### Active Layer Targets
- records/errors: keep representative unresolved evidence only; review when >30
- records/reviews: keep latest 10–15 key reports active; archive superseded reports when >25
- records/candidates: keep open or accepted candidates active
- records/patterns: keep active/resolved pattern topic files plus PATTERN_INDEX.md
- compact/plans and compact/reports: keep latest compact plan/report active, archive old plans when superseded

### Archive Layer
- archive/raw may grow, but must be summarized by archive/summaries
- large raw noise groups should be date-sharded
- archive/summaries/ARCHIVE_INDEX.md should point to important raw groups

### Overwrite Prevention
- repeated smoke tests, dry-run reviews, compact reports, cleanup reports must use: YYYYMMDD_HHMMSS_<slug>.md
- one-off stage reports may use: YYYYMMDD_<stage>-<slug>.md
- never overwrite an existing report unless user explicitly asks
- prefer writing a new timestamped report and updating LATEST pointer

### Latest Pointers
Optional short pointer files:
- records/reviews/LATEST_REVIEW.md
- records/reviews/LATEST_SMOKE_TEST.md
- compact/reports/LATEST_COMPACT.md

Pointer files must be short and human-facing only.

### No Delete By Default
- default action is summarize + archive
- deletion requires explicit user approval