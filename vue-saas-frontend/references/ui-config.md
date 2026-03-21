# UI 配置化规范

## 一、配置化理念

### 为什么需要配置化

- **减少重复代码**：表格列、表单字段通过配置对象声明
- **提升可维护性**：配置集中管理，修改只需调整配置对象
- **增强可读性**：配置即文档
- **便于复用**：配置可抽取为公共模块

### 配置 vs 代码的权衡

| 场景 | 推荐方式 |
|------|----------|
| 标准增删改查 | 配置化 |
| 复杂交互逻辑 | 代码实现 |
| 高度定制渲染 | render 函数 |
| 跨页面复用 | 配置 + 组合式函数 |

---

## 二、表格配置

### TableColumn 接口

```typescript
interface TableColumn<T> {
  key: keyof T | string              // 列标识，支持嵌套路径
  label: string                       // 列标题
  width?: string | number             // 列宽度
  fixed?: 'left' | 'right'            // 固定列
  sortable?: boolean | SortConfig<T>  // 排序配置
  filterable?: boolean | FilterConfig // 筛选配置
  render?: (row: T, index: number) => VNode | string | number
  align?: 'left' | 'center' | 'right'
  ellipsis?: boolean                  // 文本溢出省略
  tooltip?: boolean | ((row: T) => string)
  hidden?: boolean | ((row: T) => boolean)
}
```

### SortConfig / FilterConfig

```typescript
interface SortConfig<T = any> {
  field?: string
  direction?: 'asc' | 'desc'
  multiple?: boolean
  sorter?: (a: T, b: T, dir: string) => number
  remote?: boolean
}

interface FilterConfig {
  type: 'select' | 'input' | 'date' | 'daterange' | 'number' | 'cascader'
  options?: { label: string; value: any; disabled?: boolean }[]
  multiple?: boolean
  remote?: boolean
  placeholder?: string
  remoteMethod?: (query: string) => Promise<{ label: string; value: any }[]>
}
```

### TableAction 接口

```typescript
interface TableAction<T> {
  label: string
  icon?: Component
  handler: (row: T) => void | Promise<void>
  show?: (row: T) => boolean
  disabled?: (row: T) => boolean
  confirm?: string                    // 确认提示
  variant?: 'default' | 'destructive' | 'outline' | 'ghost'
  loading?: (row: T) => boolean
  permission?: string
}

interface ActionColumnConfig<T> {
  label?: string
  width?: number | string
  fixed?: 'left' | 'right'
  actions: TableAction<T>[]
  maxVisible?: number                 // 超出折叠
}
```

### DataTable Props

```typescript
interface DataTableProps<T extends { id: string }> {
  data: T[]
  columns: TableColumn<T>[]
  actions?: ActionColumnConfig<T>
  loading?: boolean
  selectable?: boolean
  selectedIds?: string[]
  pagination?: { total: number; pageSize: number; currentPage: number }
  emptyText?: string
  bordered?: boolean
  striped?: boolean
}
```

### 服务端集成

```typescript
// composables/useTableQuery.ts
export function useTableQuery(defaults: TableQueryDefaults) {
  const route = useRoute()
  const router = useRouter()
  const query = computed({
    get: () => ({
      page: Number(route.query.page) || 1,
      pageSize: Number(route.query.pageSize) || 20,
      sortField: route.query.sortField as string,
      sortDirection: route.query.sortDirection as 'asc' | 'desc'
    }),
    set: (val) => router.push({ query: { ...route.query, ...val } })
  })
  return { query }
}
```

### 使用示例

```vue
<script setup lang="ts">
interface User { id: string; name: string; email: string; status: 'active' | 'inactive' }

const columns: TableColumn<User>[] = [
  { key: 'name', label: '用户名', width: 120, sortable: true },
  { key: 'email', label: '邮箱', ellipsis: true, tooltip: true },
  { key: 'status', label: '状态', width: 100,
    filterable: { type: 'select', options: [{ label: '已激活', value: 'active' }] },
    render: (row) => h(Badge, { variant: row.status === 'active' ? 'success' : 'secondary' })
  }
]

const actions: ActionColumnConfig<User> = {
  width: 160, fixed: 'right',
  actions: [
    { label: '编辑', handler: (row) => openEditModal(row) },
    { label: '删除', variant: 'destructive', confirm: '确定删除？', handler: handleDelete }
  ]
}
</script>

<template>
  <DataTable :data="users" :columns="columns" :actions="actions" :pagination="pagination"
    selectable @sort="sortState = $event" @filter="filters = $event" />
</template>
```

---

## 三、表单配置

### FormField 接口

```typescript
interface FormField {
  name: string
  label: string
  type: FieldType
  placeholder?: string
  required?: boolean
  defaultValue?: any
  disabled?: boolean | FieldCondition
  hidden?: boolean | FieldCondition
  options?: FieldOptions | AsyncFieldOptions
  validation?: ZodSchema
  span?: number                       // Grid 栅格（1-24）
  dependencies?: string[]             // 依赖字段
  props?: Record<string, any>
}

type FieldType = 'text' | 'email' | 'password' | 'number' | 'textarea' | 'select' 
  | 'multiselect' | 'date' | 'daterange' | 'switch' | 'checkbox' | 'radio' | 'file' | 'custom'

type FieldCondition = (form: Record<string, any>) => boolean
type FieldOptions = { label: string; value: any }[]
type AsyncFieldOptions = (form?: Record<string, any>) => Promise<FieldOptions>
```

