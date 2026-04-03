---
name: drawio-architect
description: >
  创建和编辑生产级 draw.io 架构图和流程图。
  触发：架构图/流程图/系统拓扑/业务流程/draw.io文件。
  支持阿里云/AWS/GCP/Azure/Kubernetes 图标库。
---

# draw.io 架构图与流程图技能

## 何时使用

适用：创建/修改 `.drawio` 或 `.xml` 架构图、流程图、系统拓扑
触发词：draw.io、架构图、部署图、流程图、泳道图、拓扑图

不适用：纯文字输出、图片编辑、其他图表工具、UML 类图/时序图（用 PlantUML/Mermaid）

## 支持的图类型

| 类型 | 说明 | 专用参考 |
|------|------|---------|
| 云部署架构图 | 云资源拓扑、K8s 集群、数据流 | `deploy_arch_patterns.md` |
| 功能/系统/技术架构图 | 功能模块、系统边界、技术栈 | `functional_arch_patterns.md` |
| 业务流程图 | 活动/判断/泳道、并行网关 | `flowchart_patterns.md` |

## 参考文档加载

1. **必须加载**：本 SKILL.md
2. **按图类型加载**：deploy_arch_patterns.md / functional_arch_patterns.md / flowchart_patterns.md
3. **按需加载**：
   - `tech_stack_icons.md` — 技术栈图标（前端/后端/数据库/中间件）
   - `alibaba_cloud_shapes.md` — 阿里云 311 个图标
   - `visual-systems.md` — 视觉系统
   - `design-guide.md` — 设计指南
   - `style-presets.md` — 样式预设
4. **调试时加载**：debug-guide.md

---

## 一、XML 必须规则（违反会导致文件损坏）

### 1. mxGeometry 必须有 as="geometry"

```xml
<!-- 正确 -->
<mxGeometry x="100" y="200" width="50" height="50" as="geometry"/>

<!-- 错误 → Could not add object mxGeometry -->
<mxGeometry x="100" y="200" width="50" height="50"/>
```

### 2. 特殊字符转义

| 字符 | 转义 |
|------|------|
| `&` | `&amp;` |
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |

最常见：`&` 未转义 → `xmlParseEntityRef: no name`

### 3. HTML 内容需 html=1

```xml
<mxCell value="&lt;b&gt;标题&lt;/b&gt;" style="...html=1;..." .../>
```

---

## 二、文件结构

```xml
<mxfile host="app.diagrams.net">
  <diagram name="name" id="id">
    <mxGraphModel dx="1400" dy="1000" grid="1" gridSize="10"
                  pageWidth="1200" pageHeight="1000">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 所有图元放这里 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

要点：
- id="0" 和 id="1" 根 cell 必须存在且在最前面
- Cell ID 用描述性字符串（如 `id="slb"`）
- pageWidth/pageHeight 按内容调整

---

## 三、布局核心原则

**调用方在上/左，被调用方在下/右，最大限度减少连线交叉。**

1. **纵向**：调用方在上，被调用方在下
2. **横向**：同层组件按调用顺序从左到右
3. **边栏**：横切关注点（消息队列、配置中心）放在右侧独立列

详细布局公式、间距标准 → `references/design-guide.md`

---

## 四、图标库

### 技术栈图标（SimpleIcons CDN）

用于功能架构图、技术栈展示图，覆盖前端/后端/数据库/中间件等主流技术。

```xml
<mxCell style="image;html=1;verticalLabelPosition=bottom;verticalAlign=top;align=center;
        strokeColor=none;fillColor=none;labelBackgroundColor=none;
        image=https://cdn.simpleicons.org/{icon-name}/{hex-color};"
        value="React" vertex="1" parent="1">
  <mxGeometry width="60" height="60" x="100" y="100" as="geometry"/>
