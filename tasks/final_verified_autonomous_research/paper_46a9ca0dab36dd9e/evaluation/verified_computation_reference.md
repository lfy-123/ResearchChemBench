# 已验证成功计算链：Cat1 六重态 TD / IFCT

- 论文 ID：`paper_46a9ca0dab36dd9e`
- 本任务模式：`autonomous_research`（自主科研模式）
- 论文 DOI：`10.1021/jacs.5c20945`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_4](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_4.md)
- 最新已归档科学状态：当前最高 f 规则由既有 state20/Mulliken-like IFCT 支持（63.541%/3.820%）；下面 state22 分析保留为历史及敏感性证据，不当作当前选态主结果。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_autonomous_research`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../autonomous_research/paper_46a9ca0dab36dd9e)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本自主模式共用同一论文的科学参考链；原有逐项资格审计主要针对作者路线/论文复现模式，不将其写成另一次自主 agent 盲测通过。

## 2. 当前主结果的已完成计算链及历史对照

1. 确认 Cat1 为完整 TEA+·FeCl4−、34 原子、中性六重态；片段固定为 Cl31–34、Fe30、TEA1–29，后续分析保持相同原子顺序。

2. 完成作者 B3LYP-D3(BJ)/6-31G(d)（轻元素）–SDD（Fe）、SMD 乙腈的 Gaussian Opt/Freq；输出 96 实频、0 虚频。实际显式基组和 ECP 区块见原始 input.com。

3. 在同一优化几何上运行 UM06-GD3、6-311+G(d,p)（轻元素）/SDD（Fe）、SMD 乙腈 TD30，保留全部 30 态与展开。当前按最高振子强度物理准则选态：本输出最高 f 为第 20 态（0.0415），第 21/22 态分别为 0.0299/0.0237。历史曾按论文编号选择第 22 态，该分支仅保留作对照，不作为当前主结果。

4. 当前主链采用已完成的第 20 态 Mulliken-like Multiwfn IFCT（2026.7.15，4 CPU），读取同一 TD30 波函数，按 Cl31–34、Fe30、TEA1–29 分片，使用所有片段通道的同一归一化。原始表中 Cl→Fe=0.63541、Fe→Cl=0.03820，乘以 100 后分别为 63.541%/3.820%；两项不能重新归一化成和为 100%。输入命令、fchk 和输出见第 4 节的 20 Mulliken-like IFCT 行。

5. 已完成的辅助分支包括第 21/22 态 Mulliken-like IFCT，以及第 22 态 Hirshfeld IFCT（75 径向×434 角向网格）。命令文件、fchk/settings 与原始输出均在下方证据表。检查三片段转移与守恒，披露 Mulliken-like 的微小负 TEA hole 贡献；这些分支不替代最高 f 主态。

6. 当前以第 20 态 Mulliken-like LMCT/MLCT 对照原 evaluator 的 62.4±10/4.3±5 个百分点，差值分别为 +1.141/−0.480 个百分点，支持 LMCT 主导。历史第 22 态结果及第 21 态只提供选态/分区敏感性对照，不扩展成整个 carborane 光反应复现。

## 3. 实际结果与支持的结论

| 指标 | 实际结果 | 参考/备注 |
|---|---:|---|
| state 22 能量 / 波长 / f | 3.2676 eV / 379.44 nm / 0.0237 | S²=8.78 |
| state 22 Hirshfeld LMCT / MLCT | 62.060% / 4.103% | 62.4±10 / 4.3±5 个百分点 |
| state 22 Mulliken-like LMCT / MLCT | 62.492% / 4.351% | TEA hole 有 −0.03% 小负贡献 |
| state 20 Mulliken-like LMCT / MLCT | 63.541% / 3.820% | 当前最高 f 主结果；62.4±10 / 4.3±5 个百分点 |
| state 21 Mulliken-like LMCT / MLCT | 62.061% / 4.445% | 交叉检查 |

三态均支持 LMCT 主导；计算亮度为 20>21>22，与 SI 22>20>21 不同。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| minimum | [input.com](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/hpc_runs/cat1_author_b3lyp_d3bj_optfreq_hpc20_p3__resubmit_001/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/hpc_runs/cat1_author_b3lyp_d3bj_optfreq_hpc20_p3__resubmit_001/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| td30 | [input.com](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/hpc_runs/cat1_m06_gd3_source_parent_td30_20260914_hpc20_p6/input.com) | [stdout.log](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/hpc_runs/cat1_m06_gd3_source_parent_td30_20260914_hpc20_p6/stdout.log) | Gaussian 正常终止标记 1 处 |
| 22 Hirshfeld IFCT | [state22_hirshfeld_clean_commands.txt (1)](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/state22_hirshfeld_clean_commands.txt)<br>[wavefunction.fchk (2)](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/td30.fchk)<br>[settings.ini (3)](../../../../.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/settings.ini) | [stdout.log](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/state22_hirshfeld_clean/stdout.log) | 采用已审计的分析结果；进程/菜单边界见下文 |
| 22 Mulliken-like IFCT | [state22_mulliken_clean_commands.txt (1)](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/state22_mulliken_clean_commands.txt)<br>[wavefunction.fchk (2)](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/td30.fchk)<br>[settings.ini (3)](../../../../.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/settings.ini) | [stdout.log](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/state22_mulliken_clean/stdout.log) | 采用已审计的分析结果；进程/菜单边界见下文 |
| 20 Mulliken-like IFCT | [state20_mulliken_commands.txt (1)](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/state20_mulliken_commands.txt)<br>[wavefunction.fchk (2)](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/td30.fchk)<br>[settings.ini (3)](../../../../.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/settings.ini) | [stdout.log](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/state20_mulliken/stdout.log) | 采用已审计的分析结果；进程/菜单边界见下文 |
| 21 Mulliken-like IFCT | [state21_mulliken_commands.txt (1)](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/state21_mulliken_commands.txt)<br>[wavefunction.fchk (2)](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/td30.fchk)<br>[settings.ini (3)](../../../../.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/settings.ini) | [stdout.log](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/multiwfn_ifct_20260915/state21_mulliken/stdout.log) | 采用已审计的分析结果；进程/菜单边界见下文 |

## 5. 后处理、结果与逐项核验依据

- [provenance/ifct_closure_20260915.json](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/ifct_closure_20260915.json)
- [provenance/evaluation_task_qualification.json](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/evaluation_task_qualification.json)
- [report/results.json](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/report/results.json)
- [verification_report.md](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/verification_report.md)
- [prepare_source_td_20260914.py](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/prepare_source_td_20260914.py)
- [run_multiwfn_ifct_20260915.py](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/run_multiwfn_ifct_20260915.py)
- [finalize_ifct_20260915.py](../../../../docs/verification/group_4/paper_46a9ca0dab36dd9e/finalize_ifct_20260915.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- 实际 Multiwfn 并非作者 3.8dev 原始 build；保持 IFCT 方法/公式一致而不声称历史可执行文件一致。SI 未指定原子布居划分；当前主比较采用已获批准的 Mulliken-like 口径，历史 Hirshfeld 结果仅作分区敏感性对照。
- Cl 组内部项合并局部与 Cl 间贡献，不把它解释成已分辨的单配体 LCCT/LLCT。
- 第 22 态代表性与最亮态是不同概念；states 4–6 也存在 f>0.01，完整 30 态结果不删选。

## 7. 成功阶段计时

两个 Gaussian 主作业均 20 CPU，elapsed 为 1259.1/1303.6 s，合计 2562.7 s（42.71 min），CPU 50109.1 s（13.9192 核时）。Multiwfn 各次独立 4 CPU，后处理耗时另见其执行记录。

本次归档没有提交、重启或停止任何计算作业。


## 当前获准的选态口径（非新增计算）

SI S34–S35 按最高振子强度选择代表态，而非固定编号。现有 TD30 的最大 f 在 state20；既有 `docs/verification/group_4/paper_46a9ca0dab36dd9e/provenance/ifct_closure_20260915.json` 索引保留其 Mulliken-like LMCT=63.541%、MLCT=3.820%，满足原数值范围。此前分析 state22 的历史仍按其真实编号保留，不能当成按最高 f 规则选出的主态。本次没有新 TD/IFCT 计算；主布居口径为负责人批准的比较定义。
