# paper_9a58a1fa6ed7d780 特定V2方案

计划形成：2026-09-28T16:37:34.693916+00:00；先于本篇包复制/编辑。

## 来源与范围

The source compares internal BN incorporation in BN-AkFlu5a with the all-carbon CC-AkFlu5b. This bounded task addresses isolated-molecule low-energy electronic excitations rather than crystallographic assembly, photoluminescence kinetics or devices.

- `papers/paper_9a58a1fa6ed7d780/documents/main.pdf` SHA256 `aeebf1cd58e33932312c18720a87e7fddd1c12d72f39a5afb963baaa5ce4ca92`：Main pp2–4 molecular/optical discussion; SI pp3,39,41–43 methods and tables,49–51 coordinate identities.
- `papers/paper_9a58a1fa6ed7d780/documents/supplementary_001.pdf` SHA256 `dcd192b5e3b92b087855114bacea08f5316e4de2d8a105fa4af949b8459531fe`：Main pp2–4 molecular/optical discussion; SI pp3,39,41–43 methods and tables,49–51 coordinate identities.

The supplied complete graphs are BN-AkFlu5a, C22H14B2N2, and CC-AkFlu5b, C26H14, each a40-atom neutral singlet. Investigate the isolated molecules in gas phase, consistent with the source single-molecule calculations. Geometry and electronic excitations are not supplied as answers. This comparison is about these two actual chemical identities; changing a B/N nucleus into C is a change of molecule, not a geometric perturbation.

## 旧任务诊断

relaxed_states/common_scaffold/attribution 是预定解释程序；有限气相分子比较不能承接器件迁移率或固态发光结论。

旧schema面板：{"relaxed_states": ["BN_relaxed", "CC_relaxed"], "common_scaffold": ["BN_on_CC", "CC_on_BN"], "attribution": ["chemical_effect", "geometry_effect", "analysis_convergence"]}。同一矩阵存在于私有规则，需联动移除。

## 新AR问题

How does replacing the specified internal carbon sites by BN units affect the low-energy molecular electronic excitations of BN-AkFlu and CC-AkFlu, and what molecular explanation can be supported? Determine which differences are robust and which depend on the chosen model or state interpretation.

## 自主决定权

- Select electronic-state and structural models, spectral window and quantitative evidence adequate for this pair.
- Choose which explanations and comparisons can account for differences and test their limitations.
- Determine state correspondence and whether the evidence supports a distinct change or unresolved behavior.

## 公开输入处理

- Keep only atom-resolved BN/CC identities; remove optimized answer coordinates and predicted root/state descriptors.
- Remove compulsory frozen cross-scaffold geometry pairs, S1–S6 count and D/Sr attribution matrix from task/schema/evaluator.
- Keep physically defined state correspondence and descriptor normalization as requirements only when the submitted claim uses them.

## 提交与科学评价

- Check independently produced excitation properties and the numerical BN/CC comparison using actual mapped molecular states and raw outputs. Source S1/S4 labels or root indices cannot substitute for physical identification; quantities and analysis definitions must be consistent.
- Judge whether the molecular explanation is supported by the agent-selected evidence and relevant uncertainty. Do not require a cross-geometry decomposition, a particular Sr/D metric, a bright root number or the author conclusion.

Separate orbital gaps, vertical excitations and any other observable you calculate. Match physical states using adequate evidence whenever comparing states across molecules or methods; specify descriptor definitions and numerical convergence if such descriptors support the explanation. Test limitations important for the asserted BN effect without a prescribed control axis.

## PR作者路线及新增工作区分

The source uses Gaussian16 B3LYP/6-311G(d,p) for molecular geometries and electronic calculations and Multiwfn for hole–electron analysis (SI pp3,39). FigureS27 explicitly describes a single gas-phase molecule. TablesS11 and S14 give BN-AkFlu density descriptors and vertical transitions, while TableS15 gives CC-AkFlu transitions; TablesS21–S22 give geometries. The authors link BN insertion to altered frontier levels and excitation character. Main text describes a bright S4 for a broader BN-Flu discussion, while BN-AkFlu TableS14 places the large oscillator strength at S5; preserve molecule/root distinctions. The benchmark former mandatory cross-scaffold decomposition was not the original author route. Reproduction must disclose unresolved extraction/descriptor disagreement rather than force matching labels.

## 旧证据复用与限制

group_3 冻结记录为 finite scientifically_validated；保留实际输出和来源条件，V2 语义评分与盲测不继承通过。

精确已有产物、SHA256、V1绑定、在途尝试与科学缺口见同名JSON；未把排队输入当已完成结果。

## 检查与限制

- Official schema/package/hash/runtime/materialization tests; AR/PR shared science and actual different process rubrics.
- Accept free model/hypothesis counts, evidence-supported alternatives and bounded unresolved outcomes; reject empty or legacy-scalar complete reports.
- Check supplied molecular formulas, graphs and observation provenance; test paper-specific invalid inferences in the scoring casebook.

- Expanded reference coverage and actual semantic-judge calibration remain pending; existing evidence has only its documented scope.
- Physical public export is checked; isolated execution and evaluator-controlled chronology remain pending.

## Implementation binding

Source facts and material identities are public; author interpretation is confined to PR and private records. All previous public controls, fixed matrices and scientific rules are retired in .snapshot. New evaluator scores actual question coverage and claim-dependent validity.
