# paper_b1467cd61ca8022d 特定V2方案

计划形成：2026-09-28T16:59:11.272518+00:00；先于本篇包复制/编辑。

## 来源与范围

The source compares PM, BM, TFPM and TFBM in LiFSI electrolytes and proposes a molecular solvation rationale. The task selects their local molecular interactions, not full electrolyte transport, interphase formation or battery performance.

- `papers/paper_b1467cd61ca8022d/documents/main.pdf` SHA256 `5d8206d63bf9546ab21cd825a8b6401671658eb2b405a2a6f4d2512b9079a058`：Main p3 chemical identities, Fig2 discussion and distinction between molecular/MD results; main p12 complete theoretical methods; formal publisher SI pp2–8, especially p7 FigS7.
- `tasks/upgrade_tasks/coordination_20260927/batch3/evidence/paper_b1467cd61ca8022d_official_si.pdf` SHA256 `990e77372a82e68e2f69c340c32bad64e4f83a0d2065a48f55751e312ea3b155`：Main p3 chemical identities, Fig2 discussion and distinction between molecular/MD results; main p12 complete theoretical methods; formal publisher SI pp2–8, especially p7 FigS7.

The supplied graphs define PM C4H10O, BM C5H12O, TFPM C4H7F3O and TFBM C5H9F3O, Li+ and FSI−. The neutral solvents and closed-shell ions are singlet starting species. Source electrolyte formulations use 2 M LiFSI in each of the four ethers. Investigate molecular/local solvation within these components; distinguish a finite molecular model from the 2 M bulk liquid. Cluster composition, configurations, medium treatment and informative quantities are research decisions. There is no prescribed Li:FSI:solvent cluster ratio.

## 旧任务诊断

题面先给O/F chelation、anion competition解释并强制1:1:1和固定片段/描述符程序；有限模型与体相作用边界要重审。

旧schema面板：{"cluster_orientations": ["PM_solvent_contact", "PM_anion_contact", "BM_solvent_contact", "BM_anion_contact", "TFPM_solvent_contact", "TFPM_anion_contact", "TFBM_solvent_contact", "TFBM_anion_contact"], "fragment_controls": ["PM", "BM", "TFPM", "TFBM"], "descriptor_test": ["O_F_contrast", "anion_competition", "method_sensitivity"]}。同一矩阵存在于私有规则，需联动移除。

## 新AR问题

How do the molecular identities of PM, BM, TFPM and TFBM affect local lithium solvation in the presence of FSI, and what account of their differences is supported by a defensible molecular investigation? Determine the extent to which the evidence supports a common explanation across these four solvents.

## 自主决定权

- Choose a local molecular representation that can address the four-solvent comparison and justify its relation to the stated electrolyte context.
- Select hypotheses, configurations, electronic methods and informative observables or comparisons without a supplied chelation mechanism.
- Determine which structural and numerical uncertainties limit cross-solvent conclusions and whether a single rationale survives.

## 公开输入处理

- Keep six molecular component graphs and the four 2 M formulations; remove obligatory 1:1:1 salt clusters.
- Remove O-only versus O/F chelation labels, TFPM winner/optimal descriptor windows and prescribed isolated/cluster descriptor matrix from all AR inputs and private requirements.
- Distinguish true formal publisher SI from the local peer-review PDF; keep computed author structures/results private.

## 提交与科学评价

- Check quantitative local-solvation comparisons with consistent component/state definitions, atom mapping, energy or observable conventions and actual outputs. Absolute energies of different solvent formulas are not comparative binding evidence.
- Judge whether the agent-selected evidence supports a local molecular explanation across the four stated identities and appropriately bounds model dependence. Credit alternative or unresolved accounts; do not require six-membered chelation, an oxygen/fluorine decomposition, fixed clusters or a TFPM winner.

Define the observable, molecular composition and reference of every comparison. Show adequate validity for any claimed structure or relative interaction, and justify transfer from selected models to the stated local question. If electrostatic or charge descriptors are used, distinguish potential units/locations from fitted atomic charges and document the calculation; an ESP extremum is not automatically a RESP charge.

## PR作者路线及新增工作区分

The authors propose dual RESPO/dipole descriptors and synergistic O/F lithium coordination, favoring a six-membered TFPM chelate. Source calculations use Gaussian16 B3LYP/6-311+G(d,p), geometry/frequency checks, and Eb=Ecomplex−ELi+−Esolvent; Multiwfn3.8 is named for RESP. The source RESPO axis is labeled eV, whereas RESP atomic charges are in e; reproduce the actual defined quantity or explicitly flag this ambiguity instead of treating them as interchangeable. Their separate GROMACS2018 OPLS-AA bulk simulations use30 LiFSI with145 PM/125 BM/129 TFPM/110 TFBM,8 ns NVT and40 ns NPT with final30 ns analysis. The molecular task does not require that MD protocol or the builder’s former1:1:1 FSI cluster grid. Reproduce the relevant disclosed molecular baseline or justify substitutions; any new local model is an additional investigation. Published computed chelation and populations are author interpretations/results, not required answers.

## 旧证据复用与限制

group_6 冻结的LiFSI参考及部分PM/TFPM结果保留；BM/TFBM及配对方法/构象不确定性不足。

精确已有产物、SHA256、V1绑定、在途尝试与科学缺口见同名JSON；未把排队输入当已完成结果。

## 检查与限制

- Official schema/package/hash/runtime/materialization tests; AR/PR shared science and actual different process rubrics.
- Accept free model/hypothesis counts, evidence-supported alternatives and bounded unresolved outcomes; reject empty or legacy-scalar complete reports.
- Check supplied molecular formulas, graphs and observation provenance; test paper-specific invalid inferences in the scoring casebook.

- Expanded reference coverage and actual semantic-judge calibration remain pending; existing evidence has only its documented scope.
- Physical public export is checked; isolated execution and evaluator-controlled chronology remain pending.
