---
name: drawio-architect
description: >
  创建和编辑生产级 draw.io（.drawio / .xml）架构图和流程图文件。支持的图类型：云部署架构图、功能架构图、系统架构图、业务流程图、数据流图。支持阿里云/AWS/GCP/Azure 云厂商图标库和 Kubernetes 图标库。当用户需要创建、修改、修复 draw.io 图表，绘制任何类型的架构图或流程图，将架构描述或业务流程转为可视化图表，或排查 draw.io XML 格式问题时使用此技能。触发词包括：draw.io、diagrams.net、mxfile、架构图、部署图、功能架构、系统架构、流程图、泳道图、拓扑图。输出可直接在 draw.io 桌面版和网页版打开的独立 XML 文件。
license: MIT
compatibility:
  - Claude Code
  - OpenCode
  - Cursor
  - Codex
metadata:
  author: wwy
  version: "3.0"
  tags: draw.io, architecture, diagram, flowchart, cloud, kubernetes
---

# draw.io 架构图与流程图技能

创建和编辑生产级 `.drawio` XML 文件，覆盖多种图表类型。

## 何时使用

使用此技能当：
- 用户请求创建 `.drawio` 或 `.xml` 架构图文件
- 用户提及"画一个架构图"、"绘制流程图"、"系统拓扑"
- 用户需要将文字描述转为可视化图表
- 用户需要修改现有 draw.io 文件
- 用户提及触发词：draw.io、diagrams.net、mxfile、架构图、部署图、功能架构、系统架构、流程图、泳道图、拓扑图

## 何时不使用

不使用此技能当：
- 纯文字描述输出（无图表需求）
- 图片编辑（PNG/JPG 处理）
- 非 draw.io 格式的图表工具（Visio、Lucidchart、Mermaid）
- UML 类图/时序图（建议用 PlantUML 或 Mermaid）
- 数据可视化图表（ECharts、D3）

## 支持的图类型

| 类型 | 说明 | 专用参考 |
|------|------|---------|
| **云部署架构图** | 云资源拓扑、K8s 集群、数据流 | `references/deploy_arch_patterns.md` |
| **功能架构图** | 功能模块分层、系统边界、接口 | `references/functional_arch_patterns.md` |
| **业务流程图** | 活动/判断/泳道、并行网关 | `references/flowchart_patterns.md` |

**使用方式**：先读本文件了解通用规则，再按图类型读取对应的 references 文件获取专用模式和模板。

---

## 输入参数

| 参数 | 说明 | 获取方式 |
|------|------|---------|
| **图类型** | `deploy` / `functional` / `flowchart` | 从用户描述推断 |
| **云厂商** | `alibaba` / `aws` / `gcp` / `azure` / `none` | 默认 `alibaba`，用户指定则覆盖 |
| **是否修改存量** | `true` / `false` | 用户是否提供现有文件 |
| **页面尺寸** | `auto` / 指定 width×height | 默认 `auto`，根据内容自动计算 |

---

## 一、必须遵守的规则（违反会导致文件损坏）

### 1. 每个 `<mxGeometry>` 必须包含 `as="geometry"`

遗漏会报 `Could not add object mxGeometry`。**所有** mxGeometry 都必须加，无例外。

```xml
<!-- 正确 -->
<mxGeometry x="100" y="200" width="50" height="50" as="geometry"/>

<!-- 错误 -->
<mxGeometry x="100" y="200" width="50" height="50"/>
```

### 2. XML 实体转义

`value` 中的特殊字符必须转义：`&` → `&amp;`，`<` → `&lt;`，`>` → `&gt;`，`"` → `&quot;`。

最常见：`&` 未转义导致 `xmlParseEntityRef: no name`。

### 3. value 中嵌套 HTML

style 中加 `html=1`，HTML 标签和属性完整转义：

```xml
<mxCell value="&lt;b&gt;标题&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#888&quot; style=&quot;font-size:8px&quot;&gt;描述&lt;/font&gt;"
        style="rounded=1;whiteSpace=wrap;html=1;..." .../>
```

---

## 二、文件结构

