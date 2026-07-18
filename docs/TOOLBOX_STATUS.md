# ResearchChem Atomic Toolbox Status

Generated: `2026-07-18T21:28:41.946877+00:00`
Catalog hash: `f3c4f3f7a40b5b2b27a1b031b4d6269fea0ec29e59a471e35b589e23cba22949`

## Summary

- Scientific Actions: 40
- Data Actions: 4
- BackendSpecs: 45
- Available backends: 45
- Unavailable backends: 0
- Exposure: full catalog for every task
- Backend selection: Agent required
- Automatic fallback: disabled

## Structural checks

- catalog: **pass**
- runtime_profiles: **pass**
- handler_coverage: **pass**
- legacy_public_tools_removed: **pass**

## Unavailable backends


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
- `orca_6_1_1_linux_x86_64_shared_openmpi418_avx2` / orca: **available**; selection `runtime-managed`
- `openmpi_4_1_8_orca_runtime` / orca: **available**; selection `runtime-managed`

## Smoke

- `standardize_structure` / `rdkit`: **success**
- `generate_3d_structure` / `rdkit`: **success**
- `calculate_energy` / `ase_emt`: **success**
- `integrate_reaction_network` / `scipy`: **success**
- `assign_partial_charges` / `openff_am1bcc`: **success**
- `assign_force_field_parameters` / `openff`: **success**
- `solvate_molecular_system` / `packmol`: **success**
