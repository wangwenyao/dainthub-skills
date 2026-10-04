# Implementation Deep Review

## Review 顺序

```text
Repository facts
→ Design Contract
→ Implementation Mapping
→ Code structure
→ Runtime state
→ Browser render
→ Validation
```

## 常见风险

- 设计 Token 没有真正进入实现。
- vendor API 直接泄漏到 domain component。
- page-local 逻辑被误抽成通用组件。
- 状态只覆盖 default。
- Responsive 只是缩放，没有任务级变换。
- 代码能编译，但真实渲染仍然像默认后台模板。

## 通过条件

代码、运行时行为、视觉结果和 Design Contract 必须一致；出现重要偏差必须记录 deviation。
