# V3 final-results scope and evidence reuse — 2026-10-28

Historical status is USER_ACCEPTED_DEVIATION, not strict numerical replication. The retained opening RRHO barrier is 6.47915454585207 kcal/mol (target 6.2 ±0.5); documented thermal variants span 6.205814785–6.479287064. The matched-grid direct-attack result is 21.271705690975633 kcal/mol versus the unchanged Table S22-derived target 21.920259635394032 ±0.5: residual −0.648553944418399, FAIL for that numeric outcome. UltraFine gives 21.28054020860675, so the grid shift −0.0088345176311 does not explain the residual. Source-user acceptance of about 0.65 kcal/mol does not alter the current window. Native opening/direct saddles have one negative mode (−82.8205/−303.8323 cm−1) and mode/two-sided-descent evidence, not full IRC. The 15-point constrained-geometry electronic path in MeCN decreases by 30.6018173 kcal/mol over N–N 3.35→1.39 Å; it is not a solution free-energy path or proof of diffusion control. The optimized product has N–N 1.270210347 Å and ligand O–H 0.973232916 Å, with positive frequencies (minimum 31.5233 cm−1), supporting local N–N formation and oxygen proton acceptance. Source Figure S57 shows the corresponding H–N/H–O exchange. This evidence supports a local mechanistic comparison, not the whole experimental catalytic cycle.

- `r_opening_g_barrier`: 正文PDF9–10、SI PDF70/S55、77–78/S22 → `docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_e2d9397dff2a3f0f/NATIVE_READBACK.json` opening_reactant/TS；RRHO势垒6.4791545 kcal/mol，目标6.2±0.5，窗内。最低模23.9413 / −82.8205 cm−1，模式/两侧下降只作势垒证据。
- `r_direct_attack_g_barrier`: 正文PDF10、SI S22 → `docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/RU_SAME_BARRIER_GRID_RESULT.json`；21.271705691 vs21.9202596354±0.5 kcal/mol，残差−0.648553944，超窗fail。网格变动仅−0.0088345，不能消除偏差。
- `r_post_opening_nn_path`: SI PDF71/S57 → `docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/results/profile.json`；15点N–N3.35→1.39 Å，相对第一点电子能0→−30.6018 kcal/mol且单调下降。native open_product全正频率、N–N1.27021 Å；不代表溶液自由能全程无垒或扩散控制。
- `r_opening_preferred_local_route`: 正文PDF9–10及SI S55–57 → 上述势垒与有限路径共同支持局部开环后成键；直接势垒超窗不自动使此项失败；不能据此断言全催化循环RDS。
- `r_oxygen_proton_acceptor_role`: SI PDF71/S57同时显示H1–O2形成/H1–N2断裂 → native open_product：N–N1.2702103、O–H0.9732329 Å，正曲率；支持局部羧酸氧受质子，不外推整个bcs循环。

This update performs no new scientific calculation or validation. Historical PASS labels below are not a new V3 overall pass. The active rubric is `paper_science_v3` / `final_results_100`; all preceding versions and numerical conflicts remain archival evidence.

---

# V2 验证计算参考：Ru–bda–Py局部反应

论文：`paper_e2d9397dff2a3f0f`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：历史用户明确接受数值偏差（USER_ACCEPTED_DEVIATION），不计入 30 篇无额外偏差授权的独立严格通过。** 下述科学计算已完成，但保留未解释的数值/定义差异。

当前验收依据：必要局部计算已完成，按用户已明确接受约0.65 kcal/mol偏差使用。将特许验收与残差已独立解释的严格通过分列，避免夸大。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

局部含氮模型与NH3形成N–N键的可行化学及配体环境作用。

冻结题面中的科学目标：

For the source Ru–bda–Py nitrogen-containing model, what local molecular chemistry can support N–N bond formation with ammonia, and what role, if any, can be established for the ligand environment?

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

The source attributes the bda model's behaviour to N–O stabilization in15bda, a6.2kcal/mol opening step viaTS3bda, and a21.9kcal/mol direct NH3-attack barrier; after opening, a downhill electronic scan is interpreted as diffusion-controlled attack (main pp9–10; SI FiguresS55–S57). Forbcs, a dangling sulfonate is proposed to assist proton transfer during N–N formation. These are source assignments to reproduce/audit, not compulsory correct conclusions. SI PDFp47 specifies Gaussian16 B3LYP-D3(BJ), SDD(Ru)/6-31G(d,p) optimization and frequencies, def2-TZVP single points withSMD MeCN and298.15K Gibbs corrections; source standard-state corrections include1atm→1M, solvent concentration19.2M, Fc absolute4.548V and specified proton reference. Keep electrochemical/proton reservoirs distinct from chemical barriers. The supplied source model inventory does not certify a singlet or N–O minimum; raw modes/endpoints are needed for a saddle claim. Additional bda/bcs paired routes were benchmark development choices, not all source calculations.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_e2d9397dff2a3f0f/documents/main.pdf](../../../../papers/paper_e2d9397dff2a3f0f/documents/main.pdf) | `c24bbaae86761a8d40104b001d415708990565d075c29789011a3c8104993875` |
| [papers/paper_e2d9397dff2a3f0f/documents/supplementary_001.pdf](../../../../papers/paper_e2d9397dff2a3f0f/documents/supplementary_001.pdf) | `1f4f524a63c1856d741bc9b9016079f9fe8ba2eea9117df6a2df9f72bd626975` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

B3LYP-D3BJ/SDD(Ru)低层OptFreq，def2-TZVP/SMD MeCN单点与298.15 K热项；NH3角函数/对称数及一次1M修正明确。

1. 从作者局部 Ru–bda–Py/NH3 反应路线核对原子、电荷/自旋及分离反应物参照；NH3 的角函数/对称数与其他组分一同检查，避免不同热参考导致伪差。

2. 核收 B3LYP-D3BJ、SDD(Ru) 低层 Opt/Freq 和 def2TZVP/SMD MeCN 高层单点，按 298.15 K 合并热项，1 atm→1 M 只修正一次。每个参考态、最低点与所用鞍点有独立原生记录。

3. 检查鞍点位移、双侧下降连通性及已完成的十五点开环后扫描，支持局部路径。该证据不是完整 IRC，也不是全催化循环/扩散控制认证。

4. 以同一计量重建直接进攻与开环势垒 21.2717057/6.4791545 kcal/mol，对源 21.9202596/6.2；主效应差约 14.79 对源 15.72。实际 SuperFine 控制仅改变约 −0.0088345 kcal/mol，不足以解释全部 −0.6485539 的直接进攻残差。

5. 沿用用户已接受的小势垒差，基于完整局部计算、参考态和保持的主效应认证当前科学问题；保留残差未唯一归因的事实，不声称精确速率、完整 IRC 或源势垒末位一致。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| N–O opening barrier (kcal/mol) | 6.2 | {"native_RRHO":6.47915454585207,"five_thermal_range":[6.205814785293632,6.4792870636030155]} | 同+1 singlet Ru-bda/reference→TS,N–O mode及双侧minima。 Opening has its own executed thermal sensitivity6.205815–6.479287 and validated mode/endpoints. Neither the old±2 benchmark tolerance nor this interval is transferred to the directNH3 barrier. |
| Direct NH3 attack ΔG‡,source1M (kcal/mol) | 21.920259635394032 | {"UltraFine_baseline":21.28054020860675,"SuperFine_control":21.271705690975633} | Matched low5D/high5D NH3; 298.15K gas RRHO with physical sigma3, SMD MeCN high SP and one -1.9 kcal/mol association standard-state correction. Baseline and numerical control remain separate. Completed same-reaction XC grid refinement changes the barrier by -0.008834518 kcal/mol. Baseline residual -0.639719427 and refined residual -0.648553944 remain. This control supplies no physical/source tolerance and does not prove all numerical approximations harmless. |
| NH3 low energy and Gcorr (Eh) | {"low":-56.55763,"Gcorr":0.01642} | {"low":-56.5576304118,"Gcorr_sigma3":0.016420293098368417} | sourceSI physical77(printS76);low5D表示及physicalσ3。 定向控制解释旧6D不一致，geometry匹配/6正模/σ3各一次独立通过；printed吻合是诊断不是整题PASS。 |
| High SP electronic residuals (Eh) | {"closed":-1518.21089,"direct_TS":-1574.78835,"NH3":-56.5956} | {"UltraFine_baseline":{"closed":-1518.20025581,"direct_TS":-1574.77613261,"NH3":-56.5930936353},"SuperFine_control":{"closed":-1518.20025106,"direct_TS":-1574.7761419,"NH3":-56.5930935966}} | actualsourcefunctional/basis/SMD definition reproduction; independentECP/state控制。 All three SMD/D3BJ high-SP results are native-valid. Their noncancelling source residual survives the matched-reference and grid controls. No absolute-energy last-digit pass criterion is imposed. |
| After-opening electronic scan / product | sourceFigS57 downhill; no explicit diffusion coefficient | {"15point_drop_kcal":-30.601817272631134,"product_NN_A":1.2702103470287904,"product_OH_A":0.973232916348394} | gasconstrainedgeometries with SMD electronicSP, separatelyfreeproductpositivecurvature。 支持finite化学可行性与protonacceptor几何；不给solutionkineticdiffusion/RDS认证。 |
| Same-reaction XC-grid sensitivity (kcal/mol) | No source grid-convergence value disclosed | -0.008834517631118644 | Exactly the same three geometries/states, B3LYP-D3BJ/def2TZVP/SMD MeCN, and identical RRHO/standard-state terms; UltraFine to SuperFine only. Completed same-reaction XC grid refinement changes the barrier by -0.008834518 kcal/mol. Baseline residual -0.639719427 and refined residual -0.648553944 remain. This control supplies no physical/source tolerance and does not prove all numerical approximations harmless.；这是保留的非必要源差异，不作为已复现量。 |

