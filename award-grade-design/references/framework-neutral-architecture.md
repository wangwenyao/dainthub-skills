# Framework-Neutral Architecture

## 设计原则

框架只是实现层。

```text
Product intent
→ Design Direction
→ Design Tokens
→ Component Contracts
→ Page / Journey Specification
→ Framework implementation
→ Browser QA
```

## 禁止

- 以某个 UI Library 的默认样式定义产品语言。
- 把 Tailwind class、组件库 Theme API 当成 Design System 本身。
- 让具体框架 API 泄漏到业务设计契约。

## 好的边界

```text
Design Contract = 稳定
Implementation Adapter = 可替换
```
