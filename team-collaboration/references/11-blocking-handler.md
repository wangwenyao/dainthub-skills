# 阻塞处理规范

/ralph-loop 循环执行过程中遇到阻塞时的处理逻辑。

---

## 阻塞类型

| 阻塞类型 | 触发条件 | 处理角色 |
|---------|---------|---------|
| 偏差阻塞 | 实现验证 ❌，生成偏差报告 | product-manager |
| 前置未完成 | 任务依赖的前置任务未完成 | 等待前置完成 |
| 用户暂停 | 用户输入 `stop` 或 `暂停` | 等待用户恢复 |
| 资源冲突 | 多会话同时修改同一文件 | 协调顺序 |

---

## 偏差阻塞处理

### 触发流程

```
tech-manager 实现验证
    ↓
发现 PRD 与实现不一致
    ↓
生成偏差报告（deviation-{模块}-v{版本}.md）
    ↓
更新 status.md:
  - 验证: ❌
  - 偏差: 🚧
  - 新增待处理项: 偏差决策 → product-manager
    ↓
/ralph-loop 检测到阻塞 → 暂停循环
    ↓
询问用户决策
```

### 偏差报告格式

```markdown
# 实现偏差报告

## 基本信息
- 模块: user
- 版本: v1.0
- 生成时间: 2026-04-12 10:30

## 偏差项列表

| # | PRD 规格 | 实际实现 | 偏差类型 | 影响评估 |
|---|---------|---------|---------|---------|
| 1 | 用户状态枚举: active/inactive/banned | 实现为: active/inactive | 缺少 banned | 中等 |
| 2 | 注册必须验证邮箱 | 实现为可选验证 | 逻辑简化 | 低 |

## 建议处理方案

| # | 方案 | 说明 | 影响 |
|---|------|------|------|
| 1 | 接受偏差 | 调整 PRD，删除 banned 状态 | 需更新 PRD |
| 2 | 坚持原需求 | 开发补充 banned 状态 | 需重新开发 |
| 3 | 协商调整 | banned 状态延后到 v1.1 | 记录到 backlog |

## 技术限制说明
- 当前枚举类已部署到数据库
- 新增状态需 DML 变更 + 历史数据迁移
```

### 决策选项

| 选项 | 说明 | 后续动作 |
|------|------|---------|
| **接受偏差** | 调整 PRD 匹配实现 | 更新 PRD → 重新验证 → ✅ |
| **坚持原需求** | 要求重新实现 | tech-manager 分发任务 → 开发补充 → 验证 |
| **协商调整** | 延后到下一版本 | 记录 backlog → 当前版本标记部分完成 |

### 决策执行流程

```typescript
function handleDeviationBlocking(deviationReport) {
  // 1. 显示偏差详情
  report("发现 {n} 项偏差：{偏差列表}");
  
  // 2. 提供决策选项
  const options = [
    { id: 1, label: "接受偏差", action: "adjustPRD" },
    { id: 2, label: "坚持原需求", action: "reimplement" },
    { id: 3, label: "协商调整", action: "deferToNext" }
  ];
  
  // 3. 询问用户
  const decision = askUser("请选择处理方案", options);
  
  // 4. 执行决策
  switch (decision.action) {
    case "adjustPRD":
      // 调用 product-manager 更新 PRD
      executeSkill("product-manager", {
        task: "偏差决策-接受",
        input: deviationReport,
        action: "更新PRD删除偏差项"
      });
      // 生成决策记录
      createDecisionRecord("接受偏差", deviationReport);
      // 更新 status.md: 验证 → ✅
      break;
      
    case "reimplement":
      // 调用 tech-manager 分发补充任务
      executeSkill("tech-manager", {
        task: "补充开发",
        input: deviationReport.unmatchedItems
      });
      break;
      
    case "deferToNext":
      // 记录到 backlog
      addToBacklog(deviationReport, "v1.1");
      // 当前版本标记部分完成
      updateStatus("部分完成");
      break;
  }
}
```

---

## 决策记录格式

```markdown
# 偏差决策记录

## 基本信息
- 模块: user
- 版本: v1.0
- 决策时间: 2026-04-12 11:00
- 决策人: {用户名或AI会话ID}

## 决策内容
- 决策: 接受偏差
- 原因: banned 状态非 MVP 核心功能，延后风险可控

## 受影响项
- PRD 章节: 用户状态枚举 → 删除 banned
- 验收标准: 删除 banned 状态相关验收条件

## 后续动作
- [x] 更新 PRD v1.0
- [x] 更新 OpenAPI 规格删除 banned
- [x] 验证通过 → user ✅ 已完成

## Backlog 记录
- 延后项: banned 用户状态
- 计划版本: v1.1
- 优先级: P2
```

---

## 前置未完成阻塞

### 依赖关系表

| 任务 | 前置依赖 |
|------|---------|
| 技术分析 | PRD ✅ |
| OpenAPI生成 | 技术分析 ✅ |
| DML生成 | 技术分析 ✅ |
| 后端开发 | OpenAPI ✅ + DML ✅ |
| 前端开发 | OpenAPI ✅ + 线框图 ✅ |
| 实现验证 | 后端开发 ✅ + 前端开发 ✅ |

### 处理逻辑

```typescript
function checkPrecondition(task, status) {
  const preconditions = getPreconditions(task.type);
  
  for (const pre of preconditions) {
    if (!status.isCompleted(pre.module, pre.stage)) {
      // 前置未完成 → 暂停当前任务
      report("{任务} 依赖 {前置任务}，等待前置完成");
      return { blocked: true, reason: "前置未完成" };
    }
  }
  
  return { blocked: false };
}
```

---

## 用户暂停处理

### 暂停指令

| 指令 | 效果 |
|------|------|
| `stop` | 终止循环，保存当前进度 |
| `暂停` | 暂停循环，可恢复 |
| `skip` | 跳过当前任务 |

### 恢复指令

```
/ralph-loop "继续"
```

**恢复逻辑**：

```typescript
function resumeLoop() {
  // 1. 读取 status.md
  const status = readStatusMD();
  
  // 2. 找到暂停位置
  const lastTask = status.lastExecutedTask;
  
  // 3. 检查是否有阻塞项
  if (hasBlocking(status)) {
    // 优先处理阻塞
    handleBlocking(status.blockingItems);
  } else {
    // 继续下一个任务
    executeNextTask(status);
  }
}
```

---

## 循环恢复点保存

每次执行任务后保存恢复点：

```markdown
## 循环恢复点
> 最后更新: 2026-04-12 10:30

| 最后执行任务 | 状态 | 下一步 |
|-------------|------|--------|
| product PRD编写 | ✅ 完成 | tech-manager 技术分析 |

## 循环配置
- autoCommit: true
- confirmEachStep: false
- maxIterations: 100
- currentIteration: 5
```

---

## 多会话冲突处理

### 冲突检测

```typescript
function detectConflict(sessionId, task) {
  // 检查任务是否被其他会话锁定
  const lock = getTaskLock(task);
  
  if (lock && lock.sessionId !== sessionId) {
    report("任务 {task} 正被会话 {lock.sessionId} 处理");
    return { conflict: true, lockedBy: lock.sessionId };
  }
  
  // 获取锁
  acquireTaskLock(task, sessionId);
  return { conflict: false };
}
```

### 冲突解决

| 方案 | 说明 |
|------|------|
| 等待 | 等待其他会话完成后 git pull |
| 协调 | 手动沟通，分配任务顺序 |

