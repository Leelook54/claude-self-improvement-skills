# Claude Self-Improvement Skills

## 项目定位

这是一个用于维护 Claude Code 自改进记忆系统的 skill 定义仓库。

本仓库只包含两个 Claude Code skills：
- `auto-memory-compact`
- `self-improvement-review`

本仓库不是完整的 memory 仓库，不保存运行期证据，不保存用户 memory records，不保存 hook 日志，不保存 settings 或 `CLAUDE.md`。

运行产物都应落在 `~/.claude/memory/`，而不是提交到本仓库。

## 为什么需要这个仓库

日常纠错、工具失败、阶段总结不适合直接写入全局 `CLAUDE.md`。全局 `CLAUDE.md` 是默认加载层，内容过多会增加 token 成本、降低缓存命中稳定性，并可能导致 agent 行为漂移。

Skill 更适合承载多步骤流程、检查清单、review 逻辑和 compact 逻辑。把复杂策略放进 skill，可以把默认 prompt 前缀保持得更短、更稳定，也更容易做 cache hygiene。

Runtime evidence 应放在 `~/.claude/memory/`，而不是放在 skill 仓库中。本仓库的职责只是版本化 skill 本体，便于维护、回滚、同步和复用。

另外，本仓库不自动写 `CLAUDE.md`。promotion candidate 只是建议，不是 apply；要真正进入全局或项目规则层，必须由用户单独明确批准。

## 当前系统分层

| 层级 | 路径 | 是否默认加载 | 职责 |
|---|---|---:|---|
| Skill 定义层 | `~/.claude/skills/auto-memory-compact/` | 按需 | compact / cache hygiene |
| Skill 定义层 | `~/.claude/skills/self-improvement-review/` | 按需 | review / promotion candidate / skill candidate |
| 运行证据池 | `~/.claude/memory/records/` | 否 | errors / reviews / promotions / rejected |
| 捕获入口 | `~/.claude/memory/inbox/` | 否 | H1 捕获的 correction candidates |
| 归档层 | `~/.claude/memory/archive/` | 否 | legacy / test noise / raw artifacts |
| 默认索引 | `~/.claude/memory/MEMORY.md` | 轻量 | memory 读取策略 |
| 全局指令层 | `~/.claude/CLAUDE.md` | 是 | 极少量稳定规则，不由本仓库自动修改 |

## 本仓库结构

```text
claude-self-improvement-skills/
├── README.md
├── .gitignore
├── auto-memory-compact/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
└── self-improvement-review/
    ├── SKILL.md
    ├── references/
    └── scripts/
```

- `SKILL.md`：skill 入口、触发场景、安全边界
- `references/`：详细策略、分类规则、输出模板
- `scripts/`：确定性只读检查脚本

## Skill 1：auto-memory-compact

### 作用

- 检查 memory 目录结构
- 检查 `MEMORY.md` 行数
- 区分 `active warnings` 与 `archived_notes`
- 生成 compact plan
- 辅助归档测试噪声和低价值记录
- 检查 cache hygiene

### 不做什么

- 不自动写 `CLAUDE.md`
- 不自动改 Claude Code 官方 auto memory
- 不自动删除 `.md`
- 不把 `records/` 当 active rules
- 不把 `archive/` 重新激活

### 主要文件

- `SKILL.md`
- `references/auto-memory-safety.md`
- `references/cache-hygiene.md`
- `references/compact-classification.md`
- `references/output-formats.md`
- `scripts/inspect_memory.py`

### 典型调用

- compact memory
- 检查 memory 健康
- 检查 cache hygiene
- 清理测试噪声

## Skill 2：self-improvement-review

### 作用

- 分析 `inbox/`
- 分析 `records/errors/`
- 分析 `records/reviews/`
- 提取 repeated friction patterns
- 生成 review report
- 生成 promotion candidate
- 生成 skill candidate

### 不做什么

- 不自动 apply promotion
- 不自动创建 skill
- 不自动写全局或项目 `CLAUDE.md`
- 不自动修改 Claude Code 官方 auto memory
- 不把 `records/` 当规则执行

### 主要文件

- `SKILL.md`
- `references/review-taxonomy.md`
- `references/promotion-policy.md`
- `references/skill-extraction-policy.md`
- `references/cache-hygiene-review.md`
- `references/report-template.md`
- `scripts/collect_records.py`

### 典型调用

