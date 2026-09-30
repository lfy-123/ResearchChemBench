# paper_a3892396b1843698：V2 特定升级方案

方案时间：2026-09-28T17:29:26.043595+00:00；先于该篇 V2 包创建。

## 来源与问题

What rearrangement behavior is supported for the specified dibutadienylcyclopropane3a, and how do its accessible molecular geometries and electronic structure constrain the mechanistic interpretation?

Study the full source C11H14 substrate3a and its intramolecular rearrangements. Generate and justify relevant conformations, electronic states and transformations. Other bridged derivatives, substituted families and quantitative trajectory branching are outside the required scope. No reaction-channel list, geometric intervention, saddle count or dynamics protocol is imposed.

The source studies thermal rearrangements of polyene-bearing cyclopropane frameworks computationally. The present subproblem is the specified3a connectivity and stereochemistry, neutralC11H14. The graph defines the starting molecule, not its preferred conformation or reaction outcome. No measured3a rate or product distribution is supplied. Define the thermodynamic state and environment of each model; changes in geometry alone do not create a new chemical species.

- papers/paper_a3892396b1843698/documents/main.pdf；SHA256 fae49816db907e5dce86872c757d439fca946b2721e5af626900a04e54c98f57；PDF页 2,3,4,5,6
- papers/paper_a3892396b1843698/documents/supplementary_001.pdf；SHA256 d70347560db74d188f67b4507f632405908a9b8e8ef217e96519d8f4381ae7ea；PDF页 1,2,3,4,5

## 旧版约束与公开改造

去掉33/55键编辑提示和±120度强制干预；明确原文3a的实质依据在正文Figure5与SI第2页，而SI第5页溶剂分析属于其他体系。保留真实图、态和公共基准要求，未知路径与构象留给agent。
- 3a.xyz：private_snapshot_only; retain mapped graph；Remove inherited reactive conformation as a starting-route cue.
- species_registry.json：remove bond_edits and geometric_control; preserve3a graph/stereochemistry；The bond edits and ±120 degree torsions disclose the proposed routes and intervention.
- research_matrix.json：private_snapshot_only；Remove forced [3,3]/[5,5], multi-start count and opposite-torsion control matrix.

## Agent 自主决策

- Generate relevant rearrangements and conformers from the supplied graph.
- Choose electronic-state and pathway methods sufficient for the proposed interpretation.
- Design tests that assess the role of molecular organization and distinguish model artifacts.
- Determine what static evidence can establish and whether additional dynamic claims are warranted.

## 提交、评价和 PR

Agent-defined objects/models/methods/records/quantities/claims/decisions; no named mechanism keys or hypothesis-count minimum. report/results.json and report/report.md required. Claim-triggered validity, not mandatory TS/IRC for every investigation.

The source compares [3,3] and [5,5] rearrangements of3a, reporting double-boat free-energy barriers23.5 and26.2 kcal/mol and double-chair barriers38.2 and36.9 kcal/mol (main p4 Figure5; SI p2 FigureS1). It attributes differences to cyclopropane strain and geometric organization. Main pp2–4 specifies Gaussian16, ωB97X-D/def2SVP optimization/frequency and ωB97X-D/def2TZVPP single points; low-frequency corrections use GoodVibes, and conformer sampling uses xTB-CREST. Wavefunction stability/unrestricted treatment is relevant to proposed radical states. Reproduce and assess the3a baseline or justify controlled substitutions, while checking what its evidence actually establishes. The source also studies dynamics, pancake bonding and negative-energy behavior for other bridged systems; those are not automatically established for3a. The V1 imposed opposite-sign±120 degree torsional control is not a source-synthesized derivative or a demonstrated separate minimum. Solvent results inSI p5 concern other named scaffolds, not a calibrated3a solvent series.

- identity (20/100)：PreserveC11H14 and the specified starting stereochemistry; define proposed bond changes, charge/spin and conformers explicitly. A constrained geometry is not automatically an independently stable species.
- rearrangement (30/100)：New auditable calculations/analysis must address the claimed rearrangement behavior and mechanistic scope. Claimed saddles and endpoint connections need corresponding evidence. Do not require both author-named channels, a fixed multistart count or a prescribed intervention when an adequate alternative argument is supplied.
- explanation (20/100)：Support the role assigned to geometry/electronic structure with discriminating evidence, not only structural pictures or source barrier repetition. Document observed collapse or indistinguishability honestly; missing paths alone do not prove their absence.
- references (15/100)：Separate electronic energy, enthalpy and free energy; use compatible reactant references, temperatures and correction conventions. Account for preparation costs if an imposed conformation is used. Investigate uncertainty that matters to the conclusion without mandatory±120 degree restraints.
- scope (15/100)：Answer the3a question with supported, revised or investigated unresolved conclusions. A static barrier difference does not establish a trajectory branching ratio or the dynamic behavior of another bridged scaffold. Partial coverage and unsuccessful searches must remain explicit.

