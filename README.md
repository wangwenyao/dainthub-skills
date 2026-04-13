# AI Skills Collection

AI 辅助编程技能集合，为 AI 助手提供专业领域的规范化开发指导。

## 📖 项目简介

本项目是一系列 AI 技能定义的集合，每个技能针对特定技术领域提供完整的工作流程、约束规范和参考文档。技能可被 Claude Code、OpenCode、Cursor、Codex 等 AI 编程助手加载使用，实现规范化、高质量的代码生成。

## 🎯 技能列表

### 1. Java 后端开发技能

**目录**: [`java-backend-dev/`](java-backend-dev/)

单体 SpringBoot 后端开发技能，覆盖全部后端开发场景。

| 特性 | 说明 |
|------|------|
| **技术栈** | Spring Boot 3 + MyBatis Plus + MySQL 8 |
| **缓存** | Spring Cache · Redis · Redisson |
| **任务调度** | Quartz |
| **工具库** | Hutool · Lombok |

**适用场景**:
- 新建功能模块、实体 CRUD、查询接口
- 字段增删改、接口变更
- 业务逻辑重构、SQL 优化
- 缓存策略、定时任务、外部服务调用

**触发词**: `新建模块`、`实体CRUD`、`字段变更`、`接口开发`、`SQL优化`、`缓存`、`定时任务`、`外部调用`

**详细文档**: [`java-backend-dev/SKILL.md`](java-backend-dev/SKILL.md)

---

### 2. Vben 前端开发技能

**目录**: [`vben-frontend-dev/`](vben-frontend-dev/)

Vben Admin 5.x 前端页面开发技能，基于 Vue 3 + Vite + VxeGrid + VbenForm。

| 特性 | 说明 |
|------|------|
| **框架** | Vue 3 · Vben Admin 5.x · Vite |
| **UI 组件** | VbenForm · VxeGrid · VbenModal |
| **样式** | Tailwind CSS · 自定义主题 |
| **状态管理** | Pinia · TanStack Query |
| **表单** | Schema驱动 · Zod验证 |

**适用场景**:
- Vben Admin 5.x 页面开发
- 列表页、表单页、详情页
- 主题配置、路由配置
- 弹窗/抽屉组件开发

**触发词**: `Vben Admin`、`列表页`、`表单页`、`VxeGrid`、`VbenForm`、`VbenModal`、`路由配置`

**不适用**: 非Vben框架、纯后端、React/Angular项目、纯样式设计

**详细文档**: [`vben-frontend-dev/SKILL.md`](vben-frontend-dev/SKILL.md)

---

### 3. 产品经理技能

**目录**: [`product-manager/`](product-manager/)

产品经理全流程工作技能，覆盖需求分析、PRD 撰写、产品设计、评审等场景。

| 特性 | 说明 |
|------|------|
| **需求分析** | KANO模型、MoSCoW优先级、用户故事地图 |
| **PRD 撰写** | 结构化文档、功能架构、验收标准 |
| **产品设计** | Design Thinking、双钻模型、UX五要素 |
| **评审机制** | 完整性/清晰度/合理性/风险检查清单 |

**适用场景**:
- 需求分析与优先级排序
- PRD 文档撰写
- 产品设计与评审
- 用户故事编写
- 生成线框图、页面原型
- 处理偏差反馈

**触发词**: `写PRD`、`需求分析`、`产品设计`、`用户故事`、`需求评审`、`线框图`、`页面原型`、`偏差反馈`

**详细文档**: [`product-manager/SKILL.md`](product-manager/SKILL.md)

---

### 4. 技术经理技能

**目录**: [`tech-manager/`](tech-manager/)

连接产品需求与技术实现，负责变更影响分析、任务分发、实现验证。

| 特性 | 说明 |
|------|------|
| **变更影响分析** | 分析 PRD/接口/数据库变更的影响范围 |
| **接口规格生成** | 从 PRD 生成 OpenAPI 3.0 规范文档 |
| **DML脚本生成** | 生成数据库脚本（含回滚脚本） |
| **任务分发** | 并行启动前后端开发 subagent |
| **技术同步** | 前后端接口对齐、变更通知分发 |
| **实现验证** | 对照 PRD 验证代码实现 |

**适用场景**:
- 需求逻辑调整，分析影响范围
- 生成接口文档、OpenAPI规格
- 生成数据库脚本、DML脚本
- PRD 变更后分发开发任务
- 前后端接口对齐
- 开发完成后验证实现
- 实现偏差反馈

**触发词**: `分析影响`、`生成接口文档`、`生成数据库脚本`、`分配任务`、`前后端对齐`、`检查实现`、`偏差反馈`

**详细文档**: [`tech-manager/SKILL.md`](tech-manager/SKILL.md)

---

### 5. 协同开发技能

**目录**: [`team-collaboration/`](team-collaboration/)

多角色分布式协同开发指南，确保不同 AI 会话之间的协作一致性。

| 特性 | 说明 |
|------|------|
| **状态快照** | status.md 单文件全局状态 |
| **拉取同步** | git pull 后的任务识别流程 |
| **版本归档** | 文档归档与新版本切换 |
| **测试协作** | 开发 skill 与测试 skill 的协作框架 |

