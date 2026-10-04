# Stage: component — 组件深度工程模式

## 目录

- 任务与组件边界
- 抽象与选择
- Contract
- 状态 / 密度 / 响应式
- Accessibility
- 输出与停止条件

## 目的

把一个可复用组件或紧密相关的组件族，设计成明确、稳定、可复用的视觉与工程契约。

## Context Budget

只加载当前组件真正需要的 Pack / Profile：先读 Contract、状态、密度与可访问性相关的
资料，其余留到确实需要时再读。不要因为“可能相关”就整包读进来——把组件做对靠的是
准确的契约，不是更多的资料。

## 输入

- target component / family
- 当前使用场景或截图
- 相关 Page / Design Spec
- 已有组件清单
- 技术 Profile（只有要落代码时才深入）

## 决策顺序

1. 明确用户任务与组件责任。
2. 判断层级：`foundation` / `pattern` / `domain` / `page-local`。
3. 检查是否已有满足 Contract 的组件。
4. 选择动作：`REUSE` / `CONFIGURE` / `WRAP` / `EXTEND` / `REPLACE` / `CREATE`。
5. 先形成 Component Contract，再改代码。
6. 定义状态与 Density。
7. 定义 Responsive 与 Accessibility。
8. 只有有业务价值时才增加 analytics / test hooks。

## Component Contract 必须包含

```text
purpose
scope / non-goals
anatomy
props / inputs
outputs / events
slots / composition points
variants
sizes / density modes
states
interaction rules
keyboard behavior
responsive transformation
accessibility semantics
content constraints
motion
performance considerations
testability
examples / anti-examples
```

## 抽象粒度

- 相同交互或视觉契约出现 2 次以上，或明确会复用，可以考虑抽组件。
- 文件很长不是单独的抽象理由。
- 不要为了“统一命名”创建没有行为或契约价值的 wrapper。
- 重复组合优先抽成 pattern，如 `FilterBar`、`MetricGroup`、`ResultToolbar`。
- 稳定的业务概念优先抽成 domain component。
- 复用价值不确定时保持 page-local。

## Ant Design Vue 策略

Ant Design Vue 是行为基础设施，不是最终视觉语言。

判断：

```text
满足行为 + 可访问性 + 交互契约？
  ├─ yes → REUSE / CONFIGURE
  ├─ yes，但视觉或产品契约不同 → WRAP / EXTEND
  ├─ 行为不足 → CREATE / REPLACE
  └─ 一次性组合 → 保持 page-local
```

## 状态完整性

按组件级别决定状态集合。普通展示组件不必机械实现全部状态；交互复杂或数据密集组件才使用完整状态矩阵。

基础交互组件至少考虑：

```text
default / hover / focus-visible / active / selected
expanded / collapsed / disabled / loading / skeleton
empty / error / success / partial / readonly
long-content
```

高复杂度或数据密集组件再增加：`selected / expanded / collapsed / permission-denied / partial / dense / skeleton / success`。

## 高密度组件

Table、Filter、Toolbar、Metric Group、分析控件必须明确：

- comfortable / standard / compact
- 控件与行高策略
- 主次操作层级
- 溢出与截断
- 键盘路径
- Loading / Empty / Error 恢复方式

不能只靠缩小字号和 padding 制造密度。

## Responsive

必须明确是 `preserve / collapse / reorder / stack / substitute / hide / move-to-overflow` 哪一种变换，而不是简单按比例缩放。

## Accessibility

至少定义语义、accessible name、focus-visible、keyboard、disabled/readonly、错误提示、非颜色提示以及 reduced-motion 行为。

## 输出

默认只输出：

- Component Contract（按 `templates/component-contract-deep.yaml` 的字段结构）
- selection decision
- implementation notes

本阶段默认不改业务代码；只有 Scope 明确包含代码实现，或显式切换到 `implementation` Stage 时才进入代码变更。

## 限制

- 不修改产品 IA。
- 不修改无关页面。
- 不为单个组件创建无复用价值的新 Token 家族。
- 不把 vendor API 原样透传到 domain component。
