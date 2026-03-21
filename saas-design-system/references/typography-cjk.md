# 中文排版规范（CJK Typography）

针对中文环境的企业级 SaaS 产品排版规范。基于飞书、企业微信等主流平台实践。

---

## 一、字体配置

### 1.1 推荐字体栈

```css
:root {
  /* 主字体：Geist（英文）+ PingFang SC（中文）+ Microsoft YaHei（Windows 回退） */
  --font-sans: 'Geist', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-mono: 'Geist Mono', 'JetBrains Mono', 'Fira Code', monospace;
}

/* 系统级字体栈（备用） */
font-family: system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
```

### 1.2 字体特性

| 字体 | 平台 | 特点 |
|------|------|------|
| **PingFang SC** | macOS / iOS | Apple 默认，现代感，屏幕渲染优秀 |
| **Microsoft YaHei** | Windows | ClearType 优化，覆盖 99% Windows 设备 |

### 1.3 字重映射

```css
/* 中文与英文字重对应 */
font-weight: 400;  /* Regular → 中文常规 */
font-weight: 500;  /* Medium → 中文中等（小标题） */
font-weight: 600;  /* Semibold → 中文半粗（页面标题） */
font-weight: 700;  /* Bold → 中文粗体（大数字） */
```

> **注意**：Microsoft YaHei 仅支持 400/700 两档字重，中间值会被浏览器插值或就近匹配。

---

## 二、行高规范

### 2.1 中文行高基准

中文视觉密度高于英文，需要更大的行高保证可读性。

| 场景 | 行高 | 说明 |
|------|------|------|
| **正文** | `1.6` | 中文正文标准，保证阅读舒适 |
| **标题** | `1.3` | 紧凑，减少视觉松散 |
| **表格/列表** | `1.5` | 信息密度优先 |
| **移动端** | `1.7` | 小屏幕需要更大呼吸空间 |

### 2.2 Tailwind 实现

```css
/* 自定义行高 */
.line-height-body { line-height: 1.6; }
.line-height-tight { line-height: 1.3; }
.line-height-table { line-height: 1.5; }

/* Tailwind 扩展 */
@layer utilities {
  .leading-body { line-height: 1.6; }
  .leading-tight-cn { line-height: 1.3; }
  .leading-table { line-height: 1.5; }
}
```

### 2.3 字号与行高对照表

| Token | 字号 | 中文行高 | 英文行高 | 使用场景 |
|-------|------|----------|----------|----------|
| `text-xs` | 11px | 1.5 (16px) | 1.45 (16px) | 标签、角标 |
| `text-sm` | 13px | 1.54 (20px) | 1.54 (20px) | UI 默认、表格 |
| `text-base` | 15px | 1.6 (24px) | 1.5 (22px) | 正文、表单 |
| `text-lg` | 17px | 1.65 (28px) | 1.47 (25px) | 小标题 |
| `text-xl` | 20px | 1.4 (28px) | 1.4 (28px) | 区块标题 |
| `text-2xl` | 24px | 1.33 (32px) | 1.33 (32px) | 页面标题 |

---

## 三、中英文混排

### 3.1 间距问题

中英文混排时，字符粘连不美观，需要添加间距。

**问题示例**：
```
中文English中文  → 视觉粘连
中文 English 中文 → 手动空格，不一致
```

### 3.2 解决方案

**方案一：CSS text-spacing（推荐，现代浏览器）**

```css
.text-spacing {
  text-spacing: trim-start allow-end ideograph-alpha ideograph-numeric;
  /* 或简写 */
  text-spacing: ideograph-alpha ideograph-numeric;
}
```

**方案二：JavaScript 自动处理（兼容方案）**

```javascript
// 自动在中英文之间添加细间距
function addSpacing(text) {
  return text
    .replace(/([\u4e00-\u9fa5])([a-zA-Z0-9])/g, '$1\u200A$2')
    .replace(/([a-zA-Z0-9])([\u4e00-\u9fa5])/g, '$1\u200A$2');
}
// \u200A = 细空格（hair space），约 1/6 em
```

**方案三：Tailwind 工具类（手动控制）**

```css
@layer utilities {
  /* 中英文间距（使用细空格） */
  .mix-spacing {
    text-spacing: ideograph-alpha ideograph-numeric;
  }
}
```

### 3.3 数字与中文

```html
<!-- 推荐：数字与中文间有视觉间隔 -->
<p>共 <span class="font-variant-numeric tabular-nums">128</span> 条记录</p>

<!-- CSS -->
.font-variant-numeric {
  font-variant-numeric: tabular-nums;  /* 等宽数字 */
}
```

---

## 四、段落排版

### 4.1 段落缩进

**B 端 SaaS 场景**：通常 **不需要** 首行缩进。

| 场景 | 缩进 | 理由 |
|------|------|------|
| **列表项** | 无 | 列表符号已提供视觉层级 |
| **卡片内容** | 无 | 卡片边界已定义段落 |
| **长文章/帮助文档** | `2em` | 传统排版习惯 |

```css
/* 仅长文章启用缩进 */
.prose p {
  text-indent: 2em;
}
.prose p:first-of-type {
  text-indent: 0;  /* 首段不缩进 */
}
```

### 4.2 对齐方式

