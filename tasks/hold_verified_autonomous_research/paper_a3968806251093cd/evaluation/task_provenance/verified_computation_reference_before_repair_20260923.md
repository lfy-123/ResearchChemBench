# 已被替代的 reference 快照（仅维护历史，不用于验证或评分）

本文件保存本轮修改前的完整原文，其中旧 PASS/未认证/待确认表述具有不同历史日期。当前有效成功链见上级 evaluation/verified_computation_reference.md。旧位置异构体计算不再作为当前 7a 的证据。

以下原文的相对链接保留原 evaluation/ 所在位置的语境；查阅现行有效入口请使用上级 reference，勿把快照中的状态或路径当成现行规范。

---

# 当前迁移复核（2026-09-23）

正确对象的真实验证已完成，但本轮发现发布评分仍有待确认的构象边界，两个模式暂保留 HOLD。公开任务允许独立构象和混合排名，PR 最终结论却仍期望 CAM 整体更好。最新原始验收 §6 已明确指出该公平性问题。作者路线从 CIF 出发的成功验证有效；不能将这一次成功排名解释为任意合法构象都必须同向。详见 [迁移前复核及建议](task_provenance/release_review_20260923.md)。未修改科学目标或评分，未重算。

## 最新正确对象的成功计算链

1. 从私有 CCDC 2266402 单分子提取 46 原子 Cartesian 起点，保留正确吡唑连接、E-imine、N5–H thione 和事先确定的源标签；两方法用同一起点，不引入晶体周期环境。
2. Gaussian 16 C.01 下分别执行 B3LYP/6-311+G(d,p) 和 CAM-B3LYP/6-311+G(d,p)，Opt=(CalcFC,MaxCyc=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine，气相、无约束、无经验色散。
3. 两条均正常优化结束，分别 132 个正频率，最低频率 6.0884/3.9248 cm^-1；逐索引图匹配当前公开分子，排除历史位置异构体。
4. 按公开 13/23/11 选择器提取 94 条真实几何值，numpy 和 RDKit 独立重算一致；三类单位分别统计，二面角最小圆周差，不重复计 SI 的重复角。

| 指标 | B3LYP | CAM-B3LYP |
|---|---:|---:|
| 键长 MAE / Å | 0.009136258 | 0.007269655 |
| 键长 RMSE / Å | 0.011941034 | 0.008624190 |
| 键角 MAE / ° | 0.834539904 | 0.796413820 |
| 键角 RMSE / ° | 1.105572345 | 1.070749519 |
| 二面角 MAE / ° | 8.241270836 | 5.521946286 |
| 二面角 RMSE / ° | 13.480720202 | 8.689311681 |

5. 对照另一已成功验证的正确对象构象：其二面角 MAE 是 4.678395°/5.544711°，混合排名真实存在。CIF 两端点相对该盆地电子能高约 0.624033/0.524278 kcal/mol；不能把 CIF 排名外推为全局结论。

当前原始日志索引为 docs/verification/group_2/paper_a3968806251093cd/provenance/cif_hold_acceptance_20260921/PRIMARY_CIF_RESULTS.json，逐行几何为同目录 PRIMARY_GEOMETRY_94_ROWS.csv。该目录 FINAL_AUDIT.md §4、§6 记录构象敏感性及评分待处理问题。下方旧位置异构体链仅为历史，不参与当前正确对象验证。

# 2026-09-21 作者路线验收摘要（不等于评分公平性已解决）

正文/SI 所定义的正确 compound 7a 已有独立成功的作者路线验证；本目录仍是 HOLD，未执行发布目录迁移。正确对象为 C20H17ClN6OS、46 原子、中性单重态，正文 Fig. 3 的连接关系已作为身份依据。B3LYP/6-311+G(d,p) 与 CAM-B3LYP/6-311+G(d,p) 气相 Opt/Freq 均正常完成，各有 132 个实频；按正文/SI 的 47 个去重几何观测重新比较，94 个观测及 6 个分单位误差均有记录，CAM-B3LYP 的三类 MAE/RMSE 均不劣且总体更小。4/4 key points、2/2 conclusions、6/6 scoring rules 均获得支持，0/3 critical failures。当前权威证据为 `docs/verification/group_2/paper_a3968806251093cd/provenance/cif_hold_acceptance_20260921/FINAL_AUDIT.md` 与 `EVALUATOR_AUDIT.json`；旧异构体计算只保留为历史，不能替代本段。

本段验证的是作者路线对应的科学子目标，不是让自主 agent 看到作者终态坐标；作者坐标只存在于 evaluator-private 验证记录。下方旧记录仍然保留，原因是它说明此前为何被 HOLD；其“正确 7a 尚未认证”状态已被本段当前闭环取代。

# 历史证据适用性：正确 7a 尚未由下方历史链认证

正文 PDF p4 明确 pyrazole N1–N2–C9–C8–C7 的取代位置。此前两条主要成功 Opt/Freq 与 7a_repaired 模型属于不同位置异构体。当前已按正文/SI修复公开图和47行纯SCXRD比较输入，但这不改变旧计算对象。下方保留历史步骤供追溯，不是正确7a的成功验证；未经正确对象存量证据复核，不得使用旧PASS认证当前任务。没有新增计算、没有修改group原记录。

---

# 历史实际计算链（论文对象身份核对未通过）：compound 7a 两种泛函几何

- 论文 ID：`paper_a3968806251093cd`
- 本任务模式：`autonomous_research`（自主科研模式）
- 论文 DOI：`10.1016/j.molstruc.2025.144272`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_2](../../../../docs/verification/group_2/paper_a3968806251093cd)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_2.md)
- 最新已归档科学状态：两条 Opt/Freq 执行成功，但本轮核对发现吡唑取代连接关系错误，撤回本副本中“论文 compound 7a 已验证通过”的表述。group 原报告保留不改。
- 当前目录/审批状态：负责人于本轮明确授权，确认不能仅靠现有材料修复验证资格后，已移入对应 hold_verified 目录；不是已发布任务。

