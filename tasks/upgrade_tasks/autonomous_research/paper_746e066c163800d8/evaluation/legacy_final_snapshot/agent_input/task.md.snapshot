# Scientific objective

For the uniquely supplied compound 5 (hexa-peri-hexabenzo[7]helicene) structure, independently determine a defensible equilibrium geometry and quantify its mean inner-rim torsion angle. The scored observable is the mean of the absolute values, in degrees, of five individual inner-rim dihedrals that you identify unambiguously by four atom indices in the supplied ordering (symmetry-equivalent sites may be averaged only after being listed individually).

# Public inputs and scientific boundaries

`data/inputs/compound5.xyz` is a 72-atom Cartesian XYZ structure in Å, with atom ordering fixed by file order. It is compound 5, neutral (charge 0), closed-shell singlet (multiplicity 1), isolated in the gas phase. No paper, SI, general web search, solvent, crystal packing, counterion, or external experimental structure is needed or allowed; no experimental target angle is supplied. The evaluator handles the private experimental comparison; the Agent reports its calculation. The target state is a stationary equilibrium structure. You choose the computational method, software, convergence settings, and any bounded independent checks, and must disclose them. A calculation is complete when an optimized structure, stationary-point/minimum check, all five named dihedrals with atom indices and convention, mean absolute torsion are reported. If this cannot be achieved, report bounded failure with diagnostics rather than inventing a result.

# Required scientific validation/investigation

Define the five inner-rim torsions by atom indices in the supplied ordering before scoring; identify each as an inner-rim dihedral by its local connectivity or an equivalent structural description, retain the signed values in a declared dihedral convention, and report mean_torsion_deg = sum(abs(phi_i))/5. Generate at least one optimized candidate from the public structure, deduplicate any additional candidates by connectivity and geometry, and advance only converged candidates. Validate the reported candidate with a frequency calculation or another scientifically justified stationary-point test, identify any imaginary modes, and perform one independent plausibility check. Record the candidates actually calculated. If bounded failure occurs, successful-result quantities may be omitted, but attempted coverage and diagnostics are required.

The XYZ is an independently embedded, unoptimized starter, not an author-optimized endpoint. `data/inputs/compound5_identity.json` supplies the mapped graph and the inner-rim chain [1,66,65,64,63,62,61,59]. Use its five consecutive quadruples, preserving the given molecular identity and source-labelled handedness; if you reorder atoms, supply a complete map back to these IDs. No optimized torsion magnitude was used to generate the starter. On bounded failure, unavailable imaginary-mode counts may be null with diagnostics; never use zero for unknown. A complete result with no frequency count must instead supply auditable equivalent minimum-test evidence in validation.equivalent_minimum_evidence.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. It must contain status, software/model details, candidate identity, optimization and validation evidence, five per-torsion records, mean torsion, uncertainty, interpretation. If bounded failure occurs, use the failure branch and include diagnostics and attempted coverage.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
