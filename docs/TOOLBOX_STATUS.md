# ResearchChem Atomic Toolbox Status

Generated: `2026-07-18T16:21:12.941535+00:00`
Catalog hash: `424356a552bb106c17d1e4920d9624a217341ccbe96c4cd4047fee0d9d8383ca`

## Summary

- Scientific Actions: 40
- Data Actions: 4
- BackendSpecs: 45
- Available backends: 43
- Unavailable backends: 2
- Exposure: full catalog for every task
- Backend selection: Agent required
- Automatic fallback: disabled

## Structural checks

- catalog: **pass**
- runtime_profiles: **pass**
- handler_coverage: **pass**
- legacy_public_tools_removed: **pass**

## Unavailable backends

- `orca`
- `gnina`

## Packages to install/download

Conda: none

Pip: none

External scientific data resources:

- `quantum_espresso`: UPF pseudopotentials covering every element in the calculation (for example SSSP or PseudoDojo), supplied as workspace Artifacts
- `siesta`: SIESTA PSF or compatible pseudopotentials covering every element, supplied as workspace Artifacts
- `dftbplus`: A DFTB+ Slater-Koster parameter-set directory containing every required element-pair .skf file (for example 3ob or matsci), supplied as a workspace Artifact
- `abinit`: ABINIT-compatible pseudopotentials covering every element, supplied as workspace Artifacts

Manual/licensed:

- `orca`: Download ORCA from the official portal and set CHEMGRAPH_ORCA_COMMAND.
- `gnina`: Download a GNINA release binary and set CHEMGRAPH_GNINA_COMMAND.

## Smoke

- `standardize_structure` / `rdkit`: **success**
- `generate_3d_structure` / `rdkit`: **success**
- `calculate_energy` / `ase_emt`: **success**
- `integrate_reaction_network` / `scipy`: **success**
- `assign_partial_charges` / `openff_am1bcc`: **success**
- `assign_force_field_parameters` / `openff`: **success**
- `solvate_molecular_system` / `packmol`: **success**
