---
name: self-improvement-review
description: 分析本地 self-improvement memory records、用户纠错、工具错误、审查报告和压缩报告，识别重复摩擦模式，提出规则/配置更新建议和 skill 提取候选。当用户要求审查 agent 行为、发现重复错误、改进工作流、提取可复用 skill 或准备 self-improvement 建议时使用。
---

# Self Improvement Review

## 目的

- 审查低频 self-improvement evidence records
- 检测重复摩擦模式
- 识别反复出现的用户纠错和工具错误模式
- 生成 promotion candidates 而不自动应用
- 为可复用的多步骤工作流生成 skill extraction candidates
- 检查 cache hygiene 和默认上下文膨胀风险
- 除非用户明确批准单独的 apply 步骤，否则保持全局 CLAUDE.md 和 Claude Code auto memory 不变

## 安全规则

- 不得写入全局 `~/.claude/CLAUDE.md`
- 不得写入项目 `CLAUDE.md`
- 不得修改 Claude Code 官方 auto memory
- 不得修改 `/Users/qunqing/.claude/memory/MEMORY.md`
- 不得将 `records/` 作为 active rules
- 不得 promotion 一次性纠错
- 不得将动态会话状态转换为默认加载上下文
- 不得自动应用建议
- **不得删除任何 `.md` 文件；删除必须由用户明确批准**
- **`collect_sessions.py` 和 session discovery 只做候选会话发现；不读取 transcript 全文，不提取 quote，除非用户明确要求进入 session review**
- **`archive/raw/` 默认 inactive，除非用户明确要求追溯，不作为 active rules 或默认 evidence source**

## 工作流程

1. 识别 `/Users/qunqing/.claude/memory/records/` 下的目标 records
2. 收集纠错、错误、审查、compact 报告、promotions、skill-candidates 和 rejected records
3. 分类重复模式
4. 交叉检查建议是否已存在于 `records/promotions/` 或 `records/skill-candidates/`
5. 在 `records/reviews/` 下生成审查报告
6. 仅当 evidence 重复且稳定时生成 promotion candidate 文件
7. 仅对可复用的多步骤工作流生成 skill candidate 文件
8. 输出验证摘要

## 参考文档

- 阅读 `references/review-taxonomy.md` 进行 evidence 分类
- 在提议 CLAUDE.md 或配置变更前阅读 `references/promotion-policy.md`
- 在提议新 skill 前阅读 `references/skill-extraction-policy.md`
- 在审查默认上下文和缓存友好性时阅读 `references/cache-hygiene-review.md`
- 编写审查报告时阅读 `references/report-template.md`
- 阅读 `references/record-schema.md` 了解统一 frontmatter 和状态机
- 阅读 `references/pattern-lifecycle.md` 了解摩擦模式检测和生命周期
- 在写入长期 memory 前阅读 `references/do-not-remember-policy.md`
- 阅读 `references/session-review-policy.md` 了解 session transcript evidence 提取

## 脚本

- `scripts/collect_records.py` — 收集 records 摘要（支持 v0.1/v0.2）
- `scripts/update_pattern_index.py` — 扫描和索引摩擦模式（默认 dry-run）
- `scripts/collect_sessions.py` — 发现用于未来审查的 session 文件（dry-run）