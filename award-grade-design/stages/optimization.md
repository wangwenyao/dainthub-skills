# Stage: optimization — 局部优化

## 目的

在现有设计已基本成立的前提下，只寻找少量高价值局部优化。

## 典型问题

```text
“再高级一点”
“再精致一点”
“提升 10% 品质”
“只优化首屏”
```

## 方法

1. 先找 Top 3 最高收益问题。
2. 优先处理层级、密度、对齐、状态和品牌识别；视觉通道不可用时，Top 3 依据上游审计
   证据选取，浏览器可用时辅以程序化指标（对齐与间距离群、Token 异常），感知类问题
   移交用户。
3. 不重复做完整 Design Direction。
4. 不在 P0/P1 尚未解决时添加装饰性 Motion。
5. 修改后立即进行局部 Visual QA；浏览器可用而视觉通道不可用时，按
   `references/visual-qa-protocol.md` 的「能力判定与运行模式」降级为程序化替代 QA
   （修改前后 computed style / DOM diff、console 复查），结果标注「视觉未复核」，截图
   归档移交用户；浏览器不可用时相关项标「未验证」。

## 输出

- 局部修改
- Before / After 说明
- 影响范围
- 是否产生 design drift

报告按 `templates/optimization-report.md` 的结构输出；第 5 步的局部 Visual QA 按
`templates/visual-qa-report.md` 的结构输出，与 visual-qa Stage 保持同一格式，
保证跨轮次可比。

## 停止条件

```text
Top 3 收益问题未选定 → 未完成：先完成问题排序
浏览器可用而修改后的局部 Visual QA 未执行 → 未完成：执行第 5 步后再评估
浏览器可用而视觉通道不可用 → 执行第 5 步的程序化替代 QA 并标注「视觉未复核」，
不得跳过或谎报
产生未记录的 design drift → 未完成：记录 deviation 并更新对应设计资产
局部修改完成、drift 为「无」或已记录、局部 QA 通过（视觉通道不可用时为程序化替代 QA
通过且已标注「视觉未复核」；浏览器不可用时为局部 QA 标「未验证」并移交用户复核）
→ 停止：不扩大优化范围
```

## 限制

不得把局部优化演变成 broad redesign（与 `references/stage-governance.md` 的关键原则一致）。
