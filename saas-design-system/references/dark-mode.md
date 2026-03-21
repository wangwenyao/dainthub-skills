# 暗色模式规范

## 核心原则

B端 SaaS 的暗色模式不是"把白色变黑色"，而是一套**独立设计的第二套主题**。

Linear、Notion、GitHub 的暗色主题共同特征：
- 背景不是纯黑（`#000`），而是带轻微蓝灰色调的深色
- 边框比背景亮度高约 8–12%，层次通过亮度差而非颜色差区分
- 文字不是纯白，主文字约 `oklch(95%)`，避免刺眼

---

## 一、Token 体系（亮色模式）

```css
:root {
  /* ── 背景层级 ── */
  --bg-base:     oklch(98% 0.004 265);   /* 页面主背景 */
  --bg-elevated: oklch(100% 0 0);         /* 卡片、面板 */
  --bg-sunken:   oklch(95% 0.006 265);    /* 输入框、内嵌 */
  --bg-overlay:  oklch(100% 0 0);         /* 弹窗、下拉 */

  /* ── 边框 ── */
  --border-default: oklch(90% 0.008 265);
  --border-strong:  oklch(82% 0.010 265);

  /* ── 文字 ── */
  --text-primary:     oklch(13% 0.004 265);
  --text-secondary:   oklch(42% 0.010 265);
  --text-placeholder: oklch(68% 0.012 265);
  --text-disabled:    oklch(78% 0.008 265);

  /* ── 交互 ── */
  --interactive-default: oklch(53% 0.165 265);
  --interactive-hover:   oklch(45% 0.160 265);
}
```

---

## 二、Token 体系（暗色模式）

```css
.dark {
  /* 背景层级（从深到浅，表达层次） */
  --bg-base:     oklch(12% 0.005 265);   /* 最底层，页面背景 */
  --bg-elevated: oklch(15% 0.006 265);   /* 卡片、面板 */
  --bg-sunken:   oklch(10% 0.004 265);   /* 输入框、内嵌 */
  --bg-overlay:  oklch(18% 0.007 265);   /* 下拉、弹窗 */

  /* 边框 */
  --border-default: oklch(25% 0.008 265);
  --border-strong:  oklch(32% 0.010 265);

  /* 文字 */
  --text-primary:     oklch(92% 0.005 265);
  --text-secondary:   oklch(55% 0.008 265);
  --text-placeholder: oklch(40% 0.006 265);
  --text-disabled:    oklch(30% 0.005 265);

  /* 交互 */
  --interactive-default: oklch(58% 0.165 265);  /* 暗色下主色略亮 */
  --interactive-hover:   oklch(65% 0.160 265);
  --focus-ring:          oklch(58% 0.165 265 / 0.4);
}
```

---

## 三、shadcn-vue 变量对照

与 shadcn-vue 内置变量完全对齐，确保组件库兼容：

```css
/* 亮色模式 */
:root {
  --background: 0 0% 100%;
  --foreground: 222 47% 11%;
  --card: 0 0% 100%;
  --card-foreground: 222 47% 11%;
  --popover: 0 0% 100%;
  --popover-foreground: 222 47% 11%;
  --primary: 221 83% 53%;           /* brand-500 */
  --primary-foreground: 0 0% 100%;
  --secondary: 210 40% 96%;
  --secondary-foreground: 222 47% 11%;
  --muted: 210 40% 96%;
  --muted-foreground: 215 16% 47%;
  --accent: 210 40% 96%;
  --accent-foreground: 222 47% 11%;
  --destructive: 0 84% 60%;         /* danger-500 */
  --destructive-foreground: 0 0% 100%;
  --border: 214 32% 91%;
  --input: 214 32% 91%;
  --ring: 221 83% 53%;
  --radius: 0.5rem;
}

/* 暗色模式 */
.dark {
  --background: 222 47% 11%;
  --foreground: 210 40% 98%;
  --card: 222 47% 13%;
  --card-foreground: 210 40% 98%;
  --popover: 222 47% 13%;
  --popover-foreground: 210 40% 98%;
  --primary: 217 91% 60%;
  --primary-foreground: 222 47% 11%;
  --secondary: 217 33% 17%;
  --secondary-foreground: 210 40% 98%;
  --muted: 217 33% 17%;
  --muted-foreground: 215 20% 65%;
  --accent: 217 33% 17%;
  --accent-foreground: 210 40% 98%;
  --destructive: 0 62% 50%;
  --destructive-foreground: 210 40% 98%;
  --border: 217 33% 20%;
  --input: 217 33% 20%;
  --ring: 224 76% 48%;
}
```

---

## 四、层次区分策略

暗色下不能用边框区分层次（边框太多会有"格子感"），改用**背景亮度差**：

```
页面背景        oklch(12% 0.010 255)   ← 最深
侧边栏/顶栏     oklch(13% 0.012 255)   ← 略亮
卡片/面板       oklch(15% 0.013 255)   ← 再亮一级
Popover/Dropdown oklch(17% 0.015 255)  ← 最亮，浮于页面之上
```

---

## 五、暗色模式下的阴影

暗色模式阴影要弱化，改用边框增强层次感：

```css
.dark {
  --shadow-sm: 0 1px 3px oklch(0% 0 0 / 0.3);
  --shadow-md: 0 4px 16px oklch(0% 0 0 / 0.4);
  --shadow-lg: 0 12px 48px oklch(0% 0 0 / 0.5);
}
```

---

## 六、实现方式（Tailwind + Vue）

```typescript
// composables/useTheme.ts
import { useColorMode } from '@vueuse/core'

export function useTheme() {
  const mode = useColorMode({
    attribute: 'class',           // 通过 class="dark" 切换
    modes: { light: 'light', dark: 'dark' },
    storageKey: 'color-scheme',
    initialValue: 'system',       // 默认跟随系统
  })

  const isDark = computed(() => mode.value === 'dark')

  function toggle() {
    mode.value = isDark.value ? 'light' : 'dark'
  }

  return { mode, isDark, toggle }
}
```

```vue
<!-- 切换按钮 -->
<script setup lang="ts">
import { Moon, Sun } from 'lucide-vue-next'
import { useTheme } from '@/composables/useTheme'

const { isDark, toggle } = useTheme()
</script>

<template>
  <Button variant="ghost" size="icon" aria-label="切换主题" @click="toggle">
    <Sun v-if="isDark" class="h-4 w-4" />
    <Moon v-else class="h-4 w-4" />
  </Button>
</template>
```

---

## 七、常见暗色模式陷阱

| 问题 | 错误做法 | 正确做法 |
|------|----------|----------|
| 图片在暗色下太亮 | 不处理 | `filter: brightness(0.85)` 或使用带透明通道的 SVG |
| 阴影在暗色下不可见 | 用浅色阴影 | 暗色下阴影改用 `ring-1 ring-white/5`（内发光边框替代） |
| 表格斑马纹太强 | `bg-gray-100` 隔行 | 暗色下用 `odd:bg-white/[0.02]`，极轻微 |
| 代码块背景 | 跟随页面背景 | 代码块背景比页面深一级，制造"沉入感" |
| Skeleton 颜色 | 固定灰色 | 暗色下 `bg-white/8` + `animate-pulse` |

---

## 八、注意事项

- 图表颜色在暗色模式下需单独调整（提高亮度 10-15%）
- 截图/图片组件需加 `dark:brightness-90` 避免过亮
- 语义色在暗色下使用 `*-400` 替代 `*-500`（提高可读性）
- 禁止彩色阴影、多层叠加阴影、hover 时加大阴影