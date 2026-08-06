---
software_id: plumed
versions: ["installed MD runtime"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["PLUMED", "plumed"]
inputs: ["plumed.dat", "trajectory", "optional topology or masses"]
outputs: ["COLVAR", "HILLS", "grids", "stdout.log"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# PLUMED Common Tasks

## Appropriate calculation families
- **Trajectory Post-Processing**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Collective Variables**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Metadynamics Input Validation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Restraint Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `evaluate_collective_variables`: validated structured route through backend `plumed`.

## Minimum input responsibilities
- `plumed.dat`
- `trajectory`
- `optional topology or masses`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `COLVAR`
- `HILLS`
- `grids`
- `stdout.log`

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
- `PLUMED: Finished`
- `PLUMED: Timestep`

## Scientific convergence notes
Driver completion confirms evaluation only; enhanced-sampling convergence requires separate statistical analysis and is not inferred from exit code.

## Version-specific caution
These mechanics target the installed `installed MD runtime` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `plumed`
- Synopsis: `plumed <subcommand> [options]`.
- Input mode: `arguments`.
- Declared example inputs: `plumed.dat`, `trajectory.xtc`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Subcommand-specific outputs are written in the job directory.
- Caution: The first argument must be explicit, commonly driver, sum_hills, or info.
