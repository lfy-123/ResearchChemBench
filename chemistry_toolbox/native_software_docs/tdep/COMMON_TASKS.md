---
software_id: tdep
versions: ["25.03 (d38f435)"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["TDEP", "tdep"]
inputs: ["unit-cell POSCAR", "supercell POSCAR", "packed simulation HDF5", "fitted force constants"]
outputs: ["effective force constants", "thermal configurations", "phonon dispersion and HDF5 data"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# TDEP Common Tasks

## Appropriate calculation families
- **Effective Force-Constant Fitting**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Canonical Thermal Sampling**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Phonon Dispersion**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Vibrational Thermodynamics**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Thermal Transport**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `fit_effective_force_constants`: validated structured route through backend `tdep`.
- `generate_thermal_displacement_configurations`: validated structured route through backend `tdep`.
- `calculate_temperature_dependent_phonon_dispersion`: validated structured route through backend `tdep`.

## Minimum input responsibilities
- `unit-cell POSCAR`
- `supercell POSCAR`
- `packed simulation HDF5`
- `fitted force constants`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `effective force constants`
- `thermal configurations`
- `phonon dispersion and HDF5 data`

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
- `Done in`
- `All done in`
- `exit code 0`

## Scientific convergence notes
Force-constant models require force-residual and cross-validation checks plus cutoff, trajectory-length, and temperature convergence; phonon completion alone does not validate the fitted model.

## Version-specific caution
These mechanics target the installed `25.03 (d38f435)` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `extract_forceconstants`
- Synopsis: `extract_forceconstants -rc2 CUTOFF [-rc3 CUTOFF] [options]`.
- Input mode: `fixed_files`.
- Declared example inputs: `infile.ucposcar`, `infile.ssposcar`, `infile.sim.hdf5`.
- Declared example outputs: `outfile.forceconstant`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 4096, 'gpu_count': 0}`.
- Output behavior: Writes fitted outfile.forceconstant files and diagnostics in the job directory.

## Command: `canonical_configuration`
- Synopsis: `canonical_configuration --nconf COUNT --temperature TEMPERATURE [model options]`.
- Input mode: `fixed_files`.
- Declared example inputs: `infile.ucposcar`, `infile.ssposcar`, `infile.forceconstant`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes contcar_confNNNN thermal configurations.

## Command: `phonon_dispersion_relations`
- Synopsis: `phonon_dispersion_relations --unit UNIT -nq POINTS [--readpath]`.
- Input mode: `fixed_files`.
- Declared example inputs: `infile.ucposcar`, `infile.forceconstant`.
- Declared example outputs: `outfile.dispersion_relations`, `outfile.dispersion_relations.hdf5`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 4096, 'gpu_count': 0}`.
- Output behavior: Writes text and HDF5 dispersion, group-velocity, activity, and requested DOS outputs.
