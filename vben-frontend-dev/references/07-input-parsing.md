# 输入解析：YAML 页面规格与 HTML 线框图

Vben 前端开发支持三种输入方式，按优先级排列：

```
YAML 页面规格 > HTML 线框图 > 关键词推断
```

---

## 一、YAML → Schema 转换

当输入包含 YAML 页面规格时，直接读取生成 Schema：

```typescript
// 读取 YAML 页面规格
const pageSpec = parseYaml(input.yaml_page_spec);

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

---

## 二、HTML 线框图解析

当输入包含 HTML+CSS 线框图时，解析 class → 组件映射：

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

### 解析逻辑

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

### CSS 样式处理

**线框图 CSS 是灰色示意，不是真实样式**：

```css
/* 线框图 CSS - 不应用 */
.wireframe { border: 1px dashed #999; background: #f5f5f5; }
.field { border: 1px solid #999; background: #fff; color: #999; }
.btn-primary { background: #aaa; }  /* 灰色，不是真实主色 */
```

线框图 CSS 只用于识别结构，不直接应用到生成的代码中。生成代码使用 Vben 框架默认样式。

---

## 版本

- v1.0
- 更新: 2026-04-11
