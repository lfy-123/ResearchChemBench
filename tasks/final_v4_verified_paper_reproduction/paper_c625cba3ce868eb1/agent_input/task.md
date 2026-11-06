# Molecular origin of hydroperoxide halocyclization selectivity

## Scientific question

What molecular electronic evidence explains the supplied halocyclization outcome of hydroperoxide (R)-4, and what does that evidence establish about the nonenzymatic NBS reaction?

## Input files

- `data/inputs/systems.json`: complete atom-mapped (R,E)-4, compound 7 and reagent identities, including charge and spin. The graphs do not specify optimized conformations or reaction intermediates.
- `data/inputs/observations.json`: the reported ring-product observations and their experimental contexts.
- `data/inputs/source_facts.json`: quantities, medium and duration for the chemical experiment.

## Scope

The given experiment produces six-membered tetrahydropyrans and reports similar chromatographic/NMR profiles for chemical and enzyme reactions. The chemical procedure uses a 3/4 hydroperoxide mixture (50 mg, 0.27 mmol), NBS (51 mg, 0.284 mmol) and Et3N (4.2 µL, 0.03 mmol) in 6 mL anhydrous DCM under argon for 4 h. Its printed NBS concentration is 473 mM, whereas the stated amount and volume imply 47.3 mM. Preserve this discrepancy and declare the convention used for any concentration-dependent inference.

The molecular target here is full neutral-singlet (R,E)-4, C10H20O3, rather than the whole substrate mixture. Select and justify molecular states and an environment appropriate to the claimed local explanation. Compare its alkene sites using the supplied atom maps. The enzyme, substrate photogeneration and full cascade are outside scope. A supplied ring outcome is an observation to explain, not a prediction to claim as new.

## Author baseline for reproduction

Reproduce and assess the reported molecular comparison of (R)-4 and hydroperoxide-free 7. The authors use Gaussian16 A.03, B3LYP/CBSB7, C-PCM water, frequency-checked minima and MEP-fitted (Merz–Kollman) charges at the same level (main computational methods; SI pp30–32/Fig.S50). Main pp3–4 discusses an allylic-hydroperoxide-associated alkene polarization and its possible relation to ring closure; it explicitly distinguishes reactant polarization from proof of a specific mechanism.

Report the signed alkene contrasts Δq4=q(C2)−q(C4) and Δq7=q(C8)−q(C10), in electron units, and |Δq4|/|Δq7|. Source values are −0.441 e, −0.049 e and approximately 9.0, respectively, derived from printed charges −0.507/−0.066 and −0.311/−0.262. The fit grid is not fully specified. Retain the author observable and report justified substitutions; Mulliken or NPA values are not interchangeable with MK merely because all are called charges. Actual computation is required; copying disclosed targets earns no credit.

Compound 7 is required for this disclosed reproduction comparison. Its reported six-/seven-member products are from an enzyme experiment, and it differs from 4 in more than the hydroperoxide group. Assess the causal reach of this comparison. The source provides no validated DCM/NBS reaction-path/free-energy network; extending the aqueous monomer model does not automatically validate one.

## Required results

1. Quantify and interpret the electronic difference between the two alkene sites, identifying the observable, sign convention, atom mapping, medium and uncertainty. In reproduction mode also report the disclosed comparator quantities in the author baseline.
2. Explain how the computed molecular features bear on the alternative intramolecular oxygen-closure connectivities and the given ring outcome. Distinguish the proposed explanation from any kinetics or unique mechanism that the evidence has not established.
3. State the supported reach of your model for the chemical NBS experiment, accounting for the modeled composition/medium and any comparator confounding actually used.

## Submission

Submit `report/results.json` and `report/report.md` following the supplied guide and schema. Link native calculations and reproducible analysis. Only final scientific conclusions earn points. No fixed mechanism, software, number of searches or transition-state matrix is prescribed. Use the mode's public inputs and available tools plus general documentation; do not access private evaluation files, prior verification archives or the other mode's guidance.
