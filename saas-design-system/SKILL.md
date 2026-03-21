---
name: saas-design-system
description: >
  B端 SaaS 产品设计规范 skill，风格基准为专业克制（类 Linear/Notion）。当用户需要定义色彩体系、字体排版、间距布局、组件选型决策，或者问"这里该用什么组件"、"配色怎么定"、"间距用多少"、"字号规范是什么"、"这个交互合不合理"时必须使用此 skill。适用于从零建立设计语言、审查设计一致性、生成设计 token、以及指导页面视觉实现。与 vue-saas-frontend skill 协同工作——本 skill 决定"设计长什么样"，vue-saas-frontend skill 决定"代码怎么实现"。
license: MIT
compatibility:
  - Claude Code
  - OpenCode
  - Cursor
  - Codex
metadata:
  author: dainthub
  version: "2.0"
  tags: design-system, UI, UX, SaaS, design-token, tailwind
---

# SaaS Design System

## 何时使用

使用此技能当：
- 定义色彩体系、设计 Token、暗色模式适配
- 制定字体排版规范、字阶系统
- 确定间距布局标准、组件内间距
- 组件选型决策（"这里该用什么组件"）
- 审查设计一致性、检查违规项
- 回答设计相关问题：
  - "配色怎么定？"
  - "间距用多少？"
  - "字号规范是什么？"
  - "这个交互合不合理？"
  - "空状态该怎么设计？"
- 设计复杂组件（命令面板、行内编辑、看板等）
- 建立品牌视觉识别

## 何时不使用

不使用此技能当：
- 前端代码实现（使用 `vue-saas-frontend` skill）
- 后端 API 设计（使用 `java-backend-dev` skill）
- 移动端原生设计（iOS/Android 设计规范）
- 营销页面/Landing Page 设计（非 B 端产品风格）
- 游戏化产品设计
- 数据可视化图表库选型（仅涉及图表组件时）

---

## 设计哲学

> **少即是多。每一个视觉元素都必须有存在的理由。**

本设计系统以 **Linear、Notion、Vercel Dashboard、GitHub** 为风格基准，核心原则：

- **克制（Restraint）**：不用渐变、不用阴影堆叠、不用装饰性插图。视觉噪音是认知负担。
- **密度（Density）**：B端用户长时间使用，信息密度优先于呼吸感。紧凑但不拥挤。
- **一致（Consistency）**：相同的行为用相同的视觉语言表达。用户不应该猜测。
- **功能先行（Function First）**：颜色用于传达信息（状态、层级、交互），而非装饰。

---

## 一、色彩系统

### 1.1 设计原则

- 主色只用于**最重要的交互锚点**（主按钮、选中态、链接）
- 页面中主色占比不超过 **5%**，大面积留给中性色
- 语义色（红/黄/绿）**仅用于传达状态**，不用于装饰
- 深色模式与亮色模式同等重要，token 命名语义化而非描述颜色值

### 1.2 Token 体系（Tailwind CSS 4 CSS变量）

```css
@theme {
  /* ── 品牌色（蓝紫中性，类 Linear） ── */
  --color-brand-50:  oklch(97% 0.015 265);
  --color-brand-100: oklch(93% 0.030 265);
  --color-brand-200: oklch(86% 0.055 265);
  --color-brand-300: oklch(76% 0.090 265);
  --color-brand-400: oklch(64% 0.130 265);
  --color-brand-500: oklch(53% 0.165 265);   /* 主色 */
  --color-brand-600: oklch(45% 0.160 265);
  --color-brand-700: oklch(37% 0.145 265);
  --color-brand-800: oklch(29% 0.115 265);
  --color-brand-900: oklch(21% 0.080 265);

  /* ── 中性色（略带冷调，避免纯灰） ── */
  --color-neutral-0:   oklch(100% 0 0);
  --color-neutral-50:  oklch(98% 0.004 265);
  --color-neutral-100: oklch(95% 0.006 265);
  --color-neutral-200: oklch(90% 0.008 265);
  --color-neutral-300: oklch(82% 0.010 265);
  --color-neutral-400: oklch(68% 0.012 265);
  --color-neutral-500: oklch(54% 0.012 265);
  --color-neutral-600: oklch(42% 0.010 265);
  --color-neutral-700: oklch(31% 0.008 265);
  --color-neutral-800: oklch(21% 0.006 265);
  --color-neutral-900: oklch(13% 0.004 265);
  --color-neutral-950: oklch(8%  0.003 265);

  /* ── 语义色 ── */
  --color-success-500: oklch(62% 0.17 145);
  --color-success-100: oklch(94% 0.05 145);
  --color-warning-500: oklch(72% 0.17 75);
  --color-warning-100: oklch(96% 0.05 75);
  --color-danger-500:  oklch(58% 0.22 25);
  --color-danger-100:  oklch(95% 0.05 25);
  --color-info-500:    oklch(60% 0.18 230);
  --color-info-100:    oklch(95% 0.04 230);
}
```