</mxCell>
```

**常用图标**：

| 技术 | URL |
|------|-----|
| React | `https://cdn.simpleicons.org/react/61DAFB` |
| Vue.js | `https://cdn.simpleicons.org/vuedotjs/4FC08D` |
| Spring Boot | `https://cdn.simpleicons.org/springboot/6DB33F` |
| MySQL | `https://cdn.simpleicons.org/mysql/4479A1` |
| Redis | `https://cdn.simpleicons.org/redis/FF4438` |
| Kubernetes | `https://cdn.simpleicons.org/kubernetes/326CE5` |
| Docker | `https://cdn.simpleicons.org/docker/2496ED` |
| Kafka | `https://cdn.simpleicons.org/apachekafka/231F20` |

完整 80+ 图标 → `references/tech_stack_icons.md`

---

## 五、自定义图形库导入

### 导入技术栈图标库

项目提供了预定义的技术栈图标库文件 `tech_stack_library.drawiolib`，包含 50+ 常用技术栈图标。

**导入步骤**：

1. 打开 draw.io 桌面版或网页版
2. 菜单：**文件 → 打开库从 → 设备**
3. 选择 `tech_stack_library.drawiolib` 文件
4. 导入后，左侧面板会出现 "Tech Stack" 图形分类
5. 直接拖拽图标到画布使用

**导入后效果**：

```
左侧面板
├── 通用
├── 杂项
├── Tech Stack  ← 新增的分类
│   ├── HTML5
│   ├── CSS3
│   ├── JavaScript
│   ├── TypeScript
│   ├── React
│   ├── Vue.js
│   ├── Spring Boot
│   ├── MySQL
│   ├── Redis
│   ├── Docker
│   ├── Kubernetes
│   └── ... (50+ 图标)
```

### 手动创建自定义库

如果想自己创建库文件，格式如下：

```xml
<mxlibrary>[
  {"xml": "&lt;mxCell style=\"image;...image=https://cdn.simpleicons.org/react/61DAFB;\" vertex=\"1\"&gt;&lt;mxGeometry width=\"60\" height=\"60\" as=\"geometry\"/&gt;&lt;/mxCell&gt;", "w": 60, "h": 60, "title": "React"},
  {"xml": "...", "w": 60, "h": 60, "title": "Vue"}
]</mxlibrary>
```

**字段说明**：

| 字段 | 说明 |
|------|------|
| `xml` | mxCell 的 XML（需要转义 `<` `>` `"`） |
| `w` | 宽度 |
| `h` | 高度 |
| `title` | 显示名称 |

### 阿里云（mxgraph.alibaba_cloud.*）

Shape name 必须用**全小写下划线**格式：

```xml
<!-- 正确 -->
shape=mxgraph.alibaba_cloud.redis_kvstore

<!-- 错误 → 空白方块 -->
shape=mxgraph.alibaba_cloud.Redis KVStore
```

图标必须带完整属性：
```xml
<mxCell style="points=[];aspect=fixed;html=1;align=center;shadow=0;dashed=0;
       fillColor=#FF6A00;strokeColor=none;
       shape=mxgraph.alibaba_cloud.redis_kvstore;
       verticalLabelPosition=bottom;verticalAlign=top;
       fontSize=9;fontStyle=1;spacingTop=8;" .../>
```

| 属性 | 缺失后果 |
|------|---------|
| `fillColor` + `strokeColor=none` | 只显示空轮廓 |
| `shape=mxgraph.alibaba_cloud.{小写名}` | 空白方块 |
| `verticalLabelPosition=bottom` | 标签与图标重叠 |

常用图标：

| 服务 | Shape Name |
|------|-----------|
| 用户 | `user` |
| CDN | `cdn_content_distribution_network` |
| SLB | `slb_server_load_balancer_01` |
| API 网关 | `apigateway` |
| ACK/K8s | `ask_ack_container_service_for_kubernetes` |
| MySQL | `mysql` |
| Redis | `redis_kvstore` |
| OSS | `oss_object_storage_service` |

完整 311 个图标 → `references/alibaba_cloud_shapes.md`

