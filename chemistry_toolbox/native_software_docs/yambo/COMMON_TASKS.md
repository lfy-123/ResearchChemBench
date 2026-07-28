---
software_id: yambo
versions: ["5.3.0"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["Yambo", "yambo"]
inputs: ["compatible upstream save database", "SAVE directory", "input.in", "optional restart databases"]
outputs: ["SAVE database", "report", "output data files", "restart databases"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# Yambo Common Tasks

## Appropriate calculation families
- **Database Conversion**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Gw**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Bethe-Salpeter Equation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Optical Spectra**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Real-Time Propagation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `compatible upstream save database`
- `SAVE directory`
- `input.in`
- `optional restart databases`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `SAVE database`
- `report`
- `output data files`
- `restart databases`

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
- `Game Over & Game summary`
- `Timing Overview`

## Scientific convergence notes
p2y success only creates a database. GW, BSE, and spectra require task completion and convergence with bands, cutoffs, k points, and frequency grids.

## Version-specific caution
These mechanics target the installed `5.3.0` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `p2y`
- Synopsis: `p2y [conversion options]`.
- Input mode: `arguments`.
- Required files: `compatible upstream electronic-structure save database`.
- Output behavior: Creates the Yambo SAVE database and conversion log.

## Command: `yambo`
- Synopsis: `yambo -F input.in -J job_name [explicit options]`.
- Input mode: `arguments`.
- Required files: `input.in`, `SAVE database`, `and required restart databases`.
- Output behavior: Writes report, database, quasiparticle, response, or excitonic files selected by input.in.
