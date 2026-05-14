# self-improvement-memory Plugin

## 目的

Claude Code 自改进记忆治理 plugin，提供 memory review、compact、retention、session discovery 和 CLAUDE.md/settings 写入保护。

## 包含内容

### Skills

- **auto-memory-compact**：MEMORY.md 压缩与归档，保留索引、归档详情、删除低价值记录。
- **self-improvement-review**：分析 evidence records、检测重复摩擦模式、生成 promotion candidates。

两个 skill 均遵守安全规则：**不得写入全局 `~/.claude/CLAUDE.md`**，不得擅自修改 Claude Code auto memory。

### Hooks

- **PreToolUse write guard**（`hooks/pretool_write_guard.py`）：拦截 `Edit/Write/MultiEdit` 工具调用，保护以下路径：
  - `~/.claude/CLAUDE.md`
  - `~/.claude/settings.json`
  - `~/.claude/settings.local.json`
  - 任意目录的 `CLAUDE.md`
  - 任意目录的 `.claude/settings.json`
  - 任意目录的 `.claude/settings.local.json`

## 不包含内容

- **旧 H1/H2/H3 hooks**：本版 plugin 不恢复。H1/H2/H3 曾因作用域过宽导致路径失效和噪声，本版专注最小写入保护。
- **PreCompact hook activation**：PreCompact snapshot 功能存在（`scripts/precompact_snapshot.py`），但 hook 默认未安装，本版 scope 不包含激活。

## 本地测试

```bash
# Mock 测试（不安装 plugin）
cd plugin/hooks
echo '{"tool_name":"Write","tool_input":{"file_path":"~/.claude/CLAUDE.md"}}' | python3 pretool_write_guard.py
# 期望：deny JSON

echo '{"tool_name":"Write","tool_input":{"file_path":"README.md"}}' | python3 pretool_write_guard.py
# 期望：exit 0，无 stdout
```

## 禁用 Plugin

```bash
claude plugin disable self-improvement-memory
```

或临时注释 `~/.claude/settings.json` 中的 plugin 配置。

## 安装

```bash
claude plugin install /path/to/plugin
```

或使用 `plugin-dir` 方式加载本地路径。
