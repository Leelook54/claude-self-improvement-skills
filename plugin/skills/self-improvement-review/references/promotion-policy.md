# Promotion Policy

Promotion 只表示"建议"，不自动应用。所有 promotion 必须经过用户确认。

## Promotion Candidate 必要条件

以下条件必须全部满足，方可进入 promotion candidate：

1. **跨项目有效性**: 规则适用于多个项目或跨任务场景，不是单一项目专用
2. **证据强度**: 至少有 2 个独立证据来源，或用户明确要求长期遵守
3. **约束强度**: 是强约束或高频偏好，不是一次性经验或偶发偏好
4. **可压缩性**: 能压缩为 1-3 行，便于 CLAUDE.md 或规则文件引用
5. **上下文成本**: 不增加明显的默认上下文负担

### 证据来源优先级

| 优先级 | 来源 | 说明 |
|--------|------|------|
| P0 | 用户明确指令 | "始终..."、"必须..."、"以后都..." |
| P1 | 跨项目重复 | 2+ 项目/会话中出现相同偏好 |
| P2 | 同项目多次 | 同一项目 >= 3 次验证 |

---

## 禁止行为

以下行为严格禁止：

- **禁止自动写 CLAUDE.md**: 不得在未确认情况下创建或修改项目的 CLAUDE.md
- **禁止自动提升项目 auto memory**: 不得将项目级记忆自动写入 MEMORY.md
- **禁止将 records/ 当作规则源**: records/ 是观察记录，非规则来源
- **禁止在用户确认前写入任何配置文件**: 包括但不限于 CLAUDE.md、settings.json、.claude/ 目录下的任何文件

---

## Promotion 执行流程

```
1. 识别 → 从 review 中标记 promotion candidate
2. 验证 → 确认满足全部 5 个必要条件
3. 建议 → 向用户提出 promotion 建议，说明理由
4. 等待确认 → 获得用户明确同意后才执行
5. 落地 → 用户指定写入位置（CLAUDE.md / MEMORY.md / 其他）
```

---

## 注意事项

- Promotion 是"建议"而非"命令"：用户有权拒绝或修改
- 拒绝的 promotion 应标记为 `rejected-low-value`，保留理由
- 多次被拒绝的建议降级为低优先级观察

---

## CLAUDE.md Placement Guardrail

Promotion candidate 不代表自动写入全局或项目 CLAUDE.md。

- **Global ~/.claude/CLAUDE.md 是默认加载指令层**，必须保持简短、稳定、极少修改
- 日常纠错、记忆系统边界、review 摘要、hook 行为注释、compact 报告默认不应写入全局 CLAUDE.md
- Self-improvement guardrail 应首先存在于 skill references 或 records/promotions/ 作为候选 guardrail
- 写入全局或项目 CLAUDE.md 必须经过用户明确批准和单独的 apply 步骤
- 如果 candidate 本身声明"不要写入 CLAUDE.md"，其推荐目标不得是 CLAUDE.md
