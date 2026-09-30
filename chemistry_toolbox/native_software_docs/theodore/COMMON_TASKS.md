---
software_id: theodore
versions: ["installed TheoDORE runtime"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["TheoDORE", "theodore"]
inputs: ["dens_ana.in or subcommand input", "excited-state output", "orbital and density files"]
outputs: ["summary tables", "charge-transfer matrices", "NTO files", "spectra and plots"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# TheoDORE Common Tasks

## Appropriate calculation families
- **Transition-Density Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Charge-Transfer Numbers**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Natural Transition Orbitals**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Spectrum Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- No typed Action is registered for this software. Use the reviewed native command interface when the task needs this runtime.

## Minimum input responsibilities
- `dens_ana.in or subcommand input`
- `excited-state output`
- `orbital and density files`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `summary tables`
- `charge-transfer matrices`
- `NTO files`
- `spectra and plots`

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
- `TheoDORE analysis finished`
- `Analysis finished`

## Scientific convergence notes
Require all requested states and descriptors; verify state ordering, orbital basis, parser support, and upstream excited-state convergence.

## Version-specific caution
These mechanics target the installed `installed TheoDORE runtime` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `theodore_compat`
- Synopsis: `theodore_compat <analyze_tden|analyze_sden> [-f FILE]`.
- Input mode: `arguments`.
- Declared example inputs: `orbital`, `dens_ana.in`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Uses the explicit theodore-reader-1 adapter for known ORCA tables. Preserves native scientific analysis and missing-data errors; does not rerun calculations.

## Command: `theodore`
- Synopsis: `theodore <subcommand> [subcommand options]`.
- Input mode: `arguments`.
- Declared example inputs: `orbital`, `dens_ana.in`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes state-character tables, charge-transfer metrics, plots, and requested analysis files.
