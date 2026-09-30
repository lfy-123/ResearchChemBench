# 已验证成功计算链：四个 quartet 插入 TS 的局部自由能势垒

- 论文 ID：`paper_d7967e22bb965daa`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1021/jacs.5c18484`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_2](../../../../docs/verification/group_2/paper_d7967e22bb965daa)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_2.md)
- 最新已归档科学状态：2026-09-16 当前 ordinary paper_reproduction 作者路线科学参考验证通过（四个给定 quartet 候选的局部插入势垒）。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_d7967e22bb965daa)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 核对四个 TS3A–D-quartet 与两个配位参考 INT2A/B-quartet 均为 C31H32FeN3O、68 原子、中性 quartet（多重度 4）；历史验证采用作者四个 TS 起点及两个 INT2，保留各自原子顺序。当前仅公开 INT2 和四个映射通道，要求 agent 自行构建相应 TS；历史作者路线验证不是未知答案条件下的搜索。

2. 使用 Gaussian 16 C.01，气相 M06L/6-31G(d)（轻元素）–SDD(Fe)、UltraFine，分别完成四 TS 的 Opt/Freq 和两个 INT2 参考的 Opt/Freq。四 TS 各 198 模中一个目标虚频，两个参考各 198 实频、0 虚频。

3. 对六个实际优化末态逐坐标核对，再分别做 M06L/6-311+G(d,p)（轻元素）–SDD(Fe)、IEFPCM THF 单点；归档表中 Opt/Freq→SP 的最大坐标差均为 0 Å。

4. 用各负模式位移的键长投影核对 Fe–H/炔插入归属；四 TS 的 Fe/H/C/C2 原子映射逐一保留于独立审计。每 TS 再运行双向同级 40 点 IRC，观察 hydride-like Fe–H/非键合 H···C 与形成 H–C/Fe–H 拉长的两个方向。八条均正常结束于 MaxPoints；不把路径末端说成已频率验证的极小值。

5. 按正文 Fig.6 与 SI S96 的局部零点组装自由能：G_sol = E_SP + (H_gas−E_gas) − (2/3)×(H_gas−G_gas)，298.15 K。TS3A/B 减 INT2A，TS3C/D 减 INT2B，乘 627.509474 转为 kcal/mol。不能以游离 INT1A-sextet + 2a 的总能面高度替代这四个局部插入势垒。

6. 核对四个原目标及 ±1 kcal/mol 原容差、排序和机制限定；9 条规则、4 关键点、2 结论通过，4 项 critical failure 未触发。读取逐分支 S²，保留 quartet 自旋污染和版本差异，不引入未做的自旋投影或稳定性测试。

## 3. 实际结果与支持的结论

| 候选 | 相对零点 | ΔG‡ / kcal mol⁻¹ | 原参考（±1） | 唯一虚频 / cm⁻¹ |
|---|---|---:|---:|---:|
| TS3A | INT2A | 10.258029148 | 10.2 | −851.0093 |
| TS3B | INT2A | 12.425524265 | 12.4 | −835.2003 |
| TS3C | INT2B | 13.190985421 | 13.2 | −827.7649 |
| TS3D | INT2B | 12.022525130 | 12.0 | −829.6630 |

G_sol(INT2A)=−1563.675949440 Eh，G_sol(INT2B)=−1563.676158777 Eh；排序 A < D < B < C。

六个驻点的气相/单点 S² 在湮灭前约 4.32–4.40，湮灭后约 3.80–3.82；理想 quartet 为 3.75。完整逐分支数值与几何映射见独立结果表。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| INT2A Opt/Freq | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_INT2A_quartet_bound_reference_optfreq_20260915_20260915T081850Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_INT2A_quartet_bound_reference_optfreq_20260915_20260915T081850Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_INT2A_quartet_bound_reference_optfreq_20260915_20260915T081850Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| INT2A THF SP | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_INT2A_quartet_bound_minimum_THF_sp_20260915_20260915T135019Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_INT2A_quartet_bound_minimum_THF_sp_20260915_20260915T135019Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_INT2A_quartet_bound_minimum_THF_sp_20260915_20260915T135019Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| INT2B Opt/Freq | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_INT2B_quartet_bound_reference_optfreq_20260915_20260915T082913Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_INT2B_quartet_bound_reference_optfreq_20260915_20260915T082913Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_INT2B_quartet_bound_reference_optfreq_20260915_20260915T082913Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| INT2B THF SP | [input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_INT2B_quartet_bound_minimum_THF_sp_20260915_20260915T135026Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_INT2B_quartet_bound_minimum_THF_sp_20260915_20260915T135026Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_INT2B_quartet_bound_minimum_THF_sp_20260915_20260915T135026Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| TS3A Opt/Freq | [input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3A_m06l_mixed_basis_ts_hpc20_p6_20260912T114010Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3A_m06l_mixed_basis_ts_hpc20_p6_20260912T114010Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3A_m06l_mixed_basis_ts_hpc20_p6_20260912T114010Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| TS3A THF SP | [input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3A_thf_sp_genecp_terminated_hpc20_p6_submit_20260912T174431Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3A_thf_sp_genecp_terminated_hpc20_p6_submit_20260912T174431Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3A_thf_sp_genecp_terminated_hpc20_p6_submit_20260912T174431Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| TS3B Opt/Freq | [input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3B_m06l_mixed_basis_ts_hpc20_p6_20260912T114011Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3B_m06l_mixed_basis_ts_hpc20_p6_20260912T114011Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3B_m06l_mixed_basis_ts_hpc20_p6_20260912T114011Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| TS3B THF SP | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3B_thf_sp_genecp_terminated_hpc20_p6_submit_20260912T174507Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3B_thf_sp_genecp_terminated_hpc20_p6_submit_20260912T174507Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3B_thf_sp_genecp_terminated_hpc20_p6_submit_20260912T174507Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| TS3C Opt/Freq | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3C_m06l_mixed_basis_ts_hpc20_p6_20260912T114012Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3C_m06l_mixed_basis_ts_hpc20_p6_20260912T114012Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3C_m06l_mixed_basis_ts_hpc20_p6_20260912T114012Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| TS3C THF SP | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3C_thf_sp_genecp_terminated_hpc20_p6_submit_20260912T174524Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3C_thf_sp_genecp_terminated_hpc20_p6_submit_20260912T174524Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3C_thf_sp_genecp_terminated_hpc20_p6_submit_20260912T174524Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| TS3D Opt/Freq | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3D_m06l_mixed_basis_ts_hpc20_p6_20260912T114012Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3D_m06l_mixed_basis_ts_hpc20_p6_20260912T114012Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3D_m06l_mixed_basis_ts_hpc20_p6_20260912T114012Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| TS3D THF SP | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3D_thf_sp_genecp_terminated_hpc20_p6_submit_20260912T174528Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3D_thf_sp_genecp_terminated_hpc20_p6_submit_20260912T174528Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/author_route_mixed_basis/author_TS3D_thf_sp_genecp_terminated_hpc20_p6_submit_20260912T174528Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| TS3A IRC forward | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3A_quartet_IRC_forward_20260915_20260915T065604Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3A_quartet_IRC_forward_20260915_20260915T065604Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3A_quartet_IRC_forward_20260915_20260915T065604Z/stdout.log) | Gaussian 正常终止标记 1 处；40 点上限正常结束；未认证端点极小值 |
| TS3A IRC reverse | [input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3A_quartet_IRC_reverse_20260915_20260915T070739Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3A_quartet_IRC_reverse_20260915_20260915T070739Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3A_quartet_IRC_reverse_20260915_20260915T070739Z/stdout.log) | Gaussian 正常终止标记 1 处；40 点上限正常结束；未认证端点极小值 |
| TS3B IRC forward | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3B_quartet_IRC_forward_20260915_20260915T073129Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3B_quartet_IRC_forward_20260915_20260915T073129Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3B_quartet_IRC_forward_20260915_20260915T073129Z/stdout.log) | Gaussian 正常终止标记 1 处；40 点上限正常结束；未认证端点极小值 |
| TS3B IRC reverse | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3B_quartet_IRC_reverse_20260915_20260915T073526Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3B_quartet_IRC_reverse_20260915_20260915T073526Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3B_quartet_IRC_reverse_20260915_20260915T073526Z/stdout.log) | Gaussian 正常终止标记 1 处；40 点上限正常结束；未认证端点极小值 |
| TS3C IRC forward | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3C_quartet_IRC_forward_20260915_20260915T073533Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3C_quartet_IRC_forward_20260915_20260915T073533Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3C_quartet_IRC_forward_20260915_20260915T073533Z/stdout.log) | Gaussian 正常终止标记 1 处；40 点上限正常结束；未认证端点极小值 |
| TS3C IRC reverse | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3C_quartet_IRC_reverse_20260915_20260915T074424Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3C_quartet_IRC_reverse_20260915_20260915T074424Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3C_quartet_IRC_reverse_20260915_20260915T074424Z/stdout.log) | Gaussian 正常终止标记 1 处；40 点上限正常结束；未认证端点极小值 |
| TS3D IRC forward | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3D_quartet_IRC_forward_20260915_20260915T075816Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3D_quartet_IRC_forward_20260915_20260915T075816Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3D_quartet_IRC_forward_20260915_20260915T075816Z/stdout.log) | Gaussian 正常终止标记 1 处；40 点上限正常结束；未认证端点极小值 |
| TS3D IRC reverse | [source_input.com (1)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3D_quartet_IRC_reverse_20260915_20260915T080840Z/source_input.com)<br>[input.com (2)](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3D_quartet_IRC_reverse_20260915_20260915T080840Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/qzcli_hpc/author_TS3D_quartet_IRC_reverse_20260915_20260915T080840Z/stdout.log) | Gaussian 正常终止标记 1 处；40 点上限正常结束；未认证端点极小值 |

## 5. 后处理、结果与逐项核验依据

- [provenance/final_closure_20260916/FINAL_AUDIT.md](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/final_closure_20260916/FINAL_AUDIT.md)
- [provenance/final_closure_20260916/independent_report.json](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/final_closure_20260916/independent_report.json)
- [provenance/final_closure_20260916/author_route_evaluation_audit.json](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/final_closure_20260916/author_route_evaluation_audit.json)
- [provenance/chemical_mode_projection_20260914.json](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/chemical_mode_projection_20260914.json)
- [provenance/IRC_chemical_assignment_20260915/independent_IRC_assignment.json](../../../../docs/verification/group_2/paper_d7967e22bb965daa/provenance/IRC_chemical_assignment_20260915/independent_IRC_assignment.json)
- [report/results.json](../../../../docs/verification/group_2/paper_d7967e22bb965daa/report/results.json)
- [verification_report.md](../../../../docs/verification/group_2/paper_d7967e22bb965daa/verification_report.md)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- 历史计算适用于当前四个指定 quartet 通道的 TS 性质与局部势垒。验证时作者 TS 是已知起点；当前四份 TS 坐标均已私有化到 evaluation/author_results，agent 仅获得 INT2 与通道定义。公开输入边界变化不抹去作者路线验证，但不能宣称曾从当前公开 INT2 独立搜索到四个 TS。
- 八条 IRC 只支持局部反应方向/负模式身份，没有末端 Opt/Freq；当前局部势垒任务不要求完整催化循环，不能据此宣称该循环已验证。
- 作者 Gaussian09，实际 Gaussian16 C.01；NoSymm/TightSCF 等细参数选择已披露。未计算跨自旋动力学、实验绝对速率、替代泛函敏感性或穷尽构象搜索。
- 使用正文/SI 审计科学参考不等于 agent 在禁止源论文访问条件下的盲回放。现有 final 目录的不同版本不被此归档自动认证。

## 7. 成功阶段计时

20 个被采纳 HPC 作业均使用 20 CPU；Gaussian elapsed 合计 27.6943056 h、CPU 合计 551.3448611 核时。仅含六个 Opt/Freq、六个 SP、八条 IRC；排除测试、失败、游离参考诊断分支及排队。并行 elapsed 之和不是日历工期。

本次归档没有提交、重启或停止任何计算作业。


## 2026-09-16 当前输入与历史计算的关系

2026-09-16 四个 SI TS 文件从 agent_input 移入 author_results；公开仅保留两个已给定 INT2 与 reaction_channels.json。正文 pp9–10/Fig6 和 SI 结构角色共同确认：A/C 为氢迁移至端位碳、B/D 至取代碳，A/B 与 C/D 分属两反应物配位面。旧 TS 原子顺序各异，不能按同一行号盲比。历史 20 阶段作者路线和局部势垒仍有效；未从当前公开反应物重新搜索 TS。八条历史 IRC 达 MaxPoints 的限制保留。
