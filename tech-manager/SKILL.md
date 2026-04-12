---
name: tech-manager
description: Use when 需求逻辑调整、PRD变更、接口变更、数据库变更需要分析影响范围，或需要前后端技术同步、验证代码实现是否符合需求、实现偏差反馈产品经理，或提到：分析一下影响、前后端对齐、检查实现、技术方案评估、分配任务、分发任务、反馈产品、方案调整、生成接口文档、OpenAPI规格、接口定义、生成数据库脚本、DML脚本、SQL脚本、建表语句。
---

# Tech Manager

技术经理能力，连接产品需求与技术实现，确保变更被正确理解和执行。

---

## 运行模式

本 skill 支持两种运行模式，按场景自动切换：

| 模式 | 适用场景 | 特点 |
|------|---------|------|
| **独立开发** | 单会话，无协作需求 | 只加载本 skill workflows |
| **协同开发** | 多会话，git 协作 | 加载 team-collaboration + 迭代循环 |

### 模式检测规则

**检测协同模式**：
- 用户明确说 "协同开发"、"多角色"、"分布式"
- 项目根目录存在 `docs/status.md`
- 用户触发 `/ralph-loop` 迭代循环

**默认**：独立开发模式

### 模式加载内容

| 文档 | 独立开发 | 协同开发 |
|------|---------|---------|
| 本 skill workflows (change-analysis 等) | ✅ 加载 | ✅ 加载 |
| `testing-collaboration.md` (测试协作) | ✅ 加载 | ✅ 加载 |
| `sync-flow.md` (拉取同步) | ❌ 不加载 | ✅ 加载 |
| `status-mechanism.md` (状态同步) | ❌ 不加载 | ✅ 加载 |
| `iteration-workflow.md` (迭代循环) | ❌ 不加载 | ✅ 加载 |
| 其他 team-collaboration references | ❌ 不加载 | ✅ 按需加载 |

---

## 快速路由

### 核心（所有模式）

| 用户意图 | 执行流程 | 立即读取 |
|---------|---------|---------|
| 需求逻辑调整 / PRD变更 / 分析影响 | 变更影响分析 | `references/workflows/change-analysis.md` |
| 生成接口文档 / OpenAPI / 接口规格 | 接口规格生成 | `references/workflows/interface-spec-generation.md` |
| 生成数据库脚本 / DML / SQL脚本 | DML脚本生成 | `references/workflows/dml-script-generation.md` |
| 分配任务 / 分发任务 / 并行开发 | 任务分发 | `references/workflows/task-dispatch.md` |
| 前后端接口对齐 / 技术同步 | 技术同步协调 | `references/workflows/tech-sync.md` |
| 检查实现 / 验证代码 | 实现验证 | `references/workflows/implementation-verify.md` |
| 实现偏差 / 方案调整 / 反馈产品 | 偏差反馈 | `references/workflows/deviation-feedback.md` |
| 技术方案评估 / 技术选型 | 技术决策支持 | 内联处理 |

### 协同模式专用

| 用户意图 | 立即读取 |
|---------|---------|
| git pull / 拉取同步 / 检查变更 | `../team-collaboration/references/06-sync-flow.md` |
| 项目初始化 / 协同开发 / 分布式协作 | `../team-collaboration/references/01-overview.md` |
| 目录结构 / 项目结构 | `../team-collaboration/references/02-project-structure.md` |
| status.md / 归档 / 状态更新 | `../team-collaboration/references/05-status-mechanism.md` |
| 按优先级迭代 / 循环开发 | `../team-collaboration/references/09-iteration-workflow.md` |
| skill 路由 / 任务分发规则 | `../team-collaboration/references/10-skill-router.md` |

识别用户意图后，立即读取对应的 workflow 文件并执行。

---

## 六大核心能力

### 一、变更影响分析

分析变更对后端接口、数据库、前端页面的影响，输出影响范围报告。

**输入**：PRD变更 / 接口变更 / 数据库变更 / 需求逻辑调整
**输出**：影响范围报告（后端改动、数据库改动、前端改动、风险提示）

读取 `@references/workflows/change-analysis.md` 执行完整流程。

### 二、接口规格生成

从 PRD ER图 + 字段约束生成符合 OpenAPI 3.0 规范的接口文档。

**输入**：ER图 + 实体属性 + 字段约束 + 业务规则 + YAML页面规格
**输出**：openapi-{模块名}-v{版本}.yaml（前后端可直接使用）

读取 `@references/workflows/interface-spec-generation.md` 执行完整流程。

**输出用途**：
- 前端 vben-frontend-dev 直接读取 → API 类型定义 + 接口调用
- 后端 java-backend-dev 直接读取 → Controller 接口定义
- 接口对齐：基于 OpenAPI 文档进行前后端一致性检查

