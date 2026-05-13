# Claude Self-Improvement Skills

## 1. 项目定位

本仓库是 Claude Code self-improvement memory system 的 skill 定义仓库。

**职责范围：**
- 保存两个 skill 本体（`auto-memory-compact` 和 `self-improvement-review`）
- 版本化管理 skill 定义

**不在本仓库：**
- Runtime evidence（运行产物位于 `~/.claude/memory/`）
- `records/`、`archive/`、`inbox/`、`compact/`
- `settings.json` / `CLAUDE.md`
- Hook logs
- Claude Code official auto memory

本仓库**不自动修改** `CLAUDE.md`，**不自动修改** Claude Code official auto memory。

## 2. 当前版本状态

<table>
  <thead>
    <tr>
      <th>字段</th>
      <th>值</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>当前版本</td>
      <td>v0.2</td>
    </tr>
    <tr>
      <td>状态</td>
      <td>结构稳定，已通过 smoke test，进入真实使用观察期</td>
    </tr>
  </tbody>
</table>

**已完成：**
- schema / policy references
- v0.2 runtime structure
- candidates path
- pattern index
- dashboard
- compact policy
- retention audit
- archive index summary
- smoke test

**观察项：**
- H2 tail-noise 仍可能增长
- `records/errors` 超过阈值（> 30）后再 compact
- session transcript deep review 尚未启用，仅 discovery

## 3. Skill 总览

<table>
  <thead>
    <tr>
      <th>Skill</th>
      <th>路径</th>
      <th>主要职责</th>
      <th>输出目标</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>auto-memory-compact</code></td>
      <td><code>auto-memory-compact/</code></td>
      <td>memory 结构检查、compact policy、dashboard、retention audit、archive index</td>
      <td><code>~/.claude/memory/compact/</code>、<code>archive/summaries/</code>、dashboard</td>
    </tr>
    <tr>
      <td><code>self-improvement-review</code></td>
      <td><code>self-improvement-review/</code></td>
      <td>review 证据、pattern lifecycle、候选项、session discovery、promotion policy</td>
      <td><code>~/.claude/memory/records/reviews/</code>、patterns、candidates</td>
    </tr>
  </tbody>
</table>

**说明：**
- 两个 skill 使用同一套 memory schema
- review skill 负责发现问题 和候选
- compact skill 负责治理内容 和压缩策略
- 两者都**不自动写 CLAUDE.md**

## 4. 仓库结构

```
claude-self-improvement-skills/
├── README.md
├── .gitignore
├── auto-memory-compact/
│   ├── SKILL.md
│   ├── references/
│   │   ├── auto-memory-safety.md
│   │   ├── cache-hygiene.md
│   │   ├── compact-classification.md
│   │   ├── compact-retention-policy.md
│   │   ├── dashboard-policy.md
│   │   └── output-formats.md
│   └── scripts/
│       ├── generate_dashboard.py
│       ├── inspect_memory.py
│       └── retention_audit.py
└── self-improvement-review/
    ├── SKILL.md
    ├── references/
    │   ├── cache-hygiene-review.md
    │   ├── do-not-remember-policy.md
    │   ├── pattern-lifecycle.md
    │   ├── promotion-policy.md
    │   ├── record-schema.md
    │   ├── report-template.md
    │   ├── review-taxonomy.md
    │   ├── session-review-policy.md
    │   └── skill-extraction-policy.md
    └── scripts/
        ├── collect_records.py
        ├── collect_sessions.py
        └── update_pattern_index.py
```

**说明：**
- `SKILL.md`：触发入口、核心流程和边界
- `references/`：详细策略、policy、模板、分类标准
- `scripts/`：只读检查、统计、dry-run 或受控生成工具

## 5. Runtime memory 结构

当前目标结构：

```
~/.claude/memory/
├── MEMORY.md
├── SELF_IMPROVEMENT_DASHBOARD.md
├── inbox/
├── records/
│   ├── errors/
│   ├── reviews/
│   ├── patterns/
│   │   └── PATTERN_INDEX.md
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
    │   └── ARCHIVE_INDEX.md
    └── raw/
```

**逐项说明：**

### MEMORY.md
- 轻量索引和读取策略
- 不放长报告
- 不放错误详情
- 不放候选全文

### SELF_IMPROVEMENT_DASHBOARD.md
- 人类状态面板
- 不是 active rules
- 控制在短内容
- 展示 version / last review / errors / warnings / next actions

### inbox/
- 未 review 的 correction candidates
- 主要来自 H1 UserPromptSubmit
- 不长期堆积

