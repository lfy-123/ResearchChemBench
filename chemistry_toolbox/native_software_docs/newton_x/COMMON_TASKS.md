---
software_id: newton_x
versions: ["26a"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["Newton-X", "newton x"]
inputs: ["control files", "initial conditions", "geometry", "electronic-structure interface files"]
outputs: ["TRAJ directories", "dynamics logs", "populations", "geometries", "test reports"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# Newton-X Common Tasks

## Appropriate calculation families
- **Initial-Condition Generation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Surface Hopping**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Spectrum Simulation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Trajectory Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Installation Tests**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- No typed Action is registered for this software. Use the reviewed native command interface when the task needs this runtime.

## Minimum input responsibilities
- `control files`
- `initial conditions`
- `geometry`
- `electronic-structure interface files`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `TRAJ directories`
- `dynamics logs`
- `populations`
- `geometries`
- `test reports`

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
- `Newton-X finished`
- `test passed`

## Scientific convergence notes
Require completed trajectories and successful electronic-structure steps; analyze energy conservation, state populations, and failed-trajectory counts.

## Version-specific caution
These mechanics target the installed `26a` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `nx_geninp`
- Synopsis: `nx_geninp [explicit generator options]`.
- Input mode: `arguments_or_stdin`.
- Declared example inputs: none declared.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes Newton-X control and initial-condition files.

## Command: `nx_moldyn`
- Synopsis: `nx_moldyn`.
- Input mode: `fixed_files`.
- Declared example inputs: none declared.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes trajectory, state, energy, hopping, and restart outputs in the job directory.

## Command: `nx_test`
- Synopsis: `nx_test <test_id> [options]`.
- Input mode: `arguments`.
- Declared example inputs: none declared.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes Newton-X test diagnostics to stdout and test directories.
