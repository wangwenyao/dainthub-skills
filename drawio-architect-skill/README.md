# draw.io 架构图与流程图技能

创建和编辑生产级 `.drawio` XML 文件，覆盖多种图表类型。

## 支持的图类型

| 类型 | 说明 | 专用参考 |
|------|------|---------|
| **云部署架构图** | 云资源拓扑、K8s 集群、数据流 | `deploy_arch_patterns.md` |
| **功能/系统/技术架构图** | 功能模块、系统边界、技术栈 | `functional_arch_patterns.md` |
| **业务流程图** | 活动/判断/泳道、并行网关 | `flowchart_patterns.md` |

## 项目结构

```
drawio-architect-skill/
├── SKILL.md                        # 技能主文件（核心规则、约束总表）
└── references/                     # 参考文档
    ├── alibaba_cloud_shapes.md     # 阿里云图标库（311个）
    ├── deploy_arch_patterns.md     # 云部署架构图模式
    ├── functional_arch_patterns.md # 功能架构图模式
    ├── flowchart_patterns.md       # 业务流程图模式
    ├── visual-systems.md           # 视觉系统与风格选择
    ├── design-guide.md             # 设计指南（布局/连线/成品感）
    ├── style-presets.md            # 样式预设模板
    └── debug-guide.md              # 调试指南
```

## 触发词

`draw.io`、`架构图`、`部署图`、`流程图`、`泳道图`、`拓扑图`

## 核心规范速查

### XML 必须规则

```xml
<!-- mxGeometry 必须有 as="geometry" -->
<mxGeometry x="100" y="200" width="50" height="50" as="geometry"/>

<!-- 特殊字符转义 -->
value="A &amp; B"

<!-- 图标完整属性 -->
<mxCell style="shape=mxgraph.alibaba_cloud.redis_kvstore;
       fillColor=#FF6A00;strokeColor=none;
       verticalLabelPosition=bottom;verticalAlign=top;
       spacingTop=8;aspect=fixed;" .../>
```

### 高级特性

```xml
<!-- 容器嵌套（子元素 parent 指向容器） -->
<mxCell id="child" parent="container1" vertex="1" .../>

<!-- 连线锚点控制 -->
<mxCell style="exitX=1;exitY=0.5;entryX=0;entryY=0.5;" .../>
```

### 布局原则

**调用方在上/左，被调用方在下/右，减少连线交叉。**

### 配色

| 色系 | fillColor | 用途 |
|------|-----------|------|
| 冷色 | `#DAEDF7` | 外部接入 |
| 暖色 | `#FBE9E7` | 核心/计算 |
| 中性 | `#E8F5E9` | 业务服务 |

## 工作流程

1. 理解需求 → 判断图类型，读取 references
2. 分析元素 → 列出组件、关系、分组
3. 规划布局 → 按核心原则计算位置
4. 编写 XML → 按 Z-order 顺序
5. 交付前自检 → 验证清单

## 常见错误

| 症状 | 原因 | 修复 |
|------|------|------|
| `Could not add object mxGeometry` | 缺 `as="geometry"` | 给每个 mxGeometry 加上 |
| `xmlParseEntityRef: no name` | 未转义 `&` | 改为 `&amp;` |
| 图标空白方块 | shape name 格式错 | 用小写下划线 |
| 图标空轮廓 | 缺 fillColor | 加渲染属性 |

## 许可证

MIT License