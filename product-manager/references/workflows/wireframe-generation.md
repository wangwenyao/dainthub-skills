# 页面线框图生成流程

**何时使用**: 需要生成页面原型、线框图、页面结构设计时

---

## 输出格式

### 双轨输出（按一级模块分开）

| 输出 | 文件命名 | 用途 | 格式 |
|------|---------|------|------|
| **HTML 线框图** | `wireframes-[一级模块名]-v[版本].html` | 人 review/调整 | HTML + CSS |
| **YAML 页面规格** | `pages-[一级模块名].yaml` | 前端代码生成 | YAML |

**文件分开规则**：
- 每个一级模块（如"商品管理"、"订单管理"）生成独立的 HTML 和 YAML 文件
- 文件命名使用一级模块名，不含二级页面名
- 每个文件包含该一级模块下的所有二级页面

**示例**：
```
docs/wireframes/
├── wireframes-商品管理-v1.html   # 包含：商品列表、商品分类页面
├── wireframes-订单管理-v1.html   # 包含：订单列表、退款管理页面
├── pages-商品管理.yaml           # 商品管理模块 YAML
├── pages-订单管理.yaml           # 订单管理模块 YAML
```

---

## 线框图设计原则

### 核心原则

| 原则 | 说明 |
|------|------|
| **只表达结构** | 不涉及 UI 视觉（颜色、字体、图标） |
| **灰色示意** | 边框 #999、填充 #eee/#f5f5f5 |
| **占位文字** | `[字段名]` 表示字段位置 |
| **组件标注** | `<div class="label">组件：表格</div>` |
| **交互标注** | 用文字表示交互（点击、跳转） |
| **统一布局** | 顶部导航 + 左侧菜单 + 内容区 |

### 不包含的内容

| 不包含 | 原因 |
|--------|------|
| 真实颜色 | UI 由前端 skill 处理 |
| 图标 | 只用文字表示（如 `+` `✕` `▼`） |
| 字体样式 | 不指定 font-family |
| 阴影效果 | 线框图不需要 |
| 动画效果 | 只标注交互，不画动画 |

---

## 统一布局结构

### 标准布局模板

```
┌─────────────────────────────────────────────────────┐
│ 顶部导航栏（60px，灰色背景）                          │
│ ├─ Logo                                              │
│ ├─ 系统名称                                           │
│ └─ 用户信息                                           │
├─────────────────────────────────────────────────────┤
│      │                                              │
│ 左侧 │              内容区                           │
│ 菜单 │                                              │
│      │   ┌─────────────────────────────────────┐    │
│ 200px│   │ 模块内容                              │    │
│      │   │                                       │    │
│      │   │                                       │    │
│      │   └─────────────────────────────────────┘    │
│      │                                              │
└─────────────────────────────────────────────────────┘
```

### 左侧菜单结构

菜单支持跳转到指定模块页面：

```html
<!-- 左侧菜单示例 -->
<div class="sidebar">
  <div class="menu-item">首页</div>
  <div class="menu-group">
    <div class="menu-group-title">商品管理</div>
    <div class="menu-item active">商品列表</div>  <!-- active 表示当前页 -->
    <div class="menu-item">商品分类</div>
  </div>
  <div class="menu-group">
    <div class="menu-group-title">订单管理</div>
    <div class="menu-item">订单列表</div>
    <div class="menu-item">退款管理</div>
  </div>
</div>
```

### 菜单 → 页面跳转映射

在 YAML 中定义菜单与页面的对应关系：

```yaml
menu:
  structure:
    - name: 首页
      route: /dashboard
      pageId: P000
    - group: 商品管理
      items:
        - name: 商品列表
          route: /product/list
          pageId: P001
        - name: 商品分类
          route: /product/category
          pageId: P002
    - group: 订单管理
      items:
        - name: 订单列表
          route: /order/list
          pageId: P003
```

---

## 生成流程

### Step 0：从三级功能点提取页面/组件

**三级功能点 → 页面/组件映射规则**：

| 功能点类型分类 | 页面/组件类型 | 是否独立页面 | 说明 |
|----------------|---------------|--------------|------|
| **查看类** | list（列表页） | 是 | 数据列表展示 |
| **查看类** | detail（详情页） | 是（按需） | 流程类、需要独立查看的场景 |
| **搜索类** | list 搜索区组件 | 否（嵌入） | 搜索筛选条件 |
| **新增类** | form-modal（表单弹窗） | 是 | 数据录入表单 |
| **编辑类** | form-modal（表单弹窗） | 是（复用） | 复用新增弹窗 |
| **删除类** | confirm-modal（确认弹窗） | 否（简单） | 简单确认弹窗 |
| **导出类** | 无页面 | 否 | 触发异步任务 |
| **业务操作类** | action-modal（操作弹窗） | 是 | 业务特定的操作弹窗 |

