> 2026-10-17：以下原计划按历史保留。现行限定科学结果已由后续验收覆盖，见[当前状态](current_verification_status.json)及[验证参考](verified_computation_reference.md)。不因旧待办重算；仍有效的来源、数值资格及发布限制单列。

# 后续参考验证计划

本文件是后续参考验证清单，本轮没有提交 HPC、没有运行新量化计算，也不把结构校验当科学 PASS。

先复核候选 package hash、当前题面与 schema，然后只读接收原始作业，核对软件原生日志、分子图/电荷自旋、收敛、相关 Hessian/连接、单位和参照。按 target_map 逐项判断；不能因平台作业成功或历史 PASS 宣布新合同全部通过。后续计算由父进程另行安排。

对缺失、失败、部分结果保留独立有效结果的部分分，不给缺失结果满分。来源模型或数字矛盾进入 needs_review，不能通过改阈值、拼接失衡总能或强求作者路线解决。公开题面允许自主方法；本私有参考计划不是评测 agent 的流程清单。

1. 从 `docs/verification/group_4/paper_c625cba3ce868eb1/small_molecules_20261010T231612Z_g03/` 及其 MK 源日志复用证据。本轮 source_review/native_reextraction.json 重新读取未合并氢的 ESP 电荷：R4 C2/C4 = -0.533926/-0.049661 e；7 C8/C10 = -0.313449/-0.258383 e。它们支持方向，但不是新增合同的自动 PASS。
2. `reactant_polarization`：来源 B3LYP/CBSB7/C-PCM water、MEP fitting（refs 38/39 为 MK 系列），S50 C2/C4 -0.507/-0.066，7 -0.311/-0.262，差 -0.441/-0.049 e，比值 9.0 是源数值推导。原生差为 -0.484265/-0.055066。检查 population 表而非 Mulliken 或合并氢表，复核稠密拟合/构象及既有 DCM 敏感性；不发明一个统一数值容差。7 是可选比较，无需隐藏强制水相复现。
3. 身份校验先去掉人工 atom-map 优先级再赋 CIP，确认公开图和 SI 坐标的 R,E 一致，勿将 RDKit 的未清理映射排序误判为 S。保留 C10H20O3/33 原子、OH O21/H22、OOH O23/O24/H25 的物理映射。
4. `local_regioselectivity`：核对真实 6/7 元竞争闭环图：O21-18-15-9-6-C4 为六元，延伸到 C2 为七元。分数必须有超越重复极化标量的结构/反应分析，联系亲电溴来源及 NBS/Et3N/DCM 条件。旧水相、稠密拟合与 DCM 结果可支撑有限反应物电子解释；未主张动力学时不强制补固定 bromiranium/TS。
5. 公开程序按 0.284 mmol/6 mL = 47.333... mM NBS；混合物 3/4 的 18% 不作纯 R4 产率或势垒。温度源未明述，记录模型假定；7 的 16/25/27% 是酶实验，不能作 NBS 目标。
6. 如要声称唯一 OOH 因果或严格 kinetic selectivity，另做独立竞争反应补证并与源计算区分；论文明确称 reactant polarization 不蕴含特定机理，也把 Thorpe–Ingold 效应留作未来工作。新增检查不得生成作者 TS 金数值。
7. 按 45/55 结果权重回放，不能用泛泛合理/未解决答案满分；历史 PASS 只覆盖旧有限解释，需父进程核验当前 rubric。
