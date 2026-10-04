# Component Strategy — 组件策略

## 选择顺序

```text
现有产品组件
→ Ant Design Vue 能力
→ Wrap / Extend
→ Custom Component
```

前提是先判断 Contract，而不是先看组件库里“有什么”。

## 分层

```text
foundation → pattern → domain → page-local
```

避免 page-local 业务逻辑直接堆在 vendor primitive 上。
