# 表单组件 VbenForm

> Schema驱动的表单系统，支持验证、依赖联动

---

## 基础用法

```typescript
import { useVbenForm } from '#/adapter/form';

const [Form, formApi] = useVbenForm({
  schema: [
    { fieldName: 'name', label: '名称', component: 'Input', rules: 'required' },
    { fieldName: 'status', label: '状态', component: 'RadioGroup', componentProps: { options: [...] } },
  ],
  handleSubmit: (values) => {
    console.log(values);
  },
});
```

```vue
<template>
  <Form />
</template>
```

---

## VbenFormProps

```typescript
interface VbenFormProps {
  // 布局
  layout?: 'horizontal' | 'vertical' | 'inline';
  wrapperClass?: string;           // "grid-cols-1 md:grid-cols-2"
  labelWidth?: number;             // Label宽度
  compact?: boolean;               // 紧凑模式
  
  // Schema
  schema?: VbenFormSchema[];       // 字段定义
  
  // 折叠
  collapsed?: boolean;
  collapsedRows?: number;
  showCollapseButton?: boolean;
  
  // 操作按钮
  showDefaultActions?: boolean;
  submitButtonOptions?: { content: '提交' };
  resetButtonOptions?: { content: '重置' };
  
  // 回调
  handleSubmit?: (values) => void;
  handleReset?: (values) => void;
  handleValuesChange?: (values, fields) => void;
}
```

---

## FormSchema 字段定义

```typescript
interface VbenFormSchema {
  // 必填
  fieldName: string;               // 字段名
  component: string;               // 组件类型
  
  // 标签
  label?: string;
  help?: string;
  description?: string;
  
  // 组件
  componentProps?: object | ((values) => object);
  defaultValue?: any;
  
  // 验证
  rules?: 'required' | 'mobile' | ZodTypeAny;
  
  // 依赖联动
  dependencies?: {
    triggerFields: string[];
    show?: (values) => boolean;
    disabled?: (values) => boolean;
    required?: (values) => boolean;
    rules?: (values) => ZodTypeAny;
    componentProps?: (values) => object;
  };
  
  // 样式
  hide?: boolean;
  formItemClass?: string;
}
```

---

## 常用组件

### Input 输入框
```typescript
{
  fieldName: 'name',
  label: '名称',
  component: 'Input',
  componentProps: {
    placeholder: '请输入',
    allowClear: true,
    maxlength: 50,
  },
  rules: 'required',
}
```

### InputPassword 密码框
```typescript
{
  fieldName: 'password',
  label: '密码',
  component: 'InputPassword',
  componentProps: {
    passwordStrength: true,  // 显示强度
  },
  rules: z.string().min(6, '密码至少6位'),
}
```

### Select 选择器
```typescript
{
  fieldName: 'type',
  label: '类型',
  component: 'Select',
  componentProps: {
    options: [
      { label: '类型A', value: 1 },
      { label: '类型B', value: 2 },
    ],
    placeholder: '请选择',
    allowClear: true,
  },
}
```

### ApiSelect 远程选择
```typescript
{
  fieldName: 'deptId',
  label: '部门',
  component: 'ApiSelect',
  componentProps: {
    api: getDeptList,          // API函数
    labelField: 'name',        // 显示字段
    valueField: 'id',          // 值字段
    mode: 'multiple',          // 多选
    placeholder: '请选择',
  },
}
```

### ApiTreeSelect 远程树选择
```typescript
{
  fieldName: 'deptId',
  label: '部门',
  component: 'ApiTreeSelect',
  componentProps: {
    api: getDeptTree,
    labelField: 'name',
    valueField: 'id',
    childrenField: 'children',
    treeDefaultExpandAll: true,
  },
}
```

### RadioGroup 单选组
```typescript
{
  fieldName: 'status',
  label: '状态',
  component: 'RadioGroup',
  componentProps: {
    options: getDictOptions(DICT_TYPE.COMMON_STATUS, 'number'),
    buttonStyle: 'solid',
    optionType: 'button',
  },
  rules: z.number().default(0),
}
```

### DatePicker 日期选择
```typescript
{
  fieldName: 'date',
  label: '日期',
  component: 'DatePicker',
  componentProps: {
    format: 'YYYY-MM-DD',
    showTime: false,
  },
}
```

