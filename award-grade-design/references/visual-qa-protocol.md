# Visual QA Protocol

## 目标

只依据真实浏览器渲染判断视觉质量，不根据源代码想象结果。

审查流程、三层审查、缺陷分级与评分停止条件见 `stages/visual-qa.md`。
本文件只补充取证工具与采样范围，不重复流程定义——两处各写一份必然漂移。

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
