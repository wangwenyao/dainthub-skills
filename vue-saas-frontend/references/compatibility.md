# 兼容性与迁移规范

> Vue SaaS 前端浏览器兼容性、版本管理与升级迁移指南

---

## 一、浏览器兼容性

### 1.1 目标浏览器矩阵

| 浏览器 | 最低版本 | 市场份额 | 状态 |
|--------|----------|----------|------|
| Chrome | 90+ | 65% | 完全支持 |
| Safari | 14+ | 20% | 完全支持 |
| Firefox | 90+ | 8% | 完全支持 |
| Edge | 90+ | 5% | 完全支持（Chromium） |
| IE | - | - | 不支持 |

**版本选择依据：** Chrome 90+ 支持 `oklch`、Container Queries、CSS Nesting

### 1.2 Browserslist 配置

```json
// package.json
{
  "browserslist": {
    "production": ["chrome >= 90", "safari >= 14", "firefox >= 90", "edge >= 90"],
    "development": ["last 1 chrome version", "last 1 firefox version"]
  }
}
```

### 1.3 Polyfill 策略

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    target: 'es2020',
    polyfillModulePreload: true,
    rollupOptions: {
      output: { manualChunks: { polyfills: ['core-js/stable'] } }
    }
  }
})
```

Vue 3 已内置：Proxy 响应式、Composition API、Teleport、Fragment

| 特性 | Chrome 90+ | Safari 14+ | Firefox 90+ |
|------|------------|------------|-------------|
| Optional Chaining | ✅ | ✅ | ✅ |
| Nullish Coalescing | ✅ | ✅ | ✅ |
| Promise.allSettled | ✅ | ✅ | ✅ |
| globalThis | ✅ | ✅ | ✅ |

### 1.4 CSS 兼容性处理

```javascript
// postcss.config.js
module.exports = {
  plugins: [
    require('@csstools/postcss-oklab-function'),
    require('postcss-container-queries'),
    require('postcss-nesting'),
    require('autoprefixer')({ grid: true })
  ]
}
```

```css
/* oklch 自动降级 */
:root {
  --primary: rgb(100, 180, 220);
  --primary: oklch(0.7 0.15 200);
}
```

### 1.5 渐进增强策略

```typescript
// 特性检测
export const featureDetection = {
  hasContainerQueries: () => CSS.supports('container-type', 'inline-size'),
  hasOkLch: () => CSS.supports('color', 'oklch(0 0 0)'),
  hasNesting: () => { try { return CSS.supports('selector(&') } catch { return false } }
}
```

```css
/* @supports 增强 */
.grid-layout { display: flex; flex-wrap: wrap; }
@supports (display: grid) {
  .grid-layout { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
}
```

---

## 二、版本管理

### 2.1 语义化版本

- **Major**: 不兼容 API 变更，需全面评估
- **Minor**: 向后兼容的功能新增，可安全升级
- **Patch**: Bug 修复，推荐及时更新

### 2.2 依赖版本锁定

```json
{
  "dependencies": {
    "vue": "^3.5.0",        // 允许 minor 更新
    "vue-router": "~4.3.0", // 仅允许 patch 更新
    "pinia": "2.1.7"        // 锁定版本
  }
}
```

### 2.3 更新频率

| 类型 | 频率 |
|------|------|
| Patch | 每周检查 |
| Minor | 每月评估 |
| Major | 季度规划 |

---

## 三、升级迁移

### 3.1 Vue 升级命令

```bash
pnpm update vue vue-router pinia
pnpm why vue && pnpm ls vue  # 检查依赖关系
```

### 3.2 Breaking Changes 处理

```bash
pnpm lint              # ESLint 检查
pnpm type-check        # TypeScript 类型检查
npx vue-codemod@latest # Codemod 自动迁移
```

```typescript
// Vue 3.5: defineProps 解构响应性变更
// 推荐：使用 toRefs 保持响应性
const props = defineProps<{ title: string }>()
const { title } = toRefs(props)
```

### 3.3 迁移检查清单

```
□ 阅读更新日志（CHANGELOG）
□ 检查 Breaking Changes
□ 创建迁移分支
□ 更新依赖版本
□ 运行 pnpm install
□ 运行测试套件 (pnpm test)
□ 修复类型错误 (pnpm type-check)
□ 修复 ESLint 错误 (pnpm lint)
□ 本地功能验证
□ 构建验证 (pnpm build)
□ Code Review
□ 预发布环境验证
```

### 3.4 常见迁移场景

```bash
# Vite 5 → 6
pnpm update vite@^6.0.0  # 注意 Node.js >= 18

# TypeScript 5.6 → 5.7
pnpm update typescript@^5.7.0

# Tailwind CSS 3 → 4
pnpm update tailwindcss@^4.0.0  # 配置格式变更

# shadcn-vue 组件更新
npx shadcn-vue@latest add button --overwrite
```

---

## 四、回滚策略

### 4.1 Git 分支策略

```
main (生产) → release/v1.5.0 (预发布) → feature/upgrade-vue-3.5 (迁移分支)
```

### 4.2 快速回滚流程

```bash
# 回滚到上一版本
git revert HEAD && git push

# 回滚到指定版本
git checkout v1.2.3 && git checkout -b hotfix/rollback-v1.2.3

# 紧急回滚依赖
git checkout pnpm-lock.yaml && pnpm install --frozen-lockfile
```

---

## 五、构建配置

### 5.1 Vite 目标配置

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import autoprefixer from 'autoprefixer'
import { postcssNesting } from 'postcss-nesting'

export default defineConfig({
  plugins: [vue()],
  css: {
    postcss: { plugins: [postcssNesting(), autoprefixer()] },
    devSourcemap: true
  },
  build: {
    target: 'es2020',
    cssTarget: 'chrome90',
    cssMinify: 'lightningcss',
    rollupOptions: {
      output: { manualChunks: { vendor: ['vue', 'vue-router', 'pinia'] } }
    }
  }
})
```

### 5.2 PostCSS 完整配置

```javascript
// postcss.config.js
module.exports = {
  plugins: [
    require('@csstools/postcss-oklab-function'),
    require('postcss-container-queries'),
    require('postcss-nesting'),
    require('autoprefixer')({
      overrideBrowserslist: ['chrome >= 90', 'safari >= 14', 'firefox >= 90', 'edge >= 90'],
      grid: true
    })
  ]
}
```

---

## 六、禁止事项

| 禁止项 | 原因 |
|--------|------|
| ❌ 支持 IE 浏览器 | 已停止维护，成本过高 |
| ❌ 使用 `-webkit-` 前缀硬编码 | 由 Autoprefixer 自动处理 |
| ❌ 内联 polyfill 全量引入 | 按需引入，减少包体积 |
| ❌ 忽略 Safari 兼容性 | 市场份额 20%，必须支持 |
| ❌ 使用实验性 CSS 特性 | 缺乏广泛支持 |
| ❌ 直接在 main 分支升级 | 无法回滚，风险极高 |
| ❌ 跳过测试直接发布 | 可能引入严重 Bug |
| ❌ 同时升级多个 Major 版本 | 难以定位问题来源 |
| ❌ 忽略 deprecation 警告 | 未来升级成本更高 |
| ❌ 不提交 lockfile | 团队环境不一致 |
| ❌ 使用 `latest` 标签 | 版本不可控 |

---

**最后更新：** 2025-03-21 | **维护者：** 前端团队