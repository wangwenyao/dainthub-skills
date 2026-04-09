# 复杂组件规范

专业 SaaS 应用中的高级交互组件规范，参考 Linear、Notion、GitHub 等产品。

---

## 一、命令面板（Command Palette）

### 交互规范

| 项目 | 规范 |
|------|------|
| 触发方式 | `⌘K`（Mac）/ `Ctrl+K`（Windows） |
| 关闭方式 | `Esc` 键或点击遮罩层 |
| 键盘导航 | `↑↓` 选择项目，`Enter` 执行，`Esc` 返回上级 |
| 搜索 | 实时过滤，支持拼音首字母 |
| 分组 | Recent（最近）、Actions（操作）、Navigation（导航）、Settings（设置） |

### 视觉规范

```
宽度：max-w-lg（512px）
圆角：rounded-lg（8px）
阴影：shadow-lg
背景：bg-elevated（neutral-0）
边框：border border-neutral-200
动画：fade-in + scale(95%→100%)，150ms
```

### Vue 3 + Tailwind 示例

```vue
<template>
  <DialogRoot v-model:open="open">
    <DialogTrigger as-child>
      <button class="flex items-center gap-2 px-3 py-1.5 text-sm text-neutral-500 bg-neutral-100 rounded-md hover:bg-neutral-200">
        <Search class="w-4 h-4" /><span>搜索...</span>
        <kbd class="ml-auto px-1.5 py-0.5 text-xs bg-neutral-200 rounded">⌘K</kbd>
      </button>
    </DialogTrigger>
    <DialogContent class="max-w-lg p-0 overflow-hidden">
      <div class="flex items-center gap-3 px-4 py-3 border-b border-neutral-200">
        <Search class="w-4 h-4 text-neutral-400" />
        <input v-model="query" placeholder="搜索命令或跳转..." class="flex-1 text-sm bg-transparent outline-none" />
      </div>
      <div class="max-h-80 overflow-y-auto">
        <div v-for="group in filteredGroups" :key="group.label" class="py-2">
          <div class="px-4 py-1.5 text-xs text-neutral-500 font-medium">{{ group.label }}</div>
          <button v-for="item in group.items" :key="item.id" class="w-full flex items-center gap-3 px-4 py-2 text-sm hover:bg-neutral-100">
            <component :is="item.icon" class="w-4 h-4 text-neutral-500" />
            <span>{{ item.label }}</span>
            <kbd v-if="item.shortcut" class="ml-auto text-xs text-neutral-400">{{ item.shortcut }}</kbd>
          </button>
        </div>
      </div>
    </DialogContent>
  </DialogRoot>
</template>
```

---

## 二、行内编辑（Inline Edit）

### 交互规范

| 项目 | 规范 |
|------|------|
| 触发方式 | 单击文字 或 悬停显示编辑图标后点击 |
| 保存方式 | 失焦自动保存 或 显式保存按钮（重要字段） |
| 取消方式 | `Esc` 键取消编辑，恢复原值 |
| 验证反馈 | 行内错误提示，输入框边框变红 |
| 加载态 | 保存时显示 spinner，禁用输入框 |

### 视觉规范

```
显示态：hover 时显示浅灰背景，cursor: text
编辑态：输入框无边框，仅底部蓝色线或完整边框
错误态：border-danger-500 + 下方 error text
过渡：background-color 150ms
```

### Vue 3 + Tailwind 示例

```vue
<template>
  <div class="group relative" @mouseenter="showIcon = true" @mouseleave="showIcon = false">
    <div v-if="!editing" @click="startEdit" class="px-2 py-1 -mx-2 rounded hover:bg-neutral-100 cursor-text">
      <span :class="{ 'text-neutral-400': !modelValue }">{{ modelValue || placeholder }}</span>
      <Pencil v-if="showIcon" class="inline w-3.5 h-3.5 ml-2 text-neutral-400" />
    </div>
    <div v-else class="flex items-center gap-2">
      <input v-model="tempValue" @blur="save" @keydown.esc="cancel" @keydown.enter="save"
             class="flex-1 px-2 py-1 -mx-2 bg-white border border-neutral-200 rounded focus:border-brand-500 outline-none" />
      <Loader2 v-if="loading" class="w-4 h-4 animate-spin text-neutral-400" />
    </div>
    <p v-if="error" class="mt-1 text-xs text-danger-500">{{ error }}</p>
  </div>
</template>
```

---

## 三、多列排序/筛选面板

### 交互规范

