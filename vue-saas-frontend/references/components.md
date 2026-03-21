# Components Reference — Vue SaaS Frontend

## 目录

1. [数据表格组件](#数据表格组件)
2. [通用弹窗模式](#通用弹窗模式)
3. [状态反馈组件](#状态反馈组件)
4. [布局组件](#布局组件)

---

## 数据表格组件

SaaS 最常见场景，集成分页 + 排序 + 筛选 + 批量操作：

```vue
<!-- components/DataTable.vue -->
<script setup lang="ts" generic="T extends { id: string }">
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '@/components/ui/table'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Skeleton } from '@/components/ui/skeleton'

interface Column<T> {
  key: keyof T | string
  label: string
  sortable?: boolean
  render?: (row: T) => string | number
}

interface Props {
  data: T[]
  columns: Column<T>[]
  isLoading?: boolean
  selectable?: boolean
  totalCount?: number
  pageSize?: number
  currentPage?: number
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false,
  selectable: false,
  pageSize: 20,
  currentPage: 1,
})

const emit = defineEmits<{
  (e: 'sort', key: string, direction: 'asc' | 'desc'): void
  (e: 'page-change', page: number): void
  (e: 'select', ids: string[]): void
}>()

const selectedIds = ref<Set<string>>(new Set())
const isAllSelected = computed(
  () => props.data.length > 0 && props.data.every(row => selectedIds.value.has(row.id))
)

function toggleSelectAll() {
  if (isAllSelected.value) {
    selectedIds.value.clear()
  } else {
    props.data.forEach(row => selectedIds.value.add(row.id))
  }
  emit('select', [...selectedIds.value])
}
</script>

<template>
  <div class="rounded-md border">
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead v-if="selectable" class="w-12">
            <Checkbox :checked="isAllSelected" @update:checked="toggleSelectAll" />
          </TableHead>
          <TableHead v-for="col in columns" :key="String(col.key)">
            {{ col.label }}
          </TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <!-- Loading skeleton -->
        <template v-if="isLoading">
          <TableRow v-for="i in pageSize" :key="i">
            <TableCell v-for="col in columns" :key="String(col.key)">
              <Skeleton class="h-4 w-full" />
            </TableCell>
          </TableRow>
        </template>
        <!-- Empty state -->
        <TableRow v-else-if="data.length === 0">
          <TableCell :colspan="columns.length + (selectable ? 1 : 0)" class="h-24 text-center text-muted-foreground">
            暂无数据
          </TableCell>
        </TableRow>
        <!-- Data rows -->
        <TableRow v-else v-for="row in data" :key="row.id"
          :class="{ 'bg-muted/30': selectedIds.has(row.id) }">
          <TableCell v-if="selectable">
            <Checkbox
              :checked="selectedIds.has(row.id)"
              @update:checked="(v) => { v ? selectedIds.add(row.id) : selectedIds.delete(row.id); emit('select', [...selectedIds]) }"
            />
          </TableCell>
          <slot :row="row" :columns="columns">
            <TableCell v-for="col in columns" :key="String(col.key)">
              {{ col.render ? col.render(row) : row[col.key as keyof T] }}
            </TableCell>
          </slot>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
```

---

## 通用弹窗模式

### 确认删除对话框

```vue
<!-- components/ConfirmDeleteDialog.vue -->
<script setup lang="ts">
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel,
  AlertDialogContent, AlertDialogDescription,
  AlertDialogFooter, AlertDialogHeader, AlertDialogTitle,
} from '@/components/ui/alert-dialog'

interface Props {
  open: boolean
  title?: string
  description?: string
  isDeleting?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '确认删除',
  description: '此操作不可撤销，数据将被永久删除。',
  isDeleting: false,
})

const emit = defineEmits<{
  (e: 'update:open', v: boolean): void
  (e: 'confirm'): void
}>()
</script>

<template>
  <AlertDialog :open="open" @update:open="emit('update:open', $event)">
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>{{ title }}</AlertDialogTitle>
        <AlertDialogDescription>{{ description }}</AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel :disabled="isDeleting">取消</AlertDialogCancel>
        <AlertDialogAction
          class="bg-destructive text-destructive-foreground hover:bg-destructive/90"
          :disabled="isDeleting"
          @click="emit('confirm')"
        >
          {{ isDeleting ? '删除中...' : '确认删除' }}
        </AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
```

---

## 状态反馈组件

### 三态展示模式（Loading / Error / Content）

```vue
<!-- composables/useAsyncState.ts -->
<script setup lang="ts">
// 在页面组件中使用 TanStack Query 处理三态
const { data, isLoading, isError, error } = useUserList(filters)
</script>

<template>
  <!-- Loading -->
  <div v-if="isLoading" class="space-y-3">
    <Skeleton class="h-10 w-full" v-for="i in 5" :key="i" />
  </div>
  
  <!-- Error -->
  <div v-else-if="isError" class="flex flex-col items-center justify-center py-12 gap-3">
    <AlertCircle class="h-12 w-12 text-destructive" />
    <p class="text-muted-foreground">加载失败：{{ error?.message }}</p>
    <Button variant="outline" @click="refetch">重试</Button>
  </div>
  
  <!-- Content -->
  <DataTable v-else :data="data?.items ?? []" :columns="columns" />
</template>
```

### Toast 通知模式

```typescript
// 使用 shadcn-vue 的 useToast
import { useToast } from '@/components/ui/toast'

const { toast } = useToast()

// 成功
toast({ title: '保存成功', description: '用户信息已更新' })

// 错误
toast({ title: '操作失败', description: error.message, variant: 'destructive' })

// 带操作
toast({
  title: '已删除',
  description: '用户已被移除',
  action: h(ToastAction, { altText: '撤销', onClick: handleUndo }, '撤销'),
})
```

---

## 布局组件

### SaaS Dashboard 布局结构

```vue
<!-- layouts/DashboardLayout.vue -->
<script setup lang="ts">
import { SidebarProvider, Sidebar, SidebarContent } from '@/components/ui/sidebar'
import AppSidebar from '@/components/AppSidebar.vue'
import AppHeader from '@/components/AppHeader.vue'
</script>

<template>
  <SidebarProvider>
    <AppSidebar />
    <main class="flex-1 flex flex-col min-h-screen">
      <AppHeader />
      <div class="flex-1 p-6">
        <RouterView />
      </div>
    </main>
  </SidebarProvider>
</template>
```

### 页面容器标准间距

```html
<!-- 标准页面容器 -->
<div class="space-y-6">
  <!-- 页头 -->
  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-2xl font-semibold tracking-tight">页面标题</h1>
      <p class="text-sm text-muted-foreground">页面描述</p>
    </div>
    <Button>新增</Button>
  </div>
  
  <!-- 筛选区 -->
  <Card>
    <CardContent class="pt-6">
      <!-- 筛选表单 -->
    </CardContent>
  </Card>
  
  <!-- 数据区 -->
  <DataTable />
</div>
```
