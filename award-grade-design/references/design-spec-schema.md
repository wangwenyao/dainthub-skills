# Design Specification Schema

Design Specification 是设计与开发之间的稳定契约。

至少包含：

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

## 目标

既能给人审阅，又能给 Agent 消费。不要绑定具体框架。

机器结构见 `schemas/design-spec.json` 与 `schemas/design-spec.json`。


规范入口：`schemas/design-spec.json`。该文件是唯一机器 Schema，避免多个副本产生漂移。
