# Changelog

## v9.1 — 2026-10-04

v9.0 → v9.1：修复「浏览器自动化可用但模型端点拒绝图片输入（400 No endpoints found
that support image input）时无规定行为」的失败类——skill 原文把「自动化可用」等价于
「视觉验收可行」。把浏览器自动化能力与模型视觉通道拆为两项独立能力，新增三种运行模式
（完整 / 盲查 / 未验证）、视觉通道懒判定（首次读图即探针 + 会话备忘 + 不盲目重试）、
盲查取证通道（DOM / computed style / 几何 / 对比度 / 状态枚举 / Token 契约比对 /
console / 前后 diff）与感知项人工复核移交；权威定义唯一落在
references/visual-qa-protocol.md，SKILL.md 与各文件只留投影与指针。visual-qa / audit /
implementation / optimization / component / direction / design-system 补视觉通道不可用时的
降级分支；报告与计划模板补证据渠道声明、人工复核移交章节与 channel / visual_review 字段；
rubric 补「无视觉通道时的评分姿态」（感知维度不评分、门槛 DEFERRED、不用满分补权重）；
「不得宣称视觉验收通过」禁令统一措辞，新增 consistency.evidence-channel-failclosed
确定性检查钉住。回归用例：视觉通道不可用的会话执行 visual-qa，验证文本渠道取证、
感知项标「未验证（需视觉通道）」、报告含证据渠道声明，而非谎报像素审查通过。
触发词与 Stage 路由零变动。

## v9.0 — 2026-10-04

v8.9 → v9.0：充实 design-spec-agent-protocol 的推进顺序 / 交接物 / 相位映射；收敛
packs 信息流与 Token 提取阈值的双写漂移（含 tailwind-implementation 第四处）；组件契约
词表中立化（inputs / events / composition points）并在 Profile 补 Vue 映射，模板补
content constraints 与 anti-examples 承载字段，density 三档 / 审计五字段 / Theme Strategy
章节补齐；implementation 删除框架专节改 Profile 指针、组件库策略中立化，design-system 的
Profile 资源改为确认技术栈后加载并补指针句，交接物清单与协议统一为五项；implementation
补登记 stage-governance（optimization 同），optimization Stage 输出点名登记模板；audit /
direction / design-system / component / optimization 五个 Stage 补可判定停止条件；门禁修复
常驻计数把 stage 指针计入的偏差，scope-safety 覆盖省略 / 空值 forbidden，信息流检查覆盖
packs，数值检查改 fail-closed 并新增资源条目形态校验，新增数值投影一致与检查名注册表同步
两项检查（条件性检查豁免、注册表自身断言）；触发回归集补 4 条正例，stage-router 补
设计走查 / 一致性审查信号；视觉 QA 报告补下一轮 Top 3 章节；清除与其他 skill 的关联表述
（description 边界、触发负例与 policy 措辞），本 Skill 独立适用。
