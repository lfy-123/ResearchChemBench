# paper_c625cba3ce868eb1：V2 特定升级方案

方案时间：2026-09-28T17:06:11.598176+00:00；先于该篇 V2 包创建。

## 来源与问题

What molecular evidence can explain the observed halocyclization selectivity of hydroperoxide (R)-4, and what remains uncertain when the source nonenzymatic NBS reaction is used as the chemical model?

Investigate the local molecular origin of selectivity for (R)-4 in the source NBS/Et3N chemical halocyclization context. The enzyme, photocatalytic formation of the substrate and full biocatalytic cascade are outside the modeled system. The source comparison compound 7 is available as an additional identified molecule, not a required branch. Choose relevant structures, chemical states and competing processes within this scope.

The source reports six-membered tetrahydropyran products from hydroperoxide 4 and similar chromatographic/NMR profiles in its enzyme and NBS experiments. The nonenzymatic procedure uses a 3/4 hydroperoxide mixture (50 mg,0.27 mmol), NBS (51 mg,0.284 mmol) and Et3N (4.2 µL,0.03 mmol) in 6 mL anhydrous DCM, under argon for4 h. The present molecular subproblem selects (R)-4 rather than the whole mixture. The printed NBS concentration 473 mM disagrees with amount/volume (47.3 mM); use the stated amounts and disclose this discrepancy. The substrate identity and stereochemistry are supplied as a graph, not an optimized conformation. No reaction intermediate or barrier is supplied.

- papers/paper_c625cba3ce868eb1/documents/main.pdf；SHA256 44b374957665d941b519f781fe9341f1632c84a6c7b975c4cd231874281e0ef8；PDF页 3,5,6,7
- papers/paper_c625cba3ce868eb1/documents/supplementary_001.pdf；SHA256 19d3e128aae61e6d8f4904d7f5f3cc8cd31230ccb210eb81ba15402de096e4db；PDF页 30,31,32

## 旧版约束与公开改造

保留(R)-4完整图、NBS和源实验观测，移走作者优化构象与固定脸/闭环/质子转移矩阵。源4/7的结构差异与两类溶剂不能被省略为“单变量证实”。保留六/七环拓扑纠错但不预给反应路径。
- compound_4_R.xyz and compound_7.xyz：private_snapshot_only; retain explicit graph/stereochemical identities；The SI coordinates are author optimized minima, not neutral experimental input.
- species_registry.json：retain identities without named closure bonds or forced intermediates；Keep correct O/H identities and atom maps; let agent generate mechanistic objects.
- research_matrix.json：private_snapshot_only；Remove prescribed faces, six/seven closure matrix and fixed NBS/Et3N cluster/proton-transfer sequence.

## Agent 自主决策

- Choose the chemically relevant brominating and protonation states and molecular environment.
- Determine which pathway, structural or electronic evidence can explain selectivity without supplied candidates.
- Design comparisons that separate the claimed explanation from important confounding.
- Assess whether the DCM chemical model supports the experimental inference and state where it does not.

## 提交、评价和 PR

Agent-defined objects/models/methods/records/quantities/claims/decisions; no named mechanism keys or hypothesis-count minimum. report/results.json and report/report.md required. Claim-triggered validity, not mandatory TS/IRC for every investigation.

The authors propose that the allylic hydroperoxide polarizes the alkene and affects bromiranium-ion ring closure. They compare4 and hydroperoxide-free7 using MEP maps/MEP-fitted charges and note different enzyme product distributions; these substrates also differ structurally, so the comparison does not isolate every possible cause. Their NBS experiment argues that enzyme participation is unnecessary for the observed profile (main pp3,5–7). Source computations are B3LYP/CBSB7 with C-PCM water in Gaussian16 A.03; minima were checked by frequencies, and MEP/charges used the same level. SI pp30–32 give source optimized minima and charge visualization. Reproduce/audit this molecular baseline or justify substitutions, explicitly separating aqueous monomer calculations from the DCM/NBS chemical model. The source does not supply a validated NBS reaction-path/free-energy network; the old mandatory face/closure/proton-relay matrix was a benchmark extension. Do not turn the source polarization hypothesis into a presumed answer.

