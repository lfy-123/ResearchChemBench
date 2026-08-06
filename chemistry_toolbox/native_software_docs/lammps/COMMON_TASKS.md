---
software_id: lammps
versions: ["installed build"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["LAMMPS", "lammps"]
inputs: ["input.lammps", "optional data file", "potential files", "included scripts"]
outputs: ["log.lammps", "dump files", "restart files", "user-defined tables"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# LAMMPS Common Tasks

## Appropriate calculation families
- **Energy Minimization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Molecular Dynamics**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Monte Carlo-Assisted Workflows**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Materials Deformation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Trajectory Generation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `minimize_system_energy`: validated structured route through backend `lammps`.
- `propagate_dynamics`: validated structured route through backend `lammps`.

## Minimum input responsibilities
- `input.lammps`
- `optional data file`
- `potential files`
- `included scripts`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `log.lammps`
- `dump files`
- `restart files`
- `user-defined tables`

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
- `Total wall time`
- `Loop time of`

## Scientific convergence notes
Minimization requires the requested force and energy tolerances; dynamics requires the intended run length and physically stable thermo output.

## Version-specific caution
These mechanics target the installed `installed build` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `lmp`
- Synopsis: `lmp -in input.lammps [command-line variables]`.
- Input mode: `arguments`.
- Declared example inputs: `input.lammps`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes log.lammps plus dumps/restarts selected in the input script.
