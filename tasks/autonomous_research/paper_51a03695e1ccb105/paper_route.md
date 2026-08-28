# Private paper route

## 1. Scientific objective and author claim

The paper studies visible-light oxidative coupling of aminotriazoles to 3,3′-azo-1,2,4-triazoles. Its computational objective is to examine elementary steps in a photocatalytic mechanism, including formation of nitrosotriazole and its coupling with an aminotriazole-derived species. The authors qualitatively propose that base-assisted deprotonation makes the nitrosotriazole-to-azo coupling kinetically accessible.

## 2. System and model boundary

The model reaction uses the 1,2,4-triazole scaffold with nitrosotriazole, an aminotriazole-derived anion, and the 3,3′-azo-1,2,4-triazole product. Calculations are continuum-solvent molecular calculations in methanol; the published mechanism also discusses the Ir photocatalyst, oxygen/superoxide, and radical intermediates, but the benchmark endpoint is the base-assisted coupling substep.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground-state molecular structures | Reactant, intermediate, product and catalyst geometries | Gaussian 16 DFT | B3LYP-D3; SDD on Ir and 6-31G* on other atoms; CPCM methanol; singlet ground state for closed-shell species | Optimized minima | ev_doc_a1a23c70aea5_000122_0a4c32d9b09f; ev_doc_a1a23c70aea5_000123_8089ae62aaa4; ev_doc_a1a23c70aea5_000124_b48e516ba6f4 |
| 2 | Locate and verify saddle points | Optimized minima and reaction guesses | Gaussian 16 TS search and IRC | Same B3LYP-D3/SDD/6-31G*/CPCM-methanol model | TS geometries and IRC connections | ev_doc_a1a23c70aea5_000172_5c1ea6e262b7; ev_doc_a1a23c70aea5_000122_0a4c32d9b09f |
| 3 | Refine energies | Optimized minima and TS structures | Gaussian 16 single points | M06-2X/def2-TZVP with SMD methanol | Refined electronic energies | ev_doc_a1a23c70aea5_000124_b48e516ba6f4 |
| 4 | Obtain reaction free energies and barriers | Refined energies plus thermochemical corrections | Energy differences from the optimized/TS states | Barrier measured from the specified separated reactant reference to the coupling TS; reaction free energy from reactants to azo product | Mechanistic energy profile | ev_doc_8fe32c74f526_000184_e18a17bc3d7d |

## 4. Validation and analysis protocol

Minima were checked for absence of imaginary frequencies. A candidate transition state was accepted only when it had one relevant imaginary mode and IRC calculations connected it to the intended reactant and product basins. The authors compared the base-assisted coupling with the unassisted nitrosotriazole/aminotriazole route and interpreted the lower base-assisted barrier as support for the role of base in the mechanism.

## 5. Private reference results

The paper reports a base-assisted coupling barrier of 13.35 kcal/mol and a reaction free energy of −29.58 kcal/mol for this step. The unassisted coupling barrier is reported as 46.07 kcal/mol. These values are hidden from the Agent and are used only in evaluator references.

## 6. Limitations and interpretation boundaries

The benchmark tests one computed elementary step, not the complete photochemical catalytic cycle or experimental yield. Continuum solvation, finite conformer sampling, spin/electronic-state choices, and the treatment of separated reactants can affect absolute energies. Agreement with the reference supports consistency with the published model calculation but does not establish a unique physical mechanism.
