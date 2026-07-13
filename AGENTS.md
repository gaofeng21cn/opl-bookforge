<INSTRUCTIONS>
你始终用中文回复。

本仓是 OPL Book Forge 的 OPL 标准 Foundry Agent 领域包。修改前先读取相关 `contracts/`、`agent/`、`docs/` 与验证入口，结论以 fresh OPL validator 输出为准。

核心边界：
- 产品名：`OPL Book Forge`。
- repo slug / domain_id / foundry_agent_id：`opl-bookforge`。
- 本仓当前目标是书籍写作智能体的标准结构基线，不能把 scaffold/interface 通过声明为 production ready、book delivery ready、质量通过、出版通过或 owner acceptance。
- OPL 拥有生成接口、runtime 投影和通用框架；OPL Book Forge 拥有领域真相、书稿质量、导出/出版裁决、记忆正文和 owner receipts。
- 不在本仓实现通用 OPL runtime、queue、attempt ledger、generic scheduler、app shell 或手写默认入口。
- `agent/primary_skill/SKILL.md` 是标准 OPL Agent 的 canonical rich primary skill；`plugins/<agent>/skills/<agent>/SKILL.md` 是 Codex plugin 安装要求的 materialized full-skill carrier mirror。该关系以 `contracts/capability_map.json` 中的 `carrier_projection_contract` 为机器权威；两者字节相同表示同步健康，不表示应删除重复，mirror 漂移才是问题。
- OPL canonical agent/package id 固定为 `obf`；`opl-bookforge` 只作为 repo slug、`domain_id`、`foundry_agent_id`、npm package name 和 Codex plugin/现有 distribution carrier locator，不得通过 alias 维持第二个 package identity。

验证入口：
- `scripts/verify.sh` / `scripts/verify.sh fast`：默认快速 policy lane。
- `scripts/verify.sh structural`：policy 加 OPL scaffold/interfaces/source-hygiene readback。
- `scripts/verify.sh helpers`：native-helper probe 与 PDF/image adapter 单元测试。
- `scripts/verify.sh pdf`：两条真实 Pandoc/XeLaTeX compile/render E2E。
- `scripts/verify.sh full`：上述 lane 的去重并集。
- 或分别运行：
  - `/Users/gaofeng/workspace/one-person-lab/bin/opl agents scaffold --validate . --json`
  - `/Users/gaofeng/workspace/one-person-lab/bin/opl agents interfaces --repo-dir . --json`

维护规则：
- contract/schema/authority 边界变更按 L3 处理，至少跑上面的 OPL scaffold 和 interfaces 验证。
- README、docs、status 只能记录已有 fresh evidence；不要把文档计划包装成 runtime truth。
- 变更范围保持最小，不改其他 OPL 系列仓库，除非用户明确要求。
</INSTRUCTIONS>

<!-- CODEGRAPH_START -->
## CodeGraph

- 本仓库使用本地 `.codegraph/` 索引；该目录不得纳入 Git。
- 定义、调用、影响范围和代码路径等结构检索优先使用 CodeGraph；字面文本检索使用 `rg`。
- 索引缺失或过期时运行 `codegraph init .` 或 `codegraph sync .`。
<!-- CODEGRAPH_END -->
