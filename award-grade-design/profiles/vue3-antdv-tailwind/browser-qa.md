# Browser QA Profile

当使用该技术栈进行 Visual QA 时，优先验证：

```text
真实数据长度
Table overflow
Toolbar wrapping
Modal / Drawer
Focus
Loading / Empty / Error
Responsive
Console warnings / errors
```

默认优先真实浏览器截图，而不是只看源码。

截图供用户或有视觉通道的模型查看；模型视觉通道不可用时按
`references/visual-qa-protocol.md` 的「盲查取证通道」执行——上面清单全部可经文本
渠道验证，不得跳过。
