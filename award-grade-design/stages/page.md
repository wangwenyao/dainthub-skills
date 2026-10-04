# Stage: page — 页面设计

## 目的

只设计目标页面或页面族，明确层级、布局、状态、响应式变换和关键交互。

## 顺序

```text
用户任务
→ 信息层级
→ 页面区域
→ 主路径
→ 状态
→ 响应式转换
→ 视觉表达
```

## 高密度页面

优先形成：

```text
Context → Signal → Comparison → Explanation → Exception → Action
```

而不是机械堆叠 Card。

## 产出

- `<page-id>.page.yaml`（Schema：`schemas/page-dsl.schema.json`；示例：`schemas/page-dsl.example.yaml`）
- 页面 Design Notes 与关键交互 / 状态说明：写入 Page DSL 的对应字段，或 Design
  Specification 的 `screens[]`（composition / motion / accessibility），不另起无模板的独立文档

写进 Design Specification 时按 `templates/design-specification.yaml` 的对应章节，
整体结构与 `schemas/design-spec.json` 对齐；Page DSL 是 `screens[]` 的投影，
字段名必须一致，不要另起同义词。产出后按 `references/design-spec-lint-rules.md`
自检一遍再交付。

## 限制

不得借页面设计修改产品级 IA，除非 Scope 明确包含。
