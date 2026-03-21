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

**详细文档**: [`java-backend-dev-skill/README.md`](java-backend-dev-skill/README.md)

---

### 3. SaaS 设计系统技能

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

### 4. Vue SaaS 前端开发技能

**目录**: [`vue-saas-frontend/`](vue-saas-frontend/)

SaaS 多租户前端开发技能，基于 Vue 3 + TypeScript + Element Plus。

| 特性 | 说明 |
|------|------|
| **框架** | Vue 3 · TypeScript · Vite |
| **UI 组件** | Element Plus |
| **状态管理** | Pinia |
| **多租户** | 租户隔离、主题定制、权限控制 |

**适用场景**:
- SaaS 管理后台开发
- 多租户功能实现
- 组件库扩展
- 路由与权限配置

**触发词**: `SaaS 前端`、`Vue 前端`、`管理后台`、`多租户前端`

**详细文档**: [`vue-saas-frontend/SKILL.md`](vue-saas-frontend/SKILL.md)

---

## 📁 项目结构

```
dainthub-skills/
├── README.md                           # 项目说明（本文件）
├── drawio-architect-skill/             # draw.io 架构图技能
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 参考文档
│       ├── alibaba_cloud_shapes.md     # 阿里云图标库（311个）
│       ├── deploy_arch_patterns.md     # 云部署架构图模式
│       ├── flowchart_patterns.md       # 业务流程图模式
│       └── functional_arch_patterns.md # 功能架构图模式
├── java-backend-dev-skill/             # Java 后端开发技能
│   ├── README.md                       # 技能说明
│   ├── SKILL.md                        # 技能主文件
│   └── references/                     # 参考文档
│       ├── java-best-practices.md      # Java 最佳实践
│       ├── code-templates.md           # 代码模板
│       ├── data-layer.md               # 数据层规范
│       ├── service-layer.md            # 服务层规范
│       ├── maven-standards.md          # Maven 规范
│       ├── application-config.md       # 配置文件规范
│       ├── test-standards.md           # 测试规范
│       ├── security-standards.md       # 安全规范
│       ├── api-design.md               # API 设计规范
│       └── design-principles.md        # 设计原则与最佳实践
├── saas-design-system/                  # SaaS 设计系统技能
│   ├── SKILL.md                        # 技能主文件（设计哲学、核心规范、约束总表）
│   └── references/                     # 参考文档
│       ├── typography-cjk.md           # 中文排版规范（行高、中英文间距、标点处理）
│       ├── dark-mode.md                # 暗色模式规范（Token 映射、shadcn-vue 变量）
│       ├── responsive.md               # 响应式断点策略
│       ├── motion.md                   # 动画与过渡规范
│       ├── visual-hierarchy.md         # 视觉层级规范
│       ├── advanced-details.md         # 高级质感细节（微交互、图标、数据展示）
│       ├── brand-personality.md        # 品牌个性化指导
│       ├── complex-components.md       # 复杂组件规范（命令面板、行内编辑、看板）
│       ├── emotional-design.md         # 情感化设计指导
│       ├── accessibility.md            # 可访问性规范（WCAG 2.1 AA）
│       └── page-examples.md            # 页面设计示例
└── vue-saas-frontend/                  # Vue SaaS 前端开发技能
    ├── SKILL.md                        # 技能主文件
    └── references/                     # 参考文档
        ├── compatibility.md            # 浏览器兼容性
        ├── components-guide.md         # 组件开发指南
        ├── config-center.md            # 配置中心
        ├── feature-flags.md            # 功能开关
        ├── route-config.md             # 路由配置
        ├── ui-config.md                # UI 配置
        └── utils.md                    # 工具函数
```

## 🚀 使用方式

### 在 Claude Code 中使用

1. 将技能目录放置在 Claude Code 的 skills 目录下
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

## 📋 技能开发规范

如需开发新技能，请遵循以下结构：

```yaml
---
name: skill-name
description: |
  技能描述，用于 AI 判断是否触发
license: MIT
compatibility:
  - Claude Code
  - OpenCode
  - Cursor
  - Codex
metadata:
  author: author-name
  version: "1.0"
  tags: tag1, tag2, tag3
---
```

## 📄 许可证

本项目采用 MIT 许可证，仅供内部开发参考使用。

---

> 💡 **提示**: 每个技能目录下都有详细的 README 或 SKILL.md 文件，包含完整的使用说明和约束规范。
