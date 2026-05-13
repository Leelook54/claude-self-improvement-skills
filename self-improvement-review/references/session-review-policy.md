# Session Review Policy

## Purpose
定义未来从 Claude Code session transcript/jsonl 中提取 evidence 的边界。

## Scope
- 只读扫描 transcript/jsonl
- 先统计和定位候选 session
- 不默认读取全文
- 不复制长 transcript 到 records/
- 不自动写 CLAUDE.md
- 不自动修改 Claude Code 官方 auto memory

## Candidate Signals
- 用户纠错
- 用户说"不是/错了/重新/以后不要/下次默认"
- 多轮重复失败
- 工具失败上下文
- 长循环或低效路径
- subagent 合并质量问题
- check 类短指令误解

## Evidence Quote Rule
- 每个 candidate 最多提取 1–3 条短 quote
- quote 必须包含 source path 和时间信息
- 不复制敏感大段文本
- 不把 quote 当 active rule

## v0.2 Implementation
- collect_sessions.py 先做 dry-run discovery
- 后续 v0.2.1 再做 short quote extraction