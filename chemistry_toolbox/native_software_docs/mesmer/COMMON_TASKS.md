---
software_id: mesmer
versions: ["7.1"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["MESMER", "mesmer"]
inputs: ["input.xml"]
outputs: ["output.xml", "console log", "rate tables", "optional grain and diagnostic files"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# MESMER Common Tasks

## Appropriate calculation families
- **Pressure-Dependent Rates**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Phenomenological Kinetics**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Fitting**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Sensitivity Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `solve_master_equation`: validated structured route through backend `mesmer`.

## Minimum input responsibilities
- `input.xml`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `output.xml`
- `console log`
- `rate tables`
- `optional grain and diagnostic files`

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
- `MESMER calculation complete`
- `Calculation complete`

## Scientific convergence notes
Require successful model parsing and the requested rate or fit results; inspect grain, energy-transfer, and fitting diagnostics.

## Version-specific caution
These mechanics target the installed `7.1` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `mesmer`
- Synopsis: `mesmer input.xml -o output.xml [options]`.
- Input mode: `arguments`.
- Declared example inputs: `input.xml`.
- Declared example outputs: `output.xml`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes audit/result XML and text diagnostics.
