# 视觉系统与风格选择

> 新建图时需有意识地选择视觉风格，避免陷入"默认蓝+圆角框"的同质化。

---

## 三种推荐视觉系统

### 1. Blueprint（蓝图风格）— 架构图首选

**适用**：云部署架构图、功能架构图、系统边界图

**特征**：冷色系（蓝、灰、白）、清晰分层、边框略强、容器结构明显

**配色**：
```
主色：#2196F3（蓝）  辅助：#90CAF9  背景：#FAFAFA  边框：#1976D2
```

**节点样式**：
```
rounded=1;whiteSpace=wrap;html=1;
fillColor=#E3F2FD;strokeColor=#1976D2;strokeWidth=2;
fontSize=14;fontColor=#0D47A1;
```

**避免**：装饰性渐变、图标大小不一致、过多颜色

---

### 2. Operations Board（运营看板风格）— 流程图首选

**适用**：业务流程图、审批流、工作流

**特征**：强方向感、主流程高对比、决策节点清晰

**配色**：
```
主流程：#43A047（绿）  决策：#FF9800（橙）  异常：#F44336（红）
```

**节点样式**：
```
普通节点：fillColor=#E8F5E9;strokeColor=#43A047;strokeWidth=2
决策节点：fillColor=#FFF3E0;strokeColor=#FF9800;strokeWidth=2
异常节点：fillColor=#FFEBEE;strokeColor=#F44336;strokeWidth=2
```

**避免**：每个节点做成同一种卡片、分支颜色乱用

---

### 3. Editorial Minimal（极简风格）— 组件图首选

**适用**：组件图、说明型技术图

**特征**：极少颜色、依靠线型和留白表达、重视对齐

**配色**：
```
节点：#FFFFFF  边框：#9E9E9E  文字：#212121  强调：#1976D2（仅标题）
```

**节点样式**：
```
rounded=0;whiteSpace=wrap;html=1;
fillColor=#FFFFFF;strokeColor=#9E9E9E;strokeWidth=1;
fontSize=14;fontColor=#212121;
```

**避免**：用大面积背景色替代结构设计

---

## 风格选择决策

| 图类型 | 推荐风格 |
|--------|---------|
| 云部署架构图 | Blueprint |
| 功能架构图 | Blueprint 或 Editorial Minimal |
| 业务流程图 | Operations Board |
| 组件图 | Editorial Minimal |

---

## 去同质化手段

从以下维度选择 **2-3 个** 做差异化：

| 维度 | 变化方式 |
|------|---------|
| 容器形状 | 圆角程度、直角 |
| 线条粗细 | 主线 2-3px、辅线 1px |
| 配色关系 | 冷色系 / 暖色系 / 中性 |
| 标题层级 | 字号差异、加粗/常规 |
| 留白节奏 | 紧凑 / 宽松 |

**注意**：不要所有维度同时变化，否则变成风格拼盘。