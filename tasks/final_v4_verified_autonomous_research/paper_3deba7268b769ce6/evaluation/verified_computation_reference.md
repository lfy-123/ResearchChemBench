# 2026-10-28 二次审查（group_10）

电子归属、分子间排序和固定模型方向有支持；DCM源值疑点、EtOAc残差与连续介质反号保留，不认定严格全面复现。本轮只直接读源文、原生证据和必要算术核对；未新增计算，不继承历史PASS。逐命题覆盖及专家问题见本轮审查材料。

---

# 2026-10-28 V3范围与逐命题证据复用（group_10）

保留两种完整阴离子、三溶剂低能吸收解释题。将电子归属、分子间比较、各染料溶剂响应解释及样品适用性拆为6个独立最终结论；不重复奖励给定谱带趋势，不规定作者计算节点。AR自主建模，PR保留分子计算与固定Catalán基线。

- `r_electronic_origin_dye3`：正文p4 Fig5；NTO_REUSE_SUMMARY.json中dye3_DCM hole phenolate 0.51558→particle 0.14873，bridge/acceptor增大，其他三介质同方向；支持ICT归属，不是弛豫电荷转移量。
- `r_electronic_origin_dye4`：SI p9 FigS8；NTO_REUSE_SUMMARY.json中dye4_DCM hole phenolate 0.62119→particle 0.21662，particle bridge 0.60293、acceptor 0.18045；支持向桥/受体重分布，不能强制受体>50%。
- `r_inter_dye_response`：REUSED_SCIENTIFIC_RESULTS.json：共同DCM fullTD 56.97959<65.36992；TDA 59.56191<68.23950 kcal/mol。排序支持，作者59.44/66.18不同时精确复现。
- `r_solvent_explanation_dye3`：固定Catalán 57.42180→56.85472→63.64499 kcal/mol；MeOH SA +7.24185；结合NTO支持有界差异溶剂化解释。EtOAc残差+3.91472、纯CPCM反号须保留。
- `r_solvent_explanation_dye4`：固定Catalán 61.60384→59.73978→70.11053 kcal/mol；MeOH SA +11.12595；结合NTO支持有界解释，不能由模型系数单独证明唯一原因。
- `r_sample_applicability`：正文pp2–3,5：5 μL 1 M NBu4OH/MeOH，dye3 EtOAc约10 s光降解；模型无NBu4+、显式溶剂及降解。SOURCE_SCOPE_REVIEW与原生模型支持有界适用性结论。

证据缺口：历史验收为用户接受定性结果及数值偏差，不是严格源数值复现；共同full-TD/TDA均未同时精确重现两染料DCM作者计算值，源响应近似未明确；dye3 EtOAc固定Catalán残差+3.91472 kcal/mol；纯CPCM的Tol→EtOAc方向相反；只有三溶剂及有限寿命信息，不能证实唯一微观溶剂机制或完整实验物种。本轮无新增量化计算、无重验证、无ARCHE盲测；历史PASS不自动继承。以下历史正文原样保留，历史评分描述不再是当前评分合同。

---

# 当前计算验证与科学分V2参考 — 2026-10-20

验收类型：**ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION**。当前冻结任务范围的必要定性节点、重要披露方法与有效计算已获协调确认；formal_scoring_permitted=true。当前评分为paper_science_v2，二元叶子总分100，无过程分。此验收不声称原数值容差已通过，不承诺全部源表或整篇实验精确复现。出版/专家复核与运行评分资格分开。

## 当前科学范围与对象

Complete E-imine, phenolate -1 singlet dye3 nitrothiophene and dye4 nitrophenyl graphs in toluene, ethyl acetate and methanol. Fixed published regression evaluation; no refitting of19-solvent data.

- source: r2SCAN-3c opt/frequency with DCM continuum, then TD-omegaB97X-D4/def2-TZVP with RI/COSX and CPCM; fixed published Catalán coefficients interpreted alongside TDDFT.
- native: Disclosed DCM baseline executed; eight parent minima and eight response/NTO endpoints, plus four same-geometry common-DCM TD/TDA endpoint records. Six solvent-specific TD endpoints are labeled additional source-method adaptations.
- version: ORCA6.1.1 versus6.1.0 covered by existing version exception.
- response: Full TD and TDA common protocols are both retained; no dye-specific selection of whichever response fits better.