**业务操作类功能点识别与定义**：

业务操作是**业务特定的**，不同系统有不同的业务操作。PRD 编写时需根据业务场景自行定义。

| 识别规则 | 说明 |
|----------|------|
| **是否改变数据状态** | 改变状态（如审批通过、任务完成）→ 需操作弹窗 |
| **是否需要额外信息** | 需填写信息（如审批意见、分配原因）→ 需操作弹窗 |
| **是否涉及多选项** | 需选择对象（如分配给谁）→ 需操作弹窗 |
| **是否简单确认即可** | 只需确认无额外信息 → 使用确认弹窗 |

**业务操作弹窗通用结构**：

```
操作弹窗结构：
├── 信息摘要区（可选）：展示操作对象的关键信息
├── 操作选项区（按需）：选择、下拉、单选等
├── 操作信息区（按需）：文本框、备注、原因等
└── 确认按钮区：取消 + 确认
```

**页面生成规则**：

1. **必须生成独立页面**：
   - list（列表页）：每个二级功能至少一个
   - form-modal（表单弹窗）：新增/编辑共用一个弹窗
   - detail（详情页）：流程审批类、需要独立查看的场景

2. **不生成独立页面**：
   - 删除确认弹窗：简单的确认弹窗，在 HTML 中用 `<div class="confirm-modal">` 占位表示
   - 批量操作确认弹窗：同删除确认弹窗处理
   - 搜索筛选：嵌入列表页的搜索区组件

3. **在 YAML 中标注组件位置**：
   - 删除操作：`rowActions` 中标注 `{ confirm: true, confirmText: "确认删除此商品？" }`
   - 批量删除：`toolbarActions` 中标注 `{ confirm: true, confirmText: "确认删除选中的 N 条数据？" }`

### Step 1：确定页面清单

从三级功能点提取页面：

| 功能类型 | 二级功能 | 三级功能点 | 页面清单 |
|---------|---------|-----------|---------|
| 数据管理类 | 商品列表 | 查看、搜索、新增、编辑、删除 | P001 列表页 + P002 表单弹窗 |
| 流程审批类 | 订单审批 | 查看、搜索、详情、审批 | P001 列表页 + P002 详情页 + P003 审批弹窗 |
| 统计报表类 | 销售报表 | 查看图表、筛选 | P001 仪表盘 |

**页面数量估算**：
- 简单 CRUD 功能：1 个列表页 + 1 个表单弹窗 = 2 个页面
- 流程审批功能：1 个列表页 + 1 个详情页 + 1 个审批弹窗 = 3 个页面
- 统计报表功能：1 个仪表盘 = 1 个页面

### Step 2：定义菜单结构

确定模块层级 → 菜单分组 → 页面路由映射 → **按一级模块分组**

```
模块层级（按一级模块分开）:

商品管理模块:
├─ 商品管理（一级菜单）
│   ├─ 商品列表（二级菜单 → P001）
│   └─ 商品分类（二级菜单 → P002）

订单管理模块:
├─ 订单管理（一级菜单）
│   ├─ 订单列表（二级菜单 → P003）
│   └─ 退款管理（二级菜单 → P004）
```

**注意**：一级模块对应一个 HTML/YAML 文件，文件内包含该模块的所有二级页面。

### Step 3：按一级模块生成 HTML 线框图

**逐模块生成**（每个一级模块一个文件）：

| 步骤 | 操作 |
|------|------|
| 3.1 | 确定一级模块清单 |
| 3.2 | 为每个一级模块创建 `wireframes-[模块名]-v[版本].html` |
| 3.3 | 写入共享 CSS 样式（所有模块共用同一套样式） |
| 3.4 | 生成布局框架（顶部导航 + 左侧菜单 + 内容区） |
| 3.5 | **只包含该一级模块的页面**（菜单高亮当前模块） |
| 3.6 | 添加页面分隔符和 ID（#p001, #p002...） |

**菜单显示规则**：
- 左侧菜单显示完整菜单结构（包含其他一级模块）
- 当前一级模块的菜单项高亮显示
- 其他一级模块的菜单项正常显示（可点击跳转）

