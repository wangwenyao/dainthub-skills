---
name: qa-engineer
description: |
  系统测试设计与质量保证能力，覆盖测试计划、测试用例设计、缺陷管理、质量度量、E2E测试。
  触发：测试计划/测试用例设计/测试覆盖率分析/缺陷管理/测试报告/E2E测试/Playwright测试/质量度量。
  不适用：单元测试规范（由 java-backend-dev/test-standards.md 处理）、纯开发实现。
---

# QA Engineer Skill

测试工程师能力体系，从测试计划到质量度量，填补 vibe coding 场景下的质量保证缺口。

---

## 何时使用

**触发场景**：
- 编写测试计划、确定测试范围和优先级
- 设计测试用例（系统性方法论）
- 分析测试覆盖率、补充边缘场景
- 缺陷管理、缺陷生命周期追踪
- 生成测试报告
- E2E 自动化测试设计
- Playwright 测试编写与执行
- 质量度量分析与报告

**不适用**：
- 单元测试规范（由 `java-backend-dev/references/test-standards.md` 处理）
- 纯代码开发实现（由开发 skill 处理）
- 技术方案评估（由 tech-manager 处理）

---

## 快速路由

| 用户意图 | 执行流程 | 立即读取 |
|---------|---------|---------|
| 测试计划 / 测试范围 / 测试优先级 | 测试计划生成 | `references/workflows/test-planning.md` |
| 测试用例设计 / 用例编写 | 测试用例设计 | `references/workflows/test-case-design.md` |
| E2E测试 / Playwright / 自动化测试 | E2E 测试流程 | `references/workflows/playwright-testing.md` |
| 缺陷管理 / Bug追踪 / 缺陷记录 | 缺陷管理流程 | `references/workflows/defect-management.md` |
| 测试报告 / 测试总结 | 测试报告生成 | `references/workflows/test-report.md` |
| 质量度量 / 覆盖率分析 | 质量度量分析 | `references/quality-metrics.md` |

---

## 六大核心能力

### 一、测试计划生成

从 PRD 功能清单生成系统性测试计划，定义测试范围、优先级、资源分配。

**输入**：PRD 功能清单 + 功能优先级 + 验收标准
**输出**：test-plan-{模块名}-v{版本}.md（测试范围、优先级矩阵、资源计划）

读取 `@references/workflows/test-planning.md` 执行完整流程。

### 二、测试用例设计

系统性测试设计方法论，将 PRD 验收标准转化为结构化测试用例。

**设计方法**：
- 边界值分析
- 状态迁移测试
- 正交实验设计
- 错误猜测法

**输入**：PRD 功能描述 + 业务规则 + 验收标准
**输出**：test-cases-{模块名}-v{版本}.md（测试用例清单）

读取 `@references/workflows/test-case-design.md` 执行完整流程。

### 三、E2E 自动化测试（Playwright）

设计并编写 Playwright E2E 测试，覆盖关键业务流程。

**覆盖范围**：
- 用户旅程完整流程
- 关键业务操作路径
- 跨系统集成场景

