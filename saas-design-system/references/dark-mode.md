# 暗色模式规范

## 设计原则

B端 SaaS 的暗色模式不是"把白色变黑色"，而是一套独立的色彩层级体系。参照 Linear、Vercel、GitHub 的暗色方案：背景不用纯黑，用略带色调的深色；避免高对比度造成的视觉疲劳。

## Token 映射（暗色模式）

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

## 暗色模式下的阴影

暗色模式阴影要弱化，改用边框增强层次感：

```css
.dark {
  --shadow-sm: 0 1px 3px oklch(0% 0 0 / 0.3);
  --shadow-md: 0 4px 16px oklch(0% 0 0 / 0.4);
  --shadow-lg: 0 12px 48px oklch(0% 0 0 / 0.5);
}
```

## 实现方式（Tailwind + Vue）

```typescript
// composables/useColorMode.ts
import { useColorMode } from '@vueuse/core'

export function useTheme() {
  const mode = useColorMode({
    attribute: 'class',
    modes: { light: 'light', dark: 'dark' },
    storageKey: 'color-scheme',
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
const { isDark, toggle } = useTheme()
</script>

<template>
  <Button variant="ghost" size="icon" @click="toggle" aria-label="切换主题">
    <Sun v-if="isDark" class="h-4 w-4" />
    <Moon v-else class="h-4 w-4" />
  </Button>
</template>
```

## 注意事项

- 图表颜色在暗色模式下需单独调整（提高亮度 10-15%）
- 截图/图片组件需加 `dark:brightness-90` 避免过亮
- 语义色在暗色下使用 `*-400` 替代 `*-500`（提高可读性）
