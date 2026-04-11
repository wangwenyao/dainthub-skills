---
name: product-manager
description: Use when 用户需要写PRD、写需求文档、需求评审、功能设计、产品规划、用户故事，或提到：帮我梳理需求、整理功能点、写产品方案、这个功能怎么设计、帮我想想产品逻辑、产品需求文档、生成线框图、页面原型、设计页面结构、处理偏差反馈、技术反馈、偏差决策、接受技术建议。
---

# Product Manager Skill

B端产品经理能力体系，从需求发现到PRD交付（含页面线框图）。

---

## 运行模式

本 skill 支持两种运行模式，按场景自动切换：

| 模式 | 适用场景 | 特点 |
|------|---------|------|
| **独立开发** | 单会话，无协作需求 | 只加载本 skill workflows |
| **协同开发** | 多会话，git 协作 | 加载 team-collaboration references |

### 模式检测规则

**检测协同模式**：
- 用户明确说 "协同开发"、"多角色"、"分布式"
- 项目根目录存在 `docs/status.md`
- 用户触发 `/ralph-loop` 迭代循环

**默认**：独立开发模式

### 模式加载内容

| 文档 | 独立开发 | 协同开发 |
|------|---------|---------|
| 本 skill workflows (prd-writing 等) | ✅ 加载 | ✅ 加载 |
| 本 skill references (prd-writing-guide 等) | ✅ 加载 | ✅ 加载 |
| `sync-flow.md` (拉取同步) | ❌ 不加载 | ✅ 加载 |
| `status-mechanism.md` (状态同步) | ❌ 不加载 | ✅ 加载 |
| 其他 team-collaboration references | ❌ 不加载 | ✅ 按需加载 |

---

## 快速路由（核心）

根据用户意图，直接跳转对应流程：

| 用户意图 | 执行流程 | 立即读取 |
|---------|---------|---------|
| 写PRD / 写需求文档 / 帮我写产品需求 | 流程三：PRD编写 | `references/workflows/prd-writing.md` |
| 生成线框图 / 页面原型 / 设计页面结构 | 线框图生成 | `references/workflows/wireframe-generation.md` |
| 评审PRD / 检查需求文档 | 流程四：需求评审 | `references/workflows/review.md` |
| 分析需求 / 排优先级 / 梳理需求 | 流程一：需求分析 | `references/workflows/requirement-analysis.md` |
| 设计产品方案 / 规划功能 / 产品逻辑 | 流程二：产品设计 | `references/workflows/product-design.md` |
| 处理偏差反馈 / 接收技术反馈 / 偏差决策 | 流程五：偏差反馈处理 | `references/workflows/deviation-handling.md` |

### 协同模式专用

| 用户意图 | 立即读取 |
|---------|---------|
| git pull / 拉取同步 / 检查偏差报告 | `../team-collaboration/references/06-sync-flow.md` |
| 项目初始化 / 协同开发 / 输出物存放位置 | `../team-collaboration/references/01-overview.md` |
| 目录结构 / 项目结构 | `../team-collaboration/references/02-project-structure.md` |
| status.md / 归档 / 状态更新 | `../team-collaboration/references/05-status-mechanism.md` |

识别用户意图后，立即读取对应的 workflow 文件并开始执行。

---

## 五大流程

### 流程一：需求分析
读取 `@references/workflows/requirement-analysis.md` 执行完整流程。
方法论详解（KANO分类规则、MoSCoW判断标准、RICE计算、JTBD访谈）需要时读取 `@references/requirement-analysis.md`。

### 流程二：产品设计
读取 `@references/workflows/product-design.md` 执行完整流程。
方法论详解（Design Thinking五阶段、双钻模型、UX五要素设计输出模板）需要时读取 `@references/product-design.md`。

### 流程三：PRD编写
读取 `@references/workflows/prd-writing.md` 执行完整流程。
编写具体章节时（流程图规范、功能清单、ER图、功能详细描述模板、非功能需求基准值、页面原型约束）读取 `@references/prd-writing-guide.md`。

### 流程四：需求评审
读取 `@references/workflows/review.md` 执行完整流程。
执行完整性/清晰度/合理性/边界/风险逐项检查时读取 `@references/review-checklist.md`。

### 流程五：偏差反馈处理
读取 `@references/workflows/deviation-handling.md` 执行完整流程。
接收 tech-manager 偏差反馈报告 → 评估产品影响 → 做出产品决策 → 更新 PRD → 生成决策通知。

---

## 页面线框图生成

**输出双轨格式：**
- **wireframes.html**：HTML+CSS 线框图（产品经理review/调整）
- **pages.yaml**：YAML 页面规格（前端代码生成）

**线框图原则：**
- 灰色边框、浅灰填充、占位文字
- 不使用真实颜色和图标
- 只表达布局结构和交互流程
- 统一的顶部导航 + 左侧菜单布局
- 菜单支持跳转到指定模块页面

读取 `@references/workflows/wireframe-generation.md` 执行完整流程。

---

## 速查

### 需求优先级方法选择

| 场景 | 用哪个 | 核心规则 |
|------|--------|---------|
| 功能分类 | KANO | 基本需求必须满足，兴奋需求加分 |
| 排优先级 | MoSCoW | Must ≤ 60%，不能全是P0 |
| 量化对比 | RICE | (Reach × Impact × Confidence) / Effort |

### 用户故事 & 验收标准

```
用户故事：作为 [角色]，我想要 [目标]，以便于 [价值]
验收标准：Given [前置条件] When [操作] Then [结果]
```

### PRD必需章节（P0）

```
1. 执行摘要          6. 核心业务流程（2-5个关键流程）
2. 成功标准          7. 用户旅程
3. 产品范围          8. 业务实体模型(ER图)
4. 用户画像          9. 非功能需求（性能/安全/可用性）
5. 功能架构
```

---

## 协同Skill

**页面线框图生成**：不需要 UI 设计 skill。
- 线框图只表达结构，不涉及 UI 视觉
- 前端 skill（vben-frontend-dev）直接读取 YAML → 代码
- UI 样式由前端 skill 内置约束处理

**验收标准转化**：
- 验收标准 → `test-driven-development` 的测试场景
- 用户旅程 → E2E 测试流程
- 业务规则 → Service 层单元测试

详细转化指引 → `@references/workflows/prd-writing.md#验收标准与测试协作`

**偏差反馈处理**：与 tech-manager 协作
- 接收 tech-manager 的偏差反馈报告（实现验证阶段发现）
- 评估产品影响（用户体验/业务价值/MVP范围）
- 做出产品决策（接受偏差/坚持原需求/协商调整）
- 更新 PRD 对应章节并标注决策结果
- 生成决策通知反馈给 tech-manager

详细流程 → `@references/workflows/deviation-handling.md`

**完整协作链路** → `../README.md#技能协作关系`

---

## 版本

- v3.0
- 更新: 2026-04-12
- 新增: 三级功能点定义（通用分类 + 业务操作类识别规则）
- 新增: 操作弹窗通用模板
- 精简: wireframe-layout-templates.md 减少 36% 行数，提高信息密度