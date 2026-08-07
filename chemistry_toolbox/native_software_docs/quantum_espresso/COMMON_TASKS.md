---
software_id: quantum_espresso
versions: ["7.5"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["Quantum ESPRESSO pw.x", "quantum espresso"]
inputs: ["input.in", "one pseudopotential per species"]
outputs: ["stdout.log", "prefix.save database", "charge density", "wavefunctions", "relaxed structure"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# Quantum ESPRESSO pw.x Common Tasks

## Appropriate calculation families
- **Scf**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Nscf**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Bands**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Relax**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Vc-Relax**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Molecular Dynamics**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `calculate_periodic_energy`: validated structured route through backend `quantum_espresso`.
- `calculate_periodic_forces`: validated structured route through backend `quantum_espresso`.
- `calculate_periodic_stress`: validated structured route through backend `quantum_espresso`.
- `relax_periodic_structure`: validated structured route through backend `quantum_espresso`.

## Minimum input responsibilities
- `input.in`
- `one pseudopotential per species`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `stdout.log`
- `prefix.save database`
- `charge density`
- `wavefunctions`
- `relaxed structure`

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
- `JOB DONE.`

## Scientific convergence notes
Require estimated scf accuracy or convergence achieved and the calculation-specific ionic, cell, band, or MD completion marker.

## Version-specific caution
These mechanics target the installed `7.5` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `pw.x`
- Synopsis: `pw.x -in input.in`.
- Input mode: `arguments`.
- Declared example inputs: `input.in`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes the main output to stdout and save/restart data under outdir.
- Caution: Calculation type, structure, pseudopotentials, cutoffs, k-points, occupations, convergence, and outdir must be explicit.
