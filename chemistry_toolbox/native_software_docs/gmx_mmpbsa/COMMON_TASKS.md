---
software_id: gmx_mmpbsa
versions: ["1.6.5"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["gmx_MMPBSA", "gmx mmpbsa"]
inputs: ["mmpbsa.in", "complex TPR", "index NDX", "trajectory XTC", "topology TOP and ITP includes"]
outputs: ["FINAL_RESULTS_MMPBSA.dat", "FINAL_RESULTS_MMPBSA.csv", "optional FINAL_DECOMP_MMPBSA.dat and CSV"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# gmx_MMPBSA Common Tasks

## Appropriate calculation families
- **Binding Free Energy**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Mm Gbsa**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Mm Pbsa**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Per-Frame Energy Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Residue Decomposition**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `calculate_end_state_binding_free_energy`: validated structured route through backend `gmx_mmpbsa`.
- `calculate_end_state_energy_decomposition`: validated structured route through backend `gmx_mmpbsa`.
- `summarize_end_state_free_energy_results`: validated structured route through backend `gmx_mmpbsa`.

## Minimum input responsibilities
- `mmpbsa.in`
- `complex TPR`
- `index NDX`
- `trajectory XTC`
- `topology TOP and ITP includes`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `FINAL_RESULTS_MMPBSA.dat`
- `FINAL_RESULTS_MMPBSA.csv`
- `optional FINAL_DECOMP_MMPBSA.dat and CSV`

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
- `Calculation completed`
- `Final Results`
- `exit code 0`

## Scientific convergence notes
Completion does not establish scientific convergence; frame selection, trajectory equilibration, solvent model, dielectric constants, entropy treatment, topology consistency, and uncertainty must be justified and tested.

## Version-specific caution
These mechanics target the installed `1.6.5` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `gmx_MMPBSA`
- Synopsis: `gmx_MMPBSA -O -i mmpbsa.in -cs complex.tpr -ci index.ndx -cg RECEPTOR_GROUP LIGAND_GROUP -ct trajectory.xtc -cp topology.top -o FINAL_RESULTS_MMPBSA.dat -eo FINAL_RESULTS_MMPBSA.csv -nogui`.
- Input mode: `arguments`.
- Declared example inputs: `mmpbsa.in`, `complex.tpr`, `index.ndx`, `trajectory.xtc`, `topology.top`, `toppar/forcefield.itp`.
- Declared example outputs: `FINAL_RESULTS_MMPBSA.dat`, `FINAL_RESULTS_MMPBSA.csv`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 4096, 'gpu_count': 0}`.
- Output behavior: Writes final summary and per-frame energy tables; explicit -do and -deo options additionally write residue-decomposition results.
- Caution: The solvent model, frame range, entropy treatment, receptor and ligand groups, decomposition selection, and topology are scientific inputs and must be explicit.
- Caution: Use only the configured isolated runtime; the shared AmberTools 26 environment is incompatible with this release.
