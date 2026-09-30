# Scientific objective

Determine, by an independently chosen computational investigation, the optimized isolated-molecule electronic structure of neutral singlet 1-phenyl-5-(m-tolyl)-1H-tetrazole (C14H12N4). Report EHOMO, ELUMO, the HOMO-LUMO gap, ionization potential, electron affinity, chemical potential, electronegativity, hardness, softness and electrophilicity, and state what those quantities imply within this model boundary about electronic stability/reactivity.

# Public inputs and scientific boundaries

Use `data/inputs/molecule.json`, which uniquely defines the molecular connectivity by SMILES and supplies formula, neutral formal charge and singlet multiplicity. The system is one isolated molecule; exclude solvent, counterion, crystal packing, protein binding and biological efficacy. Select and justify your own computational method, basis, geometry strategy and analysis. No author route or target numerical value is supplied.

# Required scientific validation/investigation

Construct a chemically valid starting geometry, optimize it to a stationary point, and verify the final state and convergence. Perform a vibrational or equivalent curvature check to establish whether the state is a minimum and report imaginary modes. If more than one conformer or computational model is investigated, preserve candidate identities, explain deduplication and coverage, and justify the state used for the final observables. Completion requires one validated minimum, reproducible provenance, explicit descriptor formulas/sign conventions and every requested observable with units. Stop at that point, or give a bounded-failure report identifying the unmet validation and completed evidence.

# Deliverables

Submit `report/results.json` conforming to the submission schema. Include identity, method/provenance, validation, observables, formulas and a concise model-bounded interpretation. For `bounded_failure`, report the best completed evidence, identify the exact unmet validation or calculation, and use `null` only for observables that could not honestly be obtained, with an explanation in `availability_note`; do not fabricate placeholders. Do not claim experimental or biological validation from these calculations alone.
