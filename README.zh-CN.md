<p align="center">
  <img src="assets/branding/opl-bookforge-logo.png" alt="OPL BookForge 标志" width="132" />
</p>

<p align="center">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

<h1 align="center">OPL BookForge</h1>

<p align="center"><strong>把故事线推进到完整书稿包的 OPL 标准写书智能体</strong></p>
<p align="center">故事线梳理 · 章节写作 · 插图和表格 · 风格控制 · 导出交接</p>

<!--
Owner: `opl-bookforge`
Purpose: `public_repository_entry`
State: `public_entry`
Machine boundary: 人读公开入口。机器真相继续归 `contracts/`、`agent/`、OPL validator 输出、OMA Agent Lab evidence、pilot exports、owner receipts、typed blockers 和未来 runtime receipts。
-->

写书是长线交付工作。难点在于读者承诺、章节逻辑、材料依据、声音、插图、表格、排版和 owner 审阅要沿着同一本书持续推进，直到书稿可以交接。

`OPL BookForge` 围绕这件事设计：

- 这本书的读者承诺、目标读者、论证弧线和章节论点链是什么？
- 哪些材料支撑每章、每张图、每张表和关键表达？
- 多轮写作和修订后，章节之间能否保持同一种声音？
- 文字能否采用直接、肯定、具体的人工编辑口吻？
- DOCX/PDF 导出、插图计划、表格计划、风格报告和 owner gate 能否保持可追踪？

它面向的是完整写书流程：先做故事线架构，再做书籍物化，并把质量检查和交接证据绑定在同一个书籍项目上。

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>服务对象</strong><br/>
      作者、专家、研究者、教师，以及需要把材料写成一本书的 operator
    </td>
    <td width="33%" valign="top">
      <strong>组织内容</strong><br/>
      故事线、章节论点链、正文、插图和表格计划、风格契约、质量报告、导出文件和 owner gate
    </td>
    <td width="33%" valign="top">
      <strong>开始方式</strong><br/>
      提供书籍 brief、读者对象、材料包、声音要求和目标导出交接方式
    </td>
  </tr>
</table>

<p align="center">
  <img src="assets/branding/opl-bookforge-overview.png" alt="OPL BookForge overview" width="100%" />
</p>

## 核心亮点

**故事线优先**<br/>
BookForge 先建立前提、读者承诺、材料地图、论证弧线、章节论点链和风格契约，再进入章节写作。

**把书稿物化成一个阶段**<br/>
第二阶段产出章节草稿、正文、插图计划、表格计划、风格报告、AI 味措辞检查、排版 QC 和导出交接 refs。

**声音和风格可检查**<br/>
风格契约随书籍项目推进。检查重点包括术语一致、表达具体、肯定式编辑口吻，以及会让文字显得模板化的重复模式。

**插图、表格和排版进入主流程**<br/>
BookForge 把图、表、标题、导出形态、渲染页面和版式检查视为书籍交付面的一部分。

**出版边界 owner-gated**<br/>
BookForge 可以产出证据、草稿、导出文件和 typed blocker。出版批准、owner acceptance 和 production-ready 声明必须依赖 owner receipt 和运行时证据。

**由 OMA 和 Agent Lab 打磨**<br/>
当前基线已经包含 OPL Meta Agent takeover evidence、独立 AI reviewer evidence 和 external-suite self-evolution pass。新建智能体交付必须经过这条闭环，不能停在 scaffold ready。

## 一句话启动

可以这样开始：

- “用这批材料先梳理一本书的故事线，定义读者承诺、章节论点链和风格契约，然后停在 owner review。”
- “把已确认的故事线写成短书稿，包含章节草稿、插图计划、表格计划、风格检查、排版 QC 和 DOCX/PDF 导出交接。”
- “审查这份书稿的声音漂移、AI 味措辞、章节衔接、图表缺口和导出排版问题。”

## 适合处理

- 把笔记、材料包、讲义、报告或研究材料整理成书籍故事线。
- 让章节逻辑、依据引用、声音和编辑约束在整本书中保持一致。
- 在导出前规划插图、表格、caption 和放置意图。
- 把风格一致性、AI 味措辞、用词、排版和导出检查纳入写书路线。
- 用交接证据区分生成草稿、质量报告、owner blocker 和可接受出版材料。

## 当前交付重点

