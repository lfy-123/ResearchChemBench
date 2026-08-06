---
software_id: acpype
versions: ["2023.10.27"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["ACPYPE", "acpype"]
inputs: ["PDB MOL2 or MDL molecular structure", "or matching prmtop and inpcrd files"]
outputs: ["AMBER prmtop and inpcrd", "GROMACS top itp and gro", "optional CNS or CHARMM files"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# ACPYPE Common Tasks

## Appropriate calculation families
- **Small-Molecule Parameterization**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Gaff And Gaff2 Atom Typing**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Amber Topology Generation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Amber-To-Gromacs Conversion**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `generate_small_molecule_topology`: validated structured route through backend `acpype`.
- `convert_amber_topology_to_gromacs`: validated structured route through backend `acpype`.

## Minimum input responsibilities
- `PDB MOL2 or MDL molecular structure`
- `or matching prmtop and inpcrd files`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `AMBER prmtop and inpcrd`
- `GROMACS top itp and gro`
- `optional CNS or CHARMM files`

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
- `ACPYPE`
- `Total time of execution`
- `exit code 0`

## Scientific convergence notes
ACPYPE completion validates file generation only; selected charges, protonation, tautomer, atom typing, and force-field compatibility must be checked explicitly before simulation.

## Version-specific caution
These mechanics target the installed `2023.10.27` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `acpype`
- Synopsis: `acpype -i input -b BASENAME -n CHARGE -m MULTIPLICITY -c CHARGE_METHOD -a ATOM_TYPE -q CHARGE_PROGRAM -o OUTPUT [options]`.
- Input mode: `arguments`.
- Declared example inputs: `input.mol2`.
- Declared example outputs: `molecule.acpype/molecule_AC.prmtop`, `molecule.acpype/molecule_AC.inpcrd`, `molecule.acpype/molecule_GMX.top`, `molecule.acpype/molecule_GMX.gro`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Creates BASENAME.acpype for parameterization or BASENAME.amb2gmx for conversion.
- Caution: Net charge, multiplicity, charge method, atom type, charge program, and output family are scientific inputs and must be explicit.
- Caution: Use `-p topology.prmtop -x coordinates.inpcrd -b BASENAME` for conversion without regenerating parameters.
