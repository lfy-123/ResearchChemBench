# Round-one scope notice — 2026-11-03

The existing scientific scope is retained. Existing calculations below are historical evidence and apply only to matching current conclusions. Removed tasks are not required. No new QM or blind-agent validation was performed. Current scoring: `scoring_rules.json`; scope/provenance: `round1_review.json`.

---

## 2026-10-27 Confirmed repair: model-specific explanatory reach

The current yield criterion assesses the demonstrated reach of the submitted computed molecular model. The nonmonotonic yield relationship recorded below belongs to the source triplet-energy comparison; it does not exclude a different independently computed, physically established explanation. Fitting the supplied yields alone is insufficient. No new quantum calculations were performed. All earlier text below is retained verbatim as dated evidence and scope history; current scoring_rules.json governs.

## 2026-10-27 V3 final-result migration

Six final conclusions explain each named photocatalyst and the independent nonmonotonic yield relationship; substrate S0/T1 energies are shared supporting evidence, not a separate stage score. No new quantum-chemistry or HPC jobs were run. Existing native results are reused only for the matching final claims listed in evidence_map.json; historical PASS labels are not transferred. Only substrate S0/T1 were calculated locally; catalyst triplet energies are source properties. Gap61.465356 versus source62.0 kcal/mol; absolute-state offsets around−11kcal/mol and MeCN/THF/irradiation differences remain. No complete photocycle is verified. The dated record below is retained verbatim.

## 2026-10-23 科学分V2维护副本

当前私有评分为`paper_science_v2`，共8个二元科学项，中间关键节点60分、最终结论40分，总计100分。全部过程分已删除。新规则不设数值硬窗口，不改变既有定性验收或数值差异记录。公开输入保持原样，题面中旧过程分/60+40措辞不代表本维护副本实际计分，作为专家待审文字遗留披露。科学评分资格与发布资格分开，见`reference_qualification.json`。

## 2026-10-23 当前科学问题验证过程与结果汇总

当前AR状态：`PROVISIONAL_PASS_QUALITATIVE`；这是已完成独立审查后的定性验收，不是尚未验收的候选。严格整题数值复现未登记，数值偏差和实现差异保留供专家判断。本节整合既有实际计算，没有新增量化计算。

### 方法、模型与执行过程

PBE0/6-311G(d)、IEFPCM-MeCN优化/频率；PBE0/def2-TZVP、SMD-MeCN同几何单点；298 K、1 atm RRHO。实际Gaussian16 C.01，作者明确层级一致；S0流程及坐标重建，未公开热化学约定不能声称完全恢复。

1. 从完整C19H13NOS底物构建S0中性单重态和T1中性三重态；每态35原子，分别执行优化、频率和高层单点。
2. 两态均优化完成，各99个正频率；频率与单点坐标一致，T1湮灭后S²约2.0014。S0后续Hessian位移重估例外保留，不能伪称每一诊断均通过。
3. 以每态自身单点电子能加热G修正形成G，再取T1−S0；结合来源五催化剂能量与实验条件进行有限比较。催化剂能量是来源上下文，不冒称本次独立计算。

### 论文与计算数值对照

|物理量与参照|论文值|计算值|计算−论文|单位|
|---|---|---|---|---|
|G(S0)|−1258.961473|−1258.97862038|−0.01714738（−10.760143 kcal/mol）|Eh|
|G(T1)|−1258.862640|−1258.88066910|−0.01802910（−11.313431 kcal/mol）|Eh|
|G(T1)−G(S0)|62.0|61.465356|−0.534644|kcal/mol|

### 定性结论与保留项

底物激发代价与三个有效催化剂及两个痕量催化剂的能量可及性分组相容。标准Ir接近共振，来源−0.2与自算+0.334644的小差值符号不同；不建立普适硬阈值。能量高低不构成产率大小的单调定量预测。

- 两态绝对自由能约−11 kcal/mol的偏移来源尚未解释；差分相消不是偏移成因的解释。
- 溶剂Hessian配理想气体RRHO是已披露的来源解释；作者是否另做气相Hessian无法确认。
- 计算连续介质为作者使用的MeCN，实验为THF；thioxanthone光照及负载条件也不同。
- 只支持有限分子能量关联，不证明排他性EnT因果、完整氮烯/HAA/rebound网络、精确速率或产率。

### 原生结果、独立复核及来源

- [acceptance_audit.md](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_87f5/acceptance_audit.md)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [acceptance_audit.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_87f5/acceptance_audit.json)：独立核对的原始输入、日志、数值、结构/态/频率及哈希入口。
- [main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_87f5566528287b60/documents/main.pdf)：PDF页序（1-based）5,6。
- [supplementary_001.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_87f5566528287b60/documents/supplementary_001.pdf)：PDF页序（1-based）31,32,33。

