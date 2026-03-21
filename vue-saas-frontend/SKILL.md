---
name: vue-saas-frontend
description: >
  SaaS 级 Vue 3.5+/TypeScript 5.7+ 前端开发技能。当用户需要使用 Vue 3、TypeScript、Tailwind CSS、Shadcn-vue、Pinia、TanStack Query 等技术栈开发前端页面、UI 组件、SaaS 仪表盘、数据表格、复杂表单时触发。触发词：Vue 组件、SaaS 页面、shadcn、数据表格、表单、仪表盘。
license: MIT
compatibility:
  - Claude Code
  - OpenCode
  - Cursor
  - Codex
metadata:
  author: dainthub
  version: "1.0"
  tags: vue, typescript, frontend, saas, shadcn-vue, tanstack-query
---

# Vue SaaS Frontend 开发 Skill

> **设计规范**：颜色/字体/间距/交互/视觉层级 → 参考 `saas-design-system` skill

## 何时使用

| 场景 | 示例请求 |
|------|----------|
| 开发 Vue 3 组件 | "帮我写个用户卡片组件" |
| 构建 SaaS 页面 | "做一个用户管理列表页" |
| 使用 shadcn-vue | "用 shadcn 的 Table 组件" |
| 数据表格开发 | "带分页筛选的数据表格" |
| 表单开发 | "用户注册表单" |
| 状态管理 | "用 TanStack Query 获取用户列表" |

## 何时不使用

| 场景 | 应使用 |
|------|--------|
| React 项目 | React 相关 skill |
| 纯 CSS/样式设计 | `saas-design-system` skill |
| 后端 API 开发 | 后端相关 skill |
| 移动端开发 | React Native / Flutter skill |
| 静态网站 | Astro / Next.js skill |

## 前置条件

- [ ] 项目使用 Vue 3.5+
- [ ] 已安装 Node.js 18+
- [ ] 已初始化 pnpm/npm 项目

## 技术栈

| 类别 | 选型 | 版本 |
|------|------|------|
| Core | Vue 3 + TypeScript | 3.5+ / TS 5.7+ |
| Build | Vite | 6 |
| Styling | Tailwind CSS + CVA | 4 |
| UI | Shadcn-vue + Radix Vue | — |
| State | Pinia 3 + TanStack Query | — |
| Forms | FormKit + Zod | — |
| Testing | Vitest + Playwright | — |

---

## 开发决策流程

```
用户请求
    │
    ├─ 判断输出粒度
    │   ├── 单个组件 → Step 2 → components-guide.md
    │   ├── 完整页面 → Step 3 → page-patterns.md
    │   └── 多页面模块 → Step 1 (项目结构)
    │
    ├─ 判断页面类型
    │   ├── 数据表格 → ui-config.md#表格
    │   ├── 表单页 → ui-config.md#表单
    │   ├── 仪表盘 → page-patterns.md#仪表盘
    │   ├── 认证页 → page-patterns.md#认证
    │   └── 设置页 → page-patterns.md#设置
    │
    └─ 质量门控 → Step 5 检查清单
```

---

## Step 1 — 项目结构

```
src/
├── components/
│   ├── ui/              # shadcn-vue 组件
│   ├── common/          # 通用业务组件
│   └── business/        # 领域组件
├── composables/         # 组合式函数
├── pages/               # 路由页面
├── stores/              # Pinia stores
├── services/            # API 层
└── types/               # TypeScript 类型
```

> 详细结构 → `references/architecture.md`

---

## Step 2 — 组件开发

### SFC 结构顺序
```
1. 外部 import
2. Props / Emits 定义
3. Composables / Stores
4. 响应式状态
5. Computed
6. 方法
7. 生命周期
```

### 组件分层
| 层级 | 用途 | 示例 |
|------|------|------|
| `ui/` | shadcn-vue 基础组件 | Button, Input |
| `common/` | 跨模块复用 | PageHeader, EmptyState |
| `business/` | 领域专用 | UserCard, OrderForm |
| `layout/` | 页面骨架 | DashboardLayout |

> 组件模式/扩展机制/文档规范 → `references/components-guide.md`

---

## Step 3 — 页面模式

| 页面类型 | 关键组件 | 状态策略 |
|----------|----------|----------|
| 数据表格 | DataTable + 分页 + 筛选 | TanStack Query + URL 同步 |
| 表单页 | Form + 验证 | Query + Mutation |
| 仪表盘 | Cards + Charts | 多 Query 并行 |
| 认证页 | Form + 步骤 | Local state + Pinia |
| 设置页 | Tabs + Form | 乐观更新 |

> 完整示例 → `references/page-patterns.md`

---

## Step 4 — 核心规范速查

