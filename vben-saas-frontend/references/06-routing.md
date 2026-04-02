# 路由与权限

> 路由配置与权限控制

---

## 路由结构

```
apps/web-antd/src/router/
├── index.ts           # 路由入口
├── guard.ts           # 路由守卫
├── access.ts          # 权限处理
└── routes/
    ├── index.ts       # 路由聚合
    ├── core.ts        # 核心路由
    └── modules/       # 业务路由
        ├── system.ts
        └── ...
```

---

## 添加静态路由

**routes/modules/wellness.ts**:
```typescript
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/wellness',
    name: 'Wellness',
    component: () => import('#/layouts/basic.vue'),
    meta: {
      title: '康养管理',
      icon: 'ant-design:heart-filled',
      order: 1,
    },
    children: [
      {
        path: 'resident',
        name: 'ResidentList',
        component: () => import('#/views/wellness/resident/index.vue'),
        meta: {
          title: '住户管理',
          icon: 'ant-design:user-outlined',
          authority: ['wellness:resident:list'],
        },
      },
      {
        path: 'resident/:id',
        name: 'ResidentDetail',
        component: () => import('#/views/wellness/resident/detail.vue'),
        meta: {
          title: '住户详情',
          hideInMenu: true,
          activeMenu: '/wellness/resident',
        },
      },
    ],
  },
];

export default routes;
```

---

## 路由Meta配置

```typescript
interface RouteMeta {
  title: string;                   // 菜单标题
  icon?: string;                   // 菜单图标
  order?: number;                  // 排序
  hideInMenu?: boolean;            // 菜单中隐藏
  hideChildrenInMenu?: boolean;    // 隐藏子菜单
  hideInBreadcrumb?: boolean;      // 面包屑隐藏
  hideInTab?: boolean;             // 标签页隐藏
  keepAlive?: boolean;             // 缓存页面
  authority?: string[];            // 权限码
  activeMenu?: string;             // 高亮菜单
  ignoreAuth?: boolean;            // 忽略权限
  frameSrc?: string;               // iframe地址
}
```

---

## 权限模式

```typescript
// preferences.ts
app: {
  accessMode: 'backend',  // 'frontend' | 'backend' | 'mixed'
}
```

| 模式 | 说明 |
|------|------|
| `frontend` | 前端路由 + 按钮权限 |
| `backend` | 后端返回菜单 + 权限 |
| `mixed` | 混合模式 |

---

## 按钮权限

### 方式1: TableAction
```vue
<TableAction
  :actions="[
    {
      label: '编辑',
      auth: ['system:user:update'],
      onClick: handleEdit,
    },
  ]"
/>
```

### 方式2: v-access指令
```vue
<Button v-access:code="'system:user:create'">新增</Button>
```

### 方式3: 函数判断
```vue
<script setup>
import { useAccess } from '@vben/access';
const { hasAccessByCodes } = useAccess();
</script>

<template>
  <Button v-if="hasAccessByCodes(['system:user:create'])">新增</Button>
</template>
```

---

## 权限Store

```typescript
import { useAccessStore } from '@vben/stores';

const accessStore = useAccessStore();

// 权限码列表
const codes = accessStore.accessCodes;

// 菜单列表
const menus = accessStore.accessMenus;

// 检查权限
const hasPermission = accessStore.hasAccessByCodes(['system:user:create']);
```

---

## 动态路由

后端返回菜单数据格式:
```json
{
  "name": "ResidentList",
  "path": "/wellness/resident",
  "component": "wellness/resident/index",
  "meta": {
    "title": "住户管理",
    "icon": "ant-design:user-outlined",
    "authority": ["wellness:resident:list"]
  }
}
```

前端自动转换为路由。

---

## 常见场景

### 隐藏菜单项
```typescript
meta: {
  hideInMenu: true,
}
```

### 详情页高亮父菜单
```typescript
meta: {
  hideInMenu: true,
  activeMenu: '/wellness/resident',  // 高亮住户管理
}
```

### 外链
```typescript
meta: {
  frameSrc: 'https://example.com',
}
```

### 忽略权限
```typescript
meta: {
  ignoreAuth: true,
}
```