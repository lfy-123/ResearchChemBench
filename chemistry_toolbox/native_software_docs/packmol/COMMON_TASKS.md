---
software_id: packmol
versions: ["installed build"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["Packmol", "packmol"]
inputs: ["packmol.inp", "one coordinate template per structure block"]
outputs: ["packed.xyz or another requested output", "stdout.log"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# Packmol Common Tasks

## Appropriate calculation families
- **Solvent Boxes**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Mixtures**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Interfaces**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Spherical Droplets**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Fixed-Solute Packing**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `packmol.inp`
- `one coordinate template per structure block`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `packed.xyz or another requested output`
- `stdout.log`

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
- `Success!`
- `Final objective function value`

## Scientific convergence notes
Require Success and validate molecule counts, box dimensions, minimum distances, and absence of severe overlaps.

## Version-specific caution
These mechanics target the installed `installed build` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `packmol`
- Synopsis: `packmol < packmol.inp`.
- Input mode: `stdin_file`.
- Required files: `packmol.inp`, `all structure files referenced by packmol.inp`.
- Output behavior: Writes the output filename declared inside packmol.inp and progress to stdout.
- Caution: Set stdin_file to the staged target packmol.inp; filenames inside it must match staged targets.
