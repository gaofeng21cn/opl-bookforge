<p align="center">
  <img src="assets/branding/opl-bookforge-logo.png" alt="OPL Book Forge 标志" width="132" />
</p>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

<h1 align="center">OPL Book Forge</h1>

<p align="center"><strong>把故事线推进到完整书稿包的 OPL 标准写书智能体</strong></p>
<p align="center">故事线梳理 · 章节写作 · 插图和表格 · 风格控制 · 导出交接</p>

<!--
Owner: `opl-bookforge`
Purpose: `public_repository_entry`
State: `public_entry`
Machine boundary: 人读公开入口。机器真相继续归 `contracts/`、`agent/`、OPL 校验输出、OMA Agent Lab 证据、试运行导出、负责人签收记录、结构化阻塞和未来运行时回执。
-->

写书是长线交付工作。真正的难点在于让读者承诺、章节逻辑、材料依据、叙述声音、插图、表格、排版和负责人审阅沿着同一本书持续推进，直到书稿能够交接。

`OPL Book Forge` 围绕这件事设计：

- 明确这本书的读者承诺、目标读者、论证弧线和章节论点链。
- 追踪每章、每张图、每张表和关键表达背后的材料依据。
- 让多轮写作和修订后的章节保持同一种声音。
- 用直接、肯定、具体的人工编辑口吻打磨文字。
- 让 DOCX/PDF 导出、插图计划、表格计划、风格报告和签收门保持可追踪。

Book Forge 以 stage-led 路线推进写书：先梳理故事线，再通过聚焦的 materialization stages 进入章节规划、章节写作、来源/风格审查和 proof/export 交接，并把质量检查和交接证据绑定在同一个书籍项目上。

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>服务对象</strong><br/>
      作者、专家、研究者、教师，以及需要把材料写成一本书的专业操作者
    </td>
    <td width="33%" valign="top">
      <strong>组织内容</strong><br/>
      故事线、章节论点链、正文、插图和表格计划、风格契约、质量报告、导出文件和签收门
    </td>
    <td width="33%" valign="top">
      <strong>开始方式</strong><br/>
      提供书籍简要说明、读者对象、材料包、声音要求和目标导出交接方式
    </td>
  </tr>
</table>

<p align="center">
  <img src="assets/branding/opl-bookforge-overview-v2.png" alt="OPL Book Forge 总览" width="100%" />
</p>

## 核心亮点

**故事线优先**<br/>
Book Forge 先建立前提、读者承诺、材料地图、论证弧线、章节论点链和风格契约，再进入章节写作。

**Materialization 拆成聚焦阶段**<br/>
`book-materialization` 现在是故事线通过后的显式 handoff locator。章节规划、章节写作、来源/风格审查、proof/export 交接分别由顶层 stage 承担，避免一个 stage 同时吞下多个独立判断。

**声音和风格可检查**<br/>
风格契约随书籍项目推进。检查重点包括术语一致、表达具体、肯定式编辑口吻，以及容易让文字显得模板化的重复模式。

**插图、表格和排版进入主流程**<br/>
Book Forge 把图、表、标题、导出形态、渲染页面和版式检查视为书籍交付面的一部分。

**出版级 proof 有独立质量门**<br/>
review PDF 继续作为进度优先的阅读检查点。publication proof 额外要求出版设计 tokens、组件清单、字体实际加载/回读、渲染页面 QA、前置页和目录清洁度、页面节奏/密度/孤行检查、素材覆盖和 pre-ship proof review。final export 仍需要负责人/导出接受回执。

**Meta Review 先路由返修层级**<br/>
整书审阅或严肃批评之后，Book Forge 会先判断返修应从目标产物、故事线、大纲顺序、章节功能、证据/模型、出版设计、局部文字，还是 owner/source blocker 开始，再进入改稿。

**出版边界由负责人签收**<br/>
Book Forge 可以产出证据、草稿、导出文件和结构化阻塞。出版批准、负责人接受和生产可用声明必须依赖相应签收记录和运行时证据。

**通过 OMA 和 Agent Lab 打磨**<br/>
当前基线已经包含 OPL Meta Agent 接管测试证据、独立 AI 评审证据和外部套件自进化记录。新建智能体交付必须经过这条闭环，不能停在脚手架通过。

## 一句话启动

可以这样开始：

- “用这批材料先梳理一本书的故事线，定义读者承诺、章节论点链和风格契约，然后停在负责人审阅。”
- “把已确认的故事线写成短书稿，包含章节草稿、插图计划、表格计划、风格检查、排版质检和 DOCX/PDF 导出交接。”
- “对整本书做 Meta Review，并判断返修应从故事线、大纲、章节功能、证据/模型、出版设计还是局部文字开始。”

## 适合处理

- 把笔记、材料包、讲义、报告或研究材料整理成书籍故事线。
- 让章节逻辑、依据引用、声音和编辑约束在整本书中保持一致。
- 在导出前规划插图、表格、图表说明和放置意图。
- 把风格一致性、AI 味措辞、用词、排版和导出检查纳入写书路线。
- 用交接证据区分生成草稿、质量报告、负责人阻塞和可接受出版材料。

## 当前交付重点

