# 状态更新模板

各 skill 完成任务后输出给 /ralph-loop 的状态更新指令模板。

---

## 模板格式

每个 skill 完成后输出：

```markdown
## 状态更新指令

### 模块状态更新
- 模块: {模块名}
- 字段变更: {字段列表}
- 当前阶段: {新阶段}

### 待处理项更新
- 完成: {当前任务}
- 新增: {后续任务列表}

### 下一步任务
- 角色: {处理角色}
- 任务: {任务描述}
- 输入: {输入文件}
```

---

## product-manager 完成模板

### PRD编写完成

```markdown
## 状态更新指令

### 模块状态更新
- 模块: product
- PRD: v1.0 ✅
- 线框图: v1.0 ✅
- 当前阶段: 🚧 待技术分析

### 待处理项更新
- 完成: PRD编写 (product)
- 新增: 
  - 技术分析 (product) → tech-manager
  - OpenAPI生成 (product) → tech-manager
  - DML生成 (product) → tech-manager

### 下一步任务
- 角色: tech-manager
- 任务: 分析 product PRD + 生成 OpenAPI + DML
- 输入: docs/prd/prd-product-v1.0.md

### 输出文件
- docs/prd/prd-product-v1.0.md
- docs/wireframes/wireframes-product-v1.0.html
- docs/wireframes/pages-product-v1.0.yaml
```

### 偏差决策完成

```markdown
## 状态更新指令

### 模块状态更新
- 模块: user
- 偏差: v1.0 ✅ (已处理)
- 决策: v1.0 ✅
- 验证: v1.0 → 待重新验证
- 当前阶段: 🚧 重新验证

### 待处理项更新
- 完成: 偏差决策 (user)
- 新增: 
  - 重新验证 (user) → tech-manager

### 下一步任务
- 角色: tech-manager
- 任务: 重新验证 user 实现
- 输入: docs/prd/prd-user-v1.0.md (已更新)

### 输出文件
- docs/decisions/decision-user-v1.0.md
- docs/prd/prd-user-v1.0.md (更新版)
```

---

## tech-manager 完成模板

### 技术分析完成

```markdown
## 状态更新指令

### 模块状态更新
- 模块: product
- 当前阶段: 🚧 待规格生成

### 待处理项更新
- 完成: 技术分析 (product)
- 新增: 
  - OpenAPI生成 (product) → tech-manager
  - DML生成 (product) → tech-manager

### 下一步任务
- 角色: tech-manager
- 任务: 生成 product OpenAPI + DML
- 输入: docs/reports/impact-product-v1.0.md

### 输出文件
- docs/reports/impact-product-v1.0.md
```

### OpenAPI + DML 生成完成

```markdown
## 状态更新指令

### 模块状态更新
- 模块: product
- OpenAPI: v1.0 ✅
- DML: v1.0 ✅
- 当前阶段: 🚧 待开发

### 待处理项更新
- 完成: OpenAPI生成 + DML生成 (product)
- 新增: 
  - 后端开发 (product) → java-backend-dev
  - 前端开发 (product) → vben-frontend-dev

### 下一步任务
- 角色: java-backend-dev + vben-frontend-dev (并行)
- 任务: 开发 product 模块
- 输入: 
  - 后端: docs/api/openapi-product-v1.0.yaml + docs/db/dml-product-v1.0.sql
  - 前端: docs/api/openapi-product-v1.0.yaml + docs/wireframes/pages-product-v1.0.yaml

### 输出文件
- docs/api/openapi-product-v1.0.yaml
- docs/db/dml-product-v1.0.sql
- docs/db/dml-product-v1.0-rollback.sql
- docs/db/dml-product-checklist-v1.0.md
```

### 实现验证完成（通过）

```markdown
## 状态更新指令

### 模块状态更新
- 模块: product
- 验证: v1.0 ✅
- 当前阶段: ✅ 已完成

### 待处理项更新
- 完成: 实现验证 (product)
- 新增: 无

### 下一步任务
- 模块 product 已完成
- 检查是否有其他待处理模块

### 输出文件
- docs/reports/verify-product-v1.0.md
```

### 实现验证完成（不通过）

```markdown
## 状态更新指令

### 模块状态更新
- 模块: user
- 验证: v1.0 ❌
- 偏差: v1.0 🚧
- 当前阶段: 🚧 偏差待处理

### 待处理项更新
- 完成: 实现验证 (user) - 发现偏差
- 新增: 
  - 偏差决策 (user) → product-manager

### 下一步任务
- 角色: product-manager
- 任务: 处理 user 偏差决策
- 输入: docs/reports/deviation-user-v1.0.md

### 阻塞标记
- **阻塞**: 偏差决策未完成，循环暂停
- 阻塞原因: 实现验证 ❌

### 输出文件
- docs/reports/verify-user-v1.0.md
- docs/reports/deviation-user-v1.0.md
```

---

## java-backend-dev 完成模板

```markdown
## 状态更新指令

### 模块状态更新
- 模块: product
- 后端开发: ✅ 完成
- 当前阶段: 🚧 待前端完成 + 验证

### 待处理项更新
- 完成: 后端开发 (product)
- 状态: 等待前端开发完成

### 下一步任务
- 检查前端开发状态
- 如前端已完成 → tech-manager 验证
- 如前端未完成 → 等待

### 输出文件
- src/main/java/.../product/controller/ProductController.java
- src/main/java/.../product/service/ProductService.java
- src/main/java/.../product/dal/ProductMapper.java
- src/main/java/.../product/dal/ProductDO.java
- src/test/java/.../product/service/ProductServiceTest.java
```

---

## vben-frontend-dev 完成模板

```markdown
## 状态更新指令

### 模块状态更新
- 模块: product
- 前端开发: ✅ 完成
- 当前阶段: 🚧 待后端完成 + 验证

### 待处理项更新
- 完成: 前端开发 (product)
- 状态: 等待后端开发完成

### 下一步任务
- 检查后端开发状态
- 如后端已完成 → tech-manager 验证
- 如后端未完成 → 等待

### 输出文件
- apps/web-antd/src/views/product/index.vue
- apps/web-antd/src/views/product/data.ts
- apps/web-antd/src/views/product/modules/form.vue
- apps/web-antd/src/api/product/product.ts
```

---

## 状态合并逻辑

当后端和前端都完成后：

```typescript
function mergeDevStatus(backendStatus, frontendStatus) {
  if (backendStatus.completed && frontendStatus.completed) {
    return {
      module: backendStatus.module,
      backend: "✅",
      frontend: "✅",
      currentStage: "🚧 待验证",
      newPendingItem: {
        type: "实现验证",
        role: "tech-manager"
      }
    };
  }
}
```

---

## 循环控制器处理逻辑

```typescript
function processStatusUpdate(skillOutput) {
  // 1. 解析状态更新指令
  const update = parseStatusUpdate(skillOutput);
  
  // 2. 更新 status.md
  updateStatusMD(update);
  
  // 3. 检查是否阻塞
  if (update.blocking) {
    pauseLoop();
    handleBlocking(update);
  } else {
    // 4. 找下一个任务
    const nextTask = findNextTask(status);
    
    // 5. 继续循环
    executeNext(nextTask);
  }
}
```

---

## 版本

- v1.0
- 更新: 2026-04-12
- 变更: 新增状态更新模板