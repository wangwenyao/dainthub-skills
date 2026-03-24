# 功能架构图 / 系统架构图 / 技术架构图专用模式

本文件在绘制功能架构图、系统架构图、技术架构图、能力分层图时读取。

## 三种架构图的区别

| 维度 | 功能架构图 | 系统架构图 | 技术架构图 |
|------|-----------|-----------|-----------|
| 关注点 | 功能模块、能力分层 | 系统边界、子系统关系 | 技术选型、技术栈 |
| 主要元素 | 功能模块、子功能 | 系统、子系统、外部系统 | 技术组件、框架、中间件 |
| 图标使用 | 少，色块+文字 | 少，系统框为主 | 多，技术组件图标 |
| 连线含义 | 依赖关系 | 系统调用、数据流 | 技术集成、依赖 |

## 功能架构图 vs 部署架构图

| 维度 | 功能架构图 | 部署架构图 |
|------|-----------|-----------|
| 关注点 | 系统有哪些能力/功能 | 系统部署在哪些资源上 |
| 组件 | 功能模块、子系统 | 服务器、容器、数据库 |
| 图标 | 很少用，主要是色块+文字 | 大量云/K8s 图标 |
| 连线 | 较少，主要是依赖方向 | 较多，表示数据流 |
| 布局 | 嵌套矩形为主 | 泳道分层为主 |

## 典型层次结构

功能架构图通常按"前台—中台—后台"或"展示—业务—支撑"分层：

```
展示层 / 前台        — 面向用户的功能入口（Web、APP、小程序）
业务层 / 中台        — 核心业务能力（搜索、推荐、订单、支付）
能力层 / 支撑平台    — 通用能力（AI 平台、数据平台、消息平台）
基础层 / 后台        — 基础设施（存储、计算、网络、安全）
```

## 嵌套矩形模式

功能架构图的核心元素是**嵌套的矩形块**——大模块内含子模块：

```xml
<!-- 大模块（外层容器） -->
<mxCell id="search_module" value=""
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1565C0;strokeWidth=2;arcSize=3;"
  vertex="1" parent="1">
  <mxGeometry x="40" y="200" width="400" height="200" as="geometry"/>
</mxCell>

<!-- 模块标题 -->
<mxCell id="search_title" value="搜索服务"
  style="text;html=1;fontSize=13;fontStyle=1;fontColor=#1565C0;align=center;verticalAlign=top;"
  vertex="1" parent="1">
  <mxGeometry x="40" y="204" width="400" height="24" as="geometry"/>
</mxCell>

<!-- 子功能（内层卡片） -->
<mxCell id="full_text" value="全文检索"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#90CAF9;fontColor=#333;fontSize=10;arcSize=6;"
  vertex="1" parent="1">
  <mxGeometry x="55" y="240" width="110" height="40" as="geometry"/>
</mxCell>

<mxCell id="semantic" value="语义搜索"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#90CAF9;fontColor=#333;fontSize=10;arcSize=6;"
  vertex="1" parent="1">
  <mxGeometry x="180" y="240" width="110" height="40" as="geometry"/>
</mxCell>
```

### 嵌套层级

- **第一级**：大分区（展示层、业务层等）— 用深色边框、浅色背景
- **第二级**：功能模块 — 用中等色边框
- **第三级**：子功能 — 白色背景、浅色边框

推荐最多 3 层嵌套，超过会不清晰。

## 横向分区模式

功能架构图常按业务域横向分区：

```
┌──────────┬──────────┬──────────┬──────────┐
│  搜索域   │  商品域   │  用户域   │  订单域   │
│          │          │          │          │
│ 全文检索  │ 商品管理  │ 用户认证  │ 订单创建  │
│ 语义搜索  │ SKU 管理  │ 权限控制  │ 支付流程  │
│ AI 推荐   │ 库存管理  │ 用户画像  │ 物流跟踪  │
│          │          │          │          │
└──────────┴──────────┴──────────┴──────────┘
```

每个域用不同色系的外框区分。

## 系统边界框

用虚线框标示系统边界，区分"我们的系统"和"外部系统"：

```xml
<!-- 系统边界 -->
<mxCell id="sys_boundary" value=""
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#666;strokeWidth=2;dashed=1;dashPattern=8 4;arcSize=2;"
  vertex="1" parent="1">
  <mxGeometry x="20" y="100" width="800" height="500" as="geometry"/>
</mxCell>
<mxCell id="sys_label" value="优宁维商城系统"
  style="text;html=1;fontSize=11;fontStyle=3;fontColor=#666;align=left;verticalAlign=top;"
  vertex="1" parent="1">
  <mxGeometry x="30" y="104" width="200" height="20" as="geometry"/>
</mxCell>

<!-- 外部系统 -->
<mxCell id="ext_pay" value="第三方支付"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#9E9E9E;fontColor=#666;fontSize=10;arcSize=6;dashed=1;"
  vertex="1" parent="1">
  <mxGeometry x="900" y="200" width="140" height="50" as="geometry"/>
</mxCell>
```

