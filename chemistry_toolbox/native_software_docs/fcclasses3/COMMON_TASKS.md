---
software_id: fcclasses3
versions: ["3.0.4"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["FCclasses3", "fcclasses3"]
inputs: ["FCclasses3 input file", "state files", "Hessian/normal-mode files", "dipole files"]
outputs: ["spectrum data", "rate constants", "convergence/diagnostic stdout", "requested intermediate files"]
last_smoke_tested: null
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# FCclasses3 Common Tasks

## Appropriate calculation families
- **Franck-Condon Spectra**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Herzberg-Teller Spectra**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Fluorescence**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Absorption**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Ecd**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Intersystem-Crossing Rates**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Internal-Conversion Rates**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- No typed Action is registered for this software. Use the reviewed native command interface when the task needs this runtime.

## Minimum input responsibilities
- `FCclasses3 input file`
- `state files`
- `Hessian/normal-mode files`
- `dipole files`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `spectrum data`
- `rate constants`
- `convergence/diagnostic stdout`
- `requested intermediate files`

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
- `FCclasses finished successfully`

## Scientific convergence notes
Process completion is not a scientific convergence test. Verify the selected property/model/dipole treatment, coordinate representation, temperature, broadening, state energies, mode counts, and all declared state/dipole/vibrational inputs.

## Version-specific caution
These mechanics target the installed `3.0.4` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `fcclasses3`
- Synopsis: `fcclasses3 input.fcc`.
- Input mode: `arguments`.
- Declared example inputs: `input.fcc`.
- Declared example outputs: `spectrum.dat`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 4096, 'gpu_count': 0}`.
- Output behavior: Writes requested spectra, rates, diagnostics, and intermediate files to the job directory according to the supplied FCclasses3 input.
- Caution: Property, model (FC/HT), TI/TD formulation, Cartesian/internal coordinates, temperature, broadening, state energies, and all referenced upstream files remain Agent-authored.
- Caution: The configured binary is user-supplied FCclasses3 3.0.4 built from the archived source tarball; this native interface does not infer or replace missing scientific inputs.
