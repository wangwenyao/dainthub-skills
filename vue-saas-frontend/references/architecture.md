# Architecture Reference — Vue SaaS Frontend

## 目录

1. [Vite 6 配置](#vite-6-配置)
2. [路由架构](#路由架构)
3. [服务层封装](#服务层封装)
4. [错误处理策略](#错误处理策略)
5. [环境变量规范](#环境变量规范)

---

## Vite 6 配置

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'query-vendor': ['@tanstack/vue-query'],
          'ui-vendor': ['radix-vue'],
        },
      },
    },
    target: 'esnext',
    minify: 'esbuild',
  },
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL,
        changeOrigin: true,
      },
    },
  },
})
```

---

## 路由架构

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/DashboardLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: '/dashboard' },
        {
          path: 'dashboard',
          component: () => import('@/pages/DashboardPage.vue'),
          meta: { title: '仪表盘' },
        },
        {
          path: 'users',
          children: [
            { path: '', component: () => import('@/pages/users/UserListPage.vue') },
            { path: ':id', component: () => import('@/pages/users/UserDetailPage.vue') },
          ],
        },
      ],
    },
    {
      path: '/auth',
      component: () => import('@/layouts/AuthLayout.vue'),
      children: [
        { path: 'login', component: () => import('@/pages/auth/LoginPage.vue') },
        { path: 'register', component: () => import('@/pages/auth/RegisterPage.vue') },
      ],
    },
  ],
})

// 路由守卫
router.beforeEach((to) => {
  const store = useUserStore()
  if (to.meta.requiresAuth && !store.isAuthenticated) {
    return { path: '/auth/login', query: { redirect: to.fullPath } }
  }
})

export default router
```

---

## 服务层封装

```typescript
// services/http.ts — 基础 HTTP 客户端
import axios from 'axios'
import { useUserStore } from '@/stores/useUserStore'
import router from '@/router'

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 15_000,
  headers: { 'Content-Type': 'application/json' },
})

http.interceptors.request.use((config) => {
  // token 从 httpOnly cookie 由服务端注入，无需手动附加
  return config
})

http.interceptors.response.use(
  (res) => res.data,
  (error) => {
    if (error.response?.status === 401) {
      useUserStore().logout()
      router.push('/auth/login')
    }
    return Promise.reject(error)
  }
)

// services/userService.ts — 业务服务
import { http } from './http'
import { UserSchema, UserListSchema } from '@/types/models'

export const userService = {
  getMe: () => http.get('/users/me').then(UserSchema.parse),
  getList: (params: UserFilters) => http.get('/users', { params }).then(UserListSchema.parse),
  getById: (id: string) => http.get(`/users/${id}`).then(UserSchema.parse),
  create: (data: CreateUserInput) => http.post('/users', data).then(UserSchema.parse),
  update: (id: string, data: UpdateUserInput) => http.patch(`/users/${id}`, data).then(UserSchema.parse),
  delete: (id: string) => http.delete(`/users/${id}`),
}
```

---

## 错误处理策略

```typescript
// composables/useErrorHandler.ts
import { useToast } from '@/components/ui/toast'

export function useErrorHandler() {
  const { toast } = useToast()

  function handleError(error: unknown, fallbackMessage = '操作失败，请重试') {
    if (error instanceof ZodError) {
      toast({ title: '数据格式错误', description: error.errors[0].message, variant: 'destructive' })
      return
    }
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.message ?? fallbackMessage
      toast({ title: '请求失败', description: message, variant: 'destructive' })
      return
    }
    toast({ title: '未知错误', description: fallbackMessage, variant: 'destructive' })
  }

  return { handleError }
}
```

**TanStack Query 全局错误处理：**

```typescript
// main.ts
import { VueQueryPlugin, QueryClient } from '@tanstack/vue-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error) => {
        if (axios.isAxiosError(error) && error.response?.status === 404) return false
        return failureCount < 2
      },
      staleTime: 2 * 60 * 1000,
    },
    mutations: {
      onError: (error) => {
        // 全局 mutation 错误兜底
      },
    },
  },
})
```

---

## 环境变量规范

```bash
# .env.development
VITE_API_BASE_URL=http://localhost:3000/api/v1
VITE_APP_TITLE=MyApp (Dev)

# .env.production
VITE_API_BASE_URL=https://api.myapp.com/v1
VITE_APP_TITLE=MyApp

# .env.d.ts — 类型声明
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_APP_TITLE: string
}
```
