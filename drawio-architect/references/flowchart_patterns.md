# 业务流程图 / 数据流图专用模式

本文件在绘制业务流程图、审批流程、数据流图、泳道图时读取。

## 流程图 vs 架构图

| 维度 | 流程图 | 架构图 |
|------|--------|--------|
| 关注点 | 事情怎么做（步骤/顺序） | 系统长什么样（结构/组成） |
| 核心元素 | 活动、判断、开始/结束 | 组件、层、容器 |
| 连线含义 | 流转顺序 | 调用/依赖 |
| 方向 | 通常上→下或左→右单向 | 多方向 |
| 分区 | 按角色（泳道） | 按层次/职责 |

## 标准流程图形状

### 开始 / 结束节点（圆角矩形或椭圆）

```xml
<mxCell id="start" value="开始"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#C8E6C9;strokeColor=#43A047;fontColor=#1B5E20;fontSize=11;fontStyle=1;arcSize=50;"
  vertex="1" parent="1">
  <mxGeometry x="300" y="20" width="120" height="40" as="geometry"/>
</mxCell>

<mxCell id="end" value="结束"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFCDD2;strokeColor=#E53935;fontColor=#B71C1C;fontSize=11;fontStyle=1;arcSize=50;"
  vertex="1" parent="1">
  <mxGeometry x="300" y="600" width="120" height="40" as="geometry"/>
</mxCell>
```

`arcSize=50` 让矩形变成胶囊形（类似椭圆），这是开始/结束的标准样式。

### 活动节点（圆角矩形）

```xml
<mxCell id="step1" value="提交申请"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;fontColor=#0D47A1;fontSize=10;arcSize=8;"
  vertex="1" parent="1">
  <mxGeometry x="280" y="100" width="160" height="50" as="geometry"/>
</mxCell>
```

### 判断节点（菱形）

```xml
<mxCell id="check1" value="金额 &gt; 5000?"
  style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFF9C4;strokeColor=#F9A825;fontColor=#F57F17;fontSize=10;"
  vertex="1" parent="1">
  <mxGeometry x="290" y="200" width="140" height="80" as="geometry"/>
</mxCell>
```

注意：菱形中的 `>` 要转义为 `&gt;`。

### 条件分支连线

```xml
<!-- 是 — 向下 -->
<mxCell value="是" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#43A047;strokeWidth=2;fontSize=9;fontColor=#43A047;fontStyle=1;"
  edge="1" parent="1" source="check1" target="step_approve">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 否 — 向右 -->
<mxCell value="否" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#E53935;strokeWidth=2;fontSize=9;fontColor=#E53935;fontStyle=1;"
  edge="1" parent="1" source="check1" target="step_reject">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

建议："是"用绿色向下/向前，"否"用红色向右/向旁。

### 并行网关

用粗边框菱形 + 加号表示：

```xml
<!-- 并行开始（fork） -->
<mxCell id="fork1" value="+"
  style="rhombus;whiteSpace=wrap;html=1;fillColor=#E8EAF6;strokeColor=#3949AB;strokeWidth=3;fontSize=16;fontStyle=1;fontColor=#3949AB;"
  vertex="1" parent="1">
  <mxGeometry x="320" y="300" width="40" height="40" as="geometry"/>
</mxCell>

<!-- 并行结束（join） -->
<mxCell id="join1" value="+"
  style="rhombus;whiteSpace=wrap;html=1;fillColor=#E8EAF6;strokeColor=#3949AB;strokeWidth=3;fontSize=16;fontStyle=1;fontColor=#3949AB;"
  vertex="1" parent="1">
  <mxGeometry x="320" y="500" width="40" height="40" as="geometry"/>
