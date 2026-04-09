# 高级细节规范

> 专业感来自细节的精确控制。每个微交互都有存在的理由。

## 一、微交互规范

### 1.1 按钮交互

```vue
<script setup lang="ts">
import { ChevronRight } from 'lucide-vue-next'
</script>

<template>
  <!-- 主按钮：hover 时微妙上移 + 阴影加深 -->
  <button class="px-4 py-2 rounded-md bg-brand-500 text-white
    transition-all duration-100 ease-out
    hover:-translate-y-px hover:shadow-sm hover:bg-brand-600
    active:translate-y-0 active:shadow-none
    focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/50">
    提交
  </button>
  <!-- 幽灵按钮 -->
  <button class="px-3 py-1.5 rounded-md text-neutral-600 transition-colors duration-100
    hover:bg-neutral-100 hover:text-neutral-900 active:bg-neutral-200">取消</button>
  <!-- 图标按钮 -->
  <button class="p-2 rounded-md text-neutral-500 transition-all duration-100
    hover:bg-neutral-100 hover:text-neutral-700 active:scale-95">
    <ChevronRight class="w-4 h-4" />
  </button>
</template>
```

**时序标准**：
| 状态 | 时长 | 属性 |
|------|------|------|
| hover 背景色 | 100ms | `transition-colors` |
| hover 位移/缩放 | 100ms | `transition-all` |
| active 按下 | 即时 | 无过渡 |
| focus ring | 100ms | `transition-shadow` |

### 1.2 输入框焦点

```vue
<template>
  <input class="w-full px-3 py-2 rounded-md border border-neutral-200 bg-white
    transition-all duration-100 hover:border-neutral-300
    focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20
    placeholder:text-neutral-400" placeholder="请输入" />
</template>
```

### 1.3 复选框

```vue
<script setup lang="ts">
import { Check } from 'lucide-vue-next'
import { ref } from 'vue'
const checked = ref(false)
</script>

<template>
  <button @click="checked = !checked"
    class="w-4 h-4 rounded-sm border flex items-center justify-center transition-all duration-100"
    :class="checked ? 'bg-brand-500 border-brand-500' : 'border-neutral-300 hover:border-neutral-400'">
    <Check v-if="checked" class="w-3 h-3 text-white" />
  </button>
</template>
```

### 1.4 开关切换

```vue
<script setup lang="ts">
import { ref } from 'vue'
const enabled = ref(false)
</script>

<template>
  <button @click="enabled = !enabled"
    class="relative w-9 h-5 rounded-full transition-colors duration-150"
    :class="enabled ? 'bg-brand-500' : 'bg-neutral-200'">
    <span class="absolute top-0.5 left-0.5 w-4 h-4 rounded-full bg-white shadow-sm
      transition-transform duration-150 ease-out" :class="enabled && 'translate-x-4'" />
  </button>
</template>
```

### 1.5 下拉菜单

```vue
<template>
  <DropdownMenuContent class="animate-in fade-in-0 zoom-in-95 duration-150
    data-[state=closed]:animate-out data-[state=closed]:fade-out-0 
    data-[state=closed]:zoom-out-95 data-[state=closed]:duration-100 origin-top-left">
  </DropdownMenuContent>
</template>
```

---

## 二、图标系统

### 2.1 标准尺寸

| 尺寸 | Tailwind | 使用场景 |
|------|----------|---------|
| 12px | `w-3 h-3` | 内联标签、角标 |
| 14px | `w-3.5 h-3.5` | 小按钮、表格操作 |
| 16px | `w-4 h-4` | **默认尺寸** |
| 20px | `w-5 h-5` | 导航项、卡片标题 |
| 24px | `w-6 h-6` | 页面标题 |

### 2.2 文字对齐

```vue
<template>
  <!-- 垂直居中 -->
  <span class="inline-flex items-center gap-1.5">
    <Settings class="w-4 h-4" /><span>设置</span>
  </span>
  <!-- 基线对齐 -->
  <a class="inline-flex items-baseline gap-1">
    <ExternalLink class="w-3.5 h-3.5 relative top-0.5" /><span>查看详情</span>
  </a>
</template>
```

### 2.3 颜色层级

