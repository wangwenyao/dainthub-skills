# Stage: implementation — 实现深度工程模式

## 目录

- 仓库事实
- Design Contract → Implementation Mapping
- 实现顺序
- 验证
- Drift / Deviation

## 目的

根据已经批准的 Design Direction、Design System、Page Spec、Component Contract 和 Technology Profile，把设计准确落成生产代码；本 Stage 不是重新设计阶段。

## Context Budget

先读 Design Spec、Page / Component Contract 与 Technology Profile；仓库现有约定在
“第一步：识别仓库事实”里按需探查。只有遇到深层问题才扩大读取范围。

## 输入顺序

```text
Design Spec
→ Page / Component Contract
→ Design Tokens
→ Technology Profile
→ 仓库现有约定
→ Implementation Mapping
```

## 第一步：识别仓库事实

先确认：

- 前端框架与渲染模式
- TypeScript 配置
- 路由与状态方案
- 组件库与版本
- CSS / 样式方案（utility CSS、预处理器等）
- 图表方案
- 测试 / Lint / Build 命令
- 现有目录和命名规范

不得假设项目版本和 API。

## Implementation Mapping

每个设计对象必须映射为：

```text
REUSE     → 现有实现满足 Contract
CONFIGURE → 只需配置即可满足
WRAP      → 用产品层包装 vendor 能力
EXTEND    → 在现有实现上增加受控能力
REPLACE   → 现有实现与 Contract 冲突
CREATE    → 缺少合适基础能力
```

并记录理由。策略的完整定义见 `references/design-to-code-protocol.md`。

命中技术 Profile 后的工程基线（状态组织方式 / 类型策略 / 组件库与 utility CSS
的分工）由 Profile 资料提供，按 `routing/resource-map.yaml` 的
`profile_resources` 加载，不在本 Stage 重复维护。

## 实现顺序

```text
Tokens / Theme
→ Foundation
→ Pattern
→ Domain Component
→ Page Composition
→ States
→ Responsive
→ Accessibility
→ Performance
```

## 禁止设计漂移

实现阶段不得静默改变：

- Information Architecture
- Design Direction
- Component Contract
- 页面主任务
- 关键状态
- 设计 Token

确有工程原因需要变化时，记录 deviation；重要变化需要更新 Design Spec。
越界处理与权限规则见 `references/stage-governance.md`。

## 验证

完成代码后必须执行项目中存在的自动化验证；不存在对应脚本时标记为 N/A。对视觉相关实现，若浏览器自动化能力可用，必须执行真实渲染验证：

```text
typecheck
lint（如有）
test（如有）
build（如有）
real browser validation（若环境可用则必须执行；不可用时标记为未验证，不能宣称视觉验收通过）
```

并检查：

- console warning / error
- 关键状态
- keyboard
- responsive transformation
- 真实内容长度
- 表格/图表高负载场景

## 完成标准

“TypeScript 能编译”不等于完成。必须同时满足设计 Contract、运行时行为和实际渲染质量。

## 输出

- 实现代码
- Implementation Mapping
- 必要的 deviation 记录
- 验证结果

Mapping、Token Mapping、State Mapping 与验证清单按
`templates/implementation-plan-deep.md` 的结构输出；命中技术 Profile 时，逐项过一遍
该 Profile 的 implementation checklist 与 quality gates（见
`routing/resource-map.yaml` 的 `profile_resources`）再声明完成。
