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

---

## 输入参数

| 参数 | 说明 | 优先级 |
|------|------|--------|
| **yaml_page_spec** | YAML 页面规格（从 PRD 提取） | 最高（直接读取） |
| **html_wireframe** | HTML+CSS 线框图 | 中等（解析 class → Schema） |
| **task_type** | `new_page` / `field_change` / `theme_config` / `route_add` / `modal_add` | 最低（从关键词推断） |
| **page_type** | `list` / `form` / `detail` / `dashboard` | 最低（从关键词推断） |
| **component_type** | `VbenForm` / `VxeGrid` / `VbenModal` / `VbenDrawer` | 最低（从关键词推断） |
| **project_root** | Vben项目根目录 | 从当前工作目录推断 |

### 输入优先级

```
YAML 页面规格 > HTML 线框图 > 关键词推断
```

### YAML → Schema 转换

当输入包含 YAML 页面规格时，直接读取生成 Schema：

```typescript
// 读取 YAML 页面规格
const pageSpec = parseYaml(input.yaml_page_spec);

// 直接生成 Schema（无需推断）
// 搜索区 → formOptions.schema
const searchSchema = pageSpec.config.search.fields.map(f => ({
  fieldName: f.field,
  label: f.name,
  component: f.component,
  placeholder: f.placeholder,
}));

// 表格列 → gridOptions.columns
const tableColumns = pageSpec.config.table.columns.map(c => ({
  field: c.field,
  title: c.title,
  width: c.width,
  align: c.align,
  component: c.component,
}));

// 表单字段 → VbenForm schema
const formSchema = pageSpec.config.form.fields.map(f => ({
  fieldName: f.field,
  label: f.name,
  component: f.component,
  rules: f.required ? 'required' : undefined,
}));
```

### HTML 线框图解析

当输入包含 HTML+CSS 线框图时，解析 class → 组件映射：

```typescript
// 从 HTML class 推断组件
const classMap = {
  'field input': 'Input',
  'field select': 'Select',
  'field date': 'DatePicker',
  'field number': 'InputNumber',
  'field textarea': 'TextArea',
  'tag': 'Tag',
  'btn btn-primary': 'Button(primary)',
  'table': 'VxeGrid',
  'modal': 'VbenModal',
};

// 从占位文字提取字段名
// [商品名称] → fieldName: 'name', label: '商品名称'
const fieldName = html.match(/\[(.*?)\]/)?.[1];

// 从组件标注确认类型
// <div class="label">组件：搜索表单</div> → search area
const componentLabel = html.match(/组件：(\w+)/)?.[1];
```

### HTML class → 组件映射表

| HTML class | Vben 组件 | Schema 配置 |
|-----------|----------|-------------|
| `field input` | Input | `{ component: 'Input' }` |
| `field select` | Select / ApiSelect | `{ component: 'Select' }` |
| `field date` | DatePicker | `{ component: 'DatePicker' }` |
| `field number` | InputNumber | `{ component: 'InputNumber' }` |
| `field textarea` | TextArea | `{ component: 'TextArea' }` |
| `tag` | Tag | 列配置 `slots` |
| `btn btn-primary` | Button(primary) | 主按钮样式 |
| `btn` | Button(default) | 默认按钮样式 |
| `btn btn-danger` | Button(danger) | 删除按钮 |
| `table` | VxeGrid | `useVbenVxeGrid` |
| `modal` | VbenModal | `useVbenModal` |

### CSS 样式处理

**注意**：HTML 线框图的 CSS 样式是灰色示意，不是真实样式。

```css
/* 线框图 CSS - 不应用 */
.wireframe { border: 1px dashed #999; background: #f5f5f5; }
.field { border: 1px solid #999; background: #fff; color: #999; }
.btn-primary { background: #aaa; }  /* 灰色，不是真实主色 */

/* 真实样式 - 使用 Vben 框架默认或 saas-ui-design 约束 */
.btn-primary { 
  /* 使用框架默认样式，自动符合约束 */
}
```

线框图 CSS 只用于识别结构，不直接应用到生成的代码中。

### UI 约束应用

生成的代码自动应用内置约束（无需显式调用 saas-ui-design）：

