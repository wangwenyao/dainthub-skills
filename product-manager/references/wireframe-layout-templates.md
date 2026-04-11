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

```html
<div id="p001" class="page-divider">
  <div class="page-title">商品列表 <span class="page-id">(P001)</span></div>
  
  <div class="wireframe">
    
    <!-- 搜索区 -->
    <div class="section">
      <div class="row">
        <div class="field input">[商品名称]</div>
        <div class="field select">[商品分类]</div>
        <div class="field select">[状态]</div>
        <div class="field date">[创建时间]</div>
        <div class="btn btn-primary">查询</div>
        <div class="btn">重置</div>
      </div>
      <div class="label">组件：搜索表单</div>
    </div>
    
    <!-- 操作栏 -->
    <div class="section">
      <div class="btn btn-primary">+ 新增商品</div>
      <div class="btn btn-margin-left">批量导出</div>
      <div class="interaction">点击新增 → 打开 P002 商品表单弹窗</div>
      <div class="label">组件：操作栏</div>
    </div>
    
    <!-- 数据表格 -->
    <div class="section-white">
      <table class="table">
        <tr>
          <th class="th th-checkbox">☐</th>
          <th class="th">ID</th>
          <th class="th">商品名称</th>
          <th class="th">分类</th>
          <th class="th">价格</th>
          <th class="th">库存</th>
          <th class="th">状态</th>
          <th class="th">操作</th>
        </tr>
        <tr>
          <td class="td td-checkbox">☐</td>
          <td class="td">001</td>
          <td class="td">[商品名称数据]</td>
          <td class="td">[分类数据]</td>
          <td class="td td-right">¥99.00</td>
          <td class="td td-right">100</td>
          <td class="td"><div class="tag">上架</div></td>
          <td class="td">
            <div class="btn btn-small">编辑</div>
            <div class="btn btn-small btn-danger">删除</div>
          </td>
        </tr>
        <tr>
          <td class="td td-checkbox">☐</td>
          <td class="td">002</td>
          <td class="td">[商品名称数据]</td>
          <td class="td">[分类数据]</td>
          <td class="td td-right">¥199.00</td>
          <td class="td td-right">50</td>
          <td class="td"><div class="tag">草稿</div></td>
          <td class="td">
            <div class="btn btn-small">编辑</div>
            <div class="btn btn-small btn-danger">删除</div>
          </td>
        </tr>
      </table>
      <div class="label-padding">组件：数据表格（VxeGrid）</div>
    </div>
    
    <!-- 分页 -->
    <div class="section">
      <div class="row-between">
        <span class="user-text">共 128 条</span>
        <div class="row-gap-sm">
          <div class="field field-small field-active">1</div>
          <div class="field field-small">2</div>
          <div class="field field-small">3</div>
          <div class="field field-small">...</div>
        </div>
      </div>
      <div class="label">组件：分页器</div>
    </div>
    
  </div>
</div>
```

### 表单弹窗（form-modal）

