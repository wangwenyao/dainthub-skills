# 表格组件 VxeGrid

> 基于 VxeTable 封装，集成搜索、分页、工具栏

---

## 基础用法

```typescript
import { useVbenVxeGrid, TableAction, ACTION_ICON } from '#/adapter/vxe-table';

const [Grid, gridApi] = useVbenVxeGrid({
  formOptions: {
    schema: [
      { fieldName: 'name', label: '名称', component: 'Input' },
    ],
  },
  gridOptions: {
    columns: [
      { type: 'checkbox', width: 40 },
      { field: 'id', title: 'ID', width: 80 },
      { field: 'name', title: '名称', minWidth: 120 },
      { title: '操作', width: 180, slots: { default: 'actions' } },
    ],
    proxyConfig: {
      ajax: {
        query: async ({ page }, formValues) => {
          const res = await getList({
            pageNo: page.currentPage,
            pageSize: page.pageSize,
            ...formValues,
          });
          return { list: res.list, total: res.total };
        },
      },
    },
  },
});
```

```vue
<template>
  <Grid table-title="数据列表">
    <template #actions="{ row }">
      <TableAction :actions="[
        { label: '编辑', onClick: () => handleEdit(row) },
      ]" />
    </template>
  </Grid>
</template>
```

---

## VxeGridProps

```typescript
interface VxeGridProps {
  // 标题
  tableTitle?: string;
  tableTitleHelp?: string;
  
  // 搜索表单
  formOptions?: VbenFormProps;
  showSearchForm?: boolean;
  
  // 表格
  gridOptions?: VxeTableGridOptions;
  gridEvents?: VxeGridListeners;
  gridClass?: string;
  
  // 其他
  separator?: boolean;
  class?: string;
}
```

---

## GridOptions 核心配置

```typescript
interface VxeTableGridOptions {
  // 列定义
  columns: VxeTableColumn[];
  
  // 数据代理
  proxyConfig: {
    ajax: {
      query: async ({ page }, formValues) => ({ list: [], total: 0 });
      delete?: async ({ body }) => {};
      save?: async ({ body }) => {};
    };
    autoLoad?: boolean;
  };
  
  // 行配置
  rowConfig: {
    keyField: 'id';
    isHover: boolean;
    isCurrent?: boolean;
  };
  
  // 复选框
  checkboxConfig?: {
    reserve?: boolean;
    highlight?: boolean;
  };
  
  // 工具栏
  toolbarConfig: {
    refresh?: boolean;
    search?: boolean;
    zoom?: boolean;
    custom?: boolean;
  };
  
  // 分页
  pagerConfig?: {
    enabled?: boolean;
    pageSize?: number;
    pageSizes?: number[];
  };
  
  // 其他
  height?: 'auto' | number;
  keepSource?: boolean;
  showOverflow?: boolean;
  stripe?: boolean;
  border?: boolean;
}
```

---

## 列定义

### 基础列
```typescript
columns: [
  { type: 'checkbox', width: 40 },
  { type: 'seq', title: '序号', width: 60 },
  { field: 'id', title: 'ID', width: 80 },
  { field: 'name', title: '名称', minWidth: 120 },
  { field: 'createTime', title: '创建时间', minWidth: 180, formatter: 'formatDateTime' },
]
```

### 操作列
```typescript
{
  title: '操作',
  width: 180,
  fixed: 'right',
  slots: { default: 'actions' },
}
```

### 自定义渲染

**开关**
```typescript
{
  field: 'status',
  title: '状态',
  width: 100,
  cellRender: {
    name: 'CellSwitch',
    attrs: { beforeChange: handleStatusChange },
    props: {
      checkedValue: 1,
      unCheckedValue: 0,
    },
  },
}
```

**标签**
```typescript
{
  field: 'type',
  title: '类型',
  cellRender: {
    name: 'CellTag',
    props: {
      options: [
        { value: 1, label: '类型A', type: 'success' },
        { value: 2, label: '类型B', type: 'warning' },
      ],
    },
  },
}
```

**链接**
```typescript
{
  field: 'name',
  title: '名称',
  cellRender: {
    name: 'CellLink',
    events: { click: ({ row }) => handleDetail(row) },
  },
}
```

---

## 数据代理

### 分页查询
```typescript
proxyConfig: {
  ajax: {
    query: async ({ page }, formValues) => {
      const res = await getList({
        pageNo: page.currentPage,
        pageSize: page.pageSize,
        ...formValues,
      });
      // 必须返回此格式
      return { list: res.list, total: res.total };
    },
  },
}
```

### 删除
```typescript
proxyConfig: {
  ajax: {
    delete: async ({ body }) => {
      await deleteItem(body.id);
    },
  },
}
```

---

## 表格API

