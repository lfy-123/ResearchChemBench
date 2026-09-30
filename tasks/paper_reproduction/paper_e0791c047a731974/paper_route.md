# Private paper route

## 1. Scientific objective and author claim

The authors use electronic-structure calculations to rationalize why selenium-integrated heptamethine cyanine Cy2 is an effective 830 nm triplet–triplet-annihilation upconversion sensitizer. Their claim is that heavy-atom incorporation, especially selenium, increases spin–orbit coupling and intersystem crossing while preserving an energetically suitable triplet state. The computationally testable core is the Cy2 S0 geometry, low-lying vertical S1/T1/T2 energies, and relaxed T1 adiabatic energy in chloroform.

## 2. System and model boundary

The modeled species is the Cy2 cation, with no iodide counterion, with the SI Cartesian S0 structure as the starting geometry. The calculations use chloroform continuum solvation. The relevant states are singlet ground state S0, lowest singlet excited state S1, and lowest triplet states T1 and T2. The reported T1 adiabatic energy is relative to S0.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground-state structure | Cy2 S0 coordinates, iodides omitted | Gaussian 16 DFT | B3LYP/6-31G(d,p); SMD chloroform; def2TZVP for the two Se atoms; Cy2 has no iodine, so the general SI iodine/SDD clause is inactive | optimized S0 geometry and vibrational analysis | ev_doc_12faeb9900c2_000087_bfb5062814ef; ev_doc_12faeb9900c2_000088_e3402a1f5a87; ev_doc_12faeb9900c2_000283_fbb6424a09c6 |
| 2 | Compute vertical excited states | optimized S0 geometry | Gaussian 16 TDDFT | same functional, solvent and heavy-element basis treatment | vertical S1, T1, T2 energies and transitions | ev_doc_12faeb9900c2_000088_e3402a1f5a87; ev_doc_12faeb9900c2_000177_2042854d666b |
| 3 | Relax the lowest triplet | optimized S0 geometry and T1 state | Gaussian 16 TDDFT triplet-root optimization on the singlet reference (TD=Triplets,Root=1); not unrestricted ground-state DFT at multiplicity 3 | same model boundary and solvent | relaxed T1 geometry and adiabatic T1 energy | ev_doc_abac62ae831c_000240_eb03647e9fdc; ev_doc_abac62ae831c_000242_6593d5c6384c |
| 4 | Interpret photophysics | computed states and orbital/electron-hole descriptors | Multiwfn/GaussView analysis plus comparison with kinetics | compare state gaps, selenium contributions and ISC-related observations | mechanistic interpretation of selenium-enhanced triplet formation | ev_doc_abac62ae831c_000212_608edbbbbd81; ev_doc_abac62ae831c_000240_eb03647e9fdc |

## 4. Validation and analysis protocol

The S0 optimization is accepted only when it converges to a stationary point and the vibrational analysis has no imaginary frequency. The state calculation must identify S1, T1 and T2 explicitly, retain state labels and report vertical energies in eV. The T1 relaxation must preserve triplet multiplicity and report the adiabatic energy relative to the corresponding S0 energy. The authors compare the energetic ordering and gaps with the criterion 2T1 > S1 and discuss the small S1–T2 gap as relevant to ISC. Their electronic analysis finds localized excitations and substantial selenium contributions to the Cy2 hole distribution; the article reports 14.8%, 10.6% and 14.9% for the two Se atoms in S1, T1 and T2, respectively. Method sensitivity and the known tendency of the chosen approach to underestimate T1 energies are interpretation limitations.

## 5. Private reference results

SI Table S3 reports Cy2 vertical energies: S1 1.8909 eV, T1 1.0556 eV and T2 2.1221 eV. The article reports the Cy2 relaxed T1 adiabatic energy as 1.09 eV. The same article reports Cy2 ISC rate 3.2 × 10^8 s−1 and triplet quantum yield 23%, and attributes the enhancement to selenium-associated spin–orbit coupling. These values are hidden evaluator references.

## 6. Limitations and interpretation boundaries

The coordinates are a single published conformer and omit iodide counterions as in the authors' calculations. Numerical agreement is model-dependent; the article explicitly notes systematic T1 underestimation. The task evaluates reproducible state identification, validation and comparison, not experimental quantum yields or a universal ranking of sensitizers.
