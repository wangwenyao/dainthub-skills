# 配置中心规范

## 一、配置层级与优先级

```
优先级从高到低：
1. 远程配置（API 动态下发）
2. 运行时注入（window.__CONFIG__）
3. 环境变量（import.meta.env）
4. 默认配置（代码内置）
```

配置合并策略：后加载配置覆盖先加载配置，深层合并对象属性。

---

## 二、应用配置

```typescript
interface AppConfig {
  app: { name: string; version: string; apiBaseURL: string; buildTime: string }
  features: { darkMode: boolean; i18n: boolean; analytics: boolean; maintenance: boolean }
  ui: { theme: 'light' | 'dark' | 'system'; language: string; pageSize: number; dateFormat: string }
  services: { sentry?: { dsn: string; environment: string }; analytics?: { trackingId: string } }
}

// 默认配置
const defaultConfig: AppConfig = {
  app: { name: 'SaaS App', version: '1.0.0', apiBaseURL: '/api', buildTime: '' },
  features: { darkMode: false, i18n: true, analytics: false, maintenance: false },
  ui: { theme: 'system', language: 'zh-CN', pageSize: 20, dateFormat: 'YYYY-MM-DD' },
  services: {},
}
```

---

## 三、API 配置

### 配置定义

```typescript
// src/config/api.config.ts
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 15_000,
  retry: { count: 2, delay: 1_000 },
  cache: { enabled: true, ttl: 5 * 60 * 1000 },
  requestId: { header: 'X-Request-ID', generator: () => crypto.randomUUID() },
} as const
```

### Axios 实例

```typescript
// src/lib/http.ts
import axios from 'axios'
import { API_CONFIG } from '@/config/api.config'

export const http = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
})

// 请求拦截器
http.interceptors.request.use((config) => {
  config.headers[API_CONFIG.requestId.header] = API_CONFIG.requestId.generator()
  if (config.method === 'get') config.params = { ...config.params, _t: Date.now() }
  if (import.meta.env.DEV) console.log(`[HTTP] → ${config.method?.toUpperCase()} ${config.url}`)
  return config
})

// 响应拦截器
http.interceptors.response.use(
  (response) => response.data,
  (error) => { handleHttpError(error); return Promise.reject(error) }
)
```

### 错误处理

```typescript
// src/lib/errorHandler.ts
const ERROR_MESSAGES: Record<number, string> = {
  400: '请求参数错误', 401: '登录已过期', 403: '没有权限',
  404: '资源不存在', 422: '数据验证失败', 429: '请求过于频繁',
  500: '服务器错误', 502: '网关错误', 503: '服务不可用',
}

export function handleHttpError(error: AxiosError): void {
  const status = error.response?.status
  // 根据 status 执行对应处理（跳转登录、提示等）
}
```

### API 端点定义

```typescript
// src/config/endpoints.ts
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login', LOGOUT: '/auth/logout', REFRESH: '/auth/refresh',
    ME: '/auth/me', FORGOT_PASSWORD: '/auth/forgot-password',
  },
  USER: {
    LIST: '/users', DETAIL: (id: string) => `/users/${id}`,
    CREATE: '/users', UPDATE: (id: string) => `/users/${id}`,
    DELETE: (id: string) => `/users/${id}`,
  },
  ROLE: { LIST: '/roles', DETAIL: (id: string) => `/roles/${id}` },
  FILE: { UPLOAD: '/files/upload', PRESIGN: '/files/presign' },
} as const
```

---

## 四、业务配置

### 枚举配置

```typescript
// src/config/enums.ts
import { Clock, Check, Truck, X } from 'lucide-vue-next'

export const USER_STATUS = {
  ACTIVE: { value: 1, label: '正常', color: 'success' },
  INACTIVE: { value: 0, label: '禁用', color: 'destructive' },
} as const

export const ORDER_STATUS = {
  PENDING: { value: 'pending', label: '待支付', color: 'warning', icon: Clock },
  PAID: { value: 'paid', label: '已支付', color: 'info' },
  SHIPPED: { value: 'shipped', label: '已发货', color: 'primary', icon: Truck },
  COMPLETED: { value: 'completed', label: '已完成', color: 'success', icon: Check },
  CANCELLED: { value: 'cancelled', label: '已取消', color: 'destructive', icon: X },
} as const

export type UserStatus = typeof USER_STATUS[keyof typeof USER_STATUS]['value']
export type OrderStatus = typeof ORDER_STATUS[keyof typeof ORDER_STATUS]['value']
```

### 枚举工具函数

```typescript
// src/config/enum-utils.ts
interface EnumItem { value: string | number; label: string; color?: string; icon?: Component }

export function getEnumOptions(enumObj: Record<string, EnumItem>) {
  return Object.values(enumObj).map(item => ({ label: item.label, value: item.value }))
}

export function getEnumLabel(enumObj: Record<string, EnumItem>, value: string | number) {
  return Object.values(enumObj).find(item => item.value === value)?.label ?? '-'
}

export function getEnumColor(enumObj: Record<string, EnumItem>, value: string | number) {
  return Object.values(enumObj).find(item => item.value === value)?.color ?? 'default'
}
```

### 字典配置（远程加载）