## 实际计算验证过程与关键节点

1. Validate two distinct complete phenolate E-imine graphs and -1/singlet states; source synthesis contradicts loose positional-isomer prose.
2. Execute r2SCAN-3c geometry/frequency parents with continuum; source DCM parents kept separate from added Tol/EtOAc/MeOH adaptations. Eight parent minima and response/NTO endpoints are present.
3. Evaluate omegaB97X-D4/def2-TZVP RI/COSX CPCM transitions and NTO assignments. Four shared DCM full-TD/TDA results retain one common protocol per comparison; no source-near cherry-picking.
4. Evaluate the published Catalán coefficients on the supplied three-solvent subset without refitting. Combine that result with ICT evidence and preparation/stability data.
5. Additional six continuum endpoints give blue Tol→EtOAc shifts. This is retained model counterevidence and is not represented as successful source inversion.

所有以下记录复用真实既有计算；本次迁移不启动量子化学/HPC任务，不拟合参考值或容差。版本差异依既有授权，不自动视为误差来源或数值准确度证据。

## 论文值、实际值与偏差

差值定义为native−source；绝对偏差另列。表中为实数减法汇总，无新科学模拟。相对误差对近零能隙、位移或不同实验/理论口径可能误导，未机械计算。无数值评分叶子，表值不形成隐藏容差门。

| 量 | 论文值 | 实算值 | 有符号差 | 绝对差 | 单位 / 定义 |
|---|---:|---:|---:|---:|---|
| dye3 DCM fullTD S1 | 59.44 | 56.979592757693815 | -2.460407242306185 | 2.460407242306185 | kcal/mol / Source calculated baseline; same-geometry shared fullTD |
| dye3 DCM TDA S1 | 59.44 | 59.56191290376653 | 0.12191290376653 | 0.12191290376653 | kcal/mol / Separate sharedTDA diagnostic |
| dye4 DCM fullTD S1 | 66.18 | 65.36991941983841 | -0.81008058016159 | 0.81008058016159 | kcal/mol / Source calculated baseline; same-geometry shared fullTD |
| dye4 DCM TDA S1 | 66.18 | 68.23950481023715 | 2.05950481023715 | 2.05950481023715 | kcal/mol / Separate sharedTDA diagnostic |
| dye3 Tol fixedCatalan | 57.76 | 57.4218 | -0.3382 | 0.3382 | kcal/mol / Experimental lower band versus published fixed-function evaluation; not a new quantum target |
| dye3 EtOAc fixedCatalan | 52.94 | 56.85472 | 3.91472 | 3.91472 | kcal/mol / Experimental lower band versus published fixed-function evaluation; not a new quantum target |
| dye3 MeOH fixedCatalan | 63.39 | 63.64499 | 0.25499 | 0.25499 | kcal/mol / Experimental lower band versus published fixed-function evaluation; not a new quantum target |
| dye4 Tol fixedCatalan | 61.75 | 61.60384 | -0.14616 | 0.14616 | kcal/mol / Experimental lower band versus published fixed-function evaluation; not a new quantum target |
| dye4 EtOAc fixedCatalan | 59.44 | 59.73978 | 0.29978 | 0.29978 | kcal/mol / Experimental lower band versus published fixed-function evaluation; not a new quantum target |
| dye4 MeOH fixedCatalan | 69.23 | 70.11053 | 0.88053 | 0.88053 | kcal/mol / Experimental lower band versus published fixed-function evaluation; not a new quantum target |

## 额外实际结果与未复现项

