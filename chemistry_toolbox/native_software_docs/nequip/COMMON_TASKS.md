---
software_id: nequip
versions: ["installed NequIP runtime"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["NequIP", "nequip"]
inputs: ["config.yaml and datasets for training", "or an explicitly selected registered checkpoint for inference"]
outputs: ["training log", "checkpoints", "metrics", "packaged model"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# NequIP Common Tasks

## Appropriate calculation families
- **Training**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Validation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Model Packaging**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Inference**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Lammps Deployment**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `config.yaml and datasets for training`
- `or an explicitly selected registered checkpoint for inference`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `training log`
- `checkpoints`
- `metrics`
- `packaged model`

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
- `Training complete`
- `best_model.pth`

## Scientific convergence notes
Training completion does not establish scientific validity; require held-out energy and force errors, learning curves, and domain coverage.

## Version-specific caution
These mechanics target the installed `installed NequIP runtime` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `nequip-train`
- Synopsis: `nequip-train -cn <config_basename_without_yaml> [Hydra overrides]`.
- Input mode: `arguments`.
- Declared example inputs: `config.yaml`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes training logs and checkpoints under paths selected in config.yaml.
- Caution: The installed NequIP 0.19 entry point uses Hydra with the job directory as its config search path; stage config.yaml and pass -cn config rather than a positional YAML path.
