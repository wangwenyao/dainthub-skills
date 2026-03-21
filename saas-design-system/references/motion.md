# 动画与过渡规范

## 原则

克制风格的动画哲学：**动画服务于理解，而非吸引注意力**。

- 时长短：UI 过渡不超过 200ms，避免用户等待感
- 目的明确：每个动画都在传达状态变化（出现/消失/移动/反馈）
- 可关闭：尊重系统 `prefers-reduced-motion` 设置

## 时长规范

```css
@theme {
  --duration-instant:  50ms;   /* 即时反馈（hover 背景色） */
  --duration-fast:    100ms;   /* 快速反馈（按钮点击） */
  --duration-normal:  150ms;   /* 标准过渡（下拉展开、颜色变化） */
  --duration-slow:    200ms;   /* 复杂动画（模态框进入） */
  --duration-enter:   250ms;   /* 页面级进入动画（上限） */
}
```

## 缓动曲线

```css
@theme {
  --ease-default: cubic-bezier(0.16, 1, 0.3, 1);    /* 快出慢入，自然感 */
  --ease-in:      cubic-bezier(0.4, 0, 1, 1);         /* 退出动画 */
  --ease-out:     cubic-bezier(0, 0, 0.2, 1);         /* 进入动画 */
  --ease-spring:  cubic-bezier(0.34, 1.56, 0.64, 1); /* 弹性（谨慎使用）*/
}
```

## 常用动画模式

### Tailwind 内置类（优先使用）

```html
<!-- 旋转加载 -->
<Loader2 class="animate-spin" />

<!-- 脉冲骨架屏 -->
<div class="animate-pulse bg-neutral-200 rounded" />

<!-- 渐入 -->
<div class="animate-in fade-in duration-150" />

<!-- 从下方滑入（Toast/通知） -->
<div class="animate-in slide-in-from-bottom-2 duration-200" />

<!-- 从上方缩放进入（下拉菜单） -->
<div class="animate-in fade-in zoom-in-95 duration-150" />
```

### Radix Vue 内置过渡

Shadcn-vue 组件（Dialog、DropdownMenu、Tooltip 等）已内置 data-state 过渡，直接使用，无需额外处理：

```css
/* shadcn-vue 已配置，无需手写 */
[data-state='open']  { animation: fadeIn 150ms ease-out; }
[data-state='closed']{ animation: fadeOut 100ms ease-in; }
```

## 禁止事项

- ❌ 禁止页面路由切换加全屏过渡动画（干扰操作效率）
- ❌ 禁止 `transition-all`（性能差，用具体属性如 `transition-colors`）
- ❌ 禁止循环播放动画（除 loading 状态）
- ❌ 禁止弹性动画（ease-spring）用于功能性 UI（只可用于空状态插图等装饰）

## 减少动画支持

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
