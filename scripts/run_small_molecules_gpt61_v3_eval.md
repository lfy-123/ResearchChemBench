# 小分子 V3：六篇任务的 ARCHE / Codex 运行命令

日期：2026-10-26。

任务来源为 `tasks/small_molecules_verified_autonomous_research/` 顶层的 14 篇任务，本批选择下列六篇。使用每篇当前的公开任务输入及 `evaluation/scoring_rules.json`，评分策略为 `paper_science_v3`，运行时模式为 `final_results_100`。

| Case | 论文 ID |
|---|---|
| case01 | paper_a3892396b1843698 |
| case02 | paper_8fefc96b015c4577 |
| case03 | paper_cf8ce1fc0fbcd300 |
| case04 | paper_3c3d73b8715d5fcd |
| case05 | paper_1db677efcdd782ac |
| case06 | paper_32dea3515c2c7240 |

## 配置与输出

- Agent 和 Judge 均为 `gpt-6.1-sol`，推理强度均为 `high`，沿用已有本地 API 配置。
- ARCHE：初始生成 3 × 2 = 6 个候选假设，仅选 Top 1 进行调查，一批假设；关闭外部论文搜索。此设置针对带 `--v3` 的新运行。
- 每次运行分配 48 CPU 核、204800 MiB 内存（200 GiB），总时限 345600 秒（4 天），单个计算动作上限 86400 秒（1 天）。建议每台服务器启动一个任务。
- ARCHE 输出：`workspaces/arche_gpt61_high_small_molecules_v3/`。
- Codex 输出：`workspaces/codex_gpt61_high_small_molecules_v3/`。
- 每次新运行都创建 `paper_<ID>_<UTC时间>_<随机标识>/`，与历史结果隔离。重复执行新运行命令会创建另一轮评估；中断后应指定原结果目录 resume。
- `--v3` 会在启动前拒绝非 `paper_science_v3` 的任务包。评分策略由包内规则选择，既有评分条目和权重原样使用。
- 运行时完整复制单个任务包以满足现有入口的目录布局，校验 manifest，并记录来源、内容哈希及评分策略到新输出根目录的 `.runtime/task_sources/<标识>/source.json`。Agent 只接收公开输入，私有评分参考交给 Judge。
- Codex 的 V3 新运行启用现有有界自动恢复；服务器关闭后的恢复仍需指定原结果目录。保留结果目录及 `.runtime`。

## 运行命令

先在各服务器进入项目目录；下面每一行都是一个独立任务，可以分别在不同服务器运行。

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench
```

ARCHE，按 case01 → case06 排列：

```bash
bash scripts/run_small_molecules_gpt61_eval.sh --v3 arche paper_a3892396b1843698
bash scripts/run_small_molecules_gpt61_eval.sh --v3 arche paper_8fefc96b015c4577
bash scripts/run_small_molecules_gpt61_eval.sh --v3 arche paper_cf8ce1fc0fbcd300
bash scripts/run_small_molecules_gpt61_eval.sh --v3 arche paper_3c3d73b8715d5fcd
bash scripts/run_small_molecules_gpt61_eval.sh --v3 arche paper_1db677efcdd782ac
bash scripts/run_small_molecules_gpt61_eval.sh --v3 arche paper_32dea3515c2c7240
```

Codex，顺序相同：

```bash
bash scripts/run_small_molecules_gpt61_eval.sh --v3 codex paper_a3892396b1843698
bash scripts/run_small_molecules_gpt61_eval.sh --v3 codex paper_8fefc96b015c4577
bash scripts/run_small_molecules_gpt61_eval.sh --v3 codex paper_cf8ce1fc0fbcd300
bash scripts/run_small_molecules_gpt61_eval.sh --v3 codex paper_3c3d73b8715d5fcd
bash scripts/run_small_molecules_gpt61_eval.sh --v3 codex paper_1db677efcdd782ac
bash scripts/run_small_molecules_gpt61_eval.sh --v3 codex paper_32dea3515c2c7240
```

在任一命令末尾加 `--dry-run` 可进行本地预检，不调用 Agent、Judge 或化学计算；预检不验证 API 余额、连通性或 ARCHE 实际沙箱服务启动。

## 恢复已有 V3 运行

同一服务器恢复时，将下方占位路径替换为启动日志中的实际结果目录：

```bash
bash scripts/run_small_molecules_gpt61_eval.sh --v3 arche --resume workspaces/arche_gpt61_high_small_molecules_v3/paper_ID_时间_标识
bash scripts/run_small_molecules_gpt61_eval.sh --v3 codex --resume workspaces/codex_gpt61_high_small_molecules_v3/paper_ID_时间_标识
```

跨服务器恢复继续使用已有 `--migrate-from-host 原主机完整名称` 机制；仅在原实例已停止后使用，Codex 还需满足冻结的 CLI 版本与环境校验。恢复使用原运行保存的任务和评分版本，不会把旧版本运行升级成 V3。

V3 中允许 `need_review` 的条目可能产生待裁定分。报告应同时读取已确认分、待裁定分和整题结论，不能把待裁定分当成已得分。

## 本地检查结果

六篇 × 两种 Agent 共 12 组最终配置均通过预检；任务快照与源包逐文件一致，均成功加载 V3 评分。ARCHE 最终配置为 6 个候选 / Top 1。相关启动与 V3 评分测试共 64 项通过。本次没有启动正式评估；检查产生的临时预检目录已清理。

检查记录：[小分子V3_六题启动检查_20261026.json](../docs/handle/小分子V3_六题启动检查_20261026.json)。
