# Private paper route

## 1. Scientific objective and author claim

The paper studies the thermal crossed [2+2] cycloaddition of an N-allyl gem-difluoroenamine to a gem-difluoro azabicyclo[2.1.1]hexane. The computational claim is that regioselective C–C bond formation by the open-shell-singlet [2+2] route is kinetically preferred over the competing aza-Claisen rearrangement.

## 2. System and model boundary

The computational starting species is the in-situ N-allyl gem-difluoroenamine called Int1. The authors treat minima and transition states with implicit toluene solvation, thermal corrections at 298 K, and a 1 mol/L solution standard-state correction. Competing pathways include C1 attack leading to a diradical and subsequent bicyclization, and C2 attack leading to aza-Claisen products.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Locate minima and transition states | Int1 and pathway geometries | Gaussian 16 DFT | M06-2X/def2-SVP, SMD(toluene) | Optimized structures | ev_doc_5ade8f2808e1_000369_5f9efdbd2028 |
| 2 | Verify stationary points and thermochemistry | Optimized structures | Gaussian 16 frequency analysis | 298 K; ZPE, thermal H/G corrections | Gibbs free energies and imaginary frequencies | ev_doc_5ade8f2808e1_000369_5f9efdbd2028 |
| 3 | Select electronic state | Minima and TS wavefunctions | Gaussian 16 stability analysis | Open-shell singlet, closed-shell singlet and triplet checks | Stable wavefunction assignment | ev_doc_5ade8f2808e1_000378_3221db237609; ev_doc_5ade8f2808e1_000381_688a21ad9f76 |
| 4 | Refine energies | Verified structures | Gaussian 16 single points | M06-2X/def2-TZVP-SMD(toluene) on def2-SVP geometries | Refined G values | ev_doc_5ade8f2808e1_000369_5f9efdbd2028 |
| 5 | Verify critical connectivity | Critical TSs | Gaussian 16 IRC | Same level as optimization | Reactant/product connectivity check | ev_doc_5ade8f2808e1_000369_5f9efdbd2028 |
| 6 | Compare regioselective paths | Int1-referenced free energies | Derived from stationary-point G values | Solution standard-state correction 1.89 kcal/mol | Barrier profile and preferred pathway | ev_doc_5ade8f2808e1_000384_d2274144acba; ev_doc_d81e23b24127_000099_a264bcde3d05 |

## 4. Validation and analysis protocol

The authors checked frequencies, wavefunction stability, and IRC connectivity for critical transition states. They compared open-shell-singlet, closed-shell-singlet, and triplet alternatives. The complete SI profile enumerates the three aza-Claisen possibilities and the [2+2] route.

## 5. Private reference results

The published overall [2+2] barrier from Int1 is 31.0 kcal/mol, and the lowest aza-Claisen barrier (TS8, trans-imine route) is 37.1 kcal/mol. The [2+2] route is therefore lower by 6.1 kcal/mol. The open-shell-singlet route is the viable electronic description; the CSS and triplet alternatives are reported as inaccessible.

## 6. Limitations and interpretation boundaries

These are method-dependent computed free energies, not experimental activation parameters. Conformer search, TS assignment, spin contamination and IRC quality can affect independently reproduced values. The task scores the two Int1-referenced barriers and the mechanistic interpretation within the stated model boundary, not an assertion that every possible computational method must reproduce the paper exactly.
