---
software_id: siesta
versions: ["5.4.2"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["SIESTA", "siesta"]
inputs: ["input.fdf", "pseudopotential files", "optional included structure and basis files"]
outputs: ["stdout.log", ".XV", ".DM", ".WFSX", ".bands", ".DOS and trajectory files"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# SIESTA Common Tasks

## Appropriate calculation families
- **Single Point**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Geometry Optimization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Molecular Dynamics**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Bands**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Dos**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Transport Preparation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `input.fdf`
- `pseudopotential files`
- `optional included structure and basis files`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `stdout.log`
- `.XV`
- `.DM`
- `.WFSX`
- `.bands`
- `.DOS and trajectory files`

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
- `Job completed`
- `{'siesta': 'Final energy'}`

## Scientific convergence notes
Require SCF convergence and the requested geometry, MD, band, or property completion marker.

## Version-specific caution
These mechanics target the installed `5.4.2` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `siesta`
- Synopsis: `siesta < input.fdf`.
- Input mode: `stdin_file`.
- Required files: `input.fdf`, `pseudopotentials and structure files referenced by it`.
- Output behavior: Writes primary output to stdout and SIESTA result/restart files in the job directory.
