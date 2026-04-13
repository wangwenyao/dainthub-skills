# Playwright E2E 测试流程

**何时使用**: 设计并编写 Playwright E2E 自动化测试，覆盖关键业务流程。

---

## 流程步骤

```
1. 获取输入
   ├── 用户旅程（PRD 章节）
   ├── 页面线框图 YAML
   ├── 关键功能清单（P0 功能）
   └── 测试计划（E2E 覆盖范围）

2. 确定测试场景
   ├── 提取关键用户旅程
   ├── 提取 P0 核心流程
   └── 定义 E2E 测试范围

3. 设计测试脚本结构
   ├── 创建测试文件结构
   ├── 设计 Page Object 模型
   └── 设计测试数据准备

4. 编写测试脚本
   ├── 编写 Page Object
   ├── 编写测试用例
   └── 编写测试数据 fixture

5. 执行测试
   ├── 本地调试执行
   ├── CI/CD 集成
   └── 生成测试报告

6. 输出测试文件
   └── tests/e2e/*.spec.ts
```

---

## 测试目录结构

```
tests/
├── e2e/
│   ├── auth.spec.ts              # 登录/登出测试
│   ├── order.spec.ts             # 订单流程测试
│   ├── product.spec.ts           # 商品管理测试
│   └── pages/                    # Page Object 模型
│   │   ├── login.page.ts
│   │   ├── dashboard.page.ts
│   │   ├── order.page.ts
│   │   └── product.page.ts
│   └── fixtures/                 # 测试数据
│   │   ├── test-data.ts
│   │   └── auth.fixture.ts
│   └── utils/                    # 测试工具
│   │   ├── helpers.ts
│   │   └── assertions.ts
│   └── playwright.config.ts      # Playwright 配置
```

---

## Playwright 配置

### playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results.json' }]
  ],
  
  use: {
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```

---

## Page Object 模型

### Page Object 设计规范

```typescript
// tests/e2e/pages/login.page.ts

import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    // 使用 data-testid 定位元素
    this.usernameInput = page.getByTestId('username-input');
    this.passwordInput = page.getByTestId('password-input');
    this.loginButton = page.getByTestId('login-button');
    this.errorMessage = page.getByTestId('error-message');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async expectError(message: string) {
    await this.errorMessage.waitFor({ state: 'visible' });
    await expect(this.errorMessage).toHaveText(message);
  }
}
```

### Page Object 使用示例

```typescript
// tests/e2e/auth.spec.ts

import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/login.page';
import { DashboardPage } from './pages/dashboard.page';

test.describe('用户登录流程', () => {
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    dashboardPage = new DashboardPage(page);
  });

  test('登录成功 - 正确的用户名和密码', async ({ page }) => {
    // Given: 用户在登录页面
    await loginPage.goto();
    
    // When: 输入正确的用户名和密码并点击登录
    await loginPage.login('admin', 'password123');
    
    // Then: 跳转到首页，显示用户信息
    await expect(page).toHaveURL('/dashboard');
    await expect(dashboardPage.userProfile).toBeVisible();
  });

  test('登录失败 - 错误的密码', async ({ page }) => {
    await loginPage.goto();
    await loginPage.login('admin', 'wrongpassword');
    await loginPage.expectError('用户名或密码错误');
  });
});
```

---

## 测试用例编写规范

### Given/When/Then 结构

```typescript
test('{场景描述}', async ({ page }) => {
  // ── Given: 前置条件 ─────────────────────────
  // 数据准备、页面导航、状态初始化
  
  // ── When: 执行操作 ───────────────────────────
  // 用户交互、点击、输入、导航
  
  // ── Then: 验证结果 ───────────────────────────
  // 断言检查、页面状态验证
});
```

### 测试数据准备

```typescript
// tests/e2e/fixtures/test-data.ts

export const testUsers = {
  admin: {
    username: 'admin',
    password: 'admin123',
    role: 'admin',
  },
  normalUser: {
    username: 'user001',
    password: 'user123',
    role: 'user',
  },
};

export const testProducts = {
  validProduct: {
    name: '测试商品A',
    price: 100,
    stock: 50,
  },
  invalidProduct: {
    name: '',  // 名称为空
    price: -1, // 价格无效
  },
};
```

### Auth Fixture（登录状态持久化）

```typescript
// tests/e2e/fixtures/auth.fixture.ts

import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/login.page';

type AuthFixtures = {
  authenticatedPage: Page;
  adminPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user001', 'user123');
    await use(page);
  },
  
  adminPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('admin', 'admin123');
    await use(page);
  },
});
```

### 使用 Auth Fixture

```typescript
// tests/e2e/order.spec.ts

import { test, expect } from './fixtures/auth.fixture';
import { OrderPage } from './pages/order.page';

test.describe('订单管理（已登录）', () => {
  test('创建订单 - 正常流程', async ({ authenticatedPage }) => {
    const orderPage = new OrderPage(authenticatedPage);
    
    await orderPage.goto();
    await orderPage.createOrder(testProducts.validProduct);
    
    await expect(orderPage.successMessage).toBeVisible();
  });
});
```

---

## 关键流程测试示例

### 用户旅程 → E2E 测试

**PRD 用户旅程**:

```
用户旅程 UJ-001: 商品购买流程
1. 用户登录
2. 搜索商品
3. 添加购物车
4. 确认订单
5. 支付
6. 查看订单状态
```

**E2E 测试转化**:

```typescript
// tests/e2e/purchase-flow.spec.ts

