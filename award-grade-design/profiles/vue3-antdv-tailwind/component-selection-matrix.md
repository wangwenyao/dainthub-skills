# Component Selection Matrix — 组件选择矩阵

| 条件 | 动作 |
|---|---|
| 行为与视觉契约都满足 | `REUSE` |
| 只需轻量配置 | `CONFIGURE` |
| 行为复用但需要稳定产品 API | `WRAP` |
| 现有实现可控增强 | `EXTEND` |
| 现有能力与关键 Contract 冲突 | `REPLACE` |
| 不存在合适基础能力 | `CREATE` |

决策以 Contract 为中心，不以“哪个组件最方便”为中心。
