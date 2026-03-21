# 组件开发完整指南

> Vue 3 + shadcn-vue 组件开发规范，涵盖分层架构、基础模式、扩展机制、复杂实现与文档规范。

---

## 一、组件分层架构

### 四层架构

```
┌─────────────────────────────────────────┐
│  layout/     布局组件（页面骨架）          │
├─────────────────────────────────────────┤
│  business/   业务领域组件（特定领域）       │
├─────────────────────────────────────────┤
│  common/     通用业务组件（跨模块复用）      │
├─────────────────────────────────────────┤
│  ui/         UI 基础组件（shadcn-vue）     │
└─────────────────────────────────────────┘
```

**依赖方向**：`business → common → ui`（单向依赖，禁止反向）

### 分层决策树

```
开始 → 是否为页面骨架结构？ ──是──▶ layout/
      │
      否
      ↓
      是否为 shadcn-vue 基础组件？ ──是──▶ ui/
      │
      否
      ↓
      是否跨业务模块复用？ ──是──▶ common/
      │
      否
      ↓
      是否跨页面复用？ ──是──▶ business/{domain}/
      │
      否
      ↓
      页面目录 _components/
```

### 目录结构

```
components/
├── ui/                    # shadcn-vue 组件（禁止修改）
├── common/                # 通用业务组件
│   ├── PageHeader.vue
│   ├── EmptyState.vue
│   ├── LoadingState.vue
│   ├── ErrorState.vue
│   ├── ConfirmDialog.vue
│   └── index.ts
├── business/              # 业务领域组件
│   ├── user/
│   ├── order/
│   └── product/
└── layout/                # 布局组件
    ├── DashboardLayout.vue
    ├── AuthLayout.vue
    ├── AppSidebar.vue
    └── AppHeader.vue
```

---

## 二、基础组件模式

### DataTable 数据表格

SaaS 最常见场景，集成分页 + 排序 + 筛选 + 批量操作：

```vue
<!-- components/common/DataTable.vue -->
<script setup lang="ts" generic="T extends { id: string }">
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
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
  pageSize?: number
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false,
  selectable: false,
  pageSize: 20,
})

const emit = defineEmits<{
  (e: 'sort', key: string, direction: 'asc' | 'desc'): void
  (e: 'page-change', page: number): void
  (e: 'select', ids: string[]): void
}>()

const selectedIds = ref<Set<string>>(new Set())
</script>

<template>
  <div class="rounded-md border">
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead v-if="selectable" class="w-12">
            <Checkbox :checked="isAllSelected" @update:checked="toggleSelectAll" />
          </TableHead>
          <TableHead v-for="col in columns" :key="String(col.key)">{{ col.label }}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <template v-if="isLoading">
          <TableRow v-for="i in pageSize" :key="i">
            <TableCell v-for="col in columns" :key="String(col.key)">
              <Skeleton class="h-4 w-full" />
            </TableCell>
          </TableRow>
        </template>
        <TableRow v-else-if="data.length === 0">
          <TableCell :colspan="columns.length + (selectable ? 1 : 0)" class="h-24 text-center text-muted-foreground">
            暂无数据
          </TableCell>
        </TableRow>
        <TableRow v-else v-for="row in data" :key="row.id">
          <slot :row="row" :columns="columns" />
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
```

### ConfirmDialog 确认对话框

```vue
<!-- components/common/ConfirmDialog.vue -->
<script setup lang="ts">
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog'

interface Props {
  open: boolean
  title?: string
  description?: string
  confirmText?: string
  destructive?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '确认操作',
  description: '此操作不可撤销。',
  confirmText: '确认',
  destructive: false,
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
        <AlertDialogCancel>取消</AlertDialogCancel>
        <AlertDialogAction :class="{ 'bg-destructive': destructive }" @click="emit('confirm')">
          {{ confirmText }}
        </AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
```

### 状态反馈组件

```vue
<!-- components/common/LoadingState.vue -->
<script setup lang="ts">
defineProps<{ type?: 'skeleton' | 'spinner' }>()
</script>
<template>
  <div v-if="type === 'spinner'" class="flex justify-center py-8">
    <Loader2 class="h-8 w-8 animate-spin" />
  </div>
  <div v-else class="space-y-3">
    <Skeleton class="h-4 w-full" />
    <Skeleton class="h-4 w-3/4" />
  </div>
</template>
```

```vue
<!-- components/common/ErrorState.vue -->
<script setup lang="ts">
import { Button } from '@/components/ui/button'
defineProps<{ message: string }>()
const emit = defineEmits<{ retry: [] }>()
</script>
<template>
  <div class="flex flex-col items-center py-8 text-center">
    <AlertCircle class="h-10 w-10 text-destructive" />
    <p class="mt-2 text-sm text-muted-foreground">{{ message }}</p>
    <Button variant="outline" class="mt-4" @click="emit('retry')">重试</Button>
  </div>
</template>
```

### 三态展示模式

