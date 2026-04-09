# 页面开发模式

> 标准化的列表页、详情页、表单页模板

---

## 文件结构

```
views/module/feature/
├── index.vue           # 列表页
├── data.ts             # Schema定义
└── modules/
    ├── form.vue        # 新增/编辑表单
    ├── detail.vue      # 详情页
    └── import-form.vue # 导入表单
```

---

## 列表页模板

**index.vue**:
```vue
<script lang="ts" setup>
import type { VxeTableGridOptions } from '#/adapter/vxe-table';
import type { UserApi } from '#/api/system/user';

import { Page, useVbenModal } from '@vben/common-ui';
import { useVbenVxeGrid, TableAction, ACTION_ICON } from '#/adapter/vxe-table';
import { getUserPage, deleteUser, updateUserStatus } from '#/api/system/user';
import { useGridColumns, useGridFormSchema } from './data';
import Form from './modules/form.vue';

// Modal
const [FormModal, formModalApi] = useVbenModal({
  connectedComponent: Form,
  destroyOnClose: true,
});

// Grid
const [Grid, gridApi] = useVbenVxeGrid({
  formOptions: { schema: useGridFormSchema() },
  gridOptions: {
    columns: useGridColumns(handleStatusChange),
    height: 'auto',
    keepSource: true,
    proxyConfig: {
      ajax: {
        query: async ({ page }, formValues) => {
          return await getUserPage({
            pageNo: page.currentPage,
            pageSize: page.pageSize,
            ...formValues,
          });
        },
      },
    },
    rowConfig: { keyField: 'id', isHover: true },
    toolbarConfig: { refresh: true, search: true },
  } as VxeTableGridOptions<UserApi.User>,
});

// 操作
function handleRefresh() { gridApi.query(); }
function handleCreate() { formModalApi.setData(null).open(); }
function handleEdit(row: UserApi.User) { formModalApi.setData(row).open(); }
async function handleDelete(row: UserApi.User) {
  await deleteUser(row.id!);
  handleRefresh();
}
async function handleStatusChange(newStatus: number, row: UserApi.User) {
  await updateUserStatus(row.id!, newStatus);
  return true;
}
</script>

<template>
  <Page auto-content-height>
    <FormModal @success="handleRefresh" />
    
    <Grid table-title="用户列表">
      <template #toolbar-tools>
        <TableAction :actions="[
          { label: '新增', type: 'primary', icon: ACTION_ICON.ADD, onClick: handleCreate },
        ]" />
      </template>
      
      <template #actions="{ row }">
        <TableAction :actions="[
          { label: '编辑', type: 'link', onClick: handleEdit.bind(null, row) },
          { label: '删除', type: 'link', danger: true, popConfirm: { title: '确认删除？', confirm: handleDelete.bind(null, row) } },
        ]" />
      </template>
    </Grid>
  </Page>
</template>
```

---

## Schema定义模板

**data.ts**:
```typescript
import type { VbenFormSchema } from '#/adapter/form';
import type { VxeTableGridOptions } from '#/adapter/vxe-table';

import { z } from '#/adapter/form';
import { DICT_TYPE } from '@vben/constants';
import { getDictOptions } from '@vben/hooks';

// 新增/编辑表单
export function useFormSchema(): VbenFormSchema[] {
  return [
    { component: 'Input', fieldName: 'id', dependencies: { triggerFields: [''], show: () => false } },
    { fieldName: 'username', label: '用户名', component: 'Input', rules: 'required' },
    { fieldName: 'password', label: '密码', component: 'InputPassword', rules: 'required', dependencies: { triggerFields: ['id'], show: (v) => !v.id } },
    { fieldName: 'deptId', label: '部门', component: 'ApiTreeSelect', componentProps: { api: getDeptTree, labelField: 'name', valueField: 'id', childrenField: 'children' } },
    { fieldName: 'status', label: '状态', component: 'RadioGroup', componentProps: { options: getDictOptions(DICT_TYPE.COMMON_STATUS, 'number'), optionType: 'button' }, rules: z.number().default(1) },
    { fieldName: 'remark', label: '备注', component: 'Textarea', formItemClass: 'col-span-2' },
  ];
}

// 搜索表单
export function useGridFormSchema(): VbenFormSchema[] {
  return [
    { fieldName: 'username', label: '用户名', component: 'Input', componentProps: { allowClear: true } },
    { fieldName: 'createTime', label: '创建时间', component: 'RangePicker', componentProps: { allowClear: true } },
  ];
}

// 列定义
export function useGridColumns(onStatusChange?: Function): VxeTableGridOptions['columns'] {
  return [
    { type: 'checkbox', width: 40 },
    { field: 'id', title: 'ID', width: 80 },
    { field: 'username', title: '用户名', minWidth: 120 },
    { field: 'nickname', title: '昵称', minWidth: 120 },
    { field: 'status', title: '状态', width: 100, cellRender: { name: 'CellSwitch', attrs: { beforeChange: onStatusChange } } },
    { field: 'createTime', title: '创建时间', minWidth: 180, formatter: 'formatDateTime' },
    { title: '操作', width: 180, fixed: 'right', slots: { default: 'actions' } },
  ];
}
```

