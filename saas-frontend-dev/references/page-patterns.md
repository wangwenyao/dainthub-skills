# Page Patterns Reference — Vue SaaS Frontend

## 目录

1. [用户列表页（完整示例）](#用户列表页)
2. [认证登录页](#认证登录页)
3. [设置页面](#设置页面)
4. [仪表盘页](#仪表盘页)

---

## 用户列表页

完整示例，包含搜索、筛选、分页、批量删除：

```vue
<!-- pages/users/UserListPage.vue -->
<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserList, useDeleteUser } from '@/composables/useUsers'
import { useUserStore } from '@/stores/useUserStore'
import DataTable from '@/components/DataTable.vue'
import ConfirmDeleteDialog from '@/components/ConfirmDeleteDialog.vue'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Plus, Search, Trash2 } from 'lucide-vue-next'
import { useToast } from '@/components/ui/toast'
import { useDebounceFn } from '@vueuse/core'

const router = useRouter()
const route = useRoute()
const { toast } = useToast()
const userStore = useUserStore()

// URL 同步的筛选状态
const filters = ref({
  search: String(route.query.search ?? ''),
  role: String(route.query.role ?? ''),
  page: Number(route.query.page ?? 1),
  pageSize: 20,
})

// 同步到 URL
watch(filters, (val) => {
  router.replace({ query: { ...val, page: val.page > 1 ? val.page : undefined } })
}, { deep: true })

// 服务端状态
const { data, isLoading, isError, error, refetch } = useUserList(filters)

// 删除逻辑
const deleteTarget = ref<string[]>([])
const showDeleteDialog = ref(false)
const { mutate: deleteUser, isPending: isDeleting } = useDeleteUser()

function confirmDelete(ids: string[]) {
  deleteTarget.value = ids
  showDeleteDialog.value = true
}

function handleDelete() {
  deleteUser(deleteTarget.value, {
    onSuccess: () => {
      toast({ title: '删除成功', description: `已删除 ${deleteTarget.value.length} 个用户` })
      showDeleteDialog.value = false
      selectedIds.value = []
    },
    onError: (err) => {
      toast({ title: '删除失败', description: err.message, variant: 'destructive' })
    },
  })
}

// 批量选中
const selectedIds = ref<string[]>([])

// 列定义
const columns = [
  { key: 'name', label: '姓名' },
  { key: 'email', label: '邮箱' },
  { key: 'role', label: '角色' },
  { key: 'createdAt', label: '创建时间', render: (row) => formatDate(row.createdAt) },
]

// 防抖搜索
const handleSearch = useDebounceFn((val: string) => {
  filters.value.search = val
  filters.value.page = 1
}, 300)
</script>

<template>
  <div class="space-y-6">
    <!-- 页头 -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-semibold tracking-tight">用户管理</h1>
        <p class="text-sm text-muted-foreground">
          共 {{ data?.total ?? 0 }} 个用户
        </p>
      </div>
      <Button @click="router.push('/users/new')">
        <Plus class="mr-2 h-4 w-4" />
        新增用户
      </Button>
    </div>

    <!-- 筛选区 -->
    <div class="flex gap-3">
      <div class="relative flex-1 max-w-sm">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          class="pl-9"
          placeholder="搜索姓名或邮箱..."
          :model-value="filters.search"
          @update:model-value="handleSearch"
        />
      </div>
      <!-- 批量操作（仅选中时显示） -->
      <Button
        v-if="selectedIds.length > 0"
        variant="destructive"
        @click="confirmDelete(selectedIds)"
      >
        <Trash2 class="mr-2 h-4 w-4" />
        删除选中 ({{ selectedIds.length }})
      </Button>
    </div>

    <!-- 表格 -->
    <DataTable
      :data="data?.items ?? []"
      :columns="columns"
      :is-loading="isLoading"
      :total-count="data?.total"
      :current-page="filters.page"
      :page-size="filters.pageSize"
      selectable
      @page-change="filters.page = $event"
      @select="selectedIds = $event"
    >
      <template #default="{ row }">
        <TableCell>{{ row.name }}</TableCell>
        <TableCell class="text-muted-foreground">{{ row.email }}</TableCell>
        <TableCell>
          <Badge :variant="row.role === 'admin' ? 'default' : 'secondary'">
            {{ row.role === 'admin' ? '管理员' : '成员' }}
          </Badge>
        </TableCell>
        <TableCell class="text-muted-foreground text-sm">
          {{ formatDate(row.createdAt) }}
        </TableCell>
        <TableCell>
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <Button variant="ghost" size="icon">
                <MoreHorizontal class="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem @click="router.push(`/users/${row.id}`)">
                查看详情
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem class="text-destructive" @click="confirmDelete([row.id])">
                删除
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </TableCell>
      </template>
    </DataTable>
  </div>

  <!-- 确认删除 -->
  <ConfirmDeleteDialog
    v-model:open="showDeleteDialog"
    :description="`将删除 ${deleteTarget.length} 个用户，此操作不可撤销。`"
    :is-deleting="isDeleting"
    @confirm="handleDelete"
  />
</template>
```

---

## 认证登录页

```vue
<!-- pages/auth/LoginPage.vue -->
<script setup lang="ts">
import { z } from 'zod'
import { useForm } from '@formkit/vue'
import { useUserStore } from '@/stores/useUserStore'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const loginSchema = z.object({
  email: z.string().email('请输入有效的邮箱地址'),
  password: z.string().min(8, '密码至少 8 位'),
})

const isLoading = ref(false)
const serverError = ref('')

async function handleLogin(values: z.infer<typeof loginSchema>) {
  isLoading.value = true
  serverError.value = ''
  try {
    await userStore.login(values)
    const redirect = String(route.query.redirect ?? '/dashboard')
    router.push(redirect)
  } catch (err) {
    serverError.value = err instanceof Error ? err.message : '登录失败，请重试'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-muted/30 p-4">
    <Card class="w-full max-w-md">
      <CardHeader class="text-center">
        <CardTitle class="text-2xl">欢迎回来</CardTitle>
        <CardDescription>登录到你的账户</CardDescription>
      </CardHeader>
      <CardContent>
        <FormKit type="form" :actions="false" @submit="handleLogin">
          <div class="space-y-4">
            <FormKit type="email" name="email" label="邮箱" placeholder="you@example.com" />
            <FormKit type="password" name="password" label="密码" />
            
            <p v-if="serverError" class="text-sm text-destructive">{{ serverError }}</p>
            
            <Button type="submit" class="w-full" :disabled="isLoading">
              {{ isLoading ? '登录中...' : '登录' }}
            </Button>
          </div>
        </FormKit>
      </CardContent>
    </Card>
  </div>
</template>
```

---

## 仪表盘页

```vue
<!-- pages/DashboardPage.vue -->
<script setup lang="ts">
import { useQueries } from '@tanstack/vue-query'
import { statsKeys } from '@/composables/useStats'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { TrendingUp, Users, DollarSign, Activity } from 'lucide-vue-next'

// 并行加载多个数据源
const [usersQuery, revenueQuery, activityQuery] = useQueries({
  queries: [
    { queryKey: statsKeys.users(), queryFn: statsService.getUsers, staleTime: 60_000 },
    { queryKey: statsKeys.revenue(), queryFn: statsService.getRevenue, staleTime: 60_000 },
    { queryKey: statsKeys.activity(), queryFn: statsService.getActivity, refetchInterval: 30_000 },
  ],
})

const metrics = computed(() => [
  {
    title: '总用户数',
    value: usersQuery.data?.total ?? '-',
    change: usersQuery.data?.changePercent,
    icon: Users,
    color: 'text-blue-600',
  },
  {
    title: '本月营收',
    value: revenueQuery.data ? formatCurrency(revenueQuery.data.monthly) : '-',
    change: revenueQuery.data?.changePercent,
    icon: DollarSign,
    color: 'text-green-600',
  },
])
</script>

<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-semibold tracking-tight">仪表盘</h1>
    
    <!-- 指标卡片 -->
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card v-for="metric in metrics" :key="metric.title">
        <CardHeader class="flex flex-row items-center justify-between pb-2">
          <CardTitle class="text-sm font-medium text-muted-foreground">
            {{ metric.title }}
          </CardTitle>
          <component :is="metric.icon" :class="['h-4 w-4', metric.color]" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ metric.value }}</div>
          <p v-if="metric.change" class="text-xs text-muted-foreground mt-1">
            <span :class="metric.change > 0 ? 'text-green-600' : 'text-red-600'">
              {{ metric.change > 0 ? '+' : '' }}{{ metric.change }}%
            </span>
            较上月
          </p>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
```
