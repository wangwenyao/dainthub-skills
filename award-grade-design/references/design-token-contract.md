# Design Token Contract

## 目标

Token 表达稳定的产品视觉语义，而不是把某个框架的变量名搬进产品层。

## 推荐层级

```text
Product Semantic Tokens
        ↓
Theme Adapter
        ↓
Framework / UI Library / Utility CSS
```

## 典型 Token

```text
color.action.primary
color.surface.base
color.surface.raised
color.text.primary
color.text.secondary
color.border.subtle
space.1 / space.2 / space.3
radius.sm / md / lg
shadow.sm / md
motion.fast / normal
```

## 规则

- 优先语义命名。
- 重复出现三次以上的任意值应考虑提取 Token。
- 不要直接用 vendor token 定义产品品牌语言。
- 不要为单个页面创造大量一次性 Token。
