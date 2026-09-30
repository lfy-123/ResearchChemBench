# paper_534ae3b6e2fb695f：V2 特定升级方案

方案时间：2026-09-28T17:02:11.714796+00:00；先于该篇 V2 包创建。

## 来源与问题

What can molecular evidence establish about the relative intrinsic reactivity of ODA, 6FODA and PFMB toward trimesoyl chloride, and how far does that evidence support interpretation of their interfacial polymerization?

Address the molecular reactivity of the three specified diamines and trimesoyl chloride (TMC). The source forms polyamide films at an ionic-liquid/water–hexane interface; this task selects the local molecular question. State the environment and chemical state represented by each model. Do not infer membrane permeability, salt rejection, bulk crosslink density or an interfacial rate from isolated-molecule quantities alone.

ODA, 6FODA and PFMB are the source aromatic diamines; TMC is the acyl chloride comonomer. The source produces films using each diamine, with different measured film properties. No elementary rate constant or reaction-path measurement is supplied. Supplied structures define chemical identities, not a conformation, intermediate, reactive site ranking or mechanism. The polymerization context includes transport and medium effects that need not be captured by a molecular model.

- papers/paper_534ae3b6e2fb695f/documents/main.pdf；SHA256 285a5ec0e199ceec20676911267bae9407b30b2576f345aa5884611d83955e11；PDF页 2,3
- tasks/upgrade_tasks/coordination_20260927/batch4/source_review/paper_534ae3b6e2fb695f/publisher_formal_SI.pdf；SHA256 b1244e83d3294b7f9628231d1c173995c3158077fcf8663266632602c2306c89；PDF页 10,11,12,13,14,20,21,22,32

## 旧版约束与公开改造

原首酰化/Cl质子受体/应变矩阵不是作者已有证据。V2限定三种原单体与TMC的分子反应性解释，保留完整连接，开放环境、反应模型和判别方法；严格区分分子描述符、基元动力学与膜尺度。真实SI与审稿文件明确分开。
- monomers.json：retain identity graphs/maps/formulas as systems.json；Remove mandatory first-acylation roles and prescribed torsion indices while preserving all four source monomers.
- research_matrix.json and species_registry.json：private_snapshot_only；Remove forced gas-phase first acylation, chloride-assisted proton transfer, strain decomposition and fixed per-monomer TS searches.

## Agent 自主决策

- Define what intrinsic reactivity means for a stated local chemical environment.
- Select quantities, conformations and chemical states that can discriminate the monomer comparison.
- Decide whether molecular descriptors, explicit reaction modeling or another valid analysis can support the claimed interpretation.
- Test relevant uncertainty and determine which film-scale conclusions remain unsupported.

## 提交、评价和 PR

Agent-defined objects/models/methods/records/quantities/claims/decisions; no named mechanism keys or hypothesis-count minimum. report/results.json and report/report.md required. Claim-triggered validity, not mandatory TS/IRC for every investigation.

The source interprets monomer reactivity using molecular electrostatic potential, average local ionization energy, Fukui/LEAE information and a frontier-orbital nucleophilicity index; the reported indices are ODA 4.26, 6FODA 3.68 and PFMB 3.56 eV (main p3; formal SI pp20–22). These are descriptors, not elementary rate measurements. Formal SI p10 reports ORCA 5.0.4, B3LYP-D3BJ, def2-SVP optimization followed by def2-TZVP single points, AutoAux, and gfn2-xTB conformer screening. A later methods paragraph on p11 describes vacuum optimization and single points with def2-TZVP, so the source is not fully unambiguous; record the protocol chosen and its effect rather than inventing a single exact protocol. Reproduce and assess the disclosed molecular descriptor baseline or justify controlled substitutions, then determine what mechanistic/kinetic interpretation it warrants. V1 first-acylation TS, chloride proton acceptor and strain matrix were benchmark additions, not established source reaction-path calculations. Polymer MD and measured membrane properties address other scales.

