# paper_8fefc96b015c4577：V2 特定升级方案

方案时间：2026-09-28T17:36:46.986339+00:00；先于该篇 V2 包创建。

## 来源与问题

What local cyclization behavior is supported for the specified short- and long-tether carbon radicals, and what molecular evidence can explain any difference without assuming a unique cause?

Investigate the two neutral doublet post-addition radicals defined in systems.json. The sole constitutional difference is an N-benzyl versus N-phenethyl tether. These are source-proposed molecular models, not experimentally isolated intermediates. Choose the relevant conformations, transformations, environmental representations and evidence. The full photoredox cycle, excitation kinetics, complete substrate scope and quantitative synthetic yield prediction are outside the required subproblem.

The source reacts N-allyl N-benzyl or N-phenethyl p-toluenesulfonamides with ethyl bromodifluoroacetate under 390 nm irradiation. The defined radicals result from addition of the ester-containing carbon fragment to the terminal alkene. Source experiments use substrate 0.2 mmol, radical precursor 0.4 mmol, PTH-2 5 mol%, zinc acetate 0.2 mmol, solvent 2 mL, argon, room temperature and 8 h. The short-tether preparation uses dry DMSO; the long-tether preparation uses dry 1,2-dichloroethane. Thus the optimized experimental comparison changes solvent as well as tether length and is not a matched causal intervention on chain length. Main Scheme2 omits zinc acetate from its caption, while both detailed SI procedures include it. The local models contain no zinc or photocatalyst; justify the relevance and limits of any environmental model. Their graph definitions do not establish a stable geometry, preferred ring closure or reaction barrier.

- papers/paper_8fefc96b015c4577/documents/main.pdf；SHA256 6fdb5e76c4af7f7b03c05b28d33bdbc9173ca66fcfa476df7c1346cbe422d01b；PDF页 2,3,4
- papers/paper_8fefc96b015c4577/documents/supplementary_001.pdf；SHA256 e4b428c6727ab05447160b59531f470d81ecb1d07986771510870c657b6f9a56；PDF页 1,2,3,10,20,34

## 旧版约束与公开改造

保留原论文两个加成后自由基这一有界子问题，去掉预设六/七元环路径、环张力指标和2×2×2矩阵。正文与SI同时改变链长和溶剂；SI详细步骤两者均有醋酸锌，不能虚构为不同添加剂的因果实验。PR明确负相对能量不等于负局部势垒，以及PTH标签/图注不一致。
- species_registry.json：replace with neutral radical and solvent graphs；Retain both precise post-addition identities while removing route-labeled bond edits, named target atoms, fixed geometric constraints and inherited coordinate choices.
- research_matrix.json：private_snapshot_only；No forced ring-size by tether by solvent matrix or predetermined strain decomposition.
- long_radical.xyz / short_radical.xyz：private_snapshot_only；Source or constructed conformations must not prescribe approach direction or certify a minimum.

## Agent 自主决策

- Generate and justify relevant local transformations and conformations from the two supplied radical graphs.
- Choose molecular and environmental representations, and decide which comparisons are needed to explain any difference.
- Establish the evidential basis of any proposed kinetic or causal interpretation, including whether competing factors can be separated.
- Revise the interpretation or retain a bounded unresolved conclusion when the available evidence does not distinguish causes.

## 提交、评价和 PR

Agent-defined objects/models/methods/records/quantities/claims/decisions; no named mechanism keys or hypothesis-count minimum. report/results.json and report/report.md required. Claim-triggered validity, not mandatory TS/IRC for every investigation.

The authors propose radical addition followed by competing aryl cyclizations. For the short N-benzyl tether they favor benzyl-ring annulation toward hydroisoquinoline 3a; for the N-phenethyl tether they favor arenesulfonyl annulation toward benzosultam 5a, attributing the change to unfavorable seven-membered closure and electronic effects (main pp2–4, Scheme3). These are hypotheses to reproduce and assess, not unique accepted explanations. SI p34 specifies Gaussian16, B3LYP-D3/def2-TZVPP optimization and frequencies with SMD DMSO for the short branch and SMD 1,2-dichloroethane for the long branch. The source checks minima/transition states by imaginary-frequency counts. Main p4 gives B at -13.13 kcal/mol, TS2 at -0.05 and TS2-prime at 6.12 on one profile reference; -0.05 is not a local activation barrier from B. It gives E at -9.89 and TS4-prime at 8.07 for the other profile. Reconstruct each physical reference before comparing local activation free energies; different substrates and solvents do not share an absolute molecular energy zero. The source reports 73% isolated 3a and 69% isolated 5a under separately optimized solvent conditions, not a controlled tether-only effect. SI pp10 and20 include Zn(OAc)2 in both protocols although main Scheme2 captions omit it. SI p10 optimization rows call the zinc-containing catalyst PTH-1, whereas main Table1 and the SI preparative procedures use PTH-2; retain this documentary ambiguity rather than silently invent a resolved protocol. No isolated strain descriptor proves the sole cause of selectivity, and no static radical barrier alone predicts isolated yield.

