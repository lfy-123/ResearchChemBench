---
software_id: amber_pmemd
versions: ["26"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["Amber PMEMD", "amber pmemd"]
inputs: ["mdin", "topology.prmtop", "input.rst7"]
outputs: ["mdout", "output.rst7", "trajectory.nc", "mdinfo"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# Amber PMEMD Common Tasks

## Appropriate calculation families
- **Energy Minimization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Heating**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Nvt Dynamics**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Npt Dynamics**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Restart Continuation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `mdin`
- `topology.prmtop`
- `input.rst7`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `mdout`
- `output.rst7`
- `trajectory.nc`
- `mdinfo`

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
- `Final Performance Info`
- `5.  TIMINGS`

## Scientific convergence notes
Minimization requires the requested gradient or cycle criterion; MD requires the intended number of steps and stable thermodynamic diagnostics.

## Version-specific caution
These mechanics target the installed `26` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `pmemd`
- Synopsis: `pmemd -O -i mdin -o mdout -p topology.prmtop -c input.rst7 -r output.rst7 -x trajectory.nc`.
- Input mode: `arguments`.
- Required files: `mdin`, `topology.prmtop`, `input.rst7`.
- Output behavior: Writes paths explicitly supplied by -o, -r, -x, and related options.

## Command: `pmemd.MPI`
- Synopsis: `pmemd.MPI -O -i mdin -o mdout -p topology.prmtop -c input.rst7 -r output.rst7 -x trajectory.nc`.
- Input mode: `arguments`.
- Required files: `mdin`, `topology.prmtop`, `input.rst7`.
- Output behavior: Writes paths explicitly supplied by PMEMD output options.
- Caution: MPI rank allocation belongs to the deployment scheduler. The generic mpirun launcher is intentionally not exposed as a native command.

## Command: `mpirun`
- Synopsis: `mpirun <program> [arguments]`.
- Input mode: `arguments`.
- Required files: none declared.
- Output behavior: Not publicly executable because it is a general process launcher.
