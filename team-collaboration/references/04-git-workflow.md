# Git 工作流

分布式协同开发中的 Git 操作规范，确保多角色、多会话之间的代码一致性。

---

## 分支结构详细说明

### 分支层级图

```
main (生产环境)
  │
  │  ← merge from develop (release)
  │
develop (开发集成)
  │
  │  ← merge from feature/* (功能完成)
  │
feature/{模块}-v{版本} (功能开发)
  │
  │  ← rebase from develop (每日同步)
  │
工作目录 (AI 当前会话)
```

### 各分支职责

| 分支 | 职责 | 操作限制 | 生命周期 |
|------|------|---------|---------|
| `main` | 生产代码，已发布版本 | 只接受 merge，禁止直接 push | 永久 |
| `develop` | 开发集成，每日自动测试 | 接受 feature merge，禁止直接修改 | 永久 |
| `feature/*` | 单功能/模块开发 | 可自由修改，完成后 merge 到 develop | 临时（完成后删除） |

### 分支保护规则

**main 分支**：
- 禁止 `git push origin main`
- 禁止 `git commit` 直接在 main 上
- 只通过 PR/merge 从 develop 合入
- 合入前必须通过测试验证

**develop 分支**：
- 禁止直接修改业务代码
- 只接受 feature 分支的 merge
- 每日自动运行集成测试
- merge 后触发 CI 构建

**feature 分支**：
- 单人/单 AI 会话负责
- 每日 rebase develop 保持同步
- 完成后删除（merge 成功后）

---

## 分支创建与切换流程

### 创建 feature 分支

**标准流程**：

```bash
# 1. 确保在 develop 分支
git checkout develop

# 2. 拉取最新代码
git pull origin develop

# 3. 创建 feature 分支
git checkout -b feature/{模块}-v{版本}

# 示例
git checkout -b feature/product-v1.2
git checkout -b feature/user-v1.3
git checkout -b fix/order-v1.2
```

### 分支切换时机

| 场景 | 切换目标 | 命令 |
|------|---------|------|
| 开始新功能开发 | develop → feature | `git checkout -b feature/xxx` |
| 继续已有功能开发 | 切换到对应 feature | `git checkout feature/xxx` |
| 功能完成准备合并 | feature → develop | `git checkout develop` |
| 查看生产代码 | → main | `git checkout main` |
| 每日同步 develop | feature 上执行 rebase | 见下方 |

### 分支间同步策略

**feature 分支每日同步 develop**：

```bash
# 在 feature 分支上执行
git checkout feature/product-v1.2

# 拉取 develop 最新代码
git fetch origin develop

# rebase 到 develop（保持线性历史）
git rebase origin/develop

# 如果有冲突，解决后继续
git status              # 查看冲突文件
# 手动解决冲突
git add .               # 标记已解决
git rebase --continue   # 继续 rebase

# 推送到远程（首次需要 -u）
git push origin feature/product-v1.2
# 如果之前已推送，rebase 后需要 force push
git push origin feature/product-v1.2 --force-with-lease
```

**同步时机**：
- 每日开始工作前
- develop 有重要更新后（其他模块合并）
- 准备 merge 前必须同步

---

## 提交规范详细版

### Commit Message 格式

```
<type>(scope): <description>

[可选：详细说明]
[可选：关联 issue/PRD]
```

### Type 类型说明

| Type | 含义 | 使用场景 |
|------|------|---------|
| `feat` | 新增功能 | 新模块、新接口、新页面 |
| `fix` | Bug 修复 | 修复已知问题 |
| `docs` | 文档更新 | PRD、OpenAPI、DML、status.md |
| `refactor` | 重构 | 不改变功能的代码优化 |
| `test` | 测试相关 | 测试代码、测试配置 |
| `chore` | 杂项 | 配置、依赖、工具 |

### Scope 规范（模块名列表）

| Scope | 对应模块 | 示例 |
|-------|---------|------|
| `product` | 商品模块 | `feat(product): 新增商品列表页` |
| `user` | 用户模块 | `fix(user): 修复登录状态校验` |
| `order` | 订单模块 | `docs(order): 更新订单 OpenAPI` |
| `trade` | 交易模块 | `refactor(trade): 优化支付流程` |
| `system` | 系统配置 | `chore(system): 更新数据库连接配置` |
| `api` | 接口文档 | `docs(api): 更新 OpenAPI v1.2` |
| `db` | 数据库脚本 | `docs(db): 新增 user 表 DML` |
| `status` | 状态快照 | `docs(status): 更新 status.md v1.2` |

### 多文件提交策略

**按逻辑分组提交**：

```bash
# 错误：一次提交所有文件
git add .
git commit -m "feat(product): 完成商品模块"

# 正确：按逻辑分组
git add src/main/java/com/example/product/controller/
git commit -m "feat(product): 新增商品 Controller"

git add src/main/java/com/example/product/service/
git commit -m "feat(product): 新增商品 Service"

git add docs/api/product-openapi.yaml
git commit -m "docs(api): 更新商品 OpenAPI v1.2"
```

### AI 执行的 Commit Message 示例

