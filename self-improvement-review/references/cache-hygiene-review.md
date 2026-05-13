# Cache Hygiene Review Checklist

## 审查项

1. 默认加载的文件短且稳定（MEMORY.md <100 行，理想 <50 行）
2. 无动态日期、会话状态或队列状态泄露到默认上下文
3. MEMORY.md 超过 100 行，150 行是警告阈值
4. `records/` 被常规任务读取
5. 应转为 skill 的长工作流
6. 频繁变化的 prompt 前缀

## 风险等级定义

| 等级 | 条件 |
|------|------|
| low | 无明显膨胀风险 |
| medium | 1-2 项存在风险 |
| high | 3+ 项存在风险或 MEMORY.md >150 行 |