```typescript
const [Grid, gridApi] = useVbenVxeGrid({ ... });

// 刷新
gridApi.query();                    // 刷新当前页
gridApi.reload();                   // 重新加载
gridApi.reload({ name: 'test' });   // 带条件重新加载

// 获取数据
const data = gridApi.getData();     // 当前页数据
const records = gridApi.getSelectRows();  // 选中行
const record = gridApi.getSelectRow();    // 当前行

// 表单
const formValues = await gridApi.formApi.getValues();
await gridApi.formApi.resetForm();

// 分页
gridApi.setPage(1, 20);
const page = gridApi.getPageInfo();

// 状态
gridApi.setLoading(true);
gridApi.clearSelection();
```

---

## 搜索表单

```typescript
const [Grid, gridApi] = useVbenVxeGrid({
  formOptions: {
    schema: [
      {
        fieldName: 'name',
        label: '名称',
        component: 'Input',
        componentProps: { placeholder: '请输入', allowClear: true },
      },
      {
        fieldName: 'status',
        label: '状态',
        component: 'Select',
        componentProps: {
          options: getDictOptions(DICT_TYPE.COMMON_STATUS),
          allowClear: true,
        },
      },
      {
        fieldName: 'createTime',
        label: '创建时间',
        component: 'RangePicker',
        componentProps: { allowClear: true },
      },
    ],
    showCollapseButton: true,  // 显示折叠按钮
  },
  gridOptions: { ... },
});
```

---

## 工具栏按钮

```vue
<Grid table-title="用户列表">
  <template #toolbar-tools>
    <TableAction
      :actions="[
        {
          label: '新增',
          type: 'primary',
          icon: ACTION_ICON.ADD,
          auth: ['system:user:create'],
          onClick: handleCreate,
        },
        {
          label: '导出',
          type: 'primary',
          icon: ACTION_ICON.DOWNLOAD,
          auth: ['system:user:export'],
          onClick: handleExport,
        },
      ]"
    />
  </template>
</Grid>
```

---

## 行操作按钮

```vue
<template #actions="{ row }">
  <TableAction
    :actions="[
      {
        label: '编辑',
        type: 'link',
        icon: ACTION_ICON.EDIT,
        auth: ['system:user:update'],
        onClick: handleEdit.bind(null, row),
      },
      {
        label: '删除',
        type: 'link',
        danger: true,
        icon: ACTION_ICON.DELETE,
        auth: ['system:user:delete'],
        popConfirm: {
          title: '确认删除？',
          confirm: handleDelete.bind(null, row),
        },
      },
    ]"
    :drop-down-actions="[
      {
        label: '分配角色',
        type: 'link',
        auth: ['system:user:assign'],
        onClick: handleAssignRole.bind(null, row),
      },
    ]"
  />
</template>
```

---

## 完整示例

```vue
<script lang="ts" setup>
import { useVbenVxeGrid, TableAction, ACTION_ICON } from '#/adapter/vxe-table';
import { getUserPage, deleteUser, updateUserStatus } from '#/api/system/user';

// 状态变更
async function handleStatusChange(newStatus: number, row: any) {
  await updateUserStatus(row.id, newStatus);
  return true;
}

// 列定义
const columns = [
  { type: 'checkbox', width: 40 },
  { field: 'id', title: 'ID', width: 80 },
  { field: 'username', title: '用户名', minWidth: 120 },
  { field: 'nickname', title: '昵称', minWidth: 120 },
  {
    field: 'status',
    title: '状态',
    width: 100,
    cellRender: {
      name: 'CellSwitch',
      attrs: { beforeChange: handleStatusChange },
    },
  },
  { field: 'createTime', title: '创建时间', minWidth: 180, formatter: 'formatDateTime' },
  { title: '操作', width: 180, fixed: 'right', slots: { default: 'actions' } },
];

// 表格
const [Grid, gridApi] = useVbenVxeGrid({
  formOptions: {
    schema: [
      { fieldName: 'username', label: '用户名', component: 'Input' },
      { fieldName: 'createTime', label: '创建时间', component: 'RangePicker' },
    ],
  },
  gridOptions: {
    columns,
    height: 'auto',
    proxyConfig: {
      ajax: {
        query: async ({ page }, formValues) => {
          const res = await getUserPage({ pageNo: page.currentPage, pageSize: page.pageSize, ...formValues });
          return { list: res.list, total: res.total };
        },
      },
    },
    rowConfig: { keyField: 'id', isHover: true },
    toolbarConfig: { refresh: true, search: true },
  },
});

// 操作
function handleCreate() { /* ... */ }
function handleEdit(row: any) { /* ... */ }
async function handleDelete(row: any) {
  await deleteUser(row.id);
  gridApi.query();
}
</script>

<template>
  <Grid table-title="用户列表">
    <template #toolbar-tools>
      <TableAction :actions="[
        { label: '新增', type: 'primary', icon: ACTION_ICON.ADD, onClick: handleCreate },
      ]" />
    </template>
    <template #actions="{ row }">
      <TableAction :actions="[
        { label: '编辑', type: 'link', onClick: () => handleEdit(row) },
        { label: '删除', type: 'link', danger: true, popConfirm: { title: '确认删除？', confirm: () => handleDelete(row) } },
      ]" />
    </template>
  </Grid>
</template>
```