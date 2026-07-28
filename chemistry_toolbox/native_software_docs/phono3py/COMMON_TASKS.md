---
software_id: phono3py
versions: ["installed phonons runtime"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["phono3py", "phono3py"]
inputs: ["unit cell", "displacement configuration", "force data", "optional Born charges"]
outputs: ["supercell displacement structures", "phono3py_disp.yaml", "fc2.hdf5", "fc3.hdf5", "kappa files"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# phono3py Common Tasks

## Appropriate calculation families
- **Third-Order Displacement Generation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Force-Set Creation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Phonon Lifetimes**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Thermal Conductivity**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `unit cell`
- `displacement configuration`
- `force data`
- `optional Born charges`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `supercell displacement structures`
- `phono3py_disp.yaml`
- `fc2.hdf5`
- `fc3.hdf5`
- `kappa files`

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
- `Summary of phono3py`
- `Thermal conductivity`

## Scientific convergence notes
Displacement generation is preparation only; conductivity requires complete force sets and convergence with supercell, mesh, cutoff, and solver settings.

## Version-specific caution
These mechanics target the installed `installed phonons runtime` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `phono3py`
- Synopsis: `phono3py [mode/options] [configuration files]`.
- Input mode: `arguments`.
- Required files: `mode-specific structure`, `displacement`, `force`, `and configuration files`.
- Output behavior: Writes fc2/fc3, collision, conductivity, and other selected files.
