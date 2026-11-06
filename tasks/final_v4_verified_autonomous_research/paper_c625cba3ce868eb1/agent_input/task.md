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

Compound 7 is supplied as an optional comparator. No calculation of it is required to answer the (R)-4 question. Choose electronic descriptors and methods independently.

## Required results

1. Quantify and interpret the electronic difference between the two alkene sites, identifying the observable, sign convention, atom mapping, medium and uncertainty.
2. Explain how the computed molecular features bear on the alternative intramolecular oxygen-closure connectivities and the given ring outcome. Distinguish the proposed explanation from any kinetics or unique mechanism that the evidence has not established.
3. State the supported reach of your model for the chemical NBS experiment, accounting for the modeled composition/medium and any comparator confounding actually used.

## Submission

Submit `report/results.json` and `report/report.md` following the supplied guide and schema. Link native calculations and reproducible analysis. Only final scientific conclusions earn points. No fixed mechanism, software, number of searches or transition-state matrix is prescribed. Use the mode's public inputs and available tools plus general documentation; do not access private evaluation files, prior verification archives or the other mode's guidance.
