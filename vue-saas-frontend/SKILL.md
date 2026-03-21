---
name: vue-saas-frontend
description: >
  SaaS 级 Vue 3.5+/TypeScript 5.7+ 前端开发技能。当用户需要使用 Vue 3、TypeScript、Tailwind CSS、Shadcn-vue、Pinia、TanStack Query、FormKit、Zod、Radix Vue 等技术栈开发前端页面、UI 组件、SaaS 仪表盘、数据表格、复杂表单、认证页面、设置页面、管理后台时，必须使用此 skill。即使用户只是说"帮我写个 Vue 组件"、"做个 SaaS 页面"、"用 shadcn 组件"也应触发。覆盖从文件结构、组件设计、状态管理、服务端状态、到测试的完整 SaaS 前端开发流程。
---

# Vue SaaS Frontend 开发 Skill

本 skill 指导使用以下技术栈构建生产级 SaaS 前端应用：

| 类别 | 选型 | 版本/备注 |
|------|------|-----------|
| Core | Vue 3 + TypeScript | 3.5+ / TS 5.7+，严格模式 |
| Build | Vite | 6，利用 Rolldown |
| Styling | Tailwind CSS + CVA | 4，原子化 + 变体管理 |
| UI Logic | Radix Vue | Headless，无障碍基石 |
| UI Library | Shadcn-vue | 复制源码，完全可控 |
| State | Pinia 3 + Persisted State | 模块化状态管理 |
| Server State | TanStack Query | 缓存、重试、同步 |
| Forms | FormKit + Zod | 复杂表单 |
| Icons | Lucide Vue | 现代简洁 |
| Testing | Vitest + Vue Test Utils + Playwright | 单元 + E2E |
| Docs | VitePress | 组件文档 |

---

## 开发流程

### Step 1 — 理解需求，确定输出范围

在写任何代码前，先明确：
- **页面类型**：仪表盘 / 数据列表 / 表单页 / 认证 / 设置 / 详情页
- **交互复杂度**：静态展示 / 本地状态 / 服务端状态 / 表单提交
- **输出粒度**：单个组件 / 完整页面 / 多页面模块

> 如需了解架构决策细节，参阅 `references/architecture.md`

---

### Step 2 — 项目结构与文件组织

标准 SaaS 项目目录：

```
src/
├── assets/              # 静态资源
├── components/
│   ├── ui/              # shadcn-vue 组件（复制源码）
│   └── [feature]/       # 业务组件，按特性分组
├── composables/         # use* 开头的组合式函数
├── layouts/             # 页面布局（AuthLayout, DashboardLayout...）
├── pages/               # 路由页面组件
├── router/              # Vue Router 配置
├── stores/              # Pinia stores（模块化）
├── services/            # API 调用层（axios / fetch 封装）
├── types/               # TypeScript 类型定义
│   ├── api.ts           # API 响应类型
│   └── models.ts        # 业务模型类型
├── lib/
│   └── utils.ts         # cn() 等工具函数
└── main.ts
```

---

### Step 3 — TypeScript 规范

**严格模式配置（tsconfig.json）：**
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true
  }
}
```

**核心原则：**
- 所有 props 使用 `defineProps<T>()` 泛型语法，禁止 `PropType`
- 所有 emits 使用 `defineEmits<{ (e: 'update:modelValue', v: string): void }>()` 形式
- API 响应必须定义 Zod schema 并推导类型，不允许 `any`
- 优先用 `interface` 定义对象类型，`type` 用于联合/交叉类型

```typescript
// ✅ 推荐
interface User {
  id: string
  name: string
  email: string
  role: 'admin' | 'member' | 'viewer'
}

// API schema + 类型推导
import { z } from 'zod'
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  role: z.enum(['admin', 'member', 'viewer'])
})
type User = z.infer<typeof UserSchema>
```

---

### Step 4 — 组件开发规范

**SFC 结构顺序（严格遵守）：**

```vue
<script setup lang="ts">
// 1. 外部 import
import { ref, computed } from 'vue'
import { useQuery } from '@tanstack/vue-query'

