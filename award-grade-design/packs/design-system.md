# Pack: design-system

## 资产分层

```text
Tokens          视觉原子：颜色、字阶、间距、圆角、阴影、动效
Components      带行为与契约的单元
Patterns        重复出现的交互组合（FilterBar、MetricGroup、ResultToolbar）
Density         档位规则
States          交互状态集合
Motion          动效原则
Responsive      空间不足时的重组规则
Accessibility   语义、焦点、对比度、键盘
```

## Token 规则

- Token 表达稳定语义，不是框架变量的改名。用 `color.action.primary`，不用
  `--ant-primary-color`。
- 层级：Product Semantic Tokens → Theme Adapter → 框架 / UI 库 / utility CSS。
- 重复出现三次以上的任意值，考虑提取 Token；为单个页面造一批一次性 Token 不划算。
- 判断标准：只改一处就能生效的，不是 Token；必须改多处才生效的，是耦合。

## 组件与 Token 的边界

- 视觉差异能用 Token 表达，就不要再包一层组件。
- 行为差异（状态、键盘、异步、组合）才是抽组件的理由。
- 为统一命名而建立的、没有行为或契约价值的 wrapper 是负债。

## Theme 策略

- 第三方 UI 库的 Theme API 是适配层，不是产品语言的定义处。
- 允许：Product Token → Theme Adapter → 组件库 Theme。
- 禁止：组件库默认 Theme → 反向决定 Product Token。

## 一致性检查

```text
同义不同名（primary / brand / accent 混用）
同名不同值（两处 success 色不一致）
绕过 Token 的硬编码颜色或间距
只在暗色模式下失效的对比度
```

发现这类问题优先修 Token 定义，不要在页面里逐个打补丁。
