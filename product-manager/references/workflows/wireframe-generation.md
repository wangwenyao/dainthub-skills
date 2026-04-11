# 页面线框图生成流程

**何时使用**: 需要生成页面原型、线框图、页面结构设计时

---

## 输出格式

### 双轨输出

| 输出 | 文件 | 用途 | 格式 |
|------|------|------|------|
| **HTML 线框图** | `wireframes-[模块名]-v[版本].html` | 人 review/调整 | HTML + CSS |
| **YAML 页面规格** | 嵌入 PRD 或独立 `pages-[模块名].yaml` | 前端代码生成 | YAML |

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

### Step 1：确定页面清单

从功能清单提取页面：

| 功能类型 | 页面类型 | 页面数量 |
|---------|---------|---------|
| 数据管理类（台账、档案） | list + form-modal | 2 页 |
| 流程审批类 | list + detail + form-modal | 3 页 |
| 统计报表类 | dashboard | 1 页 |

### Step 2：定义菜单结构

确定模块层级 → 菜单分组 → 页面路由映射

```
模块层级:
├─ 商品管理（一级菜单）
│   ├─ 商品列表（二级菜单 → P001）
│   └─ 商品分类（二级菜单 → P002）
├─ 订单管理（一级菜单）
│   ├─ 订单列表（二级菜单 → P003）
│   └─ 退款管理（二级菜单 → P004）
```

### Step 3：生成 HTML 线框图

1. **创建 wireframes.html 文件**
2. **写入共享 CSS 样式**（一次定义，所有页面共用）
3. **生成布局框架**（顶部导航 + 左侧菜单 + 内容区）
4. **按页面类型选择内容模板**
5. **添加页面分隔符和 ID**（#p001, #p002...）

### Step 4：生成 YAML 页面规格

每个页面一段 YAML，包含：
- page_type（list / form-modal / detail / dashboard）
- search/table/form 配置
- 路由和菜单映射

### Step 5：嵌入 PRD 或独立输出

- YAML 嵌入 PRD 的"页面规格说明"章节
- HTML 线框图独立文件，PRD 中引用路径

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

### 基础结构

```yaml
# 页面规格 - [模块名]
version: 1.0
module: [模块名]

# 菜单结构
menu:
  structure:
    - name: 首页
      route: /dashboard
      pageId: P000
    - group: [一级菜单名]
      items:
        - name: [二级菜单名]
          route: [路由路径]
          pageId: [页面ID]

# 页面清单
pages:
  P001:
    name: [页面名称]
    type: [list/form-modal/detail/dashboard]
    route: [路由路径]
    config:
      ...
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

### wireframes.html 结构

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
  
  <!-- 左侧菜单 -->
  <div class="sidebar">
    <div class="menu-item">首页</div>
    <div class="menu-group">
      <div class="menu-group-title">商品管理</div>
      <div class="menu-item active">商品列表</div>
      <div class="menu-item">商品分类</div>
    </div>
  </div>
  
  <!-- 内容区 -->
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

---

## 版本

- v1.0
- 创建: 2026-04-11