### 1.3 语义角色映射（亮色模式）

| Token 角色 | 使用场景 | 对应值 |
|-----------|---------|--------|
| `bg-base` | 页面主背景 | neutral-50 |
| `bg-elevated` | 卡片、面板背景 | neutral-0（白） |
| `bg-sunken` | 输入框、内嵌区域 | neutral-100 |
| `bg-overlay` | 弹窗、下拉背景 | neutral-0 + shadow |
| `border-default` | 通用分割线、输入框边框 | neutral-200 |
| `border-strong` | 强调边框 | neutral-300 |
| `text-primary` | 主要文字 | neutral-900 |
| `text-secondary` | 次要/辅助文字 | neutral-500 |
| `text-placeholder` | 占位符文字 | neutral-400 |
| `text-disabled` | 禁用状态文字 | neutral-300 |
| `text-on-brand` | 主色背景上的文字 | neutral-0 |
| `interactive-default` | 主操作按钮背景 | brand-500 |
| `interactive-hover` | 主操作按钮悬停 | brand-600 |
| `focus-ring` | 键盘焦点环 | brand-500（50% opacity） |

> 暗色模式 token 映射详见 `references/dark-mode.md`

### 1.4 颜色使用禁令

- ❌ 禁止用渐变色作为背景或按钮填充
- ❌ 禁止在同一页面出现超过 2 个不同品牌色色调
- ❌ 禁止用颜色作为**唯一**区分手段（需配合图标或文字，保证色盲可用）
- ❌ 禁止使用纯黑（`#000000`）作为文字色，使用 neutral-900

---

## 二、字体与排版

### 2.1 字体选型

```css
@theme {
  /* 英文：Geist（Vercel 出品，专为界面设计） */
  /* 中文：PingFang SC（macOS/iOS）+ Microsoft YaHei（Windows） */
  --font-sans: 'Geist', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-mono: 'Geist Mono', 'JetBrains Mono', 'Fira Code', monospace;
}
```

**选型理由**：
- **Geist**：字重区分清晰、字间距适合高密度 UI、与 shadcn-vue 默认风格一致
- **PingFang SC**：Apple 平台默认中文字体，现代、屏幕渲染优秀
- **Microsoft YaHei**：Windows 平台通用字体，ClearType 优化

> 中文排版细节（行高、中英文间距、标点处理）详见 `references/typography-cjk.md`

### 2.2 字阶系统（Type Scale）

| Token | 大小 | 行高 | 字重 | 使用场景 |
|-------|------|------|------|---------|
| `text-xs` | 11px | 16px | 400 | 标签、角标、辅助说明 |
| `text-sm` | 13px | 20px | 400 | **UI 默认字号**、表格内容、次要文字 |
| `text-base` | 15px | 24px | 400 | 正文、表单输入 |
| `text-lg` | 17px | 28px | 500 | 小标题、卡片标题 |
| `text-xl` | 20px | 28px | 600 | 区块标题 |
| `text-2xl` | 24px | 32px | 600 | 页面标题 |
| `text-3xl` | 30px | 36px | 700 | 仪表盘大数字 |

> **B端设计关键**：UI 默认字号用 `text-sm`（13px），不是 `text-base`（16px）。这是 Linear、GitHub、Figma 等专业工具的共同选择——更高的信息密度。

### 2.3 字重规范

```
400 Regular  → 正文、次要信息
500 Medium   → 小标题、强调文字、导航项
600 Semibold → 页面标题、表格列头、重要数据
700 Bold     → 大数字（KPI）、空状态标题
```

### 2.4 排版禁令

- ❌ 禁止在 UI 中使用超过 3 个字重
- ❌ 禁止正文行长超过 75 个字符（约 680px），否则加 `max-w` 约束
- ❌ 禁止全大写中文
- ❌ 禁止 `letter-spacing` 用于中文（只可用于全英文标题）

