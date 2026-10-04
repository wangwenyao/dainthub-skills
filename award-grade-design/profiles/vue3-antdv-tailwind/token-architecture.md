# Token Architecture

## 分层

```text
Product Semantic Tokens
        ↓
Theme Adapter
   ┌────┴────┐
AntDV       Tailwind / CSS
```

## 原则

不要让 Ant Design Vue token 或 Tailwind utility 成为产品级视觉命名空间。

推荐：

```text
color.action.primary
color.surface.base
color.text.primary
space.2
radius.md
motion.fast
```

然后再适配到具体技术实现。