- 运行 self-improvement review
- 检查 promotion candidates
- 检查 repeated friction patterns
- 处理 skill candidates

## 与 Hook 层的关系

本仓库不包含 Hook 脚本，但这两个 skill 通常与本地 Hook 配合使用。

| Hook | 本地脚本 | 作用 | 输出 |
|---|---|---|---|
| H1 UserPromptSubmit | `~/.claude/memory/hooks/capture_user_correction.py` | 捕获用户纠错 | `~/.claude/memory/inbox/` |
| H2 PostToolUse | `~/.claude/memory/hooks/capture_tool_failure.py` | 捕获真实工具失败 | `~/.claude/memory/records/errors/` |
| H3 PreToolUse Bash | `~/.claude/memory/hooks/pretool_safety_guard.py` | 阻断高风险 Bash | `~/.claude/memory/records/errors/` |

要点：
- Hook 只捕获证据或阻断风险
- Hook 不做 review / compact / promotion
- Skill 才做 review / compact
- H1/H2 默认不应输出 stdout
- H3 block 使用 `exit 2` + `stderr`

## 运行产物放在哪里

运行产物不属于本仓库，统一放在 `~/.claude/memory/`：

```text
~/.claude/memory/
├── MEMORY.md
├── inbox/
├── records/
│   ├── errors/
│   ├── reviews/
│   ├── promotions/
│   ├── rejected/
│   └── skill-candidates/
├── compact/
└── archive/
```

- `MEMORY.md`：轻量索引，保持短、稳、可缓存
- `inbox/`：H1 捕获的 correction candidates
- `records/errors/`：真实工具失败与异常
- `records/reviews/`：review 产物
- `records/promotions/`：promotion candidate 记录
- `records/rejected/`：被拒绝的候选项
- `records/skill-candidates/`：待提炼的 skill 候选
- `compact/`：compact 过程中的临时/结果材料
- `archive/`：历史、legacy、test noise、raw artifacts

## Promotion Candidate 规则

- promotion candidate 只是候选建议
- 不代表自动写入 `CLAUDE.md`
- 不代表自动修改配置
- 不代表自动成为 active rule
- 写入全局或项目 `CLAUDE.md` 必须有用户单独明确批准
- 更适合优先写入 skill references 的规则，不应轻易提升到全局 `CLAUDE.md`
- 已接受进入 skill policy 的 candidate 可标记为 `accepted_into_skill_policy`

## Cache Hygiene 设计原则

- 默认 prompt 前缀应短、稳定
- `records/`、`archive/`、`compact/` 不默认读取
- `MEMORY.md` 应保持轻量索引
- 日常纠错、失败记录、阶段总结不写入全局 `CLAUDE.md`
- 长流程进入 skill，而不是 `CLAUDE.md`
- `archive/` 中的大文件只作为 `archived_notes`，不作为 `active warnings`

## 安装方式

```bash
git clone https://github.com/Leelook54/claude-self-improvement-skills.git
cp -R claude-self-improvement-skills/auto-memory-compact ~/.claude/skills/
cp -R claude-self-improvement-skills/self-improvement-review ~/.claude/skills/
```

也可以用同步工具或本地镜像把两个 skill 目录复制到 `~/.claude/skills/`，但不要把运行证据、settings、`CLAUDE.md` 或 hook 日志同步进来。

## 同步、升级与版本标记

- 同步时，只同步两个 skill 目录和它们各自的 `SKILL.md`、`references/`、`scripts/`
- 升级时，优先在仓库中改 skill 本体，再同步到 `~/.claude/skills/`
- 版本标记建议使用 Git tag，例如 `v0.1.0`、`v0.2.0`
- 版本说明应只描述 skill 定义变化，不描述 runtime evidence
- 如果某个 promotion candidate 已进入 skill policy，可在相关引用里标记为 `accepted_into_skill_policy`

## 不应提交的内容

以下内容不应提交到本仓库：

- `records/`
- `archive/`
- `inbox/`
- `compact/`
- `settings.json`
- `CLAUDE.md`
- hook logs
- 任何 runtime evidence

## 面向未来维护

维护这个仓库时，优先保证三件事：

1. skill 本体稳定，默认前缀短且可缓存
2. 运行证据始终留在 `~/.claude/memory/`
3. promotion candidate 只作为建议，必须由用户明确批准后再进入更高层规则

这样可以让 review、compact、cache hygiene 和长期维护互相独立，也便于回滚和复用。
