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

渲染事实可经视觉渠道（模型查看截图）或文本渠道（DOM / computed style / 几何等确定性
事实）取证，两者都算真实渲染证据；美学判断只属于视觉渠道。运行模式按
`references/visual-qa-protocol.md` 的「能力判定与运行模式」判定，本 Stage 不重复维护
判定规则。

默认只读：除非用户明确要求“审查并修复”，否则本 Stage 不修改代码。

## 证据要求

每条发现都必须能追溯到一次真实渲染，并附：

```text
page / viewport / state / observed behavior / user impact / confidence
channel（视觉渠道 / 文本渠道，可选，省略视为视觉渠道）
```

浏览器自动化能力可用时，先按 `references/visual-qa-protocol.md` 的
「能力判定与运行模式」判定模型视觉通道：可用 → 完整模式，用协议描述的任意工具取证
并做像素审查；不可用 → 盲查模式，只做文本渠道取证，截图照常生成并归档移交用户，
逐项加注 `channel: 文本渠道`，感知项标「未验证（需视觉通道）」。自动化能力不可用时，
本地渲染相关项只能标记为「未验证」（用户提供的截图若模型可查看，仍可作为作证
证据），不得宣称视觉验收通过；从源码推断出的问题必须单独标注为「未验证推断」，
不要混进已观察到的缺陷里。

用户直接提供截图作为唯一证据且视觉通道不可用时，先如实告知本会话无法查看图片，
请其口述画面要点或提供可导航的页面（改走文本渠道取证），不要产出一份全「未验证」
的空报告，更不得假装已查看截图。口述只用于澄清任务与上下文：据口述得出的界面结论
一律标「未验证推断」并在 confidence 注明依据为用户口述，未经真实渲染佐证不得计入
P0 / P1。

## 采样矩阵

Viewport 采样矩阵的唯一权威定义在 `references/visual-qa-protocol.md` 的「默认截图矩阵」；
本 Stage 不重复维护副本，按产品真实设备矩阵调整即可。矩阵中的每个 viewport 同时是两种
渠道的取样点：完整模式截图像素审查，盲查模式在同一 viewport 做 DOM 几何测量与状态
断言；截图始终生成，作为移交用户的证据。

代表性状态至少覆盖：

```text
default / loading / empty / error / success / focus-visible / long-content / narrow-width
```

页面采样范围见 `references/visual-qa-protocol.md`。

## 三层审查

渠道分工：Macro 的构图、导向、节奏、视觉重量是感知判断，需视觉通道，盲查模式下标
「未验证（需视觉通道）」并移交人工复核；信息层级有文本代理（标题层级、computed 字号
阶梯），高密度页面的扫描性无文本代理，同样移交人工复核。Meso 全部可经文本渠道核实
（包围盒重叠、elementFromPoint / z-index 命中、跨实例 computed style 一致性）；Micro
的可计算属性可经文本渠道核实（字号 / 行高 / 间距 / 边缘差值对齐 / 边框宽度 /
box-shadow 值 / transition 属性 / focus-visible outline，映射表见协议「盲查取证通道」），
但「是否过度」「感知质量」类判断（如 Card / Border / Shadow 过度）无文本代理，按
`references/visual-defect-catalog.md` 的「渠道可验证性」标「未验证（需视觉通道）」。

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
每条分数附上面要求的证据与置信度。盲查模式按 `references/design-review-rubric.md`
的「无视觉通道时的评分姿态」执行：文本渠道可验证维度照常评分并注明 channel；
感知维度标「未评分（无视觉通道）」，不得静默估分。

停止条件：

```text
存在未解决 P0     → 本 Stage 未完成：输出缺陷清单与下一轮 Top 3，回到修复
已评分硬门槛中任一未达标（DEFERRED 项不计入）→ 本 Stage 未完成：给出最小修复建议
盲查模式且感知项已移交人工复核、其余硬门槛全部通过
                  → 停止：视觉项标「未验证（需视觉通道）」并移交人工复核，
                    Gate Status 标「DEFERRED（无视觉通道）」，不得宣称视觉验收通过
全部硬门槛通过     → 停止，不主动扩大审查范围
未验证模式（无本地渲染证据）→ 不评分、不判门槛：输出未验证项清单与人工复核请求，
                  移交用户决定下一步，不得宣称视觉验收通过
唯一证据为截图且视觉通道不可用、用户无法补充材料
                  → 停止：说明证据不足并移交人工目检，不评分
```

迭代时不要在两次审查之间做大量无关修改——否则无法判断是哪一处改动造成了差异。

## 输出

`visual-qa-report.md`，按 `templates/visual-qa-report.md` 的结构输出。