- Common DCM S1 energies, dyes3/4：source=[59.44, 66.18]；native={"full_TD": [56.979592757693815, 65.36991941983841], "TDA": [59.56191290376653, 68.23950481023715]}；Same-geometry comparisons within each dye; shared response protocols preserved
- Tol/EtOAc/MeOH observed versus fixed Catalán：source={"dye3": [57.76, 52.94, 63.39], "dye4": [61.75, 59.44, 69.23]}；native={"dye3": [57.4218, 56.85472, 63.64499], "dye4": [61.60384, 59.73978, 70.11053]}；Published coefficient function, no tolerance fitting; largest listed residual dye3 EtOAc +3.91472
- Additional pure-continuum S1 solvent scan：source={"experimental_direction_Tol_to_EtOAc": "red for both dyes", "experimental_direction_EtOAc_to_MeOH": "blue for both dyes"}；native={"dye3_approx_eV": [2.126, 2.421, 2.611], "dye4_approx_eV": [2.445, 2.774, 2.979], "native_direction_Tol_to_EtOAc": "blue for both dyes"}；Counterevidence to continuum-only inversion; not omitted or renamed a numerical deviation

## 定性关键节点与仍有边界

- Identity, charge and sample model：SUPPORTED: two chemically distinct anions, not positional isomers; bare-anion calculation distinguished from Bu4N+ and added-methanol experimental preparation.
- Lower-band electronic assignment and two-dye ordering：SUPPORTED: donor→bridge/acceptor NTO evidence across8 systems; common DCM TD and TDA both preserve dye3 lower than dye4.
- Observed red then blue solvent shifts：SUPPORTED by fixed published Catalán function for both dyes; all4 adjacent shift directions agree. This is source-model evaluation, not a new blind prediction.
- Specific interactions and continuum limitation：SUPPORTED bounded interpretation: positive SA contribution in methanol7.24185/11.12595 kcal/mol is dominant but not uniquely causal. Pure CPCM yields the wrong Tol→EtOAc direction, making a continuum-only explanation unsupported.
- Limited identifiability and sample stability：SUPPORTED: three solvents cannot determine the full inversion point or freely fit4 solvent descriptors; short-lived EtOAc samples, ion pairing, preparation methanol and degradation remain consequential limitations.
- Calculation validity and audit：SUPPORTED: parent minima/frequency and response/NTO chains completed; raw native files and hashes re-read. Normal termination alone was not used as validity proof.
- Main Fig5/prose dye3 experimental DCM57.18 differs from SI TableS2 DCM55.19 kcal/mol; neither is silently substituted for the source calculated59.44.
- Source loose positional-isomer wording does not override distinct nitrothiophene/nitrophenyl graphs.
- Source TDA/full-TD choice is not disclosed; both common protocols retained.
- Fixed Catalán has +3.91472 kcal/mol dye3 EtOAc residual and is not a new19-solvent refit or blind prediction.
- Pure continuum predicts the wrong Tol→EtOAc direction; only the combined bounded author interpretation is accepted.
- Acceptance is for the combined bounded molecular interpretation and disclosed DCM baseline. It does not certify a pure-CPCM solvent inversion, a causal H-bond proof,19-solvent refit, unique counterion-free experimental species or predictive accuracy.
- The incorrect continuum shift is a genuine limitation of the added model. It is not a reversal of a source claim that this specific continuum-only scan reproduces inversion.
- No V1 one-MeOH contact/remote intervention, fixed matrix or frozen prediction requirement is reintroduced.

## 原生输入/输出与验证分析位置

以下路径为仓库/服务器真实文件，hash为2026-10-20独立重读值。正常终止只作为执行证据；对象、状态、频率/曲率、响应定义仍是科学资格前提。

- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/papers/paper_3deba7268b769ce6/cases/DCM_default_grid_controls/dye3_TDA/input.inp`；SHA256 `008407d2167408090bcfd49f5a6ef462dbb810ded5fd9820146a3f9b1008fa8c`；input；normal_marker=None
- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/papers/paper_3deba7268b769ce6/cases/DCM_default_grid_controls/dye3_TDA/stdout.log`；SHA256 `e2a70642c0fc18c4388767ce63c642c4de97c3eb4fa804252475bc26656a28b1`；native_output；normal_marker=True
- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/papers/paper_3deba7268b769ce6/cases/DCM_default_grid_controls/dye4_TD/input.inp`；SHA256 `76234e6fe9756406b4d55fd8e63a1ac93caf5dc92ff051be0bfd4c02b6ebc104`；input；normal_marker=None
- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/papers/paper_3deba7268b769ce6/cases/DCM_default_grid_controls/dye4_TD/stdout.log`；SHA256 `87f5a1dd7dc2973a8b719634c0981c06a20de0f6c10abc89a135dc002a8241a1`；native_output；normal_marker=True
- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/papers/paper_3deba7268b769ce6/cases/DCM_default_grid_controls/dye4_TDA/input.inp`；SHA256 `0575c76d0820e8de7f2f91eada95e1c1222c607f6c1cfd43922f27b65eed617f`；input；normal_marker=None
- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/papers/paper_3deba7268b769ce6/cases/DCM_default_grid_controls/dye4_TDA/stdout.log`；SHA256 `624d3ee6abdc5b5a306bfb87f55a011caed7cdaea3779e59e9bf48b2219bc1bc`；native_output；normal_marker=True
- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/papers/paper_3deba7268b769ce6/cases/DCM_dye3_samegeom_fullTD_20261011/input.inp`；SHA256 `5ff41a257a09db4d86b78ff3cbf3a716611dfd40e44c1549f10d5e47788f1d0c`；input；normal_marker=None
- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/papers/paper_3deba7268b769ce6/cases/DCM_dye3_samegeom_fullTD_20261011/stdout.log`；SHA256 `74896b924b231231c7575d087401eb7dee1b5c5809e1d4f15731b928df874e77`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/dye3_ethyl_acetate_continuum_optfreq/attempt_001/input.inp`；SHA256 `1bbdcadf2cd7e66f0a548f0a9b87b6f81944482f9ff5e6c6230b53025cc7378e`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/dye3_ethyl_acetate_continuum_optfreq/attempt_001/stdout.log`；SHA256 `6d07cac573d5d9d4f22844f266bcb97b00324c295f1412476aa6d975d6f953cf`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/dye3_methanol_continuum_optfreq/attempt_001/input.inp`；SHA256 `30ab1c7d5bfd5773123f0b3914c7908e66eaa6a80707f13f275806a8cd8446c8`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/dye3_methanol_continuum_optfreq/attempt_001/stdout.log`；SHA256 `87644ba5ba7a7902a3ae17b654551514ee8406b6ebde87ed40c12a39134994b2`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/dye3_toluene_TD12_source/attempt_001/input.inp`；SHA256 `5c77697c324d82c1883a6d4b94c13ca298e50444dd43fee906514188a0e45c00`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/dye3_toluene_TD12_source/attempt_001/stdout.log`；SHA256 `170b5886338136dd91913d2749433ceae32f859d0d45c9ccd56d40f982606501`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/dye3_toluene_independent_pilot_optfreq/attempt_001/input.inp`；SHA256 `caeb699250f86f70201d8bcf54d584bff6c39523b567a64c3a0f4b237cd1ebd8`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/dye3_toluene_independent_pilot_optfreq/attempt_001/stdout.log`；SHA256 `c318faac8308ec7c8920968091c9842557adfc9fb6cab502e6218866a70b3024`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/dye4_ethyl_acetate_continuum_optfreq/attempt_001/input.inp`；SHA256 `e29fdaba51ee120e33bb0fbbb654f07a2f6837505a74978464974dd8c5940175`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/dye4_ethyl_acetate_continuum_optfreq/attempt_001/stdout.log`；SHA256 `4ddcec7991f3ace6f48e411edf3fa1eabdf38331956758f00413d25eac7f3d67`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/dye4_toluene_independent_pilot_optfreq/attempt_001/input.inp`；SHA256 `9af12bd618d2a4ae406d85a3683d1a409da8f0313984e88d1a2b15592b219912`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/dye4_toluene_independent_pilot_optfreq/attempt_001/stdout.log`；SHA256 `a6e0f6a5c2cea6ce841d7d79b7e463779b5b03428e87f76ccf8d21b9ec74ebec`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye3_ethylacetate_approximate_stationary_source_TD20/attempt_001/input.inp`；SHA256 `bf70232f1ab862aa18a5f68e5fdf30b74a67a149a212a729a6ea96df0d862274`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye3_ethylacetate_approximate_stationary_source_TD20/attempt_001/stdout.log`；SHA256 `1a665ab03f015347b9318feedae016bdd835795becfe14da1ff5fb9b91e5c653`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye3_methanol_approximate_stationary_source_TD20/attempt_001/input.inp`；SHA256 `ba19c2c4617729cf43f8c11fd7dde69fc04306dbb830f38e2978de83a70c3037`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye3_methanol_approximate_stationary_source_TD20/attempt_001/stdout.log`；SHA256 `1663be7f3fba1519fdfeab529dad0bc8e4580954010457836137dffb50e10c8e`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye4_MeOH_numerical_precision_optfreq/attempt_001/input.inp`；SHA256 `310f09f5853f22484c90d46e55b1e5a7405891c3dd8f0f6b9fa4fdf10e9e618a`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye4_MeOH_numerical_precision_optfreq/attempt_001/stdout.log`；SHA256 `35156b39bc20a7a383eff0225254ef6dc843ffe31518152a35ac3e05fb04c4c7`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye4_ethylacetate_source_method_TD20/attempt_001/input.inp`；SHA256 `98b557d4f44a640a68b1b2671d9e6683d739a13a115565b31b04ab239aafda9c`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye4_ethylacetate_source_method_TD20/attempt_001/stdout.log`；SHA256 `cd3c6a5f275aa8773918d4123b5b877e71478d2cb98f5e009e7d5f594e24983a`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye4_methanol_source_method_TD20/attempt_001/input.inp`；SHA256 `14b6bc7901fa1eae55348bf282548edc2110bfe55b0dfcf1de9d35eb42a43225`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye4_methanol_source_method_TD20/attempt_001/stdout.log`；SHA256 `2d261f42c218c59177cc22baa0ded1ae2b9d6be46e85b8376e8a6e818d9ff85c`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye4_source_DCM_TD20/attempt_001/input.inp`；SHA256 `d408dfb6b7ca8c5d1693c43f1970ead7e36c907933629d3d94b9fdc9f72d25ee`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye4_source_DCM_TD20/attempt_001/stdout.log`；SHA256 `6764ba34f06269d9537160e4f3e4080ef59c5b69ecb9374c0040df027d0933f9`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye4_source_DCM_optfreq/attempt_001/input.inp`；SHA256 `ab36cef42bf2ada1299a078177499aac521805c7ec3278c558734e3a0301d259`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye4_source_DCM_optfreq/attempt_001/stdout.log`；SHA256 `c9ae11907242969b95ccec24ec550e285c15f5f16753cccfcd0e1720d457b0ff`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye4_toluene_source_method_TD20/attempt_001/input.inp`；SHA256 `4b4590229fbe30ef13a22bce3f892a3cbb53943c7c09d1893c48d527f11a91b0`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_3deba7268b769ce6/outputs/v2_dye4_toluene_source_method_TD20/attempt_001/stdout.log`；SHA256 `f38be82b6271e158d1d3397473b04f866d6f27ee01e0d0b4b6280e0e8e515892`；native_output；normal_marker=True
- `runs/hold_verification/group_5/dye3_identity_20260916/paper_3deba7268b769ce6/provenance/qzcli_hpc/dye3_correct_thiophene_s0_optfreq_20260916/20260916T063130_096116_341/input.inp`；SHA256 `c4efb8e85c3a41d86de36b7f17ce3a866fd06e34f7e2f324d43cc23a73c05073`；input；normal_marker=None
- `runs/hold_verification/group_5/dye3_identity_20260916/paper_3deba7268b769ce6/provenance/qzcli_hpc/dye3_correct_thiophene_s0_optfreq_20260916/20260916T063130_096116_341/orca_stdout.log`；SHA256 `66ee07dadfe7d19b5b5a5d74efe1135bf8f63d25cb20d5d2432e52c266b5eb77`；native_output；normal_marker=True
- `runs/hold_verification/group_5/followup_20260916/paper_3deba7268b769ce6/provenance/local_tests/recovery_20260914/dye3_correct_minimum_fulltddft_nto_20260916/20260916T110755_941206_3368861/input.inp`；SHA256 `c81c84cc48c5fc1dd6f77ddeb783e1bfd3d1f2d3e867264c966f7f6acd011780`；input；normal_marker=None
- `runs/hold_verification/group_5/followup_20260916/paper_3deba7268b769ce6/provenance/local_tests/recovery_20260914/dye3_correct_minimum_fulltddft_nto_20260916/20260916T110755_941206_3368861/orca_stdout.log`；SHA256 `b9e6315dada4bdc15580af89dbb9f31b8bed49d5fc5f7975027e4b4bd97eab82`；native_output；normal_marker=True

