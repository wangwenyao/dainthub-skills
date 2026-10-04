# Component Deep Review

审查重点：

1. 是否真的具有复用语义。
2. 是否选择了正确层级：foundation / pattern / domain / page-local。
3. API 是否过度耦合 vendor。
4. State、Density、Responsive、Accessibility 是否完整。
5. 是否存在过度抽象或 wrapper 套娃。
6. 是否有明确的性能与可测试性策略。

## 通过标准

组件必须能够在没有额外“页面特例补丁”的情况下稳定完成自己的 Contract。