来源方法未报告项、数值差异与题外未计算项目不能混为同一类问题。下方原有记录按日期保留，旧candidate/pending仅表示当时状态，不覆盖本节引用的最新父级验收。

---

## 历史验证记录（原文保留）

<!-- parent-acceptance-20261022T1743Z -->
## Parent acceptance — 2026-10-22 17:43 UTC follow-up

Current mode status: `PROVISIONAL_PASS_QUALITATIVE`. Independent source/native-log review supports all required qualitative conclusions of this current scientific question under the disclosed author model. This is provisional qualitative verification, not strict numerical replication or a change to scoring/release. The earlier candidate statements below are historical and are superseded only within the scope recorded here.

Parent decision: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/parent_acceptance_decision.json`. Independent audit: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T1743Z/acceptance_audit_87f5/acceptance_audit.json`.

Paired gap: computed 61.465356 versus reported 62.0 kcal/mol; computed minus reported −0.534644 kcal/mol. Absolute S0/T1 free-energy offsets are −10.760143/−11.313431 kcal/mol and remain unexplained; paired cancellation does not explain the underlying offsets. Both states have converged Opt, 99 positive frequencies and same-geometry SP. The molecular energetic test supports the bounded five-catalyst association, not an exact activation threshold, quantitative yield or unique EnT mechanism.

Retained qualifications:

- Single-state absolute offsets remain unexplained; cancellation in the paired gap is not an explanation of their origin.
- S0 and source coordinates reconstructed, same-level singlet baseline justified but not recovered original inputs.
- Ideal-gas RRHO on solvent Hessian is a defensible disclosed source interpretation; exact unreported thermal protocol not established.
- S0 optimization converged and all frequencies positive; frequency-link displacement re-estimate retained as diagnostic uncertainty.
- Supports bounded energetic association across five catalyst conditions, not unique EnT causality, exact threshold, rates or yields. Standard Ir source gap is near-resonant and its small sign difference is explicitly retained.

<!-- end-parent-acceptance-20261022T1743Z -->

# Verified computation reference — 2026-10-22 short-job follow-up

Verification status: PROVISIONAL_PASS_QUALITATIVE. This records verifier evidence; scoring rules, tolerances and release status are unchanged.

S0/T1两态均完成优化、频率和单点；能隙61.465356kcal/mol，对作者62.0的有符号差−0.534644。五种催化剂有效/痕量分组均与能量可及性一致。候选仅针对当前有边界的C1解释；绝对态自由能偏移、MeCN/THF、光照/负载差异及重建假设完整披露，不宣称排他性EnT因果或定量产率。

Current C1 is supported in both modes as a bounded energetic association. PROVISIONAL_PASS_QUALITATIVE is a candidate, not strict numerical acceptance or a release action. Both absolute-state energy offsets and all method assumptions below require explicit expert review.

Evidence (native inputs/outputs, exit codes, geometry/mode checks and hashes are linked inside):

- `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_87f5566528287b60/short_job_followup_20261022T1645Z/paired_triplet_review.json`

