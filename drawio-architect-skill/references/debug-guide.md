# 调试指南

> draw.io XML 常见问题诊断与修复，由 SKILL.md 按需加载。

---

## 一、XML 解析错误

### 1.1 Could not add object mxGeometry

| 症状 | 原因 | 修复 |
|------|------|------|
| 打开文件报错 `Could not add object mxGeometry` | `<mxGeometry>` 缺少 `as="geometry"` | 给所有 mxGeometry 加上该属性 |

```xml
<!-- ❌ 错误 -->
<mxGeometry x="100" y="200" width="50" height="50"/>

<!-- ✅ 正确 -->
<mxGeometry x="100" y="200" width="50" height="50" as="geometry"/>
```

### 1.2 xmlParseEntityRef: no name

| 症状 | 原因 | 修复 |
|------|------|------|
| XML 解析失败 | `value` 中 `&` 未转义 | 改为 `&amp;` |

```xml
<!-- ❌ 错误 -->
<mxCell value="A & B" .../>

<!-- ✅ 正确 -->
<mxCell value="A &amp; B" .../>
```

### 1.3 特殊字符转义表

| 字符 | 转义 | 示例 |
|------|------|------|
| `&` | `&amp;` | `A &amp; B` |
| `<` | `&lt;` | `&lt;b&gt;标题&lt;/b&gt;` |
| `>` | `&gt;` | `x &gt; 10` |
| `"` | `&quot;` | `style=&quot;color:red&quot;` |

---

## 二、图标显示问题

### 2.1 图标显示为空白方块

| 症状 | 原因 | 修复 |
|------|------|------|
| 云图标显示为空白方块 | shape name 格式错误 | 使用全小写下划线格式 |

```xml
<!-- ❌ 错误 -->
shape=mxgraph.alibaba_cloud.Redis KVStore
shape=mxgraph.alicloud.redis

<!-- ✅ 正确 -->
shape=mxgraph.alibaba_cloud.redis_kvstore
```

### 2.2 图标只显示空轮廓

| 症状 | 原因 | 修复 |
|------|------|------|
| 图标只有边框，无填充色 | 缺少 fillColor 属性 | 添加 `fillColor=#FF6A00;strokeColor=none;` |

```xml
<!-- ✅ 完整属性 -->
<mxCell style="shape=mxgraph.alibaba_cloud.redis_kvstore;
       fillColor=#FF6A00;strokeColor=none;
       verticalLabelPosition=bottom;verticalAlign=top;
       spacingTop=8;aspect=fixed;points=[];html=1;align=center;shadow=0;dashed=0;"
  .../>
```

### 2.3 标签与图标重叠

| 症状 | 原因 | 修复 |
|------|------|------|
| 文字显示在图标内部 | 缺少 verticalLabelPosition | 添加 `verticalLabelPosition=bottom;verticalAlign=top;spacingTop=6-8;` |

---

## 三、布局问题

### 3.1 内容被背景遮挡

| 症状 | 原因 | 修复 |
|------|------|------|
| 卡片/图标被层背景遮盖 | Z-order 错误 | XML 中先写背景，再写内容 |

```xml
<!-- ✅ 正确顺序 -->
<mxCell id="layer_bg" .../>     <!-- 1. 背景 -->
<mxCell id="k8s_outline" .../>  <!-- 2. 嵌套框 -->
<mxCell id="label" .../>        <!-- 3. 标签 -->
<mxCell id="service" .../>      <!-- 4. 组件 -->
<mxCell id="edge" .../>         <!-- 5. 连线 -->
```

### 3.2 同排组件不对称

| 症状 | 原因 | 修复 |
|------|------|------|
| 同一行组件宽高不一致 | 手动硬编码宽度 | 使用等距公式计算 |

```
n 个组件，容器宽度 W，间距 gap
组件宽度 w = (W - (n+1) × gap) / n
第 i 个 x = 容器左边 + gap + i × (w + gap)
```

### 3.3 连线大量交叉

| 症状 | 原因 | 修复 |
|------|------|------|
| 连线乱成一团 | 组件位置不合理 | 按依赖关系重排：调用方在上/左，被调用方在下/右 |

---

## 四、连线问题

### 4.1 连线丢失

| 症状 | 原因 | 修复 |
|------|------|------|
| 连线不显示 | source/target ID 不存在 | 检查 ID 是否匹配实际 cell ID |

```xml
<!-- 确保 source="a" 和 target="b" 对应的 cell 存在 -->
<mxCell id="a" .../>
<mxCell id="b" .../>
<mxCell id="edge" source="a" target="b" .../>
```

### 4.2 连线样式不生效

| 症状 | 原因 | 修复 |
|------|------|------|
| 连线无箭头 | 缺少 edge="1" | 添加 `edge="1" parent="1"` |

---

## 五、HTML 嵌套问题

### 5.1 HTML 标签不渲染

| 症状 | 原因 | 修复 |
|------|------|------|
| `<b>标题</b>` 直接显示原文 | 缺少 html=1 | 在 style 中添加 `html=1` |

```xml
<!-- ✅ 正确 -->
<mxCell value="&lt;b&gt;标题&lt;/b&gt;"
        style="rounded=1;whiteSpace=wrap;html=1;..." .../>
```

### 5.2 HTML 样式不生效

| 症状 | 原因 | 修复 |
|------|------|------|
| style 属性无效 | HTML 属性未转义 | `"` 改为 `&quot;` |

```xml
<!-- ✅ 正确 -->
value="&lt;font color=&quot;#888&quot; style=&quot;font-size:8px&quot;&gt;描述&lt;/font&gt;"
```

---

## 六、性能问题

### 6.1 文件打开慢

| 症状 | 原因 | 修复 |
|------|------|------|
| 大文件打开卡顿 | 元素过多（>500个） | 拆分为多个 diagram |

### 6.2 导出图片失败

| 症状 | 原因 | 修复 |
|------|------|------|
| 导出 PNG 空白 | 页面尺寸设置错误 | 检查 `pageWidth`/`pageHeight` 是否覆盖内容 |

---

## 七、快速诊断清单

```
□ 每个 <mxGeometry> 有 as="geometry"
□ 所有 & 已转义为 &amp;
□ 云图标 shape name 用小写下划线
□ 图标有 fillColor + strokeColor=none
□ 连线 source/target ID 存在
□ Z-order 正确（背景在内容之前）
□ HTML 内容有 html=1
□ 同排组件宽高一致
```

---

## 八、约束索引

| 错误类型 | 相关约束 |
|---------|---------|
| mxGeometry 错误 | C-XML-001 |
| XML 解析错误 | C-XML-002 ~ C-XML-007 |
| 图标空白方块 | C-ICON-001 |
| 图标空轮廓 | C-ICON-002, C-ICON-003 |
| 标签重叠 | C-ICON-004 ~ C-ICON-006 |
| 内容被遮挡 | C-ZORDER-001, C-ZORDER-002 |
| 布局不对称 | C-LAYOUT-001 ~ C-LAYOUT-004 |
| 连线交叉 | C-LAYOUT-009 ~ C-LAYOUT-011, C-EDGE-001 |