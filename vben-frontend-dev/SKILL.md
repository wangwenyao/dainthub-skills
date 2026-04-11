---
name: vben-frontend-dev
description: |
  Vben Admin 5.x 前端页面开发（Vue 3 + Vite + VxeGrid + VbenForm）。
  触发：列表页/表单页/详情页/主题配置/路由配置/Vben组件/VxeGrid表格/VbenModal弹窗/VbenDrawer抽屉。
  不适用：非Vben框架、纯后端、React/Angular项目、纯样式设计。
---

# Vben Admin 前端开发技能

## 概述

指导 AI 开发者使用 Vben Admin 5.x 框架构建标准化前端页面。确保代码模式一致、组件使用规范、架构可维护。

<HARD-GATE>
遇到不熟悉的场景时，务必先读取知识库文档。禁止猜测组件 API 或模式。
</HARD-GATE>

## 何时使用

**触发此技能的场景：**
- 创建新页面（列表、详情、表单）
- 使用 VbenForm、VxeGrid、Modal 组件
- 配置主题或布局
- 添加路由或权限
- 任何 Vue 3 + Vben Admin 前端开发工作

不适用：
- 非 Vben 框架项目
- 纯后端、React/Angular 项目
- 纯样式设计

---

## 技术栈

| 分层 | 技术 |
|------|------|
| 框架 | Vue 3 · Vben Admin 5.x · Vite |
| UI | VbenForm · VxeGrid · VbenModal · VbenDrawer |
| 样式 | Tailwind CSS · 自定义主题 |
| 状态 | Pinia · TanStack Query |
| 表单 | Schema 驱动 · Zod 验证 |

---

## 输入参数

| 参数 | 说明 | 优先级 |
|------|------|--------|
| **yaml_page_spec** | YAML 页面规格（从 PRD 提取） | 最高（直接读取） |
| **html_wireframe** | HTML+CSS 线框图 | 中等（解析 class → Schema） |
| **task_type** | `new_page` / `field_change` / `theme_config` / `route_add` / `modal_add` | 最低（推断） |
| **page_type** | `list` / `form` / `detail` / `dashboard` | 最低（推断） |
| **project_root** | Vben 项目根目录 | 从当前工作目录推断 |

### 输入优先级

```
YAML 页面规格 > HTML 线框图 > 关键词推断
```

> YAML→Schema 转换、HTML 线框图解析详细规则 → `references/07-input-parsing.md`

### task_type 优先级

```
new_page > route_add > theme_config > modal_add > field_change
```

### 组合场景

