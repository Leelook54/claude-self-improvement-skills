---
name: auto-memory-compact
description: Review and compact Claude Code auto memory and local self-improvement memory records. Use when the user asks to clean, summarize, deduplicate, compact, prune, or remove low-value memory; when MEMORY.md is too long; or when cache hygiene and prompt-prefix stability need review.
---

# Auto Memory Compact

## 目的

- 安全压缩 Claude Code 自动内存
- 保持 MEMORY.md 作为简短索引
- 将详细内容移至 topic 文件或归档
- 删除重复、过时、矛盾或低价值记忆
- 生成审查报告和缓存健康检查
- 未经用户明确批准不提升任何内容到 CLAUDE.md

## PreCompact Snapshot 支持

支持 PreCompact hook 在上下文压缩前采集轻量级会话状态快照。

- Policy: `references/precompact-policy.md`
- Script: `scripts/precompact_snapshot.py`
- Output: `~/.claude/memory/compact/precompact/`
- Hook 默认未安装（v0.2 观察期）

Snapshot ≠ compact execution。Snapshot 仅记录 payload 字段，不运行完整审查。

## 安全规则

- 不写入全局 `~/.claude/CLAUDE.md`
- 不生成压缩计划前不重写 Claude Code auto MEMORY.md
- 默认不删除记忆记录；先归档
- 不将 records/ 当作活动规则
- 未经用户批准不提升任何内容
- 不将 topic 文件合并回 MEMORY.md
- 正常工作时不扫描 records/

## 工作流程

1. 识别目标记忆路径
2. 检查 MEMORY.md 和 topic 文件
3. 分类记忆条目
4. 生成压缩计划
5. 应用修改前请求用户批准
6. 批准后仅执行最小安全变更
7. 生成压缩报告

## 参考文档

- `references/auto-memory-safety.md` — 修改 Claude Code auto memory 的安全规则
- `references/compact-classification.md` — 记忆条目分类法
- `references/cache-hygiene.md` — 缓存稳定性和 prompt 前缀检查
- `references/output-formats.md` — 压缩计划和报告输出格式
- `references/compact-retention-policy.md` — 内容治理、保留和归档策略
- `references/dashboard-policy.md` — Dashboard 内容、行数限制和更新规则

## 脚本

- `scripts/inspect_memory.py` — 检查记忆结构（支持 v0.2 检查）
- `scripts/generate_dashboard.py` — 生成 dashboard markdown（默认 dry-run）
- `scripts/retention_audit.py` — 只读审计文件累积和覆盖风险