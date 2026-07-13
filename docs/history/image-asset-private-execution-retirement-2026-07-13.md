<!--
Owner: `opl-bookforge`
Purpose: `retired_image_asset_execution_route_provenance`
State: `history_tombstone`
Machine boundary: 仅保留人读迁移来历；当前机器真相见 contracts/image_asset_host_handoff.json 与 contracts/domain_handler_registry.json。
-->

# 图像资产私有执行路径退役记录

2026-07-13，OPL Book Forge 退役了 `runtime/native_helpers/bookforge_imagegen_asset.py` 中由领域仓自行执行图像生成的路径。

旧实现会构造 executor request、写入临时请求文件、启动 `opl executor run`、解析 executor receipt，并写入 bitmap、receipt 与 asset manifest 状态。这些职责属于通用执行、attempt/output 绑定和持久化边界，不应由领域包重复实现。

替代实现是只读的 Book Forge authority handler。OPL 负责图像生成、transport、workspace output slot、bitmap materialization、attempt/output refs 与 candidate persistence；Book Forge 只消费 host 注入的 bitmap ref、SHA-256 和 figure metadata，校验领域相关资产属性，并返回 figure-authority receipt candidate 或 quality debt。

同一迁移中还删除了历史 project-hygiene 实现。source、package payload、verification、generated/default caller、`rg` 与 CodeGraph 复核均未发现 operational active caller；它原有的通用 source/lifecycle 检查由 OPL 持有，领域 voice/style/source/figure/proof 规则继续由 Book Forge skills、quality gates、artifact contracts 与 PDF helper 持有。Red Bird 特定实现仅在 Git 历史中保留 provenance，不再作为 active package surface。
