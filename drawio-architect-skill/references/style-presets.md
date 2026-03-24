# 样式预设模板

> 可直接复用的 style 字符串，减少拼写错误。

---

## 容器样式

```xml
<!-- 层背景（冷色） -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#DAEDF7;strokeColor=#2196F3;strokeWidth=2;arcSize=3;"

<!-- 层背景（暖色） -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FBE9E7;strokeColor=#FF5722;strokeWidth=2;arcSize=3;"

<!-- 层背景（中性） -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#43A047;strokeWidth=2;arcSize=3;"

<!-- K8s/容器边界 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EBF3FF;strokeColor=#326CE5;strokeWidth=2;arcSize=3;"

<!-- 虚线嵌套框 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#9E9E9E;strokeWidth=1;dashed=1;dashPattern=8 8;"
```

---

## 卡片样式

```xml
<!-- 服务卡片（白底+彩色边框） -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#FF6600;strokeWidth=2;fontColor=#333;fontSize=11;arcSize=8;align=center;"

<!-- 简单标签 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#9E9E9E;strokeWidth=1;fontColor=#333;fontSize=11;arcSize=4;align=center;"
```

---

## 文字样式

```xml
<!-- 层标题 -->
style="text;html=1;fontSize=16;fontStyle=1;fontColor=#0D47A1;align=left;verticalAlign=top;"

<!-- 层副标题 -->
style="text;html=1;fontSize=12;fontColor=#666;align=left;verticalAlign=top;"
```

---

## 图标样式

```xml
<!-- 阿里云图标模板（替换 shape 和 fillColor） -->
style="points=[];aspect=fixed;html=1;align=center;shadow=0;dashed=0;fillColor=#FF6A00;strokeColor=none;shape=mxgraph.alibaba_cloud.{shape_name};verticalLabelPosition=bottom;verticalAlign=top;fontSize=9;fontStyle=1;spacingTop=8;"

<!-- K8s 图标模板 -->
style="points=[];aspect=fixed;html=1;align=center;shadow=0;dashed=0;shape=mxgraph.kubernetes.icon2;prIcon={type};fillColor=#326CE5;strokeColor=#ffffff;verticalLabelPosition=bottom;verticalAlign=top;fontSize=9;fontStyle=1;spacingTop=8;"
```

---

## 连线样式

```xml
<!-- 基本连线 -->
style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#2196F3;strokeWidth=2;"

<!-- 带动画 -->
style="edgeStyle=orthogonalEdgeStyle;rounded=1;flowAnimation=1;strokeColor=#2196F3;strokeWidth=2;"

<!-- 主链路 -->
style="edgeStyle=orthogonalEdgeStyle;rounded=1;flowAnimation=1;strokeColor=#FF5722;strokeWidth=2.5;"

<!-- 虚线（可选） -->
style="edgeStyle=orthogonalEdgeStyle;rounded=1;dashed=1;dashPattern=5 3;strokeColor=#90CAF9;strokeWidth=1.5;"

<!-- 带标签 -->
style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#2196F3;strokeWidth=2;fontSize=9;fontColor=#2196F3;"
```

---

## 流程图样式

```xml
<!-- 开始/结束 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#C8E6C9;strokeColor=#43A047;fontSize=11;fontStyle=1;arcSize=50;"

<!-- 活动节点 -->
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;fontSize=10;arcSize=8;"

<!-- 判断节点 -->
style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFF9C4;strokeColor=#F9A825;fontSize=10;"

<!-- 是分支 -->
style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#43A047;strokeWidth=2;fontSize=9;fontColor=#43A047;"

<!-- 否分支 -->
style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#E53935;strokeWidth=2;fontSize=9;fontColor=#E53935;"
```

---

## 使用原则

1. 同类元素使用相同样式字符串
2. 只在颜色上区分，不在结构上变化
3. 从预设色板选色，避免随意取色