直接进攻源21.9202596→实算21.2717057 kcal/mol，差-0.6485539；开环6.2→6.4791545；两障碍差约15.72→14.79。网格控制仅0.0088345，未解释全部直接进攻残差。

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Ligand, nitrogen and electronic inventories

冻结要求：Verify bda/Py constitution and any analogue, ammonia/proton/electron accounting and source model versus experimental catalyst distinction. Do not encode an unknown N–O bond as a fixed identity or infer spin from an oxidation-state label. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：局部结构、鞍点/模式、双侧下降连结、15点开环后扫描、统一标准态均已实际执行，源局部大尺度结论保持。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

作者Ru–bda–Py及NH3局部模型的配体/氮库存、电荷自旋与分离参照绑定；低层SDD(Ru)与高层def2TZVP/SMD MeCN的实际输入/输出均可追溯。

证据记录：`E0011`。

```json
[
  {
    "source_locator": "SI47/73,77–78,81; current bda/Py inventory",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/gaussian.log",
        "sha256": "89942fd590f3732d69a458347f099236dcc17021d5ef8260441b80e6b5fc93a7"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "ba3e19266254e3a1240aa0e158c776ea0ae152df8482f890c42308dc22f491be"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/gaussian.log",
        "sha256": "0d1f26f274a66947a6897abaab121dde022e9a5c85efe704b93b43ee0d23a6ef"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/MATCHED_REFERENCE_RESULT.json",
        "sha256": "2154938e979fc30275f4a533dceb0a5d411dad2af3813e2426c7c8c1135fefdd"
      }
    ]
  }
]
```


证据记录：`E0066`。

```json
[
  {
    "raw_evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/gaussian.log",
        "sha256": "89942fd590f3732d69a458347f099236dcc17021d5ef8260441b80e6b5fc93a7"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "ba3e19266254e3a1240aa0e158c776ea0ae152df8482f890c42308dc22f491be"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/gaussian.log",
        "sha256": "0d1f26f274a66947a6897abaab121dde022e9a5c85efe704b93b43ee0d23a6ef"
      }
    ]
  },
  {
    "source_locator": "SI47/73,77–78,81; current bda/Py inventory",
    "actual_result": "48原子Ru–bda–Py–N/q+1/singlet，加入NH3后52原子C22H19N6O4Ru；240显式电子及Ru28core，NH3 q0/singlet与物理σ3。",
    "reason": "未把源氧化态标签用作spin证明；实际原生charge/multiplicity、成键/模式与全库存均检验，解释限制在此局部自旋模型。",
    "raw_evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/gaussian.log",
        "sha256": "89942fd590f3732d69a458347f099236dcc17021d5ef8260441b80e6b5fc93a7"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "ba3e19266254e3a1240aa0e158c776ea0ae152df8482f890c42308dc22f491be"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/gaussian.log",
        "sha256": "0d1f26f274a66947a6897abaab121dde022e9a5c85efe704b93b43ee0d23a6ef"
      }
    ]
  }
]
```


涉及源辅助量与本题必要量的判定采用第 1 节最终裁决；以上旧记录不被解读为所有源输出均精确重现。

### kp_reactivity — Quantitative evidence for local nitrogen chemistry

冻结要求：Compute or quantitatively analyze relevant local structure/reactivity and connect it to N–N formation. An old imaginary-frequency scalar or orbital drawing alone does not establish the chemistry. Appropriate non-author routes and evidence-backed unresolved states are eligible. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：局部结构、鞍点/模式、双侧下降连结、15点开环后扫描、统一标准态均已实际执行，源局部大尺度结论保持。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

实际低层Opt/Freq、高层SP及热项给直接进攻/开环势垒21.2717057/6.4791545kcal/mol，对源21.9202596/6.2；两通道约14.79对15.72kcal/mol的主效应保持。

证据记录：`E0011`。

```json
[
  {
    "source_locator": "mainp10/SI70–71FigsS55–S57",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log",
        "sha256": "c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "ba3e19266254e3a1240aa0e158c776ea0ae152df8482f890c42308dc22f491be"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_after_open_NH3_approach1_scan/a01/gaussian.log",
        "sha256": "130384cb41c46f6e7591fdb0c5c4d78c1446658eb676e58d02c8b4d34ebe042a"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/gaussian.log",
        "sha256": "5294f895c1cb83bccbe17a3b32e076f12b0bed253b670abd6611a638bc75eb18"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/direct_attack_TS_review_20260930.json",
        "sha256": "ed1059f503459adb880db0bcf5ea5d6e04dfc00219f47ea93707e7443154dfea"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/open_scan15_profile_review_20261001.json",
        "sha256": "af331eac6d24f6e3b5cce5c54060f7251b39cc40cf24facf51ce6c0ba96781b1"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/MATCHED_REFERENCE_RESULT.json",
        "sha256": "2154938e979fc30275f4a533dceb0a5d411dad2af3813e2426c7c8c1135fefdd"
      }
    ]
  }
]
```


证据记录：`E0066`。

```json
[
  {
    "raw_evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log",
        "sha256": "c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "ba3e19266254e3a1240aa0e158c776ea0ae152df8482f890c42308dc22f491be"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_after_open_NH3_approach1_scan/a01/gaussian.log",
        "sha256": "130384cb41c46f6e7591fdb0c5c4d78c1446658eb676e58d02c8b4d34ebe042a"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/gaussian.log",
        "sha256": "5294f895c1cb83bccbe17a3b32e076f12b0bed253b670abd6611a638bc75eb18"
      }
    ]
  },
  {
    "source_locator": "mainp10/SI70–71FigsS55–S57",
    "actual_result": "N–O opening6.47915455kcal/mol/−82.8205i；direct−303.8323i，N–N1.865244Å，两下降盆地断/成N10–N49；matched直接1M21.280540，open15点电子下降30.601817。",
    "reason": "已有新N–N证据覆盖扩展问题。源量21.920260与实算不一致另列，不能把旧opening通过当新增直接势垒自动通过。",
    "raw_evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log",
        "sha256": "c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "ba3e19266254e3a1240aa0e158c776ea0ae152df8482f890c42308dc22f491be"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_after_open_NH3_approach1_scan/a01/gaussian.log",
        "sha256": "130384cb41c46f6e7591fdb0c5c4d78c1446658eb676e58d02c8b4d34ebe042a"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/gaussian.log",
        "sha256": "5294f895c1cb83bccbe17a3b32e076f12b0bed253b670abd6611a638bc75eb18"
      }
    ]
  }
]
```


涉及源辅助量与本题必要量的判定采用第 1 节最终裁决；以上旧记录不被解读为所有源输出均精确重现。

### kp_causality — Ligand-role and pathway claims tested

冻结要求：Assess actual evidence for any claimed ligand role or required transformation. A claimed transition state needs chemically relevant displacement and endpoint evidence; a downhill electronic scan cannot by itself prove diffusion-controlled solution kinetics. No bcs control or N–O opening branch is obligatory. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：局部结构、鞍点/模式、双侧下降连结、15点开环后扫描、统一标准态均已实际执行，源局部大尺度结论保持。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

鞍点位移、双侧下降连通与15点开环后扫描支持局部路径和配体环境角色；这些是已执行的局部证据，不冒称完整IRC或唯一完整催化机理。

证据记录：`E0011`。

```json
[
  {
    "source_locator": "mainp10 N–Ogate andSI55/57",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "ba3e19266254e3a1240aa0e158c776ea0ae152df8482f890c42308dc22f491be"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/gaussian.log",
        "sha256": "67b70ff52bb0c3e5113a0304b637f9b5948f4e54ccd63f27f06db48c24ff982a"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/direct_attack_two_endpoint_review_20260930.json",
        "sha256": "8013bf43303892bceb2cc0199843ffd60dc86c1676a31e5e1be796ca83ab7ce5"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/open_Int3bda_minimum_review_20260930.json",
        "sha256": "0bd02742c93684ed46e581a511d57beb7d44c8008a5303e948ae39f9c15b56a2"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/open_scan15_profile_review_20261001.json",
        "sha256": "af331eac6d24f6e3b5cce5c54060f7251b39cc40cf24facf51ce6c0ba96781b1"
      }
    ]
  }
]
```


证据记录：`E0066`。

```json
[
  {
    "raw_evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "ba3e19266254e3a1240aa0e158c776ea0ae152df8482f890c42308dc22f491be"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/gaussian.log",
        "sha256": "67b70ff52bb0c3e5113a0304b637f9b5948f4e54ccd63f27f06db48c24ff982a"
      }
    ]
  },
  {
    "source_locator": "mainp10 N–Ogate andSI55/57",
    "actual_result": "直接attack两侧三个氢仍在N49；after-opening产物NN1.270210、O–H0.973233Å，支持不同局部氮/质子化学；有限电子曲线未证diffusioncontrol。",
    "reason": "以结构/模式/端点改变约束bda位点作用，不把ligand替换或全周期RDS矩阵强加为任务；未计算全局动力学不称已证不可识别，只撤回无证据的强推断。",
    "raw_evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "ba3e19266254e3a1240aa0e158c776ea0ae152df8482f890c42308dc22f491be"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/gaussian.log",
        "sha256": "67b70ff52bb0c3e5113a0304b637f9b5948f4e54ccd63f27f06db48c24ff982a"
      }
    ]
  }
]
```


涉及源辅助量与本题必要量的判定采用第 1 节最终裁决；以上旧记录不被解读为所有源输出均精确重现。

### kp_reference — Energy reservoirs and model uncertainty