---

## 表单弹窗模板

**modules/form.vue**:
```vue
<script lang="ts" setup>
import type { UserApi } from '#/api/system/user';

import { computed, ref } from 'vue';
import { useVbenModal, useVbenForm } from '@vben/common-ui';
import { message } from 'ant-design-vue';
import { createUser, getUser, updateUser } from '#/api/system/user';
import { useFormSchema } from '../data';

const emit = defineEmits(['success']);
const formData = ref<UserApi.User>();

const title = computed(() => formData.value?.id ? '编辑用户' : '新增用户');

const [Form, formApi] = useVbenForm({
  commonConfig: { componentProps: { class: 'w-full' }, labelWidth: 80 },
  schema: useFormSchema(),
  showDefaultActions: false,
});

const [Modal, modalApi] = useVbenModal({
  async onConfirm() {
    const { valid } = await formApi.validate();
    if (!valid) return;
    
    modalApi.lock();
    const data = await formApi.getValues();
    try {
      await (formData.value?.id ? updateUser(data) : createUser(data));
      await modalApi.close();
      emit('success');
      message.success('操作成功');
    } finally {
      modalApi.unlock();
    }
  },
  async onOpenChange(isOpen: boolean) {
    if (!isOpen) { formData.value = undefined; return; }
    
    const data = modalApi.getData<UserApi.User>();
    if (data?.id) {
      modalApi.lock();
      try {
        formData.value = await getUser(data.id);
        await formApi.setValues(formData.value);
      } finally {
        modalApi.unlock();
      }
    }
  },
});
</script>

<template>
  <Modal :title="title" class="w-1/3">
    <Form class="mx-4" />
  </Modal>
</template>
```

---

## API集成模式

**api/system/user/user.ts**:
```typescript
import { defHttp } from '#/utils/http/axios';

export namespace UserApi {
  export interface User {
    id?: number;
    username: string;
    nickname: string;
    status: number;
    createTime?: string;
  }
}

// 分页查询
export function getUserPage(params: any) {
  return defHttp.get<{ list: UserApi.User[]; total: number }>({
    url: '/system/user/page',
    params,
  });
}

// 详情
export function getUser(id: number) {
  return defHttp.get<UserApi.User>({
    url: `/system/user/get?id=${id}`,
  });
}

// 创建
export function createUser(data: UserApi.User) {
  return defHttp.post({ url: '/system/user/create', data });
}

// 更新
export function updateUser(data: UserApi.User) {
  return defHttp.put({ url: '/system/user/update', data });
}

// 删除
export function deleteUser(id: number) {
  return defHttp.delete({ url: `/system/user/delete?id=${id}` });
}
```

---

## 常见页面变体

### 树形筛选 + 列表
```vue
<template>
  <Page auto-content-height>
    <div class="flex h-full w-full">
      <!-- 左侧树 -->
      <Card class="mr-4 h-full w-1/4">
        <DeptTree @select="handleDeptSelect" />
      </Card>
      <!-- 右侧列表 -->
      <div class="w-3/4">
        <Grid table-title="列表">...</Grid>
      </div>
    </div>
  </Page>
</template>
```

### 标签页切换
```vue
<template>
  <Page auto-content-height>
    <Tabs v-model:activeKey="activeKey">
      <TabPane key="1" tab="待处理">
        <Grid1 />
      </TabPane>
      <TabPane key="2" tab="已完成">
        <Grid2 />
      </TabPane>
    </Tabs>
  </Page>
</template>
```

### 详情页
```vue
<template>
  <Page>
    <template #title>
      <Button @click="router.back()">返回</Button>
      <span>详情标题</span>
    </template>
    
    <Card class="mb-4">
      <Descriptions :column="3">...</Descriptions>
    </Card>
    
    <Card>
      <Tabs>...</Tabs>
    </Card>
  </Page>
</template>
```