# Design Specification

> 本模板是 `templates/design-specification.yaml`（机器权威，对齐 `schemas/design-spec.json`）的人读投影。
> 字段名必须与 Schema 一致，不得另起同义词；章节顺序即 Schema 顶层字段顺序。

## spec_version

- 设计规格版本（`X.Y.Z`），每次发布递增。

## 1. Product Context → `product`

### Name / Type / Business context

### Target users

- Primary:
- Secondary:

### Jobs to be done

1.
2.
3.

### Constraints

-

## 2. Experience Goals → `experience`

### Goals

-

### Principles

-

### Success metrics

-

### Anti-goals

-

## 3. Information Architecture → `information_architecture`

### Navigation

### Hierarchy

### Objects

### Journeys

```text
Entry → Task → Decision → Action → Feedback → Next action
```

## 4. Design Direction → `art_direction`

### Concept

### Mood

### Visual pillars

1.
2.
3.

### Typography

### Color

### Shape

### Surface

### Imagery / data visualization direction

### Iconography

## 5. Design Tokens → `system.tokens`

### Color

### Type

### Space

### Radius

### Surface

### Motion

### Focus / accessibility

### Density

## 6. Component Contracts → `system.components` / `system.patterns`

For each key component:

```text
Purpose
Anatomy
Variants
Density
States
Interaction
Keyboard
Responsive behavior
Content rules
Motion
Accessibility
```

## 7. Screen Specifications → `screens[]`

> 字段名与 `schemas/design-spec.json` 的 `screens[]` 一致；`required` 字段不得缺省。

### Screen: {id}

**archetype:**

**purpose:**

**primary_task:**

**primary_action:**

**density:**

**information_hierarchy:**

**composition:**

**components:**

**states:**

**responsive:**

**motion:**

**accessibility:**

**data_viz:**

## 8. Implementation Mapping → `implementation`

> 策略词表为六项：reuse / configure / wrap / extend / replace / create，与 Schema 一致。

| Design element | Strategy (reuse/configure/wrap/extend/replace/create) | Current implementation | Notes |
|---|---|---|---|
| | | | |

## 9. QA Plan → `qa`

### Viewports

> 默认四档与 `templates/design-specification.yaml` 的 `qa.viewports` 一致。

-

### Critical flows

-

### Defect thresholds

- unresolved_p0: 0
- unresolved_p1_critical_flow: 0

### Acceptance criteria

- [ ]
- [ ]
- [ ]

### Evidence

-

## 10. Exceptions / Deviations → `exceptions`

> 每条包含 decision / reason / impact / follow_up。

| Decision | Reason | Impact | Follow-up |
|---|---|---|---|
| | | | |