Current task coverage: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_87f5566528287b60/short_job_followup_20261022T1645Z/coverage.json`. Author comparisons and method boundaries:

```json
{
  "paper_id": "paper_87f5566528287b60",
  "method": "Gaussian16; unrestricted triplet PBE0/6-311G(d),IEFPCM(MeCN) Opt/Freq; PBE0/def2-TZVP,SMD(MeCN) singlepoint; add RRHO thermal Gibbs contribution at298K. Reconstructed neutral singlet and neutral triplet of35atom sulfilimine.",
  "source_locations": [
    "SI PDFp32 (printedS31) methods; PDFp33(printedS32)TableS7",
    "main Scheme4E/current task conditions"
  ],
  "differences_and_qualification": [
    "S0 andT1 use the same exact sulfilimine molecular graph; no counterion or catalyst is incorrectly substituted for the substrate.",
    "Source gives G(T1)−G(S0)=62.0; catalyst energies are contextual reported values, not additional author-computed catalyst objectives.",
    "Singlet optimization details, author coordinates and raw jobs are not supplied; restricted same-level singlet reconstruction disclosed. Solvent-frequency versusgas-phase-correction wording remains an explicit convention ambiguity.",
    "Actual THF versuscomputedMeCN and thioxanthone370nm/10mol% versusblue470nm/1mol% prevent a causal threshold or quantitative yield proof."
  ],
  "comparisons": [
    {
      "quantity": "G(S0)",
      "author_value": -1258.961473,
      "calculated_value": -1258.97862038,
      "signed_error": -0.017147379999869372,
      "absolute_error": 0.017147379999869372,
      "signed_error_kcal_mol": -10.76014340419615,
      "unit": "hartree",
      "status": "VALID_NATIVE_CONDITIONAL_COMPOSITE"
    },
    {
      "quantity": "G(T1)",
      "author_value": -1258.86264,
      "calculated_value": -1258.8806691,
      "signed_error": -0.018029099999921527,
      "absolute_error": 0.018029099999921527,
      "signed_error_kcal_mol": -11.313431057644157,
      "unit": "hartree",
      "status": "VALID_NATIVE_CONDITIONAL_COMPOSITE"
    },
    {
      "quantity": "G(T1)-G(S0)",
      "author_value": 62.0,
      "calculated_value": 61.46535619040232,
      "signed_error": -0.5346438095976822,
      "absolute_error": 0.5346438095976822,
      "unit": "kcal/mol",
      "status": "QUALITATIVELY_SUPPORTED"
    }
  ],
  "execution_assumptions": [
    "Source explicitly specifies unrestricted triplet; singlet procedure reconstructed as restricted same-level optimization/frequency.",
    "Coordinates reconstructed; no author raw coordinates supplied.",
    "Source says gas-phase thermal correction but frequencies at solvated optimization level; using ideal-gas RRHO correction from stated IEFPCM Hessian, explicitly disclosed.",
    "298.0K used as printed;1atm Gaussian default. Acetonitrile model differs from actual THF reaction.",
    "Lowest triplet and exclusive energy-transfer causality require review; no complete nitrene reaction mechanism claimed."
  ],
  "at_utc": "2026-10-22T17:32:45.400348+00:00",
  "catalyst_comparison": [
    {
      "catalyst": "thioxanthone",
      "reported_triplet_energy_kcal_mol": 65.5,
      "observed_yield": "66%",
      "irradiation_loading": "370nm,10mol%",
      "donor_energy_minus_computed_substrate_gap_kcal_mol": 4.034643809597682,
      "qualitative_group_consistency": true
    },
    {
      "catalyst": "Ir(dFppy)3",
      "reported_triplet_energy_kcal_mol": 63.5,
      "observed_yield": "61%",
      "irradiation_loading": "470nm,1mol%",
      "donor_energy_minus_computed_substrate_gap_kcal_mol": 2.034643809597682,
      "qualitative_group_consistency": true
    },
    {
      "catalyst": "Ir[dF(CF3)ppy]2(dtbbpy)",
      "reported_triplet_energy_kcal_mol": 61.8,
      "observed_yield": "76%",
      "irradiation_loading": "470nm,1mol%",
      "donor_energy_minus_computed_substrate_gap_kcal_mol": 0.33464380959767936,
      "qualitative_group_consistency": true
    },
    {
      "catalyst": "fac-Ir(ppy)3",
      "reported_triplet_energy_kcal_mol": 58.1,
      "observed_yield": "trace",
      "irradiation_loading": "470nm,1mol%",
      "donor_energy_minus_computed_substrate_gap_kcal_mol": -3.3653561904023164,
      "qualitative_group_consistency": true
    },
    {
      "catalyst": "Mes-Acr",
      "reported_triplet_energy_kcal_mol": 44.7,
      "observed_yield": "trace",
      "irradiation_loading": "470nm,1mol%",
      "donor_energy_minus_computed_substrate_gap_kcal_mol": -16.765356190402315,
      "qualitative_group_consistency": true
    }
  ],
  "method_limits": [
    "Authors supply no raw coordinates and no explicit singlet procedure: source graph reconstructed and same-level restricted S0 used.",
    "Source gas-phase-thermal wording interpreted as ideal-gas RRHO term from the explicitly stated solvated frequency calculation; this is disclosed, not a hidden method change.",
    "Calculated solvent MeCN differs from experimental THF; thioxanthone irradiation/loading differs from other catalysts.",
    "T1 spin expectation2.0495 before annihilation and2.0014 after indicates small contamination; one converged triplet minimum does not prove exhaustive global state/conformer completeness.",
    "Absolute S0 and T1 free energies differ by about11kcal/mol from printed values; paired difference agrees qualitatively and within0.535kcal/mol.",
    "Catalyst energies are reported contextual values; they were not independently recalculated. No additional catalyst calculations are required by the source baseline for this question."
  ],
  "SMD_bookkeeping": "Native log includes SMD non-electrostatic term in the nuclear-repulsion contribution before final SCF; it is not added a second time."
}
```

Previous-round evidence is preserved under `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_87f5566528287b60/new44_20261022`.