### Step 4：按一级模块生成 YAML 页面规格

**逐模块生成**（每个一级模块一个文件）：

| 步骤 | 操作 |
|------|------|
| 4.1 | 为每个一级模块创建 `pages-[模块名].yaml` |
| 4.2 | 写入模块基本信息（version, module） |
| 4.3 | 定义该模块的菜单结构 |
| 4.4 | 定义该模块的所有页面（pages 配置） |

### Step 5：独立输出

- HTML 线框图：独立文件，存放于 `docs/wireframes/` 目录
- YAML 页面规格：独立文件，存放于 `docs/wireframes/` 目录
- PRD 中引用所有线框图文件路径

---

## HTML 线框图模板

读取 `@wireframe-layout-templates.md` 获取完整模板。

### 页面类型 → 内容模板

| 页面类型 | 内容区结构 | 适用场景 |
|---------|-----------|---------|
| **list（列表页）** | 搜索区 → 操作栏 → 表格 → 分页 | 数据管理 |
| **form-modal（表单弹窗）** | 标题 → 表单字段 → 操作按钮 | 新增/编辑 |
| **detail（详情页）** | 信息区 → 关联区 → 操作按钮 | 查看 |
| **dashboard（仪表盘）** | 筛选 → 图表 → 卡片 | 统计报表 |

---

## CSS 样式规范

### 共享样式（所有线框图共用）

