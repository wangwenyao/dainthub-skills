# Stage Governance

## 目的

防止 Agent 在一个小任务中擅自扩大职责范围。

## Stage 权限

| Stage | 权限 |
|---|---|
| audit | read-only |
| direction | artifact-only |
| design-system | design-artifacts |
| page | design-artifacts |
| component | design-artifacts |
| implementation | code |
| visual-qa | read-only |
| optimization | patch |

## 越界规则

需要越界时：

1. 停止静默修改。
2. 记录 dependency / deviation。
3. 说明为什么需要。
4. 等待当前 Scope 允许，或换 Stage。

## 关键原则

```text
Visual QA 不应重做设计。
Implementation 不应偷偷改变 Design Direction。
Component 不应擅自改变 Product IA。
Optimization 不应演变成 broad redesign。
```