| 请求 | 类型 | 输出 |
|------|------|------|
| "新建商品列表页" | `new_page` (list) | index.vue + data.ts + modules/form.vue + api |
| "修改主题颜色" | `theme_config` | preferences.ts + tailwind.config.mjs |
| "添加用户管理路由" | `route_add` | router/routes/modules/*.ts |
| "修改表格列定义" | `field_change` | data.ts |

---

## 项目结构

```
{project_root}/
├── apps/web-antd/
│   ├── src/
│   │   ├── views/                     # 页面目录
│   │   ├── api/                       # API 定义
│   │   └── preferences.ts             # 主题/布局配置
│   └── tailwind.config.mjs            # Tailwind 扩展
└── packages/
    ├── @core/ui-kit/shadcn-ui/        # UI 组件库
    └── effects/plugins/vxe-table/     # 表格组件
```

## 页面开发模式

### 标准结构

```
views/module/feature/
├── index.vue           # 主页面（列表/详情）
├── data.ts             # Schema 定义
└── modules/
    └── form.vue        # 表单弹窗
```

### 开发流程

1. **定义 Schema** → `data.ts`（表单 schema、列定义）
2. **创建 API** → `api/module/feature.ts`（CRUD 函数）
3. **构建列表页** → `index.vue`（VxeGrid + 搜索表单）
4. **构建表单弹窗** → `modules/form.vue`（VbenForm + VbenModal）
5. **添加路由** → `router/routes/modules/`（如果是新页面）
6. **测试验证** → 检查渲染、验证、API 调用

## 核心组件速查

| 组件 | 用途 | 关键 API | 详细文档 |
|------|------|---------|---------|
| `useVbenForm` | Schema 驱动表单 | `formApi.getValues()` / `validate()` / `resetForm()` | `references/02-form.md` |
| `useVbenVxeGrid` | 搜索+表格 | `gridApi.query()` / `reload()` / `getSelectRows()` | `references/03-grid.md` |
| `useVbenModal` | 弹窗 | `formModalApi.setData()` / `.open()` / `.close()` | `references/04-modal.md` |

> **强制规则**：实现前必须读取对应 references 文档，禁止猜测 API。

## 常用表单组件

| 组件 | 用途 | 关键属性 |
|------|------|---------|
| `Input` | 文本输入 | `placeholder`, `allowClear` |
| `InputPassword` | 密码输入 | `passwordStrength` |
| `Select` | 下拉选择 | `options`, `mode='multiple'` |
| `ApiSelect` | 远程选择 | `api`, `labelField`, `valueField` |
| `ApiTreeSelect` | 树形选择 | `api`, `childrenField` |
| `RadioGroup` | 单选按钮 | `options`, `optionType='button'` |
| `DatePicker` | 日期选择 | `format`, `showTime` |
| `RangePicker` | 日期范围 | `format`, `allowClear` |
| `Upload` | 文件上传 | `accept`, `multiple` |

## 验证规则

| 规则 | 用法 |
|------|------|
| 内置 | `rules: 'required'` / `rules: 'mobile'` |
| Zod | `rules: z.string().min(2, '至少2个字符')` |
| 邮箱 | `rules: z.string().email('邮箱格式不正确')` |
| 范围 | `rules: z.number().min(0).max(100)` |

## UI 设计约束

内置约束自动应用，无需显式调用 UI 设计 skill：

| 约束 | 说明 |
|------|------|
| 主题色格式 | 必须使用 `hsl()` 格式 |
| 主色占比 | ≤ 5%（按钮、选中态等） |
| 禁止渐变 | 不使用渐变背景 |
| 禁止自定义阴影 | 使用框架预设 `shadow-*` |
| 间距栅格 | 4px 基准 |

线框图输入时，灰色样式只是结构示意，生成代码使用框架默认样式。

---

## 与测试 Skill 协作

开发阶段与全局测试 skill 协作确保代码质量：

| 开发阶段 | 调用测试能力 | 目的 |
|---------|-------------|------|
| **组件开发前** | `test-driven-development` | 先写测试，定义组件行为 |
| **组件开发后** | `test-generation` | 覆盖分析，补充交互测试 |
| **页面流程测试** | `test-generation` | E2E 测试关键用户流程 |

> 测试协作详细规范 → `../docs/shared/testing-collaboration.md`
> 测试命名/结构/Mock 规范 → `references/05-page-patterns.md`

### 测试覆盖率标准

| 测试类型 | 覆盖率目标 |
|---------|-----------|
| 业务组件 | ≥ 70% |
| Composables | ≥ 80% |
| 关键用户流程 | E2E 100% 覆盖 |

---

## 约束总表

### 架构约束 (C-VBEN-ARCH)

| ID | 规则 |
|----|------|
| C-VBEN-ARCH-001 | Grid `proxyConfig.ajax.query` 必须返回 `{ list: [], total: 0 }` 格式 |
| C-VBEN-ARCH-002 | VbenForm schema 必须在 `data.ts` 文件中定义，禁止组件内内联 |
| C-VBEN-ARCH-003 | Modal 必须设置 `destroyOnClose: true` 防止状态残留 |
| C-VBEN-ARCH-004 | API 函数必须在 `api/module/` 目录下定义，禁止组件内直接调用 `defHttp` |
| C-VBEN-ARCH-005 | 路由定义必须在 `router/routes/modules/` 目录下，禁止动态修改路由表 |

### 代码规范 (C-VBEN-CODE)

| ID | 规则 |
|----|------|
| C-VBEN-CODE-001 | 禁止修改 `packages/@core/ui-kit/shadcn-ui/` 源码 |
| C-VBEN-CODE-002 | 表格列定义必须配置 `rowConfig.keyField` 作为行唯一标识 |
| C-VBEN-CODE-003 | 表单验证必须使用 `rules` 字符串规则或 Zod schema |
| C-VBEN-CODE-004 | 删除操作必须有 `popConfirm` 二次确认 |
| C-VBEN-CODE-005 | 异步操作必须有 loading 状态显示 |

### 组件使用 (C-VBEN-COMP)

| ID | 规则 |
|----|------|
| C-VBEN-COMP-001 | ApiSelect 必须配置 `api` + `labelField` + `valueField` |
| C-VBEN-COMP-002 | DatePicker 必须配置 `format` 属性 |
| C-VBEN-COMP-003 | RadioGroup 使用 `optionType='button'` 时必须提供 `options` |
| C-VBEN-COMP-004 | Upload 组件必须配置 `accept` 限制文件类型 |

---

## 按需加载指引

| 任务类型 | 推荐读取 | 内容 |
|---------|---------|------|
| 输入解析 | `references/07-input-parsing.md` | YAML→Schema、HTML 线框图解析 |
| 开发表单 | `references/02-form.md` | VbenForm 完整 API、schema 配置 |
| 开发列表页 | `references/03-grid.md` → `02-form.md` | VxeGrid 完整 API、列定义 |
| 新建页面 | `references/05-page-patterns.md` | 完整页面模板（列表/表单/详情） |
| 配置主题 | `references/01-configuration.md` | 主题/布局/功能配置 |
| 添加路由 | `references/06-routing.md` | 路由定义、权限配置 |
| 开发弹窗 | `references/04-modal.md` | Modal/Drawer API |

## 协同开发文档

| 场景 | 文档 |
|------|------|
| git pull / 拉取同步 | `../docs/collaboration/06-sync-flow.md` |
| 协同开发概述 | `../docs/collaboration/01-overview.md` |
| 项目目录结构 | `../docs/collaboration/02-project-structure.md` |
| 前端工程结构 | `../docs/collaboration/03-frontend-backend.md` |
| status.md / 归档 | `../docs/collaboration/05-status-mechanism.md` |

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 主题色未生效 | 清除浏览器缓存/localStorage |
| 表格数据不显示 | 确保 API 返回 `{ list: [], total: 0 }` |
| 表单验证失败 | 检查 `rules` 和 `dependencies` 配置 |
| 弹窗无法关闭 | 确保调用了 `await modalApi.close()` |

---

## 输出清单

| task_type | 输出文件 | 必要性 |
|-----------|---------|--------|
| `new_page` (list) | views/module/feature/index.vue + data.ts + modules/form.vue + api/module/feature.ts | 全部必需 |
| `new_page` (form/detail) | views/module/feature/index.vue + data.ts + api/module/feature.ts | 全部必需 |
| `new_page` (dashboard) | views/module/feature/index.vue + api/module/feature.ts | 全部必需 |
| `theme_config` | preferences.ts + tailwind.config.mjs（如需扩展） | preferences.ts 必需 |
| `route_add` | router/routes/modules/*.ts | 路由文件必需 |
| `modal_add` | modules/*.vue + 父页面集成代码 | modal 文件必需 |
| `field_change` | data.ts + api/*.ts（如有接口参数变更） | 视具体字段 |

**输出验证**: 每个输出文件必须通过 TypeScript 类型检查，无 `any` 类型。

## 检查清单

完成工作前确认：

- [ ] Schema 已在 `data.ts` 中定义
- [ ] API 函数遵循规范模式
- [ ] 表格返回正确格式
- [ ] 表单验证工作正常
- [ ] 弹窗正常打开/关闭
- [ ] 路由已添加（如果是新页面）
- [ ] 权限已设置（如需要）
- [ ] 无 TypeScript 错误
- [ ] 页面正确渲染

---

## 版本

- v3.0
- 更新: 2026-04-11
- 变更: SKILL.md 瘦身，提取输入解析到 references/07-input-parsing.md，测试协作引用共享文档