```css
/* ========== 布局框架 ========== */

/* 基础容器 */
.layout { display: flex; min-height: 100vh; }

/* 顶部导航栏 */
.header { 
  position: fixed; top: 0; left: 0; right: 0; height: 60px;
  background: #ddd; border-bottom: 1px solid #999; z-index: 100;
  display: flex; align-items: center; justify-content: space-between; padding: 0 20px;
}
.header-left { display: flex; align-items: center; gap: 20px; }
.header-right { display: flex; align-items: center; gap: 16px; }
.logo { border: 1px solid #999; padding: 8px 16px; background: #ccc; }
.system-name { color: #333; font-weight: 500; }
.user-info { border: 1px solid #999; padding: 4px 12px; background: #ccc; }
.user-text { color: #666; }

/* 左侧菜单 */
.sidebar { 
  position: fixed; top: 60px; left: 0; bottom: 0; width: 200px;
  background: #eee; border-right: 1px solid #999; overflow-y: auto;
}

/* 内容区 */
.main { 
  margin-left: 200px; margin-top: 60px; flex: 1;
  background: #f5f5f5; padding: 20px; min-height: calc(100vh - 60px);
}

/* ========== 菜单样式 ========== */

.menu-group { border-bottom: 1px solid #ccc; }
.menu-group-title { padding: 12px 16px; color: #666; font-weight: 500; background: #ddd; }
.menu-item { padding: 8px 16px 8px 24px; color: #999; cursor: pointer; border-bottom: 1px solid #ccc; }
.menu-item.active { background: #ccc; color: #333; }
.menu-item:hover { background: #e5e5e5; }
.menu-item-home { padding: 12px 16px; color: #999; border-bottom: 1px solid #ccc; }

/* ========== 页面容器 ========== */

.wireframe { border: 1px dashed #999; padding: 16px; background: #f5f5f5; margin: 16px 0; }
.page-divider { border-top: 2px solid #666; margin-top: 24px; padding-top: 16px; }
.page-title { font-size: 18px; color: #333; margin-bottom: 16px; }
.page-id { color: #999; font-size: 14px; }

/* ========== 区块 ========== */

.section { border: 1px solid #ccc; background: #eee; padding: 12px; margin: 12px 0; position: relative; }
.section-white { border: 1px solid #ccc; background: #fff; padding: 0; margin: 12px 0; }
.row { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
.row-right { display: flex; gap: 12px; align-items: center; justify-content: flex-end; }
.row-center { display: flex; gap: 12px; align-items: center; justify-content: center; }
.row-between { display: flex; justify-content: space-between; align-items: center; }
.row-gap-lg { display: flex; gap: 24px; align-items: center; }
.row-gap-sm { display: flex; gap: 8px; align-items: center; }

/* ========== 字段组件 ========== */

.field { border: 1px solid #999; background: #fff; padding: 8px 12px; color: #999; min-width: 80px; }
.input { min-width: 150px; }
.select { min-width: 120px; }
.select::after { content: ' ▼'; color: #666; }
.date { min-width: 100px; }
.date::after { content: ' 📅'; color: #666; }
.number { text-align: right; min-width: 80px; }
.textarea { min-width: 200px; min-height: 60px; display: block; margin-top: 8px; }
.field-full { width: 100%; }
.field-small { padding: 4px 12px; }
.field-active { background: #ccc; }

/* ========== 标签和按钮 ========== */

.tag { display: inline-block; padding: 4px 8px; border: 1px solid #999; background: #ddd; font-size: 12px; }
.btn { display: inline-block; padding: 8px 16px; border: 1px solid #666; background: #ccc; cursor: pointer; }
.btn-primary { background: #aaa; border-color: #555; }
.btn-danger { color: #c00; border-color: #c00; }
.btn-small { padding: 4px 8px; }
.btn-margin { margin: 4px; }
.btn-margin-left { margin-left: 8px; }

/* ========== 表格 ========== */

.table { width: 100%; border-collapse: collapse; background: #fff; }
.th { background: #ddd; padding: 12px; border: 1px solid #ccc; color: #555; }
.td { padding: 12px; border: 1px dashed #ccc; color: #999; }
.td-center { padding: 12px; border: 1px dashed #ccc; text-align: center; }
.td-right { padding: 12px; border: 1px dashed #ccc; text-align: right; }
.th-checkbox { width: 40px; text-align: center; }
.td-checkbox { width: 40px; text-align: center; }

/* ========== 弹窗 ========== */

.modal { border: 2px solid #666; background: #f5f5f5; max-width: 600px; margin: 24px; }
.modal-header { background: #ddd; padding: 16px; border-bottom: 1px solid #ccc; display: flex; justify-content: space-between; }
.modal-body { padding: 24px; }
.modal-footer { background: #eee; padding: 16px; border-top: 1px solid #ccc; text-align: right; }
.modal-close { color: #999; cursor: pointer; }
.modal-title { font-weight: 500; color: #333; }

/* ========== 表单 ========== */

.form-group { margin: 16px 0; }
.form-label { color: #555; margin-bottom: 8px; display: block; }
.form-required::after { content: ' *'; color: #c00; }
.form-flex { display: flex; gap: 24px; }
.form-flex-item { flex: 1; }

/* ========== 详情页 ========== */

.detail-section { border: 1px solid #ccc; background: #fff; padding: 16px; margin: 12px 0; }
.detail-title { font-weight: 500; color: #555; margin-bottom: 12px; border-bottom: 1px solid #ccc; padding-bottom: 8px; }
.detail-row { display: flex; padding: 8px 0; border-bottom: 1px dashed #ccc; }
.detail-row-last { display: flex; padding: 8px 0; }
.detail-label { width: 120px; color: #666; }
.detail-value { flex: 1; color: #333; }
.detail-content { color: #666; padding: 8px; background: #eee; }

/* ========== 仪表盘 ========== */

.card { border: 1px solid #999; background: #eee; padding: 16px; width: 150px; text-align: center; }
.card-title { color: #666; font-size: 12px; }
.card-value { color: #333; font-size: 24px; margin-top: 8px; }
.card-group { display: flex; gap: 16px; justify-content: space-around; }
.chart-area { border: 1px dashed #999; height: 150px; display: flex; align-items: center; justify-content: center; color: #999; background: #eee; }
.chart-title { color: #666; margin-bottom: 12px; }

/* ========== 图片上传 ========== */

.image-box { border: 1px solid #999; background: #ddd; width: 80px; height: 80px; text-align: center; line-height: 80px; display: inline-block; }
.image-box-add { border: 1px dashed #999; background: #fff; width: 80px; height: 80px; text-align: center; line-height: 80px; display: inline-block; margin-left: 8px; }
.image-group { text-align: center; padding: 16px; background: #eee; border: 1px solid #ccc; }
.image-large { border: 1px solid #999; background: #ddd; width: 100px; height: 100px; text-align: center; line-height: 100px; }

/* ========== 组件标注 ========== */

.label { color: #666; font-size: 11px; margin-top: 8px; font-style: italic; }
.label-padding { color: #666; font-size: 11px; padding: 8px; font-style: italic; }

/* ========== 交互标注 ========== */

.interaction { color: #666; font-size: 12px; padding: 4px 8px; background: #ffe; border: 1px dashed #999; display: inline-block; margin: 4px; }
.interaction-small { color: #666; font-size: 11px; margin-top: 4px; }
```

---

## YAML 输出规范

### 基础结构（按一级模块）

每个 YAML 文件对应一个一级模块：

