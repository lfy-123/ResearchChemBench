---
software_id: pdb_tools
versions: ["installed Python package"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["pdb-tools", "pdb tools"]
inputs: ["input.pdb"]
outputs: ["stdout PDB stream or redirected PDB file"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# pdb-tools Common Tasks

## Appropriate calculation families
- **Chain Selection**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Residue Renumbering**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Record Tidying**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Atom And Residue Filtering**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `select_structure_subset`: validated structured route through backend `pdb_tools`.
- `renumber_biomolecular_structure`: validated structured route through backend `pdb_tools`.
- `normalize_pdb_records`: validated structured route through backend `pdb_tools`.

## Minimum input responsibilities
- `input.pdb`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `stdout PDB stream or redirected PDB file`

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
- `exit code 0`

## Scientific convergence notes
Validate record count, selected chains, residue numbering, MODEL boundaries, and structural meaning after every transformation.

## Version-specific caution
These mechanics target the installed `installed Python package` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `pdb_selchain`
- Synopsis: `pdb_selchain -<chain_ids> input.pdb`.
- Input mode: `arguments`.
- Declared example inputs: `input.pdb`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes transformed PDB text to stdout; capture stdout.log as the result.

## Command: `pdb_reres`
- Synopsis: `pdb_reres -<first_residue_number> input.pdb`.
- Input mode: `arguments`.
- Declared example inputs: `input.pdb`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes transformed PDB text to stdout.

## Command: `pdb_tidy`
- Synopsis: `pdb_tidy input.pdb`.
- Input mode: `arguments`.
- Declared example inputs: `input.pdb`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes normalized PDB text to stdout.
