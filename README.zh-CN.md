# OPL BookForge

OPL BookForge 是 OPL 系列的标准 Foundry Agent 领域包，用于写书。仓库名、`domain_id` 和 `foundry_agent_id` 使用 `opl-bookforge`，产品名使用 `OPL BookForge`。

核心工作流分两段：

- `storyline-architecture`：梳理故事线、读者承诺、论证弧线、材料地图、章节论点链和写作风格契约。
- `book-materialization`：把书物化为章节草稿、插图规划、表格规划、风格一致性检查、版式检查和 owner-gated handoff refs。

本仓是声明式领域包和最小 authority function surface。OPL 负责生成接口和框架 runtime 投影；OPL BookForge 负责领域真相、书稿质量和导出/出版裁决、产物权威、记忆正文和 owner receipts。

## 验证

运行：

```bash
scripts/verify.sh
```

当前结构基线证据：

- `opl agents scaffold --validate . --json`：passed
- `opl agents interfaces --repo-dir . --json`：ready

这些证据只证明 OPL 标准结构基线和生成接口描述符可用，不证明生产可用、能交付合格书稿、可出版或已获得 owner acceptance。
