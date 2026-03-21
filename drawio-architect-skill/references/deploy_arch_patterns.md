# 云部署架构图专用模式

本文件在绘制云部署架构图、K8s 集群拓扑图、基础设施部署图时读取。

## 典型层次结构

部署架构图通常自上而下按调用链分层：

```
标题栏
用户接入层      — 客户端、浏览器、小程序、第三方系统
网络/安全层     — CDN、WAF、负载均衡、API 网关
应用服务层      — 微服务、AI Agent、前端应用（通常在 K8s 内）
数据存储层      — 数据库、缓存、向量库、对象存储、搜索引擎
监控/运维层     — Prometheus、Grafana、日志、告警（可作为侧边栏）
底部注释        — VPC/网络说明
```

不是每个图都有所有层，按实际架构裁剪。

## 泳道分层模式

每层 = 带色背景矩形 + 左上角标签：

```xml
<!-- 层背景 -->
<mxCell id="layer_bg" value=""
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#DAEDF7;strokeColor=#2196F3;strokeWidth=2;arcSize=3;"
  vertex="1" parent="1">
  <mxGeometry x="20" y="60" width="1260" height="130" as="geometry"/>
</mxCell>

<!-- 层标题 -->
<mxCell id="layer_label" value="接入层"
  style="text;html=1;fontSize=12;fontStyle=1;fontColor=#0D47A1;align=left;verticalAlign=top;"
  vertex="1" parent="1">
  <mxGeometry x="36" y="64" width="150" height="22" as="geometry"/>
</mxCell>
```

## K8s 集群边界

用虚线框表示 K8s 集群范围，嵌套在平台层内：

```xml
<mxCell id="k8s_outline" value=""
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EBF3FF;strokeColor=#326CE5;strokeWidth=2;dashed=1;dashPattern=12 5;arcSize=2;"
  vertex="1" parent="1">
  <mxGeometry x="30" y="348" width="1240" height="340" as="geometry"/>
</mxCell>
<mxCell id="k8s_label" value="☸ Kubernetes 集群"
  style="text;html=1;fontSize=11;fontStyle=1;fontColor=#326CE5;align=left;verticalAlign=top;"
  vertex="1" parent="1">
  <mxGeometry x="42" y="352" width="300" height="20" as="geometry"/>
</mxCell>
```

## 左右分区布局

横切关注点（消息队列、配置中心、监控）放右侧独立列：

```
┌─── 主区（~78% 宽度）──────────────────┬── 边栏（~18%）──┐
│ 第一排：网关 / 认证                    │  消息队列       │
│ 第二排：核心服务                       │  配置中心       │
│ 第三排：基础服务                       │  其他           │
└────────────────────────────────────────┴────────────────┘
```

## 独立图标 + 副标题模式

数据存储层常用。图标在上，主标签紧跟，副标题独立 text cell：

```xml
<mxCell id="mysql" value="MySQL 8.0"
  style="...shape=mxgraph.alibaba_cloud.mysql;verticalLabelPosition=bottom;verticalAlign=top;spacingTop=6;..."
  vertex="1" parent="1">
  <mxGeometry x="188" y="685" width="45" height="45" as="geometry"/>
</mxCell>
<mxCell id="mysql_sub" value="主从复制 / 业务库"
  style="text;html=1;align=center;fontSize=7;fontColor=#555;"
  vertex="1" parent="1">
  <mxGeometry x="158" y="750" width="105" height="12" as="geometry"/>
</mxCell>
```

副标题 Y ≈ 图标Y + 图标高 + spacingTop + 主标签高 + 4px。

## K8s 图标在服务卡片中的用法

用 `fillColor` 变色区分技术栈，`prIcon` 选语义最近的 K8s 资源：

| 组件类型 | prIcon | fillColor 参考 |
|----------|--------|----------------|
| 有副本微服务 | `deploy` | 按技术栈选色 |
| AI Agent | `pod` | `#FF6600` 或 `#1890FF` |
| API Gateway | `ing` | `#6DB33F`（Spring绿） |
| 配置中心 | `cm` | `#2875E2`（K8s蓝） |
| 限流/熔断 | `limits` | `#7986CB` |
| 有专用图标的（如 Kafka） | 优先用阿里云专用图标 | — |

## 连线颜色建议

| 流量类型 | 色值 |
|----------|------|
| 外部用户请求 | `#2196F3` |
| 负载均衡/路由 | `#FF9800` |
| AI/ML 管线 | `#FF5722` |
| 业务逻辑 | `#43A047` |
| 数据层调用 | `#7B1FA2` |
| CDN/静态资源（虚线） | `#90CAF9` |
