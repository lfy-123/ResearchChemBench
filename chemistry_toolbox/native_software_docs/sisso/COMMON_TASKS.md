---
software_id: sisso
versions: ["3.5 (bc18cae)"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["SISSO", "sisso"]
inputs: ["SISSO.in", "train.dat", "optional SISSO.out and predict.dat for evaluation"]
outputs: ["SISSO.out", "Models", "SIS_subspaces", "predict_X.out", "predict_Y.out"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# SISSO Common Tasks

## Appropriate calculation families
- **Symbolic Regression**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Descriptor Discovery**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Sparse Model Selection**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Multitask Learning**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Classification**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Held-Out Prediction**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `discover_sparse_symbolic_descriptor`: validated structured route through backend `sisso`.
- `evaluate_sparse_symbolic_descriptor`: validated structured route through backend `sisso`.
- `summarize_sparse_symbolic_descriptor_results`: validated structured route through backend `sisso`.

## Minimum input responsibilities
- `SISSO.in`
- `train.dat`
- `optional SISSO.out and predict.dat for evaluation`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `SISSO.out`
- `Models`
- `SIS_subspaces`
- `predict_X.out`
- `predict_Y.out`

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
- `SISSO done successfully`
- `Have a nice day`
- `Prediction RMSE and MaxAE`

## Scientific convergence notes
A completed model is not evidence of stability. Converge feature complexity and SIS-subspace size, preserve a leakage-free split, test alternative splits or folds, and report held-out error and equation stability.

## Version-specific caution
These mechanics target the installed `3.5 (bc18cae)` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `SISSO`
- Synopsis: `SISSO > log`.
- Input mode: `fixed_files`.
- Declared example inputs: `SISSO.in`, `train.dat`.
- Declared example outputs: `SISSO.out`, `Models/data_top1/desc_D001.dat`, `SIS_subspaces/Uspace.expressions`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 4096, 'gpu_count': 0}`.
- Output behavior: Writes SISSO.out, Models, SIS_subspaces, CONTINUE state when applicable, and progress to stdout.
- Caution: Property type, task count, split size, feature units, operator set, complexity, SIS subspace, sparsifier, metric and model count are scientific inputs and must be explicit.
- Caution: The configured wrapper only sets an unlimited process stack before executing the unchanged SISSO binary.

## Command: `SISSO_predict`
- Synopsis: `SISSO_predict`.
- Input mode: `fixed_files`.
- Declared example inputs: `SISSO.out`, `predict.dat`, `SISSO_predict_para`.
- Declared example outputs: `predict_X.out`, `predict_Y.out`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes predict_X.out and predict_Y.out, including held-out descriptor coordinates, predictions, residuals, RMSE and maximum absolute error.
- Caution: The official predictor invokes bc; the configured runtime provides bc 1.07.1.