```typescript
// src/config/dictionaries.ts
export interface DictItem { value: string | number; label: string; color?: string; disabled?: boolean }

const dictCache = new Map<string, DictItem[]>()

export function useDictionary(dictType: string) {
  const loading = ref(false)
  const options = ref<DictItem[]>([])

  const load = async () => {
    if (dictCache.has(dictType)) { options.value = dictCache.get(dictType)!; return }
    loading.value = true
    try {
      const data = await fetch(`/api/dict/${dictType}`).then(r => r.json())
      dictCache.set(dictType, data)
      options.value = data
    } finally { loading.value = false }
  }

  const getLabel = (value: string | number) => options.value.find(i => i.value === value)?.label ?? '-'
  return { loading, options, load, getLabel }
}
```

### 常量配置

```typescript
// src/config/constants.ts
export const APP_CONFIG = {
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
  DEFAULT_PAGE_SIZE: 20,
  DATE_FORMAT: 'YYYY-MM-DD',
  DATETIME_FORMAT: 'YYYY-MM-DD HH:mm:ss',
  MAX_UPLOAD_SIZE: 10 * 1024 * 1024,
} as const

export const VALIDATION_RULES = {
  PASSWORD_MIN_LENGTH: 8,
  PHONE_REGEX: /^1[3-9]\d{9}$/,
  EMAIL_REGEX: /^[\w.-]+@[\w.-]+\.\w+$/,
} as const
```

---

## 五、运行时注入

### 环境变量

```typescript
// vite.config.ts
export default defineConfig({
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
  }
})

// .env.production
VITE_API_BASE_URL=https://api.example.com
VITE_FEATURE_DARK_MODE=true
```

### window.__CONFIG__ 注入

```html
<!-- index.html -->
<script>window.__CONFIG__ = { apiBaseURL: '<%= API_BASE_URL %>', ui: { theme: 'dark' } }</script>
```

```typescript
// config/runtime.ts
declare global { interface Window { __CONFIG__?: Partial<AppConfig> } }
export function loadRuntimeConfig(): Partial<AppConfig> {
  return window.__CONFIG__ || {}
}
```

### 远程配置加载

```typescript
// composables/useRemoteConfig.ts
export function useRemoteConfig() {
  const config = ref<Partial<AppConfig>>({})
  const loading = ref(false)

  async function fetchConfig() {
    loading.value = true
    try { config.value = await fetch('/api/config').then(r => r.json()) }
    finally { loading.value = false }
  }

  const { pause, resume } = useIntervalFn(fetchConfig, 60000) // 每分钟刷新
  onMounted(fetchConfig)
  onUnmounted(pause)

  return { config, loading, fetchConfig, pause, resume }
}
```

---

## 六、配置访问

### useConfig 组合式函数

```typescript
// composables/useConfig.ts
export function useConfig() {
  const runtimeConfig = loadRuntimeConfig()
  const { config: remoteConfig } = useRemoteConfig()

  const mergedConfig = computed(() => deepMerge(defaultConfig, envConfig, runtimeConfig, remoteConfig.value))

  function get<K extends keyof AppConfig>(key: K): AppConfig[K] {
    return mergedConfig.value[key]
  }

  return { config: readonly(mergedConfig), get }
}

function deepMerge<T extends Record<string, unknown>>(...sources: Partial<T>[]): T {
  return sources.reduce((acc, src) => {
    Object.keys(src).forEach(key => {
      const accVal = acc[key], srcVal = src[key]
      if (isObject(accVal) && isObject(srcVal)) acc[key] = deepMerge(accVal, srcVal)
      else if (srcVal !== undefined) acc[key] = srcVal
    })
    return acc
  }, {} as T) as T
}
```

### useEnum 组合式函数

```typescript
// composables/useEnum.ts
export function useEnum<T extends Record<string, any>>(enumObj: T) {
  const options = computed(() => getEnumOptions(enumObj))
  const getLabel = (value: string | number) => getEnumLabel(enumObj, value)
  const getColor = (value: string | number) => getEnumColor(enumObj, value)
  const createBadgeProps = (value: string | number) => ({ variant: getColor(value), label: getLabel(value) })
  return { options, getLabel, getColor, createBadgeProps }
}
```

### 使用示例

```vue
<script setup lang="ts">
import { useConfig } from '@/composables/useConfig'
import { useEnum, USER_STATUS } from '@/config'
import { useDictionary } from '@/config/dictionaries'

const { get } = useConfig()
const { createBadgeProps } = useEnum(USER_STATUS)
const { options, loading, load } = useDictionary('region')

onMounted(load)
</script>

<template>
  <Badge v-bind="createBadgeProps(row.status)" />
  <Select v-model="form.region" :options="options" :loading="loading" />
</template>
```

---

## 七、禁止事项

| 禁止项 | 原因 | 替代方案 |
|--------|------|----------|
| ❌ 硬编码 API URL | 环境差异 | `VITE_API_BASE_URL` 环境变量 |
| ❌ 直接使用 axios | 缺少统一处理 | 封装的 `http` 实例 |
| ❌ 跳过 Zod 验证 | 类型不安全 | 所有响应经过 schema 验证 |
| ❌ 在组件中直接调用 http | 耦合度高 | 通过 service 层调用 |
| ❌ 硬编码状态值 | 维护困难 | 使用枚举配置 |
| ❌ 在组件中定义枚举 | 分散难管理 | 统一放在 `enums.ts` |
| ❌ 重复请求字典数据 | 性能浪费 | 使用缓存机制 |
| ❌ 使用魔法字符串 | 可读性差 | 使用常量配置 |
| ❌ 前端存储 API Secret | 安全风险 | 服务端代理请求 |
| ❌ 配置文件提交 Git | 泄露风险 | `.gitignore` + 环境变量 |
| ❌ 明文传输敏感配置 | 中间人攻击 | HTTPS + 加密 |