// 2. 组件 props / emits
interface Props {
  userId: string
  variant?: 'default' | 'compact'
}
const props = withDefaults(defineProps<Props>(), {
  variant: 'default'
})
const emit = defineEmits<{
  (e: 'select', user: User): void
}>()

// 3. composables / stores
const store = useUserStore()

// 4. 响应式状态
const isOpen = ref(false)

// 5. computed
const displayName = computed(() => ...)

// 6. 方法
function handleClick() { ... }

// 7. 生命周期（按顺序）
onMounted(() => { ... })
</script>

<template>
  <!-- 单根元素或 Fragment -->
</template>
```

**Shadcn-vue 组件使用模式：**

```vue
<!-- 优先使用 shadcn 组件，按需从 @/components/ui 导入 -->
<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
</script>
```

**CVA 变体管理（自定义组件）：**

```typescript
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  }
)

type ButtonProps = VariantProps<typeof buttonVariants>
```

> 更多组件模式参阅 `references/components.md`

---

### Step 5 — 状态管理（Pinia 3）

**Store 定义模板：**

```typescript
// stores/useUserStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref<User | null>(null)
  const preferences = ref<UserPreferences>({
    theme: 'system',
    language: 'zh-CN',
  })

  // Getters
  const isAuthenticated = computed(() => currentUser.value !== null)
  const isAdmin = computed(() => currentUser.value?.role === 'admin')

  // Actions
  async function fetchCurrentUser() {
    const data = await userService.getMe()
    currentUser.value = UserSchema.parse(data)
  }

  function logout() {
    currentUser.value = null
  }

  return { currentUser, preferences, isAuthenticated, isAdmin, fetchCurrentUser, logout }
}, {
  persist: {
    paths: ['preferences'], // 只持久化偏好，不持久化用户数据
  }
})
```

**原则：**
- 使用 Setup Store 风格（函数式），而非 Options 风格
- 敏感数据（token、user）不应持久化到 localStorage；用 httpOnly cookie
- 每个业务域独立一个 store 文件

---

### Step 6 — 服务端状态（TanStack Query）

```typescript
// composables/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'

// 查询键工厂（类型安全）
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  detail: (id: string) => [...userKeys.all, 'detail', id] as const,
}

// 列表查询
export function useUserList(filters: Ref<UserFilters>) {
  return useQuery({
    queryKey: computed(() => userKeys.list(filters.value)),
    queryFn: () => userService.getList(filters.value),
    staleTime: 5 * 60 * 1000, // 5分钟
  })
}

// 创建变更
export function useCreateUser() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: userService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() })
    },
  })
}
```

**缓存策略：**
- `staleTime`: 静态数据 30min，列表 5min，详情 2min
- 乐观更新用于高频操作（点赞、状态切换）
- 在路由进入时用 `prefetchQuery` 预加载

---

### Step 7 — 表单处理（FormKit + Zod）

```vue
<script setup lang="ts">
import { z } from 'zod'
import { useForm } from '@formkit/vue'

const schema = z.object({
  name: z.string().min(2, '名称至少 2 个字符'),
  email: z.string().email('邮箱格式不正确'),
  role: z.enum(['admin', 'member']),
})

type FormValues = z.infer<typeof schema>

const { handleSubmit, errors } = useForm<FormValues>({
  validationSchema: schema,
})

const onSubmit = handleSubmit(async (values) => {
  await createUser(values)
})
</script>

<template>
  <FormKit type="form" @submit="onSubmit">
    <FormKit type="text" name="name" label="名称" :errors="errors.name" />
    <FormKit type="email" name="email" label="邮箱" :errors="errors.email" />
    <FormKit type="select" name="role" label="角色"
      :options="[{ label: '管理员', value: 'admin' }, { label: '成员', value: 'member' }]"
    />
  </FormKit>