**开发完成提交**：
```
feat(product): 新增商品列表查询接口

- 新增 ProductController.list()
- 新增 ProductService.queryList()
- 新增 ProductMapper.xml 查询语句

关联 PRD: docs/prd/product-v1.2.md
```

**文档更新提交**：
```
docs(status): 更新 status.md 商品模块状态

- PRD: v1.2 ✅
- OpenAPI: v1.2 ✅
- DML: v1.2 ✅
- 当前阶段: 开发中
```

**Bug 修复提交**：
```
fix(order): 修复订单状态字段类型

问题：order_status 字段定义为 varchar，应为 tinyint
修复：修改实体类字段类型 + 更新 Mapper.xml

关联偏差报告: docs/reports/deviation-order-v1.2.md
```

### 禁止的提交模式

| 禁止行为 | 原因 | 正确做法 |
|---------|------|---------|
| 提交敏感文件 | 安全风险 | `.gitignore` 排除 |
| 提交未测试代码 | 可能引入 Bug | 本地测试后再提交 |
| 提交到 main 分支 | 破坏生产稳定性 | 通过 feature → develop → main |
| 一个提交包含多模块 | 难以追踪变更 | 按模块分开提交 |
| Commit message 无 type | 无法分类 | 使用标准格式 |
| Commit message 无 scope | 无法定位模块 | 添加 scope |

---

## 合并流程

### feature → develop 合并流程

```bash
# 1. 在 feature 分支完成开发
git checkout feature/product-v1.2

# 2. 最后一次同步 develop
git fetch origin develop
git rebase origin/develop

# 3. 推送 feature 分支
git push origin feature/product-v1.2

# 4. 切换到 develop
git checkout develop
git pull origin develop

# 5. 合并 feature（使用 --no-ff 保持分支历史）
git merge feature/product-v1.2 --no-ff -m "merge: feature/product-v1.2 → develop"

# 6. 推送 develop
git push origin develop

# 7. 删除本地 feature 分支
git branch -d feature/product-v1.2

# 8. 删除远程 feature 分支
git push origin --delete feature/product-v1.2
```

### 冲突解决策略（AI 场景）

**原则：不能随意覆盖他人代码**

```bash
# 合并时发现冲突
git merge feature/product-v1.2
# 输出：CONFLICT (content): Merge conflict in xxx.java

# 1. 查看冲突文件
git status

# 2. 查看冲突内容
git diff --name-only --diff-filter=U

# 3. AI 处理策略
# - 如果是自己模块的文件：保留自己的修改
# - 如果是公共文件（如配置）：需要人工确认
# - 如果不确定：暂停合并，询问用户

# 4. 解决冲突后
git add .
git commit -m "merge: feature/product-v1.2 → develop (冲突已解决)"

# 5. 如果无法解决，放弃合并
git merge --abort
# 通知用户需要人工介入
```

**AI 冲突处理优先级**：

| 冲突类型 | 处理方式 |
|---------|---------|
| 自己模块的业务代码 | 保留自己的修改 |
| 公共配置文件 | 暂停，询问用户 |
| 依赖版本冲突 | 暂停，询问用户 |
| 不确定来源的代码 | 暂停，询问用户 |

### develop → main 发布流程

```bash
# 1. 确保 develop 通过测试
# （CI 自动运行，或手动触发）

# 2. 切换到 main
git checkout main
git pull origin main

# 3. 合并 develop（发布版本）
git merge develop --no-ff -m "release: v1.2 发布"

# 4. 打版本标签
git tag -a v1.2 -m "Release v1.2: 商品模块上线"

# 5. 推送 main 和标签
git push origin main
git push origin v1.2

# 6. 归档当前版本文档
# （触发 team-collaboration 的归档流程）
```

---

## 版本号管理

### 语义化版本号

格式：`v{大版本}.{小版本}`

| 版本变更 | 规则 | 示例 | 触发条件 |
|---------|------|------|---------|
| 大版本 | +1.0 | v1.0 → v2.0 | 架构重构、重大功能变更、技术栈升级 |
| 小版本 | +0.1 | v1.0 → v1.1 | 功能迭代、Bug 修复、小优化 |

### 版本号在 status.md 中的使用

```markdown
## 各模块当前状态
| 模块 | PRD | OpenAPI | DML | 线框图 | 验证 | 偏差 | 当前阶段 |
|------|-----|---------|-----|--------|------|------|---------|
| product | v1.2 ✅ | v1.2 ✅ | v1.2 ✅ | v1.2 ✅ | - | - | 开发中 |
| user | v1.1 ✅ | v1.1 ✅ | v1.1 ✅ | v1.1 ✅ | ✅ | - | ✅ 已完成 |
```

**版本号一致性**：
- 同一模块的所有文档使用相同版本号
- PRD、OpenAPI、DML、线框图版本号必须一致
- 版本号变更时同步更新所有相关文档

### 版本号与分支的关系

| 分支 | 版本号 | 说明 |
|------|-------|------|
| `feature/product-v1.2` | v1.2 | 开发 v1.2 版本的 product 模块 |
| `develop` | 当前开发版本 | 集成所有 feature 分支 |
| `main` + tag `v1.2` | v1.2 | 已发布的 v1.2 版本 |

