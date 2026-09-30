# paper_0dc85595cab7bc0a：V2 特定升级方案

方案时间：2026-09-28T17:26:42.162239+00:00；先于该篇 V2 包创建。

## 来源与问题

Which molecular outcomes of the source oxidative photocyclization of 2,7-distyrylphenanthrene are supported by independently developed evidence, and how strongly can that evidence constrain the observed regioselectivity?

Study the molecular transformations of source precursor1 during its oxidative photocyclization, including the sequential nature of the transformation where relevant. Product identities, states, pathways and discriminating calculations are to be developed by the agent. The task concerns molecular reactivity; crystal packing, charge transport and devices are outside scope. A ground-state constraint on possible products is a legitimate bounded result when it is not claimed as proof of photochemical branching.

The source precursor is 2,7-distyrylphenanthrene,C30H22, synthesized by coupling2,7-dibromophenanthrene with(E)-styrylboronic acid. Irradiation of1 at1.2×10−4 M in anhydrous DCM withI2(4.5 equivalents) and propylene oxide(20 equivalents), afterN2 purging, uses a1000 W medium-pressure Hg lamp overnight at room temperature. The lamp has strongest emission at365 nm. A highly regioselective transformation gives one characterized C30H18 product in90% isolated yield. The product constitution is withheld for this task. Supplied precursor graph encodes connectivity; alkene configurations and irradiated conformational/state populations must be explicitly represented and justified rather than assuming the previously supplied1-cis geometry is the experimental starting ensemble.

- papers/paper_0dc85595cab7bc0a/documents/main.pdf；SHA256 f23bf2094145eada8d43b6e1bf7cce14fdd9db27d9f82fae7948b0fd86183451；PDF页 2,3
- papers/paper_0dc85595cab7bc0a/documents/supplementary_001.pdf；SHA256 84d40a48033a1d1cfc425d3b981e79b39eaf00fa29ffdffbde03807e528bc652；PDF页 3,4,5,9,10,11

## 旧版约束与公开改造

取消预给1-cis构象、邻位配对生成规则与固定路径诊断矩阵，回到真实前体和氧化光环化条件。既不提前给作者终产物结构，也不把S0最低能候选冒充可达性证明；允许有实证边界的候选集合。
- precursor_1_cis.xyz and species_registry.json：replace cis model/coordinates by source precursor constitutional graph and experimental preparation facts；The source computational1-cis is a proposed reactive geometry, not a measured starting ensemble.
- research_matrix.json：private_snapshot_only；Remove ortho-pair enumeration rule, fixed candidate layers, prescribed representative scans and vertical-state sampling.

## Agent 自主决策

- Generate chemically plausible transformations and structures from the precursor and source conditions.
- Choose how to establish candidate coverage or other evidence sufficient for the claimed outcome.
- Choose ground/excited-state descriptions and tests that match the asserted accessibility claim.
- Determine whether the available evidence supports a unique product, a restricted set or only partial constraints.

## 提交、评价和 PR

Agent-defined objects/models/methods/records/quantities/claims/decisions; no named mechanism keys or hypothesis-count minimum. report/results.json and report/report.md required. Claim-triggered validity, not mandatory TS/IRC for every investigation.

The source assigns the product to dibenzo[a,o]picene2, confirmed by single-crystal XRD. Its mechanistic interpretation compares1-cis, dihydro intermediatesIS1/IS2 and laterIS4/IS5, with reported thermodynamic preferences9.9 and11.3 kcal/mol and orbital-density/phase arguments (main p2; SI p9 FigureS5). These are source hypotheses and molecular calculations, not a measured excited-state trajectory. SI p9 specifies Gaussian16, B3LYP/6-31G(d,p) geometries/frequencies and ωB97X-D/def2-TZVP single points, with a generalD3 statement whose application to the already dispersion-containing single-point functional should be treated as a source ambiguity. TD-B3LYP/6-31G(d) optical calculations on product2 are separate. Reproduce/audit the source thermodynamic/orbital baseline or justify substitutions. Do not equate same-formula ground-state stability with unique photochemical accessibility, and do not compare absolute energies across hydrogen counts without a balanced oxidation reference. The V1 forced candidate enumeration, S0 scans and vertical excited-state sampling were benchmark additions, not a complete source dynamic mechanism.

