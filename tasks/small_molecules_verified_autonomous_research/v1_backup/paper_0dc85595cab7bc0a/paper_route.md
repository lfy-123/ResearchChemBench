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
