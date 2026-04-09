# Testing Reference — Vue SaaS Frontend

## 目录

1. [单元测试（Vitest + Vue Test Utils）](#单元测试)
2. [E2E 测试（Playwright）](#e2e-测试)
3. [测试工具函数](#测试工具函数)

---

## 单元测试

### 组件测试模板

```typescript
// components/__tests__/UserCard.spec.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import UserCard from '../UserCard.vue'

const mockUser = {
  id: '1',
  name: '张三',
  email: 'zhangsan@example.com',
  role: 'admin' as const,
}

describe('UserCard', () => {
  it('renders user name and email', () => {
    const wrapper = mount(UserCard, {
      props: { user: mockUser },
      global: {
        plugins: [createTestingPinia()],
      },
    })
    expect(wrapper.text()).toContain('张三')
    expect(wrapper.text()).toContain('zhangsan@example.com')
  })

  it('shows admin badge for admin users', () => {
    const wrapper = mount(UserCard, { props: { user: mockUser } })
    expect(wrapper.find('[data-testid="role-badge"]').text()).toBe('管理员')
  })

  it('emits delete event when delete button clicked', async () => {
    const wrapper = mount(UserCard, { props: { user: mockUser } })
    await wrapper.find('[data-testid="delete-btn"]').trigger('click')
    expect(wrapper.emitted('delete')).toBeTruthy()
    expect(wrapper.emitted('delete')![0]).toEqual([mockUser.id])
  })
})
```

### Composable 测试

```typescript
// composables/__tests__/useUsers.spec.ts
import { describe, it, expect, vi } from 'vitest'
import { flushPromises } from '@vue/test-utils'
import { useUserList } from '../useUsers'
import { userService } from '@/services/userService'

vi.mock('@/services/userService')

describe('useUserList', () => {
  it('fetches and returns user list', async () => {
    vi.mocked(userService.getList).mockResolvedValue({
      items: [{ id: '1', name: '张三', email: 'a@b.com', role: 'member' }],
      total: 1,
    })

    const filters = ref({ page: 1, pageSize: 20 })
    const { data, isLoading } = useUserList(filters)

    expect(isLoading.value).toBe(true)
    await flushPromises()
    expect(data.value?.items).toHaveLength(1)
    expect(isLoading.value).toBe(false)
  })
})
```

### Store 测试

```typescript
// stores/__tests__/useUserStore.spec.ts
import { setActivePinia, createPinia } from 'pinia'
import { useUserStore } from '../useUserStore'

describe('useUserStore', () => {
  beforeEach(() => setActivePinia(createPinia()))

  it('isAuthenticated returns false initially', () => {
    const store = useUserStore()
    expect(store.isAuthenticated).toBe(false)
  })

  it('logout clears user', () => {
    const store = useUserStore()
    store.currentUser = { id: '1', name: 'Test', email: 'a@b.com', role: 'member' }
    store.logout()
    expect(store.currentUser).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })
})
```

---

## E2E 测试

### 登录流程测试

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('user can login with valid credentials', async ({ page }) => {
    await page.goto('/auth/login')
    
    await page.getByLabel('邮箱').fill('admin@example.com')
    await page.getByLabel('密码').fill('password123')
    await page.getByRole('button', { name: '登录' }).click()
    
    await expect(page).toHaveURL('/dashboard')
    await expect(page.getByText('仪表盘')).toBeVisible()
  })

  test('shows error for invalid credentials', async ({ page }) => {
    await page.goto('/auth/login')
    
    await page.getByLabel('邮箱').fill('wrong@example.com')
    await page.getByLabel('密码').fill('wrongpassword')
    await page.getByRole('button', { name: '登录' }).click()
    
    await expect(page.getByText(/登录失败/)).toBeVisible()
  })
})
```

### 用户管理 E2E

```typescript
// e2e/users.spec.ts
import { test, expect } from '@playwright/test'

test.describe('User Management', () => {
  test.beforeEach(async ({ page }) => {
    // 使用 API 直接登录，跳过 UI 流程
    await page.request.post('/api/auth/login', {
      data: { email: 'admin@example.com', password: 'password123' }
    })
    await page.goto('/users')
  })

  test('can search users', async ({ page }) => {
    await page.getByPlaceholder('搜索姓名或邮箱').fill('张三')
    await expect(page.getByRole('row', { name: /张三/ })).toBeVisible()
  })

  test('can delete a user', async ({ page }) => {
    await page.getByRole('row').first().getByRole('button', { name: '操作' }).click()
    await page.getByRole('menuitem', { name: '删除' }).click()
    
    // 确认对话框
    await expect(page.getByRole('alertdialog')).toBeVisible()
    await page.getByRole('button', { name: '确认删除' }).click()
    
    await expect(page.getByText('删除成功')).toBeVisible()
  })
})
```

### Playwright 配置

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 14'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
})
```

---

## 测试工具函数

```typescript
// test/utils.ts — 测试辅助函数
import { mount, type MountingOptions } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { VueQueryPlugin } from '@tanstack/vue-query'
import { createRouter, createMemoryHistory } from 'vue-router'
import { routes } from '@/router'

/**
 * 统一的组件挂载函数，预置所有必要插件
 */
export function mountWithPlugins<T>(
  Component: T,
  options: MountingOptions<any> = {}
) {
  const router = createRouter({ history: createMemoryHistory(), routes })
  
  return mount(Component, {
    ...options,
    global: {
      plugins: [
        createTestingPinia({ createSpy: vi.fn }),
        VueQueryPlugin,
        router,
      ],
      ...options.global,
    },
  })
}
```
