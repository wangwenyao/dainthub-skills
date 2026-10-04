# Stage: design-system — 设计系统

## 目的

建立可复用的 Design Tokens、Theme、Component Contracts 与 Density / Motion 规则。

## 输入

- 已批准的 Design Direction
- 品牌约束
- 目标页面
- 当前技术 Profile（如有）

## 必须定义

```text
Color
Typography
Spacing
Radius
Elevation
Density
Motion
States
Responsive
Accessibility
```

## 原则

Design Tokens 是产品视觉权威；UI Library、Tailwind 或其他框架只是实现层。

## 产出

- Tokens
- Component Contracts
- Theme Strategy
- Design System Brief

结构分别照 `templates/design-system-brief.md` 与 `templates/design-specification.yaml`
的对应章节，不要另起一套字段名——后者是机器可校验的规范文件，字段漂移会让
`schemas/design-spec.json` 的校验失效。产出后按 `references/design-spec-lint-rules.md`
自检一遍再交付。

## 限制

没有明确 Scope 时，不修改业务页面与业务逻辑。