```xml
<mxfile host="app.diagrams.net">
  <diagram name="diagram-name" id="unique-id">
    <mxGraphModel dx="1400" dy="1000" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1" page="1"
                  pageScale="1" pageWidth="1200" pageHeight="1000"
                  math="0" shadow="0">
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
- `pageWidth`/`pageHeight` 按内容调整，内容增减时同步更新
- id="0" 和 id="1" 两个根 cell 必须存在且在最前面
- Cell ID 用描述性字符串（如 `id="slb"`、`id="e_app_slb"`）

---

## 三、布局规划方法论

**先规划再编码。** 不要直接写 XML，先完成以下分析。

### 步骤 1：识别图类型

根据用户需求判断属于哪类图，然后读取对应的 `references/` 文件：
- 涉及服务器/容器/云资源/数据库部署 → `deploy_arch_patterns.md`
- 涉及功能模块/系统边界/能力分层 → `functional_arch_patterns.md`
- 涉及业务步骤/审批流/判断分支/角色分工 → `flowchart_patterns.md`

### 步骤 2：分析架构元素

1. 列出所有组件/节点
2. 梳理组件之间的依赖/调用/数据流关系
3. 按职责或层次分组

### 步骤 3：组件位置基于依赖关系排列

**核心原则：调用方在上/左，被调用方在下/右，最大限度减少连线交叉。**

- **纵向**：调用方在上，被调用方在下。层顺序反映调用链深度
- **横向**：同层组件按调用顺序从左到右排列
- **边栏**：横切关注点（消息队列、配置中心、监控）放在右侧独立列
- **目标**：所有连线尽量上→下、左→右，避免回头线和交叉

### 步骤 4：计算尺寸和间距

**不要硬编码固定宽度。** 根据元素数量和容器宽度动态计算。

**等宽排列**（推荐同类组件）：
```
n 个组件，容器可用宽度 W，期望间距 gap
组件宽度 w = (W - (n+1) × gap) / n
第 i 个 x = 容器左边 + gap + i × (w + gap)
```

**指定宽度 + 等距排列**：
```
间距 gap = (W - n × w) / (n + 1)
第 i 个 x = 容器左边 + gap × (i+1) + w × i
```

**尺寸一致性原则：**
- 同一排组件宽高必须一致
- 不同排可以不同宽高，但同排内统一
- 图标类组件统一尺寸（如 45×45）
- 卡片类组件高度统一

### 步骤 5：间距规则

**层间距**：所有层之间保持统一 gap（推荐 16-24px）。

**层内间距**：

| 位置 | 推荐值 |
|------|--------|
| 层标题 → 第一排内容 | 标题高 + 8-12px |
| 行间距（同层多排） | 16-24px，保持统一 |
| 最后一排 → 层底 | ≥ 12px |
| 图标 spacingTop | 4-8px |

**行高均分公式**（一层内有 n 排时）：
```
可用高度 H = 层高 - 标题区 - 上下 padding
行间 gap = (H - n × 行高) / (n + 1)
```

---

## 四、图标库

### 阿里云（`mxgraph.alibaba_cloud.*`）

Shape name 必须用**全小写下划线**格式：

```
✅ shape=mxgraph.alibaba_cloud.redis_kvstore
❌ shape=mxgraph.alibaba_cloud.Redis KVStore
❌ shape=mxgraph.alicloud.redis
```

图标必须带完整渲染属性：

```xml
<mxCell id="redis" value="Redis"
  style="points=[];aspect=fixed;html=1;align=center;shadow=0;dashed=0;
         fillColor=#FF6A00;strokeColor=none;
         shape=mxgraph.alibaba_cloud.redis_kvstore;
         verticalLabelPosition=bottom;verticalAlign=top;
         fontSize=9;fontStyle=1;spacingTop=8;"
  vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="45" height="45" as="geometry"/>
</mxCell>
```

| 属性 | 缺失后果 |
|------|---------|
| `fillColor=#FF6A00;strokeColor=none` | 只显示空轮廓 |
| `shape=mxgraph.alibaba_cloud.{小写名}` | 空白方块 |
| `verticalLabelPosition=bottom;verticalAlign=top` | 标签与图标重叠 |
| `spacingTop=6-8` | 标签紧贴图标 |
| `aspect=fixed` | 图标变形 |

常用图标见下表。需要完整 311 个图标时，读取 `references/alibaba_cloud_shapes.md`。

| 服务 | Shape Name |
|------|-----------|
| 用户 | `user` |
| 网站 | `enterprise_website` |
| CDN | `cdn_content_distribution_network` |
| SLB | `slb_server_load_balancer_01` |
| API 网关 | `apigateway` |
| WAF | `waf_web_application_firewall` |
| ACK/K8s | `ask_ack_container_service_for_kubernetes` |
| MySQL | `mysql` |
| Redis | `redis_kvstore` |
| ES | `elasticsearch` |
| OSS | `oss_object_storage_service` |
| Kafka | `kafka` |
| SLS | `sls_simple_log_service` |
| Prometheus | `prometheus` |

