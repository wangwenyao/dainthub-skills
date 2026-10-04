---
name: award-grade-design
description: 面向高密度信息系统的设计、交互、设计系统、组件工程实现与浏览器视觉 QA。用于 SaaS、BI、经营分析、CRM/CDP/MA、数据平台、AI 工作台、运营平台、科研软件等场景；支持界面审计、Design Direction、Design System、页面/组件设计、根据设计契约实现 UI、视觉 QA 和局部优化。仅在任务涉及界面设计质量或用户明确指定本 Skill 时使用；不要用于纯营销官网文案或与 UI 无关的普通前端开发。
---

# Award-Grade Design v8.7

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

路由时不得只凭单个宽泛词（例如“页面”“设计”“实现”）决定 Stage。优先使用“动作 + 对象”的完整短语；当强动作短语与普通目标词冲突时，以强动作短语为准。显式组件目标（如 DataTable、组件、筛选器）优先于泛化页面词。

不得因为进入某个 Stage 就自动执行后续 Stage。完成当前 Stage 的验收条件后停止。

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

**Schemas**：`schemas/design-spec.json`、`schemas/page-dsl.example.yaml`

**技术 Profile**：`profiles/vue3-antdv-tailwind/`

**Stage 深度资料**：按 `routing/resource-map.yaml` 加载，不要全量读取。

**Eval**：`evals/evolution-policy.yaml` 定义发布门禁；`scripts/run_evals.py` 是统一确定性回归入口。

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

必须覆盖：

- Stage Routing：正向、歧义、负向触发。
- Scope Safety：不得扩大到未授权页面、组件、IA 或代码。
- Profile Selection：不得因弱信号误激活技术 Profile。
- Resource Routing：所选 Stage 的必要资源必须存在，且不得要求全量加载。
- Package Hygiene：目录名与 frontmatter 一致、无 `__pycache__`、无重复 canonical schema、无发布版本残留。
- Context Budget：Core 保持精简，Stage 规则通过渐进式加载获取。

每个真实失败都要记录：

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