| 项目 | 规范 |
|------|------|
| 布局 | 侧边栏抽屉 或 下拉面板 |
| 筛选类型 | 文本输入、下拉选择、日期范围、多选标签 |
| 激活筛选 | 顶部显示筛选标签（chips），支持单独移除 |
| 清空操作 | "清除全部"按钮，一键重置 |
| URL 同步 | 筛选条件同步到 URL query 参数，支持分享链接 |

### 视觉规范

```
面板宽度：w-80（320px）侧边栏 或 max-w-sm 下拉
筛选项间距：space-y-4
激活筛选标签：bg-brand-100 text-brand-700 rounded-full px-3 py-1
```

### Vue 3 + Tailwind 示例

```vue
<template>
  <div class="w-80 border-l border-neutral-200 bg-white">
    <div v-if="activeFilters.length" class="p-4 border-b border-neutral-200">
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs text-neutral-500">已选筛选</span>
        <button @click="clearAll" class="text-xs text-brand-600 hover:underline">清除全部</button>
      </div>
      <div class="flex flex-wrap gap-2">
        <span v-for="f in activeFilters" :key="f.id" class="inline-flex items-center gap-1 px-3 py-1 bg-brand-100 text-brand-700 rounded-full text-sm">
          {{ f.label }}<X class="w-3 h-3 cursor-pointer" @click="removeFilter(f.id)" />
        </span>
      </div>
    </div>
    <div class="p-4 space-y-4">
      <div><label class="block text-xs text-neutral-500 mb-1.5">状态</label><Select v-model="filters.status" :options="statusOptions" /></div>
      <div><label class="block text-xs text-neutral-500 mb-1.5">创建时间</label><DateRangePicker v-model="filters.dateRange" /></div>
      <div><label class="block text-xs text-neutral-500 mb-1.5">标签</label><MultiSelect v-model="filters.tags" :options="tagOptions" /></div>
    </div>
  </div>
</template>
```

---

## 四、时间线/活动日志

### 交互规范

| 项目 | 规范 |
|------|------|
| 布局 | 垂直时间线，左侧圆点 + 连线，右侧内容 |
| 内容结构 | 图标 + 标题 + 描述 + 时间戳 + 操作人 |
| 分组 | 按日期分组（今天、昨天、本周、更早）或按实体分组 |
| 加载态 | 骨架屏，模拟真实布局 |
| 空状态 | 图标 + "暂无活动记录" + 说明 |

### 视觉规范

```
时间线颜色：bg-neutral-200（连线），bg-brand-500（当前项圆点）
圆点大小：w-2 h-2
内容间距：py-3
时间戳：text-xs text-neutral-400
分组标题：text-xs text-neutral-500 font-medium uppercase tracking-wide
```

### Vue 3 + Tailwind 示例

```vue
<template>
  <div class="relative">
    <div class="absolute left-1.5 top-2 bottom-2 w-px bg-neutral-200" />
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="flex gap-4 animate-pulse">
        <div class="w-2 h-2 rounded-full bg-neutral-200" />
        <div class="flex-1 space-y-2"><div class="h-4 bg-neutral-200 rounded w-1/3" /><div class="h-3 bg-neutral-200 rounded w-2/3" /></div>
      </div>
    </div>
    <div v-else-if="activities.length === 0" class="py-12 text-center">
      <Activity class="w-10 h-10 mx-auto text-neutral-300" />
      <p class="mt-2 text-sm text-neutral-500">暂无活动记录</p>
    </div>
    <div v-else class="space-y-0">
      <div v-for="group in groupedActivities" :key="group.date">
        <div class="sticky top-0 py-2 text-xs text-neutral-500 font-medium bg-neutral-50">{{ group.label }}</div>
        <div v-for="item in group.items" :key="item.id" class="flex gap-4 py-3">
          <div class="w-2 h-2 rounded-full bg-brand-500 flex-shrink-0" />
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <component :is="item.icon" class="w-4 h-4 text-neutral-400" />
              <span class="text-sm font-medium">{{ item.title }}</span>
            </div>
            <p class="mt-1 text-sm text-neutral-500">{{ item.description }}</p>
            <p class="mt-1 text-xs text-neutral-400">{{ item.timestamp }} · {{ item.actor }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
```

---

## 五、看板面板（Kanban Board）

### 交互规范

| 项目 | 规范 |
|------|------|
| 列结构 | 固定宽度（w-72），可横向滚动 |
| 卡片内容 | 标题、标签（彩色圆点）、负责人头像、截止日期 |
| 拖拽 | 卡片在列内/列间拖拽，实时更新顺序 |
| 新增卡片 | 列底部 "+ 添加" 按钮，点击展开输入框 |
| 列操作 | 标题右侧下拉菜单：编辑、删除、清空 |

### 视觉规范

