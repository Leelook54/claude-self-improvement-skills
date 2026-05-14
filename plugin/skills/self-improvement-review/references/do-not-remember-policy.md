# Do Not Remember Policy

## 目的
定义哪些内容不应写入长期 self-improvement memory。

## 不应记录
- 一次性终端输出
- 可从当前仓库或文件重新推导的事实
- 短期任务进度
- 临时路径和临时文件名
- hook dry-run 细节
- synthetic test noise
- 已被 summary 覆盖的 raw 测试碎片
- 用户没有长期保留意图的项目事实
- 纯安装日志
- 已归档且无复用价值的历史碎片

## Record When
- 用户明确纠错
- 用户明确偏好或边界
- 工具失败反复出现
- 安全阻断反复出现
- 出现可复用流程
- 出现能力缺口
- 出现 cache hygiene 风险
- 出现 promotion 或 skill candidate

## When Unsure
- Prefer needs_evidence over promotion.
- Prefer short evidence quote over full transcript.
- Prefer skill reference over global CLAUDE.md.
- Prefer archive summary over keeping raw noise active.