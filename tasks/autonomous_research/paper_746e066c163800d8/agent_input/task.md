# Scientific objective

For the uniquely supplied compound 5 (hexa-peri-hexabenzo[7]helicene) structure, independently determine a defensible equilibrium geometry and quantify its mean inner-rim torsion angle. The scored observable is the arithmetic mean, in degrees, of five individual inner-rim dihedrals that you identify unambiguously by four atom indices in the supplied ordering (symmetry-equivalent sites may be averaged only after being listed individually).

# Public inputs and scientific boundaries

`data/inputs/compound5.xyz` is a 72-atom Cartesian XYZ structure in Å, with atom ordering fixed by file order. It is compound 5, neutral (charge 0), closed-shell singlet (multiplicity 1), isolated in the gas phase. No paper, SI, general web search, solvent, crystal packing, counterion, or external experimental structure is needed or allowed. The target state is a stationary equilibrium structure. You choose the computational method, software, convergence settings, and any bounded independent checks, and must disclose them. A calculation is complete when an optimized structure, stationary-point/minimum check, all five named dihedrals with atom indices and convention, arithmetic mean, uncertainty/limitations, and a stopping reason are reported. If this cannot be achieved, report bounded failure with diagnostics rather than inventing a result.

# Required scientific validation/investigation

Define the five inner-rim torsions by atom indices in the supplied ordering before scoring; identify each as an inner-rim dihedral by its local connectivity or an equivalent structural description, use one consistent signed or absolute convention, and state the arithmetic-mean formula. Generate at least one optimized candidate from the public structure, deduplicate any additional candidates by connectivity and geometry, and advance only converged candidates. Validate the reported candidate with a frequency calculation or another scientifically justified stationary-point test, identify any imaginary modes, and perform one independent plausibility check. Report search coverage and stopping reason. If bounded failure occurs, successful-result quantities may be omitted, but attempted coverage and diagnostics are required. Explain what the torsion result does and does not establish about this isolated molecule.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. It must contain status, software/model details, candidate identity, optimization and validation evidence, five per-torsion records, mean torsion, uncertainty, interpretation, and limitations. If bounded failure occurs, use the failure branch and include diagnostics and attempted coverage.