---

## 三、间距与布局

### 3.1 间距基准

采用 **4px 基础栅格**，所有间距必须是 4 的倍数：

```
4px   → space-1  细节间距（图标与文字间距）
8px   → space-2  紧凑间距（标签内 padding）
12px  → space-3  默认小间距（列表项内边距）
16px  → space-4  标准间距（卡片内边距、表单项间距）
24px  → space-6  区块内间距
32px  → space-8  区块间间距
48px  → space-12 页面级间距
```

### 3.2 组件内间距规范

| 组件 | 内边距 |
|------|--------|
| 紧凑型按钮（sm） | `px-3 py-1.5`（12/6） |
| 默认按钮 | `px-4 py-2`（16/8） |
| 大按钮（lg） | `px-5 py-2.5`（20/10） |
| 输入框 | `px-3 py-2`（12/8） |
| 卡片 | `p-6`（24） |
| 表格单元格 | `px-4 py-3`（16/12） |
| 下拉菜单项 | `px-3 py-1.5`（12/6） |
| 对话框 | `p-6`（24） |
| 侧边栏导航项 | `px-3 py-2`（12/8） |

### 3.3 页面布局规范

```
顶部导航栏高度：    56px（h-14）
侧边栏宽度（展开）：240px
侧边栏宽度（收起）：56px（仅图标）
内容区最大宽度：    1280px（max-w-screen-xl）
内容区顶部内边距：  24px（pt-6）
移动端水平内边距：  16px（px-4）
```

### 3.4 圆角规范

```
4px  → sm  标签、徽章
6px  → md  按钮（默认）
8px  → lg  卡片、面板、下拉
12px → xl  模态框、大卡片
```

### 3.5 阴影规范（克制使用）

```
无阴影    → 卡片默认态（用 border 区分层次）
shadow-sm → 下拉菜单、tooltip
shadow-md → 模态框、侧边抽屉
shadow-lg → 命令面板（Command Palette）
```

❌ 禁止彩色阴影、多层叠加阴影、hover 时加大阴影。

---

## 四、组件交互原则

### 4.1 组件选型决策树

**触发操作：**
- 页面唯一主入口 → `Button` default（品牌色实心）
- 配合主操作的次要操作 → `Button` outline
- 删除/不可逆危险操作 → `Button` destructive
- 工具栏/行内轻量操作 → `Button` ghost

**信息反馈：**
- 操作结果（短暂） → `Toast`（3秒自动消失）
- 需用户确认阅读 → `Alert`（内联常驻）
- 字段级错误 → 输入框下方 error text
- 页面级警告 → `Alert` 放内容区顶部

**信息收集：**
- 短文本 → `Input`
- 长文本 → `Textarea`（min 3行）
- 有限选项 ≤5 → `RadioGroup` 或 `SegmentedControl`
- 有限选项 >5 → `Select`
- 多选 ≤8 → `CheckboxGroup`
- 多选 >8 → `MultiSelect`（带搜索）
- 开关型 → `Switch`（不用 Checkbox）
- 日期 → `DatePicker`

**内容组织：**
- 同级多视图切换 → `Tabs`
- 可折叠详情 → `Accordion`
- 相关内容分组 → `Card`
- 补充说明 → `Tooltip`（hover）或 `Popover`（click）

**确认与打断：**
- 不可逆操作 → `AlertDialog`（强制确认）
- 复杂表单/设置 → `Sheet`（侧边抽屉，保留上下文）
- 简单信息补充 → `Dialog`（居中，≤600px）
- 快捷操作 → `Command`（⌘K 命令面板）
- 行内编辑 → `Popover` + 表单

### 4.2 反馈时序标准

| 操作 | 反馈方式 |
|------|---------|
| 开关、选择（即时） | 直接状态变化，不需要 Toast |
| 轻量写操作 | 成功静默，失败才 Toast |
| 重要写操作（创建/删除） | 成功 Toast + 数据刷新 |
| 危险操作 | AlertDialog 确认 → 执行 → Toast |
| 长时操作（>2s） | 进度条或 Loading，完成后 Toast |

### 4.3 空状态必须包含

```
图标   → h-10 w-10，text-muted-foreground
标题   → "暂无 XX 数据"，font-medium
说明   → 解释原因 + 下一步行动
按钮   → 可选，引导创建（有权限时显示）
```

❌ 禁止空状态只写一行"暂无数据"。