**适用场景**:
- 多角色协作（PM → Tech Manager → 开发）
- git pull 后需要了解项目状态
- 更新 status.md 状态快照
- 版本归档 / 开始新版本
- 项目初始化时了解协作流程

**触发词**: `协同开发`、`分布式协作`、`git pull同步`、`status.md更新`、`版本归档`、`拉取同步`、`测试协作`

**详细文档**: [`team-collaboration/SKILL.md`](team-collaboration/SKILL.md)

---

### 6. QA 测试工程师技能

**目录**: [`qa-engineer/`](qa-engineer/)

系统测试设计与质量保证能力，填补 vibe coding 场景下的质量保证缺口。

| 特性 | 说明 |
|------|------|
| **测试计划** | 测试范围定义、优先级矩阵、资源估算 |
| **测试用例设计** | 边界值、状态迁移、正交实验、等价类划分 |
| **E2E测试** | Playwright 自动化测试设计与执行 |
| **缺陷管理** | 缺陷生命周期管理、缺陷记录追踪 |
| **质量度量** | 质量指标定义、覆盖率分析、质量报告 |
| **测试报告** | 测试执行汇总、缺陷统计、上线评估 |

**适用场景**:
- 编写测试计划、确定测试范围
- 设计测试用例（系统性方法论）
- E2E 自动化测试（Playwright）
- 缺陷管理、缺陷追踪
- 生成测试报告、质量度量分析

**触发词**: `测试计划`、`测试用例设计`、`测试覆盖率`、`缺陷管理`、`测试报告`、`E2E测试`、`Playwright`、`质量度量`

**不适用**: 单元测试规范（由 java-backend-dev 处理）、纯开发实现

**详细文档**: [`qa-engineer/SKILL.md`](qa-engineer/SKILL.md)

---

## 📁 项目结构

```
dainthub-skills/
├── README.md                           # 项目说明（本文件）
├── AGENTS.md                           # AI 助手开发指南
├── java-backend-dev/                   # Java 后端开发技能
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 参考文档
├── product-manager/                    # 产品经理技能
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 参考文档
├── tech-manager/                       # 技术经理技能
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 参考文档
├── team-collaboration/                 # 协同开发技能
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 协作流程 + 测试协作
├── vben-frontend-dev/                  # Vben 前端开发技能
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 参考文档
└── qa-engineer/                        # QA 测试工程师技能
    ├── SKILL.md                        # 技能主文件
    └── references/                     # 测试设计 + Playwright + 缺陷管理
```

---

## 🔗 技能协作关系

```
product-manager (产品经理)
       ↓ PRD + 验收标准 + 线框图
       ↓ YAML页面规格
        
qa-engineer (测试工程师)
       ↓ 测试计划 + 测试用例设计
       ↓ test-plan.md + test-cases.md
        
tech-manager (技术经理)
       ↓ 变更影响分析
       ↓ 生成 OpenAPI 接口规格
       ↓ 生成 DML 数据库脚本
       ↓ 任务分发
   ┌────────────┴────────────┐
   ↓                         ↓
java-backend-dev          vben-frontend-dev
（后端开发）                （前端开发）
       ↓                         ↓
       └────────────┬────────────┘
                    ↓
              qa-engineer (执行测试 + E2E测试 + 缺陷记录)
                    ↓
              tech-manager 实现验证
                    ↓
            ┌───────┴───────┐
            ↓               ↓
        ✅ 通过          ❌ 不通过
                            ↓
                     缺陷修复循环 → qa-engineer 验证
                            ↓
                     偏差反馈 → product-manager 确认
                            ↓
                     决策记录 → 更新PRD / 重新实现
```

### 协作流程说明

1. **产品阶段**: product-manager 输出 PRD + 线框图 + YAML页面规格
2. **测试设计阶段**: qa-engineer 输出测试计划 + 测试用例设计
3. **技术阶段**: tech-manager 进行变更分析，生成接口规格和数据库脚本
4. **开发阶段**: 并行启动前后端开发，基于 OpenAPI 和 DML 脚本协作
5. **测试阶段**: qa-engineer 执行测试 + E2E测试 + 记录缺陷
6. **验证阶段**: tech-manager 对照 PRD 验证实现，如有偏差反馈给产品确认
7. **闭环阶段**: product-manager 评估偏差影响并做出决策

### 分布式协同开发

分布式协同开发指南已整合为独立技能 **team-collaboration**：

- 状态快照机制（status.md）
- 拉取同步流程
- 版本归档机制
- 测试协作框架

详见 [`team-collaboration/SKILL.md`](team-collaboration/SKILL.md)

---

## 🚀 使用方式

### 在 Open Code 中使用

1. 将技能目录放置在 Open Code 的 skills 目录下
2. 在对话中提及触发词，AI 将自动加载对应技能
3. 根据任务类型，AI 会自动读取相关的参考文档

### 技能加载机制

每个技能包含以下核心文件：

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 技能定义：触发条件、工作流程、约束规则 |
| `references/*.md` | 参考文档：详细规范、代码模板、最佳实践 |

AI 在执行任务时会：
1. 根据 `description` 判断是否触发技能
2. 读取 `SKILL.md` 了解工作流程和约束
3. 按需加载 `references/` 下的参考文档

---

## 📄 许可证

本项目采用 MIT 许可证，仅供内部开发参考使用。
