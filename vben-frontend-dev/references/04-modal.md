# 弹窗组件 Modal/Drawer

> API驱动的模态框和抽屉组件

---

## Modal 基础用法

```typescript
import { useVbenModal } from '@vben/common-ui';
import Form from './modules/form.vue';

const [FormModal, formModalApi] = useVbenModal({
  connectedComponent: Form,    // 连接的组件
  destroyOnClose: true,        // 关闭时销毁
});

// 打开
formModalApi.setData({ id: 1 }).open();

// 关闭
await formModalApi.close();
```

```vue
<template>
  <FormModal @success="handleRefresh" />
</template>
```

---

## Modal API

```typescript
const [Modal, modalApi] = useVbenModal({
  // 回调
  onConfirm: async () => {
    // 确认回调
    await modalApi.close();
  },
  onCancel: async () => {
    // 取消回调
    await modalApi.close();
  },
  onOpenChange: async (isOpen: boolean) => {
    if (isOpen) {
      const data = modalApi.getData();  // 获取传入数据
    }
  },
  
  // 配置
  destroyOnClose: true,
  closeOnPressEscape: true,
  closeOnClickModal: true,
});

// 方法
modalApi.open();                   // 打开
modalApi.close();                  // 关闭
modalApi.setData(data);            // 设置数据
modalApi.getData<T>();             // 获取数据
modalApi.lock();                   // 锁定(防止关闭)
modalApi.unlock();                 // 解锁
modalApi.setLoading(true);         // 加载状态
modalApi.setState({ title: '' });  // 设置状态
```

---

## Modal Props

```vue
<Modal
  title="标题"
  class="w-1/2"                    <!-- 宽度 -->
  :footer="true"                   <!-- 显示底部 -->
  :closable="true"                 <!-- 关闭按钮 -->
  :draggable="true"                <!-- 可拖拽 -->
  :fullscreen="false"              <!-- 全屏 -->
  :loading="false"                 <!-- 加载状态 -->
>
  内容
</Modal>
```

---

## 表单弹窗模式

**主页面**:
```typescript
const [FormModal, formModalApi] = useVbenModal({
  connectedComponent: Form,
  destroyOnClose: true,
});

function handleCreate() {
  formModalApi.setData(null).open();  // 新增
}

function handleEdit(row: any) {
  formModalApi.setData(row).open();   // 编辑
}
```

**表单组件** (`modules/form.vue`):
```vue
<script lang="ts" setup>
import { computed, ref } from 'vue';
import { useVbenModal, useVbenForm } from '@vben/common-ui';
import { createUser, getUser, updateUser } from '#/api';

const emit = defineEmits(['success']);
const formData = ref<any>();

const title = computed(() => formData.value?.id ? '编辑' : '新增');

const [Form, formApi] = useVbenForm({
  schema: [/* ... */],
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
    if (!isOpen) {
      formData.value = undefined;
      return;
    }
    
    const data = modalApi.getData();
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

## Drawer 抽屉

```typescript
import { useVbenDrawer } from '@vben/common-ui';

const [DetailDrawer, drawerApi] = useVbenDrawer({
  onOpenChange: async (isOpen) => {
    if (isOpen) {
      const data = drawerApi.getData();
      // 加载数据
    }
  },
});
```

```vue
<Drawer
  title="详情"
  class="w-1/3"
  :placement="'right'"
>
  内容
</Drawer>
```

---

## 多弹窗管理

```typescript
// 定义多个弹窗
const [FormModal, formModalApi] = useVbenModal({ connectedComponent: Form });
const [ResetPwdModal, resetPwdModalApi] = useVbenModal({ connectedComponent: ResetPwdForm });
const [ImportModal, importModalApi] = useVbenModal({ connectedComponent: ImportForm });

// 分别调用
function handleCreate() { formModalApi.setData(null).open(); }
function handleResetPwd(row: any) { resetPwdModalApi.setData(row).open(); }
function handleImport() { importModalApi.open(); }
```

```vue
<template>
  <FormModal @success="handleRefresh" />
  <ResetPwdModal @success="handleRefresh" />
  <ImportModal @success="handleRefresh" />
  <!-- ... -->
</template>
```