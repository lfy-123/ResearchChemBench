# paper_db6c4e0558113873：V2 特定升级方案

方案时间：2026-09-28T16:45:31.254323+00:00；先于该篇 V2 包创建。

## 来源与问题

What molecular account of local C–Cl bond formation can explain the observed chlorosulfonylation selectivity of allenoate6b under the source photo/copper conditions, and what evidence limits that account?

Focus on local bond formation and selectivity for6b/benzenesulfonyl chloride with Cu(acac)2 in MeCN. A model may include chemically justified intermediates and states, but the full photoredox cycle, other allenoates and quantitative reaction yield are outside the task.

6b is ethyl4-phenyl-2-propyl-2,3-butadienoate; the source uses benzenesulfonyl chloride, Cu(acac)2 (10mol%) and4CzIPN (1mol%) with427nm irradiation in MeCN underN2 at40°C. Standard mechanistic experiments use0.05M6b and2equiv sulfonyl chloride. The observed product places chlorine at the benzylic terminus and phenylsulfonyl at the central allene carbon, with the reported Z alkene geometry. This is a measured selectivity to explain, not a hidden product prediction. Any active copper oxidation state or coordination model is a research inference.

- papers/paper_db6c4e0558113873/documents/main.pdf；SHA256 9b9d8841f0eb5ec7561cb770ad3bd43d0820639e443412d5da1bc74842318c8c；PDF页 6,7,8,9
- papers/paper_db6c4e0558113873/documents/supplementary_001.pdf；SHA256 a6585fbc4d364923517f436132456b23b012d972eeecb7a818a8a4259c1a6608；PDF页 56,60,64,65

## 旧版约束与公开改造

将原强制CuIII/自由基两出口矩阵改为源观测驱动的局部C–Cl问题。公开金属前体身份不固定活性态；SI表头G273.15与实验40°C均如实保存。
- species_registry.json：retain reactant graphs; remove intermediate seeds；CuIII_allyl/acac/Cl and allyl/sulfonyl radical structures are candidate models, not fixed starting facts.
- research_matrix.json：private_snapshot_only；Remove CuIII exit vs direct radical chlorine-transfer named branches and mandatory spin/temperature matrix.
- public_sources.json：neutral observations and scope；Keep observed selectivity and source conditions; do not publish source optimized intermediates or their energies.

## Agent 自主决策

- Choose chemically defensible local copper/reagent models and states.
- Determine which molecular explanations can connect selectivity to measured controls.
- Choose appropriate evidence and search strategies without prescribed intermediates.
- Assess whether intermediate energies, barriers or other observables support the claimed degree of mechanism discrimination.

## 提交、评价和 PR

Agent-defined objects/models/methods/records/quantities/claims/decisions; no named mechanism keys or hypothesis-count minimum. report/results.json and report/report.md required. Claim-triggered validity, not mandatory TS/IRC for every investigation.

The authors propose oxidative quenching of excited4CzIPN byCuII, reduction of sulfonyl chloride byCuI, sulfonyl-radical addition to6b, trapping byCuII(acac)Cl to allyl–CuIII species and reductive elimination (main pp8–9). Their computations compare four allyl–CuIII minima: C1 capture is lower than C3 alternatives and a2.3kcal/mol C1 conformer difference is used to rationalize selectivity. That is intermediate thermodynamics, not calculated C–Cl activation barriers. SI p65 uses Gaussian16, B3LYP-D3(BJ)/6-31G(d,p) withLANL2DZ onCu optimization/frequencies and M06/6-311+G(d,p)-SDD(Cu)/SMD MeCN single points. Its table labels a thermal column G273.15; source experiments are313.15K. Preserve and investigate this temperature-reference issue rather than silently treating old298.15K benchmark values as source conditions. Audit/reproduce the disclosed local rationale and state what further evidence is needed. The old two-route barrier matrix was a benchmark addition.

