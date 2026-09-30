# Scientific objective

For the uniquely supplied compound 5 (hexa-peri-hexabenzo[7]helicene) structure, independently determine a defensible equilibrium geometry and quantify its mean inner-rim torsion angle. The scored observable is the arithmetic mean, in degrees, of five individual inner-rim dihedrals that you identify unambiguously by four atom indices in the supplied ordering (symmetry-equivalent sites may be averaged only after being listed individually).

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors use compound 5 as a structural calibration case for whether a quantum-chemical geometry model captures helicene strain. They report that the calculated mean inner-rim torsion is close to an experimental structural value, supporting the method's use for the related derivative series.

**Candidate route or mechanism.**
A focused reproduction route is to optimize the isolated neutral singlet in its ground electronic state without imposing symmetry, then evaluate the five inner-rim dihedrals on the converged equilibrium geometry. Treat the resulting torsion mean as a structural calibration observable rather than as a universal validation of one method.

**Discriminating evidence.**
Use a stationary-point check, preferably vibrational frequencies, together with the explicitly indexed five torsions and their arithmetic mean. An independent plausibility check and comparison with the experimental structural benchmark are the evidence that distinguishes a credible equilibrium-geometry calibration from an unconverged or differently defined structure.

# Public inputs and scientific boundaries

`data/inputs/compound5.xyz` is a 72-atom Cartesian XYZ structure in Å, with atom ordering fixed by file order. The scored system is this uniquely supplied compound 5 molecule, neutral (charge 0), closed-shell singlet (multiplicity 1), isolated in the gas phase; do not add a host, solvent, crystal packing, counterion, or external structure. The target state is a stationary equilibrium structure. You choose the computational method, software, convergence settings, and any bounded independent checks, and must disclose them. A calculation is complete when an optimized structure, stationary-point/minimum check, all five named dihedrals with atom indices and convention, arithmetic mean, uncertainty/limitations, and a stopping reason are reported. If this cannot be achieved, report bounded failure with diagnostics rather than inventing a result.

# Required scientific validation/investigation

Define the five inner-rim torsions by atom indices in the supplied ordering before scoring; identify each as an inner-rim dihedral by its local connectivity or an equivalent structural description, use one consistent signed or absolute convention, and state the arithmetic-mean formula. Generate at least one optimized candidate from the public structure, deduplicate any additional candidates by connectivity and geometry, and advance only converged candidates. Validate the reported candidate with a frequency calculation or another scientifically justified stationary-point test, identify any imaginary modes, and perform one independent plausibility check. Report search coverage and stopping reason. If bounded failure occurs, successful-result quantities may be omitted, but attempted coverage and diagnostics are required. Explain what the torsion result does and does not establish about this isolated molecule.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. It must contain status, software/model details, candidate identity, optimization and validation evidence, five per-torsion records, mean torsion, uncertainty, interpretation, and limitations. If bounded failure occurs, use the failure branch and include diagnostics and attempted coverage.