```html
<div id="p002" class="page-divider">
  <div class="page-title">商品表单弹窗 <span class="page-id">(P002)</span></div>
  
  <div class="modal">
    
    <!-- 弹窗头部 -->
    <div class="modal-header">
      <span class="modal-title">商品信息</span>
      <span class="modal-close">✕</span>
    </div>
    
    <!-- 表单内容 -->
    <div class="modal-body">
      
      <div class="form-group">
        <span class="form-label form-required">商品名称</span>
        <div class="field input field-full">[请输入商品名称]</div>
        <div class="label">组件：Input | 规则：必填，1-50字符</div>
      </div>
      
      <div class="form-group">
        <span class="form-label form-required">商品分类</span>
        <div class="field select field-full">[请选择分类]</div>
        <div class="label">组件：ApiSelect | API: /api/categories</div>
      </div>
      
      <div class="form-group">
        <div class="form-flex">
          <div class="form-flex-item">
            <span class="form-label form-required">价格</span>
            <div class="field number field-full">0.00</div>
            <div class="label">组件：InputNumber | min: 0, 精度: 2位</div>
          </div>
          <div class="form-flex-item">
            <span class="form-label form-required">库存</span>
            <div class="field number field-full">0</div>
            <div class="label">组件：InputNumber | min: 0</div>
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <span class="form-label form-required">状态</span>
        <div class="row-gap-sm">
          <div class="btn btn-primary">草稿</div>
          <div class="btn">上架</div>
          <div class="btn">下架</div>
        </div>
        <div class="label">组件：RadioGroup</div>
      </div>
      
      <div class="form-group">
        <span class="form-label">商品图片</span>
        <div class="image-group">
          <div class="image-box">[图片1]</div>
          <div class="image-box">[图片2]</div>
          <div class="image-box-add">+</div>
        </div>
        <div class="label">组件：Upload | 最多5张，jpg/png，≤2MB</div>
      </div>
      
      <div class="form-group">
        <span class="form-label">商品描述</span>
        <div class="field textarea field-full">[请输入商品描述，最多500字]</div>
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

### 详情页（detail）

```html
<div id="p003" class="page-divider">
  <div class="page-title">商品详情 <span class="page-id">(P003)</span></div>
  
  <div class="wireframe">
    
    <!-- 基本信息 -->
    <div class="detail-section">
      <div class="detail-title">基本信息</div>
      <div class="detail-row">
        <div class="detail-label">商品ID：</div>
        <div class="detail-value">001</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">商品名称：</div>
        <div class="detail-value">[商品名称数据]</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">商品分类：</div>
        <div class="detail-value">[分类数据]</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">价格：</div>
        <div class="detail-value">¥99.00</div>
      </div>
      <div class="detail-row">
        <div class="detail-label">库存：</div>
        <div class="detail-value">100</div>
      </div>
      <div class="detail-row-last">
        <div class="detail-label">状态：</div>
        <div class="detail-value"><div class="tag">上架</div></div>
      </div>
    </div>
    
    <!-- 商品图片 -->
    <div class="detail-section">
      <div class="detail-title">商品图片</div>
      <div class="row-gap-lg">
        <div class="image-large">[图片1]</div>
        <div class="image-large">[图片2]</div>
        <div class="image-large">[图片3]</div>
      </div>
    </div>
    
    <!-- 商品描述 -->
    <div class="detail-section">
      <div class="detail-title">商品描述</div>
      <div class="detail-content">[商品描述内容...]</div>
    </div>
    
    <!-- 操作按钮 -->
    <div class="section">
      <div class="row-right">
        <div class="btn">返回列表</div>
        <div class="btn btn-primary btn-margin-left">编辑</div>
      </div>
      <div class="interaction">点击编辑 → 打开 P002 商品表单弹窗</div>
    </div>
    
  </div>
</div>
```

### 仪表盘（dashboard）

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
      <div class="label">组件：筛选区</div>
    </div>
    
    <!-- 统计卡片 -->
    <div class="section-white">
      <div class="card-group">
        <div class="card">
          <div class="card-title">今日订单</div>
          <div class="card-value">128</div>
        </div>
        <div class="card">
          <div class="card-title">今日销售额</div>
          <div class="card-value">¥9,980</div>
        </div>
        <div class="card">
          <div class="card-title">新增用户</div>
          <div class="card-value">32</div>
        </div>
      </div>
      <div class="label-padding">组件：统计卡片</div>
    </div>
    
    <!-- 图表区 -->
    <div class="section-white">
      <div class="chart-title">销售趋势</div>
      <div class="chart-area">[图表占位区域]</div>
      <div class="label-padding">组件：图表（Line）</div>
    </div>
    
    <div class="section-white">
      <div class="chart-title">分类占比</div>
      <div class="chart-area">[图表占位区域]</div>
      <div class="label-padding">组件：图表（Pie）</div>
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

## 版本

- v2.0
- 更新: 2026-04-11（移除内联 style，统一使用 class）