### Kubernetes（mxgraph.kubernetes.*）

```xml
<mxCell style="...shape=mxgraph.kubernetes.icon2;prIcon=pod;fillColor=#326CE5;strokeColor=#ffffff;..." .../>
```

| prIcon | 用途 |
|--------|------|
| `pod` | 独立单元 |
| `deploy` | 有副本的微服务 |
| `ing` | API 网关 |
| `svc` | K8s Service |
| `cm` | 配置中心 |

### AWS / GCP / Azure

```
AWS:   shape=mxgraph.aws4.{name}
GCP:   shape=mxgraph.gcp2.{name}
Azure: image=img/lib/azure2/{path}.svg
```

---

## 五、配色原则

按**组件职责分类**选色，一张图最多 4-5 种底色：

| 色系 | fillColor | strokeColor | 用途 |
|------|-----------|-------------|------|
| 冷色 | `#DAEDF7` | `#2196F3` | 外部接入 |
| 暖色 | `#FBE9E7` | `#FF5722` | 核心/计算 |
| 中性 | `#E8F5E9` | `#43A047` | 业务服务 |
| 数据 | `#EDE7F6` | `#7B1FA2` | 数据/基础设施 |
| K8s | `#EBF3FF` | `#326CE5` | 容器 |

更多样式模板 → `references/style-presets.md`

---

## 六、连线规范

- **方向一致**：上→下 或 左→右
- **减少交叉**：交叉过多 → 调整组件位置
- **标签用于关键流**：不是每条线都需要标签
- **线宽语义**：2.5 主链路、2 普通、1.5 次要

详细连线规则 → `references/design-guide.md`

---

## 七、Z-order 原则

XML 中先写的元素在底层。严格顺序：

```
1. 层背景容器（底色矩形）
2. 嵌套框（K8s 边界、系统边界等）
3. 标签文字
4. 组件卡片 / 图标 / 流程节点
5. 连接线（最顶层）
```

---

## 八、容器与嵌套

### parent 属性实现嵌套

子元素的 `parent` 属性指向父容器 ID，实现视觉嵌套和分组移动：

```xml
<!-- 容器 -->
<mxCell id="container1" value="服务集群"
  style="swimlane;startSize=24;fillColor=#E3F2FD;strokeColor=#1976D2;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="300" height="200" as="geometry"/>
</mxCell>

<!-- 子元素（parent 指向容器） -->
<mxCell id="service1" value="服务A"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1976D2;"
  vertex="1" parent="container1">
  <mxGeometry x="20" y="40" width="120" height="60" as="geometry"/>
</mxCell>
```

**要点**：
- 子元素坐标相对于容器左上角
- 移动容器时子元素同步移动
- 容器可以是普通矩形或 swimlane

### Swimlane 样式

泳道容器（可折叠）：

```xml
<mxCell style="swimlane;startSize=24;horizontal=1;fillColor=#E3F2FD;strokeColor=#1976D2;" .../>
```

| 属性 | 说明 |
|------|------|
| `startSize` | 标题栏高度（默认 40） |
| `horizontal` | 1=横向泳道，0=纵向泳道 |
| `swimlaneFillColor` | 泳道内部填充色 |

---

## 九、连线锚点控制

### exitX/exitY/entryX/entryY

精确控制连线在节点上的进出位置（值范围 0-1）：