### Kubernetes（`mxgraph.kubernetes.*`）

通过 `prIcon` 选类型，`fillColor` 变色区分技术栈：

```xml
<mxCell style="...shape=mxgraph.kubernetes.icon2;prIcon=pod;fillColor=#2875E2;strokeColor=#ffffff;..." .../>
```

| prIcon | 资源 | 适合表示 |
|--------|------|---------|
| `pod` | Pod | AI Agent、独立单元 |
| `deploy` | Deployment | 有副本的微服务 |
| `ing` | Ingress | API 网关 |
| `svc` | Service | K8s Service |
| `cm` | ConfigMap | 配置中心 |
| `limits` | LimitRange | 限流/熔断 |

### AWS / GCP / Azure

```
AWS:   shape=mxgraph.aws4.{name}
GCP:   shape=mxgraph.gcp2.{name}
Azure: image=img/lib/azure2/{path}.svg
```

---

## 五、通用图元样式

### 矩形容器（层背景/分区）

```xml
<mxCell style="rounded=1;whiteSpace=wrap;html=1;fillColor=#DAEDF7;strokeColor=#2196F3;strokeWidth=2;arcSize=3;" .../>
```

### 文字标签

```xml
<mxCell style="text;html=1;fontSize=12;fontStyle=1;fontColor=#0D47A1;align=left;verticalAlign=top;" .../>
```

### 服务卡片（标题+描述）

```xml
<mxCell value="&lt;b&gt;服务名&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#888&quot; style=&quot;font-size:8px&quot;&gt;描述&lt;/font&gt;"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#FF6600;fontColor=#333;fontSize=9;arcSize=8;align=center;" .../>
```

### 卡片内嵌图标

图标叠放在卡片左侧，文字居中偏右：
- 图标位置：`x = card_x + 8`，`y = card_y + (card_h - 25) / 2`
- 卡片文字：`align=center;spacingLeft=22`

### 配色原则

按**组件职责分类**选色，同类用同色系，一张图最多 4-5 种底色：

**暖色系**（核心/计算）：
- `fillColor=#FBE9E7;strokeColor=#FF5722` — 核心计算
- `fillColor=#FFF3E0;strokeColor=#E65100` — 监控/告警
- `fillColor=#FFF9E6;strokeColor=#FF9800` — 编排/平台

**冷色系**（基础/稳定）：
- `fillColor=#DAEDF7;strokeColor=#2196F3` — 外部接入
- `fillColor=#EBF3FF;strokeColor=#326CE5` — 容器/K8s
- `fillColor=#EDE7F6;strokeColor=#7B1FA2` — 数据/基础设施

**中性色系**（业务/服务）：
- `fillColor=#E8F5E9;strokeColor=#43A047` — 业务服务
- `fillColor=#E8EAF6;strokeColor=#7986CB` — 中间件

---

## 六、连接线规范

### 基本连线

```xml
<mxCell id="e_a_b" style="edgeStyle=orthogonalEdgeStyle;rounded=1;flowAnimation=1;strokeColor=#2196F3;strokeWidth=2;"
  edge="1" parent="1" source="a" target="b">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 布局原则

- **方向一致**：连线尽量上→下或左→右，避免回头线
- **减少交叉**：交叉过多说明组件位置需调整，不是调连线
- **标签仅用于关键流**：不是每条线都需要标签
- **标签颜色与线色一致**

### 连线粗细

| strokeWidth | 语义 |
|-------------|------|
| `2.5` | 主链路 |
| `2` | 普通数据流 |
| `1.5` | 次要连接 |

### 颜色编码（参考，按项目调整）

| 颜色 | Hex | 常见含义 |
|------|-----|---------|
| 蓝 | `#2196F3` | 外部流量 |
| 橙 | `#FF9800` | 路由/均衡 |
| 红 | `#FF5722` | AI/ML 链路 |
| 绿 | `#43A047` | 业务逻辑 |
| 紫 | `#7B1FA2` | 数据层调用 |
| 浅蓝虚线 | `#90CAF9` + `dashed=1` | 可选/旁路 |

### 流程图专用连线