验证汇总/实际源页与分析：

- `docs/v2_verification/maintenance/closeout_push_20261017T0719Z/papers/paper_3deba7268b769ce6/REUSED_SCIENTIFIC_RESULTS.json`；SHA256 `cee34027a4580fbea72196fdd33ff0c13129f6b836354b0e9e6337c9d7ecf891`
- `docs/v2_verification/maintenance/closeout_push_20261017T0719Z/papers/paper_3deba7268b769ce6/NTO_REUSE_SUMMARY.json`；SHA256 `411784b5b36a72ad901520e1140e431bb2108c11b553ae76564b224649ce6cdc`
- `docs/v2_verification/maintenance/closeout_push_20261017T0719Z/papers/paper_3deba7268b769ce6/NATIVE_CHAIN_READBACK.json`；SHA256 `84fffeb50e32979d90e34d0eb6dc2ee78285e539b4b1b38f76e40a2ec639c703`
- `docs/v2_verification/maintenance/closeout_push_20261017T0719Z/papers/paper_3deba7268b769ce6/SOURCE_SCOPE_REVIEW.json`；SHA256 `2d603e207c1f497236a893dd2ccee4d151c2bec867cc34bb6699f647683ee600`
- `docs/v2_verification/maintenance/closeout_push_20261017T0719Z/papers/paper_3deba7268b769ce6/FROZEN_CONTRACT_READBACK.json`；SHA256 `3bd260c3b34f398428451066af002b16acdeedb82f0a258fb462bb89944fe126`
- `docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_3deba7268b769ce6/ROUTE_ALIGNMENT.json`；SHA256 `61c5e29320edb6275d263730f58e6b20d9a40af6e61573a7c704e43e7850a83e`
- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/papers/paper_3deba7268b769ce6/cases/DCM_dye3_samegeom_fullTD_20261011/RESPONSE_COMPARISON.json`；SHA256 `4009d97170e5083dd41fa9583c0ebdbfc867c0c9cb9b4bcbf47d49df4ae6aca4`
- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W03/papers/paper_3deba7268b769ce6/cases/Catalan_published_coefficients_audit_20261009/published_coefficients_audit.json`；SHA256 `21c258cb10022a9c1ac652bdb1fc1f9bd0c7b6e71fe3d8d594bfaef90a55168f`
- source_ict：{"path": "papers/paper_3deba7268b769ce6/documents/main.pdf", "sha256": "eebb2e959d968083e791e2ac19995200be51c821cdfe0ae30ecd75c64b5d6472", "pdf_pages_1based": [4, 5], "locator": "Fig5 ICT and unified TDDFT–Catalán interpretation; section4.4 disclosed calculation method"}
- source_solvents：{"path": "papers/paper_3deba7268b769ce6/documents/supplementary_001.pdf", "sha256": "2627a34461502ae5fe699c00912eca71ff17f9b55fda53d322910ba210d51761", "pdf_pages_1based": [5, 8], "locator": "TableS2 solvent transition energies; TableS3 fixed Catalán coefficients"}
- source_dye4：{"path": "papers/paper_3deba7268b769ce6/documents/supplementary_001.pdf", "sha256": "2627a34461502ae5fe699c00912eca71ff17f9b55fda53d322910ba210d51761", "pdf_pages_1based": [9], "locator": "FigS8 dye4 ICT and DCM excitation"}
- source_sample：{"path": "papers/paper_3deba7268b769ce6/documents/main.pdf", "sha256": "eebb2e959d968083e791e2ac19995200be51c821cdfe0ae30ecd75c64b5d6472", "pdf_pages_1based": [2, 3, 4, 5], "locator": "Scheme1 distinct identities; preparation/stability; Figs2–5 solvent response"}