import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/login.page';
import { SearchPage } from './pages/search.page';
import { CartPage } from './pages/cart.page';
import { OrderPage } from './pages/order.page';

test.describe('商品购买完整流程', () => {
  test('UJ-001: 用户购买商品完整旅程', async ({ page }) => {
    // Step 1: 用户登录
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user001', 'user123');
    await expect(page).toHaveURL('/dashboard');
    
    // Step 2: 搜索商品
    const searchPage = new SearchPage(page);
    await searchPage.goto();
    await searchPage.search('测试商品A');
    await expect(searchPage.productList).toHaveCount(1);
    
    // Step 3: 添加购物车
    await searchPage.addToCart(0);
    await expect(searchPage.cartCount).toHaveText('1');
    
    // Step 4: 确认订单
    const cartPage = new CartPage(page);
    await cartPage.goto();
    await cartPage.checkout();
    
    // Step 5: 支付（模拟）
    const orderPage = new OrderPage(page);
    await orderPage.confirmOrder();
    
    // Step 6: 查看订单状态
    await expect(page).toHaveURL(/\/order\/\d+/);
    await expect(orderPage.orderStatus).toHaveText('待支付');
  });
});
```

---

## 断言规范

### 常用断言

```typescript
// 页面导航
await expect(page).toHaveURL('/dashboard');
await expect(page).toHaveURL(/\/order\/\d+/);

// 元素可见性
await expect(locator).toBeVisible();
await expect(locator).toBeHidden();
await expect(locator).toBeEnabled();
await expect(locator).toBeDisabled();

// 文本内容
await expect(locator).toHaveText('登录成功');
await expect(locator).toContainText('欢迎');

// 数值
await expect(locator).toHaveValue('100');
await expect(locator).toHaveCount(5);

// CSS 属性
await expect(locator).toHaveCSS('color', 'rgb(255, 0, 0)');

// 表格/列表
await expect(locator).toHaveText(['A', 'B', 'C']);
```

### 自定义断言

```typescript
// tests/e2e/utils/assertions.ts

import { expect, Locator } from '@playwright/test';

export async function expectTableData(
  table: Locator, 
  expectedData: Record<string, string>[]
) {
  const rows = table.getByRole('row');
  await expect(rows).toHaveCount(expectedData.length);
  
  for (let i = 0; i < expectedData.length; i++) {
    const row = rows.nth(i);
    for (const [key, value] of Object.entries(expectedData[i])) {
      await expect(row.getByTestId(key)).toHaveText(value);
    }
  }
}
```

---

## 测试执行命令

```bash
# 执行所有 E2E 测试
npx playwright test

# 执行指定文件
npx playwright test tests/e2e/auth.spec.ts

# 执行指定浏览器
npx playwright test --project=chromium

# 调试模式
npx playwright test --debug

# 生成报告
npx playwright show-report

# UI 模式
npx playwright test --ui
```

---

## CI/CD 集成

### GitHub Actions

```yaml
# .github/workflows/e2e-test.yml

name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Install Playwright browsers
        run: npx playwright install --with-deps
        
      - name: Run E2E tests
        run: npx playwright test
        
      - name: Upload test report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

---

## 测试覆盖率统计

### E2E 覆盖率目标

| 功能优先级 | E2E 覆盖率 | 测试类型 |
|-----------|-----------|---------|
| **P0** | 100% | 完整用户旅程 |
| **P1** | ≥ 80% | 关键操作路径 |
| **P2** | ≥ 50% | 核心交互 |

### 覆盖率报告

```bash
# 生成覆盖率报告
npx playwright test --reporter=json

# 解析报告统计
node scripts/parse-coverage.js test-results.json
```

---

## 常见问题处理

### 等待策略

```typescript
// 等待元素出现
await locator.waitFor({ state: 'visible' });

// 等待元素消失
await locator.waitFor({ state: 'hidden' });

// 等待网络请求完成
await page.waitForResponse(resp => 
  resp.url().includes('/api/login') && resp.status() === 200
);

// 等待加载状态
await page.waitForLoadState('networkidle');
```

### 元素定位最佳实践

```typescript
// ✅ 推荐: 使用 data-testid
page.getByTestId('login-button')

// ✅ 推荐: 使用语义化选择器
page.getByRole('button', { name: '登录' })
page.getByLabel('用户名')
page.getByPlaceholder('请输入用户名')

// ❌ 避免: 使用 CSS 选择器（不稳定）
page.locator('.btn-primary')
page.locator('#login-btn')

// ❌ 避免: 使用 XPath
page.locator('//button[@class="btn"]')
```

---

## 与 PRD 协作

| PRD 章节 | E2E 测试输入 | 测试输出 |
|---------|-------------|---------|
| 用户旅程 | 流程步骤 → 测试场景 | tests/e2e/*.spec.ts |
| 验收标准 | Given/When/Then → 测试结构 | 断言验证 |
| 线框图 YAML | 页面路由 + 组件结构 | Page Object 设计 |

### YAML 页面规格 → Page Object

```yaml
# PRD YAML 输出
pages:
  - type: list
    route: /product/list
    config:
      table:
        data-testid: product-table
      search:
        data-testid: product-search
      addButton:
        data-testid: add-product-btn
```

```typescript
// Page Object 对应
export class ProductListPage {
  readonly productTable = page.getByTestId('product-table');
  readonly searchInput = page.getByTestId('product-search');
  readonly addButton = page.getByTestId('add-product-btn');
}
```