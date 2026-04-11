# AI 配置与检查清单

---

## 项目级 AGENTS.md 示例

```markdown
# 项目 AI 配置

## 技能锁定

| Skill | 版本 | 来源 |
|-------|------|------|
| product-manager | v2.4 | dainthub-skills |
| tech-manager | v2.4 | dainthub-skills |
| java-backend-dev | v1.3 | dainthub-skills |
| vben-frontend-dev | v2.3 | dainthub-skills |

## 协作约定

- PRD 输出目录：docs/prd/
- OpenAPI 输出目录：docs/api/
- DML 输出目录：docs/db/
- 前端工程：frontend/
- 后端工程：backend/

## 版本同步

每次开发前：
1. git pull 获取最新 docs/
2. 读取 docs/status.md 了解当前状态（单文件）
3. 根据 status.md 中的"下一步任务"确认当前任务
4. 开发完成后更新 status.md（用户显式触发）

## 参考文档

- 分布式协同开发指南：docs/collaboration/
```

---

## 检查清单

### 开发前检查

- [ ] git pull 获取最新代码
- [ ] 读取 docs/status.md 了解当前状态（单文件）
- [ ] 确认技能版本（检查 .agents/skills.json）
- [ ] 根据 status.md 中的"下一步任务"确认输入文件

### 开发后检查

- [ ] 代码已提交到正确分支
- [ ] 更新 docs/status.md（状态变更 + 最近变更）- **用户显式触发**
- [ ] 如有归档需求，执行版本归档 - **用户显式触发**
- [ ] 运行测试验证
- [ ] git push 推送变更

### 合并前检查

- [ ] docs/status.md 中验证状态为 ✅
- [ ] 偏差报告已处理（status.md 中无 🚧 偏差）
- [ ] 决策记录已生成（docs/decisions/）
- [ ] 冲突已解决
- [ ] git merge 到 develop

---

## 技能链路协作关系

```
product-manager
       ↓ docs/prd/ + docs/wireframes/ + docs/status.md
       
tech-manager
       ↓ docs/api/ + docs/db/ + docs/reports/ + docs/status.md
       ↓ 任务分发（携带文档路径）
       
       ┌────────────────┴────────────────┐
       ↓                                 ↓
java-backend-dev                   vben-frontend-dev
（读取 docs/status.md + docs/db/ + docs/api/）  （读取 docs/status.md + docs/api/ + docs/wireframes/）
       ↓                                 ↓
       └─── backend/ ────────── frontend/ ────┘
                        ↓
                 tech-manager 实现验证
                        ↓
                 docs/reports/verify-{模块}-v{版本}.md
                        ↓
                 偏差反馈 → product-manager 决策
                        ↓
                 docs/decisions/ + docs/prd/ + docs/status.md 更新
```

---

## 版本

- v2.0
- 更新: 2026-04-11