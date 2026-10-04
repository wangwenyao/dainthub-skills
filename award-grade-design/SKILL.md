---
name: award-grade-design
version: 8.9.0
description: >
  面向高密度信息系统的界面设计质量工程：界面审计、Design Direction、Design System、
  页面与组件设计、按设计契约实现 UI、真实浏览器视觉 QA、局部品质优化。
  触发：界面审计/UI 审查/检查界面问题/设计方向/设计系统/Design Token/组件契约/组件设计/
  页面设计/仪表盘设计/BI 看板/经营分析界面/后台管理系统/高密度表格与筛选器/设计走查/
  视觉 QA/截图审查/界面不够精致/再高级一点/提升界面品质/根据设计稿实现页面/设计一致性审查。
  边界：与 saas-ui-design 分工——本 Skill 负责“做到什么质量、如何验收”，saas-ui-design
  负责“遵循哪套视觉规范”；两者可能同时命中，此时 Stage 与 Scope 以本 Skill 为准。
  不适用：纯营销官网文案、与 UI 无关的普通前端开发、只改后端/接口/数据层。
---

# Award-Grade Design v8.9

## 目标

把高密度信息系统做到“高效、清晰、精致、有辨识度”，而不是把企业软件做成获奖官网。Webby、Awwwards、FWA 只作为外部质量参考。

内部适配系数：

```text
Webby 45%   产品体验 / 结构 / 功能
Awwwards 35% 视觉 / 交互 / 工艺
FWA 20%     创新 / 实验 / 记忆点
```

以上是本 Skill 的内部模型，不代表任何奖项官方权重。

## 核心优先级

```text
任务成功
> 信息清晰与扫描效率
> 可访问性 / 响应式 / 性能
> 设计系统一致性
> 视觉工艺
> 创新与特效
```

高密度不是“少放东西”，而是提高单位视口的信息价值、分组、层级和决策效率。

## 一次只执行一个 Stage

支持：

```text
audit / direction / design-system / page
component / implementation / visual-qa / optimization
```

Stage 选择优先级：

```text
1. 用户明确 Stage / Stage 名称
2. 明确目标对象（组件 / 页面 / 系统）
3. 强动作短语（如“根据 Page Spec 实现”“只审查截图”）
4. 普通动作词（设计 / 实现 / 优化 / 审查）
5. 最小充分 Stage
```

路由时不得只凭单个宽泛词（例如“页面”“设计”“实现”）决定 Stage。优先使用“动作 + 对象”的完整短语；当强动作短语与普通目标词冲突时，以强动作短语为准。显式组件目标（如 DataTable、组件、筛选器）优先于泛化页面词。机器可读形式见 `routing/stage-router.yaml`，人读说明见 `templates/stage-selection.md`。

不得因为进入某个 Stage 就自动执行后续 Stage。完成当前 Stage 的验收条件后停止。

唯一例外：optimization Stage 收尾的局部 Visual QA 属于该 Stage 内的第 5 步动作
（见 `stages/optimization.md`），不构成跨 Stage 自动推进。

## 多 Stage 推进

默认行为是单 Stage：完成即停，由用户决定下一步。

当用户明确要求端到端交付（例如“把这个后台做出来”“从设计到实现”）时，按价值链推进，
但每一轮仍然只做一个 Stage，并在每轮结束时交代：

```text
已完成 Stage 与产出
下一 Stage 及需要用户确认的点
Scope 是否仍然成立
```

推进顺序与交接物见 `references/design-spec-agent-protocol.md`。任何时候发现需求或
Scope 变了，先停在当前 Stage 重新确认，不要带着旧 Scope 往下走——那正是 Design Drift
最常见的起点。

## Scope Contract

每个任务必须有明确边界：

```yaml
scope:
  stage: component
  targets: [DataTable]
  allowed: [component, scoped-token]
  forbidden: [product-ia, unrelated-pages, unrelated-components]
  write_mode: design-artifacts
```

完整契约（含 context / outputs / acceptance）见 `templates/stage-scope-contract.yaml`。

禁止静默扩大 Scope。发现越界依赖时，记录 dependency/deviation，不得顺手修改。

权限基线：

| Stage | 默认权限 |
|---|---|
| audit | read-only |
| direction | artifact-only |
| design-system | design-artifacts |
| page | design-artifacts |
| component | design-artifacts |
| implementation | code |
| visual-qa | read-only |
| optimization | patch |

机器权威定义在 `routing/scope-router.yaml`；本表是它的投影，由 Eval 门禁保证一致。
要改权限，改 `scope-router.yaml`，不要只改这张表。

## Context Routing

只加载当前 Stage 所需的最小资源：

1. 读取对应 `stages/*.md`。
2. 按 `routing/resource-map.yaml` 加载必要 Pack / Reference；仅加载与当前 Stage 和 Scope 直接相关的资源。
3. 需要代码实现时，再加载技术 Profile。
4. Benchmark、AI、Data Viz、Motion 等专项资料只在命中相关信号时加载。

