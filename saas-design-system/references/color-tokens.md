# 色彩 Token 完整定义

> 本文件包含完整的色彩 Token CSS 定义，由 SKILL.md 按需加载。

---

## 一、品牌色（蓝紫中性，类 Linear）

```css
@theme {
  --color-brand-50:  oklch(97% 0.015 265);
  --color-brand-100: oklch(93% 0.030 265);
  --color-brand-200: oklch(86% 0.055 265);
  --color-brand-300: oklch(76% 0.090 265);
  --color-brand-400: oklch(64% 0.130 265);
  --color-brand-500: oklch(53% 0.165 265);   /* 主色 */
  --color-brand-600: oklch(45% 0.160 265);
  --color-brand-700: oklch(37% 0.145 265);
  --color-brand-800: oklch(29% 0.115 265);
  --color-brand-900: oklch(21% 0.080 265);
}
```

---

## 二、中性色（略带冷调，避免纯灰）

```css
@theme {
  --color-neutral-0:   oklch(100% 0 0);
  --color-neutral-50:  oklch(98% 0.004 265);
  --color-neutral-100: oklch(95% 0.006 265);
  --color-neutral-200: oklch(90% 0.008 265);
  --color-neutral-300: oklch(82% 0.010 265);
  --color-neutral-400: oklch(68% 0.012 265);
  --color-neutral-500: oklch(54% 0.012 265);
  --color-neutral-600: oklch(42% 0.010 265);
  --color-neutral-700: oklch(31% 0.008 265);
  --color-neutral-800: oklch(21% 0.006 265);
  --color-neutral-900: oklch(13% 0.004 265);
  --color-neutral-950: oklch(8%  0.003 265);
}
```

---

## 三、语义色

```css
@theme {
  --color-success-500: oklch(62% 0.17 145);
  --color-success-100: oklch(94% 0.05 145);
  --color-warning-500: oklch(72% 0.17 75);
  --color-warning-100: oklch(96% 0.05 75);
  --color-danger-500:  oklch(58% 0.22 25);
  --color-danger-100:  oklch(95% 0.05 25);
  --color-info-500:    oklch(60% 0.18 230);
  --color-info-100:    oklch(95% 0.04 230);
}
```

---

## 四、语义角色映射速查

| Token 角色 | 使用场景 | 亮色值 | 暗色值 |
|-----------|---------|--------|--------|
| `bg-base` | 页面主背景 | neutral-50 | neutral-900 |
| `bg-elevated` | 卡片、面板背景 | neutral-0 | neutral-800 |
| `bg-sunken` | 输入框、内嵌区域 | neutral-100 | neutral-950 |
| `bg-overlay` | 弹窗、下拉背景 | neutral-0 + shadow | neutral-700 |
| `border-default` | 通用分割线 | neutral-200 | neutral-700 |
| `border-strong` | 强调边框 | neutral-300 | neutral-600 |
| `text-primary` | 主要文字 | neutral-900 | neutral-50 |
| `text-secondary` | 次要文字 | neutral-500 | neutral-400 |
| `text-placeholder` | 占位符文字 | neutral-400 | neutral-500 |
| `text-disabled` | 禁用状态文字 | neutral-300 | neutral-600 |
| `interactive-default` | 主按钮背景 | brand-500 | brand-400 |
| `interactive-hover` | 主按钮悬停 | brand-600 | brand-500 |

> 暗色模式完整定义 → `references/dark-mode.md`

---

## 五、颜色使用禁令

| ID | 规则 |
|----|------|
| C-COLOR-004 | 禁止用渐变色作为背景或按钮填充 |
| C-COLOR-005 | 禁止在同一页面出现超过 2 个不同品牌色色调 |
| C-COLOR-006 | 禁止用颜色作为**唯一**区分手段（需配合图标或文字） |
| C-COLOR-007 | 禁止使用纯黑（`#000000`）作为文字色 |