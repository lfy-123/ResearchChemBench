---
software_id: gromacs
versions: ["installed 2026-era build"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["GROMACS", "gromacs"]
inputs: ["mdp", "topology.top", "coordinates.gro", "optional index and checkpoint"]
outputs: ["run.tpr", "run.log", "trajectory.xtc", "energy.edr", "final.gro", "checkpoint.cpt"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# GROMACS Common Tasks

## Appropriate calculation families
- **Energy Minimization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Nvt**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Npt**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Production Md**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Trajectory Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `mdp`
- `topology.top`
- `coordinates.gro`
- `optional index and checkpoint`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `run.tpr`
- `run.log`
- `trajectory.xtc`
- `energy.edr`
- `final.gro`
- `checkpoint.cpt`

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
- `Finished mdrun`
- `Writing final coordinates`

## Scientific convergence notes
grompp success only validates preprocessing. For minimization inspect Fmax; for MD require completed steps and stable diagnostics.

## Version-specific caution
These mechanics target the installed `installed 2026-era build` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `gmx`
- Synopsis: `gmx <subcommand> [subcommand options]`.
- Input mode: `arguments`.
- Declared example inputs: none declared.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 4, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Determined by the selected GROMACS subcommand; stdout and stderr are captured.
- Caution: The first argument must be explicit, for example grompp, mdrun, energy, rms, rdf, or trjconv.
- Caution: Interactive group selections should be supplied through an explicit stdin_file.
