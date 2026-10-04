# Design-to-Code Protocol

每个设计对象必须选择一个主要实现策略：

```text
REUSE   → 现有实现满足 Contract
CONFIGURE → 只需配置即可满足
WRAP    → 用产品层包装 vendor 能力
EXTEND  → 在现有实现上增加受控能力
REPLACE → 现有实现与 Contract 冲突
CREATE  → 缺少合适基础能力
```

## 原则

- 不因为写代码方便就降低设计 Contract。
- 不因为视觉细节就轻易推翻稳定基础能力。
- 所有重要替换都记录理由。