- identity (20/100)：Maintain the source sulfonamide, difluoroester and one-methylene tether difference, neutral doublet radical count and auditable maps. Define generated conformers or transformed structures explicitly; supplied graphs are not certified minima.
- cyclization (30/100)：Provide new reproducible quantitative evidence that addresses the local behavior of the two specified radicals. Claimed pathways, stationary points or kinetic preferences require suitable physical evidence. An adequate alternative analysis need not reproduce all author-named ring closures or a fixed matrix.
- causality (20/100)：Support any role assigned to molecular architecture, electronics or environment using discriminating evidence. The source short/long comparison also changes DMSO to DCE, so it cannot alone identify a chain-length cause. An unexplained barrier ranking or strain proxy is not a causal demonstration. Agent-designed comparisons or demonstrated non-identifiability are eligible.
- energetics (15/100)：Use compatible reactant references for local activation quantities, distinguish profile-relative values from activation barriers and label temperature, state and solvent conventions. Assess conclusion-relevant uncertainty without mandatory solvents, methods or conformer counts.
- scope (15/100)：Answer the local two-radical question in proportion to evidence. Do not claim a full photocatalytic mechanism or isolated yield from a static local profile. Honor source protocol ambiguities, alternative explanations and genuinely investigated unresolved outcomes; incomplete coverage remains partial.

## 旧证据、可行性与限制

Both radical constitutions and the authors stationary-point method are explicitly available; their 53/56-atom molecular representations are within the existing Gaussian/ORCA-style local pathway capabilities, subject to actual runtime availability. Existing source/legacy structures or energies can support only the corresponding model, method and energy reference. Prior artificial control matrices are not validated scientific references. This authoring phase performs graph and contract checks only.

- docs/verification/group_2/paper_8fefc96b015c4577/provenance/source_zero_closure_20260923/INDEPENDENT_RESULTS.json；Earlier narrow endpoint only; re-audit identity, model, raw artifacts and reference before reuse. No inherited PASS.
- docs/verification/group_2/paper_8fefc96b015c4577/provenance/source_zero_closure_20260923/autonomous_research/report/results.json；Earlier narrow endpoint only; re-audit identity, model, raw artifacts and reference before reuse. No inherited PASS.
- docs/upgrade_tasks_v2_review_20260928/group_4/phase1/DEVELOPMENT_FREEZE_HANDOFF.json；短链DMSO三驻点原生日志与映射已核验；相对B两势垒13.2530/19.2570 kcal/mol，连接待验证；DCE先导a01被平台中断，checkpoint零原子不可用；保持科学方法/精度，从原几何用默认初始Hessian恢复a02。
- docs/upgrade_tasks_verification/group_4/papers/paper_8fefc96b015c4577/legacy/short_dmso_deep_audit.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_8fefc96b015c4577/provenance/short_DCE_preparation.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.

- Independent connected-path and environmental sensitivity references remain pending.
- The source optimized solvent comparison does not identify a unique tether-only causal effect.
- Author protocol discrepancies and local free-energy reference reconstruction need evidence-aware calibration, not fixed numeric tolerance.
- Actual semantic judge and runtime isolation remain pending.

方案写好后立即实施；不启动新科学任务。完整结构化方案见同名JSON。

## 收尾来源与旧证据复用补充

Short-tether DMSO source-like 53-atom neutral-doublet B/TS model audit at B3LYP-D3/def2-TZVPP SMD, 298.15 K/1 atm; DCE work contains failed/checkpoint diagnostics and preparations.

可复用：Reuse graph-isomorphic short-DMSO stationary results only after remapping to V2 objects; local heights are relative to B, not to a different profile zero. Preserve DCE failure as failure.

不可据此声称：No completed short/long matched-solvent kinetics or fully connected competing pathways. Source tether comparison also changes DMSO to DCE, so chain-length causality is not isolated.

逐文件版本绑定：

- docs/upgrade_tasks_verification/group_4/papers/paper_8fefc96b015c4577/legacy/short_dmso_deep_audit.json；SHA256 5ea25985ca865a4b9f2506adf383f7ff5671637205a79b43a045729b0f977f6b；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_8fefc96b015c4577/provenance/short_DCE_preparation.json；SHA256 4ffb3395809bd936270f981a71ff5b88f07e0929398f2422b5c2d50ce003dd47；冻结哈希一致=True

原始旧矩阵及活动作业状态仅在冻结行中保留为历史；不进入V2必做项目，不代表现时作业状态或新任务PASS。
