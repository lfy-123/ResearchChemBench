---
software_id: kinbot
versions: ["2.2.2+local-nwchem-patch"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["KinBot", "kinbot"]
inputs: ["input.json", "starting structure", "templates", "selected QM backend configuration"]
outputs: ["KinBot database", "structures", "quantum-chemistry inputs and logs", "PES files"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# KinBot Common Tasks

## Appropriate calculation families
- **Reaction Search**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Conformer Search**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Transition-State Validation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Pes Assembly**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `explore_reaction_network`: validated structured route through backend `kinbot`.

## Minimum input responsibilities
- `input.json`
- `starting structure`
- `templates`
- `selected QM backend configuration`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `KinBot database`
- `structures`
- `quantum-chemistry inputs and logs`
- `PES files`

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
- `PES search done!`
- `KinBot done!`
- `done`

## Scientific convergence notes
Require the full PES completion marker, completed local NWChem children, no child initial-optimization errors, an explicit reaction-search marker when requested, normal database records, intended frequency threshold, validated transition states, and correct reactant-product connectivity. A chemids file or the outer PES marker alone is not completion.

## Version-specific caution
These mechanics target the installed `2.2.2+local-nwchem-patch` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `kinbot`
- Synopsis: `kinbot input.json`.
- Input mode: `arguments`.
- Declared example inputs: `input.json`.
- Declared example outputs: `kinbot.log`, `kinbot.db`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes KinBot logs, geometries, reaction candidates, and database files.
- Caution: The local NWChem route uses the tracked KinBot compatibility patch and KINBOT_NWCHEM_COMMAND; validate one well optimization before a broad reaction search.

## Command: `pes`
- Synopsis: `pes input.json`.
- Input mode: `arguments`.
- Declared example inputs: `input.json`.
- Declared example outputs: `pes.log`, `chemids`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes PES search and postprocessing outputs in the job directory.
- Caution: A completed search must contain PES search done!, every child must avoid initial-optimization errors, and reaction_search=1 children must contain Starting reaction search...; the outer marker or creation of chemids alone is insufficient.
