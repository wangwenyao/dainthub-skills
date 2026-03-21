# Vue SaaS Frontend Skill

SaaS 级 Vue 3.5+ / TypeScript 5.7+ 前端开发技能，为 AI 辅助编程提供规范化的开发指导。

## 📖 项目简介

本技能是一套完整的 Vue 3 前端开发规范定义，用于指导 AI 助手进行规范化的 SaaS 管理后台开发。覆盖组件开发、页面构建、状态管理、表单处理、数据表格等核心场景。

## 🛠 技术栈

| 类别 | 选型 | 版本 |
|------|------|------|
| **Core** | Vue 3 + TypeScript | 3.5+ / TS 5.7+ |
| **Build** | Vite | 6 |
| **Styling** | Tailwind CSS + CVA | 4 |
| **UI** | Shadcn-vue + Radix Vue | — |
| **State** | Pinia 3 + TanStack Query | — |
| **Forms** | FormKit + Zod | — |
| **Testing** | Vitest + Playwright | — |

## 📁 项目结构

```
vue-saas-frontend/
├── SKILL.md                      # 技能主文件（触发条件、工作流、质量门控）
└── references/                   # 参考文档目录
    ├── components-guide.md       # 组件开发指南（分层、模式、扩展、文档）
    ├── route-config.md           # 路由配置规范
    ├── config-center.md          # 配置中心规范
    ├── feature-flags.md          # 功能开关规范
    ├── ui-config.md              # UI 配置规范（表格、表单）
    ├── utils.md                  # 工具函数规范
    └── compatibility.md          # 浏览器兼容性规范
```

## 🚀 适用场景

使用此技能当：
- 开发 Vue 3 组件（UI 组件、业务组件、布局组件）
- 构建 SaaS 管理后台页面
- 使用 shadcn-vue 组件库
- 开发数据表格（带分页、筛选、排序）
- 开发复杂表单（验证、联动、多步骤）
- 状态管理（TanStack Query 服务端状态、Pinia 客户端状态）

不使用此技能当：
- React 项目开发
- 纯 CSS/样式设计（使用 `saas-design-system` skill）
- 后端 API 开发
- 移动端开发（React Native / Flutter）

## 📋 核心规范速查

### 输入参数

| 参数 | 说明 | 获取方式 |
|------|------|---------|
| **输出粒度** | `component` / `page` / `module` | 从用户描述推断 |
| **组件层级** | `ui` / `common` / `business` / `layout` | 从组件用途推断 |
| **页面类型** | `list` / `detail` / `form` / `dashboard` / `auth` / `settings` | 若涉及页面则询问 |
| **状态策略** | `server-state` / `client-state` / `local` | 默认 `server-state` |

### 输出清单

| 输出类型 | 产出文件 |
|---------|---------|
| `component` | .vue 文件 + types.ts（如有）+ __tests__/*.spec.ts |
| `page` | Page.vue + composables/*.ts + _components/*.vue |
| `module` | pages/ + composables/ + services/ + types/ |

### 约束体系

本技能包含 **32 条 ID 化约束**，分为 6 大类：

| 类别 | 前缀 | 数量 | 说明 |
|------|------|------|------|
| 组件约束 | C-COMP-xxx | 10 | 组件分层、依赖方向、禁止事项 |
| 状态管理约束 | C-STATE-xxx | 4 | TanStack Query / Pinia 使用规范 |
| TypeScript 约束 | C-TS-xxx | 4 | 类型定义、泛型语法、Zod 验证 |
| 样式约束 | C-STYLE-xxx | 3 | Tailwind CSS、类名合并、图标尺寸 |
| 路由约束 | C-ROUTE-xxx | 6 | 路由配置、缓存策略、权限控制 |
| 表格/表单约束 | C-FORM-xxx | 5 | 数据表格、表单验证、渲染规范 |

> 详细约束内容见 `SKILL.md` 约束总表章节。

### 组件分层

| 层级 | 用途 | 示例 |
|------|------|------|
| `ui/` | shadcn-vue 基础组件 | Button, Input |
| `common/` | 跨模块复用 | PageHeader, EmptyState |
| `business/` | 领域专用 | UserCard, OrderForm |
| `layout/` | 页面骨架 | DashboardLayout |

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

### 状态管理策略

| 状态类型 | 方案 | 说明 |
|---------|------|------|
| 服务端状态 | TanStack Query | 缓存、重试、同步 |
| 客户端状态 | Pinia Setup Store | 用户偏好、UI 状态 |

### 质量门控

```
生成前检查：
□ Props 有明确类型，无 any
□ API 有 Zod schema
□ 异步有 loading/error 状态
□ 列表用稳定 :key
□ 三态齐全（空/加载/错误）

生成后验证：
□ pnpm typecheck 通过
□ pnpm lint 无错误
□ pnpm test 全通过
```

## 🔗 配合使用

| 需求 | 使用技能 |
|------|---------|
| 设计规范（颜色/字体/间距） | `saas-design-system` |
| 后端 API 开发 | `java-backend-dev` |

## 📄 许可证

本项目仅供内部开发参考使用。