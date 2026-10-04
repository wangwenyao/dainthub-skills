# Design Spec Agent Protocol

端到端交付时每轮仍然只执行一个 Stage；本文件定义 Stage 之间的推进顺序、交接物
与协议相位的映射。Stage / Scope 优先级高于默认流程：小任务不得因为这个协议而
自动升级为完整项目流程。

## 推进顺序

按价值链推进，audit / component / optimization 为按需环节：

```text
audit（可选，先诊断）
→ direction
→ design-system
→ page
→ component（按需：出现可复用组件族或明确组件目标时）
→ implementation
→ visual-qa
→ optimization（可选，收尾局部提升）
```

每轮结束时交代：已完成 Stage 与产出、下一 Stage 及需要用户确认的点、Scope 是否
仍然成立。任何时候发现需求或 Scope 变了，先停在当前 Stage 重新确认，不要带着
旧 Scope 往下走——那正是 Design Drift 最常见的起点。

## 交接物

下一 Stage 唯一认可的输入，是上一 Stage 按模板产出的交接物；没有交接物就没有推进：

| Stage | 交接物 | 结构权威 |
|---|---|---|
| audit | `design-audit.md` | `templates/design-audit.md` |
| direction | `design-direction.md` | `templates/design-direction.md` |
| design-system | Design System Brief + Design Specification + Tokens + Component Contracts + Theme Strategy（Theme Strategy 是 Brief 的章节） | `templates/design-system-brief.md` / `templates/design-specification.yaml` |
| page | `<page-id>.page.yaml`，或 Design Specification 的 `screens[]` | `schemas/page-dsl.schema.json`；写 `screens[]` 时按 `templates/design-specification.yaml` |
| component | Component Contract + selection decision + implementation notes | `templates/component-contract-deep.yaml` |
| implementation | 实现代码 + Implementation Mapping + deviation 记录 + 验证结果 | `templates/implementation-plan-deep.md` |
| visual-qa | `visual-qa-report.md` | `templates/visual-qa-report.md` |
| optimization | `optimization-report.md` + 局部 Visual QA 记录 | `templates/optimization-report.md` / `templates/visual-qa-report.md` |

## 相位与 Stage 的映射

`Discover → Specify → Validate → Implement → Render → Audit → Iterate → Close`
是一轮完整交付的节拍，不是另一套 Stage；两者按下面的映射对齐：

```text
Discover   问题澄清与 Scope 确认（audit / direction 之前）
Specify    设计资产产出（direction / design-system / page / component）
Validate   产出自检（各 Stage 内按 references/design-spec-lint-rules.md 与 Schema 校验完成）
Implement  implementation Stage
Render     实现后的真实浏览器渲染（implementation / visual-qa 内完成）
Audit      visual-qa Stage
Iterate    optimization Stage 的局部提升
Close      当前 Stage 验收条件通过后的停止
```
