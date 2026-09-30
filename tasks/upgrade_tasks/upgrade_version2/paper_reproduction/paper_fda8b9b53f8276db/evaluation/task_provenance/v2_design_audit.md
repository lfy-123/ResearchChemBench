# paper_fda8b9b53f8276db 特定V2方案

计划形成：2026-09-28T16:44:02.535652+00:00；先于本篇包复制/编辑。

## 来源与范围

The source compares a free quinoxaline ligand molecular calculation with its crystal geometry. The bounded task concerns ligand1, not its Re complex, biological activity or crystal-lattice thermodynamics.

- `papers/paper_fda8b9b53f8276db/documents/main.pdf` SHA256 `0afa69242ab928c082802d029d66eaa4c3c58cea7f791438d64de1c7f88de8d1`：Main p4 §2.4; SI pp10–11 TableS2 and pp11–15 molecular coordinates/frequency/structure figures; authentic CCDC record and atom-label mapping.
- `papers/paper_fda8b9b53f8276db/documents/supplementary_001.pdf` SHA256 `13ace6b2daec90e737a69c21f21a4af2d7cab7a54b967859e270ca1147c496de`：Main p4 §2.4; SI pp10–11 TableS2 and pp11–15 molecular coordinates/frequency/structure figures; authentic CCDC record and atom-label mapping.

Ligand1 is C15H13N3, neutral singlet. The public CCDC2433822 CIF is an experimentally measured crystal structure, with matching atom labels and six reported intramolecular bond measurements. Investigate this same free-ligand chemistry with finite molecular models and explicitly distinguish crystal observations from the environment represented by a calculation. The geometry of a freely optimized molecule is a research result; the crystal is an authorized observation, not a blind target.

## 旧任务诊断

gas/MeCN 的固定 2×2 构象矩阵与 torsional_intervention 不能继续作为唯一研究路线；公开晶体输入不属于盲预测。

旧schema面板：{"conformer_environment": ["cis_gas", "trans_gas", "cis_MeCN", "trans_MeCN"], "six_bond_residuals": ["cis_gas", "trans_gas", "cis_MeCN", "trans_MeCN"], "torsional_intervention": ["gas_fixed_vs_relaxed", "MeCN_fixed_vs_relaxed"]}。同一矩阵存在于私有规则，需联动移除。

## 新AR问题

What molecular description of the free quinoxaline ligand is supported by the supplied crystal structure and an independent molecular investigation, and how should agreement or disagreement with the crystal geometry be interpreted? Establish which structural conclusions are reliable and which remain model dependent.

## 自主决定权

- Choose structural models and which geometric features inform the molecular description.
- Design an investigation to interpret differences from the measured crystal without a supplied torsional explanation.
- Choose uncertainty treatment and decide the extent of structural identification supported by the evidence.

## 公开输入处理

- Keep authentic experimental CIF and six measured bond lengths with their reported0.001angstrom ESDs, separate from rounding.
- Remove computed cis/trans coordinates, source RMSE target and inferred globally lowest assignment from AR.
- Remove mandated gas/MeCN2x2 grid, torsion scan and fixed six-bond scalar completion rubric; retain explicit mapping and measurement uncertainty.

## 提交与科学评价

- Check structural quantities extracted from genuine models against correctly mapped measured coordinates/bonds, including metric definitions, original precision and crystallographic uncertainty. The reported ESD is not a universal electronic-structure tolerance.
- Judge the evidence supporting the proposed molecular structure and interpretation of crystal/model differences. No prescribed cis winner, solvent contrast or torsional scan is mandatory; alternative structures and evidence-supported unresolved phase attribution are eligible.

Verify any claimed optimized state or structural minimum and define the molecular/experimental environments compared. If reporting residuals, state the included atoms/bonds and statistic; separate marginal crystallographic ESDs, absent covariance, rounding and model error. A local minimum is not a certified global minimum, and bond agreement alone cannot explain a phase-dependent conformation.

## PR作者路线及新增工作区分

The authors use crystal-derived initial coordinates and B3LYP/6-311+G(2d,p) for free ligand1, with vibrational validation; their source Gaussian03 molecular calculation gives a cis pyridyl orientation while the experimental crystal is trans (main p4, SI TablesS2–S3/FigsS10–S11). They attribute the difference to gas versus packed solid conditions and report small selected bond residuals. Those are a local computed structure and an interpretation, not proof of exhaustive conformational or lattice thermodynamics. Reproduce that disclosed molecular baseline or explain substitutions. The previous mandatory MeCN and torsional controls were builder additions and are no longer required.

## 旧证据复用与限制

group_3 已有有限十行原生参考并修复 ESD；新 C 任务的 evaluator 校准和独立运行仍须另报。

精确已有产物、SHA256、V1绑定、在途尝试与科学缺口见同名JSON；未把排队输入当已完成结果。

## 检查与限制

- Official schema/package/hash/runtime/materialization tests; AR/PR shared science and actual different process rubrics.
- Accept free model/hypothesis counts, evidence-supported alternatives and bounded unresolved outcomes; reject empty or legacy-scalar complete reports.
- Check supplied molecular formulas, graphs and observation provenance; test paper-specific invalid inferences in the scoring casebook.

- Expanded reference coverage and actual semantic-judge calibration remain pending; existing evidence has only its documented scope.
- Physical public export is checked; isolated execution and evaluator-controlled chronology remain pending.

## Implementation binding

Source facts and material identities are public; author interpretation is confined to PR and private records. All previous public controls, fixed matrices and scientific rules are retired in .snapshot. New evaluator scores actual question coverage and claim-dependent validity.