### records/errors/
- 工具失败和安全阻断
- 主要来自 H2/H3
- 是证据，不是规则
- tail-noise 超阈值才 review

### records/reviews/
- formal review、migration report、smoke test、stabilization report
- 可重复报告应使用 `YYYYMMDD_HHMMSS` 命名
- 避免覆盖

### records/patterns/
- repeated friction pattern topic files
- `PATTERN_INDEX.md` 是索引，不是 pattern
- pattern_count 以 `update_pattern_index.py` 为准

### records/candidates/
- promotions：候选提升建议
- skills：候选 skill
- capabilities：能力缺口
- candidates 不是 apply

### records/rejected/
- 重复、低价值、误捕获、证据不足项

### records/resolved/
- 曾经重要但已解决的问题

### compact/
- compact policy、plans、reports
- plan 先于 execution
- 默认不删除 .md

### archive/
- 历史归档
- summaries 是摘要和索引
- raw 是原始历史材料
- `archive/raw` inactive unless explicitly requested

## 6. auto-memory-compact 工作逻辑

**触发场景：**
- compact memory
- 检查 memory 健康
- 检查 cache hygiene
- 运行 retention audit
- 生成 dashboard
- 生成 compact plan

**不会：**
- 不自动删除 .md
- 不自动写 CLAUDE.md
- 不自动修改 MEMORY.md
- 不自动修改 official auto memory
- 不把 `archive/raw` 当 active rules

**References：**

<table>
  <thead>
    <tr>
      <th>文件</th>
      <th>作用</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>references/auto-memory-safety.md</code></td>
      <td>修改 Claude Code auto memory 的安全规则</td>
    </tr>
    <tr>
      <td><code>references/cache-hygiene.md</code></td>
      <td>Cache 稳定性和 prompt 前缀检查</td>
    </tr>
    <tr>
      <td><code>references/compact-classification.md</code></td>
      <td>Entry 分类法（active / archived / evidence / noise）</td>
    </tr>
    <tr>
      <td><code>references/compact-retention-policy.md</code></td>
      <td>内容治理、保留策略、归档策略</td>
    </tr>
    <tr>
      <td><code>references/dashboard-policy.md</code></td>
      <td>Dashboard 内容、行数、更新规则</td>
    </tr>
    <tr>
      <td><code>references/output-formats.md</code></td>
      <td>Compact plan 和 report 输出格式</td>
    </tr>
  </tbody>
</table>

**Scripts：**

<table>
  <thead>
    <tr>
      <th>脚本</th>
      <th>作用</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>scripts/inspect_memory.py</code></td>
      <td>只读扫描 <code>~/.claude/memory/</code>，输出 target_structure_status、warnings、archived_notes、dashboard/pattern index 状态</td>
    </tr>
    <tr>
      <td><code>scripts/generate_dashboard.py</code></td>
      <td>默认 stdout，<code>--write</code> 时才写 <code>SELF_IMPROVEMENT_DASHBOARD.md</code></td>
    </tr>
    <tr>
      <td><code>scripts/retention_audit.py</code></td>
      <td>只读统计文件总量、archive/raw 增长、覆盖风险、compact recommendation</td>
    </tr>
  </tbody>
</table>

## 7. self-improvement-review 工作逻辑

**触发场景：**
- 运行 self-improvement review
- 检查 repeated friction patterns
- 检查 promotion candidates
- 检查 skill candidates
- session transcript discovery

**不会：**
- 不自动 apply promotion
- 不自动创建 skill
- 不自动写 CLAUDE.md
- 不自动读取 transcript 全文
- 不自动修改 official auto memory

**References：**

<table>
  <thead>
    <tr>
      <th>文件</th>
      <th>作用</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>references/record-schema.md</code></td>
      <td>records/ 各子目录的文件 schema 和 frontmatter 格式</td>
    </tr>
    <tr>
      <td><code>references/pattern-lifecycle.md</code></td>
      <td>Pattern 从发现到解决的生命周期</td>
    </tr>
    <tr>
      <td><code>references/do-not-remember-policy.md</code></td>
      <td>不应写入 memory 的内容</td>
    </tr>
    <tr>
      <td><code>references/session-review-policy.md</code></td>
      <td>session transcript review 范围和限制</td>
    </tr>
    <tr>
      <td><code>references/review-taxonomy.md</code></td>
      <td>Review 分类</td>
    </tr>
    <tr>
      <td><code>references/promotion-policy.md</code></td>
      <td>promotion candidate 的评判标准</td>
    </tr>
    <tr>
      <td><code>references/skill-extraction-policy.md</code></td>
      <td>skill candidate 提炼规则</td>
    </tr>
    <tr>
      <td><code>references/cache-hygiene-review.md</code></td>
      <td>review 过程中的 cache hygiene 检查点</td>
    </tr>
    <tr>
      <td><code>references/report-template.md</code></td>
      <td>Review report 输出模板</td>
    </tr>
  </tbody>
