> 2026-10-17：以下原计划按历史保留。现行限定科学结果已由后续验收覆盖，见[当前状态](current_verification_status.json)及[验证参考](verified_computation_reference.md)。不因旧待办重算；仍有效的来源、数值资格及发布限制单列。

# Current author-scope reference validation plan

Scope: `core_question_upgrade_20261012T190159Z`. Use `target_map.json` and `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/tasks/small_molecules_autonomous_research/verification_dispatch/core_question_upgrade_20261012T190159Z/papers/paper_2a71ffa4b0a90809/verification_delta.json`. 最新已读记录为 `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_2a71ffa4b0a90809/selected29_20261012T053104Z_group_01/coverage.json`，时间 2026-10-12T12:38:14.804856+00:00。记录中的作业状态是历史快照，本次未查询实时作业。

1. 复用七组匹配的 free-donor/Cl-complex、孤立 Cl− 及五份波函数，核对物种、电荷、自旋、构象、方法与各自热校正。不要重复提交有效已完成项。
2. 先核实源文 RRHO 压力及 SMD18 腔参数的可比性，再独立确定结合自由能量值比较标准。已有实现采用 I 半径 2.74 Å；这不是源文完整输入的证明。分别保留 raw 1 atm 与条件性的 1 M 转换，不能用当前残差反推容差。25 分量值判断和正式总分继续保留未判。
3. 先收取并复核已经尝试的 C/D 构象工作，只对确认仍缺的作者旋转势垒结果安排后续验证。需要正确的一阶旋转鞍点、一个虚频及通往独立优化 anti/syn 极小点的双向连接。已存快照中 D 负向端点为 anti-like；正向端点和 C 尚未闭合。D 对新端点为 1.5894814978551326 kcal/mol，对作者 2.2 的残差为 −0.6105185021448676，无已校准窗口。不得迁移金标。
4. A 旧约束扫描 29.99558036965 对 31±1 保持 MISMATCH；30.0006004454 仅为端点敏感性。不要为取得 PASS 重算、舍入或选另一端点。
5. 复用电子波函数和原有表面分析；如有必要，仅对明确的密度面/局部极值定义缺口做后处理。不能把电荷、不同密度面的电势和作者 I-ESP 值混比。
6. 按 Fig.5a 和 Figs.9–13 审核跨系列解释，区分局部物性恢复与最终判别关系。解释 A/B、A/D、C/弱供体/空白的主要差异；不要求拟合唯一速率定律，不把收率当基元速率，不补造 C 的冷却历史或初始布居。

作者方法：SI S60、S66，Gaussian 16 / M06-2X-D3 / 6-311+G(d,p)-SDD(I)，SMD18(THF)，193.15 K。free donors 0/singlet，Cl− 与 complexes −1/singlet。C/D 锚点来自正文 PDF p7/Fig.6。作者缺失的 C–C 成键 TS、真实 isoquinolinium 全网络及新反应金标均不在必答/验证范围。

全部科学结果权重仍合计 100；当前规则只可人工比较已具资格的科学发现。没有自动 release gate；正式总分及发布继续冻结。设计实施、包校验、作业正常退出均不能视为整题科学验证通过。
