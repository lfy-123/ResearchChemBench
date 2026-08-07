---
software_id: vaspkit
versions: ["1.5.1"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["VASPKIT", "vaspkit"]
inputs: ["POSCAR or CONTCAR and task-specific INCAR EIGENVAL DOSCAR OUTCAR PROCAR CHGCAR or LOCPOT files"]
outputs: ["task-specific KPOINTS structures tables grids plots and stdout summaries"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# VASPKIT Common Tasks

## Appropriate calculation families
- **K-Point Meshes**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Crystal Symmetry**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Band Gaps**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Bands**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Density Of States**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Charge And Potential Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `analyze_crystal_symmetry`: validated structured route through backend `vaspkit`.
- `generate_vasp_kpoint_mesh`: validated structured route through backend `vaspkit`.
- `extract_vasp_band_gap`: validated structured route through backend `vaspkit`.

## Minimum input responsibilities
- `POSCAR or CONTCAR and task-specific INCAR EIGENVAL DOSCAR OUTCAR PROCAR CHGCAR or LOCPOT files`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `task-specific KPOINTS structures tables grids plots and stdout summaries`

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
- `VASPKIT Standard Edition 1.5.1`
- `Summary`
- `exit code 0`

## Scientific convergence notes
Post-processing cannot establish convergence of the underlying VASP calculation. K-point density, cutoff, cell, electronic minimization, smearing, bands and energy references must be checked from the supplied calculation record.

## Version-specific caution
These mechanics target the installed `1.5.1` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `vaspkit`
- Synopsis: `vaspkit -task TASK -file POSCAR [explicit options]`.
- Input mode: `arguments`.
- Declared example inputs: `POSCAR`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 1024, 'gpu_count': 0}`.
- Output behavior: Writes task-specific KPOINTS, structure, table, or plot data and prints a structured summary to stdout.
- Caution: Task number, files, tolerances, reciprocal resolution, centering, energy reference, atom/orbital selection and every other scientific option must be explicit.
- Caution: The local package is nonredistributable; migration requires a fresh official download.
- Caution: POTCAR files are licensed VASP data and are never included or selected automatically.
