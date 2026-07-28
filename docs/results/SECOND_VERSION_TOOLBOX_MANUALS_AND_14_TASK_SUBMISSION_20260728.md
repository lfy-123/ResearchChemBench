# 化学工具箱第二版手册、验证与任务提交总结

日期：2026-07-28

## 总结

56 个原生软件条目均已建立英文结构化目录。除 EasySpin 和 MATLAB 两个缺少合法运行宿主与许可的占位条目外，54 个可调用软件均包含详细 `INDEX.md`、`QUICKSTART.md`、`COMMON_TASKS.md`、`TROUBLESHOOTING.md` 和 `examples/interface_smoke/`。全部软件均已建立逐项 smoke 记录，代表性 Flash 任务在修复运行数据库、GoodVibes 参数说明和构象 lineage 契约后通过完整验证，其余 13 个任务已提交且不再监督。

## 软件手册与测试

| 项目 | 结果 |
|---|---:|
| 软件目录 | 56 |
| 详细 QUICKSTART / COMMON_TASKS / TROUBLESHOOTING | 各 54 |
| 第一方 Markdown | 234 |
| 示例与 smoke 结果文件 | 168 |
| smoke 通过 | 40 |
| executable 已启动但需要真实科学输入 | 11 |
| 明确失败 | 3 |
| 许可占位跳过 | 2 |
| 工具箱完整测试 | 329 passed，399.70 s |
| 最终合同针对性测试 | 30 passed |

明确失败项为 Arkane、RMG 和 VESTA。Arkane/RMG 在 180 秒接口 smoke 截止前没有进入终态并被取消；VESTA 到达 wrapper，但 GUI 缺少 `libxkbcommon.so.0`。EasySpin 和 MATLAB 因 MATLAB host/license 不可用而跳过。以上状态均保留为真实证据，没有标记为伪成功。

Smoke 证据：`chemistry_toolbox/evidence/native_interface_smoke/20260728_all_software/manifest.json`。

## 代表任务验证

代表任务：`GEOM_Hierarchical_Conformer_Reranking_Reproduction`

最终运行目录：`workspaces/second_version_results/representative_final/runs/cli_runs/batch_20260728_230500_0e7ed2/GEOM_Hierarchical_Conformer_Reranking_Reproduction_opencode_20260728_230500_e09d41/`

| 指标 | 结果 |
|---|---:|
| Agent / Judger | deepseek-v4-flash / deepseek-v4-flash |
| 运行时间 | 2407.297 s |
| MCP 调用 | 37 |
| 成功 / 失败 | 35 / 2 |
| 受管科学尝试 | 24 |
| 科学结论分 | 100 |
| 科研过程分 | 86 |
| 最终分 | 86 |
| Agent model steps | 51 |
| Agent input / output / reasoning tokens | 186950 / 23272 / 10503 |
| Agent cache-read tokens | 6540032 |
| Agent 总 tokens | 6760757 |
| Judger tokens | 86384 |

最终轨迹实际执行了 4 次 RDKit ETKDG、1 次有效 CREST GFN2-xTB 搜索、8 次 ORCA r2SCAN-3c/CPCM(water) 优化、8 次 ORCA Hessian 和 1 次 GoodVibes ensemble 分析。GoodVibes 使用 `population_basis=quasi_harmonic_gibbs`、`entropy_model=grimme`、100 cm-1 cutoff，并生成归一化 Gibbs 人口。8 个精修构象均无显著虚频，lineage 逐行记录 28 个原子的显式映射及对应 ORCA/GoodVibes artifact。

模型恢复了论文结论：CREST 与准谐 Gibbs 排名的 Spearman 相关系数为 0.214，主构象由 CREST 的 `crest_conf_001` 变为 Gibbs 排名的 `crest_conf_004`。Judger 未报告 critical failure 或 evidence gate failure。

早期验证暴露并解决了三类问题：共享文件系统上的 OpenCode SQLite 导致 `SIGBUS`；GoodVibes 电子能人口被错误描述为 Gibbs 人口；构象 lineage 缺少逐原子映射和逐行 artifact。最终运行的数据库已归档到 `_opencode/opencode.db`，没有残留 ORCA、CREST 或 Supervisor 进程。

## 14 个任务提交

| 序号 | 任务名称 | 提交位置 |
|---:|---|---|
| 1 | `GEOM_Hierarchical_Conformer_Reranking_Reproduction` | `workspaces/second_version_results/representative_final/`，已完成并监督 |
| 2 | `GEOM_Hierarchical_Conformer_Reranking` | `workspaces/second_version_results/remaining_13/` |
| 3 | `Electron_Flexible_Ensemble_Surface` | `workspaces/second_version_results/remaining_13/` |
| 4 | `Electron_Flexible_Ensemble_Surface_Reproduction` | `workspaces/second_version_results/remaining_13/` |
| 5 | `Electron_Isodensity_04_Blind_Prediction` | `workspaces/second_version_results/remaining_13/` |
| 6 | `Electron_Isodensity_Reproduction_04_Blind_Prediction` | `workspaces/second_version_results/remaining_13/` |
| 7 | `PV_Protonation_Barrier_Trend` | `workspaces/second_version_results/remaining_13/` |
| 8 | `PV_Protonation_Barrier_Trend_Reproduction` | `workspaces/second_version_results/remaining_13/` |
| 9 | `BaO_Phase_Crossover_And_5d_Bonding` | `workspaces/second_version_results/remaining_13/` |
| 10 | `BaO_Phase_Crossover_And_5d_Bonding_Reproduction` | `workspaces/second_version_results/remaining_13/` |
| 11 | `Heterobiaryl_PV_02_CC_Selectivity` | `workspaces/second_version_results/remaining_13/` |
| 12 | `Heterobiaryl_PV_Reproduction_02_CC_Selectivity` | `workspaces/second_version_results/remaining_13/` |
| 13 | `Heterobiaryl_PV_05_Rate_Determining_Step` | `workspaces/second_version_results/remaining_13/` |
| 14 | `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step` | `workspaces/second_version_results/remaining_13/` |

剩余 13 个任务的 tmux session 为 `rcb_second_v_remaining_20260728`，Agent 与 Judger 均为 `deepseek-v4-flash`。按照要求，任务提交后未继续监督。

## Git 记录

| Commit | 内容 |
|---|---|
| `9e738bb` | 扩展原生软件手册和 smoke 覆盖 |
| `16c433a` | 稳定 OpenCode 数据库存储与归档 |
| `f956019` | 加强 GEOM 复现证据契约 |
| `798b87e` | 明确 Gibbs 人口和构象 lineage 契约 |
