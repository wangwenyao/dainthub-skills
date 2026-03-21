# draw.io 架构图与流程图技能

创建和编辑生产级 `.drawio` XML 文件，覆盖多种图表类型。

## 📖 项目简介

本技能用于指导 AI 助手生成可直接在 draw.io 桌面版和网页版打开的架构图、流程图 XML 文件。支持阿里云、AWS、GCP、Azure 云厂商图标库和 Kubernetes 图标库。

## 🎯 支持的图类型

| 类型 | 说明 | 专用参考 |
|------|------|---------|
| **云部署架构图** | 云资源拓扑、K8s 集群、数据流 | `references/deploy_arch_patterns.md` |
| **功能架构图** | 功能模块分层、系统边界、接口 | `references/functional_arch_patterns.md` |
| **业务流程图** | 活动/判断/泳道、并行网关 | `references/flowchart_patterns.md` |

## 📁 项目结构

```
drawio-architect-skill/
├── SKILL.md                        # 技能主文件（通用规则、布局方法、图标库）
└── references/                     # 参考文档目录
    ├── alibaba_cloud_shapes.md     # 阿里云图标库（311个）
    ├── deploy_arch_patterns.md     # 云部署架构图模式
    ├── flowchart_patterns.md       # 业务流程图模式
    └── functional_arch_patterns.md # 功能架构图模式
```

## 🚀 触发词

- `draw.io`、`diagrams.net`、`mxfile`
- `架构图`、`部署图`、`功能架构`、`系统架构`
- `流程图`、`泳道图`、`拓扑图`

## 📋 核心规范速查

### XML 必须遵守的规则

```xml
<!-- ✅ 正确：mxGeometry 必须有 as="geometry" -->
<mxGeometry x="100" y="200" width="50" height="50" as="geometry"/>

<!-- ✅ 正确：特殊字符转义 -->
value="A &amp; B"  <!-- & → &amp; -->

<!-- ✅ 正确：图标完整属性 -->
<mxCell style="shape=mxgraph.alibaba_cloud.redis_kvstore;
       fillColor=#FF6A00;strokeColor=none;
       verticalLabelPosition=bottom;verticalAlign=top;
       spacingTop=8;aspect=fixed;" .../>
```

### 布局核心原则

**调用方在上/左，被调用方在下/右，最大限度减少连线交叉。**

- **纵向**：调用方在上，被调用方在下
- **横向**：同层组件按调用顺序从左到右排列
- **边栏**：横切关注点放在右侧独立列

### 图标库

| 云厂商 | Shape 前缀 |
|--------|-----------|
| 阿里云 | `mxgraph.alibaba_cloud.{name}` |
| Kubernetes | `mxgraph.kubernetes.icon2;prIcon={type}` |
| AWS | `mxgraph.aws4.{name}` |
| GCP | `mxgraph.gcp2.{name}` |
| Azure | `image=img/lib/azure2/{path}.svg` |

### Z-order 顺序

```
1. 层背景容器（底色矩形）
2. 嵌套框（K8s 边界、系统边界等）
3. 标签文字
4. 组件卡片 / 图标 / 流程节点
5. 连接线（最顶层）
```

### 配色原则

按**组件职责分类**选色，同类用同色系：

| 色系 | 用途 | 颜色示例 |
|------|------|---------|
| 暖色系 | 核心/计算 | `#FBE9E7` / `#FF5722` |
| 冷色系 | 基础/稳定 | `#DAEDF7` / `#2196F3` |
| 中性色 | 业务/服务 | `#E8F5E9` / `#43A047` |

## 🔧 工作流程

1. **理解需求** — 判断图类型，读取对应 references
2. **分析元素** — 列出组件、关系、分组
3. **规划布局** — 按布局方法论计算尺寸和位置
4. **备份原文件** — 修改已有文件前备份
5. **编写 XML** — 按 Z-order 顺序
6. **交付前自检** — 检查清单验证
7. **迭代优化** — 用户反馈后迭代

## ⚠️ 常见错误

| 症状 | 原因 | 修复 |
|------|------|------|
| `Could not add object mxGeometry` | 缺 `as="geometry"` | 给每个 mxGeometry 加上 |
| `xmlParseEntityRef: no name` | 未转义 `&` | 改为 `&amp;` |
| 图标空白方块 | shape name 格式错 | 用小写下划线 |
| 图标空轮廓 | 缺 fillColor | 加渲染属性 |
| 内容被背景遮挡 | Z-order 错 | 背景写在内容之前 |

## 📄 许可证

MIT License