冻结要求：Use consistent N/H/electron inventories, standard states, MeCN conditions and relevant spin/model sensitivity. Oxidation free energy at an applied potential is not an elementary chemical activation barrier. Bound uncertainty without transferring old arbitrary tolerances. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：局部结构、鞍点/模式、双侧下降连结、15点开环后扫描、统一标准态均已实际执行，源局部大尺度结论保持。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

同计量参考态、NH3角函数/对称数、298.15K热项与仅一次1M修正已核。SuperFine改变约−0.0088345kcal/mol，不足解释全部残差；沿用用户接受的小势垒差，不用事后通用容差或精确速率包装。

证据记录：`E0011`。

```json
[
  {
    "source_locator": "SI47 298.15K/1M/PCET;SI77 NH3 andSI78 Ru",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/gaussian.log",
        "sha256": "0d1f26f274a66947a6897abaab121dde022e9a5c85efe704b93b43ee0d23a6ef"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/gaussian.log",
        "sha256": "f400428d9d284b36340e481c75dd57759c044fa1ef84afe70e874a2992a998a1"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/gaussian.log",
        "sha256": "0b9b5f90c50b4cbe1e73ace7e778b670f8a92ddc140cfa558e097c068e0e0c49"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/MATCHED_REFERENCE_RESULT.json",
        "sha256": "2154938e979fc30275f4a533dceb0a5d411dad2af3813e2426c7c8c1135fefdd"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/MATCHED_REFERENCE_NATIVE_REVIEW_20261008.json",
        "sha256": "9146fa12435a40d8f9999fe3c02280908415199df7b4e3c4e13e81884f62fb94"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/opening_thermal_sensitivity.json",
        "sha256": "90366f5051233dcb168a6b59bd7b6654c165dd4514506a1a11493e77f53cac9e"
      }
    ]
  }
]
```


证据记录：`E0066`。

```json
[
  {
    "raw_evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/gaussian.log",
        "sha256": "0d1f26f274a66947a6897abaab121dde022e9a5c85efe704b93b43ee0d23a6ef"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/gaussian.log",
        "sha256": "f400428d9d284b36340e481c75dd57759c044fa1ef84afe70e874a2992a998a1"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/gaussian.log",
        "sha256": "0b9b5f90c50b4cbe1e73ace7e778b670f8a92ddc140cfa558e097c068e0e0c49"
      }
    ]
  },
  {
    "source_locator": "SI47 298.15K/1M/PCET;SI77 NH3 andSI78 Ru",
    "actual_result": "NH3 low5D−56.5576304118，Gcorrσ3=0.016420293098，匹配high5D−56.5930936353Eh；direct1M21.280540209vs21.920259635，残差−0.639719427。",
    "reason": "低/高同几何、RRHO/σ3/−1.9各一次；SMD-CDS已包含不重加。残差具有明确数值/适用范围，足以回答参考不确定性，但未被接受为源核心数值重现。",
    "raw_evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/gaussian.log",
        "sha256": "0d1f26f274a66947a6897abaab121dde022e9a5c85efe704b93b43ee0d23a6ef"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/gaussian.log",
        "sha256": "f400428d9d284b36340e481c75dd57759c044fa1ef84afe70e874a2992a998a1"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/gaussian.log",
        "sha256": "0b9b5f90c50b4cbe1e73ace7e778b670f8a92ddc140cfa558e097c068e0e0c49"
      }
    ]
  }
]
```


涉及源辅助量与本题必要量的判定采用第 1 节最终裁决；以上旧记录不被解读为所有源输出均精确重现。

### kp_conclusion — Local result separated from catalytic performance

冻结要求：A valid answer may support, qualify or refute the source N–O rationale or leave it unresolved after sufficient evidence. Do not infer global rate determination, turnover or experimental catalyst ranking solely from one model barrier. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：局部结构、鞍点/模式、双侧下降连结、15点开环后扫描、统一标准态均已实际执行，源局部大尺度结论保持。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

认证局部分子N–N化学及作者路径比较，不外推全循环、周转速率、扩散控制或实际催化性能。

证据记录：`E0011`。

```json
[
  {
    "source_locator": "currentlocal bda objective, mainp10–11",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log",
        "sha256": "c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/gaussian.log",
        "sha256": "67b70ff52bb0c3e5113a0304b637f9b5948f4e54ccd63f27f06db48c24ff982a"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/gaussian.log",
        "sha256": "5294f895c1cb83bccbe17a3b32e076f12b0bed253b670abd6611a638bc75eb18"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/MATCHED_REFERENCE_RESULT.json",
        "sha256": "2154938e979fc30275f4a533dceb0a5d411dad2af3813e2426c7c8c1135fefdd"
      }
    ]
  }
]
```


证据记录：`E0066`。

```json
[
  {
    "raw_evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log",
        "sha256": "c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/gaussian.log",
        "sha256": "67b70ff52bb0c3e5113a0304b637f9b5948f4e54ccd63f27f06db48c24ff982a"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/gaussian.log",
        "sha256": "5294f895c1cb83bccbe17a3b32e076f12b0bed253b670abd6611a638bc75eb18"
      }
    ]
  },
  {
    "source_locator": "currentlocal bda objective, mainp10–11",
    "actual_result": "在+1单重态的完整Ru–bda–(Py)2–N有限模型中，N–O接触为优化所得局部特征，开环鞍点有一个相关虚频及双侧下降端点；源6.2 kcal/mol开环量复现为6.479155，热约定控制为6.2058–6.4793。加入NH3后，直接N–N进攻鞍点的虚频为−303.8323 cm−1，N10–N49方向主导且两侧盆地分别没有/形成该键；源方法匹配5D NH3参考、物理σ=3和一次1M修正后，直接升高为21.280540 kcal/mol，源表同定义21.920260，残差−0.639719需保留。开环后的15个SMD电子单点沿N–N靠近单调下降30.601817 kcal/mol，所对应产物N–N=1.270210 Å、O–H=0.973233 Å支持局部N–N形成和bda氧接受质子的可能性。由此可支持N–O占位与打开影响局部进攻的解释；不能由有限电子扫描证明溶液扩散控制、开环是唯一必要通路，或推出全周期RDS/TOF及bcs优于bda的定量因果。NH3低层5D和σ3问题已实际修复，高SP源残差未被这些控制解释，因此当前答案有效但不把新增源21.9量宣布严格一致。",
    "reason": "现题明确可支持或修正localN–O解释；结论不依赖未证globalRDS、bcs排名或速率。不是只说源不明，而有闭合参考、两类N–N结果和thermal控制。",
    "raw_evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log",
        "sha256": "c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/gaussian.log",
        "sha256": "67b70ff52bb0c3e5113a0304b637f9b5948f4e54ccd63f27f06db48c24ff982a"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/gaussian.log",
        "sha256": "5294f895c1cb83bccbe17a3b32e076f12b0bed253b670abd6611a638bc75eb18"
      }
    ]
  }
]
```


涉及源辅助量与本题必要量的判定采用第 1 节最终裁决；以上旧记录不被解读为所有源输出均精确重现。

### conclusion_investigation — For the source Ru–bda–Py nitrogen-containing model, what local molecular chemistry can support N–N bond formation with ammonia, and what role, if any, can be established for the ligand environment?

冻结要求：Answer the bounded question with claims proportional to the evidence. Support, correction, refutation and demonstrated unresolved conclusions are equally eligible. Partial/failure status preserves real work but does not confer completion credit. No required author winner or named control list.

当前复审：局部结构、鞍点/模式、双侧下降连结、15点开环后扫描、统一标准态均已实际执行，源局部大尺度结论保持。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

完整局部计算与参照链支持当前Ru–bda–Py模型的路径/配体解释；所需主效应在用户已接受的数值误差下保持，按2026-10-11统一裁决通过。

证据记录：`E0011`。

```json
[
  {
    "source_locator": "current AR/PR objective andsourceFigsS55–57",
    "evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log",
        "sha256": "c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/gaussian.log",
        "sha256": "67b70ff52bb0c3e5113a0304b637f9b5948f4e54ccd63f27f06db48c24ff982a"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/gaussian.log",
        "sha256": "f400428d9d284b36340e481c75dd57759c044fa1ef84afe70e874a2992a998a1"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/MATCHED_REFERENCE_RESULT.json",
        "sha256": "2154938e979fc30275f4a533dceb0a5d411dad2af3813e2426c7c8c1135fefdd"
      },
      {
        "kind": "analysis",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/open_scan15_profile_review_20261001.json",
        "sha256": "af331eac6d24f6e3b5cce5c54060f7251b39cc40cf24facf51ce6c0ba96781b1"
      }
    ]
  }
]
```


证据记录：`E0066`。

