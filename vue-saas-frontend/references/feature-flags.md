# 功能开关规范

## 一、功能开关定义

```typescript
interface FeatureFlag {
  key: string                    // 唯一标识
  name: string                   // 显示名称
  description: string            // 功能描述
  enabled: boolean | {           // 静态开关 或 动态规则
    percentage?: number          // 灰度比例 (0-100)
    users?: string[]             // 白名单用户ID
    roles?: string[]             // 角色限制
    regions?: string[]           // 地区限制
    dateRange?: [string, string] // 时间范围
  }
}

const FLAGS: FeatureFlag[] = [
  { key: 'new-dashboard', name: '新版仪表盘', description: '重构后的仪表盘', enabled: { percentage: 20 } },
  { key: 'dark-mode', name: '暗色模式', description: '深色主题', enabled: true },
  { key: 'export-pdf', name: 'PDF 导出', description: '报表导出', enabled: { roles: ['admin'] } },
]
```

## 二、开关评估逻辑

```typescript
// composables/useFeatureFlag.ts
function hashUserId(userId: string): number {
  let hash = 0
  for (let i = 0; i < userId.length; i++) {
    hash = ((hash << 5) - hash) + userId.charCodeAt(i)
    hash = hash & hash
  }
  return Math.abs(hash)
}

export function useFeatureFlag(key: string): ComputedRef<boolean> {
  const userStore = useUserStore()
  const config = useConfig()

  return computed(() => {
    const flag = config.features.find(f => f.key === key)
    if (!flag) return false
    if (typeof flag.enabled === 'boolean') return flag.enabled

    const rules = flag.enabled
    if (rules.users?.includes(userStore.userId)) return true
    if (rules.roles && !rules.roles.includes(userStore.role)) return false
    if (rules.regions && !rules.regions.includes(userStore.region)) return false

    if (rules.dateRange) {
      const [start, end] = rules.dateRange
      const now = new Date()
      if (now < new Date(start) || now > new Date(end)) return false
    }

    if (rules.percentage !== undefined) {
      return (hashUserId(userStore.userId) % 100) < rules.percentage
    }
    return true
  })
}
```

## 三、A/B 测试支持

```typescript
interface ABTest {
  key: string
  variants: Record<string, { weight: number }>
}

export function useABTest(key: string) {
  const userStore = useUserStore()
  const variantKey = `ab_${key}_${userStore.userId}`

  const cached = sessionStorage.getItem(variantKey)
  if (cached) return { variant: cached }

  const test = config.abTests.find(t => t.key === key)
  if (!test) return { variant: 'control' }

  const totalWeight = Object.values(test.variants).reduce((s, v) => s + v.weight, 0)
  const random = Math.random() * totalWeight

  let cumulative = 0
  for (const [name, variant] of Object.entries(test.variants)) {
    cumulative += variant.weight
    if (random < cumulative) {
      sessionStorage.setItem(variantKey, name)
      return { variant: name }
    }
  }
  return { variant: 'control' }
}
```

## 四、灰度发布策略

| 策略 | 适用场景 | 配置方式 |
|------|----------|----------|
| 按用户比例 | 全量灰度 | `percentage: 10` |
| 按用户ID | 内测/VIP | `users: ['id1']` |
| 按角色 | 权限功能 | `roles: ['admin']` |
| 按地区 | 区域功能 | `regions: ['cn']` |
| 按时间 | 限时活动 | `dateRange: [...]` |

**优先级**: 白名单 > 角色 > 地区 > 时间 > 灰度比例

## 五、Vue 集成模式

```vue
<script setup>
const isNewDashboardEnabled = useFeatureFlag('new-dashboard')
const { variant } = useABTest('checkout-flow')
</script>

<template>
  <NewDashboard v-if="isNewDashboardEnabled" />
  <OldDashboard v-else />
  <CheckoutV1 v-if="variant === 'control'" />
  <CheckoutV2 v-else-if="variant === 'variantA'" />
</template>
```

### 自定义指令

```typescript
export const vFeature = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const isEnabled = useFeatureFlag(binding.value)
    if (!isEnabled.value) el.style.display = 'none'
  }
}
// 使用: <div v-feature="'dark-mode'">内容</div>
```

### 组合式封装

```typescript
export function useFeature(key: string) {
  const isEnabled = useFeatureFlag(key)
  const abTest = useABTest(key)
  return {
    isEnabled,
    variant: abTest.variant,
    whenEnabled: (cb: () => void) => { if (isEnabled.value) cb() }
  }
}
```

## 六、开关管理

### 远程配置同步

```typescript
export function useFeatureConfig() {
  const features = ref<FeatureFlag[]>([])

  async function sync() {
    const res = await fetch('/api/features/config')
    features.value = await res.json()
    localStorage.setItem('features_cache', JSON.stringify(features.value))
  }

  setInterval(sync, 5 * 60 * 1000) // 每5分钟同步
  return { features, sync }
}
```

### 缓存策略

- **localStorage**: 完整配置，离线可用
- **sessionStorage**: A/B 测试结果
- **内存缓存**: 运行时配置

### 变更通知

```typescript
const ws = new WebSocket('/ws/features')
ws.onmessage = (event) => {
  const { key, enabled } = JSON.parse(event.data)
  updateFeature(key, enabled)
}
```

### 审计日志

```typescript
interface FeatureAuditLog {
  timestamp: string
  action: 'enable' | 'disable' | 'update'
  key: string
  operator: string
  previousValue: any
  newValue: any
  reason: string
}
```

## 七、最佳实践

### 命名规范

- kebab-case: `new-dashboard`, `export-pdf`
- 前缀: `exp-` 实验, `beta-` 测试, `feat-` 功能

### 生命周期

```
创建 → 测试 → 灰度 → 全量 → 废弃 → 清理
```

### 清理过期开关

```typescript
const DEPRECATED_FLAGS = ['old-feature-v1', 'legacy-export']
function cleanupDeprecatedFlags() {
  DEPRECATED_FLAGS.forEach(key => {
    if (isFeatureFullyRolledOut(key)) removeFeatureFlag(key)
  })
}
```

## 八、禁止事项

| 禁止行为 | 原因 | 替代方案 |
|----------|------|----------|
| 计算属性中修改状态 | 无限循环 | watch/事件 |
| 硬编码开关值 | 无法动态调整 | 配置中心 |
| 开关嵌套过深 | 难维护 | 扁平化设计 |
| 忽略默认值 | 行为不确定 | 提供默认值 |
| SSR用客户端存储 | 水合不匹配 | 请求上下文 |
| 开关长期不清理 | 代码膨胀 | 定期清理 |
| 敏感信息入配置 | 安全风险 | 服务端判断 |