### TypeScript
- Props: `defineProps<T>()` 泛型语法
- Emits: `defineEmits<{ (e: 'event', payload: T): void }>()`
- API: Zod schema + 类型推导

### 状态管理
- **服务端状态**: TanStack Query（缓存、重试、同步）
- **客户端状态**: Pinia Setup Store 风格

### 样式规范
- 使用 `cn()` 合并类名
- 图标尺寸: 按钮 `h-4 w-4`，导航 `h-5 w-5`

> 详细规范 → `references/components-guide.md`

---

## Step 5 — 质量门控

### 代码生成前检查
- [ ] Props 有明确类型，无 `any`
- [ ] API 有 Zod schema
- [ ] 异步有 loading/error 状态
- [ ] 列表用稳定 `:key`
- [ ] 三态齐全（空/加载/错误）

### 代码生成后验证
```bash
# 类型检查
pnpm typecheck

# Lint 检查  
pnpm lint

# 单元测试
pnpm test
```

### PR 前
- [ ] `typecheck` 通过
- [ ] `lint` 无错误
- [ ] `test` 全通过
- [ ] 新代码有测试

---

## 自定义配置

支持不修改 SKILL.md 的个性化配置：

### 项目级
创建 `.skill-memories/vue-saas-frontend.md`：
```markdown
# 项目偏好

## 表单库
使用 React Hook Form 替代 FormKit

## 状态管理
大型项目用 Zustand，小型用 Pinia
```

### 个人级
创建 `~/.skill-memories/vue-saas-frontend.md`：
```markdown
# 个人偏好

## 注释风格
使用 JSDoc 注释
```

---

## 输入参数

执行前端开发任务时，需要确定以下参数：

| 参数 | 说明 | 获取方式 |
|------|------|---------|
| **输出粒度** | `component` / `page` / `module` | 从用户描述推断 |
| **组件层级** | `ui` / `common` / `business` / `layout` | 从组件用途推断 |
| **页面类型** | `list` / `detail` / `form` / `dashboard` / `auth` / `settings` | 若涉及页面则询问 |
| **状态策略** | `server-state` / `client-state` / `local` | 默认 `server-state` |

---

## 输出清单

