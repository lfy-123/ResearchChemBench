---
software_id: bagel
versions: ["1.2.2-3ubuntu1 (bfceffea)"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["BAGEL", "bagel"]
inputs: ["BAGEL JSON input with geometry basis active space state manifold method and derivative target"]
outputs: ["state energies", "convergence diagnostics", "nuclear gradients", "nonadiabatic coupling vectors"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# BAGEL Common Tasks

## Appropriate calculation families
- **State-Averaged Casscf**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Xms-Caspt2**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Analytical Nuclear Gradients**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Nonadiabatic Couplings**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `calculate_multireference_state_energies`: validated structured route through backend `bagel`.
- `calculate_multireference_nuclear_gradient`: validated structured route through backend `bagel`.
- `calculate_nonadiabatic_coupling_vector`: validated structured route through backend `bagel`.

## Minimum input responsibilities
- `BAGEL JSON input with geometry basis active space state manifold method and derivative target`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `state energies`
- `convergence diagnostics`
- `nuclear gradients`
- `nonadiabatic coupling vectors`

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
- `METHOD CASSCF`
- `METHOD FORCE`
- `METHOD NACME`
- `Second-order optimization converged`

## Scientific convergence notes
Process completion is insufficient. Require convergence of the selected multireference calculation, verify the active space and state ordering, and preserve explicit target-state and basis choices.

## Version-specific caution
These mechanics target the installed `1.2.2-3ubuntu1 (bfceffea)` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `BAGEL`
- Synopsis: `BAGEL input.json`.
- Input mode: `arguments`.
- Declared example inputs: `input.json`.
- Declared example outputs: stdout/stderr or task-dependent outputs.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 4096, 'gpu_count': 0}`.
- Output behavior: Writes state energies, analytical gradients, nonadiabatic couplings and convergence diagnostics to stdout according to the supplied JSON method blocks.
- Caution: Geometry, charge, spin, orbital basis, density-fitting basis, closed and active spaces, state count, target states, derivative type and convergence thresholds must be explicit.
- Caution: The configured wrapper resolves BAGEL basis-set names to immutable files in the cached Ubuntu runtime; it does not choose or replace a basis.
- Caution: For MPI execution use the configured bagel-mpirun wrapper with an explicit rank count and the cached raw BAGEL executable.