## 时间与资源记录

本次迁移新增科学计算数0、HPC作业数0。历史输出中记录的逐作业资源可按原生/执行记录核查；没有统一完整的四篇总walltime、CPU-hour或费用记录，本报告不从核数或日志数量推算。失败、历史固定几何及控制计算不混入成功基线。

## 当前评分边界

中间科学结果76分；最终综合推断24分；全部定性叶子，满分或0。无精度充分校准的通用吸收/位移/结合能窗口，本轮不以最大残差拟合容差。身份、状态和证据是各项前提，不单独奖励。AR/PR具有相同物理判分清单；PR复现合同及合理替代义务仍由原题面约束，AR不被要求采用验证软件或固定搜索轨迹。

## 逐项科学规则—实际证据对应

下表明确本次验证对各项的支持，不使未来Agent自动获分。未来提交仍须独立有效证据。

| Rule / role / score | 实算支持 | 定位 |
|---|---|---|
| r_ict_dye3 / intermediate / 12 | Eight-system NTO evidence: donor phenolate→bridge/acceptor. CommonDCM fullTD top pairweight .93081004, TDA .92807936; no exactweight gate. | NTO_REUSE_SUMMARY.json; REUSED_SCIENTIFIC_RESULTS.json |
| r_ict_dye4 / intermediate / 12 | Eight-system NTO evidence: donor phenolate→bridge/acceptor. CommonDCM fullTD top pairweight .95585925,TDA .94397962. | NTO_REUSE_SUMMARY.json; REUSED_SCIENTIFIC_RESULTS.json |
| r_dye_energy_order / intermediate / 12 | CommonDCM fullTD56.9795927577<65.3699194198; TDA59.5619129038<68.2395048102 kcal/mol. | REUSED_SCIENTIFIC_RESULTS.json/DCM_values |
| r_solvent_shape_dye3 / intermediate / 12 | FixedCatalan57.42180→56.85472→63.64499 kcal/mol retains red then blue; experiment57.76→52.94→63.39. | REUSED_SCIENTIFIC_RESULTS.json/Catalan_results |
| r_methanol_stabilization_dye3 / intermediate / 8 | MeOH SA contribution+7.24185 kcal/mol together with independently computed donor→acceptor redistribution; not sole causal proof. | REUSED_SCIENTIFIC_RESULTS.json; NTO_REUSE_SUMMARY.json |
| r_solvent_shape_dye4 / intermediate / 12 | FixedCatalan61.60384→59.73978→70.11053; experiment61.75→59.44→69.23 kcal/mol. | REUSED_SCIENTIFIC_RESULTS.json/Catalan_results |
| r_methanol_stabilization_dye4 / intermediate / 8 | MeOH SA contribution+11.12595 kcal/mol plus independent ICT evidence. | REUSED_SCIENTIFIC_RESULTS.json; NTO_REUSE_SUMMARY.json |
| r_joint_solvatochromism_account / conclusion / 24 | Combined fixed-solvent interaction analysis and actual electronic evidence support bounded author account; additional pureCPCM Tol→EtOAc is blue, so continuum-only account fails. Short-lived/prepared samples remain bounded. | SOURCE_SCOPE_REVIEW.json; REUSED_SCIENTIFIC_RESULTS.json; NTO_REUSE_SUMMARY.json |