| 约束 | 说明 |
|------|------|
| 主题色格式 | 必须使用 `hsl()` 格式 |
| 主色占比 | ≤ 5%（按钮、选中态等） |
| 禁止渐变 | 不使用渐变背景 |
| 禁止自定义阴影 | 使用框架预设 `shadow-*` |
| 间距栅格 | 4px 基准 |

---

## 开发流程（改进版）

### Step 0：读取输入（新增）

```typescript
// 检测输入类型
if (input.yaml_page_spec) {
  // YAML 直接读取
  pageType = parseYaml(input.yaml_page_spec).type;
  schema = generateSchemaFromYaml(input.yaml_page_spec);
} else if (input.html_wireframe) {
  // HTML 解析
  pageType = inferPageTypeFromHtml(input.html_wireframe);
  schema = generateSchemaFromHtml(input.html_wireframe);
} else {
  // 关键词推断（兜底）
  pageType = inferPageType(input.keywords);
}
```

### Step 1：定义 Schema

根据输入类型生成 Schema：
- YAML → 直接读取
- HTML → class 映射
- 关键词 → 推断

### task_type 优先级

```
new_page > route_add > theme_config > modal_add > field_change
```

### 组合场景

| 请求 | 类型 | 输出 |
|------|------|------|
| "新建商品列表页" | `new_page` (list) | index.vue + data.ts + modules/form.vue + api/module/feature.ts |
| "修改主题颜色" | `theme_config` | preferences.ts + tailwind.config.mjs |
| "添加用户管理路由" | `route_add` | router/routes/modules/*.ts |
| "修改表格列定义" | `field_change` | data.ts |

---

## 项目结构

```
{project_root}/                       # Vben Admin 5.x 项目（从当前工作目录推断）
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

**注意**: `{project_root}` 从当前工作目录推断。禁止硬编码绝对路径。

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

## 核心组件

### 1. VbenForm（Schema 驱动表单）

```typescript
import { useVbenForm } from '#/adapter/form';

const [Form, formApi] = useVbenForm({
  schema: [
    { fieldName: 'username', label: '用户名', component: 'Input', rules: 'required' },
    { fieldName: 'status', label: '状态', component: 'RadioGroup' },
  ],
});
```

**关键API**: `formApi.getValues()` / `formApi.validate()` / `formApi.resetForm()`

> 完整API文档 → `references/02-form.md`

### 2. VxeGrid（带搜索的表格）

```typescript
import { useVbenVxeGrid } from '#/adapter/vxe-table';

const [Grid, gridApi] = useVbenVxeGrid({
  formOptions: { schema: [...] },      // 搜索表单
  gridOptions: {
    columns: [...],                     // 列定义
    proxyConfig: { ajax: { query: async ({ page }) => { return { list, total } } } },
  },
});
```

**关键API**: `gridApi.query()` / `gridApi.reload()` / `gridApi.getSelectRows()`

> 完整API文档 → `references/03-grid.md`

### 3. VbenModal

```typescript
import { useVbenModal } from '@vben/common-ui';

const [FormModal, formModalApi] = useVbenModal({
  connectedComponent: () => import('./modules/form.vue'),
  destroyOnClose: true,
});

// 使用方式
formModalApi.setData({ id: 1 }).open();  // 编辑模式
formModalApi.setData(null).open();        // 创建模式
```

## 配置

### 主题与布局

```typescript
// apps/web-antd/src/preferences.ts
export const overridesPreferences = defineOverridesPreferences({
  theme: {
    colorPrimary: 'hsl(25 95% 54%)',  // Brand color
    mode: 'light',
    radius: '0.5',
  },
  app: {
    name: 'System Name',
    watermark: true,
    watermarkContent: 'Watermark Text',
  },
});
```

### 内置主题

| 主题 | 颜色 | 适用场景 |
|------|------|---------|
| `default` | 蓝色 | 通用 |
| `orange` | 橙色 | 接近 #FA8C16 |
| `green` | 绿色 | 医疗健康 |
| `zinc` | 灰色 | 专业商务 |
| `custom` | 自定义 | 品牌定制 |

## API 模式

```typescript
// api/module/feature.ts
import { defHttp } from '#/utils/http/axios';

export namespace FeatureApi {
  export interface Item { id?: number; name: string; status: number }
}

// 分页查询 - 必须返回 { list: [], total: 0 }
export function getFeaturePage(params: any) {
  return defHttp.get<{ list: FeatureApi.Item[]; total: number }>({ url: '/feature/page', params });
}

// CRUD 操作
export function createFeature(data: FeatureApi.Item) { /* ... */ }
export function updateFeature(data: FeatureApi.Item) { /* ... */ }
export function deleteFeature(id: number) { /* ... */ }
```

> 完整API模式示例 → `references/05-page-patterns.md`

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

```typescript
import { z } from '#/adapter/form';