```vue
<template>
  <!-- 继承父级 -->
  <Button class="text-neutral-600"><Edit class="w-4 h-4 text-inherit" />编辑</Button>
  <!-- 次要图标 -->
  <span class="text-neutral-700"><Calendar class="w-4 h-4 text-neutral-400" />2024-01-15</span>
  <!-- 品牌色 -->
  <Sparkles class="w-4 h-4 text-brand-500" />
  <!-- 语义色 -->
  <AlertCircle class="w-4 h-4 text-danger-500" />
</template>
```

### 2.4 图标按钮

```vue
<template>
  <button aria-label="更多操作"
    class="p-1.5 rounded-md text-neutral-400 transition-colors duration-100
      hover:bg-neutral-100 hover:text-neutral-600
      focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/50">
    <MoreHorizontal class="w-4 h-4" />
  </button>
</template>
```

---

## 三、数据展示规范

### 3.1 数字格式化

```vue
<script setup lang="ts">
const formatNumber = (n: number) => n.toLocaleString('zh-CN')

const formatCompact = (n: number): string => {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1).replace(/\.0$/, '') + 'M'
  if (n >= 1_000) return (n / 1_000).toFixed(1).replace(/\.0$/, '') + 'K'
  return n.toString()
}

const formatCurrency = (n: number, currency = 'CNY') => 
  n.toLocaleString('zh-CN', { style: 'currency', currency })

const formatPercent = (n: number, decimals = 1) => 
  `${n >= 0 ? '+' : ''}${n.toFixed(decimals)}%`
</script>

<template>
  <span class="font-mono tabular-nums">{{ formatNumber(1234567) }}</span><!-- 1,234,567 -->
  <span class="font-mono tabular-nums">{{ formatCompact(1234567) }}</span><!-- 1.2M -->
  <span class="font-mono tabular-nums">{{ formatCurrency(1234.56) }}</span><!-- ¥1,234.56 -->
</template>
```

### 3.2 日期时间

```vue
<script setup lang="ts">
import { formatDistanceToNow, format, isToday, isYesterday } from 'date-fns'
import { zhCN } from 'date-fns/locale'

const formatRelative = (date: Date) => 
  formatDistanceToNow(date, { addSuffix: true, locale: zhCN })

const formatSmart = (date: Date): string => {
  if (isToday(date)) return '今天 ' + format(date, 'HH:mm')
  if (isYesterday(date)) return '昨天 ' + format(date, 'HH:mm')
  if (Date.now() - date.getTime() < 7 * 24 * 60 * 60 * 1000) 
    return format(date, 'EEEE HH:mm', { locale: zhCN })
  return format(date, 'yyyy-MM-dd HH:mm')
}
</script>

<template>
  <time class="text-neutral-500 text-sm">{{ formatRelative(createdAt) }}</time>
  <time class="font-mono text-sm">{{ format(date, 'yyyy-MM-dd HH:mm') }}</time>
</template>
```

### 3.3 空值处理

```vue
<script setup lang="ts">
const EMPTY = '—'
const display = (v: unknown): string => {
  if (v === null || v === undefined || v === '') return EMPTY
  if (typeof v === 'number' && isNaN(v)) return EMPTY
  return String(v)
}
</script>

<template>
  <td class="text-neutral-400">{{ display(user.phone) }}</td>
  <td class="font-mono tabular-nums">{{ value ?? '—' }}</td>
</template>
```

### 3.4 文本截断

```vue
<template>
  <span class="truncate max-w-[200px]">{{ longText }}</span>
  <p class="line-clamp-2">{{ description }}</p>
  <td class="max-w-[300px] truncate" :title="fullText">{{ fullText }}</td>
</template>
```

## 四、禁止事项

- ❌ 禁止动画时长超过 200ms（C-INTERACT-007）
- ❌ 禁止使用 `transition-all`，指定具体属性（C-INTERACT-008）
- ❌ 禁止装饰性动画
- ❌ 禁止图标尺寸非标准（只用 12/14/16/20/24px）
- ❌ 禁止图标按钮无 `aria-label`（C-A11Y-002）
- ❌ 禁止数字使用非等宽字体，需 `tabular-nums`（C-TYPE-007）
- ❌ 禁止空值显示为空白或"无"（统一用 `—`）
- ❌ 禁止相对时间超过 7 天（应显示绝对日期）
- ❌ 禁止百分比不带正负号