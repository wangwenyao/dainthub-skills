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

## 评分必须有证据

每个评分至少关联：

```text
page
viewport
state
observed behavior
user impact
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

| 分数 | 含义 |
|---:|---|
| 9–10 | 明显高于成熟生产级，具有内部标杆价值 |
| 8 | 稳定的高质量生产级 |
| 7 | 基本达到质量门槛，但仍有明确缺陷 |
| 5–6 | 可用但存在明显体验或一致性问题 |
| 0–4 | 失败、缺失或严重影响任务 |

证据格式：`page / viewport / state / observed behavior / user impact / confidence`。

不要因为视觉精致而提高 Task Success、IA、Accessibility 等非视觉维度的分数。
