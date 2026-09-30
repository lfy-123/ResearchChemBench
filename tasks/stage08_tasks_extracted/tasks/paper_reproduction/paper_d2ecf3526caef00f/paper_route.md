# Private paper route

## 1. Scientific objective and author claim

The paper tests whether a selective semiempirical DFT+α correction for Ge 4s-like states can repair PBE's band-edge ordering while retaining accurate bulk structure and mechanics at lower cost than HSE. The reported claim is simultaneous agreement with low-temperature Ge electronic and elastic data.

## 2. System and model boundary

Bulk elemental Ge in the diamond structure (Fd3̅m), two atoms per conventional cubic cell, nonrelativistic PAW pseudopotential including 3d electrons. The computed observables are the equilibrium lattice constant, Γ–Γ and Γ–L gaps, and B0, C11, C12, C44. Phonons and HSE are contextual validation, not required task outputs.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Define corrected electronic Hamiltonian | Ge diamond cell and Ge PAW data | Quantum ESPRESSO localized-manifold projector/LDA+U implementation | PBE; correction coefficient α; projector built from modified 4s pseudopotential orbital using Eq. (3) | DFT+α SCF model | ev_doc_9ebde426099f_000013_f86e58b5737d; ev_doc_9ebde426099f_000032_95dfbc0a4e99 |
| 2 | Find equilibrium structure | Ge cell | QE energy–volume calculations | 80 Ry wavefunction, 320 Ry density, 12^3 Monkhorst–Pack, 0.001 Ry smearing | minimum of energy–volume curve | ev_doc_9ebde426099f_000032_95dfbc0a4e99; ev_doc_9ebde426099f_000105_8115d68142f8 |
| 3 | Evaluate band edges | relaxed cell | QE band/eigenvalue calculations | DFT+α and comparison PBE; high-symmetry Γ and L points | direct and indirect gaps, band character | ev_doc_9ebde426099f_000110_ae83270abebe; ev_doc_9ebde426099f_000112_26117f40943d |
| 4 | Evaluate mechanics | relaxed cell and strained cells | QE/termo_pw elastic workflow | same core basis and BZ settings; fit stress/energy response | B0, C11, C12, C44 | ev_doc_9ebde426099f_000038_ac5b98a17134; ev_doc_9ebde426099f_000128_7a517df34b0f |
| 5 | Compare with experiment | computed properties | error analysis | low-temperature electronic references and Ge elastic references | relative errors and qualitative assessment | ev_doc_9ebde426099f_000046_6e5fc1ec1979; ev_doc_9ebde426099f_000056_a21855da08cb |

## 4. Validation and analysis protocol

The authors scan α, optimize the lattice for each value, determine both gaps at the corresponding relaxed lattice, and calculate elastic constants from deformations. They inspect band orbital character and compare DFT+α against PBE, HSE and cited measurements. The SI notes that the direct gap is closed in PBE at the optimized geometry but becomes indirect/open under the correction.

## 5. Private reference results

The paper reports, for its selected correction, an optimized lattice constant of 5.676 Å; the electronic gaps agree with the cited 0.90 eV direct and 0.74 eV indirect low-temperature values to under 2%; and B0, C11, C12 and C44 each have relative error below 6% against the cited elastic references. These values and the exact selected coefficient are private evaluator references.

## 6. Limitations and interpretation boundaries

The correction is semiempirical and selectively addresses Ge s–p mixing; it does not remove general exchange-correlation limitations. Elastic fits can be irregular near the gap-opening transition. Results depend on pseudopotential, convergence, relativistic treatment and temperature conventions. Agreement with experiment is a benchmark, not proof of universal transferability.
