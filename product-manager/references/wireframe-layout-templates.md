# 线框图布局模板

统一的布局结构和页面内容模板。所有样式通过 class 实现，CSS 定义见 `@workflows/wireframe-generation.md`。

---

## 一、布局框架模板

### 完整布局

```html
<div class="layout">
  
  <!-- 顶部导航栏 -->
  <div class="header">
    <div class="header-left">
      <div class="logo">[Logo]</div>
      <div class="system-name">[系统名称]</div>
    </div>
    <div class="header-right">
      <div class="user-text">[消息]</div>
      <div class="user-info">[用户]</div>
    </div>
  </div>
  
  <!-- 左侧菜单 -->
  <div class="sidebar">
    <!-- 菜单内容见下方模板 -->
  </div>
  
  <!-- 内容区 -->
  <div class="main">
    <!-- 页面内容见下方模板 -->
  </div>
  
</div>
```

### 左侧菜单模板

```html
<div class="sidebar">
  
  <div class="menu-item-home">
    首页
    <div class="interaction-small">→ P000</div>
  </div>
  
  <div class="menu-group">
    <div class="menu-group-title">商品管理</div>
    <div class="menu-item active">
      商品列表
      <div class="interaction-small">→ P001（当前页）</div>
    </div>
    <div class="menu-item">
      商品分类
      <div class="interaction-small">→ P002</div>
    </div>
  </div>
  
  <div class="menu-group">
    <div class="menu-group-title">订单管理</div>
    <div class="menu-item">
      订单列表
      <div class="interaction-small">→ P003</div>
    </div>
    <div class="menu-item">
      退款管理
      <div class="interaction-small">→ P004</div>
    </div>
  </div>
  
</div>
```

---

## 二、页面内容模板

### 列表页（list）

**结构**：搜索区 → 操作栏 → 表格 → 分页

```html
<div id="p001" class="page-divider">
  <div class="page-title">[页面名称] <span class="page-id">(P001)</span></div>
  
  <div class="wireframe">
    
    <!-- 搜索区 -->
    <div class="section">
      <div class="row">
        <div class="field input">[字段1]</div>
        <div class="field select">[字段2]</div>
        <div class="field date">[日期范围]</div>
        <div class="btn btn-primary">查询</div>
        <div class="btn">重置</div>
      </div>
      <div class="label">组件：搜索表单</div>
    </div>
    
    <!-- 操作栏 -->
    <div class="section">
      <div class="btn btn-primary">+ 新增</div>
      <div class="btn btn-margin-left">批量导出</div>
      <div class="interaction">点击新增 → 打开 [P002 表单弹窗]</div>
    </div>
    
    <!-- 数据表格（示例：1行数据） -->
    <div class="section-white">
      <table class="table">
        <tr>
          <th class="th th-checkbox">☐</th>
          <th class="th">[列1]</th>
          <th class="th">[列2]</th>
          <th class="th">[状态]</th>
          <th class="th">操作</th>
        </tr>
        <tr>
          <td class="td td-checkbox">☐</td>
          <td class="td">[数据]</td>
          <td class="td td-right">¥99.00</td>
          <td class="td"><div class="tag">[状态]</div></td>
          <td class="td">
            <div class="btn btn-small">编辑</div>
            <div class="btn btn-small btn-danger">删除</div>
          </td>
        </tr>
      </table>
      <div class="label-padding">组件：VxeGrid</div>
    </div>
    
    <!-- 分页 -->
    <div class="section">
      <div class="row-between">
        <span class="user-text">共 N 条</span>
        <div class="row-gap-sm">
          <div class="field field-small field-active">1</div>
          <div class="field field-small">2</div>
          <div class="field field-small">...</div>
        </div>
      </div>
    </div>
    
  </div>
</div>
```

### 表单弹窗（form-modal）

**结构**：弹窗头部 → 表单字段 → 弹窗底部