不要一次加载全部 references，也不要重复加载已在 SKILL.md 中明确规定的核心原则。

## 技术 Profile

Core 保持框架无关。确认项目技术栈后才加载 Profile。当前参考 Profile：

`profiles/vue3-antdv-tailwind/profile.yaml`

该 Profile 只改变实现指导，不改变通用设计质量门槛。

## 设计与实现的边界

统一关系：

```text
产品目标
→ Design Direction
→ Design Tokens
→ Component Contracts
→ Page / Journey Spec
→ Implementation
→ Browser QA
```

技术栈是实现约束，不是设计权威。组件库是行为基础设施，不是产品视觉真相。

## 质量门槛

重大重设计使用 100 分内部综合模型；详细评分见 `references/design-review-rubric.md`。

默认硬门槛：

```text
P0 = 0
Task Efficiency ≥ 8.0
Information Architecture ≥ 7.5
Interaction ≥ 7.0
Accessibility / Responsive / Performance ≥ 7.0
Visual Design ≥ 7.5
Design System Consistency ≥ 7.5
```

只有目标明确包含创新时，Innovation ≥ 6.5 才作为硬门槛。

## Visual QA 原则

视觉 QA 以真实浏览器渲染为证据。若具备浏览器自动化能力，`implementation` 完成后必须进行真实渲染验证；若当前环境没有浏览器能力，只能标记为“未验证”，不得宣称视觉验收通过。

## Design Drift

实现阶段不得静默改变：

- Information Architecture
- Design Direction
- Component Contract
- 页面主任务
- 关键状态
- Design Tokens

确需变化时记录 deviation；影响体验契约的变化必须更新对应设计资产。

## 资源导航

**Stage**：

- `stages/audit.md`
- `stages/direction.md`
- `stages/design-system.md`
- `stages/page.md`
- `stages/component.md`
- `stages/implementation.md`
- `stages/visual-qa.md`
- `stages/optimization.md`

**Routing**：`routing/stage-router.yaml`、`routing/scope-router.yaml`、`routing/resource-map.yaml`

**Schemas**：`schemas/design-spec.json`、`schemas/page-dsl.schema.json`、`schemas/page-dsl.example.yaml`

**Templates**：`templates/` 定义各 Stage 的产出结构。每个 Stage 必须按
`routing/resource-map.yaml` 为该 Stage 指定的模板输出，不要自创章节——结构稳定
才能跨轮次、跨页面比较。

**Governance**：`references/stage-governance.md`

**端到端流程**：`references/design-spec-agent-protocol.md`（Stage / Scope 优先级高于该流程）

**Host 接口元数据**：`agents/openai.yaml`

**技术 Profile**：`profiles/vue3-antdv-tailwind/`

**Stage 深度资料**：按 `routing/resource-map.yaml` 加载，不要全量读取。

**Eval**：`evals/evolution-policy.yaml` 定义发布门禁；`evals/trigger-evals.json` 是触发质量回归集；`scripts/run_evals.py` 是统一确定性回归入口。

## Eval-Driven Evolution

本 Skill 采用 Eval-first 的维护方式。任何会改变触发、Stage 路由、Scope、Resource Map、Technology Profile 或核心执行规则的修改，都必须先更新对应 Eval，再修改实现。

发布门禁分为两层：

```text
Deterministic Evals
→ 必须 100% 通过

Qualitative Evals
→ 针对设计判断、实现忠实度、视觉 QA 等需要模型/人工审查的行为，必须有可追踪的评分记录
```

固定回归入口：

```bash
python scripts/run_evals.py <skill-dir>
```

它逐项检查 Package Hygiene、Resource Routing、Stage Routing、Scope Safety、
Profile Selection 与 Context Budget；退出码非 0 即不得发布。

完整检查项、定性覆盖要求与失败记录格式见 `evals/evolution-policy.yaml`。
那里是门禁的唯一权威定义，本文件不重复清单，避免两处漂移。

每个真实失败都要落成一条 failure record：

```text
prompt
expected behavior
actual behavior
failure class
minimal fix
regression case
```

不要通过不断追加自然语言来掩盖系统性问题。优先修复 Router、Scope Contract、Resource Map、Profile detection 或确定性脚本。

## 完成规则

当前 Stage 的 acceptance criteria 通过后立即停止。不要把一次局部任务升级成完整 redesign。完成重大修改后，必须通过 Eval release gate 后再发布新版本。

## 版本

- v8.9
- 更新: 2026-10-04
- v8.8 → v8.9：修复模板与 Stage 契约断裂（direction / optimization / design-specification.md）、
  坏 pack 引用、框架泄漏字段；收敛信息流定义与 viewport 矩阵单一权威；补 activation 语义
  与评分合成公式；门禁新增 md 模板策略词表、信息流一致性、scope-contract packs 解析检查。