```
列宽度：w-72（288px）
列间距：gap-4
卡片圆角：rounded-md（6px）
卡片阴影：hover:shadow-sm
拖拽占位：border-2 border-dashed border-brand-300 bg-brand-50
标签圆点：w-2 h-2 rounded-full
```

### Vue 3 + Tailwind 示例

```vue
<template>
  <div class="flex gap-4 overflow-x-auto pb-4">
    <div v-for="column in columns" :key="column.id" class="flex-shrink-0 w-72 bg-neutral-100 rounded-lg">
      <div class="flex items-center justify-between p-3 border-b border-neutral-200">
        <div class="flex items-center gap-2">
          <span class="text-sm font-medium">{{ column.title }}</span>
          <span class="text-xs text-neutral-400">{{ column.cards.length }}</span>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger as-child><button class="p-1 hover:bg-neutral-200 rounded"><MoreHorizontal class="w-4 h-4 text-neutral-400" /></button></DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem @click="editColumn(column)">编辑</DropdownMenuItem>
            <DropdownMenuItem @click="clearColumn(column)" class="text-danger-600">清空</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      <div class="p-2 space-y-2 min-h-[200px]">
        <div v-for="card in column.cards" :key="card.id" draggable="true" @dragstart="onDragStart(card)"
             class="p-3 bg-white rounded-md border border-neutral-200 hover:shadow-sm cursor-grab">
          <div class="flex items-center gap-2 mb-2">
            <span v-for="tag in card.tags" :key="tag" :style="{ backgroundColor: tag.color }" class="w-2 h-2 rounded-full" />
          </div>
          <p class="text-sm font-medium">{{ card.title }}</p>
          <div class="flex items-center justify-between mt-3">
            <Avatar :src="card.assignee?.avatar" :size="20" />
            <span v-if="card.dueDate" class="text-xs text-neutral-400">{{ card.dueDate }}</span>
          </div>
        </div>
        <button @click="showAddCard[column.id] = true" class="w-full p-2 text-sm text-neutral-500 hover:bg-neutral-200 rounded-md text-left">+ 添加卡片</button>
      </div>
    </div>
  </div>
</template>
```

---

## 六、快捷键显示

### 交互规范

| 项目 | 规范 |
|------|------|
| 显示位置 | 设置页面、命令面板底部、Tooltip 提示 |
| 格式 | Mac: `⌘ + K`，Windows: `Ctrl + K` |
| 检测系统 | 自动检测操作系统，显示对应格式 |
| 分组 | 按功能分组：导航、编辑、视图 |

### 视觉规范

```
kbd 元素：px-1.5 py-0.5 text-xs bg-neutral-100 border border-neutral-200 rounded
分隔符：+ 号，text-neutral-400
组合键：空格分隔，如 ⌘ Shift N
```

### Vue 3 + Tailwind 示例

```vue
<template>
  <div class="space-y-6">
    <div v-for="group in shortcutGroups" :key="group.label">
      <h3 class="text-xs text-neutral-500 font-medium uppercase tracking-wide mb-3">{{ group.label }}</h3>
      <div class="space-y-2">
        <div v-for="shortcut in group.items" :key="shortcut.action" class="flex items-center justify-between py-2">
          <span class="text-sm text-neutral-700">{{ shortcut.action }}</span>
          <div class="flex items-center gap-1">
            <template v-for="(key, i) in getKeys(shortcut.keys)" :key="i">
              <kbd class="px-1.5 py-0.5 text-xs bg-neutral-100 border border-neutral-200 rounded">{{ key }}</kbd>
              <span v-if="i < getKeys(shortcut.keys).length - 1" class="text-neutral-400">+</span>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const isMac = computed(() => navigator.platform.toUpperCase().indexOf('MAC') >= 0)
const getKeys = (keys) => keys.map(k => k === 'mod' ? (isMac.value ? '⌘' : 'Ctrl') : k === 'shift' ? (isMac.value ? '⇧' : 'Shift') : k)
</script>
```

---

## 禁止事项

- ❌ 命令面板禁止超过 600px 宽度（破坏焦点感）
- ❌ 行内编辑禁止在编辑态显示"取消"按钮（用 Esc 取消）
- ❌ 筛选面板禁止默认展开所有筛选项（折叠不常用项）
- ❌ 时间线禁止无限滚动加载（分页或"加载更多"按钮）
- ❌ 看板禁止单列超过 50 张卡片（性能问题，分页或折叠）
- ❌ 快捷键禁止使用 `Alt` 键（与系统菜单冲突）
- ❌ 所有组件禁止忽略键盘可访问性（必须支持 Tab/Enter/Esc）
- ❌ 拖拽操作禁止无视觉反馈（必须显示拖拽占位）