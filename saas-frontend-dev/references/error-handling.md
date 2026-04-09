# 错误处理规范

> Vue 3 前端错误处理标准模式，涵盖 API 错误、表单验证、全局异常处理。

---

## 一、错误类型分类

| 类型 | 来源 | 处理方式 |
|------|------|---------|
| **网络错误** | 请求超时、断网 | Toast + 重试按钮 |
| **业务错误** | 后端返回错误码 | Toast / 表单错误提示 |
| **验证错误** | 前端 Zod 校验 | 字段级错误提示 |
| **权限错误** | 401/403 | 跳转登录/无权限页 |
| **未知错误** | 意外异常 | Toast + 日志上报 |

---

## 二、API 错误处理

### 2.1 TanStack Query 错误处理

```typescript
// composables/useUserList.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { useToast } from '@/components/ui/toast'

export function useUserList(filters: Ref<UserFilters>) {
  const { toast } = useToast()
  
  return useQuery({
    queryKey: ['users', filters],
    queryFn: () => userApi.getList(unref(filters)),
    // 错误在组件层处理，这里只做日志
    throwOnError: false,
  })
}

export function useCreateUser() {
  const { toast } = useToast()
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: userApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
      toast({ title: '创建成功' })
    },
    onError: (error: ApiError) => {
      // 业务错误
      if (error.code) {
        toast({ title: error.message, variant: 'destructive' })
      } else {
        // 网络/未知错误
        toast({ title: '网络错误，请重试', variant: 'destructive' })
      }
    },
  })
}
```

### 2.2 Axios 拦截器（全局处理）

```typescript
// utils/http.ts
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
})

// 响应拦截
http.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const { status, data } = error.response || {}
    
    // 401 未登录
    if (status === 401) {
      const auth = useAuthStore()
      auth.logout()
      window.location.href = '/login'
      return Promise.reject(error)
    }
    
    // 403 无权限
    if (status === 403) {
      window.location.href = '/403'
      return Promise.reject(error)
    }
    
    // 其他错误，交给调用方处理
    return Promise.reject(data || error)
  }
)

export default http
```

---

## 三、表单验证错误

### 3.1 Zod + 表单错误显示

```vue
<script setup lang="ts">
import { z } from 'zod'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'

const schema = z.object({
  name: z.string().min(1, '名称不能为空').max(64, '名称不超过64字符'),
  email: z.string().email('邮箱格式不正确'),
  phone: z.string().regex(/^1[3-9]\d{9}$/, '手机号格式不正确'),
})

const { handleSubmit, errors, setFieldError } = useForm({
  validationSchema: toTypedSchema(schema),
})

const onSubmit = handleSubmit(async (values) => {
  try {
    await userApi.create(values)
    // 成功处理
  } catch (error: any) {
    // 后端返回字段级错误
    if (error.fieldErrors) {
      error.fieldErrors.forEach((e: FieldError) => {
        setFieldError(e.field, e.message)
      })
    }
  }
})
</script>

<template>
  <form @submit="onSubmit">
    <FormField name="name">
      <FormItem>
        <FormLabel>名称</FormLabel>
        <FormControl>
          <Input />
        </FormControl>
        <FormMessage /><!-- 自动显示 errors.name -->
      </FormItem>
    </FormField>
  </form>
</template>
```

### 3.2 后端错误映射到表单

```typescript
// utils/form-error.ts
export function mapApiErrorsToForm(
  apiErrors: FieldError[],
  setFieldError: (field: string, message: string) => void
) {
  apiErrors.forEach(({ field, message }) => {
    // 驼峰转换
    const formField = field.replace(/_(\w)/g, (_, c) => c.toUpperCase())
    setFieldError(formField, message)
  })
}
```

---

## 四、全局错误边界

### 4.1 Vue 错误捕获

```typescript
// main.ts
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err, info)
  // 上报错误
  reportError(err, { component: instance?.$options.name, info })
}

// 捕获 Promise 未处理错误
window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled rejection:', event.reason)
  reportError(event.reason)
  event.preventDefault()
})
```

### 4.2 错误边界组件

```vue
<!-- components/ErrorBoundary.vue -->
<script setup lang="ts">
import { onErrorCaptured, ref } from 'vue'

const error = ref<Error | null>(null)

onErrorCaptured((err) => {
  error.value = err
  reportError(err)
  return false // 阻止错误继续传播
})

function retry() {
  error.value = null
}
</script>

<template>
  <slot v-if="!error" />
  <div v-else class="flex flex-col items-center py-8">
    <AlertCircle class="h-10 w-10 text-destructive" />
    <p class="mt-2 text-sm text-muted-foreground">页面出错了</p>
    <Button variant="outline" class="mt-4" @click="retry">重试</Button>
  </div>
</template>
```

---

## 五、错误提示 UI 规范

### 5.1 Toast 使用场景

| 场景 | Toast 类型 | 持续时间 |
|------|-----------|---------|
| 操作成功 | default | 3s |
| 操作失败 | destructive | 5s |
| 网络错误 | destructive | 手动关闭 |
| 警告提示 | warning | 5s |

### 5.2 Toast 示例

```typescript
const { toast } = useToast()

// 成功
toast({ title: '保存成功', description: '用户信息已更新' })

// 错误
toast({ 
  title: '操作失败', 
  description: error.message, 
  variant: 'destructive' 
})

// 网络错误（不自动关闭）
toast({ 
  title: '网络连接失败', 
  description: '请检查网络后重试',
  variant: 'destructive',
  duration: Infinity,
  action: h(Button, { onClick: retry }, '重试')
})
```

---

## 六、错误上报

### 6.1 上报内容

```typescript
interface ErrorReport {
  message: string
  stack?: string
  url: string
  line?: number
  column?: number
  userAgent: string
  userId?: string
  tenantId?: string
  timestamp: number
  extra?: Record<string, any>
}
```

### 6.2 上报函数

```typescript
// utils/report-error.ts
export function reportError(error: Error | unknown, extra?: Record<string, any>) {
  const report: ErrorReport = {
    message: error instanceof Error ? error.message : String(error),
    stack: error instanceof Error ? error.stack : undefined,
    url: window.location.href,
    userAgent: navigator.userAgent,
    userId: useAuthStore().userId,
    tenantId: useTenantStore().tenantId,
    timestamp: Date.now(),
    extra,
  }
  
  // 发送到错误监控服务
  if (import.meta.env.PROD) {
    navigator.sendBeacon('/api/errors', JSON.stringify(report))
  } else {
    console.error('[Error Report]', report)
  }
}
```

---

## 七、错误处理约束

| ID | 规则 |
|----|------|
| C-ERR-001 | 所有 API 调用必须有错误处理（try-catch 或 onError） |
| C-ERR-002 | 禁止静默吞掉错误（空 catch 块） |
| C-ERR-003 | 表单提交失败时保留用户输入 |
| C-ERR-004 | 网络错误提供重试入口 |
| C-ERR-005 | 生产环境必须上报错误 |