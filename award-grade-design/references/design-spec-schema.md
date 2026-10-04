# Design Specification Schema

Design Specification 是设计与开发之间的稳定契约。

## 顶层结构

机器 Schema（`schemas/design-spec.json`）声明 8 个顶层 required 字段：

```text
spec_version
product                  产品上下文（含目标用户 / JTBD / 约束）
experience               目标 / 原则 / 成功指标 / 反目标
information_architecture 导航 / 层级 / 对象 / 旅程
art_direction            概念 / 气质 / 视觉支柱 / Typography / Color / Shape / Surface
system                   Tokens / Component Contracts / Patterns / Density
screens[]                页面规格（responsive / motion / accessibility / states 在此层）
qa                       Viewports / Critical flows / Acceptance criteria / Evidence
```

`implementation`（六策略映射）与 `exceptions`（deviation 记录）是 Schema 声明的可选顶层字段。
概念词 "Pages / Journeys"、"Responsive"、"Interaction / Motion"、"Accessibility" 分属
`information_architecture` 与 `screens[]` 内的字段，不是独立顶层章节——按概念清单填写
会过不了校验，以 `schemas/design-spec.json` 的字段名为准。

## 机器结构

```text
schemas/design-spec.json              唯一机器 Schema，避免多个副本产生漂移
schemas/page-dsl.schema.json          Page DSL（screens[] 单个元素）的 Schema
schemas/page-dsl.example.yaml         Page DSL 示例
templates/design-specification.yaml   可直接填写的空白骨架
templates/design-specification.md     人读版本
```

Page DSL 是 `screens[]` 的投影，两者 `required` 字段集必须一致，字段名不得另起
同义词；否则页面级校验通过、并入总 Spec 时却对不上。

## 目标

既能给人审阅，又能给 Agent 消费。不要绑定具体框架。