判断分支加条件标签：
```xml
<mxCell value="是" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#43A047;strokeWidth=2;fontSize=9;fontColor=#43A047;" .../>
<mxCell value="否" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#F44336;strokeWidth=2;fontSize=9;fontColor=#F44336;" .../>
```

---

## 七、Z-order 原则

XML 中先写的元素在底层。严格按此顺序：

```
1. 层背景容器（底色矩形）
2. 嵌套框（K8s 边界、系统边界等）
3. 标签文字
4. 组件卡片 / 图标 / 流程节点
5. 连接线（最顶层）
```

---

## 八、工作流程

1. **理解需求** — 判断图类型，读取对应 references
2. **分析元素** — 列出组件、关系、分组
3. **规划布局** — 按第三章方法论计算尺寸和位置
4. **备份原文件** — 修改已有文件前复制为 `{filename}_backup.xml`（递增编号）
5. **编写 XML** — 按 Z-order 顺序
6. **交付前自检** — 见下方清单
7. **迭代优化** — 用户反馈后 → 备份 → 修改 → 自检

### 从外部文件转换（PPT/文档/图片）

1. 提取组件名称、描述、层次关系
2. 分析调用关系和数据流方向
3. 用本 skill 规则**重新规划布局**（不要照搬原图坐标）
4. 生成独立新文件

### 交付前自检清单

**XML 正确性：**
- [ ] 每个 `<mxGeometry>` 有 `as="geometry"`
- [ ] 所有 `&` 转义为 `&amp;`
- [ ] 云图标 shape name 用小写下划线
- [ ] 图标有 `fillColor` + `strokeColor=none`
- [ ] 连线 source/target ID 匹配实际 cell ID
- [ ] Z-order 正确（背景先于内容）

**布局审计：**
- [ ] 同排组件宽高一致
- [ ] 同排组件等距（验证 x 间隔相等）
- [ ] 左右边距对称
- [ ] 层间 gap 统一
- [ ] 内容不溢出层边界
- [ ] 标签和图标无重叠
- [ ] 并排区块顶部对齐、高度相同
- [ ] 整体布局居中，无大面积空白失衡

**连线审计：**
- [ ] 方向一致（上→下、左→右）
- [ ] 无明显交叉
- [ ] 关键流有标签
- [ ] 颜色编码一致

---

## 九、常见错误速查

| 症状 | 原因 | 修复 |
|------|------|------|
| `Could not add object mxGeometry` | 缺 `as="geometry"` | 给每个 mxGeometry 加上 |
| `xmlParseEntityRef: no name` | 未转义 `&` | 改为 `&amp;` |
| 图标空白方块 | shape name 格式错 | 用小写下划线 |
| 图标空轮廓 | 缺 fillColor | 加 `fillColor=#FF6A00;strokeColor=none` |
| 标签图标重叠 | 缺间距 | 加 `spacingTop=6-8` |
| 内容被背景遮挡 | Z-order 错 | 背景写在内容之前 |
| 同排不对称 | 间距计算错 | 用等距公式重算 |
| 连线大量交叉 | 组件位置不合理 | 按依赖关系重排位置 |

---

## 十、约束总表

本节汇总所有约束规则，按类别编号便于快速查阅和问题定位。

### XML 结构约束 (C-XML-xxx)

| ID | 约束 | 违反后果 | 来源章节 |
|----|------|---------|---------|
| C-XML-001 | 每个 `<mxGeometry>` 必须包含 `as="geometry"` | `Could not add object mxGeometry` | 一.1 |
| C-XML-002 | `value` 中 `&` 必须转义为 `&amp;` | `xmlParseEntityRef: no name` | 一.2 |
| C-XML-003 | `value` 中 `<` 必须转义为 `&lt;` | XML 解析错误 | 一.2 |
| C-XML-004 | `value` 中 `>` 必须转义为 `&gt;` | XML 解析错误 | 一.2 |
| C-XML-005 | `value` 中 `"` 必须转义为 `&quot;` | XML 解析错误 | 一.2 |
| C-XML-006 | value 中嵌套 HTML 必须在 style 中加 `html=1` | HTML 不渲染 | 一.3 |
| C-XML-007 | HTML 标签和属性必须完整转义 | 渲染异常 | 一.3 |

### 文件结构约束 (C-FILE-xxx)

