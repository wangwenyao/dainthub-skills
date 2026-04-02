# AI Skills Collection

AI 辅助编程技能集合，为 AI 助手提供专业领域的规范化开发指导。

## 📖 项目简介

本项目是一系列 AI 技能定义的集合，每个技能针对特定技术领域提供完整的工作流程、约束规范和参考文档。技能可被 Claude Code、OpenCode、Cursor、Codex 等 AI 编程助手加载使用，实现规范化、高质量的代码生成。

## 🎯 技能列表

### 1. draw.io 架构图与流程图技能

**目录**: [`drawio-architect-skill/`](drawio-architect-skill/)

创建和编辑生产级 `.drawio` XML 文件，覆盖多种图表类型。

| 特性 | 说明 |
|------|------|
| **云部署架构图** | 云资源拓扑、K8s 集群、数据流 |
| **功能架构图** | 功能模块分层、系统边界、接口 |
| **业务流程图** | 活动/判断/泳道、并行网关 |
| **云厂商支持** | 阿里云、AWS、GCP、Azure |
| **容器支持** | Kubernetes 图标库 |

**触发词**: `draw.io`、`diagrams.net`、`架构图`、`部署图`、`功能架构`、`流程图`、`泳道图`、`拓扑图`

**详细文档**: [`drawio-architect-skill/SKILL.md`](drawio-architect-skill/SKILL.md)

---

### 2. Java 后端开发技能

**目录**: [`java-backend-dev-skill/`](java-backend-dev-skill/)

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

**详细文档**: [`java-backend-dev-skill/SKILL.md`](java-backend-dev-skill/SKILL.md)

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

**触发词**: `写PRD`、`需求分析`、`产品设计`、`用户故事`、`需求评审`

**详细文档**: [`product-manager/SKILL.md`](product-manager/SKILL.md)

---

### 4. 技术经理技能

**目录**: [`tech-manager/`](tech-manager/)

连接产品需求与技术实现，负责变更影响分析、任务分发、实现验证。

| 特性 | 说明 |
|------|------|
| **变更影响分析** | 分析 PRD/接口/数据库变更的影响范围 |
| **任务分发** | 并行启动前后端开发 subagent |
| **技术同步** | 前后端接口对齐、变更通知分发 |
| **实现验证** | 对照 PRD 验证代码实现 |

**适用场景**:
- 需求逻辑调整，分析影响范围
- PRD 变更后分发开发任务
- 前后端接口对齐
- 开发完成后验证实现

**触发词**: `分析影响`、`分配任务`、`前后端对齐`、`检查实现`

**详细文档**: [`tech-manager/SKILL.md`](tech-manager/SKILL.md)

---

### 5. SaaS 设计系统技能

**目录**: [`saas-design-system/`](saas-design-system/)

B端 SaaS 产品设计规范技能，风格基准为专业克制（类 Linear/Notion）。

| 特性 | 说明 |
|------|------|
| **设计哲学** | 克制、密度、一致、功能先行 |
| **色彩体系** | 主色占比≤5%，禁止渐变 |
| **字体系统** | Geist + PingFang SC + Microsoft YaHei |
| **组件选型** | 命令面板/行内编辑/看板等复杂场景 |
| **中文排版** | 行高≥1.5、中英文间距、标点避让 |

**适用场景**:
- 定义色彩体系、设计 Token
- 制定字体排版规范
- 确定间距布局标准
- 组件选型决策
- 审查设计一致性

**触发词**: `设计规范`、`UI 规范`、`颜色规范`、`字体规范`、`设计 token`、`配色`、`间距`、`组件选型`

**详细文档**: [`saas-design-system/SKILL.md`](saas-design-system/SKILL.md)

---

### 6. Vben SaaS 前端开发技能

**目录**: [`vben-saas-frontend/`](vben-saas-frontend/)

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

**详细文档**: [`vben-saas-frontend/SKILL.md`](vben-saas-frontend/SKILL.md)

---

### 7. Vue SaaS 前端开发技能

**目录**: [`vue-saas-frontend/`](vue-saas-frontend/)

SaaS 多租户前端开发技能，基于 Vue 3 + TypeScript + Shadcn-vue。

| 特性 | 说明 |
|------|------|
| **框架** | Vue 3 · TypeScript · Vite |
| **UI 组件** | Shadcn-vue · Radix Vue |
| **样式** | Tailwind CSS 4 |
| **状态管理** | Pinia · TanStack Query |
| **表单** | FormKit · Zod |
| **测试** | Vitest · Playwright |

**适用场景**:
- 企业级 SaaS 系统开发
- 数据表格、复杂表单
- 状态管理、API 集成
- 组件库扩展

**触发词**: `Vue 组件`、`SaaS 页面`、`shadcn`、`数据表格`、`表单`、`仪表盘`

**详细文档**: [`vue-saas-frontend/SKILL.md`](vue-saas-frontend/SKILL.md)

---

## 📁 项目结构

```
dainthub-skills/
├── README.md                           # 项目说明（本文件）
├── drawio-architect-skill/             # draw.io 架构图技能
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 参考文档
├── java-backend-dev-skill/             # Java 后端开发技能
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 参考文档
├── product-manager/                    # 产品经理技能
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 参考文档
├── saas-design-system/                 # SaaS 设计系统技能
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 参考文档
├── tech-manager/                       # 技术经理技能
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 参考文档
├── vben-saas-frontend/                 # Vben SaaS 前端开发技能
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 参考文档
└── vue-saas-frontend/                  # Vue SaaS 前端开发技能
    ├── SKILL.md                        # 技能主文件
    └── references/                     # 参考文档
```

---

## 🔗 技能协作关系

```
product-manager (产品经理)
       ↓ PRD
tech-manager (技术经理)
       ↓ 任务分发
   ┌───┴───┐
   ↓       ↓
java     vben
backend  frontend
   ↓       ↓
   └───┬───┘
       ↓ 验证
tech-manager (技术经理)
```

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

---

> 💡 **提示**: 每个技能的详细规范见各目录下的 SKILL.md 文件。