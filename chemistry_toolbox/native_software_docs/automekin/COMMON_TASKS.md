---
software_id: automekin
versions: ["AutoMeKin2021 revision 1142"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["AutoMeKin", "automekin"]
inputs: ["AutoMeKin control file", "starting structure", "method-specific resources"]
outputs: ["reaction network", "transition-state structures", "product structures", "component logs"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# AutoMeKin Common Tasks

## Appropriate calculation families
- **Trajectory Sampling**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Transition-State Search**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Reaction-Network Construction**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Mopac Component Jobs**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `AutoMeKin control file`
- `starting structure`
- `method-specific resources`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `reaction network`
- `transition-state structures`
- `product structures`
- `component logs`

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
- `normal termination`
- `ended normally`

## Scientific convergence notes
The workflow must finish and every retained stationary point must have the expected frequency character and connectivity.

## Version-specific caution
These mechanics target the installed `AutoMeKin2021 revision 1142` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `amk.sh`
- Synopsis: `amk.sh <Agent-prepared AutoMeKin input> [explicit options]`.
- Input mode: `arguments`.
- Required files: `AutoMeKin control/structure inputs and referenced resources`.
- Output behavior: Writes reaction-discovery intermediates, trajectories, candidates, and logs in the job directory.
- Caution: This invokes the native program only; it does not prewire Gaussian, Qcore, or another electronic-structure engine.

## Command: `mopac`
- Synopsis: `mopac input.mop`.
- Input mode: `arguments`.
- Required files: `input.mop`.
- Output behavior: Writes input.out, input.arc, and method-specific MOPAC files.

## Command: `bbfs.exe`
- Synopsis: `bbfs.exe [AutoMeKin component arguments]`.
- Input mode: `arguments`.
- Required files: `AutoMeKin component-specific inputs`.
- Output behavior: Writes component-specific search data to the job directory/stdout.
- Caution: Use only when the cached AutoMeKin documentation identifies bbfs.exe as the required native component for the Agent's planned step.