**版本号流转**：
```
feature/product-v1.2 (开发)
    ↓ merge
develop (集成)
    ↓ merge + tag
main + v1.2 tag (发布)
```

---

## AI 专用 Git 规范

### 提交前必须检查的清单

**AI 在执行 `git commit` 前必须检查**：

```markdown
## 提交前检查清单

1. [ ] 当前分支正确（feature/xxx，不是 main/develop）
2. [ ] 修改的文件属于当前模块（不跨模块修改）
3. [ ] 代码已通过本地测试（如有测试）
4. [ ] Commit message 格式正确（type(scope): desc）
5. [ ] Scope 与当前模块匹配
6. [ ] 未提交敏感文件（.env、credentials 等）
7. [ ] status.md 已更新（如涉及状态变更）
```

**检查命令**：

```bash
# 检查当前分支
git branch --show-current

# 检查待提交文件
git status

# 检查文件是否属于当前模块
git diff --name-only

# 检查是否有敏感文件
git diff --name-only | grep -E "\.env|credentials|password"
```

### status.md 更新与 git commit 的配合

**顺序：先更新 status.md，再 commit**

```bash
# 1. 完成开发任务
# （如：完成 product 模块 OpenAPI 文档）

# 2. 更新 status.md
# 编辑 docs/status.md，更新对应模块状态

# 3. 提交文档变更
git add docs/api/product-openapi.yaml
git commit -m "docs(api): 更新商品 OpenAPI v1.2"

# 4. 提交 status.md 变更
git add docs/status.md
git commit -m "docs(status): 更新商品模块状态为 OpenAPI ✅"

# 5. 推送
git push origin feature/product-v1.2
```

**status.md 状态字段与 commit 的对应**：

| 状态变更 | Commit message 示例 |
|---------|---------------------|
| PRD 完成 | `docs(prd): 完成 product PRD v1.2` |
| OpenAPI 完成 | `docs(api): 完成 product OpenAPI v1.2` |
| DML 完成 | `docs(db): 完成 product DML v1.2` |
| 开发完成 | `feat(product): 完成 product 模块开发` |
| 验证通过 | `docs(status): product 模块验证通过` |

### 多角色协作中的 git 操作顺序

**产品经理 → 技术经理 → 开发 → 验证**

```
角色          Git 操作                          Commit message
───────────────────────────────────────────────────────────────
product-manager
  │           git add docs/prd/product-v1.2.md
  │           git commit                        docs(prd): 完成 product PRD v1.2
  │           git add docs/status.md
  │           git commit                        docs(status): product PRD ✅
  │
tech-manager
  │           git pull                          (同步 PRD)
  │           git add docs/api/product-openapi.yaml
  │           git commit                        docs(api): 完成 product OpenAPI v1.2
  │           git add docs/db/product-dml.sql
  │           git commit                        docs(db): 完成 product DML v1.2
  │           git add docs/status.md
  │           git commit                        docs(status): product OpenAPI/DML ✅
  │
java-backend-dev
  │           git pull                          (同步 OpenAPI/DML)
  │           git add src/main/java/...
  │           git commit                        feat(product): 完成 product 后端开发
  │           git add docs/status.md
  │           git commit                        docs(status): product 后端 ✅
  │
vben-frontend-dev
  │           git pull                          (同步 OpenAPI)
  │           git add src/views/...
  │           git commit                        feat(product): 完成 product 前端开发
  │           git add docs/status.md
  │           git commit                        docs(status): product 前端 ✅
  │
tech-manager
  │           git pull                          (同步开发成果)
  │           验证实现
  │           git add docs/status.md
  │           git commit                        docs(status): product 验证 ✅
```

### AI 会话结束前的 Git 操作

**会话结束前必须执行**：

```bash
# 1. 检查是否有未提交的变更
git status

# 2. 如果有变更，提交
git add .
git commit -m "docs(status): 更新状态快照"

# 3. 推送到远程
git push origin feature/product-v1.2

# 4. 确认推送成功
git log --oneline -3
```

**如果无法推送**：
- 记录当前状态到本地文件
- 通知用户需要手动推送
- 在 status.md 中标注"待推送"

---

## 常见问题处理

### 问题：feature 分支落后 develop

```bash
# 查看落后情况
git fetch origin
git log HEAD..origin/develop --oneline

# 解决：rebase
git rebase origin/develop
```

### 问题：合并时冲突无法解决

```bash
# 放弃合并
git merge --abort

# 通知用户
echo "合并冲突需要人工介入，已暂停合并操作"
```

### 问题：误提交到错误分支

```bash
# 如果未推送，撤销提交
git reset --soft HEAD~1

# 切换到正确分支
git checkout feature/product-v1.2

# 重新提交
git commit -m "feat(product): xxx"
```

### 问题：需要回退已推送的提交

```bash
# 创建回退提交（不改变历史）
git revert <commit-hash>

# 推送回退
git push origin feature/product-v1.2
```

---

## 版本

- v1.1
- 更新: 2025-01-14
- 变更: 扩展分支结构、合并流程、AI 专用规范