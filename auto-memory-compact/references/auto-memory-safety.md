# Auto Memory Safety

## 核心原则

Claude Code auto memory 由 Claude Code 管理。尊重其边界。

## 规则

- 前 200 行或 25KB 可能在会话启动时加载
- Topic 文件应保持独立，按需读取
- 不得随意重写整个 auto MEMORY.md
- 变更前必须生成 compact plan
- 优先 archive 而非 delete
- 保留 topic 文件引用
- 不得将 project memory 提升到全局 CLAUDE.md

## 安全操作

- 读取并分析现有 memory 结构
- 生成分类和 compact plan
- Archive 低价值 entries
- 将重复内容移至 archive
- 为详细内容创建 topic 文件

## 禁止操作

- 未经 plan 重写整个 MEMORY.md
- 未经 archive 删除 records
- 未经批准 promotion 任何内容到 CLAUDE.md
- 日常任务中扫描 `records/`