# status.md 状态快照与归档机制

---

## status.md 格式

AI 拉取后只读这一个文件，无需读取多个 index.md。

```markdown
# 项目状态快照

> AI 拉取后只需读取此文件了解全局状态
> 更新时间：2026-04-11 10:30

## 各模块当前状态

| 模块 | PRD | OpenAPI | DML | 线框图 | 验证 | 偏差 | 决策 | 当前阶段 |
|------|-----|---------|-----|--------|------|------|------|---------|
| product | v1.2 ✅ | v1.2 ✅ | v1.2 ✅ | v1.2 ✅ | v1.2 ✅ | - | - | ✅ 已完成 |
| trade | v1.1 🚧 | v1.1 ✅ | v1.1 🚧 | v1.1 ✅ | - | - | - | 🚧 DML待执行 |
| user | v1.0 ✅ | v1.0 ✅ | v1.0 ✅ | v1.0 ✅ | v1.0 ❌ | v1.0 🚧 | - | 🚧 偏差待处理 |

## 待处理项汇总

| 类型 | 模块 | 版本 | 文件路径 | 处理角色 |
|------|------|------|---------|---------|
| 偏差反馈 | user | v1.0 | docs/reports/deviation-user-v1.0.md | product-manager |
| DML执行 | trade | v1.1 | docs/db/dml-trade-v1.1.sql | java-backend-dev |

## 最近变更（最近 5 条）

| 时间 | 提交 | 变更内容 | 影响模块 |
|------|------|---------|---------|
| 2026-04-11 10:00 | abc123 | 新增 user 模块验证报告 | user |

## 下一步任务

| 角色 | 任务 | 输入文件 | 输出文件 |
|------|------|---------|---------|
| product-manager | 处理 user 偏差反馈 | docs/reports/deviation-user-v1.0.md | docs/decisions/decision-user-*.md |
```

---

## 状态符号说明

| 符号 | 含义 | 后续动作 |
|------|------|---------|
| ✅ | 已完成 | 无需处理 |
| 🚧 | 进行中 | 需要继续开发/处理 |
| ❌ | 不通过 | 需要修复或偏差处理 |
| ⏸️ | 待处理 | 等待前置条件 |
| - | 无此版本 | 不涉及 |

---

## 触发指令（用户显式触发）

### status.md 更新

| 触发指令 | AI 执行动作 | 适用场景 |
|---------|------------|---------|
| "更新 status.md" | 更新当前模块状态 + 最近变更 | 完成任务后 |
| "记录提交到 status.md" | 添加最近变更记录 | git commit 后 |
| "更新下一步任务" | 更新"下一步任务"表 | 任务分发/完成后 |
| "新增模块到 status.md" | 添加新模块行 | 开始新模块开发 |

**示例**：

```
用户：我完成了 product 模块的 PRD v1.2，帮我更新 status.md

AI 执行：
1. 读取 docs/status.md
2. 更新"各模块当前状态"表中 product 行：
   - PRD: v1.2 ✅
   - 当前阶段: 🚧 PRD完成，待技术分析
3. 更新"最近变更"表：添加本次提交记录
4. 更新"下一步任务"表：
   - tech-manager: 分析 product PRD → docs/prd/prd-product-v1.2.md
```

**注意**：AI 不会自动更新 status.md，需要用户显式触发。

---

### 版本归档

| 触发指令 | AI 执行动作 | 适用场景 |
|---------|------------|---------|
| "归档 v1.2" | 移动 v1.2 所有文档到 archive/v1.2/ | 开始新版本前 |
| "开始 v1.3，归档旧版本" | 归档当前 ✅ 版本 + 更新 index.md | 版本迭代 |
| "归档 product v1.2" | 只归档指定模块的 v1.2 | 部分归档 |

**示例**：

```
用户：开始做 product v1.3，帮我归档 v1.2

AI 执行：
1. mkdir docs/archive/v1.2/{prd,api,db,wireframes,reports,decisions}
2. mv docs/prd/prd-product-v1.2.md docs/archive/v1.2/prd/
3. mv docs/api/openapi-product-v1.2.yaml docs/archive/v1.2/api/
4. ... 移动其他文件
5. 更新 docs/prd/index.md：移除 v1.2 行
6. 更新 docs/status.md：删除 v1.2 行，添加 v1.3 🚧
```

**注意**：归档需要用户显式触发，AI 不会自动归档。

---

## 精简 index.md 格式

只保留最新版本 + 进行中版本，旧版本归档。

```markdown
# {目录名} 索引

> 当前版本 + 进行中版本，旧版本见 archive/

## 当前版本

| 文件 | 版本 | 状态 | 说明 |
|------|------|------|------|
| prd-product-v1.2.md | v1.2 | ✅ | 最新稳定版本 |

## 进行中版本

| 文件 | 版本 | 状态 | 说明 |
|------|------|------|------|
| prd-product-v1.3.md | v1.3 | 🚧 | 新增 SKU 字段 |

---

> 归档版本见 `archive/v1.0/`、`archive/v1.1/`
```

---

## 归档目录结构

```
docs/
├── archive/
│   ├── v1.0/                          # v1.0 所有文档归档
│   │   ├── prd/
│   │   ├── api/
│   │   ├── db/
│   │   ├── wireframes/
│   │   ├── reports/
│   │   ├── decisions/
│   │   └── index.md                   # v1.0 归档索引
│   ├── v1.1/
│   │   └── ...（同上结构）
│   └── index.md                       # 归档总索引
│
├── prd/
│   ├── index.md                       # 只保留最新 + 进行中
│   ├── prd-product-v1.2.md            # 最新稳定版本
│   └── prd-product-v1.3.md            # 进行中版本
│
└── status.md                          # 当前状态快照
```

