# 品牌个性指南：克制中的差异化

> **核心命题**：如何在"少即是多"的约束下，让产品拥有独特的品牌识别度？

Linear（蓝紫冷调）、Notion（暖灰温润）、Vercel（黑白高对比）——三者风格克制却各具辨识度。差异源于**细节选择**，而非装饰堆砌。

---

## 一、品牌色使用：超越主按钮

### 品牌色触点清单

| 触点 | Linear | Notion | Vercel |
|------|--------|--------|--------|
| Logo/Favicon | 蓝紫渐变 | 黑色手写体 | 黑白三角 |
| 选中态 | brand-500 背景 | 浅灰背景+左侧色条 | 黑色背景 |
| 链接 | brand-500 | 深灰+hover下划线 | 黑色 |
| Focus Ring | brand-500 50% | 橙色（唯一亮色） | 黑色 |
| 图表强调色 | brand-500 | 深灰系 | 黑色 |

### 代码示例

```css
/* 品牌色注入点 */
:root {
  --brand-accent: var(--color-brand-500);
  --brand-subtle: var(--color-brand-200);
}

/* 选中态品牌表达 */
.nav-item[data-active="true"] {
  background: var(--brand-subtle);
  border-left: 2px solid var(--brand-accent);
}

/* Focus Ring 品牌化 */
:focus-visible {
  outline: 2px solid var(--brand-accent);
  outline-offset: 2px;
}
```

---

## 二、字体即品牌

| 产品 | 字体 | 品牌气质 |
|------|------|---------|
| Linear | Inter | 几何感、技术、精确 |
| Notion | -apple-system | 亲和、文档感、无门槛 |
| Vercel | Geist | 现代、极简、速度 |

```css
/* 仅限英文标题使用 letter-spacing */
.brand-headline { letter-spacing: -0.02em; }  /* 紧凑 = 现代 */
.brand-editorial { letter-spacing: 0.01em; }  /* 宽松 = 编辑感 */
/* ❌ 中文禁止使用 letter-spacing */
```

---

## 三、微交互：品牌时刻

```css
/* Linear 风格：脉冲呼吸 */
@keyframes linear-pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

/* Notion 风格：轻柔弹跳（仅空状态） */
@keyframes notion-bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

/* 成功勾选动画 */
.success-check {
  stroke-dasharray: 20;
  stroke-dashoffset: 20;
  animation: draw-check 300ms ease-out forwards;
}
```

---

## 四、图标与插图风格

```css
/* 统一图标参数 */
.icon-system {
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}
```

**插图使用原则**：
- ✅ 空状态：单色线条插图，与图标风格统一
- ✅ 错误页：抽象几何图形
- ❌ 禁止：装饰性插图、吉祥物、场景插画

---

## 五、文案语气

```
❌ "暂无数据"
✅ "还没有创建任何项目。点击上方按钮开始。"

❌ "出错了"
✅ "无法加载项目列表。请检查网络后重试。"
```

| 产品 | 语气 | 示例 |
|------|------|------|
| Linear | 精确、技术 | "同步完成。3 个问题已更新。" |
| Notion | 温暖、引导 | "从这里开始，写下任何想法..." |
| Vercel | 直接、自信 | "部署成功。您的站点已上线。" |

---

## 六、布局签名

### 侧边栏风格

| 产品 | 特征 |
|------|------|
| Linear | 深色、紧凑、图标+文字、hover高亮 |
| Notion | 浅色、宽松、可折叠、嵌套层级 |
| Vercel | 极简、图标为主、收起时仅图标 |

### 卡片处理

```css
/* Linear 风格：细边框、无阴影 */
.card-linear { border: 1px solid var(--border-default); }

/* Notion 风格：无边框、微阴影 */
.card-notion { border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }

/* Vercel 风格：黑边框、高对比 */
.card-vercel { border: 1px solid var(--neutral-900); }
```

---

## 七、决策框架：何时偏离默认

```
是否偏离默认？
├─ 是否服务于功能？ → 是 → 继续 │ 否 → ❌ 放弃
├─ 是否增加认知负担？ → 是 → ❌ 放弃 │ 否 → 继续
└─ 是否与品牌核心价值一致？ → 是 → ✅ 采用 │ 否 → ❌ 放弃
```

**可偏离场景**：Logo/Favicon、空状态插图、成功动画、404 页面

**不可偏离场景**：表单交互、数据展示、导航结构、按钮层级

---

## 八、禁止事项

- ❌ 渐变色背景或按钮
- ❌ 多层叠加阴影
- ❌ 装饰性插图（非空状态）
- ❌ 循环动画（非加载态）
- ❌ 全屏页面过渡
- ❌ 品牌色占比超过 5%
- ❌ 同一页面超过 2 种品牌色色调
- ❌ 中文使用 letter-spacing
- ❌ 超过 3 种字重
- ❌ 彩色阴影