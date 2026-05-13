# Output Formats

## Compact Plan

```markdown
# Compact Plan

## Target Paths
- `/path/to/memory/`

## Files Inspected
- `MEMORY.md` (XXX lines)
- `topic-file-1.md`
- `topic-file-2.md`

## Proposed Changes

| File | Action | Reason |
|------|--------|--------|
| entry-1 | archive-stale | outdated |
| entry-2 | merge-duplicate | redundant |
| entry-3 | keep | still valid |

## Risk Level
[low / medium / high]

## Requires Approval
[yes / no]

## Cache Hygiene Findings
- [finding 1]
- [finding 2]

## Before/After Line Counts
- Before: XXX lines
- After: YYY lines

## Archived Files
- `archived-entry-1.md`

## Rejected Low-Value Items
- `rejected-entry-1.md`

## Promotion Candidates
- [candidate with reason]

## Skill Candidates
- [candidate with reason]

## Verification Result
[TBD after approval]
```

## Compact Report

```markdown
# Compact Report

## Execution Summary
- Executed: YYYY-MM-DD
- Changes applied: [list]

## Verification
- MEMORY.md lines: [count]
- Topic files: [count]
- Archived: [count]
- Rejected: [count]
- Promoted: [count or none]

## Cache Hygiene
- [pass / warning / fail]
- [details]

## Next Steps
- [recommendations]
```
