# 情感化设计规范

## 核心原则

B端情感设计本质：**建立信任与信心，而非制造惊喜**。

- 克制表达：情感反馈服务于任务完成，不分散注意力
- 专业优先：用户追求效率，不是娱乐体验
- 参考：Linear 成功动画、Notion 错误提示——安静、确定、专业

---

## 成功状态

### 微庆祝动画

```css
@keyframes success-check {
  0%   { transform: scale(0.8); opacity: 0; }
  50%  { transform: scale(1.05); }
  100% { transform: scale(1); opacity: 1; }
}
.success-icon { animation: success-check 200ms var(--ease-out); }
```

**时长：** 图标 150-200ms，颜色过渡 100ms，禁止弹跳效果

### Toast 时长

| 场景 | 时长 | 文案示例 |
|------|------|----------|
| 普通成功 | 2s | "已保存" |
| 重要操作 | 3s | "已发布到生产环境" |
| 可撤销 | 4s + 按钮 | "已删除" + 撤销 |

**文案：** 具体（"已保存"）而非泛泛（"操作成功"）

---

## 错误状态

### 文案原则

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| "您的输入有误" | "邮箱格式不正确，请检查后重试" |
| "操作失败" | "网络连接中断，请检查网络后重试" |
| "权限不足" | "需要管理员权限才能执行此操作" |

### 图标选择

- `alert-circle` → 推荐（中性）
- `alert-triangle` → 禁止（过于惊恐）

### 恢复路径

每个错误必须提供明确下一步：

```html
<Alert variant="destructive">
  <AlertTitle>加载失败</AlertTitle>
  <AlertDescription>
    无法获取数据。<Button variant="link">重试</Button>
  </AlertDescription>
</Alert>
```

---

## 加载状态

### 骨架屏

匹配真实布局，非通用占位：

```html
<!-- ✅ 正确 -->
<div class="space-y-3">
  <Skeleton class="h-4 w-3/4" />
  <Skeleton class="h-3 w-full" />
</div>
```

### 进度反馈

| 时长 | 反馈方式 |
|------|----------|
| < 1s | 无需反馈 |
| 1-3s | Spinner / 按钮加载态 |
| > 3s | 进度条 + 百分比 |

### 乐观更新

```typescript
async function toggleStatus(item) {
  item.status = !item.status  // 立即更新
  try { await api.update(item) }
  catch (e) {
    item.status = !item.status // 回滚
    toast.error('更新失败，已恢复')
  }
}
```

---

## 进度与成就

### 进度条

```css
.progress-bar {
  background: var(--color-brand-500);
  transition: width 300ms var(--ease-default);
}
```

**禁止：** 彩虹渐变、闪烁效果、游戏化元素

### 里程碑

用小型 Toast，禁止弹窗：

```typescript
// ✅ 正确
toast.success('已完成 80% 的配置', { duration: 2000 })
// ❌ 错误
showModal({ title: '🎉 恭喜！' })
```

---

## 文案语调

| 原则 | 示例 |
|------|------|
| 专业有人味 | 不用"亲"、"哦~" |
| 具体胜泛泛 | "已保存 3 条" 非 "操作成功" |
| 主动语态 | "系统已发送" 非 "邮件已被发送" |
| 无行话 | 避免"异步处理"、"幂等性" |

---

## 禁止事项

### 动画类

- ❌ 彩带、撒花、庆祝动画（C-EMOTION-001）
- ❌ 弹跳、回弹效果
- ❌ 循环播放的非加载动画

### 交互类

- ❌ 成功/庆祝弹窗（C-EMOTION-002）
- ❌ 游戏化元素（徽章、积分、连续天数）（C-EMOTION-003）
- ❌ 阻断式成就提示

### 文案类

- ❌ "恭喜"、"太棒了"、"厉害"（C-EMOTION-004）
- ❌ "亲"、"哦~"、"呢~"（C-EMOTION-005）
- ❌ 技术术语对用户展示
- ❌ 指责用户的表述

### 视觉类

- ❌ 彩色渐变进度条（C-COLOR-004）
- ❌ 闪烁、脉冲装饰效果
- ❌ emoji 作为主要视觉元素（C-EMOTION-006）