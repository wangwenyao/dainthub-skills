# Design Specification Schema

Design Specification 是设计与开发之间的稳定契约。

## 必须包含

```text
Product
Experience
Information Architecture
Art Direction
Tokens
Component Contracts
Pages / Journeys
Responsive
Interaction / Motion
Accessibility
Implementation Mapping
QA
Exceptions
```

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
