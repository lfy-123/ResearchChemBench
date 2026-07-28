---
software_id: vmd
versions: ["1.9.3"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["VMD", "vmd"]
inputs: ["analysis.tcl", "referenced structures and trajectories"]
outputs: ["stdout.log", "user-defined tables", "structures", "images when rendering is configured"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# VMD Common Tasks

## Appropriate calculation families
- **Structure Inspection**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Trajectory Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Atom Selections**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Measurements**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Scripted Export**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `analysis.tcl`
- `referenced structures and trajectories`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `stdout.log`
- `user-defined tables`
- `structures`
- `images when rendering is configured`

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
- `Exiting normally.`

## Scientific convergence notes
VMD is analysis software; require the script's declared result files and validate selections, frame count, units, and periodic handling.

## Version-specific caution
These mechanics target the installed `1.9.3` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `vmd`
- Synopsis: `vmd -dispdev text -e analysis.tcl [structure/trajectory options]`.
- Input mode: `arguments`.
- Required files: `analysis.tcl and referenced structures/trajectories`.
- Output behavior: Writes Tcl-selected measurements and files plus console output.
