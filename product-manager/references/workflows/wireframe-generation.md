# 页面线框图生成流程

**何时使用**: 需要生成页面原型、线框图、页面结构设计时

---

## ⚠️ 硬约束（MANDATORY）

**必须遵守以下规则，违反即为流程执行失败**：

### 1. 数量传递约束（功能点→页面）

**前置输入验证**：
```
PRD输出：M 个三级功能点（每个功能点有页面/组件标注）
    ↓ 强制接收
线框图输入：必须处理这 M 个功能点对应的页面（不得遗漏）
```

**功能点→页面映射验证表（强制输出）**：

| 三级功能点ID | 功能点名称 | 页面/组件 | 页面ID | 是否生成 | 缺失说明 |
|--------------|------------|-----------|--------|----------|----------|
| F0101 | 查看商品列表 | P001 列表页 | P001 | ✓ | |
| F0102 | 搜索商品 | P001 搜索区 | - | ✓ 嵌入 | |
| F0103 | 新增商品 | P002 表单弹窗 | P002 | ✓ | |
| F0104 | 编辑商品 | P002 表单弹窗 | P002 | ✓ 复用 | |
| F0105 | 删除商品 | 确认弹窗 | - | ✓ 嵌入 | |
| F0305 | 查看订单详情 | P006 详情页 | P006 | ❌ | 需生成 |
| F0306 | 审批订单 | P007 审批弹窗 | P007 | ❌ | 需生成 |

**约束规则**：
- 独立页面类型（list/form-modal/detail）必须有对应 HTML/YAML
- 嵌入组件类型（搜索区/确认弹窗）必须在页面内标注位置
- 任何功能点无对应页面 → 线框图不完整

---

### 2. 逐项生成约束（页面生成）- 验证式输出

**生成页面时（Step 3/4）**：

输入：功能点清单中的页面/组件列表

**⚠️ 禁止声明式输出，必须输出实际内容**：

```
错误示例（声明式，禁止）：
├── ☐ P001 商品列表页 → 正在生成... ✓
│   └── 输出：HTML 页面结构 + YAML 页面规格 ✓
├── ☐ P002 商品表单弹窗 → 正在生成... ✓

正确示例（验证式，必须）：
├── P001 商品列表页
│   ├── HTML内容（实际输出表格结构、搜索区、分页组件）：
│   │   <div class="search-section">...</div>
│   │   <table class="table">...</table>
│   │   <div class="pagination">...</div>
│   ├── YAML内容（实际输出配置）：
│   │   search: { fields: [...] }
│   │   table: { columns: [...] }
│   └── 验证：组件标注完整 ✓、灰色系配色 ✓、占位文字 ✓
│
├── P002 商品表单弹窗
│   ├── HTML内容（实际输出表单结构）：
│   │   <div class="modal">...</div>
│   │   <div class="form-group">...</div>
│   ├── YAML内容（实际输出配置）：
│   │   form: { fields: [...] }
│   └── 验证：表单字段完整 ✓、校验规则标注 ✓

完成确认：所有页面已生成完毕
验证：功能点→页面映射验证表无缺失项
```

**验证要求**：
- 每个页面必须输出实际HTML结构和YAML配置片段
- 禁止只声明"正在生成... ✓"而不输出实际内容
- 每个页面必须有具体验证项（组件标注、配色、占位文字等）

---

### 3. 生成前必须动作

```
1. 确认已读取以下文件（不得凭记忆推断）：
   ├── @wireframe-layout-templates.md    # 页面模板（必须读取）
   ├── CSS 样式规范（本文件下方）         # 必须使用定义的 class
   
2. 接收 PRD 功能清单输入：
   ├── 三级功能点数量：M 个
   ├── 页面/组件清单：从功能点清单提取
   └── 数量传递验证：是否所有功能点都有页面/组件标注？

3. 输出功能点→页面映射验证表（初始状态，标记待生成）
```

### 生成中必须动作

| 要求 | 说明 |
|------|------|
| **必须使用模板 class** | 使用 wireframe-layout-templates.md 定义的结构，不得自创样式 |
| **必须灰色系配色** | 边框 #999、填充 #eee/#f5f5f5，不得使用真实颜色 |
| **必须占位文字** | `[字段名]` 格式，不得使用真实数据 |
| **必须组件标注** | 每个区域标注 `<div class="label">组件：xxx</div>` |
| **必须按一级模块分开** | 每个 YAML 文件对应一个一级模块 |

