# Scientific objective

Test the authors' qualitative hypothesis that the allylic hydroperoxide in neutral, closed-shell (R)-4 polarizes the adjacent C=C bond, whereas hydroperoxide-free neutral, closed-shell alkenol 7 has electronically comparable alkene sites. Independently plan and execute calculations that compare the reactant-state molecular electrostatic potential/electronic density and atom-resolved electrostatic-potential-derived partial charges of the two molecules in aqueous solution. This is a reactant-state electronic comparison, not a request to calculate a transition state, product ordering, or reaction energy.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the allylic hydroperoxide in neutral, closed-shell (R)-4 changes the reactant-state electron-density distribution at the nearby C=C bond, while hydroperoxide-free neutral, closed-shell alkenol 7 has electronically comparable alkene sites. They present this as a plausible reactant-state electronic rationale for later regioselectivity, not as proof of a reaction mechanism.

**Candidate route or mechanism.**
Focus the comparison on hydroperoxide-associated polarization: assess whether the alkene carbon proximal to the hydroperoxide is electronically distinct from the distal carbon in 4, and compare that asymmetry with the two equivalent alkene sites of 7. Treat the proposed relationship to downstream 6-exo-trig haloetherification as a comparison hypothesis rather than a conclusion.

**Discriminating evidence.**
Use consistently computed molecular electrostatic potential or electronic-density descriptors and electrostatic-potential-derived atom-resolved partial charges, especially the signed difference between the two alkene carbons in each molecule. Validate the electronic states and use the same charge definition for the cross-molecule comparison.

# Public inputs and scientific boundaries

The public inputs are `data/inputs/compound_4_R.xyz` (33 atoms, explicit atom order, (R)-4) and `data/inputs/compound_7.xyz` (25 atoms, explicit atom order, 7). They are fixed, answer-neutral benchmark conformers supplied as Cartesian inputs; do not claim to reproduce a hidden optimized geometry. Treat both systems as neutral closed-shell singlets. In 4, the alkene is atoms 2 and 4 and atom 2 is bonded through atom 1 to hydroperoxide oxygen atom 22; report [2, 4] as [hydroperoxide-proximal, distal]. In 7, the alkene is atoms 8 and 10; report [8, 10] in increasing atom-index order because the sites are chemically equivalent for this comparison. Preserve atom order. The physical boundary is an isolated molecule represented in aqueous solution by the chosen computational treatment. No enzyme, brominating reagent, solvent molecule, transition state, intermediate, or product structure is supplied or required. You may choose software, electronic-structure method, solvation model, charge partition, and additional conformers, but must state them. Do not use the paper, SI, general web, or hidden evaluator as an input.

# Required scientific validation/investigation

Consistently evaluate both supplied conformers at a justified electronic-structure/solvation level; geometry optimization is optional and must not replace reporting results for the supplied conformers. Validate each reported electronic state with SCF/convergence and wavefunction or equivalent state checks, and, if you optimize, also report frequency/Hessian evidence and any imaginary modes. Retain atom identity through all transformations. Compute an MEP/electrostatic-potential descriptor and atom-resolved charges for both molecules, and report the two alkene-carbon charges and their signed difference for each molecule. Compare the hydroperoxide-containing and hydroperoxide-free cases using the same charge definition. If you explore conformers or method sensitivity, describe generation, deduplication, selection/advancement, and coverage. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` and any supporting files needed to reproduce it. The JSON must contain: `status` (`complete` or `bounded_failure`); per-molecule `molecules` entries keyed by `compound_4_R` and `compound_7`, each with `atom_count`, `alkene_carbon_indices`, `charges` (atom-indexed numeric array when available), `charge_definition`, `validation` and `method`; `comparison` with signed alkene-charge differences and a qualitative polarization statement; `coverage`; and `provenance`. A complete result must include numeric charges for every atom of each molecule, validation evidence for each molecule, and enough method/provenance detail to reproduce the analysis. A bounded failure must truthfully identify which required artifact could not be produced, report attempted validation and coverage, and may omit unavailable charge arrays while retaining per-molecule identity, method, charge definition, and validation records.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
