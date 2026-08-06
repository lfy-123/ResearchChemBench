---
software_id: pmx
versions: ["0+untagged.1.g0dd5f0a"]
topics: ["common-tasks", "inputs", "outputs", "convergence"]
aliases: ["pmx", "pmx"]
inputs: ["hydrogen-complete PDB or GRO", "GROMACS TOP or ITP", "ligand PDB pairs", "XVG work files"]
outputs: ["hybrid structures", "hybrid topologies", "atom-pair maps", "mapping scores", "free-energy estimates"]
last_smoke_tested: "2026-08-06"
generated_from: chemistry_toolbox/config/native_software_manual_profiles.yaml + chemistry_toolbox/config/native_software_example_contracts.yaml
---
# pmx Common Tasks

## Appropriate calculation families
- **Protein Dna And Rna Mutation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **B-State Hybrid Topology Generation**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Ligand Atom Mapping**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.
- **Nonequilibrium Work Analysis**: author the method-specific input, stage every dependency, and declare the outputs needed for interpretation.

## Preferred typed Action routes
- `mutate_biomolecular_residues_for_alchemy`: validated structured route through backend `pmx`.
- `generate_alchemical_hybrid_topology`: validated structured route through backend `pmx`.
- `map_alchemical_ligand_atoms`: validated structured route through backend `pmx`.

## Minimum input responsibilities
- `hydrogen-complete PDB or GRO`
- `GROMACS TOP or ITP`
- `ligand PDB pairs`
- `XVG work files`

A minimum runnable input must still specify every scientifically material quantity: molecular or periodic structure, charge and spin where applicable, model or Hamiltonian, numerical controls, boundary conditions, task type, and requested outputs. Workflow programs additionally require their database, model, or upstream-calculation references.

## Expected output families
- `hybrid structures`
- `hybrid topologies`
- `atom-pair maps`
- `mapping scores`
- `free-energy estimates`

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
- `b-states filled`
- `Final results`
- `exit code 0`

## Scientific convergence notes
Successful preparation does not validate sampling or free-energy convergence; mapping quality, state charges, dummy interactions, overlap, hysteresis, and estimator uncertainty require explicit downstream checks.

## Version-specific caution
These mechanics target the installed `0+untagged.1.g0dd5f0a` environment. Verify keywords and file formats against the official references before reusing an input written for another release.

## Minimal-example policy
The tested file under `examples/interface_smoke/` verifies the configured command route. It does not choose a paper-specific method. For scientific work, start from the smallest official example for the intended calculation family, replace all structures and methods explicitly, run the toolbox validator, and retain the complete inputs and outputs as provenance.

## Command: `pmx`
- Synopsis: `pmx <mutate|gentop|atomMapping|analyse> [explicit options]`.
- Input mode: `arguments`.
- Declared example inputs: `protein.pdb`, `mutations.txt`.
- Declared example outputs: `hybrid.pdb`.
- Example resources: `{'cpu_cores': 1, 'memory_mb': 2048, 'gpu_count': 0}`.
- Output behavior: Writes command-specific hybrid structures, topologies, mapping files, scores, logs, or free-energy estimates.
- Caution: GMXLIB must point to pmx/data/mutff for mutation and hybrid-topology commands.
- Caution: The Python 3 develop branch is unstable upstream; reproduce only with the configured fixed commit.
- Caution: Mutation, force field, mapping filters, topology scaling, and estimators are scientific inputs and must be explicit.