- `storyline-architecture`：前提、读者承诺、论证弧线、材料地图、章节论点链、风格契约和 owner handoff。
- `book-materialization`：章节草稿包、正文、插图计划、表格计划、风格一致性报告、AI 味修订报告、排版 QC、导出文件和 owner handoff。
- `OMA Agent Lab`：baseline takeover suite、AI reviewer evaluation、mechanism proposal refs、external-suite self-evolution 和 no-patch work-order receipt。
- `real book pilot`：短书 pilot 已产出故事线材料、正文、两张 PNG 插图、表格计划、DOCX/HTML/PDF 导出、PDF 渲染页、质量 receipts 和 typed owner blockers。

## 当前边界

- `OPL BookForge` 是 OPL 标准 Foundry Agent 领域包，用于书籍写作。
- OPL 负责生成接口、框架 runtime 投影、Agent Lab、work-order execution、registry/discovery 和 promotion gates。
- BookForge 负责书籍领域真相、书稿质量规则、风格政策、图表规划、导出/出版裁决边界、产物权威、memory body 和 owner receipts。
- 当前证据支持结构基线、生成接口描述符、OMA Agent Lab 评估，以及带导出/渲染检查的真实短书 pilot。
- 当前证据不能授权真实出书 production-ready 声明。pilot 仍是 `passed_with_owner_gate_blocker` / `production_ready_claim_allowed=false`，需要 human owner acceptance 以及直接 `opl-bookforge` runtime CLI 或 hosted artifact-handoff parity evidence 才能升级。

<details>
  <summary><strong>技术 OPL / operator 边界</strong></summary>

- 本包暴露 `shape-storyline` 和 `materialize-book` action contracts；当前 generated MCP/OpenAI/AI SDK descriptors 只是描述符，除非后续 runtime surface 证明可执行。
- `scripts/verify.sh` 通过本机 OPL CLI 验证 OPL 标准 scaffold 和生成接口描述符。
- OMA evidence 位于 `docs/evidence/oma-agent-lab/`。
- 真实 pilot evidence 位于 `docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/`。
- Pilot 导出包含 DOCX、HTML、PDF、渲染页面、生成插图、质量 receipts 和 typed owner blockers。这些是 evidence artifacts，不是 owner 出版接受。
- Scaffold validation、generated interface readiness、OMA takeover evidence、external-suite no-patch receipts、pilot exports 或 rendered pages 都不能单独升级为 owner receipt、publication approval、production readiness 或 hosted runtime parity。

</details>

## 如何阅读本仓

1. 潜在用户先读本页，再读 [Docs Guide](./docs/README.md)。
2. 技术读者继续读 [Project](./docs/project.md)、[Status](./docs/status.md)、[Architecture](./docs/architecture.md)、[Invariants](./docs/invariants.md) 和 [Decisions](./docs/decisions.md)。
3. Operator 在声明 readiness 或 owner acceptance 前，应检查 `contracts/`、`agent/`、`docs/evidence/oma-agent-lab/` 和真实 pilot evidence pack。

## Agent / Operator 快速入口

<details>
  <summary><strong>把本仓交给 Codex 或其他 agent 时从这里开始</strong></summary>

- 克隆本仓不会安装 OPL Framework，也不会安装 hosted BookForge runtime。需要托管执行时，先准备当前 `one-person-lab` checkout 或 release bundle。
- 修改前先读本 README、[Docs Guide](./docs/README.md)、[Status](./docs/status.md) 和 `AGENTS.md`。
- 把 `OPL BookForge` 视为书籍领域 owner，把 OPL 视为 generated/runtime surface owner。
- 评估基线时读取 OMA / Agent Lab evidence。新建智能体交付不能停在 scaffold 或 interface validation。
- 出版、导出接受和 production-ready 声明保持 fail-closed，直到 owner receipts 和 runtime parity evidence 到位。

</details>

## 命令

```bash
scripts/verify.sh
python3 docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/tools/verify_pilot.py
```

`scripts/verify.sh` 运行 OPL scaffold 和 generated-interface 验证。pilot verifier 检查现有 pilot evidence pack、导出文件、渲染页面、风格扫描、插图和 owner-gate blockers。

## 继续阅读

- [Docs Guide](./docs/README.md)
- [Project](./docs/project.md)
- [Status](./docs/status.md)
- [Architecture](./docs/architecture.md)
- [Invariants](./docs/invariants.md)
- [Decisions](./docs/decisions.md)
- [Contracts](./contracts/)
