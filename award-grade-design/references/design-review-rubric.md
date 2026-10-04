# Design Review Rubric

## 100 分内部综合模型

| 维度 | 权重 |
|---|---:|
| Task Success / UX Efficiency | 18 |
| Information Architecture / Density | 14 |
| Visual Design / Art Direction | 16 |
| Interaction / State Quality | 12 |
| Design System Consistency | 10 |
| Accessibility / Responsive / Performance | 10 |
| Data / Content Expression | 7 |
| Innovation / Differentiation | 8 |
| Motion / Micro Interaction | 5 |
| **Total** | **100** |

## 硬门槛

```text
task efficiency < 8.0              → fail
information architecture < 7.5     → fail
interaction quality < 7.0          → fail
accessibility/responsive/perf < 7.0→ fail
visual design < 7.5                → fail
design system < 7.5                → fail
innovation < 6.5（目标包含创新时） → fail
```

## 无视觉通道时的评分姿态

盲查模式（自动化可用、视觉通道不可用）时：

- 文本渠道可验证的维度照常按证据评分，证据加注 `channel: 文本渠道`。
- 依赖感知的判断不评分（Visual Design、Innovation 与 Motion 的审美部分，以及
  Information Architecture 中的扫描性判断——完整清单见
  `references/visual-qa-protocol.md` 的「感知项移交与人工复核」）：标
  「未评分（无视觉通道）」，对应硬门槛在 Gate Status 标「DEFERRED（无视觉通道）」，
  交人工目检后复评。
- Information Architecture / Density 按文本代理评分（标题层级、computed 字号
  阶梯），但「高密度页面扫描性」类感知结论不计入评分依据，在证据中注明该限制。
- 总分只汇总已评维度，并注明「证据受限（无视觉通道）」，不得用满分补齐权重。
- 不得静默估分，不得为了让硬门槛通过而编造视觉分数。

未验证模式（自动化不可用、无本地渲染证据）时不评分：全部条目标「未验证」，交
人工目检后复评。

## 评分必须有证据

每个评分至少关联：

```text
page
viewport
state
observed behavior
user impact
confidence
channel（视觉渠道 / 文本渠道，可选，省略视为视觉渠道）
```

## 分数区间

```text
90–100  卓越，可作为内部标杆
85–89   强品质生产级
78–84   良好，但仍有明显提升空间
70–77   可用，但还没有达到奖项级
<70     需要明显重设计
```


## 评分锚点

每个维度使用 0–10 分，并记录证据与置信度。

总分合成公式：`total = Σ(维度分 × 权重) / 10`。维度分 0–10、权重合计 100，
合成结果落在 0–100 区间，直接套用上方分数区间。

| 分数 | 含义 |
|---:|---|
| 9–10 | 明显高于成熟生产级，具有内部标杆价值 |
| 8 | 稳定的高质量生产级 |
| 7 | 基本达到质量门槛，但仍有明确缺陷 |
| 5–6 | 可用但存在明显体验或一致性问题 |
| 0–4 | 失败、缺失或严重影响任务 |

证据格式：`page / viewport / state / observed behavior / user impact / confidence`，盲查模式加注 `channel`。

不要因为视觉精致而提高 Task Success、IA、Accessibility 等非视觉维度的分数。