### 4.4 加载态规范

```
页面首次加载  → Skeleton 骨架屏（模拟真实布局）
数据刷新/分页 → 表格内 overlay（不清空现有数据）
按钮触发操作  → 按钮 disabled + Loader2 spin
局部区域      → Skeleton 或居中 Spinner
```

### 4.5 交互禁令

- ❌ 一个页面超过 **1 个**主按钮（品牌色实心）
- ❌ 删除操作无确认直接执行
- ❌ Toast 堆叠超过 3 条
- ❌ 模态框内嵌套模态框
- ❌ 表格行内超过 **3 个**操作按钮（超出收入 DropdownMenu）
- ❌ 自动弹出 Dialog/Alert（必须用户触发）

---

## 五、快速参考

| 问题 | 参考位置 |
|------|---------|
| 中文排版规范 | `references/typography-cjk.md` |
| 暗色模式 token 映射 | `references/dark-mode.md` |
| 响应式断点策略 | `references/responsive.md` |
| 动画与过渡规范 | `references/motion.md` |
| 视觉层级规范 | `references/visual-hierarchy.md` |
| 高级质感细节 | `references/advanced-details.md` |
| 品牌个性化指导 | `references/brand-personality.md` |
| 复杂组件规范 | `references/complex-components.md` |
| 情感化设计指导 | `references/emotional-design.md` |
| 页面设计示例 | `references/page-examples.md` |
| 代码实现 | 配合 `vue-saas-frontend` skill 使用 |

---

## 六、输入参数

执行设计任务时，需要确定以下参数：

| 参数 | 说明 | 获取方式 |
|------|------|---------|
| **设计类型** | `token` / `component` / `page` / `pattern` / `review` | 从用户描述推断 |
| **页面类型** | `list` / `detail` / `form` / `dashboard` / `auth` / `settings` | 若涉及页面设计则询问 |
| **组件类型** | `button` / `input` / `table` / `form` / `modal` / `command` 等 | 从用户描述推断 |
| **主题模式** | `light` / `dark` / `both` | 默认 `both`，用户指定则覆盖 |

### 设计类型判断

| 类型 | 触发词 | 输出范围 |
|------|--------|---------|
| `token` | "配色"、"色彩体系"、"设计 token"、"暗色模式" | Token 定义、语义映射 |
| `component` | "组件"、"按钮"、"表单"、"用什么组件" | 组件选型、样式规范 |
| `page` | "页面"、"列表页"、"详情页"、"仪表盘" | 布局决策、层级规范 |
| `pattern` | "交互"、"动画"、"空状态"、"加载态" | 交互模式、时序规范 |
| `review` | "检查"、"审查"、"是否合规"、"有什么问题" | 违规项列表、修复建议 |

---

## 七、输出清单

根据设计类型确定输出范围：

| 设计类型 | 输出内容 |
|---------|---------|
| `token` | Token 定义（CSS 变量）、语义角色映射表、禁令清单 |
| `component` | 组件选型决策、样式规范、代码示例、禁令清单 |
| `page` | 布局决策说明、视觉层级规范、Section 结构模板 |
| `pattern` | 交互模式说明、时序规范、代码示例 |
| `review` | 违规项列表（约束 ID + 描述 + 修复建议） |

---

## 八、约束总表

> 约束编号贯穿所有参考文件，违反任何一条均视为设计违规。

### 色彩约束

| ID | 规则 |
|----|------|
| C-COLOR-001 | 主色只用于最重要的交互锚点（主按钮、选中态、链接） |
| C-COLOR-002 | 页面中主色占比不超过 5%，大面积留给中性色 |
| C-COLOR-003 | 语义色（红/黄/绿）仅用于传达状态，不用于装饰 |
| C-COLOR-004 | 禁止用渐变色作为背景或按钮填充 |
| C-COLOR-005 | 禁止在同一页面出现超过 2 个不同品牌色色调 |
| C-COLOR-006 | 禁止用颜色作为唯一区分手段（需配合图标或文字） |
| C-COLOR-007 | 禁止使用纯黑（#000000）作为文字色 |

### 排版约束（通用）