</table>

**Scripts：**

<table>
  <thead>
    <tr>
      <th>脚本</th>
      <th>作用</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>scripts/collect_records.py</code></td>
      <td>只读扫描 records/，支持 v0.1 / v0.2 / mixed</td>
    </tr>
    <tr>
      <td><code>scripts/update_pattern_index.py</code></td>
      <td>默认 dry-run，跳过 <code>PATTERN_INDEX.md</code>，<code>--write</code> 才更新 index</td>
    </tr>
    <tr>
      <td><code>scripts/collect_sessions.py</code></td>
      <td>只做 session/jsonl discovery，不读取全文，不写 records</td>
    </tr>
  </tbody>
</table>

## 8. 标准工作流

### 8.1 日常使用
- H1 捕获纠错到 inbox
- H2 捕获工具失败到 records/errors
- H3 阻断高风险 Bash
- Skill **不自动运行**

### 8.2 运行 self-improvement review
1. collect_records
2. pattern lifecycle
3. candidates
4. review report
5. 不 apply

### 8.3 compact memory
1. inspect_memory
2. retention_audit
3. compact plan
4. 用户批准
5. safe execution
6. no delete by default

### 8.4 retention audit
1. 检查 total_files
2. 检查 archive/raw 增长
3. 检查 records/errors
4. 检查 records/reviews
5. 检查 overwrite risk
6. 给出 compact recommendation

### 8.5 smoke test
1. 验证两个 skill 的只读链路
2. generate_dashboard stdout
3. collect_sessions discovery
4. 不写默认上下文层

## 9. 命名规则

重复任务报告必须使用：
```
YYYYMMDD_HHMMSS_<slug>.md
```

**适用场景：**
- smoke test
- dry-run review
- compact plan
- compact report
- cleanup report
- retention audit

一次性阶段报告可使用：
```
YYYYMMDD_v0.2-g-stabilization-report.md
```

**禁止**：默认覆盖旧报告。

如果需要最新指针，未来使用：
- `LATEST_REVIEW.md`
- `LATEST_SMOKE_TEST.md`
- `LATEST_COMPACT.md`

当前不强制创建 LATEST 指针。

## 10. Safety / Boundaries

- `records/` 是 evidence pool，不是 active rules
- `candidates/` 是 proposals，不是 apply
- dashboard 是 human orientation，不是 active rules
- `archive/` inactive unless explicitly requested
- compact plan 不是 execution
- 删除 .md 需要用户明确批准
- 写 CLAUDE.md 需要用户单独明确批准
- official auto memory 不由本仓库修改
- session transcript 默认只 discovery，不读取全文

## 11. 安装和同步

**安装：**
```bash
git clone https://github.com/Leelook54/claude-self-improvement-skills.git
cp -R claude-self-improvement-skills/auto-memory-compact ~/.claude/skills/
cp -R claude-self-improvement-skills/self-improvement-review ~/.claude/skills/
```

**同步：**
```bash
rsync -av --delete auto-memory-compact/ ~/.claude/skills/auto-memory-compact/
rsync -av --delete self-improvement-review/ ~/.claude/skills/self-improvement-review/
```

**警告**：不要对 `~/.claude/memory/` 使用 `rsync --delete`。

## 12. GitHub 仓库维护

- Runtime skill 是 source of execution
- Git repo 是 versioned source
- 同步前先确认 diff
- 不提交 runtime evidence
- 不提交 settings / CLAUDE.md
- 不提交 archive/raw
- 不提交 records/

**维护流程：**
1. 修改或同步 skill
2. 运行脚本测试
3. `git diff --stat`
4. `git add`
5. `git commit`
6. `git push`

## 13. 不应提交的内容

以下内容**不应提交**到本仓库：

- `~/.claude/memory/`
- `records/`
- `archive/`
- `inbox/`
- `compact/`
- `settings.json`
- `settings.local.json`
- `CLAUDE.md`
- hook logs
- `__pycache__`
- `.DS_Store`
- `.env`

## 14. 当前观察期建议

- 正常使用 1–3 天
- `records/errors > 30` 再检查
- `active warnings > 0` 立即检查
- `inbox > 10` 运行 review
- 不新增 Hook
- 不改 CLAUDE.md
- 不继续堆功能