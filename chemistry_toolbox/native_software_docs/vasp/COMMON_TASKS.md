---
software_id: vasp
versions: ["6.3.2"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["VASP", "vasp"]
inputs: ["INCAR", "POSCAR", "POTCAR", "KPOINTS"]
outputs: ["OUTCAR", "vasprun.xml", "OSZICAR", "CONTCAR", "WAVECAR", "CHGCAR"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# VASP Common Tasks

## Appropriate calculation families
- **Single Point**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Relaxation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Cell Relaxation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Static Dos**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Bands**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Molecular Dynamics**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Frequency**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `calculate_periodic_energy`: validated structured route through backend `vasp`.
- `calculate_periodic_forces`: validated structured route through backend `vasp`.
- `calculate_periodic_stress`: validated structured route through backend `vasp`.
- `relax_periodic_structure`: validated structured route through backend `vasp`.

## Minimum input responsibilities
- `INCAR`
- `POSCAR`
- `POTCAR`
- `KPOINTS`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `OUTCAR`
- `vasprun.xml`
- `OSZICAR`
- `CONTCAR`
- `WAVECAR`
- `CHGCAR`

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
- `General timing and accounting informations for this job`

## Scientific convergence notes
Electronic EDIFF, ionic EDIFFG or required-accuracy, frequency completion, and MD step completion are distinct.

## Version-specific caution
These mechanics target the installed `6.3.2` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `vasp_std`
- Synopsis: `vasp_std`.
- Input mode: `fixed_files`.
- Declared example inputs: `INCAR`, `POSCAR`, `POTCAR`, `KPOINTS`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Reads standard fixed filenames and writes OUTCAR, OSZICAR, vasprun.xml, CONTCAR, WAVECAR, CHGCAR, and requested outputs.
- Caution: POTCAR assembly and every INCAR/KPOINTS setting must be explicit and license-compliant.