- identity (20/100)：Preserve (R)-4 connectivity, E alkene, alcohol and hydroperoxide identity. Map any proposed bond changes explicitly; ring size follows the actual graph. Use a chemically identified brominating source and balanced proton/electron inventory rather than treating bromide as electrophilic bromine.
- selectivity (30/100)：New quantitative evidence must bear on the observed selectivity and distinguish what is established from what is assumed. Do not require a particular intermediate, two alkene faces or named ring-closure matrix if another valid route addresses the question. An MEP asymmetry alone is not a kinetic selectivity proof.
- causality (20/100)：Evaluate the claimed causal factor against important model/structural confounding. Comparing4 and7 cannot automatically isolate only hydroperoxide effects; alternative justified tests are eligible. Claimed saddles/pathways require appropriate physical evidence.
- uncertainty (15/100)：Use consistent stoichiometry, solvent/temperature/standard-state assumptions and evidence-based uncertainty for the claimed effect. Source room-temperature/unspecified aspects must be stated rather than given invented precision. Do not confuse aqueous MEP with a DCM free-energy path.
- scope (15/100)：Accept supported, revised or well-investigated unresolved explanations. Distinguish the selected (R)-4 model from the mixed-substrate NBS experiment and the enzyme context; no claim of enzyme control or full cascade yield from a local model.

## 旧证据、可行性与限制

Source graphs and substrate MEP calculations support a bounded molecular study. Previous NBS-related local structures can only support their exact state/inventory and require actual stationary-point/path inspection before reuse. Expanded kinetic explanation is not already validated by source charges. No new calculations were run.

- workspaces/codex_gpt56/paper_c625cba3ce868eb1_20260921_050613_b19fdc/runs/cli_runs/batch_20260921_050617_82c9a1/autonomous_research-paper_c625cba3ce868eb1-codex-20260921_050618-a30796/report/results.json；Earlier narrow endpoint only; re-audit identity, model, raw artifacts and reference before reuse. No inherited PASS.
- docs/upgrade_tasks_v2_review_20260928/group_4/phase1/DEVELOPMENT_FREEZE_HANDOFF.json；R4/NBS/Et3N全67原子中性账本已核对：8状态、7步转溴/六七元闭环/两受体质子转移保持核素、过氧键及原有映射奇偶性；远端溴化导致CIP字母R→S不等于构型翻转。两面DCM完整遭遇输入已回读，通过前保留两次准备失败；尚无新DFT。
- docs/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/legacy/inventory.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/provenance/haloetherification_preparation.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/provenance/haloetherification_v0_stereo_diagnostic/failure.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/provenance/haloetherification_v1_partial/failure.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.

- NBS chemical-path and selectivity calibration remains pending.
- The source concentration typo and aqueous-computation/DCM-experiment mismatch must remain explicit.
- Expanded uncertainty, semantic judge and runtime isolation remain pending.

方案写好后立即实施；不启动新科学任务。完整结构化方案见同名JSON。

## 收尾来源与旧证据复用补充

Mapped (R)-4/NBS/Et3N haloetherification constructions, 67-atom inventory; eight states/seven steps were prepared but not computed. Original MEP baseline is aqueous B3LYP/CBSB7.

可复用：Reuse graph, stoichiometry and stereochemical bookkeeping diagnostics, including the distinction between a changed CIP label and true inversion. No historical named state list is imposed on V2.

不可据此声称：No validated DCM/NBS reaction path or selectivity barrier. Aqueous monomer MEP does not supply those quantities; reported NBS concentration is internally inconsistent with amount/volume.

The NBS procedure on main PDF p7 prints 51 mg, 0.284 mmol and 473 mM in 6 mL CH2Cl2. The stated amount and volume imply about 47.3 mM, a tenfold discrepancy with the printed concentration. Retain both source entries and state which is used in any concentration-dependent model; do not treat the typo as experimentally resolved.

逐文件版本绑定：

- docs/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/legacy/inventory.json；SHA256 c12105ded4120c2c7753543da1fc28604393ea5dfcf4f8e9f64273a86ffbebd9；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/provenance/haloetherification_preparation.json；SHA256 1dec4a9b3772a6b1de686eaa1643fdb8aa183fac7cd73546d095f0e82333a996；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/provenance/haloetherification_v0_stereo_diagnostic/failure.json；SHA256 cb50c775a6ba3a0bac035a3fd632b5efd56edadee397af415f9bcc129ae53e5d；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_c625cba3ce868eb1/provenance/haloetherification_v1_partial/failure.json；SHA256 9e98d394010b6980578d8e2bef8b96d55d004e2e885153d56cfe8b4c3b1eff7a；冻结哈希一致=True

原始旧矩阵及活动作业状态仅在冻结行中保留为历史；不进入V2必做项目，不代表现时作业状态或新任务PASS。
