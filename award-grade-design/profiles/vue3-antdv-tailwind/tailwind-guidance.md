# Tailwind 指导

Tailwind 是视觉编排层。

主要负责：

```text
Layout
Grid / Flex
Spacing
Typography
Responsive
Surface
Local State
```

## 原则

优先使用语义 Token；任意值只是 escape hatch。

重复三次以上且表达稳定产品语义的 class 组合，应考虑提取为 pattern、component 或 Token。