```yaml
# 页面规格 - [一级模块名]
version: 1.0
module: [一级模块名]              # 如：商品管理

# 菜单结构（只包含本模块的菜单项）
menu:
  structure:
    - group: [一级菜单名]         # 本模块的一级菜单
      items:
        - name: [二级菜单名]
          route: [路由路径]
          pageId: [页面ID]
        - name: [另一个二级菜单名]
          route: [路由路径]
          pageId: [页面ID]

# 页面清单（只包含本模块的页面）
pages:
  P001:
    name: [页面名称]
    type: [list/form-modal/detail/dashboard]
    route: [路由路径]
    config:
      ...
  P002:
    name: [另一个页面名称]
    type: ...
```

### 文件组织示例

假设有两个一级模块：

```yaml
# pages-商品管理.yaml
version: 1.0
module: 商品管理

menu:
  structure:
    - group: 商品管理
      items:
        - { name: 商品列表, route: /product/list, pageId: P001 }
        - { name: 商品分类, route: /product/category, pageId: P002 }

pages:
  P001: { ... }
  P002: { ... }

---

# pages-订单管理.yaml
version: 1.0
module: 订单管理

menu:
  structure:
    - group: 订单管理
      items:
        - { name: 订单列表, route: /order/list, pageId: P003 }
        - { name: 退款管理, route: /order/refund, pageId: P004 }

pages:
  P003: { ... }
  P004: { ... }
```

### 列表页 YAML

```yaml
P001:
  name: 商品列表
  type: list
  route: /product/list
  
  config:
    search:
      fields:
        - { name: 商品名称, field: name, component: Input, placeholder: 请输入 }
        - { name: 商品分类, field: categoryId, component: ApiSelect, api: /api/categories }
        - { name: 状态, field: status, component: Select, options: [草稿,上架,下架] }
        - { name: 创建时间, field: createdAt, component: RangePicker }
    
    table:
      columns:
        - { field: id, title: ID, width: 80, fixed: left }
        - { field: name, title: 商品名称, width: 200 }
        - { field: category, title: 分类, width: 150 }
        - { field: price, title: 价格, width: 100, align: right, format: currency }
        - { field: stock, title: 库存, width: 80, align: right }
        - { field: status, title: 状态, width: 100, component: Tag }
        - { field: createdAt, title: 创建时间, width: 160 }
        - { field: actions, title: 操作, width: 150, fixed: right }
      rowActions:
        - { name: 编辑, type: default }
        - { name: 删除, type: danger, confirm: true }
      toolbarActions:
        - { name: 新增, type: primary, pageId: P002 }
    
    pagination:
      pageSize: 20
```

### 表单弹窗 YAML

```yaml
P002:
  name: 商品表单弹窗
  type: form-modal
  
  config:
    modal:
      title: 商品信息
      width: 600px
    
    form:
      fields:
        - { name: 商品名称, field: name, component: Input, required: true, rules: [required, max(50)] }
        - { name: 商品分类, field: categoryId, component: ApiSelect, required: true, api: /api/categories }
        - { name: 价格, field: price, component: InputNumber, required: true, min: 0, precision: 2 }
        - { name: 库存, field: stock, component: InputNumber, required: true, min: 0 }
        - { name: 状态, field: status, component: RadioGroup, options: [草稿,上架,下架] }
        - { name: 商品图片, field: images, component: Upload, accept: [jpg,png], maxCount: 5 }
        - { name: 商品描述, field: description, component: TextArea, max: 500 }
```

### 详情页 YAML

```yaml
P003:
  name: 商品详情
  type: detail
  route: /product/:id
  
  config:
    sections:
      - name: 基本信息
        fields:
          - { name: 商品ID, field: id }
          - { name: 商品名称, field: name }
          - { name: 商品分类, field: category }
          - { name: 价格, field: price, format: currency }
          - { name: 状态, field: status, component: Tag }
      - name: 商品图片
        type: images
        field: images
      - name: 商品描述
        type: text
        field: description
    
    actions:
      - { name: 返回列表, type: default }
      - { name: 编辑, type: primary, pageId: P002 }
```

### 仪表盘 YAML

```yaml
P000:
  name: 数据概览
  type: dashboard
  route: /dashboard
  
  config:
    filters:
      - { name: 时间范围, field: dateRange, component: RangePicker }
    
    cards:
      - { name: 今日订单, field: orderCount, format: number }
      - { name: 今日销售额, field: salesAmount, format: currency }
      - { name: 新增用户, field: newUserCount, format: number }
    
    charts:
      - { name: 销售趋势, type: line, field: salesTrend }
      - { name: 分类占比, type: pie, field: categoryRatio }
```

