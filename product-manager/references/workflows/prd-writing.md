# PRD编写流程

**何时使用**: 编写产品需求文档、功能规格说明书时

---

## 流程步骤

```
1. 编写核心章节
   ├── 执行摘要 → 产品愿景、核心价值、目标用户
   ├── 成功标准 → 可量化指标、验收标准、时间节点
   ├── 产品范围 → In Scope / Out of Scope / MVP定义
   └── 详细模板 → @../prd-writing-guide.md#PRD模板

2. 编写用户画像
   ├── 主要用户画像 → 角色特征、使用场景、核心诉求
   ├── 用户角色权限 → 各角色的操作权限矩阵
   └── 详细规范 → @../prd-writing-guide.md#用户画像

3. 编写功能架构
   ├── 功能清单 → 功能ID、名称、优先级、模块、用户角色
   ├── 功能菜单层级结构 → 树形结构
   ├── 功能详细描述 → P0/P1功能需展开（前置条件、权限、字段约束、业务规则、异常处理）
   └── 详细规范 → @../prd-writing-guide.md#功能架构规范

4. 绘制核心业务流程
   ├── 使用 Mermaid 语法输出
   ├── 只画 2-5 个关键业务流程（而非"全局流程"）
   ├── 状态流转图（如有需要）
   └── 详细规范 → @../prd-writing-guide.md#流程图规范

5. 编写用户旅程
   ├── 核心用户流程 → 用户完成目标的步骤
   ├── 用户故事 → 作为[角色]，我想要[目标]，以便于[价值]
   ├── 异常流程 → 边界场景处理
   └── 详细规范 → @../prd-writing-guide.md#用户旅程

6. 设计业务实体模型
   ├── 实体定义 → 识别核心业务实体
   ├── 实体属性 → 字段定义
   ├── 实体关系 → ER图（Mermaid erDiagram）
   └── 详细规范 → @../prd-writing-guide.md#业务实体模型规范

7. 编写非功能需求（直接引用基准值，按需调整）
   ├── 性能 → 响应时间、并发、分页上限
   ├── 安全 → 认证、权限、数据隔离、审计
   ├── 可用性 → SLA、备份、浏览器兼容
   └── 基准值参考 → @../prd-writing-guide.md#非功能需求量化规范

8. 质量检查
   └── 使用检查清单 → @../review-checklist.md
```

---

## PRD章节清单

```
必需章节（P0）：
1. 执行摘要
2. 成功标准
3. 产品范围
4. 用户画像
5. 功能架构（含功能详细描述）
6. 核心业务流程（2-5个关键流程，Mermaid）
7. 用户旅程
8. 业务实体模型（ER图，Mermaid）
9. 非功能需求（性能/安全/可用性）

重要章节（P1）：
10. 风险与依赖
11. 页面原型（HTML）
12. 时间规划
```

---

## 用户故事格式

```
标准格式：
作为 [用户角色]
我想要 [完成目标]
以便于 [获得价值]

验收标准格式：
Given [前置条件]
When [用户操作]
Then [预期结果]
```

---

## 验收标准与测试协作

PRD 的验收标准可直接转化为测试代码，供开发阶段使用 `test-driven-development` 和 `test-generation` skill。

### 转化映射

| PRD验收标准 | 测试代码结构 | 测试类型 |
|------------|-------------|---------|
| Given [前置条件] | `// Arrange` 准备测试数据 | 单元/集成测试 |
| When [用户操作] | `// Act` 执行被测方法 | 单元/集成测试 |
| Then [预期结果] | `// Assert` 断言结果 | 单元/集成测试 |
| 用户旅程步骤 | E2E 测试场景 | Playwright/Vitest E2E |
| 业务规则(BR编号) | 业务逻辑测试 | Service层单元测试 |
| 字段约束 | 参数校验测试 | Controller/Form测试 |

### 示例转化

**PRD验收标准**：
```
Given 用户已登录，购物车有商品
When 点击结算按钮
Then 进入结算页面，显示商品清单
```

**转化为后端单元测试**（供 java-backend-dev-skill 使用）：
```java
@Test
@DisplayName("结算流程 - 购物车有商品时可结算")
void checkout_withItemsInCart_success() {
    // ── Arrange (Given) ────────────────────────────────
    Long userId = 1L;
    CartItem item = TestDataFactory.createCartItem("商品A", 2);
    when(cartMapper.selectByUserId(userId)).thenReturn(List.of(item));

    // ── Act (When) ──────────────────────────────────
    CheckoutResult result = checkoutService.checkout(userId);

    // ── Assert (Then) ───────────────────────────────
    assertThat(result.isSuccess()).isTrue();
    assertThat(result.getItems()).hasSize(1);
}
```

**转化为前端E2E测试**（供 vue-saas-frontend/vben-saas-frontend 使用）：
```typescript
test('结算流程：购物车有商品时点击结算', async ({ page }) => {
    // Given
    await page.goto('/login');
    await loginWithUser(page, 'user@example.com');
    await addToCart(page, 'product-123');

    // When
    await page.click('[data-testid="checkout-btn"]');

    // Then
    await expect(page).toHaveURL('/checkout');
    await expect(page.locator('.item-list')).toBeVisible();
});
```

### 开发阶段使用

验收标准编写完成后，告知开发者：
- 使用 `test-driven-development` skill 按验收标准先写测试
- 使用 `test-generation` skill 补充边缘情况和覆盖分析