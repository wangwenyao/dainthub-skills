# 页面设计示例 — 设计决策说明

各类典型 SaaS 页面的设计决策说明，重点解释"为什么这样设计"。

---

## 数据列表页

**设计决策：**

```
信息密度：紧凑型。行高 44px（py-3 + 14px 字号），每屏可展示 15–20 条
操作位置：行内操作 hover 后出现，批量操作勾选后浮出顶部操作栏
筛选位置：表格上方，URL 参数驱动（刷新不丢失筛选状态）
分页方式：传统分页（非无限滚动）——B端用户需要知道总量和当前位置
空状态：区分"暂无数据（引导创建）"和"筛选无结果（引导清除筛选）"
```

**视觉规范：**
```
表头：text-xs font-medium foreground-muted uppercase tracking-wider
行内容：text-sm foreground（主字段）+ foreground-muted（次字段）
边框：仅水平方向 border-b，无垂直边框（减少格子感）
hover：bg-muted/40（非常轻，不喧宾夺主）
选中：bg-brand-50（亮色）/ bg-brand-950（暗色）
```

---

## 详情/编辑页

**设计决策：**

```
布局：左侧主内容（2/3宽）+ 右侧元数据面板（1/3宽）
编辑模式：行内编辑（点击字段直接编辑），而非"进入编辑模式"
保存方式：字段级自动保存（blur 时触发），Toast 确认
危险操作：放在页面底部或右侧面板底部，用分割线隔开
面包屑：固定在页面顶部，层级 ≤ 3 级
```

**字段展示规范：**
```
label：text-sm font-medium foreground-muted，字段上方
value：text-sm foreground
空值："-"（em dash）替代空字符串，foreground-subtle 色
只读字段：无边框背景，直接展示文字
编辑中字段：input 样式，border-brand-500 聚焦态
```

---

## 设置页

**设计决策：**

```
导航：左侧二级导航（Tabs 形式），不用顶部 Tabs（字段多时容易溢出）
分组：每个 Section 用 Card 包裹，Card 之间 space-y-6
保存：分 Section 独立保存（不要全页面一个保存按钮）
危险区：独立放在最后一个 Section，红色边框 Card 强调
账号注销：最危险，放最后，需要输入确认文字
```

**Section 结构模板：**
```
Card
  CardHeader
    CardTitle    text-base font-semibold
    CardDescription  text-sm foreground-muted（说明这个 section 的用途）
  CardContent
    [表单字段]
  CardFooter（border-t）
    [取消按钮（ghost）] [保存按钮（default）]
```

---

## 仪表盘

**设计决策：**

```
指标卡：4 列网格（宽屏），2 列（平板），1 列（手机）
指标卡内容：数字大（text-2xl font-bold）+ 环比变化（text-sm + 颜色）
图表选型：趋势用折线图，占比用环形图（非饼图），对比用柱状图
图表交互：hover tooltip，不做点击下钻（跳转到对应列表页）
刷新策略：自动刷新间隔 30s，顶部显示"最后更新时间"
空数据图表：显示空状态提示，不显示空坐标轴
```

**卡片规范：**
```
指标卡：p-6，min-h-[120px]
图表卡：p-6，标题 text-base font-semibold + 副标题 text-sm foreground-muted
说明文字：图表下方 text-xs foreground-subtle，非图例（图例放图表内）
```

---

## 认证页（登录/注册）

**设计决策：**

```
布局：居中卡片（max-w-sm），垂直居中，背景 background-subtle
品牌：Logo + 产品名，不放营销文字（B端用户知道自己为什么来）
表单：邮箱 + 密码，密码可切换明文
错误反馈：表单级错误在按钮上方（红色提示框），字段级错误在字段下方
第三方登录：SSO 按钮放在表单上方（B端用户常用企业 SSO）
底部链接：忘记密码、注册入口用 text-sm text-brand-500
```

**安全性视觉信号：**
```
HTTPS 锁标志：页脚小字提示"安全连接"
密码强度：注册时实时显示强度条（4段：弱/中/强/极强）
登录失败：≥3次后显示"如需帮助请联系管理员"（B端通常企业账号）
```
