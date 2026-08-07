---
software_id: pyfrag
versions: ["2019.02 (v1.0.0 af2a122d)"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["PyFrag", "pyfrag"]
inputs: ["PyFrag input specification", "AMV or multi-XYZ reaction path", "explicit fragment partitions and reference energies", "ORCA method keywords"]
outputs: ["fragment_energies.txt", "fragment ORCA outputs", "structured activation-strain summary and validation"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# PyFrag Common Tasks

## Appropriate calculation families
- **Activation Strain Model**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Distortion Interaction Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Reaction Path Energy Decomposition**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Fragment Strain Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `analyze_activation_strain_profile`: validated structured route through backend `pyfrag`.
- `summarize_activation_strain_profile`: validated structured route through backend `pyfrag`.
- `validate_activation_strain_profile`: validated structured route through backend `pyfrag`.

## Minimum input responsibilities
- `PyFrag input specification`
- `AMV or multi-XYZ reaction path`
- `explicit fragment partitions and reference energies`
- `ORCA method keywords`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `fragment_energies.txt`
- `fragment ORCA outputs`
- `structured activation-strain summary and validation`

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
- `PyFrag finished. Have a nice day`
- `ORCA TERMINATED NORMALLY`
- `exit code 0`

## Scientific convergence notes
PyFrag completion does not validate the underlying path, fragment definition, reference states, electronic-structure method, basis-set convergence, spin state or path sampling. Every ORCA child calculation must terminate normally and the decomposition identity must close within an explicit tolerance.

## Version-specific caution
These mechanics target the installed `2019.02 (v1.0.0 af2a122d)` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `pyfrag-orca`
- Synopsis: `pyfrag-orca pyfrag.inp scratch`.
- Input mode: `arguments`.
- Declared example inputs: `pyfrag.inp`, `reaction_path.amv`.
- Declared example outputs: `fragment_energies.txt`, `fragmentfiles/fragment_1_0000.out`, `fragmentfiles/fragment_2_0000.out`, `fragmentfiles/complex_0000.out`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 4096, 'gpu_count': 0}`.
- Output behavior: Runs one complex and two isolated-fragment ORCA single points per path frame and writes fragment_energies.txt plus native outputs under fragmentfiles.
- Caution: Fragment membership, reference fragment energies, charge, multiplicity, ORCA simple keywords, path type and printed reaction coordinate are scientific inputs and must be explicit.
- Caution: The public Action accepts AMV or multi-XYZ and writes a normalized AMV file after enforcing fixed atom order across all frames.
- Caution: PyFrag path execution is serial; ORCA registration and download are separate from the LGPL-3.0 PyFrag source.
- Caution: Apply the tracked compatibility patch to exact v1.0.0 commit af2a122d after migration.