- identity (20/100)：Preserve source precursor connectivity and explicitly define stereochemical/conformational state, any new bonds and any removed hydrogens. Compare compatible compositions or include balanced reservoirs; C30H22,C30H20 andC30H18 absolute energies are not directly comparable.
- outcomes (25/100)：Provide auditable generated evidence for the outcome or supported set claimed. Define why considered possibilities are sufficient at that scope, without a required ortho enumeration rule, authorIS list or fixed candidate count. Repeating the source product name alone is insufficient.
- accessibility (25/100)：Use physical evidence appropriate to the asserted state/path. Ground-state energies or orbitals can constrain a model but do not alone prove unique photoproduct branching. Conditional supported sets and investigated unresolved outcomes remain eligible; no mandatory nonadiabatic trajectory or fixed scan.
- robustness (15/100)：Assess structural/state/method sensitivity that can change the claimed selection. Distinguish source synthesis stereochemistry from an assumed irradiated ensemble and state limitations of simplified oxidation treatment. No fabricated tolerance or pathway barrier.
- scope (15/100)：State what the analysis establishes and what remains unproved about source selectivity. A bounded ground-state finding can earn appropriate credit but cannot be sold as complete photochemical dynamics. Molecular conclusions cannot establish crystal/device behavior.

## 旧证据、可行性与限制

The source constitutional graph and small polyaromatic molecular size support candidate/structure and electronic investigations with available tools. Historical ground-state candidate outputs only support their exact composition/state; they do not validate photodynamics. Source S0/optical calculations establish a baseline, not complete accessibility calibration. No scientific engine run.

- workspaces/codex_gpt56/paper_0dc85595cab7bc0a_20260920_164554_4baadc/runs/cli_runs/batch_20260920_164558_4a5af1/autonomous_research-paper_0dc85595cab7bc0a-codex-20260920_164558-491621/report/results.json；Earlier narrow endpoint only; re-audit identity, model, raw artifacts and reference before reuse. No inherited PASS.
- docs/upgrade_tasks_v2_review_20260928/group_4/phase1/DEVELOPMENT_FREEZE_HANDOFF.json；9个旧极小点完成原生、价态及立体形式核查；112条生成历史通过闭壳层价态与H收支。新缺失首氧化C30H20无虚频，同作者组合G比旧IS3低5.62321 kcal/mol。缺失第二层4构造类的10个正式立体形式已备输入并回读，尚非DFT；均仅基态约束，不证明光产物。
- docs/upgrade_tasks_verification/group_4/papers/paper_0dc85595cab7bc0a/legacy/nine_minima_native_deep_audit.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_0dc85595cab7bc0a/provenance/finite_graph_layer_audit.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_0dc85595cab7bc0a/provenance/finite_valence_stereochemistry_audit.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_0dc85595cab7bc0a/provenance/missing_candidate_preparation.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_0dc85595cab7bc0a/outputs/alternate_first_oxidized_optfreq_sp/a01/scientific_audit.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.

- Independent excited-state accessibility and comprehensive candidate-selection calibration remain pending.
- The source dispersion-method wording and experimental-to-reactive stereochemical relation require explicit modeling choices.
- Actual judge calibration, reference error bounds and runtime isolation remain pending.

方案写好后立即实施；不启动新科学任务。完整结构化方案见同名JSON。

## 收尾来源与旧证据复用补充

Nine historical ground-state minima and finite graph/stereochemical audits; an alternative first-oxidized C30H20 minimum was optimized with the recorded source-like baseline.

可复用：Reuse its completed ground-state minimum and relative energy only within matched formula/method. Keep the alternative graph exploration as one feasible route, not the only route.

不可据此声称：Lower S0 energy does not establish a photochemical pathway or observed product selection. Prepared second-stage inputs are not results; no excited-state connectivity/selectivity reference is completed.

逐文件版本绑定：

- docs/upgrade_tasks_verification/group_4/papers/paper_0dc85595cab7bc0a/legacy/nine_minima_native_deep_audit.json；SHA256 b80360da7752227a34b7d84984e196ecd880a3c954754341b630594f437cf264；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_0dc85595cab7bc0a/provenance/finite_graph_layer_audit.json；SHA256 c63ada2342d85a649d6bc3ad8b2426c539889f82cb9e561a1e14a49d74838435；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_0dc85595cab7bc0a/provenance/finite_valence_stereochemistry_audit.json；SHA256 fbaea4b348335c7383f51ecef0cb343fd29c6a9ada0a2f45f1d17e38bd7c4014；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_0dc85595cab7bc0a/provenance/missing_candidate_preparation.json；SHA256 bfe6b9b3ba8eae45fbe741eb09471dca683e01c9cc910e7e7699ca42da28e563；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_0dc85595cab7bc0a/outputs/alternate_first_oxidized_optfreq_sp/a01/scientific_audit.json；SHA256 8785919e98911231369e604166b9cc67bcd9f5f2b690a70d0f8a14b288784b79；冻结哈希一致=True

原始旧矩阵及活动作业状态仅在冻结行中保留为历史；不进入V2必做项目，不代表现时作业状态或新任务PASS。
