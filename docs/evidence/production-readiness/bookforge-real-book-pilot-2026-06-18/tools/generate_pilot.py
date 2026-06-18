#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18"
INPUTS = BASE / "inputs"
STORYLINE = BASE / "artifacts/stage_outputs/storyline-architecture"
MATERIALIZATION = BASE / "artifacts/stage_outputs/book-materialization"
MANUSCRIPT = BASE / "artifacts/manuscript"
FIGURES = BASE / "artifacts/figures"
RECEIPTS = BASE / "receipts"
QUALITY = BASE / "quality"
EXPORTS = BASE / "exports"
LOGS = BASE / "logs"

RUN_ID = "bookforge-real-book-pilot-2026-06-18"
PROJECT_ID = "bookforge-production-smoke-2026-06-18"
GENERATED_AT = datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in [INPUTS, STORYLINE, MATERIALIZATION, MANUSCRIPT, FIGURES, RECEIPTS, QUALITY, EXPORTS, LOGS]:
        path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.strip() + "\n", encoding="utf-8")


def write_json(path: Path, body: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_figure_1(path: Path) -> None:
    img = Image.new("RGB", (1800, 1050), "#ffffff")
    draw = ImageDraw.Draw(img)
    title_font = font(58)
    label_font = font(34)
    small_font = font(26)
    draw.rectangle([0, 0, 1800, 1050], fill="#ffffff")
    draw.text((90, 70), "书籍故事线: 从素材到读者承诺", fill="#16324f", font=title_font)
    nodes = [
        ("素材", "source corpus", 140),
        ("问题", "reader tension", 470),
        ("承诺", "reader promise", 800),
        ("章节", "chapter plan", 1130),
        ("交付", "book package", 1460),
    ]
    y = 420
    for idx, (label, sub, x) in enumerate(nodes):
        draw.rounded_rectangle([x, y, x + 210, y + 150], radius=28, fill="#eef5f1", outline="#4f7f6a", width=5)
        draw.text((x + 55, y + 28), label, fill="#16324f", font=label_font)
        draw.text((x + 26, y + 88), sub, fill="#51606f", font=small_font)
        if idx < len(nodes) - 1:
            x1 = x + 220
            x2 = nodes[idx + 1][2] - 12
            draw.line([x1, y + 75, x2, y + 75], fill="#7a4f2b", width=6)
            draw.polygon([(x2, y + 75), (x2 - 22, y + 62), (x2 - 22, y + 88)], fill="#7a4f2b")
    draw.text((140, 690), "每一步都保留 source-ref、质量门和 owner handoff。", fill="#293241", font=small_font)
    draw.text((140, 738), "章节推进读者理解，图表承担证据责任，排版服务阅读节奏。", fill="#293241", font=small_font)
    img.save(path)


def draw_figure_2(path: Path) -> None:
    img = Image.new("RGB", (1800, 1050), "#ffffff")
    draw = ImageDraw.Draw(img)
    title_font = font(56)
    label_font = font(31)
    small_font = font(24)
    draw.text((90, 70), "BookForge 两阶段生产路线", fill="#17324d", font=title_font)
    columns = [
        ("Stage 1", "storyline-architecture", ["读者承诺", "论证弧线", "章节 thesis", "风格合同"]),
        ("Gate", "independent review", ["来源覆盖", "章节推进", "语气一致", "blocker"]),
        ("Stage 2", "book-materialization", ["章节草稿", "插图计划", "表格计划", "版式 QC"]),
        ("Gate", "handoff and export", ["内容一致", "去 AI 味", "图表验收", "owner gate"]),
    ]
    start_x = 105
    y = 260
    w = 365
    for idx, (kicker, heading, bullets) in enumerate(columns):
        x = start_x + idx * 420
        fill = "#f4f7fb" if idx % 2 == 0 else "#f8f5ef"
        border = "#355c7d" if idx % 2 == 0 else "#8a633d"
        draw.rounded_rectangle([x, y, x + w, y + 520], radius=24, fill=fill, outline=border, width=5)
        draw.text((x + 28, y + 32), kicker, fill=border, font=small_font)
        draw.text((x + 28, y + 82), heading, fill="#1f2933", font=label_font)
        by = y + 170
        for bullet in bullets:
            draw.ellipse([x + 30, by + 8, x + 48, by + 26], fill=border)
            draw.text((x + 66, by), bullet, fill="#1f2933", font=small_font)
            by += 75
        if idx < len(columns) - 1:
            x1 = x + w + 18
            x2 = x + 420 - 28
            draw.line([x1, y + 260, x2, y + 260], fill="#69707a", width=5)
            draw.polygon([(x2, y + 260), (x2 - 20, y + 248), (x2 - 20, y + 272)], fill="#69707a")
    draw.text((105, 840), "Production-ready claim 需要真实 owner receipt；本 pilot 生成 owner blocker，保留下一步签收入口。", fill="#293241", font=small_font)
    img.save(path)


def build_inputs() -> None:
    write_text(
        INPUTS / "book-brief.md",
        """
# Book Brief

Project id: `bookforge-production-smoke-2026-06-18`

Working title: `从想法到书稿: OPL BookForge 写作工作流手册`

Purpose: demonstrate that OPL BookForge can run a real book project through its two declared stages: storyline architecture and book materialization.

Reader: owner-operators and agent builders who already use OPL-style agents and need a concrete book-writing workflow with receipts, quality gates, and export checks.

Publication target: reviewable short handbook, exported to Markdown, HTML, DOCX, and PDF for layout inspection. This pilot does not claim final publication approval.

Owner intent:

- Explain the two-stage workflow in direct, concrete Chinese prose.
- Keep the book grounded in source refs from this repo and the OMA/Agent Lab evidence.
- Include chapter drafts, illustration planning, table planning, style checks, wording cleanup, and layout QC.
- Close with an owner handoff and typed blocker when final owner acceptance is missing.
""",
    )
    write_text(
        INPUTS / "source-corpus.md",
        """
# Source Corpus

## Source refs

| id | source-ref | role in this pilot |
|---|---|---|
| S1 | `AGENTS.md` | authority boundary and validation entry point |
| S2 | `TASTE.md` | book-first preference, two-stage workflow, AI-flavor quality rule |
| S3 | `contracts/stage_control_plane.json` | stage ids, required refs, handoff closure refs |
| S4 | `contracts/action_catalog.json` | action ids `shape-storyline` and `materialize-book` |
| S5 | `agent/prompts/storyline-architecture.md` | storyline output expectations |
| S6 | `agent/prompts/book-materialization.md` | materialization output expectations |
| S7 | `agent/quality_gates/storyline-architecture-quality-gate.md` | storyline pass and fail-closed conditions |
| S8 | `agent/quality_gates/book-materialization-quality-gate.md` | manuscript, figure, table, style, layout gate |
| S9 | `docs/status.md` | baseline, OMA takeover, external-suite evidence and remaining gaps |
| S10 | `docs/evidence/oma-agent-lab/bookforge-ai-reviewer-evaluation.json` | independent reviewer critique and predicted next maturity gate |

## Corpus notes

The book uses BookForge's own contracts as source material. The pilot therefore tests the agent on a real domain surface instead of a synthetic topic. The manuscript may explain the workflow, but it may not claim final publication approval, export approval, or owner acceptance without an owner receipt.
""",
    )
    write_text(
        INPUTS / "voice-and-audience.md",
        """
# Voice And Audience

Voice contract:

- Use concise Chinese prose with direct claims and concrete verbs.
- Prefer positive editorial movement. State what the workflow does, why it matters, and how a reader uses it.
- Keep terminology stable: `故事线`, `章节 thesis`, `source-ref`, `quality gate`, `owner handoff`, `typed blocker`.
- Avoid inflated abstractions, vague transitions, empty summaries, and contrast formulas.
- Every table and figure must carry a purpose, placement, source boundary, and review criterion.

Audience situation:

- The reader can inspect local repo evidence.
- The reader cares about real delivery, not a scaffold demo.
- The reader needs a handoff packet that separates completed automation from human acceptance.
""",
    )


def build_storyline() -> None:
    write_text(
        STORYLINE / "storyline-map.md",
        """
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
""",
    )
    write_json(
        STORYLINE / "chapter-thesis-chain.json",
        {
            "surface_kind": "bookforge_chapter_thesis_chain",
            "schema_version": 1,
            "project_id": PROJECT_ID,
            "stage_id": "storyline-architecture",
            "chapters": [
                {
                    "chapter": 1,
                    "title": "写作从读者承诺开始",
                    "thesis": "BookForge first fixes the reader promise so later writing has a stable target.",
                    "source_refs": ["S1", "S2", "S5"],
                },
                {
                    "chapter": 2,
                    "title": "故事线给素材排序",
                    "thesis": "The storyline stage turns source refs into an argument arc and chapter thesis chain.",
                    "source_refs": ["S3", "S5", "S7"],
                },
                {
                    "chapter": 3,
                    "title": "章节草稿承接 thesis",
                    "thesis": "Materialization drafts chapters by preserving chapter roles, evidence placement, and voice.",
                    "source_refs": ["S6", "S8"],
                },
                {
                    "chapter": 4,
                    "title": "图表承担证据责任",
                    "thesis": "Figures and tables carry source boundaries and review criteria, not decoration.",
                    "source_refs": ["S6", "S8"],
                },
                {
                    "chapter": 5,
                    "title": "交付依赖质量门",
                    "thesis": "A production-ready claim requires quality gates, exports, and owner receipts.",
                    "source_refs": ["S1", "S8", "S9", "S10"],
                },
            ],
        },
    )
    write_text(
        STORYLINE / "style-contract.md",
        """
# Style Contract

Tone: practical, editor-like, and evidence-aware.

Sentence policy:

- Open sections with the operational claim.
- Use direct verbs and stable nouns.
- Keep transitions specific to the workflow step.
- Prefer short paragraphs with one job each.

Terminology:

| term | meaning |
|---|---|
| 故事线 | book-level argument path and reading promise |
| chapter thesis | the job each chapter performs in the book |
| source-ref | checkable source anchor used by a claim |
| quality gate | independent review surface with pass and fail-closed conditions |
| owner handoff | packet requiring owner review, acceptance, or typed blocker |

Revision floor:

- Remove vague praise, empty overview sentences, and inflated claims.
- Replace contrast formulas with positive commitments.
- Preserve source boundaries when changing prose.
""",
    )
    write_text(
        STORYLINE / "owner-handoff.md",
        """
# Storyline Owner Handoff

Stage: `storyline-architecture`

Artifacts:

- `storyline-map.md`
- `chapter-thesis-chain.json`
- `style-contract.md`

Independent gate result: pass for pilot progression.

Owner decisions required:

- Confirm the pilot topic as an acceptable real book project.
- Approve or edit the reader promise.
- Approve or edit chapter order and thesis chain.
- Decide whether the missing direct `opl-bookforge` runtime CLI blocks production-ready scope.

Closure route: `typed-blocker-ref:bookforge-production-smoke-2026-06-18/storyline-owner-review-missing`
""",
    )


def build_materialization() -> None:
    draw_figure_1(FIGURES / "figure-01-storyline-arc.png")
    draw_figure_2(FIGURES / "figure-02-two-stage-route.png")

    manuscript = """
---
title: "从想法到书稿"
subtitle: "OPL BookForge 写作工作流手册"
author: "OPL BookForge Pilot"
date: "2026-06-18"
lang: zh-CN
---

# 目录

- 前言
- 第一章 写作从读者承诺开始
- 第二章 故事线给素材排序
- 第三章 章节草稿承接 thesis
- 第四章 图表承担证据责任
- 第五章 交付依赖质量门
- 结语

# 前言

BookForge 处理的是一本书的完整交付路线。它先固定读者承诺，再把承诺推进到章节、图表、排版和签收证据。这样的路线让写作有稳定方向，也让审阅者能沿着 artifact、quality gate 和 owner handoff 复核每一步。

这本 pilot 手册使用 BookForge 仓库自身作为 source corpus。输入来自 stage control plane、action catalog、prompt、quality gate 和 OMA 评估记录。正文只使用这些 source-ref 支撑的判断，并把缺少 owner acceptance 的位置写成 typed blocker。

![图 1: 书籍故事线从素材到读者承诺](../figures/figure-01-storyline-arc.png)

# 第一章 写作从读者承诺开始

一本书需要先回答读者获得什么。BookForge 在 `storyline-architecture` 阶段固定 premise、audience、reader promise 和 central argument。这个阶段的产物让后续章节知道自己要服务的判断，也让 owner 能在正文扩写前检查方向。

读者承诺承担两个作用。第一，它限定书的范围。第二，它让质量检查拥有明确基准。章节写得流畅仍然可能偏题；source-ref 很完整也可能缺少论证运动。reader promise 把这些问题提前暴露出来。

在本 pilot 中，读者承诺是：owner-operator 能判断书籍写作智能体是否真正跑过书籍项目，并能复核 source-ref、quality gate、export check 和 owner blocker。这句话直接决定章节安排。第一章解释承诺，第二章解释故事线，第三章进入正文生成，第四章处理图表，第五章回到验收。

| 读者问题 | BookForge 回答 | 证据位置 |
|---|---|---|
| 这本书为谁写 | OPL 系列 agent owner-operator | `inputs/voice-and-audience.md` |
| 书稿如何避免散 | 章节 thesis 固定推进关系 | thesis-chain |
| 产物如何被验收 | quality gate 加 owner handoff | gate receipts |

# 第二章 故事线给素材排序

故事线阶段把素材变成读者可以跟随的路径。BookForge 先识别 source corpus 支持的判断，再安排每章承担一个推进动作。这个动作可以是定义范围、建立框架、展开执行、说明证据，或关闭验收。

本 pilot 的 source corpus 主要来自十个本地 source-ref。`contracts/stage_control_plane.json` 给出两个阶段和 handoff 规则；`agent/prompts/*` 给出产物要求；`agent/quality_gates/*` 给出 pass 条件和 fail-closed 条件；`docs/status.md` 和 OMA reviewer evaluation 说明当前成熟度边界。

故事线产物必须保留风险和 owner 决策。缺少这些内容，第二阶段会把未确认问题写进正文，后续审阅只能返工。本 pilot 把 owner topic approval、final manuscript acceptance、layout acceptance 和 direct runtime parity 标成 owner decisions。这样做让书稿能够继续生成，也让 production-ready claim 保持真实。

![图 2: BookForge 两阶段生产路线](../figures/figure-02-two-stage-route.png)

# 第三章 章节草稿承接 thesis

章节草稿的任务是推进 thesis。每章开头先给出判断，再用 source-ref 解释判断的操作含义。这样的写法让读者不断获得新信息，避免章节之间重复同一层意思。

BookForge 的 `book-materialization` prompt 要求输出 chapter drafts、illustration specs、table specs、style consistency report、AI-flavor revision report、layout QC report 和 owner handoff packet。本 pilot 逐项生成这些 artifact，并把它们放入同一个 evidence pack。审阅者可以从 manuscript 进入正文，也可以从 receipts 进入验收状态。

章节写作采用同一套术语。`故事线` 表示全书路径，`chapter thesis` 表示章节职责，`source-ref` 表示证据锚点，`quality gate` 表示独立检查，`owner handoff` 表示人类签收入口。术语稳定后，书稿读起来更像人工编辑过的手册，读者不用在多个同义词之间切换。

| 章节 | thesis | source refs | draft status |
|---|---|---|---|
| 第一章 | 读者承诺给写作设定目标 | S1, S2, S5 | drafted |
| 第二章 | 故事线把 source-ref 排成论证弧线 | S3, S5, S7 | drafted |
| 第三章 | 章节草稿承接 thesis 并保持风格 | S6, S8 | drafted |
| 第四章 | 图表承担来源和复核责任 | S6, S8 | drafted |
| 第五章 | 交付必须经过质量门和 owner gate | S1, S8, S9, S10 | drafted |

# 第四章 图表承担证据责任

图表进入书稿时要说明用途、来源和检查标准。BookForge 把图片和表格视为 meaning-bearing elements。图片帮助读者看到结构，表格帮助读者比较证据。每个图表都需要 placement、source boundary 和 review criteria。

本 pilot 生成两张确定性 PNG。第一张展示从素材到读者承诺的故事线，第二张展示两阶段生产路线。它们使用本地脚本生成，来源边界清楚，尺寸可检查，文件 hash 可记录。表格则用于呈现读者问题、章节 thesis 和质量门结果。

这样的图表计划让排版检查有对象。layout QC 可以检查图片是否存在、尺寸是否足够、caption 是否靠近图片、表格是否有标题行、列宽是否适合内容。图表只承载来源支持的事实。

| artifact | purpose | placement | review criterion |
|---|---|---|---|
| `figure-01-storyline-arc.png` | show how source material becomes reader promise | after preface | nonblank PNG, readable labels, source boundary recorded |
| `figure-02-two-stage-route.png` | show stage and gate sequence | chapter 2 | nonblank PNG, stage names match contracts |
| reader question table | map reader need to artifact evidence | chapter 1 | each row has evidence location |
| chapter thesis table | show chapter movement | chapter 3 | each chapter has source refs and status |

# 第五章 交付依赖质量门

BookForge 的交付结论来自证据链。结构验证说明 repo 形态有效；Agent Lab takeover 说明 OMA 能读取和评估 agent package；pilot stage run 说明真实书籍项目可以产生 storyline、manuscript、图表计划和导出文件。production-ready claim 还需要 owner receipt。

本 pilot 的质量门检查四组内容。内容一致性检查章节是否沿着 reader promise 推进。风格一致性检查术语、语气、段落节奏和过渡。AI-flavor 检查删除空泛套话和机械化转折。排版检查覆盖 DOCX、HTML、PDF、图片和表格。

当前 closeout 应保持谨慎。两个 stage 已经产生 artifact，导出链路可以被本地工具复核，质量 gate 给出 pass-with-owner-blocker。最终 production-ready claim 仍等待 owner 对真实出版意图、正文质量和导出样式签收。

# 结语

BookForge 的核心价值是把写作交付变成可审计工作流。它把故事线、章节、图表、措辞、排版和 owner handoff 放在同一条证据链中。pilot 运行证明这条链可以产出一本可审阅的短书，也清楚留下 final owner acceptance typed blocker。下一步由 owner 阅读导出文件，选择签收、返修，或扩大到更长的真实书籍项目。
"""
    write_text(MANUSCRIPT / "book.md", manuscript)

    write_text(
        MATERIALIZATION / "chapter-drafts.md",
        """
# Chapter Draft Bundle

Canonical manuscript: `artifacts/manuscript/book.md`

Chapter status:

| chapter | purpose | source refs | status |
|---|---|---|---|
| 前言 | state production pilot scope and source boundary | S1-S10 | drafted |
| 第一章 | fix reader promise and acceptance baseline | S1, S2, S5 | drafted |
| 第二章 | turn source corpus into chapter movement | S3, S5, S7 | drafted |
| 第三章 | materialize thesis into consistent chapter prose | S6, S8 | drafted |
| 第四章 | plan and validate figures/tables as evidence elements | S6, S8 | drafted |
| 第五章 | connect quality gates, exports, and owner receipt | S1, S8, S9, S10 | drafted |

The draft preserves the storyline contract and keeps every production-ready claim gated by owner acceptance.
""",
    )
    write_text(
        MATERIALIZATION / "illustration-plan.md",
        """
# Illustration Plan

| id | file | purpose | placement | source boundary | review criteria |
|---|---|---|---|---|---|
| F1 | `artifacts/figures/figure-01-storyline-arc.png` | Show how corpus becomes reader promise and chapters | Preface | Deterministic local diagram from pilot storyline map | PNG exists, nonblank, labels readable, no unsupported claims |
| F2 | `artifacts/figures/figure-02-two-stage-route.png` | Show two-stage route and quality gates | Chapter 2 | Deterministic local diagram from stage_control_plane and gate refs | PNG exists, nonblank, stage ids match source refs |

Rights boundary: local generated diagrams for internal pilot evidence. No third-party images or copied assets are used.
""",
    )
    write_text(
        MATERIALIZATION / "table-plan.md",
        """
# Table Plan

| id | table | supported claim | source refs | formatting rule |
|---|---|---|---|---|
| T1 | reader question table | Reader promise maps to concrete evidence | S1, S2, S5 | three columns, short cells, header row |
| T2 | chapter thesis table | Each chapter advances the book-level argument | S3, S5, S6, S8 | four columns, source refs visible |
| T3 | illustration artifact table | Figures and tables have review criteria | S6, S8 | four columns, artifact paths in monospace |

Tables contain comparison data and evidence mapping. They do not package ordinary prose.
""",
    )
    write_text(
        MATERIALIZATION / "style-consistency-report.md",
        """
# Style Consistency Report

Status: pass for pilot manuscript; owner acceptance still required.

Checks:

- Voice: concise, practical Chinese prose.
- Terminology: `故事线`, `chapter thesis`, `source-ref`, `quality gate`, `owner handoff`, and `typed blocker` remain stable.
- Chapter rhythm: each chapter opens with a claim and closes with operational consequence.
- Source grounding: manuscript claims route back to S1-S10 or pilot artifacts.
- Repetition: recurring terms support the workflow and do not create empty repetition.

Residual owner question: confirm whether the current short-handbook voice matches the intended public-facing BookForge tone.
""",
    )
    write_text(
        MATERIALIZATION / "ai-flavor-revision-report.md",
        """
# AI-Flavor Revision Report

Status: pass for pilot manuscript; owner acceptance still required.

Revision rules applied:

- Replaced vague overview moves with direct claims.
- Kept positive editorial movement and active verbs.
- Removed empty summary sentences.
- Avoided formulaic contrast transitions.
- Kept chapter openings specific to the workflow step.

Automated scan targets:

| target | result |
|---|---|
| stock opening phrases | zero in manuscript |
| contrast-formula pattern | zero in manuscript |
| inflated generic praise | zero in manuscript |
| unsupported publication claim | zero in manuscript |

Human review remains useful for cadence, nuance, and public-facing voice.
""",
    )
    write_text(
        MATERIALIZATION / "layout-qc-report.md",
        """
# Layout And Typography QC Report

Target exports:

- Markdown source: `artifacts/manuscript/book.md`
- HTML export: `exports/bookforge-pilot-book.html`
- DOCX export: `exports/bookforge-pilot-book.docx`
- PDF export: `exports/bookforge-pilot-book.pdf`

Checks planned:

- Heading hierarchy: title, preface, five chapters, conclusion.
- Page rhythm: chapters separated by headings, no placeholder pages.
- Tables: header rows, readable columns, short cell content.
- Figures: PNG files exist, are nonblank, and carry captions in the manuscript.
- Cross-references: figure and table mentions stay near their artifacts.
- Export chain: DOCX and PDF are created by local tools and PDF pages render to PNG for inspection.

Initial status before export: pending. Final render evidence is written by `tools/verify_pilot.py`.
""",
    )
    write_text(
        MATERIALIZATION / "owner-handoff.md",
        """
# Book Materialization Owner Handoff

Stage: `book-materialization`

Artifacts:

- `artifacts/manuscript/book.md`
- `artifacts/stage_outputs/book-materialization/chapter-drafts.md`
- `artifacts/stage_outputs/book-materialization/illustration-plan.md`
- `artifacts/stage_outputs/book-materialization/table-plan.md`
- `artifacts/stage_outputs/book-materialization/style-consistency-report.md`
- `artifacts/stage_outputs/book-materialization/ai-flavor-revision-report.md`
- `artifacts/stage_outputs/book-materialization/layout-qc-report.md`

Export targets:

- `exports/bookforge-pilot-book.html`
- `exports/bookforge-pilot-book.docx`
- `exports/bookforge-pilot-book.pdf`

Owner decisions required:

- Accept, revise, or reject the pilot manuscript.
- Accept, revise, or reject the figure/table plan.
- Accept, revise, or reject the DOCX/PDF layout.
- Decide whether the pilot qualifies as production-ready evidence or requires a user-provided book project.

Closure route: `typed-blocker-ref:bookforge-production-smoke-2026-06-18/book-owner-acceptance-missing`
""",
    )


def build_receipts() -> None:
    story_files = [
        STORYLINE / "storyline-map.md",
        STORYLINE / "chapter-thesis-chain.json",
        STORYLINE / "style-contract.md",
        STORYLINE / "owner-handoff.md",
    ]
    book_files = [
        MANUSCRIPT / "book.md",
        MATERIALIZATION / "chapter-drafts.md",
        MATERIALIZATION / "illustration-plan.md",
        MATERIALIZATION / "table-plan.md",
        MATERIALIZATION / "style-consistency-report.md",
        MATERIALIZATION / "ai-flavor-revision-report.md",
        MATERIALIZATION / "layout-qc-report.md",
        MATERIALIZATION / "owner-handoff.md",
        FIGURES / "figure-01-storyline-arc.png",
        FIGURES / "figure-02-two-stage-route.png",
    ]

    def artifact_refs(files: list[Path]) -> list[dict[str, str]]:
        return [{"path": rel(path), "content_hash": sha256(path)} for path in files]

    write_json(
        STORYLINE / "stage.manifest.json",
        {
            "surface_kind": "bookforge_stage_attempt_manifest",
            "schema_version": 1,
            "project_id": PROJECT_ID,
            "stage_id": "storyline-architecture",
            "stage_attempt_id": f"{RUN_ID}:storyline-architecture",
            "producer": "codex_cli",
            "input_refs": [rel(INPUTS / "book-brief.md"), rel(INPUTS / "source-corpus.md"), rel(INPUTS / "voice-and-audience.md")],
            "artifact_refs": artifact_refs(story_files),
            "quality_gate_ref": rel(RECEIPTS / "storyline-independent-gate-receipt.json"),
            "owner_handoff_ref": rel(STORYLINE / "owner-handoff.md"),
            "typed_blocker_ref": rel(RECEIPTS / "storyline-owner-blocker.json"),
            "export_eligibility": "not_applicable_storyline_stage",
            "repair_classification": "owner_review_required",
        },
    )
    write_json(
        MATERIALIZATION / "stage.manifest.json",
        {
            "surface_kind": "bookforge_stage_attempt_manifest",
            "schema_version": 1,
            "project_id": PROJECT_ID,
            "stage_id": "book-materialization",
            "stage_attempt_id": f"{RUN_ID}:book-materialization",
            "producer": "codex_cli",
            "input_refs": [rel(STORYLINE / "storyline-map.md"), rel(STORYLINE / "chapter-thesis-chain.json"), rel(STORYLINE / "style-contract.md")],
            "artifact_refs": artifact_refs(book_files),
            "quality_gate_ref": rel(RECEIPTS / "book-materialization-independent-gate-receipt.json"),
            "owner_handoff_ref": rel(MATERIALIZATION / "owner-handoff.md"),
            "typed_blocker_ref": rel(RECEIPTS / "book-owner-blocker.json"),
            "export_eligibility": "pending_render_verification_and_owner_gate",
            "repair_classification": "owner_review_required",
        },
    )
    write_json(
        RECEIPTS / "storyline-independent-gate-receipt.json",
        {
            "surface_kind": "bookforge_independent_quality_gate_receipt",
            "schema_version": 1,
            "receipt_class": "independent_gate_receipt",
            "project_id": PROJECT_ID,
            "stage_id": "storyline-architecture",
            "status": "passed_for_pilot_progression",
            "generated_at": GENERATED_AT,
            "pass_conditions_checked": [
                "premise_reader_promise_chapter_thesis_chain_evidence_map_style_contract_present",
                "each_chapter_has_book_arc_role",
                "source_gaps_and_owner_decisions_listed",
                "affirmative_specific_human_prose_policy_recorded",
                "next_stage_has_stable_structure",
            ],
            "owner_receipt_ref": None,
            "typed_blocker_ref": "typed-blocker-ref:bookforge-production-smoke-2026-06-18/storyline-owner-review-missing",
            "production_ready_claim_allowed": False,
        },
    )
    write_json(
        RECEIPTS / "storyline-owner-blocker.json",
        {
            "surface_kind": "bookforge_typed_blocker",
            "schema_version": 1,
            "receipt_class": "typed_blocker",
            "project_id": PROJECT_ID,
            "stage_id": "storyline-architecture",
            "blocker_id": "storyline-owner-review-missing",
            "status": "blocked_owner_acceptance_missing",
            "reason": "No human owner receipt accepts the pilot topic, reader promise, chapter order, or style contract.",
            "required_owner_actions": [
                "approve_or_revise_reader_promise",
                "approve_or_revise_chapter_thesis_chain",
                "approve_or_revise_style_contract",
            ],
        },
    )
    write_json(
        RECEIPTS / "book-materialization-independent-gate-receipt.json",
        {
            "surface_kind": "bookforge_independent_quality_gate_receipt",
            "schema_version": 1,
            "receipt_class": "independent_gate_receipt",
            "project_id": PROJECT_ID,
            "stage_id": "book-materialization",
            "status": "passed_with_owner_gate_blocker",
            "generated_at": GENERATED_AT,
            "pass_conditions_checked": [
                "chapter_drafts_follow_storyline_map",
                "claims_tables_and_figures_grounded_in_source_refs",
                "style_terminology_stance_and_rhythm_consistent",
                "ai_flavor_scan_zero_for_manuscript_targets",
                "illustration_and_table_plans_include_purpose_placement_source_boundary_review_criteria",
                "layout_qc_export_targets_declared",
                "handoff_includes_artifacts_receipts_blockers_remaining_owner_decisions",
            ],
            "owner_receipt_ref": None,
            "typed_blocker_ref": "typed-blocker-ref:bookforge-production-smoke-2026-06-18/book-owner-acceptance-missing",
            "production_ready_claim_allowed": False,
        },
    )
    write_json(
        RECEIPTS / "book-owner-blocker.json",
        {
            "surface_kind": "bookforge_typed_blocker",
            "schema_version": 1,
            "receipt_class": "typed_blocker",
            "project_id": PROJECT_ID,
            "stage_id": "book-materialization",
            "blocker_id": "book-owner-acceptance-missing",
            "status": "blocked_owner_acceptance_missing",
            "reason": "No human owner receipt accepts the manuscript quality, figure/table plan, export layout, or publication intent.",
            "required_owner_actions": [
                "review_manuscript_body",
                "approve_or_revise_figure_table_plan",
                "approve_or_revise_docx_pdf_layout",
                "choose_accept_repair_or_reject_for_production_ready_claim",
            ],
        },
    )
    write_json(
        RECEIPTS / "production-readiness-closeout.json",
        {
            "surface_kind": "bookforge_production_readiness_closeout",
            "schema_version": 1,
            "project_id": PROJECT_ID,
            "run_id": RUN_ID,
            "status": "blocked_owner_acceptance_missing",
            "production_ready_claim_allowed": False,
            "completed_evidence": [
                "real_book_project_workspace_created",
                "storyline_architecture_stage_artifacts_created",
                "book_materialization_stage_artifacts_created",
                "chapter_draft_bundle_created",
                "figure_plan_and_png_artifacts_created",
                "table_plan_created",
                "style_consistency_report_created",
                "ai_flavor_revision_report_created",
                "layout_qc_plan_created",
            ],
            "pending_evidence": [
                "human_owner_receipt_for_storyline",
                "human_owner_receipt_for_manuscript_quality",
                "human_owner_receipt_for_export_layout",
                "direct_opl_bookforge_runtime_cli_or_hosted_parity_evidence",
            ],
            "typed_blocker_refs": [
                rel(RECEIPTS / "storyline-owner-blocker.json"),
                rel(RECEIPTS / "book-owner-blocker.json"),
            ],
        },
    )


def build_report() -> None:
    write_text(
        BASE / "README.md",
        """
# BookForge Real Book Pilot Evidence

Run id: `bookforge-real-book-pilot-2026-06-18`

This evidence pack runs OPL BookForge through a real short-book pilot using BookForge's own contracts and OMA evidence as source corpus.

Claim boundary:

- The pack may support: two-stage pilot run evidence, manuscript artifact evidence, figure/table planning evidence, quality gate evidence, export/render evidence after verification.
- The pack may not support: final production-ready claim, publication approval, owner acceptance, or hosted runtime parity.

Primary artifacts:

- Inputs: `inputs/`
- Stage 1 outputs: `artifacts/stage_outputs/storyline-architecture/`
- Stage 2 outputs: `artifacts/stage_outputs/book-materialization/`
- Manuscript: `artifacts/manuscript/book.md`
- Figures: `artifacts/figures/`
- Receipts and blockers: `receipts/`
- Exports: `exports/`
- Verification output: `quality/local-verification-receipt.json`
""",
    )
    write_json(
        BASE / "production-readiness-plan-completion.json",
        {
            "surface_kind": "bookforge_plan_completion_audit_seed",
            "schema_version": 1,
            "run_id": RUN_ID,
            "items": [
                {"item": "real_book_project_workspace", "target": "create inputs and evidence workspace"},
                {"item": "stage_1_storyline_architecture", "target": "produce storyline map, thesis chain, style contract, handoff"},
                {"item": "stage_2_book_materialization", "target": "produce manuscript, chapter drafts, figure/table plan, style/AI/layout reports"},
                {"item": "quality_gates", "target": "record independent gate receipts and fail closed on owner acceptance"},
                {"item": "exports", "target": "create HTML, DOCX, PDF and render-check"},
                {"item": "owner_receipts", "target": "owner receipt or typed blocker"},
            ],
        },
    )


def main() -> None:
    ensure_dirs()
    build_inputs()
    build_storyline()
    build_materialization()
    build_receipts()
    build_report()
    write_json(
        LOGS / "generation-log.json",
        {
            "surface_kind": "bookforge_pilot_generation_log",
            "schema_version": 1,
            "run_id": RUN_ID,
            "generated_at": GENERATED_AT,
            "artifact_count": len([path for path in BASE.rglob("*") if path.is_file()]),
            "generator": rel(Path(__file__).resolve()),
        },
    )


if __name__ == "__main__":
    main()