```html
<div id="p002" class="page-divider">
  <div class="page-title">[表单名称]弹窗 <span class="page-id">(P002)</span></div>
  
  <div class="modal">
    
    <!-- 弹窗头部 -->
    <div class="modal-header">
      <span class="modal-title">[表单标题]</span>
      <span class="modal-close">✕</span>
    </div>
    
    <!-- 表单内容（示例：4种字段类型） -->
    <div class="modal-body">
      
      <!-- 文本输入 -->
      <div class="form-group">
        <span class="form-label form-required">[文本字段]</span>
        <div class="field input field-full">[请输入]</div>
        <div class="label">组件：Input | 必填，max: 50</div>
      </div>
      
      <!-- 下拉选择 -->
      <div class="form-group">
        <span class="form-label form-required">[选择字段]</span>
        <div class="field select field-full">[请选择]</div>
        <div class="label">组件：ApiSelect | API: /api/xxx</div>
      </div>
      
      <!-- 数字输入（并列布局示例） -->
      <div class="form-group">
        <div class="form-flex">
          <div class="form-flex-item">
            <span class="form-label">[数字字段A]</span>
            <div class="field number field-full">0</div>
          </div>
          <div class="form-flex-item">
            <span class="form-label">[数字字段B]</span>
            <div class="field number field-full">0</div>
          </div>
        </div>
      </div>
      
      <!-- 多行文本 -->
      <div class="form-group">
        <span class="form-label">[备注字段]</span>
        <div class="field textarea field-full">[请输入备注]</div>
        <div class="label">组件：TextArea | max: 500</div>
      </div>
      
    </div>
    
    <!-- 弹窗底部 -->
    <div class="modal-footer">
      <div class="btn">取消</div>
      <div class="btn btn-primary btn-margin-left">确定</div>
    </div>
    
  </div>
</div>
```

**字段类型速查**：

| 字段类型 | class | YAML component |
|----------|-------|----------------|
| 文本输入 | `field input` | Input |
| 下拉选择 | `field select` | Select / ApiSelect |
| 数字输入 | `field number` | InputNumber |
| 多行文本 | `field textarea` | TextArea |
| 日期选择 | `field date` | DatePicker |
| 单选组 | `row-gap-sm` + `btn` | RadioGroup |
| 文件上传 | `image-group` | Upload |

### 详情页（detail）

**结构**：信息区（多个 section）→ 操作按钮

```html
<div id="p003" class="page-divider">
  <div class="page-title">[详情名称] <span class="page-id">(P003)</span></div>
  
  <div class="wireframe">
    
    <!-- 基本信息（示例：4行字段） -->
    <div class="detail-section">
      <div class="detail-title">基本信息</div>
      <div class="detail-row">
        <div class="detail-label">[字段A]：</div>
        <div class="detail-value">[数据]</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">[字段B]：</div>
        <div class="detail-value">¥99.00</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">[字段C]：</div>
        <div class="detail-value">100</div>
      </div>
      <div class="detail-row-last">
        <div class="detail-label">状态：</div>
        <div class="detail-value"><div class="tag">[状态]</div></div>
      </div>
    </div>
    
    <!-- 其他信息区（按需添加） -->
    <div class="detail-section">
      <div class="detail-title">[区块名称]</div>
      <div class="detail-content">[内容...]</div>
    </div>
    
    <!-- 操作按钮 -->
    <div class="section">
      <div class="row-right">
        <div class="btn">返回列表</div>
        <div class="btn btn-primary btn-margin-left">编辑</div>
      </div>
    </div>
    
  </div>
</div>
```

### 仪表盘（dashboard）

**结构**：筛选区 → 统计卡片 → 图表区

```html
<div id="p000" class="page-divider">
  <div class="page-title">数据概览 <span class="page-id">(P000)</span></div>
  
  <div class="wireframe">
    
    <!-- 筛选区 -->
    <div class="section">
      <div class="row">
        <div class="field select">[时间范围]</div>
        <div class="field select">[筛选条件]</div>
        <div class="btn btn-primary">刷新</div>
      </div>
    </div>
    
    <!-- 统计卡片（示例：2个） -->
    <div class="section-white">
      <div class="card-group">
        <div class="card">
          <div class="card-title">[指标A]</div>
          <div class="card-value">128</div>
        </div>
        <div class="card">
          <div class="card-title">[指标B]</div>
          <div class="card-value">¥9,980</div>
        </div>
      </div>
      <div class="label-padding">组件：统计卡片</div>
    </div>
    
    <!-- 图表区 -->
    <div class="section-white">
      <div class="chart-title">[图表标题]</div>
      <div class="chart-area">[图表占位区域]</div>
      <div class="label-padding">组件：图表（Line/Pie/Bar）</div>
    </div>
    
  </div>
</div>
```

---

## 三、交互标注模板

用于标注用户交互流程：

```html
<!-- 简单交互标注 -->
<div class="interaction">
  点击 → 打开 [P002 表单弹窗]
</div>

<!-- 菜单跳转标注 -->
<div class="interaction">
  → P001（点击跳转到商品列表页）
</div>

<!-- 详细交互标注 -->
<div class="interaction" style="display: block; padding: 8px; margin: 8px;">
  <div>用户操作：点击"新增"按钮</div>
  <div>触发：打开商品表单弹窗（P002）</div>
  <div>结果：弹窗显示表单，用户填写后点击确定保存</div>
</div>
```

