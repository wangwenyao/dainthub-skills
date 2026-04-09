# 路由配置规范 — Vue SaaS Frontend

## 一、路由配置接口（RouteConfig）

```typescript
import type { Component } from 'vue'
import type { RouteRecordRaw } from 'vue-router'

interface AppRouteConfig extends Omit<RouteRecordRaw, 'children' | 'meta'> {
  path: string
  name?: string
  component?: Component
  redirect?: string | Location
  meta?: RouteMeta
  children?: AppRouteConfig[]
}
```

---

## 二、路由元信息（RouteMeta）

```typescript
interface RouteMeta {
  title: string                      // 页面标题（必填）
  icon?: Component                   // 菜单图标
  breadcrumb?: BreadcrumbItem[]     // 自定义面包屑
  hideBreadcrumb?: boolean           // 隐藏面包屑
  permissions?: string[]             // 权限标识数组
  roles?: string[]                   // 角色限制
  requiresAuth?: boolean             // 需要登录（默认 true）
  hidden?: boolean                   // 菜单隐藏
  hiddenChildren?: boolean           // 隐藏子菜单
  activeMenu?: string                 // 高亮菜单路径
  cache?: boolean                     // Keep-alive 缓存
  affix?: boolean                     // 固定在 Tab 栏
  link?: string                       // 外链地址
}

interface BreadcrumbItem {
  title: string
  path?: string
  icon?: Component
}
```

---

## 三、权限控制

```typescript
// router/guards/permissionGuard.ts
export function setupPermissionGuard(router: Router) {
  router.beforeEach(async (to) => {
    const userStore = useUserStore()
    const permissionStore = usePermissionStore()
    const meta = to.meta as RouteMeta

    if (meta.requiresAuth === false) return true

    if (!userStore.isAuthenticated) {
      return { path: '/auth/login', query: { redirect: to.fullPath } }
    }

    if (meta.roles && !meta.roles.some(r => userStore.roles.includes(r))) {
      return { path: '/403', replace: true }
    }

    if (meta.permissions && !meta.permissions.some(p => permissionStore.hasPermission(p))) {
      return { path: '/403', replace: true }
    }

    return true
  })
}
```

---

## 四、面包屑生成

```typescript
// composables/useBreadcrumb.ts
export function useBreadcrumb() {
  const route = useRoute()

  const breadcrumbs = computed(() => {
    if (route.meta.breadcrumb) return route.meta.breadcrumb

    return route.matched
      .filter(r => r.meta?.title && !r.meta.hidden)
      .map((r, index, arr) => ({
        title: r.meta!.title,
        path: index === arr.length - 1 ? undefined : r.path,
      }))
  })

  return { breadcrumbs }
}
```

**动态面包屑示例：**
```typescript
// 组件中动态设置
const route = useRoute()
route.meta.breadcrumb = [
  { title: '用户管理', path: '/users' },
  { title: `用户 ${route.params.id}` },
]
```

---

## 五、页面缓存策略

```vue
<!-- layouts/DashboardLayout.vue -->
<router-view v-slot="{ Component, route }">
  <keep-alive :include="cachedViews">
    <component :is="Component" :key="route.fullPath" />
  </keep-alive>
</router-view>
```

```typescript
// stores/useCacheStore.ts
export const useCacheStore = defineStore('cache', {
  state: () => ({ cachedViews: [] as string[] }),
  actions: {
    addCache(name: string) {
      if (!this.cachedViews.includes(name)) this.cachedViews.push(name)
    },
    removeCache(name: string) {
      this.cachedViews = this.cachedViews.filter(v => v !== name)
    },
    clearCache() { this.cachedViews = [] },
  },
})
```

**缓存启用条件：**
```typescript
// 路由配置
{ path: 'users', meta: { title: '用户列表', cache: true } }

// 组件必须定义 name
defineOptions({ name: 'UserListPage' })
```

---

## 六、Tab 栏支持

```typescript
// stores/useTabStore.ts
interface TabItem { path: string; title: string; affix?: boolean }

export const useTabStore = defineStore('tab', {
  state: () => ({
    visitedTabs: [] as TabItem[],
    affixTabs: [] as TabItem[],
  }),
  actions: {
    addTab(route: RouteLocationNormalized) {
      if (route.meta.hidden) return
      // 添加到 visitedTabs...
    },
    closeTab(path: string) {
      this.visitedTabs = this.visitedTabs.filter(t => t.path !== path)
    },
    closeOtherTabs(path: string) {
      this.visitedTabs = this.visitedTabs.filter(t => t.path === path || t.affix)
    },
  },
})
```

**Affix 固定 Tab：**
```typescript
{ path: 'dashboard', meta: { title: '仪表盘', affix: true } }
```

---

## 七、完整配置示例

```typescript
// router/routes/modules/dashboard.ts
export default {
  path: '/dashboard',
  component: () => import('@/layouts/DashboardLayout.vue'),
  meta: { requiresAuth: true },
  children: [
    { path: '', redirect: '/dashboard/overview' },
    {
      path: 'overview',
      name: 'DashboardOverview',
      component: () => import('@/pages/dashboard/OverviewPage.vue'),
      meta: { title: '概览', icon: DashboardIcon, affix: true, cache: true },
    },
    {
      path: 'analytics',
      name: 'Analytics',
      component: () => import('@/pages/dashboard/AnalyticsPage.vue'),
      meta: {
        title: '数据分析',
        icon: ChartIcon,
        permissions: ['dashboard:analytics:view'],
        breadcrumb: [
          { title: '仪表盘', path: '/dashboard' },
          { title: '数据分析' },
        ],
      },
    },
  ],
}

// 外链路由
{ path: '/docs', meta: { title: '帮助文档', icon: BookIcon, link: 'https://docs.example.com' } }

// 隐藏子菜单
{
  path: 'settings',
  meta: { title: '设置', icon: SettingsIcon, hiddenChildren: true },
  children: [
    { path: 'profile', meta: { title: '个人资料' } },
    { path: 'security', meta: { title: '安全设置' } },
  ],
}
```

---

## 禁止事项

1. **禁止**在路由组件中使用匿名函数定义 `name`，必须使用 `defineOptions({ name: 'xxx' })`
2. **禁止**在 `meta` 中存储大对象或函数，仅限原始类型
3. **禁止**动态修改路由配置，应通过权限控制显示
4. **禁止**在 `beforeEach` 中执行异步操作不加 loading 状态
5. **禁止**缓存页面超过 10 个，影响内存性能
6. **禁止**使用 `path` 作为缓存 key，必须使用组件 `name`