# 视觉层级规范

## 核心原则

视觉层级是用户理解界面的第一入口。B端 SaaS 的层级设计目标是：**让用户在 0.5 秒内识别"什么最重要"**。

克制风格的层级不靠装饰，靠**对比度差异**：大小对比（字号、间距）、明度对比（颜色深浅）、密度对比（留白与紧凑）。

---

## 一、视觉权重计算

```
视觉权重 = 字号 × 字重系数 × 颜色明度 × 空间占比
```

| 因素 | 权重贡献 | 示例 |
|------|---------|------|
| 字号 | 每增大 2px +15% | 13px → 15px |
| 字重 | 400→500 +20%，500→600 +15% | 正文→小标题 |
| 颜色明度 | 主文字 100%，次文字 60%，辅助 40% | neutral-900/500/400 |
| 空间 | 独占一行 +30%，行内 0% | 标题 vs 标签 |

**层级划分**：一级（Primary）用户必须看到；二级（Secondary）帮助理解上下文；三级（Tertiary）可选补充说明。

---

## 二、颜色透明度层级

### 文字透明度阶梯

```css
--text-primary:   oklch(13% 0.004 265);  /* 100% 不透明 */
--text-secondary: oklch(42% 0.010 265);  /* 约 60% 视觉权重 */
--text-tertiary:  oklch(62% 0.012 265);  /* 约 40% 视觉权重 */
--text-disabled:  oklch(78% 0.008 265);  /* 约 20% 视觉权重 */
```

### Tailwind 实践

```html
<!-- 数据列表行 -->
<tr>
  <td class="text-sm text-primary font-medium">订单号 #12345</td>
  <td class="text-sm text-secondary">张三</td>
  <td class="text-xs text-tertiary">2024-01-15</td>
</tr>

<!-- 卡片标题区 -->
<div class="space-y-1">
  <h3 class="text-base font-semibold text-primary">项目名称</h3>
  <p class="text-sm text-secondary">项目描述</p>
  <span class="text-xs text-tertiary">创建于 3 天前</span>
</div>
```

### 边框透明度

```css
--border-strong:  oklch(82% 0.010 265);  /* 分割重要区块 */
--border-default: oklch(90% 0.008 265);  /* 通用分割线 */
--border-subtle:  oklch(95% 0.006 265);  /* 表格内分隔 */
```

---

## 三、排版层级

### 字号阶梯（B端专用）

| 层级 | 字号 | 字重 | 颜色 | 用途 |
|------|------|------|------|------|
| H1 | 24px | 600 | primary | 页面标题 |
| H2 | 20px | 600 | primary | 区块标题 |
| H3 | 17px | 500 | primary | 卡片标题 |
| Body | 13px | 400 | primary/secondary | 正文、表格 |
| Caption | 11px | 400 | tertiary | 标签、时间戳 |

### 行高与字间距

```css
.heading { line-height: 1.25; letter-spacing: -0.01em; }  /* 标题紧凑 */
.body { line-height: 1.5; letter-spacing: 0; }            /* 正文舒适 */
.label { letter-spacing: 0.05em; text-transform: uppercase; } /* 标签区分 */
```

---

## 四、空间层级

**核心规则**：越重要的元素，周围留白越多。

```
页面标题 → 上下 24px（space-y-6）
区块标题 → 上下 16px（space-y-4）
卡片内容 → 内边距 24px（p-6）
列表项   → 内边距 12px（p-3）
行内元素 → 间距 4-8px（gap-1 / gap-2）
```

### 分组原则

```html
<div class="space-y-6">              <!-- 区块间 -->
  <section class="space-y-4">        <!-- 区块内 -->
    <div class="space-y-2">          <!-- 组内 -->
      <label class="text-sm font-medium">标签</label>
      <Input />
    </div>
  </section>
</div>
```

### 信息密度递进

高密度（表格、列表）→ 间距 8-12px；中等密度（卡片、表单）→ 间距 16-24px；低密度（空状态）→ 间距 32-48px。

---

## 五、组件层级

### 按钮层级

```html
<!-- 一级：主操作（每页面仅 1 个） -->
<Button variant="default" class="bg-brand-500 hover:bg-brand-600">创建项目</Button>

<!-- 二级：次要操作 -->
<Button variant="outline" class="border-neutral-300 text-neutral-700">取消</Button>

<!-- 三级：辅助操作 -->
<Button variant="ghost" class="text-neutral-500 hover:text-neutral-700">更多</Button>
```

### 卡片层级

```html
<!-- 一级卡片：独立内容块 -->
<Card class="border border-neutral-200 bg-white p-6">
  <h3 class="text-lg font-medium">标题</h3>
</Card>

<!-- 二级卡片：嵌套在一级卡片内 -->
<Card class="border-0 bg-neutral-50 p-4">
  <span class="text-sm text-secondary">嵌套内容</span>
</Card>
```

