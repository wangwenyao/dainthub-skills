# Component Contract Patterns — 组件契约分层

## Foundation

稳定、低层、跨页面复用。

## Pattern

一组重复出现的交互组合，例如：

```text
FilterBar
MetricGroup
ResultToolbar
```

## Domain

带稳定业务语义，例如：

```text
ExceptionRow
InsightPanel
ApprovalItem
```

## Page-local

复用价值不确定或只属于单一页面时保持局部。
