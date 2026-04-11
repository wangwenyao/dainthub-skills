# 拉取同步流程

git pull 后，**只读取 docs/status.md** 即可了解全局状态。

---

## Step 1：检查变更

```bash
git pull origin {branch}
git log --oneline -5           # 查看最近提交
```

---

## Step 2：读取状态快照

**只读取 `docs/status.md` 一个文件**，无需读取多个 index.md：

```markdown
# AI 拉取后动作：
1. 读取 docs/status.md（单文件，包含全局状态）
2. 查看"各模块当前状态"表 → 了解所有模块状态
3. 查看"待处理项汇总"表 → 确认自己需要处理的任务
4. 查看"下一步任务"表 → 确认具体输入/输出文件路径
```

---

## Step 3：各 Skill 拉取后动作

根据 status.md 执行对应动作：

### product-manager

| status.md 显示 | 动作 |
|---------------|------|
| 偏差反馈 🚧 | 读取对应 deviation 文件 → 执行偏差处理 |
| PRD 🚧 进行中 | 继续完成 PRD |
| 无待处理项 | 等待新需求 |

### tech-manager

| status.md 显示 | 动作 |
|---------------|------|
| PRD 🚧 → 新版本 | 读取 PRD → 变更分析 → OpenAPI + DML |
| 决策 🚧 → 需重新实现 | 重新分发任务 |
| 验证 ❌ | 等待偏差处理完成 |
| 无待处理项 | 等待开发完成触发验证 |

### java-backend-dev

| status.md 显示 | 动作 |
|---------------|------|
| DML 🚧 待执行 | 读取 DML 文件 → 执行脚本 → 更新 status.md |
| OpenAPI 有更新 | 读取 OpenAPI → 更新代码 |
| 无待处理项 | 继续当前开发 |

### vben-frontend-dev

| status.md 显示 | 动作 |
|---------------|------|
| 线框图 🚧 有更新 | 读取 YAML/HTML → 更新 Schema |
| OpenAPI 有更新 | 读取 OpenAPI → 更新 API |
| 无待处理项 | 继续当前开发 |

---

## Step 4：更新 status.md

完成任务后，更新 status.md：

| 完成的任务 | 更新内容 |
|----------|---------|
| 文档状态变更 | 更新"各模块当前状态"表中的状态符号 |
| 新增待处理项 | 添加到"待处理项汇总"表 |
| 任务完成 | 更新"下一步任务"表 |
| 提交代码 | 更新"最近变更"表 |

---

## 拉取同步检查清单

每次 git pull 后，AI 只需：

- [ ] `git log --oneline -5` 了解最近提交
- [ ] `读取 docs/status.md`（单文件，替代多个 index.md）
- [ ] 查看"待处理项汇总"确认自己需要处理的任务
- [ ] 查看"下一步任务"确认输入/输出文件路径
- [ ] 执行任务
- [ ] 更新 docs/status.md

---

## 版本

- v2.0
- 更新: 2026-04-11