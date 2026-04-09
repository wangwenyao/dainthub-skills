# 响应式断点策略

## 断点定义

```css
@theme {
  --breakpoint-sm:  640px;   /* 大手机横屏 */
  --breakpoint-md:  768px;   /* 平板 */
  --breakpoint-lg:  1024px;  /* 小笔记本 */
  --breakpoint-xl:  1280px;  /* 标准桌面（主要目标） */
  --breakpoint-2xl: 1536px;  /* 大屏显示器 */
}
```

## B端 SaaS 的响应式策略

B端产品的主要使用场景是**桌面端浏览器**，但移动端查看是真实需求（领导审批、数据查看）。

### 优先级

```
xl（1280px）> lg（1024px）> md（768px）> sm（移动端兼顾）
```

### 各断点适配策略

**xl / 2xl — 主力桌面端（重点打磨）**
- 侧边栏展开，完整导航
- 多列布局（仪表盘 4 列卡片，列表 + 详情 Split View）
- 表格显示全部列

**lg — 小屏笔记本**
- 侧边栏默认收起（仅图标），hover 展开
- 仪表盘 3 列卡片
- 表格隐藏次要列

**md — 平板**
- 侧边栏变为顶部导航或抽屉
- 单列布局，卡片堆叠
- 表格只显示核心列（3-4列），其余收入展开行

**sm / 默认 — 移动端**
- 底部 Tab 导航（最多 4 个）
- 完全单列，全宽卡片
- 表格变为卡片列表（每行数据变成一张卡片）
- 禁用复杂操作（批量、拖拽排序）

## 实用模式

### 响应式侧边栏

```vue
<template>
  <SidebarProvider :default-open="isDesktop">
    <AppSidebar :collapsible="isDesktop ? 'icon' : 'offcanvas'" />
    <main>...</main>
  </SidebarProvider>
</template>

<script setup lang="ts">
import { useMediaQuery } from '@vueuse/core'
const isDesktop = useMediaQuery('(min-width: 1024px)')
</script>
```

### 响应式表格（移动端降级为卡片）

```vue
<template>
  <!-- 桌面：表格 -->
  <DataTable v-if="isDesktop" :data="data" :columns="columns" />
  
  <!-- 移动端：卡片列表 -->
  <div v-else class="space-y-3">
    <Card v-for="item in data" :key="item.id">
      <CardContent class="pt-4">
        <!-- 关键信息展示 -->
      </CardContent>
    </Card>
  </div>
</template>
```

### 响应式仪表盘卡片网格

```html
<div class="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  <StatCard v-for="metric in metrics" :key="metric.title" v-bind="metric" />
</div>
```

## 容器最大宽度

```html
<!-- 标准页面内容容器 -->
<div class="mx-auto max-w-screen-xl px-6">
  <!-- 内容 -->
</div>

<!-- 宽内容区（表格、仪表盘） -->
<div class="mx-auto max-w-screen-2xl px-6">
  <!-- 内容 -->
</div>

<!-- 窄内容区（设置、表单） -->
<div class="mx-auto max-w-2xl px-6">
  <!-- 内容 -->
</div>
```
