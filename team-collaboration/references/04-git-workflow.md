# git 工作流

---

## 分支结构

```
main (生产)
    ↓
develop (开发)
    ↓
feature/{模块}-v{版本} (功能开发)
```

---

## 分支命名规范

| 类型 | 命名格式 | 示例 |
|------|---------|------|
| 功能开发 | `feature/{模块}-v{版本}` | `feature/product-v1.0` |
| bug修复 | `fix/{模块}-v{版本}` | `fix/product-v1.1` |
| 技术重构 | `refactor/{模块}-v{版本}` | `refactor/product-v2.0` |

---

## 版本号规范

格式：`v{大版本}.{小版本}`

| 版本变更 | 规则 | 示例 |
|---------|------|------|
| 大版本 | 架构重构、重大功能变更 | v1.0 → v2.0 |
| 小版本 | 功能迭代、bug修复 | v1.0 → v1.1 |

---

## Commit Message 格式

```
<type>(scope): <description>

类型：
- feat: 新增功能
- fix: bug修复
- docs: 文档更新
- refactor: 重构
- test: 测试相关
- chore: 杂项

示例：
- feat(product): 新增商品列表页
- fix(trade): 修复订单状态字段类型
- docs(api): 更新 OpenAPI 文档 v1.1
```

