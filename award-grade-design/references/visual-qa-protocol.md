# Visual QA Protocol

## 目标

只依据真实浏览器渲染判断视觉质量，不根据源代码想象结果。

## Browser abstraction

可使用环境中现有的任意浏览器自动化能力，例如：

- Playwright
- agent-browser
- browser-use
- 其他等价工具

不把具体工具写死到 Design Spec。

## 默认截图矩阵

```text
1440 × 900
1280 × 800
1024 × 768
390 × 844（产品支持移动端时）
```

## 页面采样

至少覆盖：

- Overview / Entry
- Primary Work Surface
- 高密度数据页
- Form / Operation
- Detail
- Empty
- Loading
- Error
- Responsive

## 三层审查

### Macro

构图、层级、密度、方向感、节奏、主要视觉重量。

### Meso

Table、Card、Filter Bar、Chart、Toolbar、Sidebar、Form、Dialog。

### Micro

字体、间距、对齐、Icon、Border、状态、Focus、Shadow、Motion。

## 缺陷等级

```text
P0 task-blocking
P1 workflow-degrading
P2 visual / consistency defect
P3 optional enhancement
```

## 迭代规则

```text
找 Top 3
→ 修最高影响项
→ 重新渲染
→ 比较 Before / After
```