**输入**：用户旅程 + 页面线框图 YAML + 关键功能
**输出**：tests/e2e/*.spec.ts（Playwright 测试文件）

读取 `@references/workflows/playwright-testing.md` 执行完整流程。

### 四、缺陷管理

缺陷生命周期管理，从发现到关闭的完整流程。

**流程阶段**：
```
发现 → 记录 → 分配 → 修复 → 验证 → 关闭
                    ↓
               遗留 → 重开
```

**输入**：测试执行结果、开发反馈
**输出**：defect-log-{模块名}-v{版本}.md（缺陷记录）

读取 `@references/workflows/defect-management.md` 执行完整流程。

### 五、测试报告生成

汇总测试执行结果，输出结构化测试报告。

**报告内容**：
- 测试执行摘要
- 覆盖率统计
- 缺陷统计
- 质量评估
- 风险提示

**输入**：测试执行记录 + 缺陷记录 + 覆盖率报告
**输出**：test-report-{模块名}-v{版本}.md

读取 `@references/workflows/test-report.md` 执行完整流程。

### 六、质量度量分析

定义质量指标，分析项目质量状态。

**度量指标**：
| 指标 | 计算公式 | 目标值 |
|------|---------|--------|
| 缺陷密度 | 缺陷数/代码行数(KLOC) | < 5 |
| 测试通过率 | 通过用例数/总用例数 | ≥ 95% |
| 缺陷修复率 | 已修复缺陷/总缺陷 | ≥ 90% |
| 测试覆盖率 | 覆盖代码行/总代码行 | Service ≥ 80% |

读取 `@references/quality-metrics.md` 了解完整度量体系。

---

## 与其他 Skill 协作

### 协作链路

```
product-manager (PRD + 验收标准)
       ↓
qa-engineer (测试计划 + 测试用例设计)
       ↓ test-plan.md + test-cases.md
       ↓
tech-manager (变更分析 + 分发)
       ↓
   ┌───┴───┐
java     vben
backend  frontend
   ↓       ↓
qa-engineer (执行测试 + 记录缺陷 + E2E测试)
       ↓
tech-manager (实现验证)
       ↓ 缺陷修复循环
qa-engineer (缺陷验证 + 测试报告)
       ↓
   ✅ 通过 / ❌ 缺陷遗留
```

### 与开发 Skill 协作

| 协作场景 | qa-engineer 负责 | 开发 skill 负责 |
|---------|-----------------|----------------|
| 测试设计 | 系统性测试用例设计 | 按设计执行测试 |
| 覆盖率分析 | 分析覆盖率缺口 | 补充单元测试 |
| 缺陷处理 | 记录缺陷 → 分配 | 修复缺陷 → 反馈 |
| E2E测试 | 设计 E2E 场景 | 前端 skill 适配 |

### 与 tech-manager 协作

| 协作场景 | qa-engineer 输出 | tech-manager 使用 |
|---------|-----------------|------------------|
| 测试计划 | 测试范围 + 优先级 | 实现验证参考 |
| 测试报告 | 缺陷统计 + 风险提示 | 偏差分析输入 |
| 质量度量 | 覆盖率 + 缺陷密度 | 上线决策参考 |

---

## PRD → 测试转化

### 验收标准 → 测试场景

PRD 的验收标准（Given/When/Then）直接转化为测试：

```
PRD验收标准：
Given 用户已登录且购物车有商品
When 用户点击结算按钮
Then 进入结算页面，显示商品清单

转化 →
测试场景 TC-001: 结算流程测试
- 前置条件: 用户已登录，购物车 ≥ 1 商品
- 测试步骤: 点击结算按钮
- 预期结果: 跳转结算页，显示商品清单
```

### 业务规则 → 测试用例

```
PRD业务规则 BR-003: 订单金额 > 1000 元，自动免除运费

转化 →
测试用例 TC-003: 运费免除规则测试
- 边界值: 999元 → 有运费, 1000元 → 无运费, 1001元 → 无运费
- 正常值: 500元 → 有运费, 1500元 → 无运费
```

详细转化指引 → `@references/workflows/test-case-design.md#PRD转化规则`

---

## 测试设计方法论速查

| 方法 | 适用场景 | 输出 |
|------|---------|------|
| **边界值分析** | 数值、日期、长度校验 | 边界测试用例集 |
| **状态迁移** | 状态流转、订单状态机 | 状态路径测试用例 |
| **正交实验** | 多参数组合场景 | 正交测试用例矩阵 |
| **错误猜测** | 经验判断易出错点 | 异常场景测试用例 |
| **等价类划分** | 输入域分类 | 正常/异常类测试用例 |

详细方法论 → `@references/test-case-templates.md`

---

## 缺陷生命周期

```
    ┌─────────┐
    │  新建   │ ← 测试发现缺陷
    └────┬────┘
         ↓
    ┌─────────┐
    │  分配   │ ← 分配给开发
    └────┬────┘
         ↓
    ┌─────────┐
    │  修复   │ ← 开发修复完成
    └────┬────┘
         ↓
    ┌─────────┐
    │  验证   │ ← 测试验证修复
    └────┬────┘
         │
    ┌────┴────┐
    ↓         ↓
┌───────┐ ┌───────┐
│ 关闭  │ │ 重开  │ ← 验证不通过
└───────┘ └───────┘
```

详细流程 → `@references/workflows/defect-management.md`

---

## 参考文档索引

| 文档 | 内容 | 何时加载 |
|------|------|----------|
| `workflows/test-planning.md` | 测试计划生成流程 | 测试范围/优先级定义 |
| `workflows/test-case-design.md` | 测试用例设计流程 + 方法论 | 用例设计 |
| `workflows/playwright-testing.md` | Playwright E2E 测试流程 | 自动化测试 |
| `workflows/defect-management.md` | 缺陷管理流程 | 缺陷记录/追踪 |
| `workflows/test-report.md` | 测试报告生成流程 | 测试总结 |
| `quality-metrics.md` | 质量度量体系定义 | 质量分析 |
| `test-case-templates.md` | 测试用例模板 + 方法论详解 | 用例编写 |

---

## 版本

- v1.0
- 更新: 2026-04-13