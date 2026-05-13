# Output Formats

## Compact Plan 格式

```markdown
# Compact Plan

## 目标路径
- `/path/to/memory/`

## 检查的文件
- `MEMORY.md` (XXX 行)
- `topic-file-1.md`
- `topic-file-2.md`

## 提议变更

| 文件 | 操作 | 原因 |
|------|------|------|
| entry-1 | archive-stale | 过时 |
| entry-2 | merge-duplicate | 重复 |
| entry-3 | keep | 仍有效 |

## 风险等级
[low / medium / high]

## 需要批准
[yes / no]

## Cache Hygiene 发现
- [发现项 1]
- [发现项 2]

## 执行前后行数
- 执行前: XXX 行
- 执行后: YYY 行

## Archive 的文件
- `archived-entry-1.md`

## 拒绝的低价值项
- `rejected-entry-1.md`

## Promotion Candidates
- [候选及原因]

## Skill Candidates
- [候选及原因]

## 验证结果
[批准后填写]
```

## Compact Report 格式

```markdown
# Compact Report

## 执行摘要
- 执行日期: YYYY-MM-DD
- 已应用变更: [列表]

## 验证
- MEMORY.md 行数: [数量]
- Topic 文件: [数量]
- 已 Archive: [数量]
- 已拒绝: [数量]
- 已 Promotion: [数量或无]

## Cache Hygiene
- [pass / warning / fail]
- [详情]

## 下一步
- [建议]
```