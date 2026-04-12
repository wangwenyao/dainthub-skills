# Skill 路由规则

/ralph-loop 自动识别任务类型并路由到对应 skill 的规则。

---

## 路由映射表

| 任务类型 | 目标 Skill | 输入 | 输出 |
|---------|-----------|------|------|
| PRD编写 | `product-manager` | 需求描述 | PRD + 线框图 + YAML规格 |
| 需求评审 | `product-manager` | PRD 文件 | 评审报告 |
| 偏差决策 | `product-manager` | 偏差报告 | 决策记录 + 更新PRD |
| 技术分析 | `tech-manager` | PRD 文件 | 影响分析报告 |
| OpenAPI生成 | `tech-manager` | PRD + ER图 | openapi-*.yaml |
| DML生成 | `tech-manager` | PRD + ER图 | dml-*.sql + rollback |
| 任务分发 | `tech-manager` | OpenAPI + DML | 启动开发 subagent |
| 实现验证 | `tech-manager` | PRD + 代码 | 验证报告 |
| 偏差反馈 | `tech-manager` | 验证报告(不通过项) | 偏差报告 |
| 后端开发 | `java-backend-dev` | OpenAPI + DML | Controller/Service/Mapper |
| 前端开发 | `vben-frontend-dev` | OpenAPI + YAML规格 | Vue 页面组件 |
| git同步 | `team-collaboration` | - | status.md 更新 |

---

## 任务类型识别规则

从 status.md 的"待处理项汇总"表识别：

```markdown
## 待处理项汇总
| 类型 | 模块 | 任务 | 处理角色 |
|------|------|------|---------|
| PRD编写 | product | 编写商品管理PRD | product-manager |
```

**识别逻辑**：

```typescript
function identifyTaskType(statusRow) {
  // 优先匹配"类型"列
  const typeMap = {
    "PRD编写": "PRD编写",
    "技术分析": "技术分析",
    "OpenAPI生成": "OpenAPI生成",
    "DML生成": "DML生成",
    "后端开发": "后端开发",
    "前端开发": "前端开发",
    "实现验证": "实现验证",
    "偏差反馈": "偏差反馈",
    "偏差决策": "偏差决策"
  };
  
  if (typeMap[statusRow.type]) {
    return typeMap[statusRow.type];
  }
  
  // 从"处理角色"推断
  const roleMap = {
    "product-manager": "PRD编写",
    "tech-manager": "技术分析",
    "java-backend-dev": "后端开发",
    "vben-frontend-dev": "前端开发"
  };
  
  return roleMap[statusRow.role] || "未知";
}
```

---

## 任务优先级排序

**排序规则**：

```
优先级权重 = 模块优先级(P0=3, P1=2, P2=1) × 任务阶段权重
```

**任务阶段权重**：

| 阶段 | 权重 | 说明 |
|------|------|------|
| PRD编写 | 10 | 最高，必须先完成 |
| 技术分析 | 8 | 依赖 PRD |
| OpenAPI/DML | 7 | 依赖分析 |
| 开发 | 5 | 可并行 |
| 验证 | 3 | 依赖开发 |
| 偏差处理 | 2 | 阻塞项 |

**示例**：

```
product(P0) PRD编写 → 权重 = 3 × 10 = 30 → 最高优先
trade(P0) 开发 → 权重 = 3 × 5 = 15
user(P1) PRD编写 → 权重 = 2 × 10 = 20
```

---

## 并行任务识别

以下任务可并行执行：

| 任务组合 | 条件 |
|---------|------|
| 后端开发 + 前端开发 | 同一模块，OpenAPI + DML 已完成 |
| 多模块 PRD编写 | 无依赖关系 |

**并行执行逻辑**：

```typescript
function findParallelTasks(status) {
  const tasks = status.pendingItems;
  
  // 找可并行的开发任务
  const devTasks = tasks.filter(t => 
    t.type === "后端开发" || t.type === "前端开发"
  );
  
  // 按模块分组
  const byModule = groupBy(devTasks, "module");
  
  // 同一模块的开发任务并行
  return byModule.map(moduleTasks => ({
    parallel: true,
    tasks: moduleTasks
  }));
}
```

---

## 循环终止检测

**终止条件**：

| 条件 | 检测方法 |
|------|---------|
| 全部完成 | status.md 所有模块 `✅ 已完成` |
| 无待处理项 | "待处理项汇总"表为空 |
| 全部阻塞 | 所有待处理项类型为"偏差决策"且无决策 |
| 达到上限 | 循环次数 > maxIterations |