</template>
```

> 复杂表单场景（多步骤、动态字段、文件上传）参阅 `references/forms.md`

---

### Step 8 — Tailwind CSS 4 规范

**CSS 变量主题系统：**

```css
/* src/assets/main.css */
@import "tailwindcss";

@theme {
  --color-brand-50: oklch(97% 0.02 250);
  --color-brand-500: oklch(55% 0.18 250);
  --color-brand-900: oklch(25% 0.10 250);
  
  --radius-card: 0.75rem;
  --shadow-card: 0 1px 3px oklch(0% 0 0 / 0.08), 0 4px 16px oklch(0% 0 0 / 0.04);
}
```

**实用类使用原则：**
- 使用 `cn()` 合并类名（clsx + tailwind-merge）
- 响应式优先：`sm:` `md:` `lg:` `xl:` 断点
- 状态变体：`hover:` `focus:` `active:` `disabled:` `group-hover:`
- 暗色模式：`dark:` + CSS 变量结合
- 禁止在 class 中使用动态字符串拼接（`text-${color}-500` 无法被 Tailwind 检测）

---

### Step 9 — Icon 规范（Lucide Vue）

**导入规范：**

```typescript
// ✅ 按需具名导入，Tree-shaking 友好
import { Search, Plus, Trash2, MoreHorizontal, ChevronDown } from 'lucide-vue-next'

// ❌ 禁止全量导入
import * as Icons from 'lucide-vue-next'
```

**尺寸标准（严格遵守）：**

| 场景 | class | 像素 |
|------|-------|------|
| 按钮内图标 | `h-4 w-4` | 16px |
| 输入框前缀/后缀 | `h-4 w-4` | 16px |
| 菜单项图标 | `h-4 w-4` | 16px |
| 导航侧边栏 | `h-5 w-5` | 20px |
| 空状态插图 | `h-10 w-10` 或 `h-12 w-12` | 40–48px |
| 指标卡片装饰 | `h-4 w-4` 或 `h-5 w-5` | 16–20px |

**颜色规范：**

```html
<!-- 继承父级文字颜色（推荐，随主题自动适配） -->
<Search class="h-4 w-4" />

<!-- 弱化/辅助图标 -->
<Search class="h-4 w-4 text-muted-foreground" />

<!-- 语义色图标 -->
<CheckCircle class="h-4 w-4 text-green-600" />
<AlertCircle class="h-4 w-4 text-destructive" />
<Info class="h-4 w-4 text-blue-500" />

<!-- 品牌色图标 -->
<Star class="h-4 w-4 text-brand-500" />
```

**图标与文字对齐：**

```html
<!-- 行内对齐：使用 flex + gap，禁止用 margin 微调 -->
<button class="inline-flex items-center gap-2">
  <Plus class="h-4 w-4" />
  新增用户
</button>

<!-- 仅图标按钮：必须加 aria-label -->
<Button variant="ghost" size="icon" aria-label="删除">
  <Trash2 class="h-4 w-4" />
</Button>
```

**加载态替换图标（Spinner 模式）：**

```vue
<script setup lang="ts">
import { Loader2, Save } from 'lucide-vue-next'
</script>

<template>
  <Button :disabled="isLoading">
    <Loader2 v-if="isLoading" class="h-4 w-4 animate-spin" />
    <Save v-else class="h-4 w-4" />
    {{ isLoading ? '保存中...' : '保存' }}
  </Button>
</template>
```

**常用图标速查（SaaS 场景）：**

```typescript
// 操作类
Plus, PlusCircle          // 新增
Pencil, Edit2             // 编辑
Trash2                    // 删除（用 Trash2 而非 Trash，视觉更清晰）
Copy, ClipboardCopy       // 复制
Download, Upload          // 文件操作
RefreshCw                 // 刷新（加 animate-spin 变 loading）
MoreHorizontal            // 更多操作（dropdown trigger）
ExternalLink              // 外链跳转

