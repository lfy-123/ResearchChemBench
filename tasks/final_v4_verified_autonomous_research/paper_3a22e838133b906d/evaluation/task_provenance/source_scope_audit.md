# paper_3a22e838133b906d 特定V2方案

计划形成：2026-09-28T17:04:49.616923+00:00；先于本篇包复制/编辑。

## 来源与范围

The source prepares the full Cy/OEt phosphonate–borane2a and its dealkylated lithium salt and compares local B–O/P–O structure with small neutral/anion models. The selected task concerns what accounts for the local structural change.

- `papers/paper_3a22e838133b906d/documents/main.pdf` SHA256 `0b3a6429a4f8d324616b78c736daedf397971e63fdeff848f1b28058a39a1238`：Main pp2–3 Scheme1/Fig1 and Scheme2; SI pp62,69 crystallographic tables (previous source review) and p78 complete computational method re-read.
- `papers/paper_3a22e838133b906d/documents/supplementary_001.pdf` SHA256 `0179f85740483c73a9996ca3c5ef36fd4f0044eca862b18eadc90e03463a7235`：Main pp2–3 Scheme1/Fig1 and Scheme2; SI pp62,69 crystallographic tables (previous source review) and p78 complete computational method re-read.

The full source identities are neutral2a C22H36BO3P and its deethylated anion C20H31BO3P−, with Li+ and MeCN as salt components. Supplied starting species are closed-shell singlets. In the reported crystal [Li(MeCN)2][3] forms an inversion-related dimer with two bridging Li ions, each also associated with two MeCN molecules; this is an experimental crystal observation, not a mandatory computational model or a unique solution structure. Public local bond distances describe the actual crystals. You choose the molecular representation and evidence needed for the bounded local-structure question; no full dealkylation mechanism or complete association ladder is prescribed.

## 旧任务诊断

coordination_layers/balanced_cycles/truncation_and_mechanism预设整个层级分解；从源局部键长问题扩大到全部缔合不是天然核心。

旧schema面板：{"coordination_layers": ["full_anion", "Li_anion", "Li_anion_2MeCN", "crystal_supported_dimer"], "balanced_cycles": ["Li_association", "MeCN_association", "dimerization", "deethylation"], "truncation_and_mechanism": ["small_vs_full", "coordination_vs_aggregation"]}。同一矩阵存在于私有规则，需联动移除。

## 新AR问题

What molecular account of the local B/O/P structural differences between phosphonate–borane2a and its dealkylated lithium salt is supported by the crystallographic observations and a defensible model investigation? Determine what can be attributed within the studied models and where experimental environment or model representation limits the conclusion.

## 自主决定权

- Choose how to represent the local structure and experimental salt environment while retaining a defensible mapping to the full source molecules.
- Select informative comparisons and observables to assess proposed structural explanations and their uncertainty.
- Decide how much evidence is needed for transfer from a model to the crystal observations and where that transfer cannot be established.

## 公开输入处理

- Retain complete Cy/OEt component graphs and experimental local distances; omit the old mandatory small-model and preassembled Li/MeCN/dimer ladder from AR.
- Remove prescribed deethylation/dimerization cycles and truncation matrix; compositional conservation is still required for any energetic claim actually made.
- Expose crystal association only as an observed physical boundary; do not fabricate a missing CIF or claim an author dimer minimum. Source methyl models are described in PR, not imposed on AR.

## 提交与科学评价

- Check numerical local geometry and any additional electronic/energetic evidence against actual structures, chemically correct atom correspondence and full-versus-truncated identities. Experimental ESDs are measurement uncertainties, not a universal allowed deviation for gas-phase models.
- Judge whether the submitted study explains or appropriately bounds the observed local changes without requiring a specific decomposition or model ladder. A model can disagree with the source and receive credit when genuine evidence explains its applicability and limits.

Any attribution must be supported by evidence capable of separating the claimed effects, with explicitly defined model/environment and uncertainty. Verify structures to the extent claimed; thermodynamic/association claims require balanced reference states and conventions. An observed crystal dimer does not itself validate a finite optimized dimer or mandate its calculation for a narrower conclusion.

## PR作者路线及新增工作区分

Main Scheme1/Fig1 reports LiI dealkylation of2a under reflux, isolation of[Li(MeCN)2][3], and a crystal dimer with a Li2O2 core. The authors observe a shorter B···O contact and slightly longer associated P–O bond in the salt. Scheme2 and SI p78 use small models with R/R′=Me, Gaussian16 C.01 B3LYP-D3(BJ)/6-311++G(2d,p), optimization and no imaginary frequencies. They explicitly note that the anion calculation omits Li coordination and fits experimental P–O distances less well. Reproduce the disclosed model baseline with transparent truncation and justified substitutions; additional full-molecule, environment or association studies are new investigations. The previous benchmark’s full coordination ladder, balanced reaction cycle and mandatory dimerization panel were not performed as that complete protocol in the paper. No source CIF or effective dimer minimum has been manufactured for this package.

## 旧证据复用与限制

group_6完整anion及Li/MeCN基础输出、neutral在途结果保留；完整关联/二聚与守恒热力学还未完成。

精确已有产物、SHA256、V1绑定、在途尝试与科学缺口见同名JSON；未把排队输入当已完成结果。

## 检查与限制

- Official schema/package/hash/runtime/materialization tests; AR/PR shared science and actual different process rubrics.
- Accept free model/hypothesis counts, evidence-supported alternatives and bounded unresolved outcomes; reject empty or legacy-scalar complete reports.
- Check supplied molecular formulas, graphs and observation provenance; test paper-specific invalid inferences in the scoring casebook.

- Expanded reference coverage and actual semantic-judge calibration remain pending; existing evidence has only its documented scope.
- Physical public export is checked; isolated execution and evaluator-controlled chronology remain pending.
