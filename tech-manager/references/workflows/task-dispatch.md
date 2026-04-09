# 任务分发流程

**何时使用**: 变更分析完成后，需要将任务分发给前后端开发并行执行。

---

## 核心机制

通过 `task()` 工具并行启动 subagent，让它们加载对应的开发 skill 执行变更。

---

## 流程步骤

```
1. 确认变更任务
   ├── 已完成变更影响分析
   ├── 明确后端任务内容
   └── 明确前端任务内容

2. 生成任务块
   ├── 后端任务块 → 包含：改动内容、涉及文件、接口变化、注意事项
   └── 前端任务块 → 包含：改动内容、涉及页面、接口变化、注意事项

3. 并行启动 subagent
   ├── 启动后端开发 subagent（加载 backend-dev skill）
   └── 启动前端开发 subagent（加载 vben-saas-frontend skill）

4. 收集执行结果
   └── 等待 subagent 完成后汇总
```

---

## 任务分发执行

### 启动后端开发

```typescript
task(
  category: "deep",
  load_skills: ["backend-dev"],
  run_in_background: true,
  description: "后端变更任务",
  prompt: `
【变更任务】[任务名称]

**变更类型**: [新增功能/逻辑调整/字段变更/接口变更]
**优先级**: P0/P1/P2

**改动内容**:
1. [具体改动1]
2. [具体改动2]

**涉及文件**:
- [文件路径1]
- [文件路径2]

**接口变化**:
- [接口路径]: [变化说明]

**数据库变化**:
- [表名]: [变化说明]

**注意事项**:
- [注意点1]
- [注意点2]

请按照 backend-dev skill 规范执行开发任务。
  `
)
```

### 启动前端开发

```typescript
task(
  category: "deep",
  load_skills: ["vben-saas-frontend"],
  run_in_background: true,
  description: "前端变更任务",
  prompt: `
【变更任务】[任务名称]

**变更类型**: [新增页面/页面修改/组件调整]
**优先级**: P0/P1/P2

**改动内容**:
1. [具体改动1]
2. [具体改动2]

**涉及页面**:
- [页面路径1]
- [页面路径2]

**接口变化**:
- [接口路径]: [变化说明]

**注意事项**:
- [注意点1]
- [注意点2]

请按照 vben-saas-frontend skill 规范执行开发任务。
  `
)
```

---

## 任务块模板

### 后端任务块

```markdown
【变更任务】[任务名称]

**变更类型**: 新增功能/逻辑调整/字段变更/接口变更
**优先级**: P0/P1/P2

**改动内容**:
1. [具体改动描述]
2. [具体改动描述]

**涉及文件**:
- src/main/java/.../service/[ServiceName].java
- src/main/java/.../controller/[ControllerName].java
- src/main/java/.../entity/[EntityName].java

**接口变化**:
| 接口 | 变化类型 | 说明 |
|------|---------|------|
| GET /api/xxx | 新增/修改 | 说明 |

**数据库变化**:
| 表名 | 变化类型 | 说明 |
|------|---------|------|
| table_name | 新增字段/修改字段 | 说明 |

**注意事项**:
- [历史数据处理方式]
- [兼容性考虑]
- [性能关注点]
```

### 前端任务块

```markdown
【变更任务】[任务名称]

**变更类型**: 新增页面/页面修改/组件调整
**优先级**: P0/P1/P2

**改动内容**:
1. [具体改动描述]
2. [具体改动描述]

**涉及页面**:
- src/views/[module]/[page].vue
- src/components/[ComponentName].vue

**接口变化**:
| 接口 | 变化类型 | 说明 |
|------|---------|------|
| GET /api/xxx | 新增调用/参数变化 | 说明 |

**注意事项**:
- [交互细节]
- [状态管理]
- [边界场景]
```

---

## 完整示例

### 场景：审批流程从两级改为三级

**变更分析完成后，执行任务分发**：

```
分析结果：
- 后端：审批服务重构、接口返回值增加字段、数据库新增字段
- 前端：审批详情页调整、审批列表页增加筛选

并行启动：
```

**后端任务**:
```
【变更任务】审批服务三级审批重构

**变更类型**: 逻辑调整
**优先级**: P0

**改动内容**:
1. 审批服务增加二级审批节点
2. 审批接口返回值增加 secondApprover、secondApproveTime 字段
3. approval_record 表新增字段

**涉及文件**:
- src/main/java/.../service/ApprovalService.java
- src/main/java/.../controller/ApprovalController.java
- src/main/java/.../entity/ApprovalRecord.java

**接口变化**:
| 接口 | 变化类型 | 说明 |
|------|---------|------|
| GET /api/approvals/{id} | 修改 | 返回值新增 secondApprover 等字段 |
| POST /api/approvals/approve | 修改 | 支持二级审批操作 |

**数据库变化**:
| 表名 | 变化类型 | 说明 |
|------|---------|------|
| approval_record | 新增字段 | second_approver_id, second_approve_time |

**注意事项**:
- 历史数据 second_approver_id 默认为 null
- 需要新增二级审批人权限配置
```

**前端任务**:
```
【变更任务】审批详情页三级审批展示

**变更类型**: 页面修改
**优先级**: P0

**改动内容**:
1. 审批详情页增加二级审批人展示
2. 审批操作按钮根据状态显示
3. 审批列表页筛选增加"二级审批人"

**涉及页面**:
- src/views/approval/detail.vue
- src/views/approval/list.vue

**接口变化**:
| 接口 | 变化类型 | 说明 |
|------|---------|------|
| GET /api/approvals/{id} | 返回值变化 | 新增 secondApprover 字段 |

**注意事项**:
- 二级审批人可能为空（历史数据）
- 审批按钮显示逻辑需要适配三级状态
```

---

## 执行检查

启动 subagent 后，确认：

- [ ] 后端 subagent 已启动，加载 backend-dev skill
- [ ] 前端 subagent 已启动，加载 vben-saas-frontend skill
- [ ] 任务块内容完整（改动内容、涉及文件、注意事项）
- [ ] 等待 subagent 执行结果

---

## 结果汇总

subagent 完成后：

```markdown
## 任务执行结果

### 后端任务
- 状态: ✅ 完成 / ❌ 失败 / 🔄 进行中
- 完成内容: [已完成项]
- 问题: [遇到的问题]

### 前端任务
- 状态: ✅ 完成 / ❌ 失败 / 🔄 进行中
- 完成内容: [已完成项]
- 问题: [遇到的问题]

### 下一步
- [需要同步的内容]
- [需要验证的内容]
```