| ID | 约束 | 违反后果 | 来源章节 |
|----|------|---------|---------|
| C-FILE-001 | `id="0"` 和 `id="1"` 两个根 cell 必须存在且在最前面 | 文件无法打开 | 二 |
| C-FILE-002 | `pageWidth`/`pageHeight` 按内容调整 | 内容溢出或空白过多 | 二 |
| C-FILE-003 | Cell ID 使用描述性字符串（如 `id="slb"`） | 可维护性差 | 二 |

### 布局约束 (C-LAYOUT-xxx)

| ID | 约束 | 违反后果 | 来源章节 |
|----|------|---------|---------|
| C-LAYOUT-001 | 同一排组件宽高必须一致 | 视觉不对称 | 三.4 |
| C-LAYOUT-002 | 不同排可不同宽高，但同排内统一 | 视觉混乱 | 三.4 |
| C-LAYOUT-003 | 图标类组件统一尺寸（推荐 45×45） | 大小不一 | 三.4 |
| C-LAYOUT-004 | 卡片类组件高度统一 | 参差不齐 | 三.4 |
| C-LAYOUT-005 | 层间距保持统一 gap（推荐 16-24px） | 层次不清 | 三.5 |
| C-LAYOUT-006 | 层标题 → 第一排内容间距：标题高 + 8-12px | 标题与内容过近 | 三.5 |
| C-LAYOUT-007 | 行间距（同层多排）保持 16-24px 统一 | 排列不均 | 三.5 |
| C-LAYOUT-008 | 最后一排 → 层底间距 ≥ 12px | 内容贴边 | 三.5 |
| C-LAYOUT-009 | 调用方在上/左，被调用方在下/右 | 连线交叉多 | 三.3 |
| C-LAYOUT-010 | 同层组件按调用顺序从左到右排列 | 连线混乱 | 三.3 |
| C-LAYOUT-011 | 横切关注点（消息队列、配置中心、监控）放右侧独立列 | 布局混乱 | 三.3 |

### 图标约束 (C-ICON-xxx)

| ID | 约束 | 违反后果 | 来源章节 |
|----|------|---------|---------|
| C-ICON-001 | 阿里云 shape name 必须用全小写下划线格式 | 图标空白方块 | 四.1 |
| C-ICON-002 | 图标必须有 `fillColor` 属性 | 只显示空轮廓 | 四.1 |
| C-ICON-003 | 图标必须有 `strokeColor=none` | 边框干扰 | 四.1 |
| C-ICON-004 | 图标必须有 `verticalLabelPosition=bottom` | 标签与图标重叠 | 四.1 |
| C-ICON-005 | 图标必须有 `verticalAlign=top` | 标签位置错误 | 四.1 |
| C-ICON-006 | 图标必须有 `spacingTop=6-8` | 标签紧贴图标 | 四.1 |
| C-ICON-007 | 图标必须有 `aspect=fixed` | 图标变形 | 四.1 |
| C-ICON-008 | Kubernetes 图标通过 `prIcon` 选类型 | 类型错误 | 四.2 |

### 连线约束 (C-EDGE-xxx)

| ID | 约束 | 违反后果 | 来源章节 |
|----|------|---------|---------|
| C-EDGE-001 | 连线方向尽量上→下或左→右，避免回头线 | 可读性差 | 六.2 |
| C-EDGE-002 | 减少连线交叉（交叉多说明组件位置需调整） | 视觉混乱 | 六.2 |
| C-EDGE-003 | 标签仅用于关键流，不是每条线都需要标签 | 信息过载 | 六.2 |
| C-EDGE-004 | 标签颜色与线色一致 | 视觉不一致 | 六.2 |
| C-EDGE-005 | 连线 source/target ID 必须匹配实际 cell ID | 连线丢失 | 六.1 |

### Z-order 约束 (C-ZORDER-xxx)

| ID | 约束 | 违反后果 | 来源章节 |
|----|------|---------|---------|
| C-ZORDER-001 | XML 中先写的元素在底层 | 层级错误 | 七 |
| C-ZORDER-002 | 严格顺序：层背景容器 → 嵌套框 → 标签文字 → 组件/图标/节点 → 连接线 | 内容被遮挡 | 七 |

### 配色约束 (C-COLOR-xxx)

| ID | 约束 | 违反后果 | 来源章节 |
|----|------|---------|---------|
| C-COLOR-001 | 按组件职责分类选色，同类用同色系 | 视觉混乱 | 五.5 |
| C-COLOR-002 | 一张图最多 4-5 种底色 | 色彩过载 | 五.5 |
