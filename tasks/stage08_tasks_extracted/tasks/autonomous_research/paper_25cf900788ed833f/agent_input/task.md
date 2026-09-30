# Scientific objective

Independently determine and interpret the lowest-energy vertical electronic transition of neutral 2,5-bis(4-methoxyphenyl)-4-(thiophen-2-yl)-1H-imidazole (1bb) in an implicit DCM environment. Report excitation energy, wavelength, oscillator strength, transition dipole (if available), and orbital/NTO character, and assess what the calculation can and cannot establish about the molecule's UV absorption.

# Public inputs and scientific boundaries

Use `data/inputs/system.json`. It uniquely defines the molecule by self-contained SMILES, formal charge 0 and singlet multiplicity 1. The environment is implicit DCM. The research object is one isolated molecule and one vertical excitation from an optimized ground state. Explicit solvent, crystal packing, aggregates, counterions, vibronic envelopes and fluorescence dynamics are outside scope. Choose and disclose a defensible computational model.

# Required scientific validation/investigation

Establish a ground-state geometry and verify its charge, multiplicity and convergence. Compute enough excited states to identify the lowest-energy transition by an explicit, reproducible selection rule; report state index and whether it is physically usable (for example, non-pathological oscillator strength). Validate the result with an independent check such as a second starting conformer, frequency/stationarity evidence, state/convergence diagnostics, or a justified alternative method. Report validation evidence for the specific submitted structure and transition. Completion requires a converged geometry and an identified transition with reported observables or a fully documented bounded failure. Stop when the selected state is stable under the disclosed check, or when the available computational route cannot converge; do not claim completion from an unvalidated single output.

# Deliverables

Submit `report/results.json` conforming to the schema. Include method, software, structure identity, convergence/validation evidence, observables in stated units, orbital/NTO interpretation, conclusion and limitations. If computation fails, use the schema's failure branch and document what was attempted, what failed, and the scientifically meaningful limitation.