| ID | 规则 |
|----|------|
| C-TYPE-001 | B端 UI 默认字号用 text-sm（13px），不是 text-base（16px） |
| C-TYPE-002 | 禁止在 UI 中使用超过 3 个字重 |
| C-TYPE-003 | 禁止正文行长超过 75 个字符，否则加 max-w 约束 |
| C-TYPE-004 | 禁止全大写中文 |
| C-TYPE-005 | 禁止 letter-spacing 用于中文（只可用于全英文标题） |
| C-TYPE-006 | 中文正文行高不低于 1.6 |
| C-TYPE-007 | 表格数字列右对齐 + 等宽数字（tabular-nums） |

### 间距约束

| ID | 规则 |
|----|------|
| C-SPACE-001 | 所有间距必须是 4 的倍数（4px 栅格系统） |
| C-SPACE-002 | 同一排组件宽高必须一致 |
| C-SPACE-003 | 层间间距保持统一（推荐 16-24px） |

### 交互约束

| ID | 规则 |
|----|------|
| C-INTERACT-001 | 一个页面仅 1 个主按钮（品牌色实心） |
| C-INTERACT-002 | 删除操作必须有确认步骤 |
| C-INTERACT-003 | Toast 堆叠不超过 3 条 |
| C-INTERACT-004 | 禁止模态框内嵌套模态框 |
| C-INTERACT-005 | 表格行内操作按钮不超过 3 个（超出收入 DropdownMenu） |
| C-INTERACT-006 | Dialog/Alert 必须由用户触发，禁止自动弹出 |
| C-INTERACT-007 | 动画时长不超过 200ms |
| C-INTERACT-008 | 禁止使用 transition-all（指定具体属性） |

### 视觉层级约束

| ID | 规则 |
|----|------|
| C-HIER-001 | 禁止同一页面出现 2 个以上视觉权重相等的元素 |
| C-HIER-002 | 禁止用颜色作为唯一层级区分手段 |
| C-HIER-003 | 禁止三级信息使用深色或粗体 |
| C-HIER-004 | 禁止表格行内出现 3 种以上字号 |
| C-HIER-005 | 禁止卡片嵌套超过 2 层 |
| C-HIER-006 | 禁止用边框粗细区分层级（用颜色明度） |

### 情感设计约束

| ID | 规则 |
|----|------|
| C-EMOTION-001 | 禁止彩带、撒花、庆祝动画 |
| C-EMOTION-002 | 禁止成功/庆祝弹窗 |
| C-EMOTION-003 | 禁止游戏化元素（徽章、积分、连续天数） |
| C-EMOTION-004 | 禁止使用"恭喜"、"太棒了"、"厉害"等文案 |
| C-EMOTION-005 | 禁止"亲"、"哦~"、"呢~"等语气词 |
| C-EMOTION-006 | 禁止 emoji 作为主要视觉元素 |

### 中文排版约束（特有）

> 通用排版规则见上方 C-TYPE 约束。以下为中文环境特有约束。

| ID | 规则 |
|----|------|
| C-CJK-001 | 多行文本省略需指定中文行高（≥1.5） |
| C-CJK-002 | 中英文混排时使用 text-spacing 或手动间距 |
| C-CJK-003 | 行尾禁止出现：`、，。：；！？》」』】"` |
| C-CJK-004 | 行首禁止出现：`《「『【"`'` |

---

## 九、质量门控

### 设计输出前检查

```
色彩层：
□ 主色使用场景是否正确？
□ 品牌色占比是否 ≤ 5%？
□ 是否有渐变色（禁止）？
□ 是否用颜色作为唯一区分手段（禁止）？

排版层：
□ UI 默认字号是否为 13px？
□ 字重数量是否 ≤ 3？
□ 行长是否超限？

间距层：
□ 所有间距是否为 4 的倍数？
□ 同排组件宽高是否一致？

交互层：
□ 主按钮数量是否 = 1？
□ 删除操作是否有确认？
□ 动画时长是否 ≤ 200ms？

层级层：
□ 是否有明确的视觉焦点？
□ 是否有三级以上信息混杂？
```

### 审查输出格式

```markdown
## 设计审查报告

### 违规项

| 约束 ID | 描述 | 位置 | 修复建议 |
|---------|------|------|---------|
| C-INTERACT-001 | 页面存在 2 个主按钮 | 顶部操作区 | 将次要按钮改为 outline 变体 |
| C-TYPE-001 | 表格字号使用 14px | 数据列表 | 改为 text-sm（13px） |

### 合规项

- ✅ 主色占比约 4%，符合 C-COLOR-002
- ✅ 间距均为 4 的倍数，符合 C-SPACE-001
```