### RangePicker 日期范围
```typescript
{
  fieldName: 'dateRange',
  label: '日期范围',
  component: 'RangePicker',
  componentProps: {
    format: 'YYYY-MM-DD',
    allowClear: true,
  },
}
```

### Upload 上传
```typescript
{
  fieldName: 'file',
  label: '文件',
  component: 'Upload',
  componentProps: {
    accept: '.xlsx,.xls',
    multiple: false,
  },
  rules: 'required',
  help: '仅支持xlsx格式',
}
```

---

## 验证规则

### 内置规则
```typescript
rules: 'required'          // 必填
rules: 'mobile'            // 手机号
rules: 'mobileRequired'    // 必填手机号
rules: 'selectRequired'    // 下拉必选
```

### Zod规则
```typescript
import { z } from '#/adapter/form';

rules: z.string().min(2, '至少2个字符')
rules: z.string().email('邮箱格式错误')
rules: z.number().min(0).max(100)
rules: z.string().regex(/^1[3-9]\d{9}$/, '手机号格式错误')
```

### 动态规则
```typescript
{
  fieldName: 'password',
  dependencies: {
    triggerFields: ['confirmPassword'],
    rules: (values) => z.string().refine(
      v => v === values.confirmPassword,
      '两次密码不一致'
    ),
  },
}
```

---

## 依赖联动

### 显示/隐藏
```typescript
{
  fieldName: 'reason',
  label: '原因',
  component: 'Textarea',
  dependencies: {
    triggerFields: ['status'],
    show: (values) => values.status === 0,  // 禁用时显示
  },
}
```

### 禁用
```typescript
{
  fieldName: 'username',
  label: '用户名',
  component: 'Input',
  dependencies: {
    triggerFields: ['id'],
    disabled: (values) => !!values.id,  // 编辑时禁用
  },
}
```

### 动态选项
```typescript
{
  fieldName: 'city',
  label: '城市',
  component: 'Select',
  dependencies: {
    triggerFields: ['province'],
    componentProps: (values) => ({
      options: getCityOptions(values.province),
    }),
  },
}
```

---

## 表单API

```typescript
const [Form, formApi] = useVbenForm({ ... });

// 获取值
const values = await formApi.getValues();
const name = await formApi.getValues('name');

// 设置值
await formApi.setValues({ name: 'test' });
await formApi.setFieldValue('name', 'test');

// 验证
const { valid, errors } = await formApi.validate();
await formApi.validateField('name');

// 重置
await formApi.resetForm();

// 提交
await formApi.submitForm();

// 状态
const loading = formApi.form.loading;
const dirty = formApi.form.dirty;
```

---

## 完整示例

```typescript
const [Form, formApi] = useVbenForm({
  commonConfig: {
    componentProps: { class: 'w-full' },
    labelWidth: 100,
  },
  layout: 'horizontal',
  wrapperClass: 'grid-cols-1 md:grid-cols-2',
  schema: [
    {
      fieldName: 'id',
      component: 'Input',
      dependencies: { triggerFields: [''], show: () => false },
    },
    {
      fieldName: 'username',
      label: '用户名',
      component: 'Input',
      rules: 'required',
    },
    {
      fieldName: 'password',
      label: '密码',
      component: 'InputPassword',
      rules: 'required',
      dependencies: {
        triggerFields: ['id'],
        show: (values) => !values.id,  // 新增时显示
      },
    },
    {
      fieldName: 'deptId',
      label: '部门',
      component: 'ApiTreeSelect',
      componentProps: {
        api: getDeptTree,
        labelField: 'name',
        valueField: 'id',
        childrenField: 'children',
      },
    },
    {
      fieldName: 'status',
      label: '状态',
      component: 'RadioGroup',
      componentProps: {
        options: getDictOptions(DICT_TYPE.COMMON_STATUS, 'number'),
        optionType: 'button',
      },
      rules: z.number().default(1),
    },
    {
      fieldName: 'remark',
      label: '备注',
      component: 'Textarea',
      formItemClass: 'col-span-2',  // 占两列
    },
  ],
  showDefaultActions: false,
});
```