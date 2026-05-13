---
name: auto-memory-compact
description: 审查和压缩 Claude Code auto memory 及本地 self-improvement memory records。当用户要求清理、摘要、去重、压缩、删除低价值 memory 时使用；当 MEMORY.md 过长时使用；当需要审查 cache hygiene 和 prompt-prefix 稳定性时使用。
---

# Auto Memory Compact

## 目的

- 安全压缩 Claude Code auto memory
- 保持 MEMORY.md 为简短索引
- 将详细内容移至 topic 文件或 archive
- 删除重复、过时、矛盾或低价值 memory
- 生成审查报告和 cache hygiene 检查
- 未经用户明确批准，不得 promotion 任何内容到 CLAUDE.md

## 安全规则

- 不得写入全局 `~/.claude/CLAUDE.md`
- 未经 compact plan 不得重写 Claude Code auto MEMORY.md
- 默认不删除 memory records，先 archive
- 不得将 `records/` 作为 active rules
- 未经用户明确批准，不得 promotion 任何内容
- 不得将 topic 文件合并回 MEMORY.md
- 日常工作中不得扫描 `records/`

## 工作流程

1. 识别目标 memory 路径
2. 检查 MEMORY.md 和 topic 文件
3. 分类 entries
4. 生成 compact plan
5. 在修改 Claude Code auto memory 前请求批准
6. 批准后仅执行最小安全变更
7. 生成 compact report

## 参考文档

- `references/auto-memory-safety.md` — 修改 Claude Code auto memory 的安全规则
- `references/compact-classification.md` — Entry 分类法
- `references/cache-hygiene.md` — Cache 稳定性和 prompt 前缀检查
- `references/output-formats.md` — Compact plan 和 report 输出格式
- `references/compact-retention-policy.md` — 内容治理、保留策略和归档策略
- `references/dashboard-policy.md` — Dashboard 内容、行数和更新规则

## 脚本

- `scripts/inspect_memory.py` — 检查 memory 结构（支持 v0.2 检查）
- `scripts/generate_dashboard.py` — 生成 dashboard markdown（默认 dry-run）
- `scripts/retention_audit.py` — 只读审计文件累积和覆盖风险