```json
[
  {
    "raw_evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log",
        "sha256": "c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/gaussian.log",
        "sha256": "67b70ff52bb0c3e5113a0304b637f9b5948f4e54ccd63f27f06db48c24ff982a"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/gaussian.log",
        "sha256": "f400428d9d284b36340e481c75dd57759c044fa1ef84afe70e874a2992a998a1"
      }
    ]
  },
  {
    "source_locator": "current AR/PR objective andsourceFigsS55–57",
    "actual_result": "在+1单重态的完整Ru–bda–(Py)2–N有限模型中，N–O接触为优化所得局部特征，开环鞍点有一个相关虚频及双侧下降端点；源6.2 kcal/mol开环量复现为6.479155，热约定控制为6.2058–6.4793。加入NH3后，直接N–N进攻鞍点的虚频为−303.8323 cm−1，N10–N49方向主导且两侧盆地分别没有/形成该键；源方法匹配5D NH3参考、物理σ=3和一次1M修正后，直接升高为21.280540 kcal/mol，源表同定义21.920260，残差−0.639719需保留。开环后的15个SMD电子单点沿N–N靠近单调下降30.601817 kcal/mol，所对应产物N–N=1.270210 Å、O–H=0.973233 Å支持局部N–N形成和bda氧接受质子的可能性。由此可支持N–O占位与打开影响局部进攻的解释；不能由有限电子扫描证明溶液扩散控制、开环是唯一必要通路，或推出全周期RDS/TOF及bcs优于bda的定量因果。NH3低层5D和σ3问题已实际修复，高SP源残差未被这些控制解释，因此当前答案有效但不把新增源21.9量宣布严格一致。",
    "reason": "限定科学问题有完整实际回答；必须和严格新增源21.9量未重现分开，因此交TASK_VALID_SOURCE_CONFLICT而不扩大opening旧±2容差。",
    "raw_evidence": [
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log",
        "sha256": "c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log",
        "sha256": "1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log",
        "sha256": "8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/gaussian.log",
        "sha256": "67b70ff52bb0c3e5113a0304b637f9b5948f4e54ccd63f27f06db48c24ff982a"
      },
      {
        "kind": "native_log",
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/gaussian.log",
        "sha256": "f400428d9d284b36340e481c75dd57759c044fa1ef84afe70e874a2992a998a1"
      }
    ]
  }
]
```


