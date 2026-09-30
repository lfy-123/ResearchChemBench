# paper_c28b0a1c549f4575 特定V2方案

计划形成：2026-09-28T16:59:14.991904+00:00；先于本篇包复制/编辑。

## 来源与范围

The source investigates TEA-BF4/PC with addition of DEDABCO-(BF4)2 and links concentration-dependent spectral behavior to molecular association. This task bounds the investigation to local ion/solvent association.

- `papers/paper_c28b0a1c549f4575/documents/main.pdf` SHA256 `4e3ad96c28503f3a100df2083569811eef0ee848ae6aca2def236523628f8909`：Main pp1–3 identities/formulation and complete Fig2 discussion p3; SI pp5–6 computational protocols and separate MD specification.
- `papers/paper_c28b0a1c549f4575/documents/supplementary_001.pdf` SHA256 `51551c36ef22b1633c2ee346411edf4c5b5f3ec9edd9ea1ce7e923c011387546`：Main pp1–3 identities/formulation and complete Fig2 discussion p3; SI pp5–6 computational protocols and separate MD specification.

Components are tetraethylammonium TEA+, C8H20N+; 1,4-diethyl-1,4-diazabicyclo[2.2.2]octane dication DED2+, C10H22N2(2+); BF4−; and propylene carbonate PC, C4H6O3. All supplied starting species are closed-shell singlets. The source uses PC with 1 M TEA-BF4 and DEDABCO-(BF4)2 additions up to0.3 M; DED requires two BF4 per neutral salt unit. Source NMR/Raman observations vary with composition. Investigate local molecular association, with independently chosen composition and configurations of any model. The source does not establish a single PC stereoisomer; disclose any stereochemical choice.

## 旧任务诊断

固定PC数目、exchange_1/2与ion-pair控制把有限模型路线封闭；原文电极界面/浓度效应不可由单簇替代。

旧schema面板：{"equal_composition_clusters": ["TEA_PC1_contact", "TEA_PC1_separated", "TEA_PC2_contact", "TEA_PC2_separated", "DED_PC1_contact", "DED_PC1_separated", "DED_PC2_contact", "DED_PC2_separated"], "PC_exchange": ["first_PC", "second_PC"], "ion_pair_control": ["TEA_contact_effect", "DED_contact_effect", "conformer_sensitivity"]}。同一矩阵存在于私有规则，需联动移除。

## 新AR问题

What molecular account of propylene-carbonate association with the TEA/DED/BF4 components is supported in the stated mixed-electrolyte context? Determine whether and under which model assumptions the change of cation composition can alter the local PC environment, and what cannot be inferred from that evidence.

## 自主决定权

- Choose molecular models and references adequate to investigate how the actual ions affect PC association.
- Decide which quantities and comparisons can distinguish explanations and which composition/structure uncertainty matters.
- Assess whether the local evidence supports a general account or only a conditional result; distinguish molecular association from bulk concentration behavior.

## 公开输入处理

- Retain complete TEA, DED, BF4 and PC identities, neutral-salt stoichiometry and source formulation context.
- Remove obligatory0/1/2-PC salt clusters, fixed exchange_1/exchange_2 and contact/separated-ion controls; conservation remains a claim-dependent physical requirement.
- Keep source concentration-dependent observations without exposing the author preferential-binding explanation or adsorption winners.

## 提交与科学评价

- Verify recoverable association-related quantities against actual ion/PC identities, charges, model composition and balanced energetic references. Check observable and medium definitions rather than comparing unequal total energies.
- Assess whether the chosen study supports a molecular account of PC-environment changes and states its limits. Do not require fixed PC counts, the author DED affinity ranking or source bulk optimum; credit conditional, alternative and evidence-supported unresolved accounts.

Support each association inference with a chemically matched reference and appropriate structure/state/numerical evidence. Distinguish electronic interaction, thermodynamics and bulk speciation; justify the model and any comparison to concentration-dependent spectroscopy. If results depend on composition, solvent treatment or configurations, bound the conclusion accordingly rather than prespecifying one grid.

## PR作者路线及新增工作区分

The authors propose that DED2+ binds PC more strongly and changes TEA+ solvation, with concentration-dependent behavior and an optimum near0.2 M addition in the broader experiments. This interpretation must be tested within the bounded molecular question. SI pp5–6 reports Gaussian16 B3LYP-D3BJ/def2-SVP optimization and frequencies, B3LYP/6-311+G(2d,p) ion/solvent binding energies, separate B3LYP-D3BJ/def2-TZVP electrode adsorption, and B3LYP/6-311G** optimized frontier levels. These are distinct protocols; do not silently mix their reference energies. Separate GROMACS/GAFF/RESP bulk simulations are outside the required molecular baseline. The SI time-step text says2 nm, a dimensional error, not a validated simulation parameter. Old fixed PC-loading and exchange panels were builder additions. Reproduce or justify substitutions for the relevant molecular baseline, leaving new validation choices explicit.

## 旧证据复用与限制

group_6 既有TEA接触先导/恢复输出保留；DED、配位数和方法参考未齐。

精确已有产物、SHA256、V1绑定、在途尝试与科学缺口见同名JSON；未把排队输入当已完成结果。

## 检查与限制

- Official schema/package/hash/runtime/materialization tests; AR/PR shared science and actual different process rubrics.
- Accept free model/hypothesis counts, evidence-supported alternatives and bounded unresolved outcomes; reject empty or legacy-scalar complete reports.
- Check supplied molecular formulas, graphs and observation provenance; test paper-specific invalid inferences in the scoring casebook.

- Expanded reference coverage and actual semantic-judge calibration remain pending; existing evidence has only its documented scope.
- Physical public export is checked; isolated execution and evaluator-controlled chronology remain pending.
