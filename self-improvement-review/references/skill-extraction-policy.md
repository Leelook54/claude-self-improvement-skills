# Skill Extraction Policy

## When to Extract a Skill

A task should be extracted into a skill when it meets **multiple** of the following criteria:

- Multi-step process (3+ steps)
- Repeated usage
- Requires a checklist or fixed output format
- Not suitable for CLAUDE.md
- Has clear trigger scenarios (slash command or keywords)
- Can be organized as `SKILL.md` + `references/` + `scripts/`

## Recommended Skill Structure

```
skill-name/
├── SKILL.md              # YAML frontmatter + concise body
├── references/           # Complex rules
└── scripts/             # Executable scripts (optional)
```

## What Should NOT Be a Skill

- One-off tasks
- Simple single-step operations
- Highly project-specific workflows
- Pure exploratory research
