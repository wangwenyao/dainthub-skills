---
name: product-manager
description: Use when 用户需要写PRD、写需求文档、需求评审、功能设计、产品规划、用户故事，或提到：帮我梳理需求、整理功能点、写产品方案、这个功能怎么设计、帮我想想产品逻辑、产品需求文档。
---

# Product Manager Skill

B端产品经理能力体系，从需求发现到PRD交付。

---

## 快速路由

根据用户意图，直接跳转对应流程：

| 用户意图 | 执行流程 | 立即读取 |
|---------|---------|---------|
| 写PRD / 写需求文档 / 帮我写产品需求 | 流程三：PRD编写 | `workflows/prd-writing.md` |
| 评审PRD / 检查需求文档 | 流程四：需求评审 | `workflows/review.md` |
| 分析需求 / 排优先级 / 梳理需求 | 流程一：需求分析 | `workflows/requirement-analysis.md` |
| 设计产品方案 / 规划功能 / 产品逻辑 | 流程二：产品设计 | `workflows/product-design.md` |

识别用户意图后，立即读取对应的 workflow 文件并开始执行。

---

## 四大流程

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

编写页面原型时，引用 `saas-design-system` skill 获取色彩Token、字体规范、组件选型标准。

---

## 版本

- v1.6
- 更新: 2026-04-02
- 优化: 删除PRD类型分类、简化流程、章节重排