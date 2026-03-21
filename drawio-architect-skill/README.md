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

## 🎯 何时使用

使用此技能当：
- 用户请求创建 `.drawio` 或 `.xml` 架构图文件
- 用户提及"画一个架构图"、"绘制流程图"、"系统拓扑"
- 用户需要将文字描述转为可视化图表
- 用户需要修改现有 draw.io 文件

## 🚫 何时不使用

不使用此技能当：
- 纯文字描述输出（无图表需求）
- 图片编辑（PNG/JPG 处理）
- 非 draw.io 格式的图表工具（Visio、Lucidchart、Mermaid）
- UML 类图/时序图（建议用 PlantUML 或 Mermaid）
- 数据可视化图表（ECharts、D3）

## 📥 输入参数

| 参数 | 说明 | 获取方式 |
|------|------|---------|
| **图类型** | `deploy` / `functional` / `flowchart` | 从用户描述推断 |
| **云厂商** | `alibaba` / `aws` / `gcp` / `azure` / `none` | 默认 `alibaba`，用户指定则覆盖 |
| **是否修改存量** | `true` / `false` | 用户是否提供现有文件 |
| **页面尺寸** | `auto` / 指定 width×height | 默认 `auto`，根据内容自动计算 |

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

## 📐 约束体系

本技能采用 ID 化约束体系，便于快速定位问题。完整约束见 `SKILL.md` 第十节。

### 约束分类速查

| 类别 | 前缀 | 数量 | 典型约束 |
|------|------|------|---------|
| XML 结构 | `C-XML-xxx` | 7 条 | mxGeometry 必须有 as="geometry"、特殊字符转义 |
| 文件结构 | `C-FILE-xxx` | 3 条 | 根 cell 必须存在、页面尺寸调整 |
| 布局 | `C-LAYOUT-xxx` | 11 条 | 同排宽高一致、层间距统一、调用方在上 |
| 图标 | `C-ICON-xxx` | 8 条 | shape name 小写下划线、fillColor 必填 |
| 连线 | `C-EDGE-xxx` | 5 条 | 方向一致、减少交叉、ID 匹配 |
| Z-order | `C-ZORDER-xxx` | 2 条 | 先写元素在底层、严格顺序 |
| 配色 | `C-COLOR-xxx` | 2 条 | 按职责分类、最多 4-5 种底色 |

### 高频约束 Top 5

| ID | 约束 | 常见错误 |
|----|------|---------|
| C-XML-001 | mxGeometry 必须有 as="geometry" | `Could not add object mxGeometry` |
| C-XML-002 | `&` 必须转义为 `&amp;` | `xmlParseEntityRef: no name` |
| C-ICON-001 | 阿里云 shape name 用小写下划线 | 图标空白方块 |
| C-ICON-002 | 图标必须有 fillColor | 图标空轮廓 |
| C-ZORDER-002 | 严格顺序：背景 → 嵌套框 → 文字 → 组件 → 连线 | 内容被遮挡 |

## 📄 许可证

MIT License