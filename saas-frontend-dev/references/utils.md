# 工具函数参考

> 统一的数据格式化与通用工具函数。

## 一、数据格式化

### 1. 数字格式化

```typescript
interface NumberFormatOptions {
  decimals?: number
  locale?: string
}

export function formatNumber(value: number, options?: NumberFormatOptions): string {
  const { decimals, locale = 'zh-CN' } = options ?? {}
  if (isNaN(value)) return '—'
  return value.toLocaleString(locale, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })
}
// formatNumber(1234567) → "1,234,567"

export function formatLargeNumber(value: number, options?: { decimals?: number }): string {
  const { decimals = 1 } = options ?? {}
  if (isNaN(value)) return '—'
  const abs = Math.abs(value), sign = value < 0 ? '-' : ''
  if (abs >= 1_000_000_000) return sign + (abs / 1_000_000_000).toFixed(decimals).replace(/\.0$/, '') + 'B'
  if (abs >= 1_000_000) return sign + (abs / 1_000_000).toFixed(decimals).replace(/\.0$/, '') + 'M'
  if (abs >= 1_000) return sign + (abs / 1_000).toFixed(decimals).replace(/\.0$/, '') + 'K'
  return sign + abs.toString()
}
// formatLargeNumber(1234567) → "1.2M"
```

### 2. 货币格式化

```typescript
export function formatCurrency(
  value: number,
  currency: string = 'CNY',
  locale: string = 'zh-CN'
): string {
  if (isNaN(value) || value === null) return '—'
  return value.toLocaleString(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}
// formatCurrency(1234.56, 'CNY') → "¥1,234.56"
```

### 3. 百分比格式化

```typescript
export function formatPercent(
  value: number,
  options?: { decimals?: number; showSign?: boolean }
): string {
  const { decimals = 1, showSign = false } = options ?? {}
  if (isNaN(value)) return '—'
  const sign = showSign && value > 0 ? '+' : ''
  return sign + value.toFixed(decimals) + '%'
}
// formatPercent(85.6) → "85.6%"
```

### 4. 日期格式化

```typescript
type DateFormat = 'short' | 'long' | 'relative' | 'datetime'

export function formatDate(
  date: Date | string | number,
  format: DateFormat = 'short',
  locale: string = 'zh-CN'
): string {
  const d = typeof date === 'string' || typeof date === 'number' ? new Date(date) : date
  if (isNaN(d.getTime())) return '—'

  if (format === 'short') return d.toLocaleDateString(locale)
  if (format === 'long') return d.toLocaleString(locale, {
    year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'
  })
  if (format === 'datetime') return d.toLocaleString(locale, {
    year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'
  })
  if (format === 'relative') return formatRelativeTime(d, locale)
  return d.toLocaleDateString(locale)
}

function formatRelativeTime(date: Date, locale: string): string {
  const diff = Date.now() - date.getTime()
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' })
  
  if (seconds < 60) return rtf.format(-seconds, 'second')
  if (minutes < 60) return rtf.format(-minutes, 'minute')
  if (hours < 24) return rtf.format(-hours, 'hour')
  if (days < 7) return rtf.format(-days, 'day')
  return date.toLocaleDateString(locale)
}
// formatDate(Date.now() - 3600000, 'relative') → "1小时前"
```

### 5. 空值处理与截断

```typescript
export function formatEmpty(value: unknown, fallback: string = '—'): string {
  if (value === null || value === undefined || value === '') return fallback
  if (typeof value === 'number' && isNaN(value)) return fallback
  return String(value)
}
// formatEmpty(null) → "—"; formatEmpty(0) → "0"

export function truncate(
  text: string,
  options?: { length?: number; suffix?: string }
): string {
  const { length = 50, suffix = '...' } = options ?? {}
  if (!text) return '—'
  if (text.length <= length) return text
  return text.slice(0, length - suffix.length) + suffix
}
// truncate('这是一段很长的文本', { length: 8 }) → "这是一段..."
```

## 二、类型定义

```typescript
export type Formatter<T> = (value: T) => string
export type DateFormat = 'short' | 'long' | 'relative' | 'datetime'

export interface NumberFormatOptions {
  decimals?: number
  locale?: string
}
```

## 三、Vue Composables

```typescript
// composables/useFormatting.ts
import { computed, type Ref } from 'vue'

export function useNumberFormat(value: Ref<number>, options?: NumberFormatOptions) {
  return computed(() => formatNumber(value.value, options))
}

export function useCurrencyFormat(value: Ref<number>, currency?: string) {
  return computed(() => formatCurrency(value.value, currency))
}

export function useDateFormat(date: Ref<Date | string>, format?: DateFormat) {
  return computed(() => formatDate(date.value, format))
}
```

## 四、使用示例

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { useNumberFormat, useDateFormat } from '@/composables/useFormatting'

const amount = ref(1234567)
const createdAt = ref(new Date())
const formattedAmount = useNumberFormat(amount)
const formattedDate = useDateFormat(createdAt, 'long')
</script>

<template>
  <span class="font-mono tabular-nums">{{ formattedAmount }}</span>
  <time>{{ formattedDate }}</time>
</template>
```

## 五、与设计系统协作

数据展示样式参考 `saas-ui-design/references/advanced-details.md`：
- 数字使用等宽字体 `font-mono tabular-nums`
- 货币右对齐，负数红色
- 日期时间使用 `<time>` 标签

## 六、禁止事项

- ❌ 禁止使用 moment.js、date-fns（使用原生 Intl API）
- ❌ 禁止数字显示无千分位分隔符
- ❌ 禁止数字使用非等宽字体
- ❌ 禁止空值显示为空白、"无"、"null"、"undefined"（统一用 `—`）
- ❌ 禁止 `0` 被视为空值
- ❌ 禁止相对时间超过 7 天（应显示绝对日期）
- ❌ 禁止百分比变化率不带正负号
- ❌ 禁止货币格式不带货币符号