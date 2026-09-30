# 已验证成功计算链：free / PO / PA 接触、电荷与 ESP

- 论文 ID：`paper_ef26687d63a37e29`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1021/acs.macromol.5c03427`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_1](../../../../docs/verification/group_1/paper_ef26687d63a37e29)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_1.md)
- 最新已归档科学状态：READY / PASS / QUALIFIED（完整 free / PO / PA 三体系）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_ef26687d63a37e29)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 按正文 Figure 6/SI 核对 free、PO、PA，分别 46、56、61 原子，均为中性单重态。PA 必须是含完整芳环的 C20H34N3O3P；历史缺环 51 原子模型不纳入有效链。

2. 三体系分别完成 B3LYP-D3BJ/6-31G(d) 气相 Opt/Freq；依次得到 132、162、177 个正频率且无虚频。free/PO 复用既有正确成功端点，PA 使用完整身份端点。

3. 由最终结构按原子索引识别 PO 氧及 PA 羧酸盐氧，并测量 O···P、O···αH、O···βH。αH 定义为 N–CH2 氢，βH 为末端 CH3 氢，不误用不存在的直接 P–C 乙基连接。

4. 将相应 checkpoint 转为 fchk，使用原生 Multiwfn 提取 ADCH；保留所有 N-ethyl H 电荷、P 电荷、原子映射和最近接触 H 的单独电荷。

5. 在同一波函数上作有符号 ESP 表面分析，保留表面顶点、极值/区域和可视化产物，区分电势与电子密度。PA 采用完整成功的 stackfix 后处理；改变的是运行栈配置，不是电子结构或 ESP 算法。

6. 汇总六个接触距离、三个 P 电荷和完整氢/ESP 证据，对照修订后已验证的 15 条规则及两个结论，不缩小三体系范围。

## 3. 实际结果与支持的结论

| 量 | free | PO | PA |
|---|---:|---:|---:|
| 实频数 | 132 | 162 | 177 |
| P ADCH / e | −0.018993 | 0.447060 | 0.455684 |
| O···P / Å | 不适用 | 1.82926200 | 2.65221031 |
| O···αH / Å | 不适用 | 2.12509271 | 2.31179702 |
| O···βH / Å | 不适用 | 2.44046988 | 2.36329056 |

完整各 H 电荷与 ESP 数据见原结果和下表 Multiwfn 产物；这些结果支持限定孤立中间体模型的相互作用解释，不等于完整聚合反应验证。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| free Opt/Freq | [input.com](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_si_recovered_v2_hpc_685c4cb0/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_si_recovered_v2_hpc_685c4cb0/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| free ADCH | [Et2N3P_si_recovered_v2_hpc_685c4cb0.fchk](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_si_recovered_v2_hpc_685c4cb0/multwfn_adch_mep/Et2N3P_si_recovered_v2_hpc_685c4cb0.fchk) | [multiwfn_adch.out](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_si_recovered_v2_hpc_685c4cb0/multwfn_adch_mep/multiwfn_adch.out) | 采用已审计的分析结果；进程/菜单边界见下文；历史菜单 EOF 不抹去已完成科学表格；仅使用逐项审计确认的 ADCH/ESP 产物，不声称进程干净退出。 |
| free ESP | [Et2N3P_si_recovered_v2_hpc_685c4cb0.fchk](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_si_recovered_v2_hpc_685c4cb0/multwfn_adch_mep/Et2N3P_si_recovered_v2_hpc_685c4cb0.fchk) | [multiwfn_mep.out](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_si_recovered_v2_hpc_685c4cb0/multwfn_adch_mep/multiwfn_mep.out) | 采用已审计的分析结果；进程/菜单边界见下文；历史菜单 EOF 不抹去已完成科学表格；仅使用逐项审计确认的 ADCH/ESP 产物，不声称进程干净退出。 |
| PO Opt/Freq | [input.com](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| PO ADCH | [Et2N3P_PO_si_recovered_v2_hpc_6e9ad747.fchk](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747/multwfn_adch_mep/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747.fchk) | [multiwfn_adch.out](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747/multwfn_adch_mep/multiwfn_adch.out) | 采用已审计的分析结果；进程/菜单边界见下文；历史菜单 EOF 不抹去已完成科学表格；仅使用逐项审计确认的 ADCH/ESP 产物，不声称进程干净退出。 |
| PO ESP | [Et2N3P_PO_si_recovered_v2_hpc_6e9ad747.fchk](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747/multwfn_adch_mep/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747.fchk) | [multiwfn_mep.out](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747/multwfn_adch_mep/multiwfn_mep.out) | 采用已审计的分析结果；进程/菜单边界见下文；历史菜单 EOF 不抹去已完成科学表格；仅使用逐项审计确认的 ADCH/ESP 产物，不声称进程干净退出。 |
| PA Opt/Freq | [input.com](../../../../docs/verification/group_1/paper_ef26687d63a37e29/provenance/qzcli_hpc/PA_complete_phthalic_graph_20260914/repair_20260914T131250Z/input.com) | [gaussian.log](../../../../docs/verification/group_1/paper_ef26687d63a37e29/provenance/qzcli_hpc/PA_complete_phthalic_graph_20260914/repair_20260914T131250Z/gaussian.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| PA ADCH | [wavefunction.fchk (1)](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/wavefunction.fchk)<br>[adch_complete.stdin (2)](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/adch_complete.stdin)<br>[settings.ini (3)](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/settings.ini) | [adch_complete.out](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/adch_complete.out) | 采用已审计的分析结果；进程/菜单边界见下文 |
| PA ESP | [wavefunction.fchk (1)](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/wavefunction.fchk)<br>[mep_complete_stackfix.stdin (2)](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/mep_complete_stackfix.stdin)<br>[settings.ini (3)](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/settings.ini) | [mep_complete_stackfix.out](../../../../docs/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/mep_complete_stackfix.out) | 采用已审计的分析结果；进程/菜单边界见下文 |

## 5. 后处理、结果与逐项核验依据

- [provenance/complete_pa_closure_20260915.json](../../../../docs/verification/group_1/paper_ef26687d63a37e29/provenance/complete_pa_closure_20260915.json)
- [report/results.json](../../../../docs/verification/group_1/paper_ef26687d63a37e29/report/results.json)
- [verification_report.md](../../../../docs/verification/group_1/paper_ef26687d63a37e29/verification_report.md)
- [provenance/finalize_complete_pa_20260915.py](../../../../docs/verification/group_1/paper_ef26687d63a37e29/provenance/finalize_complete_pa_20260915.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- free/PO 旧 Multiwfn 存在菜单 EOF 退出问题，但已输出的 ADCH/ESP 表格和表面文件经专门审计确认有效；不将它们描述为无任何退出异常的进程。
- PA 超时/栈错误的后处理不计入有效流程；仅成功 stackfix 输出被列入。
- 历史验证使用 SI-derived 坐标和 PA 补建片段；这些历史结构现保留于 evaluation/author_results。当前三个公开初态已由完整化学图独立生成。历史成功计算支持相同科学对象的性质与结论，不冒称新初态已完成独立量化回放。

## 7. 成功阶段计时

三项成功 Gaussian 合计 4284.4 s；PA ADCH 后处理 31.40 s、有效 ESP 554.01 s。旧 free/PO 后处理耗时没有并入一个伪精确全链总数，失败后处理也不计入。

本次归档没有提交、重启或停止任何计算作业。


## 2026-09-16 当前输入与历史计算的关系

现有真实计算验证的是完整 free/PO/PA 模型（46/56/61 原子）的作者路线，不是当前新生成的 starter。2026-09-16 三份公开坐标全部由完整图独立嵌入；历史 SI/补全坐标保留于 author_results。保持接触定义、ADCH、signed ESP 和金标不变；未进行新量化计算。

## 2026-09-16 获准的接触选择定义澄清

这次更新明确测量口径，不新增量化计算，也不改历史结果。两模式当前统一固定输入 atom-map O49/P46；PA 的 O49 是公开图中 C48=O49 的指定氧，不按优化后 O-P 远近或金标挑选氧。完整映射图独立解析得到 12 个 N-ethyl alphaH、18 个 betaH；在各自优化末态上取同一 O49 对这两个集合的最近 H。重编号保留原子追踪，精确并列按最小输入 map ID；其他 O/H 作为辅助。

| 旧末态后处理 | O49-P46 / Å | 最近 alphaH / Å | 最近 betaH / Å |
|---|---:|---:|---:|
| PO | 1.8292620004 | H5，2.1250927092 | H45，2.4404698771 |
| PA | 2.6522103098 | H27，2.3117970249 | H29，2.3632905567 |

这些选择与旧 results.json 的全部六个 summary 和对应逐原子 ADCH 电荷一致。PA 辅助 O50 的 P/最近 alphaH/最近 betaH 距离分别为 4.5177304442、3.8713896700（H6）、2.2808258293（H15）Å，说明跨 O 取最短会换成另一物理量。上述值仅在 evaluator 侧归档，公开侧只给无答案的测量规则。AR 仍允许只用原有 species[].distances 提交，新增 summary 描述是可选，不自动增加数值评分。
