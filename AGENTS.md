# OPL Book Forge

本仓是 OPL 的书籍写作 Foundry Agent 领域包，canonical package id 为 `obf`。

- OPL Book Forge 持有书稿 truth、质量、导出/出版 verdict、领域记忆和 owner receipts。
- OPL Framework 持有通用 runtime、generated interfaces 和 shared lifecycle。
- Agent identity、capabilities 与 authority 以 `agent/` 和 `contracts/` 为准。

默认验证入口：`scripts/verify.sh`。

<!-- CODEGRAPH_START -->
## CodeGraph

- 本仓库使用本地 `.codegraph/` 索引；该目录不得纳入 Git。
- 定义、调用、影响范围和代码路径等结构检索优先使用 CodeGraph；字面文本检索使用 `rg`。
- 索引缺失或过期时运行 `codegraph init .` 或 `codegraph sync .`。
<!-- CODEGRAPH_END -->
