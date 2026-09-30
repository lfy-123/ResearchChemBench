# Scientific objective

Determine, by an independently chosen computational investigation, the optimized isolated-molecule electronic structure of neutral singlet 1-phenyl-5-(m-tolyl)-1H-tetrazole (C14H12N4). Report EHOMO, ELUMO, the HOMO-LUMO gap, ionization potential, electron affinity, chemical potential, electronegativity, hardness, softness and electrophilicity, and state what those quantities imply within this model boundary about electronic stability/reactivity.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors interpret the molecule's frontier-orbital electronic structure as consistent with comparatively high kinetic stability, limited chemical reactivity, and a hard electronic character. This is a qualitative claim to test using the optimized isolated-molecule calculation.

**Candidate route or mechanism.**
A relevant candidate explanation is that the frontier orbitals of the neutral singlet optimized structure yield a relatively wide separation, with the occupied orbital serving as the donor-like frontier state and the unoccupied orbital as the acceptor-like frontier state. The authors also relate their computed structure qualitatively to the molecular geometry observed by single-crystal diffraction, while the scored model remains an isolated molecule.

**Discriminating evidence.**
Use the optimized geometry and a minimum check to establish the state being analyzed, then examine the frontier-orbital energies and derived conceptual-DFT descriptors. Compare alternative conformers or computational models if explored, and use their identities, convergence, curvature evidence, orbital separation, and descriptor trends to assess whether the proposed stability and limited-reactivity interpretation is supported within the stated model boundary.

# Public inputs and scientific boundaries

Use `data/inputs/molecule.json`, which uniquely defines the molecular connectivity by SMILES and supplies formula, neutral formal charge and singlet multiplicity. The system is one isolated molecule; exclude solvent, counterion, crystal packing, protein binding and biological efficacy. Select and justify your own computational method, basis, geometry strategy and analysis. No author route or target numerical value is supplied.

# Required scientific validation/investigation

Construct a chemically valid starting geometry, optimize it to a stationary point, and verify the final state and convergence. Perform a vibrational or equivalent curvature check to establish whether the state is a minimum and report imaginary modes. If more than one conformer or computational model is investigated, preserve candidate identities, explain deduplication and coverage, and justify the state used for the final observables. Completion requires one validated minimum, reproducible provenance, explicit descriptor formulas/sign conventions and every requested observable with units. Stop at that point, or give a bounded-failure report identifying the unmet validation and completed evidence.

# Deliverables

Submit `report/results.json` conforming to the submission schema. Include identity, method/provenance, validation, observables, formulas and a concise model-bounded interpretation. For `bounded_failure`, report the best completed evidence, identify the exact unmet validation or calculation, and use `null` only for observables that could not honestly be obtained, with an explanation in `availability_note`; do not fabricate placeholders. Do not claim experimental or biological validation from these calculations alone.