- identity (20/100)：Preserve the three diamine substitutions and TMC identity, charge/spin and any additional species inventory. Distinguish the modeled state/environment from the experimental interface. Comparisons must refer to the same observable and compatible reference states.
- reactivity (30/100)：Provide auditable new results or analysis for the stated comparison. An orbital descriptor can support its defined electronic-property claim but cannot automatically establish a barrier or rate ordering. Assess an adequate agent-selected route without requiring a TS for every diamine or a fixed proton acceptor.
- interpretation (20/100)：Explain which chemical explanation the chosen evidence supports and what it fails to distinguish. A reactivity conclusion needs evidence that connects the chosen observable to the claimed reaction, not only repetition of author index values. Alternative orderings and evidence-backed non-identifiability are eligible.
- robustness (15/100)：Address uncertainty capable of changing the conclusion, such as modeling or conformational dependence when relevant, using actual evidence. No fixed gas-phase method, conformer count, descriptor list or strain partition is required.
- scope (15/100)：Separate local quantities from transport, network growth and film properties. Give an evidence-proportional answer for all three source diamines, identifying partial coverage if present; a limited conclusion is acceptable when its unresolved parts are investigated and explicit.

## 旧证据、可行性与限制

Source monomer graphs and formal molecular descriptor methods permit a bounded molecular investigation. Existing descriptor/conformer outputs, if reused privately after state/method checks, support only those quantities; previous attempted first-acylation calculations do not establish a validated reaction path. No scientific execution was performed for this upgrade.

- workspaces/codex_gpt56/paper_534ae3b6e2fb695f_20260921_055245_5ad2d2/runs/cli_runs/batch_20260921_055249_66bff8/autonomous_research-paper_534ae3b6e2fb695f-codex-20260921_055249-4fb4a0/report/results.json；Earlier narrow endpoint only; re-audit identity, model, raw artifacts and reference before reuse. No inherited PASS.
- docs/upgrade_tasks_v2_review_20260928/group_1/phase1/DEVELOPMENT_FREEZE_HANDOFF.json；Source/partial computation evidence; see paper-specific row.

- Reaction-path or kinetic interpretations beyond electronic descriptors remain uncalibrated.
- The source optimization-basis wording is inconsistent; a reproduction must state its interpretation.
- Semantic judge, new numerical error bounds and runtime filesystem isolation remain pending.

方案写好后立即实施；不启动新科学任务。完整结构化方案见同名JSON。

## 收尾来源与旧证据复用补充

ODA/6FODA/PFMB descriptor audits and gas-phase first-acylation endpoint/refinement audits; B3LYP-D3BJ/TZVP//SVP, 298.15 K and documented 1 M association correction in historical work.

可复用：Reuse descriptor values and validated individual endpoint/mode evidence only for the exact chosen molecular model. ODA transition-state mode evidence is provisional pending endpoint connection.

不可据此声称：An unconnected ODA saddle cannot supply a validated kinetic ranking. Historical gas-phase acylation is a benchmark model, not the source interface; molecular evidence cannot certify film transport.

逐文件版本绑定：

- docs/upgrade_tasks_verification/group_1/papers/paper_534ae3b6e2fb695f/report/acylation_refinement_audit/audit.json；SHA256 f75b2932a262fca0c1b0f49fd06b7165f0eb32858984e2579ddd1c84d08afd08；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_1/papers/paper_534ae3b6e2fb695f/report/ODA_NEB_image_audit/audit.json；SHA256 ba81af86353c049ac210b951d2a2b73b59c059ae1c1ee60746a6e4b268064623；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_1/papers/paper_534ae3b6e2fb695f/report/ODA_TS_analysis/audit.json；SHA256 6e4dad7ffe29a2dee42e490c84ce33650150dbaa8bb13a7a350c669dbf3ceb39；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_1/papers/paper_534ae3b6e2fb695f/legacy/descriptor_reuse_audit.json；SHA256 ee783529d74bc921af7437d32a393e9f80fd6f3e58c17810c074e6bdb43d1526；冻结哈希一致=True

原始旧矩阵及活动作业状态仅在冻结行中保留为历史；不进入V2必做项目，不代表现时作业状态或新任务PASS。
