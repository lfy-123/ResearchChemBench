# Current scope and scoring — 2026-11-03

Why do the two successive Mallory photocyclizations of precursor 1-cis lead to the supplied product 2, and what thermodynamic and site-specific electronic factors distinguish plausible alternative closure sites? This is an explanation task using an isolated-molecule model; the observed product connectivity is supplied.

Product 2 connectivity is supplied public input. Score only computed competing-site energetics, independent site explanations and the balanced sequence; never award product-identification points.

Only the following independently supported outcomes receive points:

- first_stage: First-cyclization regioisomer thermodynamic preference (25 points).
- first_site_electronic: Electronic origin of first-site discrimination (15 points).
- second_stage: Second-cyclization regioisomer thermodynamic preference (25 points).
- second_site_electronic: Electronic origin of second-site discrimination (15 points).
- sequential_chemistry: Chemical rationale for the sequential oxidative cyclization route (20 points).

Original evidence and historical qualification are retained below. They do not impose deleted work or automatically certify the revised task. No new quantum jobs or blind-agent runs were performed.

<details>
<summary>Historical paper route before this revision (not active requirements)</summary>

# Active scoring revision — 2026-10-29

Only independently weighted final scientific conclusions in scoring_rules.json are active (100 total; semantic pass/fail only). No numeric target/tolerance, author-node completion or process gate is active. Historical route descriptions and older scoring allocations below are source context only. Original scientific scope, real computational-evidence requirements and historical scientific acceptance are unchanged.

# Private paper route

## 1. Scientific objective and author claim

Explain the complete regioselectivity of the bis-Mallory photocyclization of precursor 1-cis to dibenzo[a,o]picene (2). The authors claim that the experimentally observed exclusive channel is rationalized by a combination of relative Gibbs energies and frontier-orbital localization/phase at the reactive sites.

## 2. System and model boundary

The computational system is neutral singlet C30H22 precursor 1-cis and the neutral singlet cyclization/oxidation intermediates leading to neutral singlet C30H18 product 2. Solvent, explicit iodine and propylene oxide are not included in the reported quantum-chemical model. The SI supplies optimized Cartesian geometries for compound 1-cis, IS1–IS7 and 2.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize structures | compound 1, 2 and IS1–IS7 geometries | Gaussian 16 DFT | B3LYP/6-31G(d,p), Grimme D3 dispersion | optimized geometries | ev_doc_965c59b084a2_000079_ab2fb2e78776 |
| 2 | Verify stationary-point nature | optimized geometries | Gaussian 16 harmonic frequencies | same level as optimization; no imaginary frequencies for minima | frequencies and thermochemistry | ev_doc_965c59b084a2_000079_ab2fb2e78776 |
| 3 | Refine electronic energies | optimized geometries | Gaussian 16 single point | ωB97X-D/def2-TZVP | single-point energies | ev_doc_965c59b084a2_000079_ab2fb2e78776 |
| 4 | Compare channels | thermochemistry plus refined energies | thermochemical analysis | Gibbs free-energy profiles for all mapped intermediates | relative ΔG values and pathway ordering | ev_doc_965c59b084a2_000060_34f22ca8a885; ev_doc_965c59b084a2_000095_d92bdfc5a932 |
| 5 | Explain site selectivity | 1-cis and IS3 orbitals | Multiwfn 3.8 and VMD 1.9.4 | LUMO density and phase at reactive sites | qualitative orbital rationale | ev_doc_5a2534d03b71_000060_34f22ca8a885 |

## 4. Validation and analysis protocol

All optimized minima were checked for absence of imaginary frequencies. The first competing intermediates IS1 and IS2 were compared thermodynamically; the second-stage alternatives IS4 and IS5 were likewise compared, while IS6 and IS7 represent higher-energy bis-dihydrophenanthrene alternatives. The reported pathway interpretation combines those energy comparisons with LUMO density/phase observations at the relevant reactive sites and the experimental observation of exclusive product formation.

## 5. Private reference results

The paper reports IS1 as 9.9 kcal/mol more favorable than IS2 and IS4 as 11.3 kcal/mol preferred over IS5. The authors state that the first-stage preference is associated with pronounced LUMO density and phase inversion at C1 rather than C2, and the second-stage preference with higher LUMO density and phase inversion at C3. Oxidation of IS1 gives IS3, later oxidation of IS4 gives 2, and the reaction affords 2 exclusively. These values and interpretations are private evaluator references.

## 6. Limitations and interpretation boundaries

The reported thermodynamic profile is not a direct photochemical excited-state reaction-path calculation and does not establish kinetics, solvent effects, or quantum yields. A reproduction may use a different defensible model and must report method, conformer treatment, charge/multiplicity and uncertainty. Agreement with the reported ordering should not be interpreted as proof that the selected electronic-structure model is uniquely correct.

## Active V3 interpretation

The six rules score independent final answers: two regioisomer energetic preferences (20+20), two electronic site explanations (15+15), sequential oxidation/cyclization chemistry (15), and final product connectivity (15). No credit is awarded for completing a named intermediate or a job. Source IS labels identify reference structures only. Native differences are 9.660087921 and 11.003730032 kcal/mol, versus source 9.9 and 11.3; no hard windows exist. Native GD3BJ damping is more specific than the SI D3 description. Local density ratios 3.345549/2.688558 support site asymmetry; the first two sampled phase signs are the same, so the full source phase-inversion drawing is not independently established by these two samples. Native product minimum exists, superseding the early audit missing-product note. No exclusive photochemical kinetics, balanced oxidation free energy, or blind public-starter replay is certified.

## Confirmed scope clarification — 2026-10-27

The sequential-chemistry criterion retains the bounded endpoint/site rationale. Mapped hydrogen-accounted structures and appropriate same-composition comparisons do not impose a new balanced oxidation-energy calculation, explicit iodine model or barrier search. Evidence requirements track the actual claims: quantitative oxidation energetics need balanced references, and kinetic ordering needs appropriate pathway or kinetic evidence. Omitting an unclaimed oxidation free energy is not itself failure or a review trigger.

</details>