### 输出格式强制要求

**HTML 线框图必须包含**：
```
<!DOCTYPE html>
<html>
<head>
  <title>线框图 - [一级模块名]</title>
  <style> /* CSS 样式规范内容 */ </style>
</head>
<body>
  <div class="layout">
    <div class="header">...</div>
    <div class="sidebar">...</div>
    <div class="main">
      <!-- 每个页面用 page-divider 分隔 -->
      <div id="p001" class="page-divider">...</div>
    </div>
  </div>
</body>
</html>
```

**YAML 必须包含**：
```yaml
version: 1.0
module: [一级模块名]
menu:
  structure: [...]  # 必须有菜单结构
pages:
  P001:
    name: [页面名称]
    type: [list/form-modal/detail/dashboard]  # 必须有类型
    route: [路由路径]                          # 必须有路由
    config: {...}                              # 必须有配置
```

### 生成后必须动作

```
1. 输出功能点→页面映射验证表（最终状态）：
   ├── 所有独立页面类型已生成 HTML/YAML
   ├── 所有嵌入组件类型已在页面内标注位置
   └── 无缺失项

2. 验证检查项（必须输出实际验证结果）：
   | 检查项 | 验证方式 | 验证结果 |
   |--------|----------|----------|
   | 功能点→页面映射验证表是否无缺失？ | 检查表格"缺失说明"列是否全为空 | ✓ / ❌ |
   | 逐项生成清单是否输出实际内容？ | 检查是否输出HTML/YAML片段而非仅声明 | ✓ / ❌ |
   | HTML是否使用模板定义的class？ | 抽查class名称是否来自CSS样式规范 | ✓ / ❌ |
   | HTML是否使用灰色系配色？ | 检查是否有真实颜色（如#ff0000） | ✓ / ❌ |
   | YAML是否包含完整的pages配置？ | 检查每个page是否有type、route、config | ✓ / ❌ |
   | 是否按一级模块分开生成文件？ | 检查文件命名是否包含模块名 | ✓ / ❌ |

3. 确认所有检查项通过后才能结束
   - 任一检查项为❌ → 违规，必须修正
```

### 禁止行为

| 禁止 | 原因 |
|------|------|
| ❌ 使用真实颜色或图标 | 线框图只表达结构，不涉及 UI 视觉 |
| ❌ 自创 class 或样式 | 必须使用 CSS 样式规范定义的 class |
| ❌ YAML 缺少 config | 每个页面必须有完整配置 |
| ❌ 所有页面放一个文件 | 必须按一级模块分开 |
| ❌ 不读取模板直接生成 | 可能使用错误结构 |
| ❌ 批量生成页面 | 必须逐项生成 |
| ❌ 不输出功能点→页面映射验证表 | 必须输出数量传递验证 |
| ❌ 功能点无对应页面 | 必须为每个功能点生成页面或标注位置 |

### 执行信号

以下行为表明流程执行失败：
- 功能点→页面映射验证表缺失
- 功能点无对应页面
- 逐项生成清单未逐项输出
- 页面数量与功能点清单不匹配

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
| **wizard（分步向导）** | 步骤导航 → 当前步骤内容 → 上一步/下一步 | 复杂表单、配置流程 |
| **kanban（看板视图）** | 筛选区 → 看板列 → 卡片列表 | 任务管理、工单流转 |
| **comparison（对比视图）** | 筛选条件 → 左右分栏对比区 | 数据对比、版本对比 |
| **approval（审批流页面）** | 搜索区 → 审批列表 → 审批操作弹窗 | 多步骤审批、多级审批 |
| **help（帮助/引导）** | 搜索框 → 分类导航 → 引导步骤/FAQ | Onboarding、帮助中心 |

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

### HTML 文件结构说明

每个 HTML 文件遵循统一布局框架（读取 `@wireframe-layout-templates.md#布局框架模板`）：
- 顶部导航 + 左侧菜单（显示完整菜单，当前模块高亮）+ 内容区（只包含该模块的页面）
- 每个页面用 `page-divider` 分隔，标注页面 ID
- CSS 样式使用本文件定义的共享样式规范

详细 HTML 模板见 `@wireframe-layout-templates.md`