```vue
<script setup lang="ts">
const { data, isLoading, isError, error } = useUserList(filters)
</script>

<template>
  <LoadingState v-if="isLoading" />
  <ErrorState v-else-if="isError" :message="error?.message" @retry="refetch" />
  <DataTable v-else :data="data?.items ?? []" :columns="columns" />
</template>
```

### Toast 通知

```typescript
import { useToast } from '@/components/ui/toast'
const { toast } = useToast()

// 成功
toast({ title: '保存成功', description: '用户信息已更新' })

// 错误
toast({ title: '操作失败', description: error.message, variant: 'destructive' })
```

---

## 三、组件扩展机制

### Slots 扩展

```vue
<!-- Card.vue -->
<template>
  <div class="card">
    <slot name="header"><h3>{{ title }}</h3></slot>
    <slot />
    <slot name="footer" :actions="actions" />
  </div>
</template>
```

| 类型 | 用途 | 示例 |
|------|------|------|
| 默认插槽 | 主内容区域 | `<slot />` |
| 具名插槽 | 特定区域定制 | `<slot name="header" />` |
| 作用域插槽 | 数据传递给父组件 | `<slot :data="items" />` |

### Props 透传

```vue
<script setup lang="ts">
defineOptions({ inheritAttrs: false })
interface Props { modelValue?: string; disabled?: boolean }
const props = defineProps<Props>()
const emit = defineEmits(['update:modelValue'])
</script>
<template>
  <input v-bind="$attrs" :value="modelValue" :disabled="disabled"
    @input="emit('update:modelValue', $event.target.value)" />
</template>
```

### Composables 组合

```typescript
export function useDataTable<T>(config: TableConfig<T>) {
  const pagination = usePagination(config.pagination)
  const sorting = useSorting(config.sorting)
  const filtering = useFiltering(config.filtering)
  return { ...pagination, ...sorting, ...filtering }
}
```

### 无渲染组件

```vue
<!-- RenderlessQuery.vue -->
<script setup lang="ts" generic="T">
const props = defineProps<{ queryFn: () => Promise<T> }>()
const { data, isLoading, error, refetch } = useQuery(() => props.queryFn())
</script>
<template>
  <slot :data="data" :is-loading="isLoading" :error="error" :refetch="refetch" />
</template>
```

### 扩展优先级

**Slots > Props 透传 > Composables > HOC**

---

## 四、复杂组件实现

### CommandPalette 命令面板

```vue
<!-- components/CommandPalette.vue -->
<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Dialog, DialogContent } from '@/components/ui/dialog'
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandSeparator } from '@/components/ui/command'

const open = ref(false)
const query = ref('')
const router = useRouter()

const commands = [
  { id: 'dashboard', label: '仪表盘', icon: Home, group: 'navigation', shortcut: 'G D', action: () => router.push('/dashboard') },
  { id: 'users', label: '用户管理', icon: Users, group: 'navigation', shortcut: 'G U', action: () => router.push('/users') },
  { id: 'new-user', label: '新建用户', icon: Users, group: 'actions', shortcut: 'N U', action: () => {} },
  { id: 'settings', label: '系统设置', icon: Settings, group: 'settings', shortcut: '⌘ ,', action: () => router.push('/settings') },
]

const groups = computed(() => {
  const groupMap = { navigation: { label: '导航', items: [] }, actions: { label: '操作', items: [] }, settings: { label: '设置', items: [] } }
  const q = query.value.toLowerCase()
  commands.filter(c => c.label.toLowerCase().includes(q)).forEach(c => groupMap[c.group]?.items.push(c))
  return Object.values(groupMap).filter(g => g.items.length > 0)
})

function handleKeydown(e: KeyboardEvent) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); open.value = !open.value }
}
onMounted(() => window.addEventListener('keydown', handleKeydown))
onUnmounted(() => window.removeEventListener('keydown', handleKeydown))
</script>

<template>
  <Dialog v-model:open="open">
    <DialogContent class="max-w-lg p-0 overflow-hidden">
      <Command class="rounded-lg border shadow-lg">
        <CommandInput v-model="query" placeholder="搜索命令或跳转..." />
        <CommandList class="max-h-80">
          <CommandEmpty>未找到相关命令</CommandEmpty>
          <template v-for="(group, i) in groups" :key="group.label">
            <CommandSeparator v-if="i > 0" />
            <CommandGroup :heading="group.label">
              <CommandItem v-for="item in group.items" :key="item.id" @select="item.action(); open = false">
                <component :is="item.icon" class="mr-2 h-4 w-4 text-muted-foreground" />
                <span>{{ item.label }}</span>
                <kbd v-if="item.shortcut" class="ml-auto text-xs text-muted-foreground">{{ item.shortcut }}</kbd>
              </CommandItem>
            </CommandGroup>
          </template>
        </CommandList>
      </Command>
    </DialogContent>
  </Dialog>
</template>
```

### InlineEdit 行内编辑

