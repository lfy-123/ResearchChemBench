---
software_id: geometric
versions: ["installed Python package"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["geomeTRIC", "geometric"]
inputs: ["input geometry", "engine-specific input or configuration"]
outputs: ["optimized geometry", "optimization trajectory", "log", "constraints summary"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# geomeTRIC Common Tasks

## Appropriate calculation families
- **Minimum Optimization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Constrained Optimization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Transition-State Optimization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Scan**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `input geometry`
- `engine-specific input or configuration`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `optimized geometry`
- `optimization trajectory`
- `log`
- `constraints summary`

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
- `Converged!`
- `Geometry optimization converged`

## Scientific convergence notes
Require the geomeTRIC convergence criteria and verify the stationary-point character with a separate Hessian when scientifically needed.

## Version-specific caution
These mechanics target the installed `installed Python package` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `geometric-optimize`
- Synopsis: `geometric-optimize [optimizer options] input.xyz --engine <engine>`.
- Input mode: `arguments`.
- Required files: `input geometry and engine-specific files`.
- Output behavior: Writes optimization logs, trajectory, and optimized coordinates in the job directory.
- Caution: Engine, constraints, coordinate system, convergence thresholds, and engine method are not selected by the runner.
