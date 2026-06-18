# Storyline Map

## Premise

一本书的生产能力来自可接力的工作流。BookForge 把写作拆成两段主线: 先把读者承诺、论证弧线和章节 thesis 固定下来，再把它们转成章节、图表、排版和 handoff 证据。这个结构让写作从灵感推进到可审阅产物。

## Reader Promise

读者读完这本短手册后，可以判断一个书籍写作智能体是否真正跑过书籍项目，并能沿着 source-ref、quality gate、export check 和 owner blocker 复核证据。

## Audience Model

核心读者是 OPL 系列 agent 的 owner-operator。他们熟悉仓库、contracts、stage、receipt 和验证命令，关心智能体能否交付真实书稿。阅读场景是一次 production-readiness 审计，读者需要快速看到章节逻辑、证据链、图表计划、排版验收和签收边界。

## Central Argument

BookForge 的价值在于把写书变成可审计的生产路线。故事线阶段负责方向，书籍呈现阶段负责正文和形式，质量门负责一致性，owner receipt 负责最终接受。

## Chapter Thesis Chain

1. 写作从读者承诺开始: 书的目标先落到读者获得什么。
2. 故事线给素材排序: source-ref 进入论证弧线，章节获得推进关系。
3. 章节草稿承接 thesis: 每章新增一个判断，避免主题平铺。
4. 图表承担证据责任: 图片和表格服务理解、来源和复核。
5. 交付依赖质量门: 风格、措辞、排版和 owner handoff 共同决定下一步。

## Evidence Map

| claim | source refs | chapter placement |
|---|---|---|
| BookForge owns book-domain semantics and owner receipts | S1, S2, S3 | Chapter 1, Chapter 5 |
| The workflow has two primary stages | S2, S3, S5, S6 | Chapter 2 |
| Materialization must include chapters, illustrations, tables, style pass, layout QC | S6, S8 | Chapter 3, Chapter 4 |
| Structural validation and Agent Lab pass do not prove production readiness | S1, S9, S10 | Chapter 5 |

## Style Contract

The book uses compact, practical Chinese prose. Each section opens with a claim, explains its operational consequence, and points to a checkable artifact. Sentences favor active verbs: 固定, 接力, 复核, 生成, 检查, 签收. The manuscript avoids stock transitions and keeps repeated terms stable.

## Risks And Owner Decisions

- Owner must confirm whether this pilot topic is an acceptable real book project for final production-ready claim.
- Owner must review whether the generated manuscript meets publication intent and style expectations.
- Owner must accept or reject the exported DOCX/PDF layout.
- Direct OPL-hosted parity remains blocked because this repo declares action descriptors but does not ship a public `opl-bookforge` runtime CLI.