// 导航类
ChevronDown, ChevronRight // 折叠/展开
ArrowLeft, ArrowRight     // 返回/前进
LayoutDashboard           // 仪表盘
Users, User               // 用户管理
Settings, SlidersHorizontal // 设置
LogOut                    // 退出登录

// 状态类
Check, CheckCircle2       // 成功
X, XCircle                // 错误/关闭
AlertTriangle             // 警告
Info, InfoCircle          // 提示
Loader2                   // 加载（配合 animate-spin）

// 数据类
Search                    // 搜索
Filter                    // 筛选
SortAsc, SortDesc         // 排序
BarChart2, LineChart      // 图表
TrendingUp, TrendingDown  // 趋势

// 通用
Eye, EyeOff               // 显示/隐藏密码
Bell                      // 通知
Shield, Lock              // 权限/安全
Globe                     // 国际化
Moon, Sun                 // 暗色/亮色模式切换
```

**禁止事项：**
- 禁止用 `width`/`height` 属性设置尺寸，统一用 Tailwind `h-* w-*`
- 禁止混用 Lucide 和其他 icon 库（如 Heroicons、FontAwesome）在同一项目
- 禁止对图标添加 `stroke-width` 属性（保持 Lucide 默认 1.5，与 shadcn-vue 一致）
- 仅图标的交互元素必须提供 `aria-label`

---

### Step 10 — 典型 SaaS 页面模式

根据页面类型选择对应模式：

| 页面类型 | 关键组件 | 状态策略 |
|----------|----------|----------|
| 数据表格 | DataTable + 分页 + 筛选 | TanStack Query + URL 参数同步 |
| 详情/编辑 | Form + 面包屑 | Query(读) + Mutation(写) |
| 仪表盘 | Cards + Charts | 多 Query 并行 + refetchInterval |
| 认证流 | Form + 步骤 | Local state + Pinia |
| 设置页 | Tabs + Form | Query + Mutation + 乐观更新 |
| 模态/抽屉 | Dialog/Sheet | Local state 或 URL 状态 |

> 完整页面实现示例参阅 `references/page-patterns.md`

---

### Step 11 — 无障碍与 Radix Vue

Radix Vue 已内置 ARIA 支持，使用时遵守：

```vue
<!-- 使用 Radix Vue 原生组件，不要覆盖 aria-* 属性 -->
<DialogRoot v-model:open="isOpen">
  <DialogTrigger as-child>
    <Button>打开</Button>
  </DialogTrigger>
  <DialogPortal>
    <DialogOverlay class="fixed inset-0 bg-black/50" />
    <DialogContent class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
      <DialogTitle>标题</DialogTitle>
      <DialogDescription>描述文字</DialogDescription>
      <!-- 内容 -->
      <DialogClose as-child>
        <Button variant="ghost"><X class="h-4 w-4" /></Button>
      </DialogClose>
    </DialogContent>
  </DialogPortal>
</DialogRoot>
```

**键盘导航**：确保所有交互可通过 Tab / Enter / Escape 操作。

---

### Step 12 — 代码质量检查清单

生成代码前自检：

- [ ] 所有 props 有明确类型，无 `any`
- [ ] Zod schema 覆盖所有 API 输入/输出
- [ ] 异步操作有 loading / error 状态处理
- [ ] 列表渲染使用唯一稳定 `:key`（非 index）
- [ ] 表单有完整验证和错误提示
- [ ] 响应式设计覆盖 mobile / tablet / desktop
- [ ] 重要操作（删除）有确认步骤
- [ ] 空状态、加载态、错误态三态齐全

---

## 快速参考

- 架构与工程规范 → `references/architecture.md`
- 组件库使用模式 → `references/components.md`
- 复杂表单场景 → `references/forms.md`
- SaaS 页面完整示例 → `references/page-patterns.md`
- 测试规范 → `references/testing.md`
