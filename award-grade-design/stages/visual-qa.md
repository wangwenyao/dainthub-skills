# Stage: visual-qa — 浏览器视觉审查

## 目录

- 证据要求
- 采样矩阵
- 三层审查
- 缺陷分级
- 评分与停止

## 目的

只审查真实浏览器渲染质量，不根据源代码想象最终界面。

## 默认只读

除非用户明确要求“审查并修复”，否则本 Stage 不修改代码。

## 检查顺序

### Macro

构图、信息层级、密度、导向、节奏、主要视觉重量。

### Meso

Table、Card、Filter Bar、Chart、Toolbar、Sidebar、Form、Dialog 等组件级关系。

### Micro

字体、间距、对齐、Icon、Border、State、Focus、Shadow、Motion。

## 默认 Viewport

```text
1440 × 900
1280 × 800
1024 × 768
390 × 844（产品支持移动端时）
```

应根据产品真实设备矩阵进行调整。

## 代表性状态

至少覆盖：

```text
default / loading / empty / error / success / focus / long-content / narrow-width
```

## 缺陷等级

```text
P0 task-blocking
P1 workflow-degrading
P2 visual / consistency defect
P3 optional enhancement
```

## 迭代

```text
找出 Top 3 缺陷
→ 优先修最高影响项
→ 重新渲染受影响页面
→ 比较前后
```

不要在两次审查之间做大量无关修改。