- `storyline-architecture`：前提、读者承诺、论证弧线、材料地图、章节论点链、风格契约和负责人交接。
- `book-materialization`：已确认故事线后的 materialization handoff locator；判断是否可以进入章节生产规划，或是否必须 route back。
- `chapter-production-planning`：目标篇幅、章节预算、生产队列、章节任务卡、context plan 和书籍记忆 refs。
- `chapter-materialization`：章节 context pack、reader-entry plan、逐章 Markdown 草稿 refs、章节 QC 和可复用返修回写。
- `source-style-integrity-review`：claim/source integrity、风格一致性、AI 味扫描、独立 meta-review 路由和返修入口 refs。
- `publication-proof-handoff`：review/proof/export 交接 refs、图表 readiness、需要时的渲染页 QA refs、负责人决策、阻塞和 artifact-role 边界。
- `OMA Agent Lab`：基线接管测试套件、AI 评审、机制提案引用、外部套件自进化和无补丁工单回执。
- `真实短书试运行`：已经产出故事线材料、正文、两张 PNG 插图、表格计划、DOCX/HTML/PDF 导出、PDF 渲染页、质量回执和结构化负责人阻塞。

## 当前边界

- `OPL Book Forge` 是用于书籍写作的 OPL 标准领域智能体包。
- 在 OPL family 中，Book Forge 是书籍写作 domain agent package：Book Forge 保留书籍领域 authority，OPL 持有通用 runtime、package carrier、generated wrapper 和 hosted surface。
- OPL 负责生成接口、框架运行时投影、Agent Lab、工单执行、注册/发现和晋级门。
- Book Forge 负责书籍领域真相、书稿质量规则、风格政策、图表规划、导出/出版裁决边界、产物权威、记忆正文和负责人签收记录。
- 当前证据支持标准结构基线、生成接口描述符、OMA Agent Lab 评估，以及带导出/渲染检查的真实短书试运行。
- 当前证据不能授权真实出书生产可用声明。试运行仍是 `passed_with_owner_gate_blocker` / `production_ready_claim_allowed=false`，需要人类负责人接受，以及 live OPL StageRun 或托管产物交接等价证据才能升级。

<details>
  <summary><strong>技术 OPL / 操作者边界</strong></summary>

- 本包暴露 `shape-storyline` 和 `materialize-book` 动作合同；当前生成的 MCP/OpenAI/AI SDK 描述符只是描述符，后续运行时表面需要单独证明可执行。
- `scripts/verify.sh` 通过本机 OPL 命令行验证 OPL 标准脚手架和生成接口描述符。
- OMA 证据位于 `docs/evidence/oma-agent-lab/`。
- 真实试运行证据位于 `docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/`。
- 试运行导出包含 DOCX、HTML、PDF、渲染页面、生成插图、质量回执和结构化负责人阻塞。这些是证据产物，不是负责人出版接受。
- Kami-inspired publication proof 规则作为 Book Forge 领域合同和 helper machine-baseline proof plumbing 吸收；不引入 Kami 视觉语言、WeasyPrint 运行路线、字体安装器、更新检查器或第二套 proof 真相源，也不替代人工出版设计审阅、final export 接受或 owner proof readiness 证据。
- 脚手架校验、生成接口就绪、OMA 接管证据、外部套件无补丁回执、试运行导出文件或渲染页面，都不能单独升级为负责人签收、出版批准、生产可用或托管运行时等价。

</details>

## 如何阅读本仓

1. 潜在用户先读本页，再读 [文档导览](./docs/README.md)。
2. 技术读者继续读 [项目概览](./docs/project.md)、[状态](./docs/status.md)、[架构](./docs/architecture.md)、[不变量](./docs/invariants.md) 和 [决策](./docs/decisions.md)。
3. 操作者在声明就绪或负责人接受前，应检查 `contracts/`、`agent/`、`docs/evidence/oma-agent-lab/` 和真实试运行证据包。

## 智能体和操作者快速入口

<details>
  <summary><strong>把本仓交给 Codex 或其他智能体时从这里开始</strong></summary>

- 克隆本仓不会安装 OPL 框架，也不会安装托管 Book Forge 运行时。需要托管执行时，先准备当前 `one-person-lab` 检出仓库或发布包。
- 修改前先读本 README、[文档导览](./docs/README.md)、[状态](./docs/status.md) 和 `AGENTS.md`。
- 把 `OPL Book Forge` 视为书籍领域负责人，把 OPL 视为生成接口和运行时表面的负责人。
- 评估基线时读取 OMA / Agent Lab 证据。新建智能体交付不能停在脚手架通过或接口校验通过。
- 出版、导出接受和生产可用声明默认拒绝升级，直到负责人签收记录和运行时等价证据到位。

</details>

## 命令

```bash
scripts/verify.sh
python3 docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/tools/verify_pilot.py
```

`scripts/verify.sh` 运行 OPL 脚手架和生成接口验证。试运行验证器检查现有证据包、导出文件、渲染页面、风格扫描、插图和负责人签收门阻塞。

## 继续阅读

- [English README](./README.md)
- [文档导览](./docs/README.md)
- [项目概览](./docs/project.md)
- [状态](./docs/status.md)
- [架构](./docs/architecture.md)
- [不变量](./docs/invariants.md)
- [决策](./docs/decisions.md)
- [合同](./contracts/)
