# Output Formats

## 压缩计划格式

```markdown
# 压缩计划

## 目标路径
- `/path/to/memory/`

## 已检查文件
- `MEMORY.md` (XXX 行)
- `topic-file-1.md`
- `topic-file-2.md`

## 提议变更

| 文件 | 操作 | 原因 |
|------|------|------|
| entry-1 | archive-stale | 过时 |
| entry-2 | merge-duplicate | 重复 |
| entry-3 | keep | 仍然有效 |

## 风险等级
[low / medium / high]

## 需要批准
[yes / no]

## 缓存健康发现
- [发现 1]
- [发现 2]

## 前后行数统计
- 修改前: XXX 行
- 修改后: YYY 行

## 已归档文件
- `archived-entry-1.md`

## 已拒绝低价值条目
- `rejected-entry-1.md`

## 提升候选
- [候选条目及原因]

## Skill 候选
- [候选条目及原因]

## 验证结果
[批准后填写]
```

## 压缩报告格式

```markdown
# 压缩报告

## 执行摘要
- 执行时间: YYYY-MM-DD
- 应用的变更: [列表]

## 验证
- MEMORY.md 行数: [数量]
- Topic 文件数: [数量]
- 已归档: [数量]
- 已拒绝: [数量]
- 已提升: [数量或无]

## 缓存健康
- [pass / warning / fail]
- [详情]

## 下一步
- [建议]
```