## 历史验证原文（保留；非当前验收/评分状态）

### 历史文件 docs/final_verified_science_v2_additions_20261020/astra_science_02/archive/autonomous_research/paper_3deba7268b769ce6/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot

# 已验证成功计算参考 — paper_3deba7268b769ce6 / autonomous_research

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 5）

正文 PDF p4 Dye3 的59.44 kcal/mol；不能把 SI 中另一个 dye 的同数值当身份依据。

[论文正文](../../../../papers/paper_3deba7268b769ce6/documents/main.pdf)；[当前成功结果与证据索引](../../../../runs/hold_verification/group_5/followup_20260916/paper_3deba7268b769ce6/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_3deba7268b769ce6/documents/supplementary_001.pdf)

## 2. 真实有效计算流程

1. 校准完整 Dye3 身份 C17H11N2O3S−、34 原子、E-imine、charge−1/singlet。五个 MMFF seeds 中选 seed2 再进 quantum；只一条完整 DFT 链，不伪称五构象都已 DFT 优化。
2. ORCA6.1.1 r2SCAN-3c/RI/CPCM Opt+Freq，102 modes=6 zeros+96 positive，最低8.08 cm⁻¹；原子连接与扭角判定来自终态，不从文件名判定。
3. 终态进行 full TDDFT ωB97X-D4/def2-TZVP/def2-J/RIJCOSX/CPCM，十 singlet roots，保存 NTO。按最低能可见态及电子性质选择 S1，不按与59.44的距离筛选：2.471173 eV=56.986603 kcal/mol、501.7 nm、f=1.815683526。
4. NTO/电子空穴片段支持 donor→nitrothiophene ICT，particle bridge≈.483、acceptor≈.369，不能设隐含 acceptor>50% 的门槛。S2≈356.1 nm 不是当前最低可见目标。

