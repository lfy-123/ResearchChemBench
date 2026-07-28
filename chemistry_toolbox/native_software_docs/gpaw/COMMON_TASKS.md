---
software_id: gpaw
versions: ["installed GPAW runtime"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["GPAW", "gpaw"]
inputs: ["program.py", "optional structure and restart files", "GPAW datasets"]
outputs: ["program output", ".gpw restart", "trajectories", "property data"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# GPAW Common Tasks

## Appropriate calculation families
- **Molecular Energy**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Periodic Ground State**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Optimization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Band Structure**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Response Properties**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `program.py`
- `optional structure and restart files`
- `GPAW datasets`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `program output`
- `.gpw restart`
- `trajectories`
- `property data`

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
- `GPAW CLEANUP`
- `completed`

## Scientific convergence notes
Check electronic convergence, force or optimizer convergence, and requested output artifacts in the Python program.

## Version-specific caution
These mechanics target the installed `installed GPAW runtime` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `gpaw`
- Synopsis: `gpaw python program.py [program arguments]`.
- Input mode: `arguments`.
- Required files: `program.py`.
- Output behavior: Determined by the Agent-authored GPAW program; stdout and stderr are always captured.
- Caution: The script must specify calculator mode, basis/grid, exchange-correlation model, k-points, occupations, convergence, and outputs.
