# Component Implementation Playbook — 组件实现手册

## 先看 Contract

开始编码前必须回答：

```text
用户任务是什么？
组件自己拥有哪部分状态？
哪些状态属于 page / domain？
哪些行为交给 Ant Design Vue？
哪些视觉由 Product Tokens / Tailwind 负责？
```

## Vue

推荐：

```text
<script setup lang="ts">
Composition API
强类型 Props / Emits
computed 优先于重复 mutable state
副作用放到明确的 composable / lifecycle 边界
```

## Ant Design Vue

把复杂交互机制交给成熟组件，但业务层只暴露语义化 API。

## Tailwind

保持 class 组合可读。重复模式应提取，不要让页面成为巨大的 utility 字符串集合。

## 数据密集组件

```text
loading → skeleton / progressive structure
empty → explanation + recovery
partial → 保留已知数据并标记不完整
error → actionable recovery
success → 稳定交互状态
```

## 性能

高频状态尽量局部化，避免 render 路径反复创建大对象/数组；保留已有虚拟化与懒加载策略。

## 完成标准

TypeScript 编译通过只是开始。还必须验证 Contract、Visual States、Keyboard、Responsive、Runtime、Console。