// 内置规则
rules: 'required'
rules: 'mobile'

// Zod 规则
rules: z.string().min(2, '至少2个字符')
rules: z.string().email('邮箱格式不正确')
rules: z.number().min(0).max(100)
```

## UI 设计规范

### 设计原则

遵循 SaaS 专业克制设计风格（Linear/Notion风格），内置约束自动应用：

| 原则 | 说明 |
|------|------|
| **克制** | 不用渐变、不用装饰性插图 |
| **密度** | 信息密度优先于呼吸感 |
| **一致** | 相同行为用相同视觉语言 |
| **功能先行** | 颜色用于传达信息，而非装饰 |

### 内置约束

| 约束 | 说明 | 自动应用 |
|------|------|---------|
| 主题色格式 | 必须使用 `hsl()` 格式，禁止 hex | ✅ |
| 阴影规范 | 禁止自定义阴影，使用 `shadow-card` / `shadow-card-hover` / `shadow-card-elevated` | ✅ |
| 主色占比 | 页面主色占比≤5%，辅助强调色占比≤10%，中性色占比≥85% | ✅ |
| 禁止渐变 | 不使用渐变背景 | ✅ |

### 线框图输入说明

当输入是 HTML+CSS 线框图时：
- 线框图的灰色样式只是结构示意
- 生成的代码使用 Vben 框架默认样式
- 框架样式自动符合上述约束
- 不需要额外调用 UI 设计 skill

---

## 与测试 Skill 协作

前端开发阶段调用测试能力确保组件质量：

| 开发阶段 | 调用测试能力 | 目的 |
|---------|-------------|------|
| **组件开发前** | `test-driven-development` | 先写测试，定义组件行为 |
| **组件开发后** | `test-generation` | 覆盖分析，补充交互测试 |
| **页面流程测试** | `test-generation` | E2E 测试关键用户流程 |

### 前端测试规范

Vben Admin 5.x 使用 Vitest 进行组件测试：

| 测试类型 | 测试内容 | 文件位置 |
|---------|---------|---------|
| 组件测试 | Props、Events、渲染状态 | `__tests__/*.spec.ts` |
| Composable 测试 | 状态管理、数据获取逻辑 | `composables/__tests__/*.spec.ts` |
| E2E 测试 | 用户操作流程、页面跳转 | `e2e/*.spec.ts`（Playwright） |

### 开发流程集成测试

```
开发表单组件：
Step 1: 定义 schema → data.ts
Step 2: TDD 先写测试 → test-driven-development
        - 测试表单验证规则
        - 测试提交/取消事件
        - 测试 loading/error 状态
Step 3: 实现组件 → modules/form.vue
Step 4: 补充测试 → test-generation
        - 边缘情况（空值、边界值）
        - 异步操作测试
```

### 测试覆盖率标准

| 测试类型 | 覆盖率目标 |
|---------|-----------|
| 业务组件 | ≥ 70% |
| Composables | ≥ 80% |
| 关键用户流程 | E2E 100%覆盖 |

### PRD 验收标准转化为 E2E 测试

```
PRD验收标准：
Given 用户在商品列表页
When 点击新增按钮
Then 打开新增表单弹窗

转化为 Playwright 测试：
test('新增商品流程', async ({ page }) => {
    // Given
    await page.goto('/product/list');
    
    // When
    await page.click('[data-testid="add-btn"]');
    
    // Then
    await expect(page.locator('.vben-modal')).toBeVisible();
});
```

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
| C-VBEN-CODE-001 | 禁止修改 `packages/@core/ui-kit/shadcn-ui/` 源码，如需定制在 `apps/web-antd/src` 覆盖 |
| C-VBEN-CODE-002 | 表格列定义必须配置 `rowConfig.keyField` 作为行唯一标识 |
| C-VBEN-CODE-003 | 表单验证必须使用 `rules` 字符串规则或 Zod schema，禁止自定义验证函数 |
| C-VBEN-CODE-004 | 删除操作必须有 `popConfirm` 二次确认，禁止直接执行删除 |
| C-VBEN-CODE-005 | 异步操作必须有 loading 状态显示，禁止无反馈的异步执行 |

### 组件使用 (C-VBEN-COMP)

| ID | 规则 |
|----|------|
| C-VBEN-COMP-001 | ApiSelect 必须配置 `api` + `labelField` + `valueField` 三个属性 |
| C-VBEN-COMP-002 | DatePicker 必须配置 `format` 属性，禁止依赖默认格式 |
| C-VBEN-COMP-003 | RadioGroup 使用 `optionType='button'` 时必须提供 `options` 数组 |
| C-VBEN-COMP-004 | Upload 组件必须配置 `accept` 限制文件类型 |

---

## 按需加载指引

**根据任务类型读取对应文档：**

| 任务类型 | 推荐读取 | 内容 |
|---------|---------|------|
| 开发表单 | `references/02-form.md` | VbenForm完整API、schema配置、验证规则 |
| 开发列表页 | `references/03-grid.md` → `references/02-form.md` | VxeGrid完整API、列定义、搜索表单 |
| 新建页面 | `references/05-page-patterns.md` | 完整页面模板（列表/表单/详情） |
| 配置主题 | `references/01-configuration.md` | 主题/布局/功能配置 |
| 添加路由 | `references/06-routing.md` | 路由定义、权限配置 |
| 开发弹窗 | `references/04-modal.md` | Modal/Drawer API |

**强制规则**：实现前必须读取对应 references 文档，禁止猜测 API。

---

## 知识库

**读取这些文档获取详细 API：**

| 文档 | 内容 | 路径 |
|------|------|------|
| git pull / 拉取同步 | 拉取同步流程 | `../docs/collaboration/06-sync-flow.md` |
| 协同开发概述 | 触发指令 + 文档索引 | `../docs/collaboration/01-overview.md` |
| 项目目录结构 | docs/ + frontend/ 目录 | `../docs/collaboration/02-project-structure.md` |
| 前端工程结构 | Vben Admin 目录结构 | `../docs/collaboration/03-frontend-backend.md` |
| status.md / 归档 | 状态快照 + 归档机制 | `../docs/collaboration/05-status-mechanism.md` |
| 配置化能力 | 主题/布局/功能配置 | `references/01-configuration.md` |
| 表单组件 | 完整 Form API | `references/02-form.md` |
| 表格组件 | 完整 Grid API | `references/03-grid.md` |
| 弹窗组件 | Modal/Drawer API | `references/04-modal.md` |
| 页面模式 | 完整页面模板 | `references/05-page-patterns.md` |
| 路由配置 | 路由与权限 | `references/06-routing.md` |

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
| `new_page` (form) | views/module/feature/index.vue + data.ts + api/module/feature.ts | 全部必需 |
| `new_page` (detail) | views/module/feature/index.vue + data.ts + api/module/feature.ts | 全部必需 |
| `new_page` (dashboard) | views/module/feature/index.vue + api/module/feature.ts | 全部必需 |
| `theme_config` | apps/web-antd/src/preferences.ts + tailwind.config.mjs（如需扩展样式） | preferences.ts必需 |
| `route_add` | router/routes/modules/*.ts + （如需权限）permissions配置 | 路由文件必需 |
| `modal_add` | modules/*.vue + 父页面集成代码（import + useVbenModal） | modal文件必需 |
| `field_change` | data.ts（schema变更） + api/*.ts（如有接口参数变更） | 视具体字段 |

**输出验证**: 每个输出文件必须通过 TypeScript 类型检查，无 `any` 类型。

---

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

## 页面模板

完整页面模板（列表页/表单页/详情页）见 `references/05-page-patterns.md`，包含：
- 标准文件结构（index.vue + data.ts + modules/form.vue）
- 完整代码示例
- API 集成模式

## 最后规则

```
知识库存在的意义 → 实现前先阅读
禁止猜测 API → 先查文档
遵循模式 → 一致性优于创造性
```

---

## 版本

- v2.4
- 更新: 2026-04-11
- 变更: 协同开发指南拆分为多个小文件，按需加载
- v2.0: YAML 页面规格输入解析、HTML 线框图解析、输入优先级、内置 UI 约束