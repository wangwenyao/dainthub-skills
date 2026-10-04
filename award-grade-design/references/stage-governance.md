# Stage Governance

## 目的

防止 Agent 在一个小任务中擅自扩大职责范围。

## Stage 权限

每个 Stage 的默认写入权限由 `routing/scope-router.yaml` **唯一**定义：

```text
read-only         只能产出报告
artifact-only     只能产出设计资产
design-artifacts  可以写设计资产，不写业务代码
code              可以改业务代码
patch             可以做局部补丁
```

本文件不再重复权限表——重复的权限声明会漂移，而权限漂移的后果是越权修改。
需要查看某个 Stage 当前允许做什么，读 `routing/scope-router.yaml`。

## 越界规则

需要越界时：

1. 停止静默修改。
2. 记录 dependency / deviation。
3. 说明为什么需要。
4. 等待当前 Scope 允许，或换 Stage。

## 关键原则

```text
Visual QA 不应重做设计。
Implementation 不应偷偷改变 Design Direction。
Component 不应擅自改变 Product IA。
Optimization 不应演变成 broad redesign。
```