```vue
<!-- components/InlineEdit.vue -->
<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import { Input } from '@/components/ui/input'

interface Props {
  modelValue: string | number
  type?: 'text' | 'number'
  disabled?: boolean
  validator?: (v: string | number) => string | null
}

const props = withDefaults(defineProps<Props>(), { type: 'text', disabled: false })
const emit = defineEmits<{
  (e: 'update:modelValue', v: string | number): void
  (e: 'save', v: string | number): Promise<void> | void
}>()

const editing = ref(false)
const tempValue = ref<string | number>('')
const loading = ref(false)
const error = ref<string | null>(null)

async function startEdit() {
  if (props.disabled) return
  tempValue.value = props.modelValue
  editing.value = true
  await nextTick()
}

async function save() {
  if (props.validator) { const err = props.validator(tempValue.value); if (err) { error.value = err; return } }
  loading.value = true
  try {
    await emit('save', tempValue.value)
    emit('update:modelValue', tempValue.value)
    editing.value = false
  } catch (e: any) { error.value = e.message || '保存失败' }
  finally { loading.value = false }
}
</script>

<template>
  <div class="group relative inline-flex items-center">
    <div v-if="!editing" @click="startEdit" :class="disabled ? 'cursor-not-allowed opacity-50' : 'hover:bg-muted cursor-text'">
      <span>{{ modelValue || '点击编辑' }}</span>
      <Pencil v-if="!disabled" class="inline ml-2 h-3.5 w-3.5 text-muted-foreground opacity-0 group-hover:opacity-100" />
    </div>
    <div v-else class="flex items-center gap-2">
      <Input v-model="tempValue" :type="type" @blur="save" @keydown.enter="save" @keydown.esc="editing = false" />
      <Loader2 v-if="loading" class="h-4 w-4 animate-spin" />
    </div>
  </div>
</template>
```

---

## 五、组件文档规范

### 文件头注释

```vue
<!--
  UserCard.vue
  用户卡片组件，展示用户基本信息和支持快捷操作

  @author 开发者姓名
  @created 2024-01-01
  @updated 2024-03-21

  @example
  <UserCard :user="currentUser" @edit="handleEdit" />
-->
```

### Props 文档

```typescript
interface Props {
  /** 用户对象，必填 */
  user: User
  /** 是否显示操作按钮，默认 true */
  showActions?: boolean
}

const props = withDefaults(defineProps<Props>(), { showActions: true })
```

### Emits 文档

```typescript
defineEmits<{
  /** 点击编辑时触发 */
  (e: 'edit', user: User): void
  /** 点击删除时触发，返回用户 ID */
  (e: 'delete', id: string): void
}>()
```

### Slots 文档

```typescript
defineSlots<{
  /** 自定义内容区域 */
  default(): any
  /** 自定义操作按钮区域，提供 user 对象 */
  actions(props: { user: User }): any
}>()
```

### 文档检查清单

- [ ] 文件头包含组件名称和描述
- [ ] 所有 Props 有 JSDoc 注释
- [ ] 所有 Emits 有事件说明
- [ ] 所有 Slots 有用途说明
- [ ] 包含至少一个使用示例

---

## 六、禁止事项

| 禁止项 | 原因 | 替代方案 |
|--------|------|----------|
| 修改 `ui/` 目录下的 shadcn-vue 源码 | 升级时会丢失修改 | 创建包装组件于 common/ |
| `ui/` 组件依赖 `common/` 或 `business/` | 违反单向依赖原则 | - |
| `common/` 组件依赖 `business/` | 违反单向依赖原则 | - |
| 在 `ui/` 组件中硬编码业务文案 | 破坏复用性 | 通过 props 传入 |
| Mixins | 命名冲突、来源不明 | Composables |
| Filters | Vue 3 已移除 | computed / 方法 |
| $on/$off | 已移除 | mitt / useEventBus |
| 直接修改 props | 违反单向数据流 | emit / v-model |
| 过度使用 provide/inject | 隐式依赖 | Props / Composables |
| 使用 `any` 类型 | 丧失类型安全 | 明确类型定义 |
| 命令面板超过 600px 宽度 | 破坏焦点感 | 限制宽度 |
| 命令面板忽略键盘导航 | 无障碍问题 | 支持 ↑↓ Enter Esc |
| 行内编辑无验证直接保存 | 数据安全 | 必须有错误处理 |
| 快捷键硬编码 `⌘` 或 `Ctrl` | 跨平台问题 | 自动检测平台 |

---

## 七、与设计系统协作

### 样式 Token 使用

组件样式参考 `saas-design-system` skill，使用设计系统定义的 Token：

```css
/* 颜色 Token */
--primary, --secondary, --destructive, --muted, --accent

/* 字体 Token */
text-sm, text-base, text-lg, font-medium, font-semibold

/* 间距 Token */
space-y-6, p-6, gap-4, mt-4
```

### 设计系统集成

| 设计系统资源 | 组件使用方式 |
|-------------|-------------|
| 颜色变量 | `class="text-primary bg-muted"` |
| 间距规范 | `class="space-y-6 p-6"` |
| 圆角规范 | `class="rounded-md rounded-lg"` |
| 阴影规范 | `class="shadow-sm shadow-lg"` |

### 响应式断点

```html
<!-- 使用设计系统断点 -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```