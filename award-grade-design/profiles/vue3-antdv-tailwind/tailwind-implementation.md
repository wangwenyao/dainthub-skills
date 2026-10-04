# Tailwind Implementation Rules

## Layout

优先通过 Grid / Flex / Container 与设计 Token 构建结构，不要依赖大量散落的任意 `px`。

## Responsive

优先描述“空间不足时如何重组任务”，而不是“桌面和手机分别长什么样”。

典型动作：

```text
preserve / collapse / reorder / stack / substitute / hide / move-to-overflow
```

## State

明确使用 hover / focus / disabled 等状态，并确保 `focus-visible` 可见。

## 任意值

重复出现三次以上的任意值应触发 Token 提取或组件化（与 `references/design-token-contract.md` 的阈值一致）。