涉及源辅助量与本题必要量的判定采用第 1 节最终裁决；以上旧记录不被解读为所有源输出均精确重现。

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 16.25 小时；16 份计时日志/47 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 4,20 线程/进程；Gaussian %Mem=100GB,16GB,48GB,8GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0025 · 5bda_author_route_strict_v2/1/gaussian.log](../../../../docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/gaussian.log) | Gaussian:339.6；Gaussian:755.9；Gaussian:756 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0026 · TS3bda_author_route_strict_v2/1/gaussian.log](../../../../docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log) | Gaussian:938.2；Gaussian:811.5；Gaussian:853.1 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0027 · bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log) | Gaussian:936.6；Gaussian:828.8；Gaussian:781.1 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0028 · direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log) | Gaussian:3858.1；Gaussian:817.3；Gaussian:781.1 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0029 · direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log) | Gaussian:1561.9；Gaussian:831.8；Gaussian:798.3 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0030 · bda_open_attack_source_product_optfreq_sp/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/gaussian.log) | Gaussian:562.4；Gaussian:832.5；Gaussian:787 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0031 · bda_after_open_NH3_approach1_scan/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_after_open_NH3_approach1_scan/a01/gaussian.log) | Gaussian:14844 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0032 · bda_open_scan15_MeCN_high_SP/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/gaussian.log) | Gaussian:1089.4；Gaussian:1096.7；Gaussian:1096.1；Gaussian:1100.3；Gaussian:1088.7；Gaussian:1083.7；Gaussian:1087.7；Gaussian:1091.9；Gaussian:1097.6；Gaussian:1097；Gaussian:1106；Gaussian:1097.3；Gaussian:1179.6；Gaussian:1128.9；Gaussian:1108.9 | 正常；正常；正常；正常；正常；正常；正常；正常；正常；正常；正常；正常；正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0033 · Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/gaussian.log) | Gaussian:1106.8 | 正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0034 · a01/low5D/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/gaussian.log) | Gaussian:3；Gaussian:2.5 | 正常；正常 | {"threads":[4],"Gaussian_mem":["8GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0035 · NH3_5D_matched_reference_20261007/a01/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/gaussian.log) | Gaussian:4.9 | 正常 | {"threads":[4],"Gaussian_mem":["8GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0036 · bda_mode_minus_descent_optfreq_sp/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_minus_descent_optfreq_sp/a01/gaussian.log) | Gaussian:2324.1；Gaussian:705.5；Gaussian:695.3 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0037 · bda_mode_plus_descent_optfreq_sp/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_plus_descent_optfreq_sp/a01/gaussian.log) | Gaussian:2323.8；Gaussian:701.9；Gaussian:696 | 正常；正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0075 · Ru_same_barrier_grid_20261009/a01/runner.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/runner.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0082 · a01/closed/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/closed/gaussian.log) | Gaussian:336.3 | 正常 | {"threads":[20],"Gaussian_mem":["48GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0087 · a01/direct_TS/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/direct_TS/gaussian.log) | Gaussian:380.9 | 正常 | {"threads":[20],"Gaussian_mem":["48GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0092 · a01/NH3/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/NH3/gaussian.log) | Gaussian:2.6 | 正常 | {"threads":[20],"Gaussian_mem":["48GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0180 · open_scan15_common_reference_analysis/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/analysis.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

双侧模式下降不是完整IRC；扫描不是扩散动力学证明；不认证全循环速控或精确速率。V3新增bds/bcs比较独立验收。

模式双侧下降不是完整IRC；没有把局部扫描当扩散动力学或全循环速控证明。未披露高层细节/余差根因尚未确定，但不声称所有作者细节逐项相同。


```json
{
  "paper_id": "paper_e2d9397dff2a3f0f",
  "initial_recommendation": "PASS_USER_ACCEPTED_DEVIATION",
  "final_status": "STRICT_PASS",
  "basis": "局部作者路线、参考态/标准态、优化频率、高层单点、相关鞍点及双侧下降连接、15点开环后扫描均已实际完成。直接进攻/开环源21.9203/6.2，实算21.2717/6.4792kcal/mol，关键差距约15.72→14.79；与硅烯使用相同的合理误差与效应尺度判断，且用户已明确允许约0.65kcal偏差，所以计入当前标准通过。网格只改变约0.0088kcal，不足以解释全部残差，但残差根因未唯一恢复不等于缺少必需计算。不得宣称精确势垒/速率、完整IRC、全催化循环或扩散控制已证实。",
  "cross_review": "strict38_audit1 reasonable-error consistency review plus root source/native review",
  "core_evidence_complete": true,
  "prior_user_accepted_numerical_deviation_applies": true,
  "unresolved_residual_cause": "high-level direct-attack barrier residual not fully attributed; no new universal tolerance"
}
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

此处沿用用户既有明确授权，不能把未解释残差改称已恢复作者全部定义，也不能将该偏差接受方式推广到其他论文。V3 扩展任务的验收另行记录。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_e2d9397dff2a3f0f.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_e2d9397dff2a3f0f/verified_computation_reference.md)；SHA-256 `7dc4529454a2e22d4e75257beb8dfc9cdc4fcccbb7ec90316a232ccb87a03ecf`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/USER_ACCEPTANCE_20261009.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/USER_ACCEPTANCE_20261009.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_USER_ACCEPTANCE_20261009.json) | `5a249d6ba64ab5bc3f05ad72eeb3e1fa1bb9b04522aa7ca1a2c650f07c297eb2` | evidence_or_analysis |
| E0002 | [tasks/v2_autonomous_research/paper_e2d9397dff2a3f0f/agent_input/task.md](../../../v2_autonomous_research/paper_e2d9397dff2a3f0f/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0002_task.md) | `42019b6302b8b1bd2c19209ea083431902a1dafd534ef4e69b46c853406c5ec1` | historical_task_binding |
| E0003 | [tasks/v2_paper_reproduction/paper_e2d9397dff2a3f0f/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0003_task.md) | `af9496c6c3c5b7f8ecf029675fa207e5becbed600528610947abf5d4548ecb3f` | historical_task_binding |
| E0004 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/TWO_DEVIATION_PRIMARY_READBACK.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/TWO_DEVIATION_PRIMARY_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_TWO_DEVIATION_PRIMARY_READBACK.json) | `b3b76c15c96f593e457d7ac95e98d4e4378f5e70e354803d22805ff9973ac4e3` | evidence_or_analysis |
| E0005 | [docs/v2_verification/history/v2_verified_task_export_20261011/TWO_USER_ACCEPTED_NATIVE_READBACK.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/TWO_USER_ACCEPTED_NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_TWO_USER_ACCEPTED_NATIVE_READBACK.json) | `2355a4f183bdce9fdb04456a0707cb8cde6d0263d22d829272e393c201658610` | evidence_or_analysis |
| E0006 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_e2d9397dff2a3f0f/NATIVE_COMPUTATION_INDEX.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_e2d9397dff2a3f0f/NATIVE_COMPUTATION_INDEX.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0006_NATIVE_COMPUTATION_INDEX.json) | `c8f1d34c50baf251d36f005077d258f63ffe106b7c863c2342cc0352ca87cbd1` | evidence_or_analysis |
| E0007 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_e2d9397dff2a3f0f/COMPUTATION_INVENTORY.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_e2d9397dff2a3f0f/COMPUTATION_INVENTORY.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0007_COMPUTATION_INVENTORY.json) | `8f8595f480d02abd53fe600eaa432680215b1f2c15d2b56dbc5809e20a20cf7d` | evidence_or_analysis |
| E0008 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/SOURCE_COMPARISON_RETURNED_fc709021fa12a55d.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/SOURCE_COMPARISON_RETURNED_fc709021fa12a55d.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0008_SOURCE_COMPARISON_RETURNED_fc709021fa12a55d.json) | `61837cfcd59458013b5d42cd67bd17d35ea6339b81139006c07036b2bf70abb2` | evidence_or_analysis |
| E0009 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/SAME_QUANTITY_NUMERICAL_CONTROL_PLAN.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/SAME_QUANTITY_NUMERICAL_CONTROL_PLAN.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0009_SAME_QUANTITY_NUMERICAL_CONTROL_PLAN.json) | `606bcfd1e9d2d3a36949b3adf49b0d43a20a8ea17a64e3abb8082fc1d9369bb8` | evidence_or_analysis |
| E0010 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/PUBLIC_DATA_LINK_AUDIT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/PUBLIC_DATA_LINK_AUDIT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0010_PUBLIC_DATA_LINK_AUDIT.json) | `7bd6271c0c7e8094daa6d04941632e999f5d02dd02e27c1a013fe28f32382c2d` | evidence_or_analysis |
| E0011 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/SOURCE_COMPARISON.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/SOURCE_COMPARISON.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0011_SOURCE_COMPARISON.json) | `1a43e644fb68e4faba7366e3a252188b9d2ddd23ef02529115752aaf28cfddbb` | evidence_or_analysis |
| E0012 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/RETURNED_GRID_NATIVE_REVIEW_fc709021fa12a55d.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/RETURNED_GRID_NATIVE_REVIEW_fc709021fa12a55d.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0012_RETURNED_GRID_NATIVE_REVIEW_fc709021fa12a55d.json) | `3176d410dd22876916e59b449cdb2c7c58b44b288822d850f37fdca7cab63c27` | evidence_or_analysis |
| E0013 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/RETURNED_fc709021fa12a55d_PLATFORM.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/RETURNED_fc709021fa12a55d_PLATFORM.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_RETURNED_fc709021fa12a55d_PLATFORM.json) | `2cafc549371f6248aa426c49cda70b83f103e363a1a85f373b5eb20309bdcb50` | evidence_or_analysis |
| E0014 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_e2d9397dff2a3f0f.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_e2d9397dff2a3f0f.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_paper_e2d9397dff2a3f0f.md) | `bd52786099d6b47c98d85b30ade02dad4b00341c99509aaf1e10968809811ab7` | evidence_or_analysis |
| E0015 | [docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `518a0c32e2b04fe8f2d48bd192ffe2c6beff5963b70a88a6ded83e7502ed0951` | historical_task_binding |
| E0016 | [tasks/v2_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot) | `518a0c32e2b04fe8f2d48bd192ffe2c6beff5963b70a88a6ded83e7502ed0951` | historical_task_binding |
| E0017 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e2d9397dff2a3f0f/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e2d9397dff2a3f0f/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0017_task.md) | `42019b6302b8b1bd2c19209ea083431902a1dafd534ef4e69b46c853406c5ec1` | historical_task_binding |
| E0018 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e2d9397dff2a3f0f/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e2d9397dff2a3f0f/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0018_reference_key_points.json) | `9fdbe8be8895697ec055a4a556fe9594225bfc52c5b49051d659f43f124563f6` | historical_task_binding |
| E0019 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e2d9397dff2a3f0f/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e2d9397dff2a3f0f/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0019_reference_conclusions.json) | `34a5aff65d243d1fe5fe2cd0d0eb626347df720d02b67213a19f88551ceff8b7` | historical_task_binding |
| E0020 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e2d9397dff2a3f0f/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e2d9397dff2a3f0f/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0020_task.md) | `af9496c6c3c5b7f8ecf029675fa207e5becbed600528610947abf5d4548ecb3f` | historical_task_binding |
| E0021 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0021_reference_key_points.json) | `9fdbe8be8895697ec055a4a556fe9594225bfc52c5b49051d659f43f124563f6` | historical_task_binding |
| E0022 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0022_reference_conclusions.json) | `34a5aff65d243d1fe5fe2cd0d0eb626347df720d02b67213a19f88551ceff8b7` | historical_task_binding |
| E0023 | [papers/paper_e2d9397dff2a3f0f/documents/main.pdf](../../../../papers/paper_e2d9397dff2a3f0f/documents/main.pdf) | `c24bbaae86761a8d40104b001d415708990565d075c29789011a3c8104993875` | source_document |
| E0024 | [papers/paper_e2d9397dff2a3f0f/documents/supplementary_001.pdf](../../../../papers/paper_e2d9397dff2a3f0f/documents/supplementary_001.pdf) | `1f4f524a63c1856d741bc9b9016079f9fe8ba2eea9117df6a2df9f72bd626975` | source_document |
| E0025 | [docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/gaussian.log](../../../../docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0025_native_excerpt.json) | `89942fd590f3732d69a458347f099236dcc17021d5ef8260441b80e6b5fc93a7` | native_output |
| E0026 | [docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log](../../../../docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0026_native_excerpt.json) | `c687cac9bfbc690369c2e1b3955ff372827a178a82ff2601ff07697b3d1fb6a2` | native_output |
| E0027 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0027_native_excerpt.json) | `1a428e02a08097f67da530d52b66d766c1f4d02555ed4e7e43a816248b13265b` | native_output |
| E0028 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0028_native_excerpt.json) | `ba3e19266254e3a1240aa0e158c776ea0ae152df8482f890c42308dc22f491be` | native_output |
| E0029 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0029_native_excerpt.json) | `8a733cd3d0e7f76f0404ed4cb3dacac90ba6b06dbe102d8320d57806454ba12c` | native_output |
| E0030 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0030_native_excerpt.json) | `67b70ff52bb0c3e5113a0304b637f9b5948f4e54ccd63f27f06db48c24ff982a` | native_output |
| E0031 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_after_open_NH3_approach1_scan/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_after_open_NH3_approach1_scan/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_native_excerpt.json) | `130384cb41c46f6e7591fdb0c5c4d78c1446658eb676e58d02c8b4d34ebe042a` | native_output |
| E0032 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0032_native_excerpt.json) | `5294f895c1cb83bccbe17a3b32e076f12b0bed253b670abd6611a638bc75eb18` | native_output |
| E0033 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_native_excerpt.json) | `0b9b5f90c50b4cbe1e73ace7e778b670f8a92ddc140cfa558e097c068e0e0c49` | native_output |
| E0034 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0034_native_excerpt.json) | `0d1f26f274a66947a6897abaab121dde022e9a5c85efe704b93b43ee0d23a6ef` | native_output |
| E0035 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0035_native_excerpt.json) | `f400428d9d284b36340e481c75dd57759c044fa1ef84afe70e874a2992a998a1` | native_output |
| E0036 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_minus_descent_optfreq_sp/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_minus_descent_optfreq_sp/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0036_native_excerpt.json) | `5855c15179ecbae042df1113dfa57687321c9cd111f21c9faa127fc9a14a9288` | native_output |
| E0037 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_plus_descent_optfreq_sp/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_plus_descent_optfreq_sp/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0037_native_excerpt.json) | `c0c98e377145ba52fd45ad4c24a1e28b57d491ce0681d817a99fb68c3d61bed6` | native_output |
| E0059 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/MATCHED_REFERENCE_RESULT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/MATCHED_REFERENCE_RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0059_MATCHED_REFERENCE_RESULT.json) | `2154938e979fc30275f4a533dceb0a5d411dad2af3813e2426c7c8c1135fefdd` | evidence_or_analysis |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/direct_attack_TS_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/direct_attack_TS_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0060_direct_attack_TS_review_20260930.json) | `ed1059f503459adb880db0bcf5ea5d6e04dfc00219f47ea93707e7443154dfea` | evidence_or_analysis |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/open_scan15_profile_review_20261001.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/open_scan15_profile_review_20261001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_open_scan15_profile_review_20261001.json) | `af331eac6d24f6e3b5cce5c54060f7251b39cc40cf24facf51ce6c0ba96781b1` | evidence_or_analysis |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/direct_attack_two_endpoint_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/direct_attack_two_endpoint_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_direct_attack_two_endpoint_review_20260930.json) | `8013bf43303892bceb2cc0199843ffd60dc86c1676a31e5e1be796ca83ab7ce5` | evidence_or_analysis |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/open_Int3bda_minimum_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/open_Int3bda_minimum_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0063_open_Int3bda_minimum_review_20260930.json) | `0bd02742c93684ed46e581a511d57beb7d44c8008a5303e948ae39f9c15b56a2` | evidence_or_analysis |
| E0064 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/MATCHED_REFERENCE_NATIVE_REVIEW_20261008.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/MATCHED_REFERENCE_NATIVE_REVIEW_20261008.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_MATCHED_REFERENCE_NATIVE_REVIEW_20261008.json) | `9146fa12435a40d8f9999fe3c02280908415199df7b4e3c4e13e81884f62fb94` | evidence_or_analysis |
| E0065 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/opening_thermal_sensitivity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/opening_thermal_sensitivity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0065_opening_thermal_sensitivity.json) | `90366f5051233dcb168a6b59bd7b6654c165dd4514506a1a11493e77f53cac9e` | evidence_or_analysis |
| E0066 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_e2d9397dff2a3f0f/CURRENT_QUESTION_REVIEW.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_e2d9397dff2a3f0f/CURRENT_QUESTION_REVIEW.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0066_CURRENT_QUESTION_REVIEW.json) | `ac1fa33ab54ddf2049b799dd7f9a612595f704af1ac49d9d77302bd12dd30731` | evidence_or_analysis |
| E0067 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/deliveries/W08_PUBLIC_SOURCE_RECHECK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/deliveries/W08_PUBLIC_SOURCE_RECHECK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0067_W08_PUBLIC_SOURCE_RECHECK.json) | `28aaa1c990f8f58745938dafa72aede78e48e97af2b5d1071b1a9a3bc469d217` | evidence_or_analysis |
| E0068 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/SOURCE_EXCERPTS.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e2d9397dff2a3f0f/SOURCE_EXCERPTS.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0068_SOURCE_EXCERPTS.txt) | `869325639cc7a5e39a577741e53efe52c387f2b9110c77b4a5918676b56f6908` | evidence_or_analysis |
| E0069 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/deliveries/W08_NEW_JOB_ACCEPTANCE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/deliveries/W08_NEW_JOB_ACCEPTANCE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0069_W08_NEW_JOB_ACCEPTANCE.json) | `e6226fdffa0b116c031fb1a9fd1ade13d735f03ac84c99e53c84042fd335edca` | evidence_or_analysis |
| E0070 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/RU_SAME_BARRIER_GRID_RESULT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/RU_SAME_BARRIER_GRID_RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0070_RU_SAME_BARRIER_GRID_RESULT.json) | `4cd8b185dc8c38981d187ddcf0d2b914f36642e9f059b83983c61caffb853470` | evidence_or_analysis |
| E0071 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/native_acceptance.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/native_acceptance.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0071_native_acceptance.json) | `b28c3ec2dafe4c69be9fe572959b8ec80fb49e0069c40c8ba201566154ef9481` | evidence_or_analysis |
| E0072 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/native-return-code.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0072_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0073 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/status.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0073_status.json) | `7c3c398d976e212a1d71b3e5e9de31649f84d83df4b88d5b507584a03c464b3e` | evidence_or_analysis |
| E0074 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/runtime-started.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/runtime-started.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0074_runtime-started.txt) | `0c19c9ca464a559304ec8c7b92c946e51c7e5b40db3390a18477e7b41f1255a1` | evidence_or_analysis |
| E0075 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/runner.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/runner.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0075_native_excerpt.json) | `230350d4789d9b4b5ccd50a2d76f85719294cf766b12c8194ed382c89aefc872` | native_output |
| E0076 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/inputs.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/inputs.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0076_inputs.json) | `bb316d7a97cd28e430d6310deb59517e0da3f03fbab84e97b609fa242cc86445` | evidence_or_analysis |
| E0077 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/inputs.sha256](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/inputs.sha256) | `cf9bbd91e871972bbf42f724b5f31e01aa14fc5d0ab9150251d57dcca885a4cf` | evidence_or_analysis |
| E0078 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/analysis.py](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0078_analysis.py) | `10bfb91c68920d7366ba8f04f9367e7ce2b887e2003ad14d675f8db7145b7dbb` | input_or_analysis_code |
| E0079 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/preparation.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/preparation.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0079_preparation.json) | `b016a9c7fb4a19267aa8a758b83c0afb62957f259c98c12dea32ac3ddbd908e5` | evidence_or_analysis |
| E0080 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/submission.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0080_submission.json) | `2678d07060dd03964ef86b358e661f7497b10aafe768062ed4f25e1cd6b530f2` | evidence_or_analysis |
| E0081 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/submit-intent.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0081_submit-intent.json) | `5978e0c59c95197b4b54b62058067b90f1013846bb1bc555cffca20dcb3099d2` | evidence_or_analysis |
| E0082 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/closed/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/closed/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0082_native_excerpt.json) | `b23d8042aa294938b29a0e0c7457824be49280f046e06eca7dbbab5cab6a9d58` | native_output |
| E0083 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/closed/native_status.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/closed/native_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0083_native_status.json) | `2a2cd4af42c410f7bea1dee39bdecc47cf815c852641ef615c8727e60bc30654` | evidence_or_analysis |
| E0084 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/closed/ACCEPTED_RESULT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/closed/ACCEPTED_RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0084_ACCEPTED_RESULT.json) | `a3d94af1baa351aa69c94eeea4401f7433d3705079a67a471d55e5db4fdea0fa` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/closed.com](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/closed.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0085_closed.com) | `74f6fdc5a0c64780c3d3d6d2f08b5dfd4ab1d0ce6a2a722b0c6f4b10a9e8680a` | input_or_analysis_code |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_minus_descent_optfreq_sp/a01/job.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_minus_descent_optfreq_sp/a01/job.chk) | `5f6491957e1e4e1d200adcb76488d25b72c388266c3eac61e57b5a9d15de5a20` | evidence_or_analysis |
| E0087 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/direct_TS/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/direct_TS/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0087_native_excerpt.json) | `b1a104ab4f284356e0ee091e9f5ec8b6c6b2d1e753bd216a9fdde6a9b7552e2f` | native_output |
| E0088 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/direct_TS/native_status.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/direct_TS/native_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0088_native_status.json) | `134aaa02396e6ca52247b1a26b8995124c504bb5745f12e8f869dc2f33bef60f` | evidence_or_analysis |
| E0089 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/direct_TS/ACCEPTED_RESULT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/direct_TS/ACCEPTED_RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0089_ACCEPTED_RESULT.json) | `b3f01dc65f48d77ff5be1c3007eb241fcfc631cee6b686d7ae3a9dcde98ea2fe` | evidence_or_analysis |
| E0090 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/direct_TS.com](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/direct_TS.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0090_direct_TS.com) | `09d476fa46f6cb9610ef8dc44de957fce4bc5999d0d4387892d0d8c7c75dca9a` | input_or_analysis_code |
| E0091 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/job.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/job.chk) | `8f3e4a739b03b607f90db98b54713ac30f890704df031cfd84f81ad23fb25e7c` | evidence_or_analysis |
| E0092 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/NH3/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/NH3/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0092_native_excerpt.json) | `fe6ab2bf4d255064c7a36958de61680b23c99f8f650ecfe512d252188fb08a58` | native_output |
| E0093 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/NH3/native_status.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/NH3/native_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0093_native_status.json) | `8ba6d3bd501eb9a775488c3035d0cf1fe265f6a256751d1a721e2bd8325f8159` | evidence_or_analysis |
| E0094 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/NH3/ACCEPTED_RESULT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/NH3/ACCEPTED_RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0094_ACCEPTED_RESULT.json) | `01a43f3bce9bab6f62c9ed003e73e6a09e204a103f5c648766c3770cf135e566` | evidence_or_analysis |
| E0095 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/NH3.com](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/NH3.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0095_NH3.com) | `89506a5032f26a6631446862481dcbae37a377fdf4f94f138e2ce211b2a4caf0` | input_or_analysis_code |
| E0096 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/matched_high.chk](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/matched_high.chk) | `339a1847b933ee495c1f6841ef4111db6e4061235614aacba43b5e00b04d11f4` | evidence_or_analysis |
| E0097 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/parent_NH3.chk](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/parent_NH3.chk) | `339a1847b933ee495c1f6841ef4111db6e4061235614aacba43b5e00b04d11f4` | evidence_or_analysis |
| E0098 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/parent_closed.chk](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/parent_closed.chk) | `5f6491957e1e4e1d200adcb76488d25b72c388266c3eac61e57b5a9d15de5a20` | evidence_or_analysis |
| E0099 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/parent_direct_TS.chk](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/parent_direct_TS.chk) | `8f3e4a739b03b607f90db98b54713ac30f890704df031cfd84f81ad23fb25e7c` | evidence_or_analysis |
| E0100 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/run.sh](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0100_run.sh) | `15ba9d1ee26c37f0f40d7d24e05ccebd9ffa9e14c1d5b43f0144b220fecb3193` | input_or_analysis_code |
| E0101 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/ROOT_RETURNED_JOB_INTAKE_20261009.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/ROOT_RETURNED_JOB_INTAKE_20261009.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0101_ROOT_RETURNED_JOB_INTAKE_20261009.json) | `9cab3a349e52d46dbd3bf74c4881b650b2eb8815a6167221bcf2d156f570b2d7` | evidence_or_analysis |
| E0102 | [docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/input.com](../../../../docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0102_input.com) | `d903c563af24537d673d832313d4b289cc4d737df528f002fea8716db4262570` | input_or_analysis_code |
| E0103 | [docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/source_input.com](../../../../docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/5bda_author_route_strict_v2/1/source_input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0103_source_input.com) | `ee9296729fcf50c5677771e5bac290734c3bd3b0da433c76443b06778beb8417` | input_or_analysis_code |
| E0104 | [docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/input.com](../../../../docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0104_input.com) | `c0e5d24af061f57bba9a3189c5aabd56e31515b4951fd151fc03840bb1a2b004` | input_or_analysis_code |
| E0105 | [docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/source_input.com](../../../../docs/v2_verification/history/verification/group_3/paper_e2d9397dff2a3f0f/provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/source_input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0105_source_input.com) | `4a3bf0b87305a165920ef6f356c2504dd3a3313bd01c2b7237fa487e5b3bec1b` | input_or_analysis_code |
| E0106 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0106_run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | input_or_analysis_code |
| E0107 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0107_input.com) | `64be7ddc844a7dc6612343773152d34dd85484fd4ae13eeef139d704c10e5ec7` | input_or_analysis_code |
| E0108 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0108_run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | input_or_analysis_code |
| E0109 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0109_input.com) | `e6ee7ca04ec967e07aa6ae3789920469df41f54539a33b94d364fa8a131ec677` | input_or_analysis_code |
| E0110 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0110_run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | input_or_analysis_code |
| E0111 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_plus_descent_optfreq_sp/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0111_input.com) | `95988ff0852facf168413ab4719befb650d16d9eae136fb763681a10aa4cd212` | input_or_analysis_code |
| E0112 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0112_run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | input_or_analysis_code |
| E0113 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0113_input.com) | `37a16fa7a3b2ffcf5d3d62b6619670fe9ea4a5f07729f7a1cc3193b8c77b9ff7` | input_or_analysis_code |
| E0114 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_after_open_NH3_approach1_scan/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_after_open_NH3_approach1_scan/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0114_run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | input_or_analysis_code |
| E0115 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_after_open_NH3_approach1_scan/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_after_open_NH3_approach1_scan/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0115_input.com) | `7e925e723eb8e7a32c80260d9403e7306831da406854e1c253f31e79f5f49c1f` | input_or_analysis_code |
| E0116 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0116_run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | input_or_analysis_code |
| E0117 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_scan15_MeCN_high_SP/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0117_input.com) | `37a73e93a2c997f9a8f7d6bf87f28060c2de69b6a74d9ed370a864e0bf8ff102` | input_or_analysis_code |
| E0118 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0118_analysis.py) | `79e09adeff3343271d14ada5d54bfdb5bb3346937a02287bd228f7097f697a33` | input_or_analysis_code |
| E0119 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/singlepoint.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/singlepoint.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0119_singlepoint.com) | `f70d454399111d8c9c02af93e9878aa294264f441d95990df4b2d4779fc8f2ae` | input_or_analysis_code |
| E0120 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/Ru_TS3prime_independent_highSP_ECP_control_20261002/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0120_run.sh) | `a1f0651595f1bea2aa6fc655d914afff2bc622cc0615c3b2ce168232dc09eff3` | input_or_analysis_code |
| E0121 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/input.com](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0121_input.com) | `096a903b69492be67a476b690dbd2ffee155fe5e9e3c1fbaa802f9616bc8525a` | input_or_analysis_code |
| E0122 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/analysis.py](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0122_analysis.py) | `432e693ba855e540b4518bcaf674c718048da8bc97af1adb02f6bfbb5fb38c2b` | input_or_analysis_code |
| E0123 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/run.sh](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0123_run.sh) | `c530855aa1d51ee05e394a64aa8749b4b3aff19f13a60801856903301c28ebd2` | input_or_analysis_code |
| E0124 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/input.com](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0124_input.com) | `9b45ce5fc10f20af740c4f0a07cc79b46ddc46df92104ee354a78afbac08e660` | input_or_analysis_code |
| E0125 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_minus_descent_optfreq_sp/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_minus_descent_optfreq_sp/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0125_run.sh) | `63f9b04bc6ab9ad9fad832b306a7255ad0fc8f0cd24ffc8f291e7b482ccfd190` | input_or_analysis_code |
| E0126 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_minus_descent_optfreq_sp/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_minus_descent_optfreq_sp/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0126_input.com) | `ed74b2402ad2b1eac7986103159d5deef0c6b4b1c7cb7ca189187c2f7567204d` | input_or_analysis_code |
| E0127 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_plus_descent_optfreq_sp/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_plus_descent_optfreq_sp/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0127_run.sh) | `63f9b04bc6ab9ad9fad832b306a7255ad0fc8f0cd24ffc8f291e7b482ccfd190` | input_or_analysis_code |
| E0128 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_plus_descent_optfreq_sp/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/outputs/bda_mode_plus_descent_optfreq_sp/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0128_input.com) | `cb2fb2cf97d548ab72c8f5d3312e0b89b080fbeaf8f7bc67afda4ba43481a8f2` | input_or_analysis_code |
| E0168 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/contract_snapshot/20260929T145459Z/binding.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/contract_snapshot/20260929T145459Z/binding.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0168_binding.json) | `e58f02b7680bf5127df6b11c53277c2c934dc137f6270dbee4a09cd56b99b683` | evidence_or_analysis |
| E0169 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0169_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0170 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0170_status.json) | `5b6dd64e223ab444e84664bdc3ce96e3997dbe092dab41736043b05d974ac848` | evidence_or_analysis |
| E0171 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_direct_attack_source_ts_optfreq_sp/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0171_submission.json) | `9ab05f036d01ee32c2864d9cd40c49e98dd7e546559205c6041588567cb8be3a` | evidence_or_analysis |
| E0172 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/author_NH3_attack_preparation_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/author_NH3_attack_preparation_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0172_author_NH3_attack_preparation_20260930.json) | `db71ff98bd6abc534710d6cd6a4f71262025adfc3f5715d42befd493048ae6bd` | evidence_or_analysis |
| E0173 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/inputs/source_extracts/supplementary_001.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/inputs/source_extracts/supplementary_001.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0173_supplementary_001.txt) | `b0216ed88ae1b0727ab57dc8774f924255ab126447c160aee7283700376a18e1` | evidence_or_analysis |
| E0174 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/inputs/direct_attack_mode_minus_descent_optfreq_sp/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/inputs/direct_attack_mode_minus_descent_optfreq_sp/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0174_input.com) | `e6ee7ca04ec967e07aa6ae3789920469df41f54539a33b94d364fa8a131ec677` | input_or_analysis_code |
| E0175 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/inputs/direct_attack_mode_plus_descent_optfreq_sp/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/inputs/direct_attack_mode_plus_descent_optfreq_sp/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0175_input.com) | `95988ff0852facf168413ab4719befb650d16d9eae136fb763681a10aa4cd212` | input_or_analysis_code |
| E0176 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0176_analysis.py) | `dfb2197e40fdf2a44913b38dfb7e82d6b859190d188ffc37801d4ea4873eb007` | input_or_analysis_code |
| E0177 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0177_submission.json) | `e67ce91f3d86ad26af762c44a557d94955bcaa6aa982857ae1e0944ca6d0bfdb` | evidence_or_analysis |
| E0178 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0178_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0179 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0179_status.json) | `4ad55707adca6b1745fa6217775c316a3660a17299e90ef112dd51930ea80f1b` | evidence_or_analysis |
| E0180 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/analysis.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/analysis.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0180_native_excerpt.json) | `4904119313ae3f667d8c99825ec0c338f3a34823dfdd8d433cedf5b9a31e6eac` | native_output |
| E0181 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/results/profile.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/results/profile.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0181_profile.json) | `70c52a8b0468ab665c92e02c30ec9668e1151bb3ba4039ce63160e5084f31569` | evidence_or_analysis |
| E0182 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/results/profile.csv](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/results/profile.csv)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0182_profile.csv) | `762bb09600c44c34fa5700151c07b27a3cfa69d9aa50aec4ac404feaf16b32f7` | evidence_or_analysis |
| E0183 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0183_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0184 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0184_status.json) | `2d003f9ef497ae888f8ade0c91e82221d02bea1dda2ebdb7af5eb9eba117db62` | evidence_or_analysis |
| E0185 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/direct_attack_mode_minus_descent_optfreq_sp/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0185_submission.json) | `48134feb47fdfb52ebf1a37753b70a3c2d60cf07d0c40dba5701750e8cee5565` | evidence_or_analysis |
| E0186 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/direct_attack_TS_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/direct_attack_TS_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0186_direct_attack_TS_review_20260930.json) | `ed1059f503459adb880db0bcf5ea5d6e04dfc00219f47ea93707e7443154dfea` | evidence_or_analysis |
| E0187 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/direct_attack_plus_endpoint_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/direct_attack_plus_endpoint_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0187_direct_attack_plus_endpoint_review_20260930.json) | `501e0ff5a37147b4544859a970aa04c74f619956f9640a2e04b545dd8079252e` | evidence_or_analysis |
| E0188 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/balanced_attack_ledger_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/balanced_attack_ledger_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0188_balanced_attack_ledger_review_20260930.json) | `8bde3d2be40f2cc6f3c746cd7d8a7a2bd3fbc5e4cad7f119658227d806f2c77e` | evidence_or_analysis |
| E0189 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0189_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0190 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0190_status.json) | `f63f9ea431f1c1f6b92f9c39730a3da85b4c4577d00b7c243e8c91abc02ea21a` | evidence_or_analysis |
| E0191 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/bda_open_attack_source_product_optfreq_sp/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0191_submission.json) | `334dd95524bd3cc8cee864410404536b0401d82e7883a3032072c84d97041f49` | evidence_or_analysis |
| E0192 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/open_route_preparation_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/open_route_preparation_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0192_open_route_preparation_review_20260930.json) | `d2228248fd41bed3157f815a622ded272f61a778d7f2a6d473d744d02bdb2f15` | evidence_or_analysis |
| E0193 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/inputs/bda_open_attack_source_product_optfreq_sp.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/inputs/bda_open_attack_source_product_optfreq_sp.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0193_bda_open_attack_source_product_optfreq_sp.com) | `37a16fa7a3b2ffcf5d3d62b6619670fe9ea4a5f07729f7a1cc3193b8c77b9ff7` | input_or_analysis_code |
| E0194 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/provenance/ligand_attack_preparation.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/provenance/ligand_attack_preparation.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0194_ligand_attack_preparation.json) | `6587dbc9d5373d1f17a6b20fd290d3912dc0aea01e55352fb511f1ef2f1f69b5` | evidence_or_analysis |
| E0195 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/inputs/open_route_audited_20260930/bda_open_attack_source_product_optfreq_sp.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/inputs/open_route_audited_20260930/bda_open_attack_source_product_optfreq_sp.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0195_bda_open_attack_source_product_optfreq_sp.com) | `37a16fa7a3b2ffcf5d3d62b6619670fe9ea4a5f07729f7a1cc3193b8c77b9ff7` | input_or_analysis_code |
| E0196 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/control.chk](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/low5D/control.chk) | `36e753a87faa34627f8eb8123928588b296d03a9ed16945f1a914ecde3304747` | evidence_or_analysis |
| E0197 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/NH3_D_REPRESENTATION_RESULT.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_d_representation_20261007/a01/NH3_D_REPRESENTATION_RESULT.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0197_NH3_D_REPRESENTATION_RESULT.json) | `9448408483889517c338f529de80bef6b822d48b46975d30cd3e48f453777af3` | evidence_or_analysis |
| E0198 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/balanced_attack_ledger_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/data/balanced_attack_ledger_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0198_balanced_attack_ledger_review_20260930.json) | `8bde3d2be40f2cc6f3c746cd7d8a7a2bd3fbc5e4cad7f119658227d806f2c77e` | evidence_or_analysis |
| E0199 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/gaussian-return-code.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/gaussian-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0199_gaussian-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0200 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/inputs.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/inputs.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0200_inputs.json) | `70338c2f3ee432340d06c7eff96f5bd8fa3834e3d722d97dc31dc2a004a1e342` | evidence_or_analysis |
| E0201 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/native_acceptance.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/native_acceptance.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0201_native_acceptance.json) | `70eb093e52ccc42506ae3925a19174bcba890ee60cf06879ead31869a5951260` | evidence_or_analysis |
| E0202 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/status.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0202_status.json) | `fc339e3be74f5a8e2e8cc4f7793440a20dc3b334c6d42ce3df643eef08b2aebf` | evidence_or_analysis |
| E0203 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/submission.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/NH3_5D_matched_reference_20261007/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0203_submission.json) | `a720c21f13c67f67bc3702dfffaa03b5e0a1b54bac589f17598313887eb15cd6` | evidence_or_analysis |
| E0204 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/legacy/strict_v2_deep_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/legacy/strict_v2_deep_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0204_strict_v2_deep_audit.json) | `dce90313536e63e2e8b09b81dca40e4fb14f58539422dea4a59fd9bc2cfb0754` | evidence_or_analysis |
| E0205 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/provenance/mode_descent_results.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/provenance/mode_descent_results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0205_mode_descent_results.json) | `ae53bce6999267ef31151578c0a6e60908238136949e3877ab61305ad49116cb` | evidence_or_analysis |
| E0206 | [.envs/general-modern-openmpi5/lib/python3.11/site-packages/goodvibes/thermo.py](../../../../.envs/general-modern-openmpi5/lib/python3.11/site-packages/goodvibes/thermo.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0206_thermo.py) | `b3c6614418407d47042792e9bfb120ede83f0db51d1cfbf82b5005fa14bb17ba` | input_or_analysis_code |
| E0207 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_e2d9397dff2a3f0f/NATIVE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_e2d9397dff2a3f0f/NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0207_NATIVE_READBACK.json) | `b59f25add228daab2605356cac630605c42f3d6060a19adc97a903326d6832f7` | evidence_or_analysis |
| E0208 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W08_RETURN_INTAKE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W08_RETURN_INTAKE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0208_W08_RETURN_INTAKE.json) | `ffcd8d44104220283be1f0de54d1fe9782f69ac6f5a70d93251052e05204f265` | evidence_or_analysis |
| E0209 | [tasks/final_verified_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/scoring_rules.json](../../../final_verified_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0209_scoring_rules.json) | `5bde899f9895382f69f97b62c8ffe7962057061f5aa54cc0680dd653e7ca3d86` | historical_task_binding |
| E0210 | [tasks/final_verified_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/verified_computation_reference.md](../../../final_verified_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/verified_computation_reference.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0210_verified_computation_reference.md) | `518a0c32e2b04fe8f2d48bd192ffe2c6beff5963b70a88a6ded83e7502ed0951` | historical_task_binding |
| E0211 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e2d9397dff2a3f0f/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e2d9397dff2a3f0f/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0211_scoring_rules.json) | `9570880dcea966cef13408f20a4531e87806bfbb75f8af1e97d0fed90bcd8796` | historical_task_binding |
| E0212 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e2d9397dff2a3f0f/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e2d9397dff2a3f0f/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0212_critical_failures.json) | `7e0a5b2ceb116e1a3dbc3347d1d0eb1bd0ca5e5c26be21a15bfc5b55479345cc` | historical_task_binding |
| E0213 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e2d9397dff2a3f0f/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e2d9397dff2a3f0f/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0213_package_manifest.json) | `cc0ac03d0ab72abe51f6b9b988554473ece9687b2ec22ae6b0e2336f11db64a5` | historical_task_binding |
| E0214 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0214_scoring_rules.json) | `9570880dcea966cef13408f20a4531e87806bfbb75f8af1e97d0fed90bcd8796` | historical_task_binding |
| E0215 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0215_critical_failures.json) | `7e0a5b2ceb116e1a3dbc3347d1d0eb1bd0ca5e5c26be21a15bfc5b55479345cc` | historical_task_binding |
| E0216 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e2d9397dff2a3f0f/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e2d9397dff2a3f0f/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0216_package_manifest.json) | `c1f32537e54e70f5ee3db73ac89432e7dd23c27b317223b13d51fe8a376362e0` | historical_task_binding |
| E0217 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/events_20261007/PUBLIC_SOURCE_RECHECK_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/events_20261007/PUBLIC_SOURCE_RECHECK_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0217_PUBLIC_SOURCE_RECHECK_20261007.json) | `b6791f0ceb0562a7fce789546e252f2937021b57b8a7bca3c15d35a716c2e01b` | evidence_or_analysis |
| E0218 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/FINAL_STARTUP_READBACK_20261009.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W08/papers/paper_e2d9397dff2a3f0f/outputs/Ru_same_barrier_grid_20261009/a01/FINAL_STARTUP_READBACK_20261009.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0218_FINAL_STARTUP_READBACK_20261009.json) | `db057fc072b026637980b010390df8821ecac576e0093e0627c6bc8e68a47ece` | evidence_or_analysis |
| E0219 | [.software_cache/installations/gaussian/g16/install/g16/g16](../../../../.software_cache/installations/gaussian/g16/install/g16/g16) | `384f3baca38297d3f11ed2168bb9be836778fa4c5f5d07cb38751e3ed1a66db5` | evidence_or_analysis |
| E0220 | [docs/v2_verification/history/strict_author_route_validation_20261001/HPC_SUBMISSION.lock](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/HPC_SUBMISSION.lock) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | evidence_or_analysis |
| E0221 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_e2d9397dff2a3f0f/v2_execution_20260929/outputs/open_scan15_common_reference_analysis/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_e2d9397dff2a3f0f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0221_run.sh) | `5738c81aac2165a40faba8a662076543fece72a2357f258ecab8e81155d364ec` | input_or_analysis_code |
| N0162 | [tasks/v2_autonomous_research/paper_e2d9397dff2a3f0f/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_e2d9397dff2a3f0f/evaluation/reference_key_points.json) | `9fdbe8be8895697ec055a4a556fe9594225bfc52c5b49051d659f43f124563f6` | latest_review_evidence |
| N0163 | [tasks/v2_autonomous_research/paper_e2d9397dff2a3f0f/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_e2d9397dff2a3f0f/evaluation/reference_conclusions.json) | `34a5aff65d243d1fe5fe2cd0d0eb626347df720d02b67213a19f88551ceff8b7` | latest_review_evidence |
| N0164 | [tasks/v2_autonomous_research/paper_e2d9397dff2a3f0f/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_e2d9397dff2a3f0f/evaluation/scoring_rules.json) | `9570880dcea966cef13408f20a4531e87806bfbb75f8af1e97d0fed90bcd8796` | latest_review_evidence |
| N0165 | [tasks/v2_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/reference_key_points.json](reference_key_points.json) | `9fdbe8be8895697ec055a4a556fe9594225bfc52c5b49051d659f43f124563f6` | latest_review_evidence |
| N0166 | [tasks/v2_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/reference_conclusions.json](reference_conclusions.json) | `34a5aff65d243d1fe5fe2cd0d0eb626347df720d02b67213a19f88551ceff8b7` | latest_review_evidence |
| N0167 | [tasks/v2_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/scoring_rules.json](scoring_rules.json) | `9570880dcea966cef13408f20a4531e87806bfbb75f8af1e97d0fed90bcd8796` | latest_review_evidence |
| N0168 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0169 | [docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json) | `3045e1e783ab41ea75b761599ea05ea0e0df1f8a9a6c1d65c3ca10bdd6daea91` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_e2d9397dff2a3f0f/agent_input/task.md](../agent_input/task.md) | `af9496c6c3c5b7f8ecf029675fa207e5becbed600528610947abf5d4548ecb3f` |
| [tasks/v2_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/reference_key_points.json](reference_key_points.json) | `9fdbe8be8895697ec055a4a556fe9594225bfc52c5b49051d659f43f124563f6` |
| [tasks/v2_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/reference_conclusions.json](reference_conclusions.json) | `34a5aff65d243d1fe5fe2cd0d0eb626347df720d02b67213a19f88551ceff8b7` |
| [tasks/v2_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/scoring_rules.json](scoring_rules.json) | `9570880dcea966cef13408f20a4531e87806bfbb75f8af1e97d0fed90bcd8796` |
| [tasks/v2_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/critical_failures.json](critical_failures.json) | `7e0a5b2ceb116e1a3dbc3347d1d0eb1bd0ca5e5c26be21a15bfc5b55479345cc` |
| [tasks/v2_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/evidence_map.json](evidence_map.json) | `dc976235d148a238850e20429ec7fec42bf241f2b3c69ea53fb75542c57e3f31` |
| [tasks/v2_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `db75dafa6fe9e70f0d6e1a65ad552e71a7b85a4d972eddbdbac6905440dd55c9` |

## Current scoring migration — 2026-10-19
Active paper_science_v2: 100 binary scientific-result points, intermediate findings plus final conclusions. Historical weights/freezes are superseded only as scoring policy. No process score or multiplier. No new chemical calculation or validation. Acceptance: USER_ACCEPTED_DEVIATION. Legacy user authorization accepts the roughly 0.65 kcal/mol bda direct-attack discrepancy; it remains unexplained and is not independent strict replication or a new universal tolerance. Opening and direct-attack saddles have mode/two-sided descent evidence, not full IRC. Finite electronic scans do not prove diffusion control, absolute rate or full-cycle rate-determining step. No exact SP-energy target or unknown source parameter is manufactured.


## 2026-10-19 — Round 3 scoring-contract repair (not a chemical acceptance update)

The original verification history above remains verbatim. Current scoring uses the physical object/state/reference definitions in scoring_rules.json; author software and previous user acceptance are evaluator provenance, not facts a new agent must report. Numeric targets, tolerances, recorded residuals, reference acceptance status and scientific scope are unchanged. PR still addresses the disclosed baseline. Relevant final-claim evidence is assessed directly rather than requiring every intermediate numeric window or an unrelated branch to pass.
