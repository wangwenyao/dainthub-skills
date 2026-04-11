# 迭代循环工作流

完整需求开发的迭代循环机制，确保所有模块按优先级依次完成。

---

## 迭代模式

### 模式 A：单 AI 会话串行（推荐小型项目）

一个 AI 会话中按优先级依次完成所有模块：

```
初始化 → 模块1(P0) → 模块2(P0) → 模块3(P1) → ...
        PRD→TM→Dev→Verify→闭环
```

**触发指令**：
```
"按优先级完成所有模块开发"
"继续下一个模块"
```

---

### 模式 B：多 AI 会话并行（推荐大型项目）

多个 AI 会话分别处理不同模块，通过 status.md 同步：

```
会话1: product 模块  ──→ git push → status.md
会话2: trade 模块   ──→ git push → status.md
会话3: user 模块    ──→ git push → status.md

git pull → 读取 status.md → 确认自己的任务
```

**触发指令**：
```
"git pull 后，帮我处理待处理项"
"检查 status.md，告诉我该做什么"
```

---

## 迭代循环流程

### Phase 0：项目初始化

```bash
# 创建项目目录结构
docs/
├── status.md          # 状态快照（核心）
├── prd/
├── api/
├── db/
├── wireframes/
├── reports/
└── decisions/
```

**触发指令**：
```
"初始化项目，创建 docs/status.md"
```

**AI 执行**：
1. 创建目录结构
2. 生成初始 status.md（列出所有待开发模块）
3. 生成 docs/prd/index.md 等索引文件

**status.md 初始模板**：
```markdown
# 项目状态快照

> 更新时间：{时间}

## 各模块当前状态

| 模块 | 优先级 | PRD | OpenAPI | DML | 线框图 | 验证 | 偏差 | 当前阶段 |
|------|--------|-----|---------|-----|--------|------|------|---------|
| product | P0 | - | - | - | - | - | - | ⏸️ 待开始 |
| trade | P0 | - | - | - | - | - | - | ⏸️ 待开始 |
| user | P1 | - | - | - | - | - | - | ⏸️ 待开始 |

## 待处理项汇总

| 类型 | 模块 | 任务 | 处理角色 |
|------|------|------|---------|
| PRD编写 | product | 编写商品管理PRD | product-manager |
| PRD编写 | trade | 编写订单管理PRD | product-manager |

## 下一步任务

| 角色 | 任务 | 优先级 |
|------|------|--------|
| product-manager | 编写 product PRD | P0 |
| product-manager | 编写 trade PRD | P0 |
```

---

### Phase 1：按优先级迭代

**循环逻辑**：

```
while (有待处理项) {
  1. 读取 status.md
  2. 找到最高优先级的待处理项
  3. 调用对应 skill 执行
  4. 更新 status.md
  5. git commit + push
  6. 用户确认：继续下一个？
}
```

**单会话迭代指令**：

```
"开始迭代开发，按优先级依次完成"
  → AI 读取 status.md
  → 找到 product-manager 的 P0 任务
  → 执行 product-manager skill
  → 完成 PRD
  → 更新 status.md
  → git commit
  
"继续下一个模块"
  → AI 读取 status.md
  → 找到 tech-manager 的待处理项（PRD已完成）
  → 执行 tech-manager skill
  → 生成 OpenAPI + DML
  → 更新 status.md
  → git commit
  
"继续"
  → AI 读取 status.md
  → 找到 java-backend-dev / vben-frontend-dev 的待处理项
  → 并行执行开发
  → 更新 status.md
  → git commit
  
"继续"
  → AI 读取 status.md
  → 找到 tech-manager 的验证任务
  → 执行实现验证
  → 如有偏差 → 反馈给 PM
  → 更新 status.md
  
"继续"
  → AI 读取 status.md
  → 找到 product-manager 的偏差决策任务
  → 执行偏差处理
  → 更新 status.md
  → git commit
  
... 直到所有模块 ✅ 已完成
```

---

### Phase 2：多会话协作

**每个会话的工作模式**：

```
git pull origin {branch}
  ↓
读取 docs/status.md
  ↓
找到"待处理项汇总"中属于自己角色的任务
  ↓
执行对应 skill
  ↓
更新 status.md
  ↓
git add docs/status.md + 输出文件
git commit -m "完成 {模块} {阶段}"
git push
```

**会话 A (PM)**：
```
$ git pull
$ AI: "检查 status.md"

AI: 您有 2 个待处理任务：
  1. 编写 product PRD (P0)
  2. 处理 user 偏差反馈 (P1)

用户: "先做 product PRD"
→ AI 执行 product-manager skill
→ 输出 docs/prd/prd-product-v1.0.md + docs/wireframes/wireframes-product.html
→ 更新 status.md

用户: "记录到 status.md 并提交"
→ git add docs/
→ git commit -m "完成 product PRD v1.0"
→ git push
```

