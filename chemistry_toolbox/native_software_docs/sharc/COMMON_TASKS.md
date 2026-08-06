---
software_id: sharc
versions: ["SHARC4 source build+gfortran-restart-patch"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["SHARC", "sharc"]
inputs: ["SHARC input", "initial conditions", "interface resources", "overlap input and orbital files"]
outputs: ["trajectory directories", "output.dat", "output.lis", "restart files", "populations", "geometries", "overlap data"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# SHARC Common Tasks

## Appropriate calculation families
- **Initial Conditions**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Sharc Dynamics**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Wavefunction Overlap**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Trajectory Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `propagate_nonadiabatic_trajectory`: validated structured route through backend `sharc`.

## Minimum input responsibilities
- `SHARC input`
- `initial conditions`
- `interface resources`
- `overlap input and orbital files`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `trajectory directories`
- `output.dat`
- `output.lis`
- `restart files`
- `populations`
- `geometries`
- `overlap data`

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
- `Finishing SHARC dynamics run.`
- `Total runtime:`

## Scientific convergence notes
Require output.lis to reach the requested final time for every accepted trajectory, then inspect failed trajectories, energy conservation, state populations, hops, and independent seeds. The validated LVC ensemble contains three 30 fs trajectories and is an execution smoke, not a converged population study.

## Version-specific caution
These mechanics target the installed `SHARC4 source build+gfortran-restart-patch` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `sharc.x`
- Synopsis: `sharc.x input`.
- Input mode: `arguments`.
- Declared example inputs: `input`.
- Declared example outputs: `output.dat`, `output.lis`, `restart.ctrl`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes trajectory, hopping, energy, state, and restart files in the job directory.
- Caution: The typed trajectory Action copies a complete trajectory directory and verifies that output.lis reaches the requested final time.
- Caution: Production ensembles require independent random seeds and explicit failed-trajectory accounting.

## Command: `wfoverlap.x`
- Synopsis: `wfoverlap.x < overlap.inp`.
- Input mode: `stdin_file`.
- Declared example inputs: `overlap.inp`.
- Declared example outputs: `overlap.out`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes overlap diagnostics and matrices to stdout or requested files.
- Caution: The configured wfoverlap.x entry resolves to the installed ASCII executable.
