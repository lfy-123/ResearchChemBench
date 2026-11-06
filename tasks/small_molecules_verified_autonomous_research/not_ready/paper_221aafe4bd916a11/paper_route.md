# Private paper route

## 1. Scientific objective and author claim

The authors computed whether protonated bisphosphines can transfer hydride to CO2, with particular emphasis on the in–out conformers 2a and 2d. They claim that these systems undergo a single-step hydride transfer with comparatively low activation barriers.

## 2. System and model boundary

The system is the monoprotonated 1,8-bisphosphine 2a reacting with CO2 in acetonitrile at 298 K. The optimized 2a in–out conformer is a singlet cation; the hydride-transfer transition structure connects it to the bisphosphine dication and formate.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate starting conformers | Molecular structures | CREST/GFN2-xTB | Lowest-energy conformers selected | Starting geometries | ev_doc_e2e6d3617ef9_000006_636483fdb85d |
| 2 | Optimize reactant and TS structures | Minima and TS guesses | Gaussian 16, ωB97XD/6-31G(d,p), PCM | Acetonitrile, 298 K, unconstrained optimization | Optimized geometries and frequencies | ev_doc_e2e6d3617ef9_000019_0b569513144d; ev_doc_e2e6d3617ef9_000023_e4c53b960470 |
| 3 | Refine energies | Optimized structures | Gaussian 16, ωB97XD/6-311++G(d,p), PCM | Acetonitrile; default SCF/grid settings | Refined electronic energies | ev_doc_e2e6d3617ef9_000026_fccc931cd72c; ev_doc_e2e6d3617ef9_000029_077dcb51a880 |
| 4 | Determine barrier | Reactant and TS free energies | Relative Gibbs-energy analysis | Hydride-transfer pathway | Activation barrier | ev_doc_3aa39a5bf46c_000113_fa8a2e035650; ev_doc_3aa39a5bf46c_000115_c96527012c62 |

## 4. Validation and analysis protocol

The SI requires all-positive frequencies for minima and exactly one negative frequency for a TS. The authors inspect whether an intermediate is present and compare the transition-state barrier for the hydride-transfer channel. Their explanation invokes the in–out orientation and favorable approach geometry, while noting that the reaction is stoichiometric rather than demonstrated catalysis.

## 5. Private reference results

For 2a, the reported single-step hydride-transfer barrier is 21.8 kcal mol−1. The paper reports no intervening intermediate for 2a; 2d is the other in–out example. These are hidden from Agent-visible inputs.

## 6. Limitations and interpretation boundaries

The result is a model-dependent DFT free-energy estimate, not an experimental rate constant. Conformer and TS coverage must be reported by the investigator. The paper explicitly does not establish regeneration of the dication or catalytic turnover.
