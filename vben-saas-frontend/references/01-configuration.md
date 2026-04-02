# 配置化能力

> 通过 `preferences.ts` 零代码改动实现UI定制

---

## 主题配置

**文件**: `apps/web-antd/src/preferences.ts`

```typescript
import { defineOverridesPreferences } from '@vben/preferences';

export const overridesPreferences = defineOverridesPreferences({
  theme: {
    builtinType: 'custom',              // 内置主题
    colorPrimary: 'hsl(25 95% 54%)',    // 主品牌色
    colorSuccess: 'hsl(122 39% 49%)',   // 成功色
    colorWarning: 'hsl(46 84% 61%)',    // 警告色
    colorDestructive: 'hsl(0 74% 56%)', // 错误色
    mode: 'light',                       // light/dark/auto
    radius: '0.5',                       // 圆角(rem)
    fontSize: 14,                        // 字号(px)
    semiDarkHeader: false,               // 半深色头部
    semiDarkSidebar: false,              // 半深色侧边栏
  },
});
```

### 内置主题

| 主题 | 主色 | 适用场景 |
|------|------|---------|
| `default` | 蓝色 | 通用 |
| `orange` | 橙色 | 接近#FA8C16 |
| `violet` | 紫色 | 科技感 |
| `green` | 绿色 | 医疗健康 |
| `zinc` | 灰色 | 专业商务 |
| `custom` | 自定义 | 品牌定制 |

---

## 布局配置

```typescript
app: {
  name: '系统名称',
  layout: 'sidebar-nav',           // 布局模式
  contentCompact: 'wide',          // 内容宽度
  contentCompactWidth: 1280,       // 最大宽度
  contentPadding: 16,              // 内边距
  watermark: true,                 // 水印开关
  watermarkContent: '水印内容',    // 水印文字
},
```

### 布局模式

| 模式 | 说明 |
|------|------|
| `sidebar-nav` | 侧边栏导航(默认) |
| `header-nav` | 顶部导航 |
| `mixed-nav` | 混合导航 |

---

## 侧边栏配置

```typescript
sidebar: {
  width: 224,              // 宽度
  collapseWidth: 60,       // 折叠宽度
  collapsed: false,        // 默认折叠
  collapsedButton: true,   // 折叠按钮
},
```

---

## 标签栏配置

```typescript
tabbar: {
  enable: true,
  styleType: 'chrome',     // chrome/card/plain/brisk
  height: 38,
  keepAlive: true,         // 页面缓存
  showRefresh: true,       // 刷新按钮
  showMaximize: true,      // 最大化按钮
},
```

---

## 功能组件开关

```typescript
widget: {
  fullscreen: true,        // 全屏
  globalSearch: true,      // 全局搜索
  lockScreen: true,        // 锁屏
  notification: true,      // 通知
  themeToggle: true,       // 主题切换
  timezone: false,         // 时区(移除)
},
```

---

## CSS变量

**文件**: `packages/@core/base/design/src/design-tokens/default.css`

### 核心颜色变量

```css
:root {
  /* 品牌色 */
  --primary: 212 100% 45%;
  --success: 144 57% 58%;
  --warning: 42 84% 61%;
  --destructive: 359 100% 65%;
  
  /* 背景 */
  --background: 0 0% 100%;
  --card: 0 0% 100%;
  --popover: 0 0% 100%;
  
  /* 布局 */
  --sidebar: 0 0% 100%;
  --header: 0 0% 100%;
  
  /* 其他 */
  --border: 240 6% 90%;
  --radius: 0.5rem;
  --font-size-base: 16px;
}
```

### Tailwind映射

```html
<div class="bg-primary text-primary-foreground">
<div class="bg-card border-border">
<div class="rounded-lg">  <!-- 使用 --radius -->
```

---

## 运行时更新

```typescript
import { preferencesManager } from '@vben/preferences';

// 更新偏好
preferencesManager.updatePreferences({
  theme: { colorPrimary: 'hsl(25 95% 54%)' }
});

// 获取当前偏好
const prefs = preferencesManager.getPreferences();
```

---

## Tailwind扩展

**文件**: `apps/web-antd/tailwind.config.mjs`

```javascript
import baseConfig from '@vben/tailwind-config';

export default {
  ...baseConfig,
  theme: {
    extend: {
      boxShadow: {
        'card': '0 1px 3px rgba(0,0,0,0.08)',
        'card-hover': '0 4px 12px rgba(0,0,0,0.12)',
      },
      borderRadius: {
        'card': '0.75rem',
      },
    },
  },
};
```