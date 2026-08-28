# Scientific objective

Independently plan and execute a computational test of the authors' qualitative claim that the lowest-energy electronic transition of neutral 1bb is predominantly π→π* and is reasonably represented by an implicit-solvent TDDFT calculation. Determine the lowest-energy vertical transition in DCM and report its excitation energy, wavelength, oscillator strength, transition dipole (if available), and orbital/NTO character. The authors' proposed qualitative route is disclosed only as a hypothesis to test; no author software, functional, basis, geometry, ordered protocol, result direction or numerical answer is supplied.

# Public inputs and scientific boundaries

Use `data/inputs/system.json`. It uniquely defines 1bb by SMILES, formal charge 0 and singlet multiplicity 1. The environment is implicit DCM. The research object is one isolated molecule and one vertical electronic excitation from its optimized ground state. Explicit solvent, crystal packing, aggregates, counterions, vibronic envelopes and fluorescence dynamics are outside scope. You may generate conformers and choose a defensible electronic-structure method, but must disclose all choices and preserve the stated identity and state.

# Required scientific validation/investigation

Establish a ground-state geometry and verify its charge, multiplicity and convergence. Compute enough excited states to identify the lowest-energy transition by an explicit, reproducible selection rule; report state index and whether it is physically usable (for example, non-pathological oscillator strength). Validate the result with an independent check such as a second starting conformer, frequency/stationarity evidence, state/convergence diagnostics, or a justified alternative method. Report the validation evidence for the specific submitted structure and transition. Completion requires a converged geometry and an identified transition with reported observables or a fully documented bounded failure. Stop when the selected state is stable under the disclosed check, or when the available computational route cannot converge; do not claim completion from an unvalidated single output.

# Deliverables

Submit `report/results.json` conforming to the schema. Include method, software, structure identity, convergence/validation evidence, observables in stated units, orbital/NTO interpretation, conclusion and limitations. If computation fails, use the schema's failure branch and document what was attempted, what failed, and the scientifically meaningful limitation.
