# TASTE

Owner: `opl-bookforge`
Purpose: 记录 OPL Book Forge 的本地维护偏好。
State: `active_preference`
Machine boundary: 本文是协作偏好；机器真相以 `contracts/`、OPL validator 输出、runtime receipts 和 owner receipts 为准。

## 偏好

1. **书籍产物优先**

   智能体设计围绕一本书的真实交付展开：故事线、读者承诺、章节论证链、插图和表格计划、写作风格、措辞、排版和质控都服务于可审阅的书稿输出。

2. **Target-First / Substrate-As-Path**

   对 manuscript、book package、export handoff 或 author-facing delivery 任务，真实进度按可审阅书稿、章节/图表/风格 delta、owner decision、human gate 或用户可用结果计算；OPL scaffold、interfaces、runtime、tests、docs 和平台修复只是支持证据。BookForge/OPL 执行基座是首选路径，不是书籍交付的前置条件：基座顺畅时走基座，基座卡住时，前端执行者继续推进合法的书稿或书籍交付增量，并把暴露出的基座问题作为 side repair lane 记录或修复。只有继续动作会越权写 publishing/export authority surface、缺少必要 source/material、或同一写集 ownership 冲突且无法隔离时，才暂停具体目标动作。repair lane 不能吞掉书稿主线，除非用户目标本身就是平台修复。

3. **两阶段主线**

   第一阶段梳理故事线，第二阶段做书籍呈现。不要把流程拆成细碎状态链；阶段应产出可接力的明确交付物和 owner handoff。

4. **AI-first 但 owner-gated**

   执行者可以完成开放式写作、改写、规划和质控，但质量、出版、导出和 owner acceptance 必须由领域 gate 或 owner receipt 支撑。

5. **去 AI 味是质量要求**

   写作检查应偏向肯定表达、具体表达、连贯叙述和人工编辑口吻。避免模板化转折、空泛形容、过度解释和机械化结构。

6. **验证区分结构与产能**

   `scaffold passed` 和 `interfaces ready` 只证明 OPL 标准结构与生成接口可读，不证明已经能交付高质量书稿。
