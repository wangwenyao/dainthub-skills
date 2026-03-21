# SaaS Design System

B端 SaaS 产品设计规范技能，风格基准为专业克制（类 Linear/Notion）。

## 📖 项目简介

本技能定义了 SaaS 产品的视觉设计语言，包括色彩体系、字体排版、间距布局、组件交互原则。用于指导 AI 助手进行一致性的 UI 设计决策。

## 🎨 设计哲学

> **少即是多。每一个视觉元素都必须有存在的理由。**

以 **Linear、Notion、Vercel Dashboard、GitHub** 为风格基准：

- **克制（Restraint）**：不用渐变、不用阴影堆叠、不用装饰性插图
- **密度（Density）**：B端用户长时间使用，信息密度优先于呼吸感
- **一致（Consistency）**：相同的行为用相同的视觉语言表达
- **功能先行（Function First）**：颜色用于传达信息，而非装饰

## 📁 项目结构

```
saas-design-system/
├── SKILL.md                        # 技能主文件（设计哲学、核心规范）
└── references/                     # 参考文档目录
    ├── dark-mode.md                # 暗色模式 Token 映射
    ├── responsive.md               # 响应式断点策略
    ├── motion.md                   # 动画与过渡规范
    ├── visual-hierarchy.md         # 视觉层级规范
    ├── advanced-details.md         # 高级质感细节
    ├── brand-personality.md        # 品牌个性化指导
    ├── complex-components.md       # 复杂组件规范
    └── emotional-design.md         # 情感化设计指导
```

## 🚀 适用场景

使用此技能当：
- 定义色彩体系、设计 Token
- 制定字体排版规范
- 确定间距布局标准
- 组件选型决策
- 审查设计一致性
- 回答"这里该用什么组件"、"配色怎么定"、"间距用多少"

不使用此技能当：
- 代码实现（使用 `vue-saas-frontend` skill）
- 后端 API 设计
- 移动端设计

## 📋 核心规范速查

### 色彩使用原则

- 主色只用于**最重要的交互锚点**
- 页面中主色占比不超过 **5%**
- 语义色（红/黄/绿）**仅用于传达状态**
- 深色模式与亮色模式同等重要

### 字阶系统

| Token | 大小 | 使用场景 |
|-------|------|---------|
| `text-xs` | 11px | 标签、角标、辅助说明 |
| `text-sm` | 13px | **UI 默认字号**、表格内容 |
| `text-base` | 15px | 正文、表单输入 |
| `text-lg` | 17px | 小标题、卡片标题 |
| `text-xl` | 20px | 区块标题 |
| `text-2xl` | 24px | 页面标题 |

> **B端设计关键**：UI 默认字号用 `text-sm`（13px），这是 Linear、GitHub、Figma 等专业工具的共同选择。

### 间距基准

采用 **4px 基础栅格**：

| 间距 | 值 | 用途 |
|------|-----|------|
| space-1 | 4px | 细节间距 |
| space-2 | 8px | 紧凑间距 |
| space-3 | 12px | 默认小间距 |
| space-4 | 16px | 标准间距 |
| space-6 | 24px | 区块内间距 |
| space-8 | 32px | 区块间间距 |
| space-12 | 48px | 页面级间距 |

### 组件选型决策

| 场景 | 组件选择 |
|------|---------|
| 页面唯一主入口 | `Button` default（品牌色实心） |
| 配合主操作的次要操作 | `Button` outline |
| 删除/危险操作 | `Button` destructive |
| 有限选项 ≤5 | `RadioGroup` 或 `SegmentedControl` |
| 有限选项 >5 | `Select` |
| 多选 ≤8 | `CheckboxGroup` |
| 多选 >8 | `MultiSelect`（带搜索） |

### 设计禁令

- ❌ 一个页面超过 **1 个**主按钮
- ❌ 删除操作无确认直接执行
- ❌ 表格行内超过 **3 个**操作按钮
- ❌ 模态框内嵌套模态框
- ❌ 用颜色作为**唯一**区分手段

## 🔗 配合使用

| 需求 | 使用技能 |
|------|---------|
| 代码实现 | `vue-saas-frontend` |
| 后端 API | `java-backend-dev` |

## 📄 许可证

本项目仅供内部开发参考使用。