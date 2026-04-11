# 测试协作框架

开发 skill 与全局测试 skill（`test-driven-development`、`test-generation`）的协作规范。

---

## 开发阶段 → 测试能力映射

| 开发阶段 | 调用全局 Skill | 目的 |
|---------|---------------|------|
| **实现前** | `test-driven-development` | 先写测试，定义行为预期 |
| **实现中** | 遵循本 skill 的测试规范文档 | 遵循命名/结构/Mock 规范 |
| **实现后** | `test-generation` | 覆盖分析，补充边缘情况 |

### 开发流程集成

```
Step 1: 影响分析 → 确定哪些代码需要测试
Step 2: TDD 先写测试 → 调用 test-driven-development skill
Step 3: 实现代码 → 读取本 skill 的代码模板
Step 4: 补充测试 → 读取本 skill 的测试规范 + test-generation
Step 5: 覆盖分析 → 调用 test-generation 检查覆盖率
```

---

## PRD 验收标准 → 测试用例

PRD 的验收标准（Given/When/Then）可直接转化为测试代码：

```
PRD验收标准：
Given [前置条件]
When [操作]
Then [结果]

转化模板：
Test: [场景描述]
// Arrange (Given)
...
// Act (When)
...
// Assert (Then)
...
```

### Java 后端转化示例

```
PRD：Given 用户已登录，购物车有商品 When 点击结算 Then 进入结算页面

→ 单元测试（参考 java-backend-dev/references/test-standards.md）：
@Test
void checkout_withItems_success() {
    // Arrange (Given)
    ...
    // Act (When)
    ...
    // Assert (Then)
    ...
}
```

### 前端 E2E 转化示例

```
PRD：Given 用户在商品列表页 When 点击新增 Then 打开新增表单弹窗

→ Playwright 测试（参考 vben-frontend-dev/references/05-page-patterns.md）：
test('新增商品流程', async ({ page }) => {
    // Given
    await page.goto('/product/list');
    // When
    await page.click('[data-testid="add-btn"]');
    // Then
    await expect(page.locator('.vben-modal')).toBeVisible();
});
```

---

## 各 Skill 测试规范索引

| Skill | 测试规范文档 | 覆盖率标准 |
|-------|------------|-----------|
| java-backend-dev | `references/test-standards.md` | Service ≥ 80% |
| vben-frontend-dev | `references/05-page-patterns.md` | 业务组件 ≥ 70%，Composables ≥ 80% |

---

## 版本

- v1.0
- 更新: 2026-04-11
