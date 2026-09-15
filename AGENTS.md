# OPL Book Forge

本仓是书籍写作 domain agent；`contracts/opl_agent_package_manifest.json` 定义 `agent_id/package_id=obf`，领域能力以 `agent/` 与 `contracts/` 为准。

- Book Forge 持有书稿 truth、质量、导出/出版 verdict、领域记忆和 owner receipts；Framework 只提供通用 runtime、transport 与 generated interfaces。
- `agent/primary_skill/SKILL.md` 是主路由；carrier、executor 和运行 receipt 不取得书稿或出版 authority。
- Package release integrity、execution evidence 与书稿/出版 owner receipt 是不同证据面，互不替代。
- 文档职责与生命周期归 `docs/README.md`；当前证据归 `docs/status.md`。仅为已证实的未完成实现创建有明确结束条件的计划，完成后移除。已退役且无调用者的入口和兼容清单直接删除，不保留别名。
- 默认验证运行 `scripts/verify.sh`；书稿或出版交付还须验证最终 artifact bytes 和 owner gate。

<!-- CODEGRAPH_START -->
## CodeGraph

- 本仓库使用本地 `.codegraph/` 索引；该目录不得纳入 Git。
- 定义、调用、影响范围和代码路径等结构检索优先使用 CodeGraph；字面文本检索使用 `rg`。
- 索引缺失或过期时运行 `codegraph init .` 或 `codegraph sync .`。
<!-- CODEGRAPH_END -->

- 软件包发布统一使用 OPL OCI 流程和标准安装入口，不创建或保留独立 GitHub Release 页面及附件。共享规则由 Framework 的 docs/delivery/artifact-package-lifecycle-boundary.md 持有。
