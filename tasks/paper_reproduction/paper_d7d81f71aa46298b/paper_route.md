# Private paper route

## 1. Scientific objective and author claim

The paper tests whether tensile-force activation of isotactic PVC can generate HCl through a mechanoradical pathway with a lower barrier than thermal PVC activation. The authors claim that an initial PVC mechanoradical undergoes intramolecular HAT and subsequent HCl release, and that the force-driven barriers are substantially below the thermal activation barrier.

## 2. System and model boundary

The computational model is an isotactic PVC oligomer (38 atoms, neutral broken-symmetry open-shell singlet) with a 1000 pN tensile force applied to terminal methyl groups C1 and C30 (1-based XYZ indices). The force-induced reactant is the SI structure Iso-PVC-R-F1000. Energies/free energies are evaluated at 298.15 K and 1 atm; the published calculations use unrestricted DFT and force-aware free energies for the constrained reactant.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate force-activated PVC mechanoradical | isotactic PVC model and terminal-methyl force sites | Gaussian 16, EX-AFIR | tensile force Fτ; unrestricted treatment | force-constrained optimized reactant and force free energy | ev_doc_7fb6a617f3ae_000100_097983fdbbea; ev_doc_7fb6a617f3ae_000130_b0e2594ce041 |
| 2 | Explore and optimize reaction transition states | force reactant and radical reaction candidates | AFIR exploration followed by unrestricted DFT optimization | isotactic model; unconstrained minima/TSs; IRC confirmation | validated TS and connected product/minimum | ev_doc_7fb6a617f3ae_000100_097983fdbbea; ev_doc_7faebe84b315_000094_afa93b62b1a1 |
| 3 | Compute free-energy barriers | optimized minima and TSs | UB3LYP-D3/6-311G(d,p) with frequencies | 298.15 K, 1 atm | HAT/HCl-release barriers and thermal comparison | ev_doc_7fb6a617f3ae_000100_097983fdbbea; ev_doc_7faebe84b315_000113_7bee73517d10 |
| 4 | Compare force and thermal channels | force profile and thermal PVC pathway | same DFT level; thermal pathway profiles | barrier comparison and mechanistic interpretation | mechanical pathway favored over thermal pathway | ev_doc_7faebe84b315_000113_7bee73517d10; ev_doc_7faebe84b315_000107_01885e131d61 |

## 4. Validation and analysis protocol

The authors used unrestricted wavefunction checks for open-shell species, optimized minima and transition states, and IRC calculations to verify TS connectivity. They compared Gibbs free-energy barriers at 298.15 K and 1 atm and additionally examined the pathway at 323.15 K. The interpretation is limited to the finite isotactic oligomer model and approximate force-induced free-energy surface.

## 5. Private reference results

The paper reports a +84.6 kJ/mol HAT free-energy barrier for the IntA-1 to TSA-1 step, a +86.7 or +79.3 kJ/mol alternative HCl-release barrier from IntA-2, a +64.6 kJ/mol IntB-1 route barrier, and a 163.2 kJ/mol thermal activation barrier. These values are hidden from agents and used only by evaluators.

## 6. Limitations and interpretation boundaries

The model is isotactic although commercial PVC is commonly atactic; force implementation is an approximate EX-AFIR representation; conformational coverage and radical termination chemistry remain incomplete. Agreement is therefore judged against the stated model/reference observables, not as a universal polymer kinetic constant.