### 三、DML脚本生成

从 PRD ER图 + 字段约束生成 MySQL 8 兼容的数据库脚本。

**输入**：ER图 + 实体属性 + 字段约束 + 业务规则 + 非功能需求
**输出**：
- dml-{模块名}-v{版本}.sql（CREATE/ALTER 含检查点）
- dml-{模块名}-v{版本}-rollback.sql（回滚脚本）
- dml-{模块名}-checklist-v{版本}.md（执行清单）

读取 `@references/workflows/dml-script-generation.md` 执行完整流程。

**输出用途**：
- 后端 java-backend-dev 直接执行 → Entity + Mapper 对应
- DBA 执行清单 → 执行顺序、依赖关系、检查项
- 变更日志 db_change_log → 追踪执行历史
- 回滚脚本 → 版本回退能力

### 四、任务分发

将变更任务分发给前后端开发，并行启动开发 subagent。

**输入**：变更影响分析结果 + OpenAPI文档 + DML脚本
**输出**：并行启动后端开发 + 前端开发 subagent

读取 `@references/workflows/task-dispatch.md` 执行完整流程。

### 五、技术同步协调

确保前后端技术方案对齐，分发变更通知。

**场景**：接口定义对齐、变更通知分发、技术方案评审

读取 `@references/workflows/tech-sync.md` 执行完整流程。

### 六、实现验证

对照 PRD 验证代码实现是否满足需求规格。

**验证维度**：功能完整性、接口一致性、字段完整性、业务规则、测试质量

读取 `@references/workflows/implementation-verify.md` 执行完整流程。

**测试验证集成**：
- 使用 `test-generation` 分析测试覆盖率
- 验证是否遵循 `test-driven-development` 流程
- 检查边缘情况测试覆盖

---

## 偏差反馈能力

开发实现与 PRD 存在偏差时，汇总偏差信息反馈给产品经理确认。

**触发**：技术限制导致方案调整、发现 PRD 逻辑缺陷、开发优化建议、新增技术约束
**输入**：实现验证报告中的"不通过"项 / 开发过程中的偏差上报
**输出**：偏差反馈报告 → 产品经理确认 → 决策记录

读取 `@references/workflows/deviation-feedback.md` 执行完整流程。

---

## 与其他 Skill 的协作

**上游**：接收 product-manager 输出的 PRD + ER 图 + YAML 页面规格
**下游**：向 java-backend-dev（DML + OpenAPI）和 vben-frontend-dev（OpenAPI）分发任务
**闭环**：实现验证 → 偏差反馈 → product-manager 确认

**完整协作链路** → `../README.md#技能协作关系`

---

## 变更类型速查

| 变更类型 | 影响范围 | 分析重点 |
|---------|---------|---------|
| 新增功能 | 全栈 | 接口设计、数据库表、前端页面 |
| 逻辑调整 | 后端+前端 | 状态机、业务规则、接口参数 |
| 字段变更 | 数据库+接口+前端 | 字段类型、默认值、历史数据 |
| 接口变更 | 后端+前端 | 参数、返回值、版本兼容 |
| 状态变更 | 全栈 | 状态机、枚举值、历史数据 |

---

## 参考文档索引

| 文档 | 用途 | 何时加载 |
|------|------|----------|
| `../team-collaboration/references/01-overview.md` | 协同开发概述 + 触发指令 | 项目初始化 |
| `../team-collaboration/references/05-status-mechanism.md` | status.md 状态快照 + 归档机制 | 更新状态/归档 |
| `../team-collaboration/references/06-sync-flow.md` | 拉取同步流程 | git pull 后 |
| `../team-collaboration/references/02-project-structure.md` | 项目目录结构 | 需要了解目录时 |
| `workflows/change-analysis.md` | 变更影响分析流程 | 需求逻辑调整、PRD变更 |
| `workflows/interface-spec-generation.md` | OpenAPI 接口规格生成流程 | 生成接口文档 |
| `workflows/dml-script-generation.md` | DML脚本生成流程（含回滚） | 生成数据库脚本 |
| `workflows/task-dispatch.md` | 任务分发流程 | 并行开发 |
| `workflows/tech-sync.md` | 技术同步协调流程 | 前后端接口对齐 |
| `workflows/implementation-verify.md` | 实现验证流程 | 检查代码实现 |
| `workflows/deviation-feedback.md` | 偏差反馈流程 | 实现偏差处理 |
| `change-templates.md` | 影响分析模板、OpenAPI模板、DML模板、决策记录模板 | 生成各类文档 |