## 3. 有效产物与原始输入/输出


下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [dye3_correct_thiophene_s0_optfreq_20260916/20260916T063130_096116_341/orca_stdout.log](../../../../runs/hold_verification/group_5/dye3_identity_20260916/paper_3deba7268b769ce6/provenance/qzcli_hpc/dye3_correct_thiophene_s0_optfreq_20260916/20260916T063130_096116_341/orca_stdout.log)；[input.inp](../../../../runs/hold_verification/group_5/dye3_identity_20260916/paper_3deba7268b769ce6/provenance/qzcli_hpc/dye3_correct_thiophene_s0_optfreq_20260916/20260916T063130_096116_341/input.inp)
- [dye3_correct_minimum_fulltddft_nto_20260916/20260916T110755_941206_3368861/orca_stdout.log](../../../../runs/hold_verification/group_5/followup_20260916/paper_3deba7268b769ce6/provenance/local_tests/recovery_20260914/dye3_correct_minimum_fulltddft_nto_20260916/20260916T110755_941206_3368861/orca_stdout.log)；[input.inp](../../../../runs/hold_verification/group_5/followup_20260916/paper_3deba7268b769ce6/provenance/local_tests/recovery_20260914/dye3_correct_minimum_fulltddft_nto_20260916/20260916T110755_941206_3368861/input.inp)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `kp_ar_coverage` | The independent investigation retains candidate identity and validation context for the structures/states actually compared. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_minimum` | The selected candidate used for the vertical excitation is validated as a ground-state minimum. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_character` | The selected lowest visible transition has an explicit electronic-character analysis. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_ar_energy` | The selected lowest-energy visible dye-3 transition is reported quantitatively in kcal/mol. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `con_ar_final` | An independently covered and validated calculation can support assignment of dye-3's lowest visible excitation as a phenolate-to-nitroaryl ICT state within the stated model boundary. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

保留原59.44±3 kcal/mol容差，未为匹配改变选态或扩容差。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。

两模式共享的作者路线结果不等同于自主模式盲测。历史没有记录的自主假设、候选提出或路线决策，不因格式映射而编造成已经执行；科学子问题计算支持与自主过程能力得分应分开。

## 6. 2026-09-23 测量定义与当前任务的补充对应

正文 p4 区分低能可见 ICT 与高能 UV 局域态；原题面“lowest visible”未给操作窗口。采用公开 400–700 nm 主比较定义（明示为 benchmark 约定，不冒称作者阈值），最低能选态而非最亮/最近答案选态。既有结果 S1=501.7 nm、S2=356.1 nm，因此不改变历史选态、59.44 kcal/mol target 或 ±3 容差。无窗口内态应如实提交缺失主结果，不用 UV 态顶替；原电子分布分析保持。

