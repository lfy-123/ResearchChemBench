# paper_9455a82229de2427 特定V2方案

计划形成：2026-09-28T16:37:30.735311+00:00；先于本篇包复制/编辑。

## 来源与范围

The source studies which SiNC5H7 products and formation mechanisms are consistent with crossed-beam SiN + isoprene scattering. The task retains that gas-phase reaction and its energetic experimental constraints.

- `papers/paper_9455a82229de2427/documents/main.pdf` SHA256 `cb6a4cf501837f252e2ceced551eefe8bcab8ca315fc4577e9daeb0d334476a1`：Main pp3–6 methods, reaction(1), Figs3–5; SI pp2–3 TableS1 and distinct energy definitions.
- `papers/paper_9455a82229de2427/documents/supplementary_001.pdf` SHA256 `27409af9dd2e70aae498d28aec9956049b2fc88bfcd5fa7439d57583ab67edbb`：Main pp3–6 methods, reaction(1), Figs3–5; SI pp2–3 TableS1 and distinct energy definitions.

Starting identities are SiN (neutral doublet), isoprene C5H8 (neutral singlet) and atomic H (neutral doublet). The observed heavy-product composition is SiNC5H7; its connectivity and electronic-state assignment are to be investigated. The total neutral reactant system has doublet spin. Conditions are isolated gas-phase single collisions at 25 ± 1 kJ/mol, not thermal solution equilibrium. The measured channel reaction energy is -162 ± 27 kJ/mol relative to separated reactants. Preserve all atoms and physical spin bookkeeping for models derived from these reactants.

## 旧任务诊断

candidate_space/connected_routes/accessibility 的预设行仍限定候选数量和主/竞争路线；作者全部产物标签或终态坐标不可作为 AR 搜索答案。

旧schema面板：{"candidate_space": ["terminal_C1_Si", "terminal_C4_Si", "terminal_C1_N", "terminal_C4_N"], "connected_routes": ["main_route", "competitor_route"], "accessibility": ["thermodynamic_vs_kinetic", "method_sensitivity"]}。同一矩阵存在于私有规则，需联动移除。

## 新AR问题

Which product structures and formation account are supported for the atomic-hydrogen-loss channel of SiN reacting with isoprene under the supplied single-collision conditions? Establish what is identifiable from a defensible molecular investigation and what alternatives remain unresolved.

## 自主决定权

- Select physically admissible product candidates and how to discover or eliminate them.
- Choose how to investigate formation and distinguish compatible endpoints from accessible chemistry within the measured energy window.
- Choose state/method treatment, search stopping criteria and the strength of the final identification.

## 公开输入处理

- Retain reactant/H identities and measured collision/channel energies; remove prescribed terminal-C1/C4 and Si/N attack families.
- Withhold source P1/P2 coordinates, product names, all38 candidate answers and source PES paths from AR.
- Remove mandatory main/competitor path count and fixed sensitivity panel from public and private rules; retain claim-dependent energetic and connectivity validity.

## 提交与科学评价

- Recover product/reaction quantities from genuine calculations with atom, charge, spin, energy reference and experimental uncertainty aligned. A lowest endpoint energy alone is insufficient for the formation part of the question.
- Assess whether discovered structures and a tested formation account explain the measured channel within the explored scope. Credit justified alternatives and remaining ambiguity; do not demand P1/P2, four attacks, two connected routes or a prescribed search.

Match energetic quantities to the single-collision observation and disclose ZPE, thermal and electronic-state conventions. A claimed reaction sequence needs actual evidence connecting its structures; a saddle-point or barrierless claim needs appropriate physical validation. Bound conclusions by the explored candidates, inaccessible channels and numerical uncertainty, choosing a defensible validation method.

## PR作者路线及新增工作区分

The authors use Gaussian16 C.01 CBS-QB3, B3LYP/CBSB7 optimized structures/frequencies, E0 = electronic energy + ZPVE and IRC checks of saddle connections. They considered38 product isomers and favor six-membered P1/P2 methylazasilacyclohexadienylidene products with adjacent Si/N, reached through N-terminal addition, rearrangement/cyclization and H elimination (main Figs4–5). Their measured channel energy is labeled ΔrG in the scattering discussion, but its derivation is translational-energy conservation; do not silently interpret it as a298 K solution Gibbs free energy. SI lists distinct CBS-QB3(0 K), Energy, Enthalpy and Free Energy fields. Reproduce the disclosed baseline or explain substitutions and source limits. The old four-attack/two-route benchmark was an added research design, not a required author protocol.

## 旧证据复用与限制

冻结记录有四个 CBS 端点及在途 i2；TS/IRC 或无垒连续路径未齐备，不新增提交。

精确已有产物、SHA256、V1绑定、在途尝试与科学缺口见同名JSON；未把排队输入当已完成结果。

## 检查与限制

- Official schema/package/hash/runtime/materialization tests; AR/PR shared science and actual different process rubrics.
- Accept free model/hypothesis counts, evidence-supported alternatives and bounded unresolved outcomes; reject empty or legacy-scalar complete reports.
- Check supplied molecular formulas, graphs and observation provenance; test paper-specific invalid inferences in the scoring casebook.

- Expanded reference coverage and actual semantic-judge calibration remain pending; existing evidence has only its documented scope.
- Physical public export is checked; isolated execution and evaluator-controlled chronology remain pending.

## Implementation binding

Source facts and material identities are public; author interpretation is confined to PR and private records. All previous public controls, fixed matrices and scientific rules are retired in .snapshot. New evaluator scores actual question coverage and claim-dependent validity.
