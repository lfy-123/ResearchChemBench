# Private paper route

## 1. Scientific objective and author claim

The authors used computation to compare the solution-phase Gibbs free energies of the two diastereomeric forms of ketoester intermediate 50 (the trans-disposed form labelled 50 and the cis alternative labelled S20). Their claim is that the trans form is thermodynamically preferred, while access to some cis material makes epimerization relevant to the planned ring closure.

## 2. System and model boundary

The system is the neutral, closed-shell 53-atom ketoester framework represented by the optimized Cartesian structures in SI Tables S35 (50) and S36 (S20). The calculation compares these two fixed stereochemical alternatives in methanol solution at 298.15 K and 1 atm standard-state thermochemistry. The comparison is a relative Gibbs free energy, not a kinetic barrier or reaction yield.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize each diastereomer and obtain frequencies/thermal corrections | Structures 50 and S20 | Gaussian 09 DFT | B3LYP-D3/6-31G(d,p); 298.15 K, 1 atm thermochemistry | Optimized geometries and thermal corrections | ev_doc_e93721ef1f70_001495_76f07baeaa72; ev_doc_e93721ef1f70_001496_97146b851864 |
| 2 | Re-evaluate electronic energies in methanol | Step-1 geometries | Gaussian 09 DFT with IEF-PCM | B3LYP-D3/6-311++G(d,p); methanol dielectric 32.63 | Solution electronic energies | ev_doc_e93721ef1f70_001495_76f07baeaa72; ev_doc_e93721ef1f70_001497_7b929684d611; ev_doc_e93721ef1f70_001498_fe6e2a1ee702; ev_doc_e93721ef1f70_001499_cc93bf83793e |
| 3 | Form the relative solution Gibbs energy | Energies and thermal corrections for both structures | Arithmetic combination of SI quantities | ΔG(sol) defined as G(S20) − G(50) | Relative diastereomer stability | ev_doc_e93721ef1f70_001500_48366ce0b361 |

## 4. Validation and analysis protocol

Each optimized structure was checked through its vibrational analysis; the SI frequency tables contain no negative frequencies for 50 or S20. The solution-phase Gibbs energies were compared using the same convention for both structures, and the cis-minus-trans difference was reported in kcal/mol. Interpretation is limited to thermodynamic preference and its relevance to the feasibility of epimerization; it does not establish an epimerization rate or transition state.

## 5. Private reference results

SI Table S34 reports the computational energy summary: G(sol) is −27368.83819 eV for 50 and −27368.73770 eV for S20, giving ΔG(sol) = G(S20) − G(50) = 2.3171919 kcal/mol (reported in the main text as 2.32 kcal/mol). Thus 50/trans is lower in free energy than S20/cis.

## 6. Limitations and interpretation boundaries

The result is a two-structure DFT/continuum-solvent comparison. It does not quantify conformational ensemble populations, explicit-solvent effects, kinetic barriers, or experimental equilibrium constants. Agreement should therefore be judged against the reported computational observable and the required frequency/identity checks, with method sensitivity reported rather than hidden.