| 场景 | 对齐 | 说明 |
|------|------|------|
| **表格内容** | 左对齐 | B 端标准 |
| **表格数字列** | 右对齐 | 便于比较数值 |
| **正文段落** | 左对齐 | 避免"河流"现象 |
| **标题** | 左对齐 | B 端标准 |

```css
/* 数字列右对齐 */
td.numeric {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
```

---

## 五、标点处理

### 5.1 标点挤压

中文字符宽度固定，但标点符号在行首/行尾需要特殊处理。

```css
.hanging-punctuation {
  /* 允许标点悬挂（行首/行尾） */
  hanging-punctuation: first last;
}
```

### 5.2 行尾标点避让

```css
.line-break {
  /* 标点不在行首 */
  line-break: strict;
  /* 中文断词规则 */
  word-break: keep-all;
  /* 溢出处理 */
  overflow-wrap: break-word;
}
```

### 5.3 省略号规范

```css
/* 单行省略 */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 多行省略（中文友好） */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.6;  /* 中文行高 */
}
```

---

## 六、断行规则

### 6.1 中文断行

```css
.chinese-text {
  /* 中文在任意字符间可断行 */
  line-break: auto;
  /* 但不拆分单词 */
  word-break: keep-all;
  /* 或使用 CJK 专用属性 */
  word-break: break-all;  /* 紧急情况允许断开 */
}
```

### 6.2 中英文混排断行

```css
.mixed-text {
  /* 英文单词保持完整 */
  word-break: keep-all;
  /* 中文可在任意位置断行 */
  line-break: anywhere;
  /* 溢出时在单词边界断行 */
  overflow-wrap: break-word;
}
```

---

## 七、字号感知

### 7.1 中英文字号差异

相同字号下，中文视觉上比英文大约 10-15%。

| 字号 | 中文视觉 | 英文视觉 | 建议 |
|------|----------|----------|------|
| 13px | 适中 | 偏小 | UI 默认（B 端标准） |
| 14px | 舒适 | 适中 | 移动端正文 |
| 16px | 偏大 | 舒适 | 中文标题可用 |

### 7.2 混排字号调整

```css
/* 中英文混排时，英文可稍大 */
.mixed-text {
  font-size: 14px;
}
.mixed-text:lang(en) {
  font-size: 15px;  /* 英文稍大 */
}
```

---

## 八、移动端适配

### 8.1 字号缩放

```css
/* 移动端字号调整 */
@media (max-width: 768px) {
  body {
    font-size: 13px;      /* 移动端正文 */
    line-height: 1.7;     /* 更大行高 */
  }
  
  h1 { font-size: 20px; }
  h2 { font-size: 18px; }
  h3 { font-size: 16px; }
}
```

### 8.2 触摸目标

```css
/* 移动端点击区域 */
@media (max-width: 768px) {
  .btn, .link, .nav-item {
    min-height: 44px;  /* Apple HIG 推荐 */
    min-width: 44px;
  }
}
```

---

## 九、约束总表

> **注意**：通用排版约束（字号、字重、行长、行高、数字对齐等）已整合到 `SKILL.md` 的 **C-TYPE** 约束中。以下仅为中文环境特有约束。

| ID | 规则 |
|----|------|
| C-CJK-001 | 多行文本省略需指定中文行高（≥1.5） |
| C-CJK-002 | 中英文混排时使用 text-spacing 或手动间距 |
| C-CJK-003 | 行尾禁止出现：`、，。：；！？》」』】"` |
| C-CJK-004 | 行首禁止出现：`《「『【"'` |

### 相关通用约束（见 SKILL.md）

| ID | 规则 | 来源 |
|----|------|------|
| C-TYPE-004 | 禁止全大写中文 | 通用排版 |
| C-TYPE-005 | 禁止 letter-spacing 用于中文 | 通用排版 |
| C-TYPE-006 | 中文正文行高不低于 1.6 | 通用排版 |
| C-TYPE-007 | 表格数字列右对齐 + 等宽数字 | 通用排版 |

---

## 十、代码示例

### 完整配置

```css
/* 中文排版基础样式 */
:root {
  --font-sans: 'Geist', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-mono: 'Geist Mono', 'JetBrains Mono', 'Fira Code', monospace;
  
  /* 中文行高 */
  --line-height-body: 1.6;
  --line-height-tight: 1.3;
  --line-height-table: 1.5;
}

body {
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: var(--line-height-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

/* 中文正文 */
.body-cn {
  line-height: 1.6;
  word-break: keep-all;
  overflow-wrap: break-word;
}

/* 表格数字 */
.table-number {
  text-align: right;
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

/* 中英文混排间距 */
.mix-spacing {
  text-spacing: ideograph-alpha ideograph-numeric;
}

/* 移动端 */
@media (max-width: 768px) {
  body {
    font-size: 13px;
    line-height: 1.7;
  }
}
```

### Vue 组件示例

```vue
<template>
  <!-- 数据列表 -->
  <table class="w-full">
    <thead>
      <tr class="border-b border-neutral-200">
        <th class="text-xs font-medium text-secondary text-left px-4 py-3">名称</th>
        <th class="text-xs font-medium text-secondary text-right px-4 py-3">数量</th>
      </tr>
    </thead>
    <tbody>
      <tr class="border-b border-neutral-100">
        <td class="text-sm text-primary px-4 py-3">{{ item.name }}</td>
        <td class="text-sm text-primary text-right px-4 py-3 tabular-nums">
          {{ item.count }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
/* 等宽数字 */
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
</style>
```