---
name: product-manager
description: Use when 企业信息系统（业务驱动）需要写PRD、写需求文档、需求评审、功能设计、产品规划、用户故事，或提到：帮我梳理需求、整理功能点、写产品方案、这个功能怎么设计、帮我想想产品逻辑、产品需求文档、生成线框图、页面原型、设计页面结构、处理偏差反馈、技术反馈、偏差决策、接受技术建议。不适用：UI 视觉设计（由 saas-ui-design 处理）、技术实现方案（由 tech-manager 处理）、纯代码开发、C端消费者产品、竞品分析。
---

# Product Manager Skill

B端产品经理能力体系，从需求发现到PRD交付（含页面线框图）。

---

## ⚠️ 执行约束（MANDATORY）

**加载本 skill 后必须遵守以下规则，违反即为 skill 执行失败**：

### 1. 流程执行约束

| 规则 | 说明 |
|------|------|
| **禁止跳步骤** | 必须按 workflow 定义步骤顺序执行，不得跳过任何步骤 |
| **禁止简化步骤** | 每个步骤必须完整执行，不得"简单处理"或"跳过详细" |
| **必须读取引用** | workflow 中 `@xxx.md` 引用必须实际读取，不得凭记忆推断 |

### 2. 输出格式约束

| 输出类型 | 强制要求 |
|----------|----------|
| **PRD 功能清单** | 必须包含三级功能点（功能ID + 功能点清单表格） |
| **PRD 功能详细描述** | P0 功能必须完整填写：前置条件、权限矩阵、字段约束、业务规则、验收标准 |
| **线框图 HTML** | 必须使用模板定义的 class，不得自创样式；灰色系配色，不得使用真实颜色 |
| **线框图 YAML** | 必须包含完整的 pages 配置，每个页面必须有 type、route、config |
| **Mermaid 图表** | 必须使用正确的 Mermaid 语法，确保可渲染 |

### 3. 质量验证约束

| 验证时机 | 必须动作 |
|----------|----------|
| **生成前** | 认已读取所有需要的 references 文件 |
| **生成中** | 每完成一个章节，对照规范检查格式 |
| **生成后** | 必须使用 `@references/review-checklist.md` 逐项验证输出质量 |

### 4. 禁止行为

| 禁止 | 原因 |
|------|------|
| ❌ 凭记忆生成内容 | skill 文件可能已更新，必须实际读取 |
| ❌ 输出不完整的章节 | P0 章节必须完整，不得"后面补充" |
| ❌ 自创格式或样式 | 必须使用 skill 定义的模板和格式 |
| ❌ 跳过质量检查 | 生成后必须验证，不得直接结束 |

### 5. 执行信号

以下行为表明 skill 执行失败：
- 输出的功能清单只有二级功能，没有三级功能点
- 输出的线框图使用了真实颜色或图标
- 输出的 YAML 缺少 pages 配置或 config 不完整
- Mermaid 图表语法错误无法渲染
- 没有读取引用文件就直接生成内容

---

## 流程执行顺序

| 阶段 | 流程 | 必选/可选 | 说明 |
|------|------|----------|------|
| **规划阶段** | 流程一：需求分析 | 必选 | 需求挖掘、优先级排序 |
| **规划阶段** | 流程二：产品设计 | 必选 | 设计思维、UX五要素 |
| **建模阶段** | 流程三：业务建模 | 必选 | 角色、流程、活动、规则定义 |
| **架构阶段** | 流程四：功能架构设计 | 必选 | 三级功能点拆解 |
| **文档阶段** | 流程五：PRD编写 | 必选 | 完整PRD文档 |
| **文档阶段** | 流程六：线框图生成 | 必选 | HTML + YAML输出 |
| **验证阶段** | 流程七：原型走查验证 | 必选 | 线框图走查 + 流程模拟 |
| **评审阶段** | 流程八：需求评审 | 必选 | 完整性/清晰度检查 |
| **迭代阶段** | 流程九：偏差反馈处理 | 可选 | 如有偏差才执行 |

---

## 快速路由

根据用户意图，直接跳转对应流程：

