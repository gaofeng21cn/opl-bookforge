# OPL Book Forge

本仓是 OPL 的书籍写作 Foundry Agent，也是 `OPL Package(kind=agent)`；canonical package id 为 `obf`。

- OPL Book Forge 持有书稿 truth、质量、导出/出版 verdict、领域记忆和 owner receipts。
- Package identity、capabilities、业务任务和 typed views 保持 executor-neutral；Codex Plugin 只是当前 carrier projection，Codex CLI 只是当前 executor。
- OPL Book Forge owner 独立发布完整 Package bytes 到自己的 GHCR `latest-stable`。普通依赖只检查 identity presence 与所需 capability callability，不以跨包 version/ABI、lock、payload、digest、Release Set 或原子闭包为门。
- OPL Framework 持有通用 runtime、generated interfaces 和跨 carrier fresh readback 聚合，不得成为第二套 OBF Package Manager。
- Package release integrity、运行 execution receipt 与书稿/出版 owner receipt 是不同证据面，互不替代。
- Agent identity、capabilities 与 authority 以 `agent/` 和 `contracts/` 为准。
- 当前机器合同仍可能保留旧 lifecycle 字段；迁移完成前不得把本文目标边界声称为已实现。

默认验证入口：`scripts/verify.sh`。

<!-- CODEGRAPH_START -->
## CodeGraph

- 本仓库使用本地 `.codegraph/` 索引；该目录不得纳入 Git。
- 定义、调用、影响范围和代码路径等结构检索优先使用 CodeGraph；字面文本检索使用 `rg`。
- 索引缺失或过期时运行 `codegraph init .` 或 `codegraph sync .`。
<!-- CODEGRAPH_END -->
