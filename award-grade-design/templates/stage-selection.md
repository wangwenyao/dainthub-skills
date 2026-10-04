# Stage Selection

> 本文件是 `routing/stage-router.yaml` 的人读投影。规则冲突时，以 SKILL.md 与
> stage-router.yaml 为准；不要在修改路由后单独改本文件而漏改权威源。

## 优先级（与 stage-router.yaml 的 precedence 一致）

1. 用户明确指定 Stage（如“只做 visual-qa”）。
2. 用户明确指定目标对象类型（组件 / 页面 / 系统）。
3. 强动作短语命中（如“根据 Page Spec 实现”“只审查截图”）。
4. 普通动作词 + 目标对象评分（设计 / 实现 / 优化 / 审查 × 页面 / 组件 / UI）。
5. 选择最小充分 Stage。

## 歧义规则（常见冲突的裁决）

- 明确组件目标（DataTable、筛选器、表格）优先于泛化页面词 → `component`。
- 实现类动作 + 页面 / UI 目标同时出现 → `implementation`。
- 审计类动作 + 页面 / dashboard 目标同时出现 → `audit`。
- QA / 审查语言 + 截图或视觉证据 → `visual-qa`。
- 明确与 UI 无关（后端 / API / 文档）→ 不进入本 Skill。

不得只凭单个宽泛词（“页面”“设计”“实现”）决定 Stage。

## 历史别名（仅兼容）

`light → optimization`，`redesign → audit`，`new-product → direction`。