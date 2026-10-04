# Stage: direction — 设计方向

## 目的

确定产品的视觉与体验方向，而不是直接写页面代码。

## 必须定义

```text
产品气质
品牌/视觉观点
Typography 方向
Color Strategy
Surface / Shape
信息密度策略
Motion 原则
视觉记忆点
```

## 高密度系统原则

视觉方向必须服务于任务效率。不能为了“像奖项作品”而引入无意义的大面积留白、动效、3D 或装饰。

## 产出

`design-direction.md`

按 `templates/design-direction.md` 的章节结构输出。下列 Stage 要求与模板章节的对应关系：

- 方向描述 → 设计人格 + 一句话设计主张
- Do / Don't → Do / Don't（含必须拒绝的 Anti-pattern）
- 核心视觉语言 → Typography / Color / Shape / Surface / Iconography / 信息密度策略
- 与现有产品的差异点 → 与现有产品的差异点
- 典型页面示例 → 典型页面示例
- 后续 Design System 应如何承接 → 后续 Design System 应如何承接

## 停止条件

```text
必须定义的八项有任何缺项 → 未完成：补齐后再交付
方向与任务效率冲突（为风格牺牲层级、密度或可扫描性）→ 未完成：回到「高密度系统原则」修订
八项齐备，且 Do / Don't 含明确 Anti-pattern → 停止：Token 与组件承接交给 design-system Stage
```

## 限制

方向以文字论证（关键词、形容词、指名参考）为主；用户提供的参考图在视觉通道不可用时，
请用户口述其视觉特质，不尝试读图。

本 Stage 不修改 application code。
