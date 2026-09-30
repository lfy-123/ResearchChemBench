# Scientific objective

Determine, by an independent computational investigation, how proton source and H* coverage affect elementary HER thermodynamics and kinetics on Au(111), and whether the resulting trends support a coherent explanation of acidic/alkaline and coverage-dependent behavior. Do not assume or reproduce an author route; formulate and discriminate plausible explanations from your calculations.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json`. The system is a 3-layer 3×3 Au(111) slab with 15 Å vacuum, bottom two layers fixed, nine top-layer sites; media are explicitly defined as H7O3+ at 0.000 V vs SHE and H8O4 at −0.826 V vs SHE; coverages are 0 and 7/9 ML. Investigate Volmer, Heyrovsky, and Tafel. Choose and justify computational methods, charge/multiplicity, solvation, conformer generation, and reference convention. The scored objects are the declared condition/step combinations, not a particular hidden geometry.

# Required scientific validation/investigation

Propose plausible mechanistic explanations, generate a finite deduplicated candidate set of states/conformers and paths, and record selection and rejection reasons. Optimize and validate each advanced candidate with stated outcome-based criteria; establish endpoint continuity and TS/path quality. Continue until every requested combination is covered by a converged calculation or report bounded failure with coverage and a scientifically meaningful limitation. Discriminate explanations using computed ΔG and G_a, compare media and coverages, and perform at least one sensitivity check.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include candidate identities, structures or hashes, observables with units, validation evidence, search coverage/stopping rationale, competing explanations, final conclusion, and truthful completion status. Bounded failure must be represented explicitly.