**会话 B (TM)**：
```
$ git pull
$ AI: "检查 status.md"

AI: 您有 1 个待处理任务：
  1. 分析 product PRD → 生成 OpenAPI + DML

用户: "执行"
→ AI 执行 tech-manager skill
→ 输出 docs/api/openapi-product-v1.0.yaml + docs/db/dml-product-v1.0.sql
→ 更新 status.md

用户: "提交"
→ git add docs/
→ git commit -m "完成 product OpenAPI + DML v1.0"
→ git push
```

---

## 自动循环触发

### 方式 1：显式确认循环

每完成一个阶段，AI 询问：
```
"已完成 product PRD。下一步任务：tech-manager 分析 product PRD。
是否继续？(y/n)"
```

用户输入 `y` → AI 自动调用 tech-manager skill
用户输入 `n` → AI 更新 status.md 后结束

### 方式 2：批量迭代指令

```
"批量完成 product 模块从 PRD 到验证的全流程"
```

AI 执行：
```
1. product-manager → PRD
2. tech-manager → OpenAPI + DML
3. java-backend-dev + vben-frontend-dev → 并行开发
4. tech-manager → 实现验证
5. 如有偏差 → product-manager → 偏差决策
6. 循环直到 ✅ 已完成
```

### 方式 3：项目级迭代指令

```
"按优先级依次完成所有模块，直到全部 ✅"
```

AI 执行：
```
while (status.md 有 ⏸️ 或 🚧 的模块) {
  优先级排序: P0 > P1 > P2
  取第一个模块
  执行完整链路: PRD → TM → Dev → Verify → 闭环
  更新 status.md
  git commit
  询问用户：继续下一个模块？
}
```

---

## 迭代进度追踪

### status.md 状态流转

```
⏸️ 待开始 → 🚧 PRD进行中 → 🚧 PRD完成(待TM) → 🚧 TM完成(待Dev) 
→ 🚧 Dev进行中 → 🚧 验证进行中 → 
  ├─ ✅ 已完成
  └─ ❌ 不通过 → 🚧 偏差处理 → ✅ 已完成 / 重新实现
```

### 每阶段完成后的 status.md 更新模板

**PRD 完成后**：
```markdown
| product | P0 | v1.0 ✅ | - | - | v1.0 ✅ | - | - | 🚧 待技术分析 |

## 待处理项汇总
| 类型 | 模块 | 任务 | 处理角色 |
|------|------|------|---------|
| 技术分析 | product | 分析 PRD + 生成 OpenAPI + DML | tech-manager |

## 下一步任务
| 角色 | 任务 | 输入文件 |
|------|------|---------|
| tech-manager | product 技术分析 | docs/prd/prd-product-v1.0.md |
```

**开发完成后**：
```markdown
| product | P0 | v1.0 ✅ | v1.0 ✅ | v1.0 ✅ | v1.0 ✅ | - | - | 🚧 待验证 |

## 待处理项汇总
| 类型 | 模块 | 任务 | 处理角色 |
|------|------|------|---------|
| 实现验证 | product | 对照 PRD 验证代码 | tech-manager |
```

---

## 迭代终止条件

循环终止当：
1. **所有模块 ✅ 已完成** — 全部需求实现并验证通过
2. **用户终止** — 输入 `stop` 或 `暂停`
3. **阻塞项未解决** — 偏差决策未完成，等待用户确认

---

## 完整迭代示例

**场景**：商品管理 + 订单管理 + 用户管理

```
用户: "初始化项目，三个模块：product(P0)、trade(P0)、user(P1)"

AI:
- 创建 docs/status.md，列出三个模块
- 下一步任务：product-manager 编写 product/trade PRD

用户: "按优先级完成所有模块"

AI (迭代 1):
- 读取 status.md
- 执行 product-manager → product PRD ✅
- 执行 tech-manager → product OpenAPI + DML ✅
- 并行: java-backend + vben-frontend → product 开发 ✅
- 执行 tech-manager → product 验证 ✅
- 更新 status.md: product ✅ 已完成
- git commit

AI (迭代 2):
- 读取 status.md
- 找到 trade (P0, ⏸️)
- 执行 product-manager → trade PRD ✅
- ... 同上流程
- trade ✅ 已完成

AI (迭代 3):
- 读取 status.md
- 找到 user (P1, ⏸️)
- ... 同上流程
- user 验证 ❌ → 偏差反馈

AI (迭代 4 - 偏差处理):
- 执行 product-manager → 偏差决策
- 决策：接受偏差，更新 PRD
- tech-manager → 重新验证 ✅
- user ✅ 已完成

AI:
- 检查 status.md：所有模块 ✅ 已完成
- 迭代终止

用户: "全部完成，归档 v1.0"
AI:
- 执行归档流程
- 创建 docs/archive/v1.0/
```

---

## 版本

- v1.0
- 更新: 2026-04-12
- 变更: 新增迭代循环工作流