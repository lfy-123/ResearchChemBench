---
software_id: vina
versions: ["f458505-mod"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["AutoDock Vina", "vina"]
inputs: ["receptor.pdbqt", "ligand.pdbqt", "box center and size"]
outputs: ["poses.pdbqt", "docking log", "affinity table"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# AutoDock Vina Common Tasks

## Appropriate calculation families
- **Docking**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Score-Only**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Local Optimization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Batch Docking**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `receptor.pdbqt`
- `ligand.pdbqt`
- `box center and size`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `poses.pdbqt`
- `docking log`
- `affinity table`

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
- `Writing output`
- `mode | affinity`

## Scientific convergence notes
Validate pose count, search-box coverage, protonation, atom types, torsions, and score interpretation; exit code alone is insufficient.

## Version-specific caution
These mechanics target the installed `f458505-mod` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `vina`
- Synopsis: `vina --receptor receptor.pdbqt --ligand ligand.pdbqt --center_x X --center_y Y --center_z Z --size_x X --size_y Y --size_z Z --out poses.pdbqt [options]`.
- Input mode: `arguments`.
- Declared example inputs: `receptor.pdbqt`, `ligand.pdbqt`.
- Declared example outputs: `poses.pdbqt`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes poses to --out and scores/logs to stdout or --log.