---

## 四、确认弹窗模板（删除/批量操作）

**适用场景**：删除、批量删除、批量导出等需要用户确认的简单操作。

**特点**：不生成独立页面，只在 HTML 中用占位框表示确认弹窗的位置和内容。

### 确认弹窗模板

**适用场景**：删除、批量删除等简单确认操作。

```html
<!-- 确认弹窗（通用） -->
<div class="confirm-modal">
  <div class="confirm-content">
    <div class="confirm-icon">⚠️</div>
    <div class="confirm-title">[确认标题]</div>
    <div class="confirm-message">[确认消息内容]</div>
    <div class="confirm-actions">
      <div class="btn">取消</div>
      <div class="btn btn-danger">确认</div>
    </div>
  </div>
  <div class="label">触发：点击按钮 | 关闭：取消/确认后关闭</div>
</div>
```

**YAML 配置**：

```yaml
rowActions:
  - name: 删除
    type: danger
    confirm: true                   # 需要确认弹窗
    confirmTitle: 确认删除
    confirmMessage: 确认删除此数据？删除后不可恢复。
```

> **CSS 样式**：见 `@workflows/wireframe-generation.md` CSS 样式规范章节。

---

## 五、操作弹窗模板（业务操作类）

**适用场景**：业务特定的操作（审批、分配、转派等），需填写操作信息。

### 通用结构

```
┌─────────────────────────────────────┐
│ 弹窗标题                          ✕ │
├─────────────────────────────────────┤
│ 信息摘要区（可选）                  │
│ 操作选项区（按需）                  │
│ 操作信息区（按需）                  │
├─────────────────────────────────────┤
│                     取消    确认操作 │
└─────────────────────────────────────┘
```

### 通用模板

```html
<div id="p-action" class="page-divider">
  <div class="page-title">[操作名称]弹窗 <span class="page-id">(P-action)</span></div>
  
  <div class="modal">
    <div class="modal-header">
      <span class="modal-title">[操作标题]</span>
      <span class="modal-close">✕</span>
    </div>
    
    <div class="modal-body">
      
      <!-- 信息摘要区（可选） -->
      <div class="detail-section">
        <div class="detail-title">[对象信息]</div>
        <div class="detail-row-last">
          <div class="detail-label">[字段]：</div>
          <div class="detail-value">[值]</div>
        </div>
      </div>
      
      <!-- 操作选项区（按需：单选/下拉） -->
      <div class="form-group">
        <span class="form-label form-required">[选项]</span>
        <div class="row-gap-sm">
          <div class="btn btn-primary">[选项A]</div>
          <div class="btn">[选项B]</div>
        </div>
        <div class="label">组件：RadioGroup</div>
      </div>
      
      <!-- 操作信息区（按需：文本/备注） -->
      <div class="form-group">
        <span class="form-label">[填写内容]</span>
        <div class="field textarea field-full">[请填写]</div>
        <div class="label">组件：TextArea | max: 200</div>
      </div>
      
    </div>
    
    <div class="modal-footer">
      <div class="btn">取消</div>
      <div class="btn btn-primary btn-margin-left">确认[操作]</div>
    </div>
  </div>
</div>
```

### 字段组合规则

| 操作复杂度 | 字段组合 | 适用场景 |
|------------|----------|----------|
| 简单 | 信息摘要 + 备注（可选） | 撤回、取消 |
| 中等 | 信息摘要 + 选择对象 + 备注 | 分配、转派 |
| 复杂 | 信息摘要 + 选项 + 条件字段 + 备注 | 审批、状态变更 |

### YAML 配置模板

```yaml
P-action:
  name: [操作名称]弹窗
  type: action-modal
  config:
    modal: { title: [操作标题], width: 500px }
    summary: { fields: [{ name: [字段], field: [字段名] }] }
    action:
      type: [操作类型]          # 业务自定义
      options: [{ label: [选项A], value: [值A] }]
      fields:
        - { name: [字段], field: [字段名], component: TextArea, required: false }
```

## 版本

- v3.0
- 更新: 2026-04-12
- 精简: 所有模板减少冗余示例，提高信息密度
- 移除: CSS 部分统一到 wireframe-generation.md
- 优化: 操作弹窗只保留通用模板，去掉具体示例