- identity (20/100)：Validate6b and full relevant ligand/substrate identity, Cu coordination/charge/spin, chlorine and reagent reservoirs. Formal CuIII labels alone do not validate electronic states. Different ligand inventories cannot be compared by bare total energies.
- reaction (30/100)：Generate auditable quantities bearing on local C–Cl formation/selectivity. Repeating the source2.3kcal/mol minima difference alone does not establish the reaction route. Non-author models and bounded conclusions are eligible when grounded in relevant raw evidence.
- test (20/100)：Judge the discriminating power of the selected tests in light of observed product and catalyst/trapping controls. A claimed activation route needs connectivity and appropriate stationary/path evidence; neither author CuIII capture nor direct transfer is mandatory. Properly demonstrated collapse or indistinguishability is acceptable.
- limits (15/100)：Bound model/spin, preparation/binding and thermal/solvation effects relevant to the inference. Explain source40°C versus any calculation temperature; do not equate the SI G273.15 label with verified313.15K thermochemistry or add arbitrary tolerance.
- conclusion (15/100)：Support or challenge the source rationale in proportion to evidence. Local energetics cannot prove the entire photocycle, quantitative yield or an exclusive global pathway. No source conformer or Cu oxidation-state winner is compulsory.

## 旧证据、可行性与限制

Source four finite Cu intermediate coordinate/energy records and historical endpoint calculations demonstrate accessible local models. They do not provide verified C–Cl transition paths or a full competing-route reference. Model/state and temperature ambiguities are reviewable within a bounded local investigation.

- workspaces/codex_gpt56/paper_db6c4e0558113873_20260918_203828_530445/runs/cli_runs/batch_20260918_203835_fcedec/autonomous_research-paper_db6c4e0558113873-codex-20260918_203835-126440/report/results.json；Earlier narrow endpoint only; re-audit identity, model, raw artifacts and reference before reuse. No inherited PASS.
- docs/upgrade_tasks_v2_review_20260928/group_4/phase1/DEVELOPMENT_FREEZE_HANDOFF.json；两个Cu中间体原生日志、完整映射和复合G已核查；anti−syn为2.29270 kcal/mol，不是出口势垒。synsyn扫描a02再次遭平台STOPPED，实例已释放，进入第二次有界checkpoint恢复a03。
- docs/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/legacy/Cu_intermediate_deep_audit.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/provenance/Cu_exit_pilot_preparation.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/provenance/synsyn_scan_recovery_a02.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.

- Expanded raw path/state evidence and numerical sensitivity remain incomplete.
- Exact source thermal convention needs clarification; retain source label without inventing corrected values.
- Alternative-route semantic calibration and execution isolation pending.

方案写好后立即实施；不启动新科学任务。完整结构化方案见同名JSON。

## 收尾来源与旧证据复用补充

Cu syn/anti source-intermediate minimum audit gives a relative free-energy difference only. Source SI free-energy table is at 273.15 K; experiment is at 40 degrees C.

可复用：Reuse matched minimum identities, original energies and electronic-state audits under their recorded reference conditions. Prepared exit scans are feasibility records only.

不可据此声称：The roughly 2.3 kcal/mol minimum separation is not a C-Cl exit barrier. No complete competing exits, spin treatment or connected transition-state comparison is validated.

逐文件版本绑定：

- docs/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/legacy/Cu_intermediate_deep_audit.json；SHA256 e88339b9543e0dfc7aabcebab27e1f0a7079d1c44403dd0120a1d3b5c1288261；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/provenance/Cu_exit_pilot_preparation.json；SHA256 b5dd85fb4c14729de0a11eac6177f16f34e061b23fd89c71abd43a1eb57301f1；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_db6c4e0558113873/provenance/synsyn_scan_recovery_a02.json；SHA256 c849f9235c0fb8170d95f878d91db5750325cf4752bc86d33b2cca9f0e252b8e；冻结哈希一致=True

原始旧矩阵及活动作业状态仅在冻结行中保留为历史；不进入V2必做项目，不代表现时作业状态或新任务PASS。
