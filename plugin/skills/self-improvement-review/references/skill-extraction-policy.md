# Skill Extraction Policy

## 何时提取 Skill

当任务满足**多个**以下条件时应提取为 skill：

- 多步骤流程（3+ 步骤）
- 重复使用
- 需要 checklist 或固定输出格式
- 不适合放入 CLAUDE.md
- 有明确的触发场景（slash command 或关键词）
- 可组织为 `SKILL.md` + `references/` + `scripts/`

## 推荐 Skill 结构

```
skill-name/
├── SKILL.md              # YAML frontmatter + 简洁正文
├── references/           # 复杂规则
└── scripts/             # 可执行脚本（可选）
```

## 什么不应作为 Skill

- 一次性任务
- 简单的单步操作
- 高度项目专用工作流
- 纯探索性研究