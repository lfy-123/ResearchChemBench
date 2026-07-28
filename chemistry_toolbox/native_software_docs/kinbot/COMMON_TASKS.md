---
software_id: kinbot
versions: ["installed KinBot runtime"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["KinBot", "kinbot"]
inputs: ["input.json", "starting structure", "templates", "selected QM backend configuration"]
outputs: ["KinBot database", "structures", "quantum-chemistry inputs and logs", "PES files"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# KinBot Common Tasks

## Appropriate calculation families
- **Reaction Search**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Conformer Search**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Transition-State Validation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Pes Assembly**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `input.json`
- `starting structure`
- `templates`
- `selected QM backend configuration`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `KinBot database`
- `structures`
- `quantum-chemistry inputs and logs`
- `PES files`

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
- `KinBot finished`
- `PES generation finished`

## Scientific convergence notes
Require completed backend jobs, validated transition states, expected imaginary modes, and correct reactant-product connectivity.

## Version-specific caution
These mechanics target the installed `installed KinBot runtime` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `kinbot`
- Synopsis: `kinbot input.json`.
- Input mode: `arguments`.
- Required files: `input.json and referenced structures/templates`.
- Output behavior: Writes KinBot logs, geometries, reaction candidates, and database files.

## Command: `pes`
- Synopsis: `pes input.json`.
- Input mode: `arguments`.
- Required files: `input.json and referenced KinBot/PES files`.
- Output behavior: Writes PES search and postprocessing outputs in the job directory.
