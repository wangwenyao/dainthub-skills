---
name: team-collaboration
description: |
  分布式协同开发指南，用于多角色协作场景。
  触发：协同开发/分布式协作/git pull同步/status.md更新/版本归档/拉取同步/项目初始化/测试协作。
  不适用：单角色独立开发、非 git 协作场景。
---

# Team Collaboration Skill

多角色分布式协同开发指南，确保不同 AI 会话、不同电脑之间的协作一致性。

---

## 何时使用

**触发场景**：
- 多角色协作（产品经理 → 技术经理 → 前后端开发）
- git pull 后需要了解项目状态
- 更新 status.md 状态快照
- 版本归档 / 开始新版本
- 项目初始化时了解协作流程
- 测试协作框架（开发 skill 与测试 skill 的协作规范）

**不适用**：
- 单角色独立开发
- 非 git 协作场景

---

## 快速路由

| 用户意图 | 立即读取 |
|---------|---------|
| git pull / 拉取同步 / 检查变更 | `references/06-sync-flow.md` |
| 项目初始化 / 协同开发概述 | `references/01-overview.md` |
| 目录结构 / 项目结构 | `references/02-project-structure.md` |
| 前后端工程结构 | `references/03-frontend-backend.md` |
| git 工作流 / 版本号规范 | `references/04-git-workflow.md` |
| status.md / 归档机制 | `references/05-status-mechanism.md` |
| 协作场景示例 | `references/07-examples.md` |
| AI 配置 / 检查清单 | `references/08-ai-config.md` |
| 测试协作框架 | `references/testing-collaboration.md` |

---

## 核心机制

### 一、status.md 状态快照

AI 拉取后只读取这一个文件，了解全局状态：

```markdown
# 项目状态快照

## 各模块当前状态
| 模块 | PRD | OpenAPI | DML | 线框图 | 验证 | 偏差 | 当前阶段 |
|------|-----|---------|-----|--------|------|------|---------|
| product | v1.2 ✅ | v1.2 ✅ | ... | ... | ... | ... | ✅ 已完成 |

## 待处理项汇总
| 类型 | 模块 | 文件路径 | 处理角色 |
|------|------|---------|---------|
| 偏差反馈 | user | docs/reports/deviation-user.md | product-manager |

## 下一步任务
| 角色 | 任务 | 输入文件 | 输出文件 |
|------|------|---------|---------|
| product-manager | 处理偏差 | deviation-user.md | decision-user.md |
```

详细规范 → `references/05-status-mechanism.md`

### 二、拉取同步流程

git pull 后的动作：

1. `git log --oneline -5` 了解最近提交
2. **只读取 docs/status.md**（单文件，无需多个 index.md）
3. 查看"待处理项汇总"确认自己需要处理的任务
4. 执行任务
5. 更新 docs/status.md

详细流程 → `references/06-sync-flow.md`

### 三、版本归档

用户显式触发：
- "归档 v1.2" → 移动所有 v1.2 文档到 archive/v1.2/
- "开始 v1.3，归档旧版本" → 归档当前版本 + 更新索引

详细规范 → `references/05-status-mechanism.md`

### 四、测试协作框架

开发 skill 与全局测试 skill 的协作规范：

| 开发阶段 | 调用全局 Skill | 目的 |
|---------|---------------|------|
| **实现前** | `test-driven-development` | 先写测试 |
| **实现中** | 遵循 skill 的测试规范 | 遵循命名/结构/Mock 规范 |
| **实现后** | `test-generation` | 覆盖分析 |

详细规范 → `references/testing-collaboration.md`

---

## 与其他 Skill 协作

本 skill 被以下 skill 引用：
- `product-manager` → 协同开发流程、status.md 更新
- `tech-manager` → 协同开发流程、拉取同步
- `java-backend-dev` → 测试协作、拉取同步
- `vben-frontend-dev` → 测试协作、拉取同步

引用方式：
```
→ `team-collaboration/references/06-sync-flow.md`
```

---

## 参考文档索引

| 文档 | 内容 | 何时加载 |
|------|------|----------|
| `01-overview.md` | 概述 + 文档索引 | 项目初始化 |
| `02-project-structure.md` | 项目目录结构 | 需要了解目录时 |
| `03-frontend-backend.md` | 前后端工程结构 | 开始开发前 |
| `04-git-workflow.md` | git 工作流 + 版本号规范 | 创建分支/提交时 |
| `05-status-mechanism.md` | status.md + 归档机制 | 更新状态/归档 |
| `06-sync-flow.md` | 拉取同步流程 | git pull 后 |
| `07-examples.md` | 协作场景示例 | 了解完整流程 |
| `08-ai-config.md` | AI 配置 + 检查清单 | 项目初始化 |
| `testing-collaboration.md` | 测试协作框架 | 开发过程中 |

---

## 版本

- v1.0
- 更新: 2026-04-11
- 变更: 从 docs/collaboration + docs/shared 合并创建