---

## 字段 → 组件映射

| 字段类型 | HTML class | YAML component |
|---------|-----------|----------------|
| 文本（短） | `field input` | Input |
| 文本（长） | `field textarea` | TextArea |
| 数字 | `field number` | InputNumber |
| 枚举/下拉 | `field select` | Select / ApiSelect |
| 日期 | `field date` | DatePicker |
| 日期范围 | `field date` + 两个框 | RangePicker |
| 状态标签 | `tag` | Tag |
| 文件上传 | `field` + `[上传区域]` | Upload |
| 必填标记 | `form-required` | required: true |

---

## 输出示例

### 文件组织结构

```
docs/wireframes/
├── wireframes-商品管理-v1.html   # 商品管理模块线框图
├── wireframes-订单管理-v1.html   # 订单管理模块线框图
├── pages-商品管理.yaml           # 商品管理模块 YAML
├── pages-订单管理.yaml           # 订单管理模块 YAML
```

### wireframes-商品管理-v1.html 结构

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>线框图 - 商品管理模块</title>
  <style>
    /* 共享样式（见上方 CSS 规范） */
  </style>
</head>
<body>

<!-- 布局框架 -->
<div class="layout">
  <!-- 顶部导航 -->
  <div class="header">
    <div class="logo">[Logo]</div>
    <div class="system-name">[系统名称]</div>
    <div class="user-info">[用户信息]</div>
  </div>
  
  <!-- 左侧菜单（显示完整菜单，商品管理高亮） -->
  <div class="sidebar">
    <div class="menu-item">首页</div>
    <div class="menu-group">
      <div class="menu-group-title">商品管理</div>
      <div class="menu-item active">商品列表</div>
      <div class="menu-item">商品分类</div>
    </div>
    <div class="menu-group">
      <div class="menu-group-title">订单管理</div>
      <div class="menu-item">订单列表</div>
      <div class="menu-item">退款管理</div>
    </div>
  </div>
  
  <!-- 内容区（只包含商品管理模块的页面） -->
  <div class="main">
    
    <!-- P001 商品列表页 -->
    <div id="p001" class="page-divider">
      <div class="page-title">商品列表 <span class="page-id">(P001)</span></div>
      <div class="wireframe">
        <!-- 搜索区、操作栏、表格、分页 -->
      </div>
    </div>
    
    <!-- P002 商品表单弹窗 -->
    <div id="p002" class="page-divider">
      <div class="page-title">商品表单弹窗 <span class="page-id">(P002)</span></div>
      <div class="modal">
        <!-- 弹窗内容 -->
      </div>
    </div>
    
  </div>
</div>

</body>
</html>
```

### wireframes-订单管理-v1.html 结构

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>线框图 - 订单管理模块</title>
  <style>
    /* 共享样式（同上） */
  </style>
</head>
<body>

<!-- 布局框架 -->
<div class="layout">
  <!-- 顶部导航（同上） -->
  <div class="header">...</div>
  
  <!-- 左侧菜单（显示完整菜单，订单管理高亮） -->
  <div class="sidebar">
    <div class="menu-item">首页</div>
    <div class="menu-group">
      <div class="menu-group-title">商品管理</div>
      <div class="menu-item">商品列表</div>
      <div class="menu-item">商品分类</div>
    </div>
    <div class="menu-group">
      <div class="menu-group-title">订单管理</div>
      <div class="menu-item active">订单列表</div>
      <div class="menu-item">退款管理</div>
    </div>
  </div>
  
  <!-- 内容区（只包含订单管理模块的页面） -->
  <div class="main">
    
    <!-- P003 订单列表页 -->
    <div id="p003" class="page-divider">
      <div class="page-title">订单列表 <span class="page-id">(P003)</span></div>
      <div class="wireframe">
        <!-- 订单列表内容 -->
      </div>
    </div>
    
    <!-- P004 退款管理页 -->
    <div id="p004" class="page-divider">
      <div class="page-title">退款管理 <span class="page-id">(P004)</span></div>
      <div class="wireframe">
        <!-- 退款管理内容 -->
      </div>
    </div>
    
  </div>
</div>

</body>
</html>
```

---

## 版本

- v1.4
- 更新: 2026-04-12
- 新增: Step 0 三级功能点映射规则（通用分类 + 业务操作识别规则）