外部系统用灰色/虚线边框，与内部系统形成视觉区分。

## 接口标注

系统间的接口在连线上标注协议：

```xml
<mxCell value="REST API" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#666;strokeWidth=1.5;fontSize=8;fontColor=#999;fontStyle=2;" .../>
```

常用标注：`REST API`、`gRPC`、`WebSocket`、`MQ`、`SDK`、`HTTP/HTTPS`。

## 配色建议

功能架构图一般不用鲜艳色，偏柔和：

| 层级 | fillColor | strokeColor |
|------|-----------|-------------|
| 展示层/前台 | `#E3F2FD` | `#1565C0` |
| 业务层/中台 | `#E8F5E9` | `#2E7D32` |
| 能力层/平台 | `#FFF3E0` | `#E65100` |
| 基础层/后台 | `#F3E5F5` | `#6A1B9A` |
| 子功能卡片 | `#FFFFFF` | 父模块浅色版 |
| 外部系统 | `#F5F5F5` | `#9E9E9E`（虚线） |

---

## 技术架构图模式

技术架构图展示技术选型、技术栈和技术组件之间的关系。

### 典型层次结构

```
前端技术栈     — Vue/React、构建工具、UI 框架
后端技术栈     — Spring Boot、微服务框架、ORM
中间件层       — 消息队列、缓存、搜索引擎
数据存储层     — 关系数据库、NoSQL、对象存储
基础设施层     — 容器平台、CI/CD、监控告警
```

### 技术栈卡片模式

每个技术组件用带图标/标签的卡片表示：

```xml
<!-- 技术栈容器 -->
<mxCell id="frontend_layer" value=""
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;strokeWidth=2;arcSize=3;"
  vertex="1" parent="1">
  <mxGeometry x="40" y="60" width="1120" height="120" as="geometry"/>
</mxCell>

<!-- 层标题 -->
<mxCell id="frontend_title" value="前端技术栈"
  style="text;html=1;fontSize=14;fontStyle=1;fontColor=#0D47A1;align=left;verticalAlign=top;"
  vertex="1" parent="1">
  <mxGeometry x="56" y="68" width="150" height="24" as="geometry"/>
</mxCell>

<!-- 技术卡片 -->
<mxCell id="vue_card" value="&lt;b&gt;Vue 3&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#888&quot; style=&quot;font-size:9px&quot;&gt;核心框架&lt;/font&gt;"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#42B883;strokeWidth=2;fontSize=11;arcSize=8;align=center;"
  vertex="1" parent="1">
  <mxGeometry x="60" y="100" width="140" height="60" as="geometry"/>
</mxCell>
```

### 技术卡片配色（按技术领域）

| 技术领域 | 边框色 | 示例 |
|---------|--------|------|
| 前端框架 | `#42B883` (Vue绿) / `#61DAFB` (React蓝) | Vue, React, Angular |
| 后端框架 | `#6DB33F` (Spring绿) / `#339933` (Node绿) | Spring Boot, Express |
| 数据库 | `#00758F` (MySQL) / `#336791` (PostgreSQL) | MySQL, PostgreSQL |
| 缓存 | `#DC382D` (Redis红) | Redis, Memcached |
| 消息队列 | `#231F20` (Kafka黑) / `#FF6600` (橙) | Kafka, RabbitMQ |
| 容器/K8s | `#326CE5` (K8s蓝) | Kubernetes, Docker |
| 监控 | `#E6522C` (Prometheus橙) | Prometheus, Grafana |

### 技术栈连线

技术组件之间的连线表示集成/依赖关系：

```xml
<!-- 技术依赖连线 -->
<mxCell value="REST API" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#666;strokeWidth=1.5;dashed=1;fontSize=8;fontColor=#666;"
  edge="1" parent="1" source="vue_card" target="spring_card">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 版本标注

在卡片或标签中标注技术版本：

```xml
<mxCell value="&lt;b&gt;MySQL 8.0&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#888&quot; style=&quot;font-size:9px&quot;&gt;主从复制&lt;/font&gt;" .../>
```

### 技术架构图布局原则

1. **自上而下**：前端 → 后端 → 中间件 → 数据 → 基础设施
2. **同层等高**：同一技术层的卡片高度统一
3. **相关就近**：有集成关系的技术组件就近放置
4. **开源标注**：可用小图标或标签区分开源/商业软件
