---
name: vue-saas-frontend
description: >
  Vue 3.5+ / TypeScript 5.7+ / Tailwind CSS 4 / Shadcn-vue 前端开发。
  触发：Vue组件/SaaS页面/管理页面/列表查询页面/图表页面/shadcn/数据表格/表单/仪表盘/TanStack Query/Pinia。
  不含后端。
---

# Vue SaaS Frontend 开发 Skill

> **设计规范**：颜色/字体/间距/交互/视觉层级 → 参考 `saas-design-system` skill

## 何时使用

适用场景：
- Vue 3 组件开发（UI 组件、业务组件、布局组件）
- SaaS 管理后台页面（数据表格、表单、仪表盘）
- shadcn-vue 组件库使用
- 状态管理（TanStack Query、Pinia）

不适用：
- React 项目
- 纯 CSS/样式设计（用 `saas-design-system` skill）
- 后端 API 开发
- 移动端开发

## 前置条件

- 项目使用 Vue 3.5+
- 已安装 Node.js 18+

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
需求分析
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

---

## 与测试 Skill 协作

前端开发阶段调用测试能力确保组件质量：

| 开发阶段 | 调用测试能力 | 目的 |
|---------|-------------|------|
| **组件开发前** | `test-driven-development` | 先写测试，定义组件行为 |
| **组件开发后** | `test-generation` | 覆盖分析，补充交互测试 |
| **页面流程测试** | `test-generation` | E2E 测试关键用户流程 |

### 测试规范参考

测试详细规范 → `references/testing.md`，包含：
- 组件测试模板（Vitest + Vue Test Utils）
- Composable 测试
- Store 测试
- E2E 测试（Playwright）

### 开发流程集成测试

```
开发业务组件：
Step 1: 设计组件 Props/Events
Step 2: TDD 先写测试 → test-driven-development
        - 测试 Props 传递
        - 测试 Events 触发
        - 测试状态变化
Step 3: 实现组件 → components/business/*.vue
Step 4: 补充测试 → test-generation + testing.md
        - 边缘情况（空数据、错误状态）
        - 异步操作测试
```

### 测试覆盖率标准

| 测试类型 | 覆盖率目标 |
|---------|-----------|
| 业务组件 | ≥ 70% |
| Composables | ≥ 80% |
| Stores | ≥ 80% |
| 关键用户流程 | E2E 100%覆盖 |

### PRD 验收标准转化为测试

```
PRD验收标准：
Given 用户在用户列表页
When 搜索"张三"
Then 显示匹配的用户行

转化为 E2E 测试（参考 testing.md）：
test('用户搜索流程', async ({ page }) => {
    // Given
    await page.goto('/users');
    
    // When
    await page.getByPlaceholder('搜索').fill('张三');
    
    // Then
    await expect(page.getByRole('row', { name: /张三/ })).toBeVisible();
});
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

| 参数 | 说明 | 默认推断规则 |
|------|------|-------------|
| **输出粒度** | `component` / `page` / `module` | 单组件→component，含页面词→page，多模块→module |
| **组件层级** | `ui` / `common` / `business` / `layout` | shadcn基础→ui，跨模块复用→common，领域专用→business |
| **页面类型** | `list` / `detail` / `form` / `dashboard` / `auth` / `settings` | 从需求推断 |
| **状态策略** | `server-state` / `client-state` / `local` | 服务端数据→server-state，UI状态→local |

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

> 执行任务时必须遵守。完整约束见各 references 文件。

### 组件约束 (C-COMP)

| ID | 约束 |
|----|------|
| C-COMP-001 | 禁止修改 `ui/` 目录下的 shadcn-vue 源码 |
| C-COMP-002 | 依赖方向：`business → common → ui`，禁止反向 |
| C-COMP-003~005 | ui/不依赖common/business/，禁止硬编码业务文案 |
| C-COMP-006~010 | 禁止 Mixins/Filters/$on/$off，禁止直接修改 props |

### 状态约束 (C-STATE)

| ID | 约束 |
|----|------|
| C-STATE-001 | 服务端状态用 TanStack Query |
| C-STATE-002 | 客户端状态用 Pinia Setup Store |
| C-STATE-003~004 | 禁止 computed 中修改状态，异步必有 loading/error |

### TypeScript 约束 (C-TS)

| ID | 约束 |
|----|------|
| C-TS-001 | 禁止 `any` 类型 |
| C-TS-002~003 | Props/Emits 用泛型语法 |
| C-TS-004 | API 响应有 Zod schema |

### 样式约束 (C-STYLE)

| ID | 约束 |
|----|------|
| C-STYLE-001 | 禁止内联样式，用 Tailwind |
| C-STYLE-002 | 用 `cn()` 合并类名 |
| C-STYLE-003 | 图标尺寸：按钮 h-4 w-4，导航 h-5 w-5 |

### 路由约束 (C-ROUTE)

| ID | 约束 |
|----|------|
| C-ROUTE-001 | 用 `defineOptions({ name })` 定义组件名 |
| C-ROUTE-002~006 | meta 仅原始类型，禁止动态改路由，缓存≤10页 |

### 表格/表单约束 (C-FORM)

| ID | 约束 |
|----|------|
| C-FORM-001~005 | render 同步，禁止 index 作 rowKey，必有 loading，验证用 Zod |

> 详细约束说明 → `references/components-guide.md`

---

## 快速参考

### 参考文档加载优先级

1. **必须加载**（涉及核心约束）：`components-guide.md`
2. **按需加载**：
   - 数据表格/表单 → `ui-config.md`
   - 页面开发 → `page-patterns.md`
   - 路由配置 → `route-config.md`
   - 测试编写 → `testing.md`
3. **可选加载**：`compatibility.md`, `feature-flags.md`, `config-center.md`

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

### 错误处理
| 文档 | 内容 |
|------|------|
| `error-handling.md` | API 错误、表单验证、全局异常处理 |