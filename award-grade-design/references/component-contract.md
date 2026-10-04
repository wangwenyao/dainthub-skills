# Component Contract

## 必备内容

字段清单以 `stages/component.md` 的「Component Contract 必须包含」为唯一权威，
本文件不重复维护副本——重复的清单会漂移，而契约字段漂移会让产出缺项。
机器结构见 `templates/component-contract-deep.yaml`，命名保持框架中立
（inputs / events / composition points），具体框架词汇由技术 Profile 映射。

## Contract 原则

组件契约描述“为什么存在、如何使用、有哪些保证”，而不仅是代码 API。

## Vendor API

业务层组件不应默认透传整个第三方组件 API。应形成更稳定、更语义化的 Product API。
