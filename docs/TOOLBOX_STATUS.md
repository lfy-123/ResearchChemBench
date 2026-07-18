# ResearchChem Atomic Toolbox Status

Generated: `2026-07-18T17:49:22.449468+00:00`
Catalog hash: `57a3f05f4ec2bfcd76e744b19430a4356934c7c88015a12deb73234b8c63a1bc`

## Summary

- Scientific Actions: 40
- Data Actions: 4
- BackendSpecs: 45
- Available backends: 44
- Unavailable backends: 1
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

## Remaining installations

Conda: none

Pip: none

## Registered external scientific resources

- `qe_sssp_1_3_pbe_efficiency` / quantum_espresso: **available**; selection `resource://qe_sssp_1_3_pbe_efficiency/<Element>`
- `qe_sssp_1_3_pbe_precision` / quantum_espresso: **available**; selection `resource://qe_sssp_1_3_pbe_precision/<Element>`
- `siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml` / siesta: **available**; selection `resource://siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml/<Element>`
- `abinit_pseudo_dojo_nc_sr_pbe_standard_psp8` / abinit: **available**; selection `resource://abinit_pseudo_dojo_nc_sr_pbe_standard_psp8/<Element>`
- `dftb_3ob_3_1` / dftbplus: **available**; selection `resource://dftb_3ob_3_1`
- `dftb_matsci_0_3` / dftbplus: **available**; selection `resource://dftb_matsci_0_3`
- `gnina_1_3_3_cuda12_8_linux_x86_64` / gnina: **available**; selection `runtime-managed`

Manual/licensed:

- `orca`: Download ORCA from the official portal and set CHEMGRAPH_ORCA_COMMAND.

## Smoke

- `standardize_structure` / `rdkit`: **success**
- `generate_3d_structure` / `rdkit`: **success**
- `calculate_energy` / `ase_emt`: **success**
- `integrate_reaction_network` / `scipy`: **success**
- `assign_partial_charges` / `openff_am1bcc`: **success**
- `assign_force_field_parameters` / `openff`: **success**
- `solvate_molecular_system` / `packmol`: **success**
