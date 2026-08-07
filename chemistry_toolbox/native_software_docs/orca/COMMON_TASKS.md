---
software_id: orca
versions: ["6.1.1"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["ORCA", "orca"]
inputs: ["input.inp", "optional external XYZ", "basis", "point charges", "or restart files"]
outputs: ["stdout.log", ".gbw", ".xyz", ".hess", ".densities", "property files"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# ORCA Common Tasks

## Appropriate calculation families
- **Single Point**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Optimization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Frequency**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Transition State**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Irc**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Excited States**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Correlated Density**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `calculate_energy`: validated structured route through backend `orca`.
- `calculate_forces`: validated structured route through backend `orca`.
- `calculate_hessian`: validated structured route through backend `orca`.
- `optimize_geometry`: validated structured route through backend `orca`.
- `calculate_dipole_moment`: validated structured route through backend `orca`.
- `calculate_atomic_charges`: validated structured route through backend `orca`.
- `calculate_orbitals`: validated structured route through backend `orca`.
- `calculate_bond_orders`: validated structured route through backend `orca`.
- `calculate_excited_states`: validated structured route through backend `orca`.
- `calculate_correlated_electron_density`: validated structured route through backend `orca`.
- `export_electron_density_grid`: validated structured route through backend `orca`.

## Minimum input responsibilities
- `input.inp`
- `optional external XYZ`
- `basis`
- `point charges`
- `or restart files`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `stdout.log`
- `.gbw`
- `.xyz`
- `.hess`
- `.densities`
- `property files`

Only collect outputs produced by the same job or by explicitly linked parent jobs. Do not combine checkpoints, force constants, trajectories, pseudopotentials, wavefunctions, or databases from unrelated calculations.

## State-specific validation
| State | Required evidence | Not sufficient |
|---|---|---|
| Process completed | Exit code zero and Supervisor did not cancel or time out | A submitted job ID |
| Software normal | Program-specific normal marker and absence of fatal diagnostics | Exit code zero alone |
| Electronic convergence | Requested SCF or electronic tolerance reached | A printed energy from an unconverged cycle |
| Geometry convergence | Optimization stopping criteria reached for the requested degrees of freedom | SCF convergence at the last geometry |
| Frequency completion | Hessian/frequencies finished and modes were parsed | Optimization completion alone |
| Transition-state candidate | Optimization converged and exactly the intended imaginary mode was verified | One negative number without mode inspection |
| Dynamics completion | Requested steps completed with acceptable stability diagnostics | Creation of a partial trajectory |
| Artifact validity | Required files exist, are non-empty, and can be parsed | Files with expected names only |

## Software-specific end markers
- `ORCA TERMINATED NORMALLY`

## Scientific convergence notes
SCF CONVERGED, geometry convergence, frequency completion, imaginary-mode count, and IRC completion are separate checks.

## Version-specific caution
These mechanics target the installed `6.1.1` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `orca`
- Synopsis: `orca input.inp`.
- Input mode: `arguments`.
- Declared example inputs: `input.inp`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes the primary output to stdout and ORCA property/restart files in the job directory.
- Caution: Method, basis, charge, multiplicity, calculation keywords, parallelism, memory, and convergence must be explicit in input.inp.
- Caution: ORCA should be launched by its resolved absolute path; the execution layer does this without changing the input.
- Caution: Use this asynchronous native-job contract when the Agent must author an ORCA input deck directly; it uses the same evaluator-controlled compute timeout as managed compute Actions and requires stable bulk supervision with wait_execution_jobs.