## 1. 本文件用途与任务版本

本文件保留此前实际完成的计算步骤与结果，并记录本轮发现的对象身份错误；这些历史步骤不再作为正确 7a 已验证的证据。不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../autonomous_research/paper_a3968806251093cd)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本自主模式共用同一论文的科学参考链；原有逐项资格审计主要针对作者路线/论文复现模式，不将其写成另一次自主 agent 盲测通过。

## 2. 历史真实执行流程及适用性更正

1. 历史流程由修复前的 SMILES 构建 C20H17ClN6OS、46 原子中性单重态 thione。分子式/原子数正确，但连接性不正确：正文 PDF p4 / Fig. 3 定义吡唑 N1–N2–C9–C8–C7，苯氧基 O1 连 C7，N1 连苯基；历史错误图的 O-bearing 碳却不邻接 N-phenyl N。不能把相同分子式当成相同论文对象。现行公开 SMILES 已按正文修正，不能与该历史输入混同。

2. 分别在气相 B3LYP/6-311+G(d,p) 和 CAM-B3LYP/6-311+G(d,p) 执行 Gaussian Opt/Freq；两条均正常终止，各 132 实频、0 虚频。

3. 历史脚本按原标签表从两条优化末态提取每种方法 13 个键长、24 个键角、11 个二面角（共 96 项记录）。其中 C6–N1–C7 角重复，当前公开表去重后为每方法 47 项；这些历史统计未经有效同分子映射确认，不能作为当前目标的正确几何比较。

4. 历史标签约定用 C7=21、C8=11、N1=4、O1=22（XYZ 1-based）。直接复核 B3LYP 末态：N1–C7=2.196492 Å，N1–C8=1.376571 Å，O1–C7=1.368864 Å。这不是简单对称原子重命名：论文要求的 N1–C7 键缺失。CAM-B3LYP 及现存初始 SDF/7a_repaired.xyz 同样具有错误连接。圆周角差处理本身不能修复错误分子图。

5. 原 MAE/RMSE 数字按历史输出保留于下表，仅说明当时做了哪些后处理。部分大角度误差来自错误连接/非键合原子三元组，不能据此确定论文模型的泛函优劣。前轮只读检查未替换身份；本轮已按正文修正任务图，但没有启动新计算。

## 3. 历史数值（不再作为论文目标已验证的证明）

| 几何误差 | B3LYP | CAM-B3LYP |
|---|---:|---:|
| 键长 MAE / Å | 0.0136422 | 0.01095824 |
| 键角 MAE / ° | 10.250931 | 10.210400 |
| 二面角 MAE / ° | 14.539979 | 13.756445 |
| 键角 RMSE / ° | 18.890748 | 18.905986 |

