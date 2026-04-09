# 可访问性规范（Accessibility）

B 端 SaaS 产品可访问性规范，确保符合 WCAG 2.1 AA 级标准。

---

## 一、键盘导航

### 1.1 焦点管理
- 所有交互元素必须可通过 Tab 键聚焦
- 焦点顺序必须符合视觉阅读顺序（从左到右、从上到下）
- 模态框打开时焦点锁定在模态框内（focus trap）
- 模态框关闭后焦点返回触发元素

### 1.2 快捷键
- 支持 Escape 关闭模态框/下拉/弹出
- 支持 Enter/Space 触发按钮
- 支持方向键在列表/菜单中导航

### 1.3 Tailwind 实现
```css
/* 焦点环样式 */
.focus-ring {
  @apply focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2;
}

/* 跳过导航链接 */
.skip-link {
  @apply sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50;
}
```

---

## 二、ARIA 标注

### 2.1 基础规则
- 图标按钮必须有 `aria-label`
- 展开/收起必须有 `aria-expanded`
- 加载状态必须有 `aria-busy`
- 错误信息必须通过 `aria-describedby` 关联输入框

### 2.2 常用模式

#### 图标按钮
```html
<Button variant="ghost" size="icon" aria-label="删除项目">
  <Trash2 class="h-4 w-4" />
</Button>
```

#### 展开/收起
```html
<Button :aria-expanded="isOpen" aria-controls="panel-content">
  {{ isOpen ? '收起' : '展开' }}
</Button>
<div id="panel-content" :hidden="!isOpen">...</div>
```

#### 表单错误
```html
<Input :aria-invalid="!!error" :aria-describedby="error ? 'email-error' : undefined" />
<p v-if="error" id="email-error" role="alert" class="text-sm text-danger-500">{{ error }}</p>
```

#### 加载状态
```html
<div aria-busy="true" aria-live="polite">
  <Skeleton class="h-4 w-full" />
</div>
```

---

## 三、颜色对比度

### 3.1 对比度要求（WCAG AA）
| 元素 | 最低对比度 | 说明 |
|------|-----------|------|
| 正文文字 | 4.5:1 | text-primary vs bg-base |
| 大字（≥18px 或 14px bold） | 3:1 | 标题 vs 背景 |
| UI 组件边框 | 3:1 | 输入框边框 vs 背景 |
| 图标（有功能含义） | 3:1 | 操作图标 vs 背景 |
| 装饰性图标 | 无要求 | 仅装饰用途 |

### 3.2 禁止事项
- ❌ 禁止使用 text-placeholder（neutral-400）作为正文色（对比度不足）
- ❌ 禁止在品牌色背景上使用 neutral-500 文字
- ❌ 禁止仅靠颜色区分状态（需配合图标/文字/形状）

---

## 四、屏幕阅读器

### 4.1 语义化 HTML
- 使用语义化标签：`<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>`
- 列表使用 `<ul>/<ol>` 而非 `<div>` 嵌套
- 表格使用 `<table>` 而非 CSS Grid 模拟

### 4.2 隐藏策略
| 方法 | 视觉隐藏 | 屏幕阅读器 | 使用场景 |
|------|---------|-----------|---------|
| `class="sr-only"` | 隐藏 | 可读 | 为屏幕阅读器添加上下文 |
| `aria-hidden="true"` | 可见 | 隐藏 | 装饰性图标 |
| `hidden` 属性 | 隐藏 | 隐藏 | 完全隐藏 |

---

## 五、动态内容

### 5.1 Live Region
- Toast 通知使用 `role="status"` + `aria-live="polite"`
- 错误提示使用 `role="alert"`（立即播报）
- 进度更新使用 `aria-live="polite"`

### 5.2 页面导航
- SPA 路由切换后，通过 `aria-live` 区域播报新页面标题
- 加载完成后焦点移至主内容区

---

## 六、约束总表

| ID | 规则 |
|----|------|
| C-A11Y-001 | 所有交互元素必须可通过键盘操作 |
| C-A11Y-002 | 图标按钮必须有 aria-label |
| C-A11Y-003 | 模态框必须实现 focus trap |
| C-A11Y-004 | 正文对比度不低于 4.5:1（WCAG AA） |
| C-A11Y-005 | 禁止仅靠颜色区分信息（需配合图标/文字） |
| C-A11Y-006 | 表单错误必须通过 aria-describedby 关联 |