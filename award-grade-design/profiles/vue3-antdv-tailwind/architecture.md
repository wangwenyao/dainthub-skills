# Architecture Profile — 工程架构建议

推荐边界：

```text
app / layout
    ↓
foundation primitives
    ↓
product patterns
    ↓
domain components
    ↓
page composition
```

## 目录建议

```text
src/
├── app/
├── layouts/
├── pages/
├── components/
│   ├── foundation/
│   ├── data-display/
│   ├── feedback/
│   ├── navigation/
│   └── business/
├── design-system/
│   ├── tokens/
│   ├── themes/
│   ├── contracts/
│   ├── primitives/
│   └── patterns/
├── composables/
├── services/
└── styles/
```

目录只是推荐；优先遵守已有仓库约定。