上述数值真实存在，但对应错误连接模型。当前不能据此确认 CAM-B3LYP 对论文 compound 7a 的几何更接近 SCXRD，也不能为当前两个任务出具科学可行性验收。本轮已按正文 Fig. 3/SI 修正正确图、标签映射和比较输入，并扩大检索；下方当前证据段记录没有找到匹配的既有成功链，旧输出不能替代。

## 4. 原始输入与输出索引

下表列出历史正常完成作业的原始输入/命令及日志，仅用于追溯错误对象的计算，不是正确 7a 的有效验证链。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系；正常终止不能替代化学身份核对。未将失败、重试过程列为有效验证步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| author_7a_B3LYP_6311pgdp_optfreq | [input.com](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/qzcli_hpc/author_7a_B3LYP_6311pgdp_optfreq_local_migration_20260904T163109Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/qzcli_hpc/author_7a_B3LYP_6311pgdp_optfreq_local_migration_20260904T163109Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| author_7a_CAM-B3LYP_6311pgdp_optfreq | [input.com](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/qzcli_hpc/author_7a_CAM-B3LYP_6311pgdp_optfreq_local_migration_20260904T151949Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/qzcli_hpc/author_7a_CAM-B3LYP_6311pgdp_optfreq_local_migration_20260904T151949Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |

## 5. 后处理、结果与逐项核验依据

- [provenance/author_route_evaluation_audit.json](../../../../docs/verification/group_2/paper_a3968806251093cd/provenance/author_route_evaluation_audit.json)
- [report/results.json](../../../../docs/verification/group_2/paper_a3968806251093cd/report/results.json)
- [verification_report.md](../../../../docs/verification/group_2/paper_a3968806251093cd/verification_report.md)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。原报告的通过标签和误差统计未因本轮维护而改写；应连同本文件的身份更正及 `task_provenance/identity_evidence_check_20260916.json` 阅读，不能用历史正常终止输出或旧 PASS 标签认证当前正确对象。

## 6. 保留的科学与记录边界

- [正文 PDF](../../../../papers/paper_a3968806251093cd/documents/main.pdf) p4/Fig. 3 与 [历史 B3LYP 末态](../../../../docs/verification/group_2/paper_a3968806251093cd/artifacts/generated_structures/7a_author_B3LYP_optimized.xyz) 给出上述身份冲突证据。
- 历史入库包缺少实验比较值/图映射，且 PR 方法对不明。本轮已补 47 行纯 SCXRD 观测和完整映射，PR 主方法固定为 B3LYP/CAM-B3LYP，误差分物理量处理；但修复这些输入不能把旧错对象结果变成正确对象验证，总体优劣仍须正确对象证据。

- 计算对象是气相孤立分子；SCXRD 是晶体结构，不能把差异全部解释为数值误差或宣称已计算晶体环境。
- 旧 ωB97X-D 代理路线不作作者双泛函证据；96 项仅是历史条目数量，并非正确论文身份/公开去重表的验收结论。

## 7. 历史正常完成阶段计时（非正确对象验证）

两条作者级作业的 HPC 摘要记录约 10615/14965 s；这是阶段 ledger 时间口径，不冒充并行验证的日历工期。

本次归档没有提交、重启或停止任何计算作业。


## 2026-09-16 当前输入与历史计算的关系

追加存量身份检索：已检查 group_2 本篇目录下 67 份可恢复 XYZ/SDF/输入/日志末态的原子连接图，符合修正后 7a 完整元素标记图的记录为 0；其中正常终止正确对象日志 0 份。详情在 task_provenance/identity_evidence_check_20260916.json。不能以错位置异构体的正常终止或 132 实频认证当前 7a；没有新计算。

## 2026-09-16 再复核及授权暂缓

再次解析 group_2 本篇目录，仍为67份可恢复几何、0份正确连接图；额外检查 author_route_queue 中两份作者级起始 XYZ，也均不匹配。独立去氢重原子图同构检查不通过，排除了仅氢原子编号/映射造成误判的可能。正文 PDF p4 的 N1–C7 键，在历史 B3LYP 末态对应原子间距为2.19649222 Å；历史 N1–C8为1.37657131 Å，确系不同位置异构体。当前任务输入已修正，但旧计算不能更名转为正确对象验证。完整包按负责人授权移入 hold；未删除原始计算、未提交新计算。若找到正确对象的既有输出，可重新核对；否则需单独安排正确对象作者路线验证。
