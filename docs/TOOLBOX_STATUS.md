# ResearchChem Atomic Toolbox Status

Generated: `2026-07-18T14:26:14.444418+00:00`
Catalog hash: `d3f34e0162f0c12364e49b22612f36e3688062c9e489b79febd100d66404ffcd`

## Summary

- Scientific Actions: 40
- Data Actions: 4
- BackendSpecs: 45
- Available backends: 40
- Unavailable backends: 5
- Exposure: full catalog for every task
- Backend selection: Agent required
- Automatic fallback: disabled

## Structural checks

- catalog: **pass**
- runtime_profiles: **pass**
- handler_coverage: **pass**
- legacy_public_tools_removed: **pass**

## Unavailable backends

- `openff_am1bcc`
- `openff`
- `packmol`
- `orca`
- `gnina`

## Packages to install/download

Conda: openff-interchange, openff-toolkit, packmol

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
