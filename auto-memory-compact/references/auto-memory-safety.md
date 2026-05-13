# Auto Memory Safety

## 核心原则

Claude Code auto memory 由 Claude Code 管理。请尊重其边界。

## 规则

- 前 200 行或 25KB 可在会话启动时加载
- Topic 文件应保持独立，按需读取
- 不自由重写整个 auto MEMORY.md
- 修改前始终生成压缩计划
- 优先归档而非删除
- 保留 topic 文件引用
- 不将项目记忆提升到全局 CLAUDE.md

## 安全操作

- 读取和分析现有记忆结构
- 生成分类和压缩计划
- 归档低价值条目
- 将重复条目移至归档
- 为详细内容创建 topic 文件

## 禁止操作

- 无计划重写整个 MEMORY.md
- 不归档直接删除记录
- 未经批准提升任何内容到 CLAUDE.md
- 正常工作期间扫描 records/