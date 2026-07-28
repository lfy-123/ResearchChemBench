---
software_id: vesta
versions: ["3.90.5a"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["VESTA", "vesta"]
inputs: ["CIF", "POSCAR", "cube", "density", "or VESTA project file"]
outputs: ["interactive session", "images", "converted structures", "VESTA project"]
last_smoke_tested: "2026-07-28"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml
---
# VESTA Common Tasks

## Appropriate calculation families
- **Structure Visualization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Density Visualization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Project Export**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Format Conversion**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Minimum input responsibilities
- `CIF`
- `POSCAR`
- `cube`
- `density`
- `or VESTA project file`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `interactive session`
- `images`
- `converted structures`
- `VESTA project`

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
- `GUI opened`
- `export completed`

## Scientific convergence notes
VESTA is not a scientific solver; validate that the intended structure or field was loaded and exported correctly.

## Version-specific caution
These mechanics target the installed `3.90.5a` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `VESTA`
- Synopsis: `VESTA structure_file`.
- Input mode: `arguments`.
- Required files: `supported crystal`, `density`, `or project file`.
- Output behavior: Starts VESTA and writes only outputs explicitly requested through its supported interface.
- Caution: VESTA is GUI-oriented; headless execution requires the deployment's Xvfb/display wrapper and many interactive operations are unsuitable for unattended benchmark runs.
