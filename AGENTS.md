# AGENTS.md

AI Skills 集合项目的开发指南。本项目定义了一系列 AI 编程助手可加载的专业技能。

---

## 项目概述

这是一个 **纯文档/定义项目**，没有可执行代码、测试或构建命令。主要产出是 Markdown 格式的 Skill 定义文件，供 AI 编程助手（Claude Code、OpenCode、Cursor 等）加载使用。

---

## Skill 文件结构

每个 Skill 目录遵循以下结构：

```
skill-name/
├── SKILL.md              # 必需 - 技能主文件
└── references/           # 可选 - 参考文档
    ├── topic-a.md
    ├── topic-b.md
    └── workflows/        # 可选 - 工作流定义
        └── workflow-a.md
```

---

## SKILL.md 格式规范

### YAML Frontmatter（必需）

```yaml
---
name: skill-name                    # 小写字母 + 连字符
description: |                      # 触发描述，用于 AI 判断是否加载
  简短描述技能用途。
  触发：关键词A/关键词B/关键词C。
  不适用：排除场景。
---
```

**description 规范**：
- 以 "Use when" 开头（英文）或直接描述触发场景（中文）
- 包含触发关键词，用 `/` 分隔
- 明确排除不适用的场景
- 总长度 < 500 字符

### 正文结构

```markdown
# Skill 名称

## 概述 / 何时使用
简述技能用途和触发场景。

## 快速路由（可选）
| 用户意图 | 执行流程 | 立即读取 |
|---------|---------|---------|
| ... | ... | ... |

## 核心能力
### 一、能力名称
描述 + 引用参考文档。

## 参考文档索引
| 文档 | 用途 | 何时加载 |
|------|------|----------|
| `file.md` | 说明 | 场景 |

## 版本
- v1.0
- 更新: YYYY-MM-DD
```

---

## 文档编写规范

### 格式规则

| 规则 | 说明 |
|------|------|
| **标题层级** | 最多 4 级（# → ####），避免过深 |
| **表格** | 用于结构化对比、参数说明 |
| **代码块** | 指定语言（`bash`、`typescript`、`markdown`） |
| **引用路径** | 使用 `@references/file.md` 格式 |
| **Mermaid 图表** | 流程图、ER图使用 Mermaid 语法 |

### 中文文档规范

| 规则 | 示例 |
|------|------|
| 标题不加点 | ✅ `## 概述` ❌ `## 概述。` |
| 表格左对齐 | 内容左对齐，表头可居中 |
| 中英文间距 | ✅ `使用 Vue 3 框架` ❌ `使用Vue 3框架` |
| 数字+单位 | ✅ `100 个` ❌ `100个` |

### 文件引用语法

```markdown
<!-- 引用同目录文件 -->
@file.md

<!-- 引用子目录文件 -->
@references/topic.md

<!-- 引用上级目录 -->
@../other-skill/SKILL.md

<!-- 引用特定章节 -->
@references/file.md#章节名
```

---

## 命名规范

### 目录命名

| 类型 | 规则 | 示例 |
|------|------|------|
| Skill 目录 | 小写字母 + 连字符 | `product-manager`、`java-backend-dev-skill` |
| 参考文件 | 小写 + 连字符 | `code-templates.md`、`api-design.md` |
| 工作流文件 | 小写 + 连字符 | `prd-writing.md`、`change-analysis.md` |

### Skill name 字段

- 使用小写字母和连字符
- 避免使用下划线或驼峰
- 示例：`tech-manager`、`vben-saas-frontend`

---

## Git 工作流

### 分支命名

```
feature/skill-name        # 新增技能
feature/skill-name-desc   # 新增功能描述
fix/skill-name            # 修复问题
docs/update-readme        # 文档更新
```

### Commit Message 格式

```
<type>(scope): <description>

类型：
- feat: 新增 skill 或功能
- fix: 修复错误
- docs: 文档更新
- refactor: 重构
- chore: 杂项

示例：
- feat(product-manager): 新增功能架构规范
- fix(tech-manager): 修正任务分发流程
- docs: 更新 README 技能列表
```

### 提交前检查

```bash
# 检查 SKILL.md 格式
# 1. YAML frontmatter 完整
# 2. name 和 description 字段存在
# 3. 版本号已更新

# 检查文件引用
# 确保所有 @path 引用的文件存在
```

---

## Skill 开发流程

### 新建 Skill

1. 创建目录：`skill-name/`
2. 创建 `SKILL.md`（含 YAML frontmatter）
3. 创建 `references/` 目录（如需要）
4. 更新 `README.md` 技能列表

### 更新现有 Skill

1. 修改 `SKILL.md` 或 `references/` 文件
2. 更新 SKILL.md 底部的版本信息
3. 如新增文件，更新参考文档索引表

### 版本号规则

- 小改动（修正错字、补充说明）：revision 不变
- 新增章节或文件：minor +1（v1.0 → v1.1）
- 结构重构或重大变更：major +1（v1.x → v2.0）

---

## 质量检查清单

编辑 Skill 后自检：

- [ ] YAML frontmatter 完整（name + description）
- [ ] description 包含触发关键词
- [ ] 所有 `@path` 引用的文件存在
- [ ] 表格格式正确（列数一致）
- [ ] 代码块指定了语言
- [ ] 版本号已更新
- [ ] README.md 技能列表已更新（如新增/删除 Skill）

---

## 常用命令

本项目为纯文档项目，无构建/测试命令。

```bash
# 检查文件结构
ls -la skill-name/

# 检查 YAML frontmatter
head -10 skill-name/SKILL.md

# 搜索引用
grep -r "@references" skill-name/
```

---

## 技能协作关系

```
product-manager (PRD)
       ↓
tech-manager (分析 → 分发)
       ↓
   ┌───┴───┐
   ↓       ↓
java     vben
backend  frontend
```

AI 助手应识别协作链路，在适当时机调用相关 Skill。

---

## 参考

- OpenSpec Skill 规范：`skill-creator` skill
- 技能列表：`README.md`