# Page Design DSL

Page DSL 用来描述页面意图、层级、区域、状态、交互和 Responsive 变换。

它不是视觉稿语言，也不是某个框架的代码生成器。

## 典型字段

```yaml
page:
  id: ops-overview
  archetype: analytical-dashboard
  purpose: "..."
  density: compact
  hierarchy: []
  primary_action: "..."
composition: {}
states: []
responsive: {}
```

## 原则

先描述“要让用户完成什么”，再描述“页面如何长”。