| 输出类型 | 产出文件 |
|---------|---------|
| `component` | .vue 文件 + types.ts（如有）+ __tests__/*.spec.ts |
| `page` | Page.vue + composables/*.ts + _components/*.vue |
| `module` | pages/ + composables/ + services/ + types/ |

---

## 与 saas-design-system 协作

本技能负责"代码怎么写"，`saas-design-system` 技能负责"设计长什么样"。

### Token 映射

| 设计 Token | Tailwind Class | 使用场景 |
|-----------|---------------|---------|
| `--color-brand-500` | `bg-primary` | 主按钮背景（交互锚点） |
| `text-sm`（13px） | `text-sm` | UI 默认字号 |
| `text-base`（15px） | `text-base` | 正文、表单输入 |
| `space-4`（16px） | `p-4` / `gap-4` | 标准间距 |
| `space-6`（24px） | `p-6` | 卡片内边距 |
| `border-default` | `border-border` | 通用分割线 |
| `bg-elevated` | `bg-card` | 卡片背景 |
| `bg-sunken` | `bg-muted` | 输入框背景 |

### 设计约束引用

编写组件时，需遵循 `saas-design-system` 定义的设计约束：

| 领域 | 约束范围 | 关键规则 |
|------|---------|---------|
| 色彩 | C-COLOR-001~007 | 主色占比≤5%，禁止渐变 |
| 排版 | C-TYPE-001~007 | UI 默认 13px，行高≥1.5 |
| 间距 | C-SPACE-001~003 | 4px 栅格 |
| 交互 | C-INTERACT-001~008 | 主按钮≤1，动画≤200ms |

### 协作流程

1. 设计决策（配色、间距、组件选型）→ 使用 `saas-design-system` skill
2. 代码实现（Vue 组件、状态管理、路由）→ 使用本 skill
3. 两者冲突时，以 `saas-design-system` 的设计约束为准

---

## 约束总表

> 从 `references/` 文档中提取的 ID 化约束，执行任务时必须遵守。

### 组件约束 C-COMP-xxx

| ID | 约束 | 来源 |
|----|------|------|
| C-COMP-001 | 禁止修改 `ui/` 目录下的 shadcn-vue 源码，升级时会丢失修改 | components-guide.md |
| C-COMP-002 | 组件依赖方向：`business → common → ui`，禁止反向依赖 | components-guide.md |
| C-COMP-003 | 禁止 `ui/` 组件依赖 `common/` 或 `business/` | components-guide.md |
| C-COMP-004 | 禁止 `common/` 组件依赖 `business/` | components-guide.md |
| C-COMP-005 | 禁止在 `ui/` 组件中硬编码业务文案，应通过 props 传入 | components-guide.md |
| C-COMP-006 | 禁止使用 Mixins，应使用 Composables | components-guide.md |
| C-COMP-007 | 禁止使用 Filters（Vue 3 已移除），应使用 computed 或方法 | components-guide.md |
| C-COMP-008 | 禁止使用 `$on/$off`（已移除），应使用 mitt 或 useEventBus | components-guide.md |
| C-COMP-009 | 禁止直接修改 props，应使用 emit 或 v-model | components-guide.md |
| C-COMP-010 | 禁止 provide/inject 跨模块传递业务数据，禁止超过 3 层嵌套 | components-guide.md |

### 状态管理约束 C-STATE-xxx

| ID | 约束 | 来源 |
|----|------|------|
| C-STATE-001 | 服务端状态必须使用 TanStack Query（缓存、重试、同步） | architecture.md |
| C-STATE-002 | 客户端状态必须使用 Pinia Setup Store 风格 | architecture.md |
| C-STATE-003 | 禁止在 computed 中修改状态 | SKILL.md |
| C-STATE-004 | 异步操作必须有 loading/error 状态处理 | SKILL.md |

### TypeScript 约束 C-TS-xxx

| ID | 约束 | 来源 |
|----|------|------|
| C-TS-001 | 禁止使用 `any` 类型，必须明确类型定义 | components-guide.md |
| C-TS-002 | Props 必须使用 `defineProps<T>()` 泛型语法 | SKILL.md |
| C-TS-003 | Emits 必须使用 `defineEmits<{ (e: 'event', payload: T): void }>()` 类型签名 | SKILL.md |
| C-TS-004 | API 响应必须有 Zod schema 进行类型推导和验证 | SKILL.md |

### 样式约束 C-STYLE-xxx

| ID | 约束 | 来源 |
|----|------|------|
| C-STYLE-001 | 禁止内联样式，必须使用 Tailwind CSS 工具类 | SKILL.md |
| C-STYLE-002 | 使用 `cn()` 合并类名，避免类名冲突 | SKILL.md |
| C-STYLE-003 | 图标尺寸规范：按钮内 `h-4 w-4`，导航内 `h-5 w-5` | SKILL.md |

### 路由约束 C-ROUTE-xxx

| ID | 约束 | 来源 |
|----|------|------|
| C-ROUTE-001 | 禁止在路由组件中使用匿名函数定义 name，必须使用 `defineOptions({ name: 'xxx' })` | route-config.md |
| C-ROUTE-002 | 禁止在 meta 中存储大对象或函数，仅限原始类型 | route-config.md |
| C-ROUTE-003 | 禁止动态修改路由配置，应通过权限控制显示 | route-config.md |
| C-ROUTE-004 | 禁止在 beforeEach 中执行异步操作不加 loading 状态 | route-config.md |
| C-ROUTE-005 | 禁止缓存页面超过 10 个，影响内存性能 | route-config.md |
| C-ROUTE-006 | 禁止使用 path 作为缓存 key，必须使用组件 name | route-config.md |

### 表格/表单约束 C-FORM-xxx

| ID | 约束 | 来源 |
|----|------|------|
| C-FORM-001 | 禁止在 render 函数中使用 async，渲染函数必须同步返回 | ui-config.md |
| C-FORM-002 | 禁止直接修改 props.data，违反单向数据流 | ui-config.md |
| C-FORM-003 | 禁止使用 index 作为 rowKey，分页时选中状态错乱 | ui-config.md |
| C-FORM-004 | 禁止忽略 loading 状态，易产生竞态问题 | ui-config.md |
| C-FORM-005 | 表单验证必须使用 Zod Schema | ui-config.md |

---

## 快速参考

### 核心规范
| 文档 | 内容 |
|------|------|
| `architecture.md` | 项目结构、路由、服务层 |
| `components-guide.md` | 组件分层、模式、扩展、文档 |
| `testing.md` | 单元测试 + E2E 测试 |

### 配置化
| 文档 | 内容 |
|------|------|
| `ui-config.md` | 表格配置 + 表单配置 |
| `route-config.md` | 路由、权限、面包屑 |
| `config-center.md` | API 配置、枚举、字典 |
| `feature-flags.md` | 功能开关、灰度发布 |

### 工具与兼容
| 文档 | 内容 |
|------|------|
| `utils.md` | 数据格式化工具函数 |
| `compatibility.md` | 浏览器兼容、版本迁移 |

### 页面模式
| 文档 | 内容 |
|------|------|
| `page-patterns.md` | 完整页面实现示例 |