```xml
<!-- 从源节点右侧中部出，从目标节点左侧中部进 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=1;
       exitX=1;exitY=0.5;exitDx=0;exitDy=0;
       entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
  edge="1" source="nodeA" target="nodeB">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

**坐标参考**：

| 位置 | X | Y |
|------|---|---|
| 左边中部 | 0 | 0.5 |
| 右边中部 | 1 | 0.5 |
| 上边中部 | 0.5 | 0 |
| 下边中部 | 0.5 | 1 |
| 左上角 | 0 | 0 |
| 右下角 | 1 | 1 |

**应用场景**：
- 多条连线进出同一节点时避免重叠
- 控制连线走特定通道

### 连线样式选项

| 样式 | 说明 |
|------|------|
| `edgeStyle=orthogonalEdgeStyle` | 直角折线（默认） |
| `edgeStyle=elbowEdgeStyle` | 单弯头连线 |
| `curved=1` | 平滑曲线 |
| `rounded=1` | 折线圆角 |
| `jettySize=auto` | 自动计算避让距离 |

---

## 十、图层管理

复杂图可用图层分离不同抽象层次：

```xml
<root>
  <mxCell id="0"/>
  <mxCell id="1" parent="0"/>
  
  <!-- 图层定义 -->
  <mxCell id="layer-bg" value="背景层" parent="1"/>
  <mxCell id="layer-main" value="主内容" parent="1"/>
  <mxCell id="layer-conn" value="连线" parent="1"/>
  
  <!-- 元素指定所属图层 -->
  <mxCell id="bg1" value="" parent="layer-bg" vertex="1" .../>
  <mxCell id="node1" value="服务" parent="layer-main" vertex="1" .../>
  <mxCell id="edge1" source="node1" target="node2" parent="layer-conn" edge="1" .../>
</root>
```

**用途**：
- 分离背景、内容、连线
- 支持显示/隐藏特定图层
- 批量锁定或移动同层元素

---

## 十一、工作流程

1. **理解需求** — 判断图类型，读取对应 references
2. **分析元素** — 列出组件、关系、分组
3. **规划布局** — 按核心原则计算位置
4. **备份原文件** — 修改已有文件前备份
5. **编写 XML** — 按 Z-order 顺序
6. **交付前自检** — 见下方清单
7. **迭代优化** — 反馈后迭代

---

## 十二、交付前自检清单

**XML 正确性**：
- [ ] 每个 `<mxGeometry>` 有 `as="geometry"`
- [ ] 所有 `&` 转义为 `&amp;`
- [ ] 云图标 shape name 用小写下划线
- [ ] 图标有 `fillColor` + `strokeColor=none`
- [ ] 连线 source/target ID 匹配实际 cell ID
- [ ] Z-order 正确（背景先于内容）

**布局审计**：
- [ ] 同排组件宽高一致
- [ ] 层间 gap 统一（16-24px）
- [ ] 调用方在上/左
- [ ] 整体布局居中，无大面积空白

**连线审计**：
- [ ] 方向一致（上→下、左→右）
- [ ] 无明显交叉
- [ ] 关键流有标签

---

## 十三、常见错误速查

| 症状 | 原因 | 修复 |
|------|------|------|
| `Could not add object mxGeometry` | 缺 `as="geometry"` | 给每个 mxGeometry 加上 |
| `xmlParseEntityRef: no name` | 未转义 `&` | 改为 `&amp;` |
| 图标空白方块 | shape name 格式错 | 用小写下划线 |
| 图标空轮廓 | 缺 fillColor | 加 `fillColor=#FF6A00;strokeColor=none` |
| 内容被背景遮挡 | Z-order 错 | 背景写在内容之前 |

详细调试指南 → `references/debug-guide.md`

---

## 十四、约束总表

| 类别 | 前缀 | 核心约束 |
|------|------|---------|
| XML 结构 | C-XML | mxGeometry 必须有 as="geometry"、特殊字符转义 |
| 文件结构 | C-FILE | 根 cell 必须存在、pageWidth/pageHeight 按内容调整 |
| 布局 | C-LAYOUT | 同排宽高一致、层间距统一、调用方在上 |
| 图标 | C-ICON | shape name 小写下划线、fillColor 必填 |
| 连线 | C-EDGE | 方向上→下/左→右、减少交叉 |
| Z-order | C-ZORDER | 背景→嵌套框→文字→组件→连线 |
| 配色 | C-COLOR | 按职责分类、最多 4-5 种底色 |