# 已验证成功计算链：3a [3,3] / [5,5] 重排势垒

- 论文 ID：`paper_a3892396b1843698`
- 本任务模式：`autonomous_research`（自主科研模式）
- 论文 DOI：`10.1021/jacs.5c19476`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_2](../../../../docs/verification/group_2/paper_a3892396b1843698)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_2.md)
- 最新已归档科学状态：当前 base paper_reproduction 作者子路线科学验证通过；四个 IRC 端点已完成后续最小值核验。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_autonomous_research`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../autonomous_research/paper_a3892396b1843698)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本自主模式共用同一论文的科学参考链；原有逐项资格审计主要针对作者路线/论文复现模式，不将其写成另一次自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 确认 3a 为 25 原子中性单重态；采用同一个公开 3a 反应物极小值作为两条势垒的共同零点。作者双船式 [3,3]、[5,5] TS 坐标是私有验证起点，不能由此声称完成了不提供 SI 的自主发现。

2. 在气相使用 Gaussian 16 的 ωB97X-D/def2SVP 完成 3a 的 Opt/Freq 和两条主 TS 的 Opt=(TS,…)/Freq。反应物有 69 个实频；两 TS 各仅一个虚频，并检查位移的断键/成键投影。共同断键为 C1–C2，新键分别为 C10–C13、C16–C20。

3. 从每个已验证 TS 分别运行 forward/reverse IRC；正向各 100 点，反向分别 83/73 点。把四条路径的末端逐一送入同级 Opt/Freq，四个端点均正常完成并有 69 实频；比较连接性，反应物侧端点可以是同一连接性的不同反应构象。

4. 在已完成的 3a 和两主 TS 几何上分别做 ωB97X-D/def2TZVPP 单点。不得以 IRC 端点较高的反应构象自由能替换共同公开 3a 最小值零点。

5. 用 GoodVibes 4.3.0 对低层级频率作 Grimme quasi-RRHO 熵修正：298.15 K、1 atm、频率尺度 1、100 cm⁻¹ 截止、global rotor；无 Head-Gordon 焓修正，也无额外对称性修正。组合 G = E_SP + G_qh,low − E_low；再计算 (G_TS − G_3a) × 627.509474 kcal/mol，并用 50/200 cm⁻¹ 截止做敏感性检查。

6. 依据最终端点审计、数值档案和最终作者路线审计核对 4 个关键点、1 个结论、6 条评分规则；3 项 critical failure 未触发。早期 numeric 文件中的 pending endpoint 历史文字已被后续四端点结果替代。

## 3. 实际结果与支持的结论

| 量 | [3,3] | [5,5] |
|---|---:|---:|
| TS 虚频 / cm⁻¹ | −364.3610 | −320.5474 |
| ΔG‡，100 cm⁻¹ 截止 / kcal mol⁻¹ | 23.505891602 | 26.227907854 |
| evaluator 目标 / kcal mol⁻¹ | 23.5 ± 3.0 | 26.2 ± 3.0 |
| ΔG‡，50 cm⁻¹ 截止 / kcal mol⁻¹ | 23.67359957 | 26.51846787 |
| ΔG‡，200 cm⁻¹ 截止 / kcal mol⁻¹ | 23.34596045 | 25.99755133 |

共同 G(3a) = −427.3279672341877 Eh；支持指定主通道中 [3,3] 势垒低于 [5,5] 的结论。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| 3a Opt/Freq | [input.com](../../../../docs/verification/group_2/paper_a3892396b1843698/artifacts/gaussian_batch/author_3a_wb97xd_def2svp_optfreq/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/artifacts/gaussian_batch/author_3a_wb97xd_def2svp_optfreq/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| 3a def2TZVPP SP | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3a_def2tzvpp_sp_20260914_20260914T120536Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3a_def2tzvpp_sp_20260914_20260914T120536Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3a_def2tzvpp_sp_20260914_20260914T120536Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| 3_ts3_3 Opt/Freq | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3a_3_ts3_3_wb97xd_def2svp_ts_optfreq_20260908T124425Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3a_3_ts3_3_wb97xd_def2svp_ts_optfreq_20260908T124425Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3a_3_ts3_3_wb97xd_def2svp_ts_optfreq_20260908T124425Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| 3_ts3_3 def2TZVPP SP | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_def2tzvpp_sp_20260914_20260914T121707Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_def2tzvpp_sp_20260914_20260914T121707Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_def2tzvpp_sp_20260914_20260914T121707Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| 3_ts5_5 Opt/Freq | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3a_3_ts5_5_wb97xd_def2svp_ts_optfreq_20260908T124436Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3a_3_ts5_5_wb97xd_def2svp_ts_optfreq_20260908T124436Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3a_3_ts5_5_wb97xd_def2svp_ts_optfreq_20260908T124436Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| 3_ts5_5 def2TZVPP SP | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_def2tzvpp_sp_20260914_20260914T121714Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_def2tzvpp_sp_20260914_20260914T121714Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_def2tzvpp_sp_20260914_20260914T121714Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| 3_ts3_3 IRC forward | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_wB97XD_def2SVP_irc_forward_hpc20_20260912_20260912T093006Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_wB97XD_def2SVP_irc_forward_hpc20_20260912_20260912T093006Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_wB97XD_def2SVP_irc_forward_hpc20_20260912_20260912T093006Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| 3_ts3_3 IRC reverse | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_wB97XD_def2SVP_irc_reverse_hpc20_20260912_20260912T093011Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_wB97XD_def2SVP_irc_reverse_hpc20_20260912_20260912T093011Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_wB97XD_def2SVP_irc_reverse_hpc20_20260912_20260912T093011Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| 3_ts5_5 IRC forward | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_wB97XD_def2SVP_irc_forward_hpc20_20260912_20260912T093028Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_wB97XD_def2SVP_irc_forward_hpc20_20260912_20260912T093028Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_wB97XD_def2SVP_irc_forward_hpc20_20260912_20260912T093028Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| 3_ts5_5 IRC reverse | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_wB97XD_def2SVP_irc_reverse_hpc20_20260912_20260912T093033Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_wB97XD_def2SVP_irc_reverse_hpc20_20260912_20260912T093033Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_wB97XD_def2SVP_irc_reverse_hpc20_20260912_20260912T093033Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| 3_ts3_3 端点 Opt/Freq forward | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_irc_forward_endpoint_optfreq_20260914_20260914T122045Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_irc_forward_endpoint_optfreq_20260914_20260914T122045Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_irc_forward_endpoint_optfreq_20260914_20260914T122045Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| 3_ts3_3 端点 Opt/Freq reverse | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_irc_reverse_endpoint_optfreq_20260914_20260914T122052Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_irc_reverse_endpoint_optfreq_20260914_20260914T122052Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts3_3_irc_reverse_endpoint_optfreq_20260914_20260914T122052Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| 3_ts5_5 端点 Opt/Freq forward | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_irc_forward_endpoint_optfreq_20260914_20260914T122059Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_irc_forward_endpoint_optfreq_20260914_20260914T122059Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_irc_forward_endpoint_optfreq_20260914_20260914T122059Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| 3_ts5_5 端点 Opt/Freq reverse | [input.com (1)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_irc_reverse_endpoint_optfreq_20260914_20260914T122107Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_irc_reverse_endpoint_optfreq_20260914_20260914T122107Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/qzcli_hpc/author_3_ts5_5_irc_reverse_endpoint_optfreq_20260914_20260914T122107Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |

## 5. 后处理、结果与逐项核验依据

- [AUTHOR_ROUTE_FINAL_AUDIT_20260914.md](../../../../docs/verification/group_2/paper_a3892396b1843698/AUTHOR_ROUTE_FINAL_AUDIT_20260914.md)
- [provenance/author_route_evaluation_audit.json](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/author_route_evaluation_audit.json)
- [provenance/independent_author_route_numeric_20260914.json](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/independent_author_route_numeric_20260914.json)
- [provenance/endpoint_minima_audit_20260914.json](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/endpoint_minima_audit_20260914.json)
- [report/results.json](../../../../docs/verification/group_2/paper_a3892396b1843698/report/results.json)
- [verification_report.md](../../../../docs/verification/group_2/paper_a3892396b1843698/verification_report.md)
- [provenance/prepare_sigmatropic_endpoints.py](../../../../docs/verification/group_2/paper_a3892396b1843698/provenance/prepare_sigmatropic_endpoints.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- 仅对应两条命名主通道；历史 double-chair 控制或旧 M062X 独立搜索不混入本主链，也不要求重演整篇论文。
- GoodVibes 的作者未披露细参数采用档案中明示约定，并保留截止敏感性；并非逐比特同软件/同参数重放。
- 这是作者路线的科学可计算性证据；历史 SI/private TS 起点不属于待评 agent 可获得的信息。

## 7. 成功阶段计时

原始日志和各作业目录保留分阶段计时；本归档不把缺乏统一口径的历史 wall/CPU/排队时间拼成总工期。

本次归档没有提交、重启或停止任何计算作业。
