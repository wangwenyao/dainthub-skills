# Page Design DSL

Page DSL 用来描述页面意图、层级、区域、状态、交互和 Responsive 变换。

它不是视觉稿语言，也不是某个框架的代码生成器。

## 与 Design Spec 的关系

Page DSL 是 `schemas/design-spec.json` 中 `screens[]` 单个元素的投影：

```text
schemas/page-dsl.schema.json   单个屏幕
schemas/design-spec.json       screens[] 的容器
```

两者的 `required` 字段集必须相同，字段名也不得另起同义词。这样单个页面可以先独立
设计和校验，再原样并入 Design Spec，而不是在两套字段名之间做一次有损翻译。

## 典型字段

```yaml
id: ops-overview
archetype: analytical-dashboard
purpose: "..."
primary_task: "..."
primary_action: "..."
density: compact
information_hierarchy: []
composition: {}
components: []
states: []
responsive: {}
motion: {}
accessibility: {}
data_viz: {}
```

完整示例见 `schemas/page-dsl.example.yaml`。

## 原则

先描述“要让用户完成什么”，再描述“页面如何长”。`primary_task` 只能有一个主答案；
出现并列说明页面职责还没切分清楚，应该拆成两个屏幕。