### 表格层级

```html
<Table>
  <TableHeader>
    <TableRow class="border-b border-neutral-200">
      <TableHead class="text-xs font-semibold text-secondary uppercase">列标题</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow class="border-b border-neutral-100">
      <TableCell class="text-sm font-medium text-primary">主数据</TableCell>
      <TableCell class="text-sm text-secondary">次数据</TableCell>
      <TableCell class="text-xs text-tertiary">辅助信息</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

---

## 六、渐进式信息披露

- **首屏**：只展示一级信息（标题、核心数据、主操作）
- **展开**：二级信息（详情、次要操作）
- **深入**：三级信息（历史记录、元数据）

```vue
<template>
  <div class="border-b border-neutral-100">
    <!-- 默认可见：一级信息 -->
    <div class="flex items-center justify-between p-4">
      <span class="text-sm font-medium text-primary">{{ item.name }}</span>
      <Button variant="ghost" size="sm" @click="expanded = !expanded">
        <ChevronDown :class="{ 'rotate-180': expanded }" class="h-4 w-4" />
      </Button>
    </div>
    <!-- 展开可见：二级信息 -->
    <div v-if="expanded" class="px-4 pb-4 space-y-2">
      <p class="text-sm text-secondary">{{ item.description }}</p>
      <div class="flex gap-2">
        <Button variant="outline" size="sm">编辑</Button>
        <Button variant="ghost" size="sm">删除</Button>
      </div>
    </div>
  </div>
</template>
```

---

## 七、常见模式示例

### 数据列表

```vue
<template>
  <div class="divide-y divide-neutral-100">
    <div v-for="item in items" :key="item.id" class="py-3 px-4 hover:bg-neutral-50">
      <div class="flex items-center justify-between">
        <div class="min-w-0">
          <div class="text-sm font-medium text-primary truncate">{{ item.title }}</div>
          <div class="text-xs text-tertiary mt-0.5">{{ item.subtitle }}</div>
        </div>
        <div class="flex items-center gap-3">
          <Badge :variant="item.statusVariant" class="text-xs">{{ item.status }}</Badge>
          <Button variant="ghost" size="icon" class="h-8 w-8">
            <MoreHorizontal class="h-4 w-4 text-tertiary" />
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>
```

### 详情页

```vue
<template>
  <div class="space-y-6">
    <!-- 页面标题区：一级 -->
    <div class="space-y-1">
      <h1 class="text-2xl font-semibold text-primary">{{ data.name }}</h1>
      <p class="text-sm text-secondary">{{ data.description }}</p>
    </div>
    <!-- 核心信息卡片：一级 -->
    <Card class="p-6">
      <h2 class="text-lg font-medium text-primary mb-4">基本信息</h2>
      <dl class="grid grid-cols-2 gap-4">
        <div>
          <dt class="text-xs text-tertiary uppercase">创建时间</dt>
          <dd class="text-sm text-primary mt-1">{{ data.createdAt }}</dd>
        </div>
      </dl>
    </Card>
    <!-- 次要信息：二级 -->
    <Card class="p-6">
      <h2 class="text-base font-medium text-secondary mb-4">操作历史</h2>
    </Card>
  </div>
</template>
```

### 仪表盘

```vue
<template>
  <div class="space-y-6">
    <!-- KPI 卡片：一级 -->
    <div class="grid gap-4 grid-cols-4">
      <Card v-for="kpi in kpis" :key="kpi.label" class="p-4">
        <div class="text-xs text-tertiary uppercase">{{ kpi.label }}</div>
        <div class="text-2xl font-semibold text-primary mt-2">{{ kpi.value }}</div>
        <div class="text-xs text-secondary mt-1">{{ kpi.change }}</div>
      </Card>
    </div>
    <!-- 图表区：二级 -->
    <div class="grid gap-4 grid-cols-2">
      <Card class="p-6">
        <h3 class="text-base font-medium text-primary mb-4">趋势图</h3>
        <Chart :data="chartData" />
      </Card>
    </div>
  </div>
</template>
```

---

## 禁止事项

- ❌ 禁止同一页面出现 2 个以上视觉权重相等的元素
- ❌ 禁止用颜色作为唯一层级区分手段（需配合字号、字重、间距）
- ❌ 禁止三级信息使用深色或粗体
- ❌ 禁止表格行内出现 3 种以上字号
- ❌ 禁止卡片嵌套超过 2 层
- ❌ 禁止用边框粗细区分层级（用颜色明度）
- ❌ 禁止"所有内容都重要"的设计（没有重点 = 没有层级）