# Ant Design Vue 指导

## 定位

Ant Design Vue 是行为基础设施，不是产品视觉语言。

## 优先使用

当它已经满足：

```text
行为
Accessibility
Keyboard
状态语义
```

时优先 `REUSE` 或 `CONFIGURE`。

## 需要封装时

如果产品需要稳定的业务语义、统一状态或视觉差异，使用 `WRAP` / `EXTEND`。

不要把所有 vendor props 原样暴露给 domain component。

## Theme

使用 Theme / ConfigProvider 等能力作为 Product Token 的适配层；不要反过来让 vendor token 决定产品视觉。