| 用户意图 | 执行流程 | 立即读取 |
|---------|---------|---------|
| 写PRD / 写需求文档 | 流程五：PRD编写 | `references/workflows/prd-writing.md` |
| 生成线框图 / 页面原型 | 流程六：线框图生成 | `references/workflows/wireframe-generation.md` |
| 评审PRD / 检查需求 | 流程八：需求评审 | `references/workflows/review.md` |
| 分析需求 / 排优先级 | 流程一：需求分析 | `references/workflows/requirement-analysis.md` |
| 设计产品方案 / 产品逻辑 | 流程二：产品设计 | `references/workflows/product-design.md` |
| 设计功能架构 / 功能拆解 | 流程四：功能架构设计 | `references/workflows/function-architecture-design.md` |
| 业务建模 / 角色/流程定义 | 流程三：业务建模 | `references/workflows/business-modeling-flow.md` |
| 处理偏差反馈 | 流程九：偏差反馈处理 | `references/workflows/deviation-handling.md` |
| 原型走查 / 验证流程 | 流程七：原型走查验证 | `references/workflows/prototype-validation.md` |

---

## 流程索引

### 流程一：需求分析

读取 `@references/workflows/requirement-analysis.md` 执行完整流程。

方法论详解（KANO/MoSCoW）见 `@references/requirement-analysis.md`。

### 流程二：产品设计

读取 `@references/workflows/product-design.md` 执行完整流程。

方法论详解（Design Thinking/双钻模型/UX五要素）见 `@references/product-design.md`。

### 流程三：业务建模

读取 `@references/workflows/business-modeling-flow.md` 执行完整流程。

业务建模规范见 `@references/business-modeling.md`。

### 流程四：功能架构设计

读取 `@references/workflows/function-architecture-design.md` 执行完整流程。

功能架构规范见 `@references/prd-writing-guide.md#功能架构规范`。

### 流程五：PRD编写

读取 `@references/workflows/prd-writing.md` 执行完整流程。

模板见 `@references/prd-template.md`，规范见 `@references/prd-writing-guide.md`。

### 流程六：线框图生成

读取 `@references/workflows/wireframe-generation.md` 执行完整流程。

模板见 `@references/wireframe-layout-templates.md`。

### 流程七：原型走查验证

读取 `@references/workflows/prototype-validation.md` 执行完整流程。

### 流程八：需求评审

读取 `@references/workflows/review.md` 执行完整流程。

检查清单见 `@references/review-checklist.md`。

### 流程九：偏差反馈处理

读取 `@references/workflows/deviation-handling.md` 执行完整流程。

---

## 方法论速查

### 需求优先级方法

| 场景 | 用哪个 | 详见 |
|------|--------|------|
| 功能分类 | KANO | `@references/requirement-analysis.md#KANO模型` |
| 排优先级 | MoSCoW | `@references/requirement-analysis.md#MoSCoW优先级法` |

### 验收标准格式

```
Given [前置条件]
When [用户操作]
Then [预期结果]
```

> 验收标准在功能详细描述中定义，无需单独写用户故事

### PRD必需章节（P0）

```
1. 执行摘要          6. 业务流程矩阵
2. 成功标准          7. 业务活动与规则
3. 产品范围          8. 功能架构（含三级功能点）
4. 业务角色模型      9. 业务实体模型（ER图）
5. 用户旅程          10. 非功能需求
```

> 完整模板见 `@references/prd-template.md`

---

## 方法论 → 输出映射

| 方法论 | 输出 | PRD章节 |
|--------|------|---------|
| 用户访谈 | 用户洞察 | 4.1 角色定义 |
| KANO分类 | 功能优先级 | 8.1 二级功能清单 |
| MoSCoW | MVP定义 | 3.3 MVP定义 |
| 用户故事地图 | 功能清单 | 8.2 三级功能点清单 |
| UX五要素范围层 | 功能规格 | 8.1 二级功能清单 |
| UX五要素结构层 | 信息架构 | 8.3 功能菜单层级结构 |

> 详细映射见 `@references/requirement-analysis.md` 和 `@references/product-design.md`

---

## 协同Skill

**页面线框图生成**：不需要 UI 设计 skill。
- 线框图只表达结构，不涉及 UI 视觉
- 前端 skill（vben-frontend-dev）直接读取 YAML → 代码

**验收标准转化**：
- 验收标准 → `test-driven-development` 的测试场景
- 用户旅程 → E2E 测试流程
- 业务规则 → Service 层单元测试

详细转化指引 → `@references/workflows/prd-writing.md#验收标准与测试协作`

**偏差反馈处理**：与 tech-manager 协作
- 接收 tech-manager 的偏差反馈报告
- 评估产品影响 → 做出产品决策 → 更新 PRD

详细流程 → `@references/workflows/deviation-handling.md`

---

## 版本

- v4.7
- 更新: 2026-04-12
- 修复: 流程索引序号（原"七大流程"实际有8个，现改为9个流程统一编号）
- 删除: 冗余的独立"页面线框图生成"章节（已纳入流程六）