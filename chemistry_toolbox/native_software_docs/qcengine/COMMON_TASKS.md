---
software_id: qcengine
versions: ["0.50.0"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["QCEngine", "qcengine"]
inputs: ["QCSchema JSON", "selected program name"]
outputs: ["QCSchema result JSON", "structured error record", "provenance"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# QCEngine Common Tasks

## Appropriate calculation families
- **Single Computation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Gradient**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Hessian**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Optimization Procedure**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Program Discovery**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `QCSchema JSON`
- `selected program name`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `QCSchema result JSON`
- `structured error record`
- `provenance`

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
- `success true`

## Scientific convergence notes
Require result.success and inspect backend-specific convergence and returned properties; QCEngine transport success alone is insufficient.

## Version-specific caution
These mechanics target the installed `0.50.0` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `qcengine`
- Synopsis: `qcengine run <program> input.json [CLI options]`.
- Input mode: `arguments`.
- Required files: `QCSchema AtomicInput or procedure input JSON`.
- Output behavior: Writes the QCEngine result record to stdout or the explicitly selected CLI output.
- Caution: The program name, model chemistry, driver, molecule, keywords, protocols, and resources must be present explicitly in the command/input.