## 旧证据、可行性与限制

The small source3a graph and source Gaussian pathway calculations support a manageable molecular rearrangement study. Existing3a path/geometry records may support their exact model and energy reference, but old artificial torsional controls and failed searches do not certify new states or full channel coverage. No new scientific calculation.

- workspaces/codex_gpt56/paper_a3892396b1843698_20260920_162206_b67206/runs/cli_runs/batch_20260920_162208_122e0e/autonomous_research-paper_a3892396b1843698-codex-20260920_162208-f6eeb7/report/results.json；Earlier narrow endpoint only; re-audit identity, model, raw artifacts and reference before reuse. No inherited PASS.
- docs/upgrade_tasks_v2_review_20260928/group_4/phase1/DEVELOPMENT_FREEZE_HANDOFF.json；原两船式TS及4个IRC端点已核验；几何准备高层代价3.70707 kcal/mol，释放回反应前体盆地。独立[3,3]扫描后无约束TS已完成：单个相关虚频−363.8229 cm−1，与旧同映射TS的RMSD为0.000755 Å、高层E差0.001221 kcal/mol。独立[5,5]扫描24个收敛点后被平台中断，已核实资源释放并checkpoint恢复a02。5种RRHO/qRRHO复算得到新[3,3]共同零点势垒23.49547–24.35550 kcal/mol，局部势垒+释放构象准备G均数值闭合；旧值重现误差<3e−9 kcal/mol。
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/legacy/baseline_deep_audit.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/legacy/independent_goodvibes_reparse.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/outputs/opposite120_release_local_a01/release_scientific_audit.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/outputs/preorganized_33_bondscan_local_a01/scan_audit.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/outputs/preorganized_33_scan_ts_local_a01/successor_ts_audit.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/provenance/preorganized_55_scan_preparation.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/provenance/independent_33_same_saddle_connectivity.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/provenance/preorganized_55_bondscan_recovery_a02.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/provenance/preorganized_55_ts_preparation.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/outputs/thermal_sensitivity_audit/results.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.

- Independent endpoint/path and method sensitivity calibration remains pending.
- Dynamic branching and any new constrained-control interpretation lack a transferred reference.
- Actual semantic judge and runtime isolation remain pending.

方案写好后立即实施；不启动新科学任务。完整结构化方案见同名JSON。

## 收尾来源与旧证据复用补充

Original 3a rearrangement saddle/IRC evidence, independent GoodVibes reparse and thermal sensitivity; a separately prepared 33 search returned the same saddle/basin. A 55 scan was interrupted.

可复用：Reuse connected baseline saddles and recorded endpoints after graph/method/reference matching. Same-saddle collapse is evidence of non-independence of that attempted alternative, not failed science.

不可据此声称：A constrained preparation cost is not a second saddle barrier. Interrupted 55 work is incomplete; source studies of other substrates/dynamics do not validate this 3a explanation.

逐文件版本绑定：

- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/legacy/baseline_deep_audit.json；SHA256 6d27daaa0fcb51f84eda34b7179c86af0e7e3d81e45e2576bee73b4187c8b786；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/legacy/independent_goodvibes_reparse.json；SHA256 4be7bd38ec121c513fb217c11decb71b30a6a44d732010e9fc53cf354a431ee7；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/outputs/opposite120_release_local_a01/release_scientific_audit.json；SHA256 82ce2f7292aded45728d9c617f25e4d1cfdc0864619e2de017cf9a36eb27caba；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/outputs/preorganized_33_bondscan_local_a01/scan_audit.json；SHA256 f905bda50b383e33314562b21f8d72176f0e006e89274a4a81700d33e6102d36；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/outputs/preorganized_33_scan_ts_local_a01/successor_ts_audit.json；SHA256 765cffea8364da894f98599555db94caf84b374fa1cc3648770f4047bab38e66；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/provenance/preorganized_55_scan_preparation.json；SHA256 5bf7169befa939928129610935d0c4a6a174b8482aba24f727d0247a5f767ee8；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/provenance/independent_33_same_saddle_connectivity.json；SHA256 f2e65e112fe9117a1827d9492bc376022e906a72b384b2de62fbcb3c2fbde303；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/provenance/preorganized_55_bondscan_recovery_a02.json；SHA256 6e0e8b0180da03a3f4bb5191244f4795cbce289ccecd448f50562fbaedd58eb5；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/provenance/preorganized_55_ts_preparation.json；SHA256 e598bc3c2cff5895a4241582e56aee946e7e366f09dcc32b1135f31766b206c8；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_a3892396b1843698/outputs/thermal_sensitivity_audit/results.json；SHA256 488f5d09ff1cb1c28f64359a7fd618b0e42405b22143467aa9e24b9dc7e02f80；冻结哈希一致=True

原始旧矩阵及活动作业状态仅在冻结行中保留为历史；不进入V2必做项目，不代表现时作业状态或新任务PASS。