</mxCell>
```

## 泳道模式

按角色/部门划分为横向或纵向泳道。

### 纵向泳道（最常用）

每个角色一列，流程从上到下：

```xml
<!-- 泳道容器 -->
<mxCell id="lane_user" value="用户"
  style="swimlane;startSize=24;horizontal=1;fillColor=#E3F2FD;strokeColor=#1976D2;fontColor=#0D47A1;fontSize=11;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="20" y="20" width="250" height="600" as="geometry"/>
</mxCell>

<mxCell id="lane_system" value="系统"
  style="swimlane;startSize=24;horizontal=1;fillColor=#E8F5E9;strokeColor=#43A047;fontColor=#1B5E20;fontSize=11;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="280" y="20" width="250" height="600" as="geometry"/>
</mxCell>

<mxCell id="lane_admin" value="管理员"
  style="swimlane;startSize=24;horizontal=1;fillColor=#FFF3E0;strokeColor=#E65100;fontColor=#BF360C;fontSize=11;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="540" y="20" width="250" height="600" as="geometry"/>
</mxCell>
```

### 横向泳道

每个角色一行，流程从左到右：

```xml
<mxCell id="lane_user" value="用户"
  style="swimlane;startSize=24;horizontal=0;fillColor=#E3F2FD;strokeColor=#1976D2;fontColor=#0D47A1;fontSize=11;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="20" y="20" width="800" height="150" as="geometry"/>
</mxCell>
```

注意 `horizontal=0` 表示横向泳道（标题在左侧竖排）。

## 流程图布局规则

### 纵向流程（推荐）

- 开始节点居中最上方
- 活动节点纵向排列，间距 30-50px
- 菱形判断节点：主路径（是）向下，异常路径（否）向右
- 结束节点居中最下方
- 所有节点水平居中对齐

### 分支处理

```
        [判断]
       ↙     ↘
    [是路径]  [否路径]
       ↘     ↙
       [汇合点]
```

- 分支后尽快汇合，避免长距离平行
- 并行分支间距 200-300px

### 循环/回退

用带标签的回头箭头，标注循环条件：

```xml
<mxCell value="修改后重新提交" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#FF9800;strokeWidth=1.5;fontSize=8;fontColor=#FF9800;dashed=1;"
  edge="1" parent="1" source="reject" target="submit">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

回退线用虚线+橙色，区别于正向流程。

## 配色建议

| 元素 | fillColor | strokeColor |
|------|-----------|-------------|
| 开始 | `#C8E6C9` | `#43A047` |
| 结束 | `#FFCDD2` | `#E53935` |
| 普通活动 | `#E3F2FD` | `#1976D2` |
| 重要活动 | `#FFF9C4` | `#F9A825` |
| 判断 | `#FFF9C4` | `#F9A825` |
| 并行网关 | `#E8EAF6` | `#3949AB` |
| 子流程 | `#F3E5F5` | `#7B1FA2` |

## 数据流图补充

数据流图和业务流程图类似，但增加：

### 数据存储（双横线矩形）

```xml
<mxCell id="db_orders" value="订单数据库"
  style="shape=partialRectangle;whiteSpace=wrap;html=1;top=0;bottom=0;fillColor=#F5F5F5;strokeColor=#9E9E9E;fontColor=#333;fontSize=10;align=center;"
  vertex="1" parent="1">
  <mxGeometry x="400" y="300" width="140" height="40" as="geometry"/>
</mxCell>
```

### 外部实体（矩形，加粗边框）

```xml
<mxCell id="ext_user" value="外部用户"
  style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ECEFF1;strokeColor=#546E7A;strokeWidth=2.5;fontColor=#37474F;fontSize=11;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="20" y="200" width="120" height="50" as="geometry"/>
</mxCell>
```

### 处理过程（圆角矩形 + 编号）

```xml
<mxCell id="proc1" value="&lt;b&gt;1.0&lt;/b&gt;&lt;br&gt;订单处理"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;fontColor=#333;fontSize=10;arcSize=50;"
  vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="120" height="60" as="geometry"/>
</mxCell>
```
