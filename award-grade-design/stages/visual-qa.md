# Stage: visual-qa — 浏览器视觉审查

## 目录

- 目的
- 证据要求
- 采样矩阵
- 三层审查
- 缺陷分级
- 评分与停止
- 输出

## 目的

只审查真实浏览器渲染质量，不根据源代码想象最终界面。

默认只读：除非用户明确要求“审查并修复”，否则本 Stage 不修改代码。

## 证据要求

每条发现都必须能追溯到一次真实渲染，并附：

```text
page / viewport / state / observed behavior / user impact / confidence
```

浏览器自动化能力可用时，用 `references/visual-qa-protocol.md` 描述的任意工具取证。
不可用时，只能把相关项标记为“未验证”，不得宣称视觉验收通过；从源码推断出的问题
必须单独标注为“未验证推断”，不要混进已观察到的缺陷里。

## 采样矩阵

Viewport：

```text
1440 × 900
1280 × 800
1024 × 768
390 × 844（产品支持移动端时）
```

应根据产品真实设备矩阵调整，不要机械照搬。

代表性状态至少覆盖：

```text
default / loading / empty / error / success / focus / long-content / narrow-width
```

页面采样范围见 `references/visual-qa-protocol.md`。

## 三层审查

### Macro

构图、信息层级、密度、导向、节奏、主要视觉重量。

### Meso

Table、Card、Filter Bar、Chart、Toolbar、Sidebar、Form、Dialog 等组件级关系。

### Micro

字体、间距、对齐、Icon、Border、State、Focus、Shadow、Motion。

## 缺陷分级

```text
P0 task-blocking
P1 workflow-degrading
P2 visual / consistency defect
P3 optional enhancement
```

每级的具体条目见 `references/visual-defect-catalog.md`。

## 评分与停止

按 SKILL.md 的默认硬门槛与 `references/design-review-rubric.md` 的 100 分模型评分，
每条分数附上面要求的证据与置信度。

停止条件：

```text
存在未解决 P0     → 本 Stage 未完成：输出缺陷清单与下一轮 Top 3，回到修复
任一硬门槛未达标   → 本 Stage 未完成：给出最小修复建议
全部硬门槛通过     → 停止，不主动扩大审查范围
```

迭代时不要在两次审查之间做大量无关修改——否则无法判断是哪一处改动造成了差异。

## 输出

`visual-qa-report.md`，按 `templates/visual-qa-report.md` 的结构输出。