### FormConfig 接口

```typescript
interface FormConfig {
  fields: FormField[]
  layout?: 'vertical' | 'horizontal' | 'grid'
  columns?: number
  labelWidth?: string
  submitText?: string
  showReset?: boolean
  loading?: boolean
  onSubmit: (values: Record<string, any>) => Promise<void> | void
  onSuccess?: (values: Record<string, any>) => void
  onError?: (error: unknown) => void
}
```

### 字段类型详解

| 类型 | 说明 | 特殊 props |
|------|------|-----------|
| `text` / `email` / `password` | 文本类 | `maxlength`, `showCount` |
| `number` | 数字 | `min`, `max`, `step` |
| `textarea` | 多行文本 | `rows`, `autosize` |
| `select` / `multiselect` | 下拉选择 | `filterable`, `remote` |
| `date` / `daterange` | 日期 | `format`, `disabledDate` |
| `switch` | 开关 | `checkedChildren` |
| `file` | 文件上传 | `accept`, `maxSize` |
| `custom` | 自定义 | `component`, `render` |

### 联动字段

```typescript
// 条件显隐
const fields: FormField[] = [
  { name: 'userType', type: 'select', label: '用户类型',
    options: [{ label: '个人', value: 'personal' }, { label: '企业', value: 'enterprise' }] },
  { name: 'companyName', type: 'text', label: '公司名称',
    hidden: (form) => form.userType !== 'enterprise',
    dependencies: ['userType']
  }
]

// 级联选项
const fields: FormField[] = [
  { name: 'province', type: 'select', label: '省份', options: provinceOptions },
  { name: 'city', type: 'select', label: '城市',
    options: async (form) => form.province ? await fetchCities(form.province) : [],
    dependencies: ['province']
  }
]

// 动态验证
const fields: FormField[] = [
  { name: 'password', type: 'password', validation: z.string().min(8) },
  { name: 'confirmPassword', type: 'password',
    validation: z.string().refine((val, ctx) => val === (ctx as any).password, 
      { message: '两次密码不一致' }),
    dependencies: ['password']
  }
]
```

### 布局模式

```typescript
// 垂直布局
const config: FormConfig = { layout: 'vertical', fields: [...] }

// 水平布局
const config: FormConfig = { layout: 'horizontal', labelWidth: '100px', fields: [...] }

// 栅格布局
const config: FormConfig = {
  layout: 'grid', columns: 3,
  fields: [
    { name: 'name', type: 'text', label: '姓名', span: 1 },
    { name: 'address', type: 'text', label: '地址', span: 3 }
  ]
}
```

### 使用示例

```vue
<script setup lang="ts">
import { z } from 'zod'

const userFormConfig: FormConfig = {
  layout: 'grid', columns: 2, submitText: '保存用户',
  fields: [
    { name: 'username', type: 'text', label: '用户名', span: 1, required: true,
      validation: z.string().min(3).max(20) },
    { name: 'email', type: 'email', label: '邮箱', span: 1, required: true,
      validation: z.string().email() },
    { name: 'role', type: 'select', label: '角色', span: 1,
      options: [{ label: '管理员', value: 'admin' }] },
    { name: 'status', type: 'switch', label: '状态', span: 1, defaultValue: true }
  ],
  onSubmit: async (values) => { await api.createUser(values) },
  onSuccess: () => { message.success('创建成功') }
}
</script>

<template>
  <ConfigForm :config="userFormConfig" />
</template>
```

---

## 四、最佳实践

### 配置复用策略

```typescript
// configs/table/user-columns.ts
export const userColumns: TableColumn<User>[] = [
  { key: 'name', label: '用户名', width: 120, sortable: true },
  { key: 'email', label: '邮箱', ellipsis: true }
]

// 页面中扩展
const columns: TableColumn<User>[] = [
  ...userColumns,
  { key: 'department', label: '部门', width: 120 }
]
```

### 类型安全

```typescript
function defineColumns<T>(columns: TableColumn<T>[]): TableColumn<T>[] {
  return columns
}

const columns = defineColumns<User>([
  { key: 'name', label: '用户名' },  // ✓ key 有类型提示
  { key: 'invalid', label: '无效' }  // ✗ 类型错误
])
```

---

## 五、禁止事项

| 禁止项 | 原因 |
|--------|------|
| 在 render 函数中使用 async | 渲染函数必须同步返回 |
| 直接修改 props.data | 违反单向数据流 |
| 在 sorter 中使用外部状态 | 排序结果不可预测 |
| 硬编码 options 而不使用配置 | 降低复用性 |
| 在 TableAction 中直接调用 API | 应通过 handler 解耦 |
| 忽略 loading 状态 | 易产生竞态问题 |
| 使用 index 作为 rowKey | 分页时选中状态错乱 |
| 在 dependencies 中遗漏依赖字段 | 联动失效 |
| 在 validation 中使用非 Zod Schema | 验证不生效 |
| 在 span 中使用超出 1-24 范围的值 | 布局错乱 |