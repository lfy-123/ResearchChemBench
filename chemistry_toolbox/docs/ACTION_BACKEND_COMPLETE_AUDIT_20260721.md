# ResearchChemBench Action–Backend 全组合测试与软件接入审计

> 生成时间：`2026-07-21T18:09:25.964513+00:00`。
> 本报告合并 2026-07-20 已有证据与本轮 65 个补测组合的真实统一分发调用；已测试组合不会重复运行。
> 另合并 GoodVibes 4.3.0 的 7 个真实 smoke，覆盖新增/升级的 6 个 Actions。
> 11个原失败组合的代码修复、现场复测及PubChem出口诊断见 [`ACTION_BACKEND_REPAIR_REPORT_20260721.md`](ACTION_BACKEND_REPAIR_REPORT_20260721.md)。

## 1. 最终结论

| 指标 | 结果 |
|---|---:|
| 公开 Actions | 106 |
| BackendSpecs | 76 |
| Catalog Action–Backend 组合 | 241 |
| 有成功证据的组合 | **236** |
| 仅有失败证据的组合 | **5** |
| 尚未测试组合 | **0** |
| 本轮补测 | 65/65 通过，0 失败 |
| GoodVibes 4.3.0 专项 | 7/7 通过，覆盖 6/6 Actions |
| 至少有一个成功 Action 的 Backend | 76/76 |
| 当前无任何成功证据的 Backend | — |

结论：**241/241 个声明组合都有真实调用证据；236 个通过，5 个仍有问题。** 当前包含 0 个本地适配问题和 5 个远端数据服务问题。

## 2. 本轮补测结果

| 分组 | 组合数 | 通过 | 失败 |
|---|---:|---:|---:|
| 分子电子结构与ML势 | 30 | 30 | 0 |
| 周期材料与弛豫 | 18 | 18 | 0 |
| 分子动力学与溶剂化 | 8 | 8 | 0 |
| 轨迹分析与反应 | 5 | 5 | 0 |
| 声子 | 4 | 4 | 0 |

证据文件：[`action_backend_matrix_smoke_status.json`](../config/action_backend_matrix_smoke_status.json)、[`goodvibes_action_smoke_status.json`](../config/goodvibes_action_smoke_status.json)、[`action_test_coverage.json`](../config/action_test_coverage.json)。

## 3. 出现问题的 Backend 调用及修复建议

### 3.1 5个仅失败组合

| 优先级 | Backend | Action | 问题类型 | 根因 | 建议修复 |
|---|---|---|---|---|---|
| P1 | `pubchem` | `resolve_chemical_identity` | 远端服务503 | 本机 DNS、TLS 和 PubChem 首页可达，但 PUG REST 当前返回 `503 PUGREST.ServerBusy`；响应头明确包含 `Retry-After: 30` 以及 `too many requests per second or blacklisted`。 | 代码已加入跨 worker 限速、尊重 `Retry-After` 的有界退避和 `retryable=true` 错误语义；剩余工作是检查共享出口 IP/代理或等待 PubChem 解除临时黑名单。 |
| P1 | `pubchem` | `retrieve_compound_properties` | 远端服务503 | PubChem PUG REST 当前对本服务器出口返回带黑名单提示的503。 | 本 Action 已共用限速、Retry-After 退避和可重试错误模型；需从服务器网络侧排查出口 IP。 |
| P1 | `pubchem` | `retrieve_compound_structure` | 远端服务503 | PubChem PUG REST 当前对本服务器出口返回带黑名单提示的503。 | 已改用可读取响应限流头的有界 HTTP 客户端并保留 PubChemPy 的 Compound 解析；需从服务器网络侧解除外部阻塞。 |
| P1 | `pubchem` | `search_similar_compounds` | 远端服务503 | PubChem fast similarity 端点当前对本服务器出口返回带黑名单提示的503。 | 已保留独立超时并加入限速、Retry-After 退避和可重试错误；不自动降低阈值或改换算法，需排查出口 IP。 |
| P1 | `pubchem` | `search_substructures` | 远端服务503 | PubChem fast substructure 端点当前对本服务器出口返回带黑名单提示的503。 | 已加入限速、Retry-After 退避，并把服务繁忙与无匹配结果严格区分；需排查出口 IP。 |

### 3.2 Backend级影响范围

| Backend | 已成功组合 | 失败组合 | 判断 |
|---|---:|---:|---|
| `pubchem` | 1 | 5 | 代码侧韧性修复已完成；当前现场失败来自远端503/出口黑名单。 |


## 4. 101个 Action 的完整 Backend 实测清单

标记：✅ 至少一次成功/部分成功；❌ 仅失败；⚠️ 有历史成功但最新现场降级。

| # | Action | 领域 | Backend实测状态 |
|---:|---|---|---|
| 1 | `normalize_qcschema_molecule` | 科学数据、Schema与输出解析 | ✅ `qcelemental` |
| 2 | `validate_qcschema_record` | 科学数据、Schema与输出解析 | ✅ `qcelemental` |
| 3 | `parse_quantum_chemistry_output` | 科学数据、Schema与输出解析 | ✅ `cclib` |
| 4 | `standardize_structure` | 结构、构象、电荷与体系构建 | ✅ `rdkit` |
| 5 | `generate_3d_structure` | 结构、构象、电荷与体系构建 | ✅ `rdkit`<br>✅ `openbabel` |
| 6 | `generate_conformer_ensemble` | 结构、构象、电荷与体系构建 | ✅ `rdkit_etkdg`<br>✅ `crest` |
| 7 | `cluster_conformers` | 结构、构象、电荷与体系构建 | ✅ `rdkit` |
| 8 | `align_molecular_structures` | 结构、构象、电荷与体系构建 | ✅ `rdkit` |
| 9 | `rank_conformers_from_results` | 结构、构象、电荷与体系构建 | ✅ `internal_statistics` |
| 10 | `repair_biomolecular_structure` | 结构、构象、电荷与体系构建 | ✅ `pdbfixer` |
| 11 | `select_structure_subset` | 结构、构象、电荷与体系构建 | ✅ `pdb_tools` |
| 12 | `renumber_biomolecular_structure` | 结构、构象、电荷与体系构建 | ✅ `pdb_tools` |
| 13 | `normalize_pdb_records` | 结构、构象、电荷与体系构建 | ✅ `pdb_tools` |
| 14 | `assign_protonation_states` | 结构、构象、电荷与体系构建 | ✅ `rdkit`<br>✅ `pdbfixer` |
| 15 | `assign_partial_charges` | 结构、构象、电荷与体系构建 | ✅ `rdkit_gasteiger`<br>✅ `openff_am1bcc` |
| 16 | `assign_force_field_parameters` | 结构、构象、电荷与体系构建 | ✅ `openff`<br>✅ `openmm_builder` |
| 17 | `solvate_molecular_system` | 结构、构象、电荷与体系构建 | ✅ `openmm_builder`<br>✅ `packmol` |
| 18 | `analyze_crystal_symmetry` | 结构、构象、电荷与体系构建 | ✅ `spglib`<br>✅ `pymatgen` |
| 19 | `standardize_crystal_structure` | 结构、构象、电荷与体系构建 | ✅ `spglib`<br>✅ `pymatgen` |
| 20 | `build_supercell` | 结构、构象、电荷与体系构建 | ✅ `pymatgen` |
| 21 | `enumerate_surface_slabs` | 结构、构象、电荷与体系构建 | ✅ `pymatgen` |
| 22 | `calculate_molecular_descriptors` | 化学信息学与分子图操作 | ✅ `rdkit` |
| 23 | `calculate_molecular_fingerprint` | 化学信息学与分子图操作 | ✅ `rdkit` |
| 24 | `calculate_molecular_similarity` | 化学信息学与分子图操作 | ✅ `rdkit` |
| 25 | `search_local_substructures` | 化学信息学与分子图操作 | ✅ `rdkit` |
| 26 | `enumerate_tautomers` | 化学信息学与分子图操作 | ✅ `rdkit` |
| 27 | `enumerate_stereoisomers` | 化学信息学与分子图操作 | ✅ `rdkit` |
| 28 | `calculate_energy` | 分子电子结构与派生性质 | ✅ `xtb`<br>✅ `pyscf`<br>✅ `psi4`<br>✅ `tblite`<br>✅ `gpaw`<br>✅ `nwchem`<br>✅ `openmolcas`<br>✅ `mace`<br>✅ `chgnet`<br>✅ `deepmd`<br>✅ `orca`<br>✅ `gaussian`<br>✅ `gamess`<br>✅ `ase_emt` |
| 29 | `calculate_forces` | 分子电子结构与派生性质 | ✅ `xtb`<br>✅ `pyscf`<br>✅ `tblite`<br>✅ `gpaw`<br>✅ `nwchem`<br>✅ `orca`<br>✅ `mace`<br>✅ `chgnet`<br>✅ `deepmd`<br>✅ `ase_emt` |
| 30 | `calculate_hessian` | 分子电子结构与派生性质 | ✅ `xtb`<br>✅ `pyscf`<br>✅ `psi4`<br>✅ `tblite`<br>✅ `nwchem`<br>✅ `orca`<br>✅ `gaussian`<br>✅ `mace`<br>✅ `chgnet`<br>✅ `deepmd`<br>✅ `ase_emt` |
| 31 | `optimize_geometry` | 分子电子结构与派生性质 | ✅ `xtb`<br>✅ `tblite`<br>✅ `gpaw`<br>✅ `mace`<br>✅ `chgnet`<br>✅ `deepmd`<br>✅ `orca`<br>✅ `gaussian`<br>✅ `gamess`<br>✅ `ase_emt`<br>✅ `geometric`<br>✅ `sella` |
| 32 | `calculate_dipole_moment` | 分子电子结构与派生性质 | ✅ `xtb`<br>✅ `tblite`<br>✅ `pyscf`<br>✅ `psi4`<br>✅ `nwchem`<br>✅ `openmolcas`<br>✅ `orca`<br>✅ `gaussian`<br>✅ `gamess` |
| 33 | `calculate_atomic_charges` | 分子电子结构与派生性质 | ✅ `xtb`<br>✅ `pyscf`<br>✅ `psi4`<br>✅ `nwchem`<br>✅ `openmolcas`<br>✅ `multiwfn`<br>✅ `orca` |
| 34 | `calculate_orbitals` | 分子电子结构与派生性质 | ✅ `pyscf`<br>✅ `psi4`<br>✅ `openmolcas`<br>✅ `orca` |
| 35 | `calculate_bond_orders` | 分子电子结构与派生性质 | ✅ `xtb`<br>✅ `multiwfn`<br>✅ `orca` |
| 36 | `calculate_excited_states` | 分子电子结构与派生性质 | ✅ `pyscf`<br>✅ `orca` |
| 37 | `analyze_electron_density_topology` | 分子电子结构与派生性质 | ✅ `critic2` |
| 38 | `calculate_atomic_basin_properties` | 分子电子结构与派生性质 | ✅ `critic2` |
| 39 | `calculate_bader_charges` | 分子电子结构与派生性质 | ✅ `critic2` |
| 40 | `derive_vibrational_modes` | 分子电子结构与派生性质 | ✅ `internal_vibrations` |
| 41 | `derive_ir_spectrum` | 分子电子结构与派生性质 | ✅ `internal_spectroscopy` |
| 42 | `derive_uv_vis_spectrum` | 分子电子结构与派生性质 | ✅ `internal_spectroscopy` |
| 43 | `derive_thermochemistry` | 分子电子结构与派生性质 | ✅ `internal_thermochemistry`<br>✅ `goodvibes` |
| 44 | `scan_thermochemistry_temperature` | 分子电子结构与派生性质 | ✅ `goodvibes` |
| 45 | `analyze_thermochemical_ensemble` | 分子电子结构与派生性质 | ✅ `goodvibes` |
| 46 | `validate_thermochemistry_inputs` | 分子电子结构与派生性质 | ✅ `goodvibes` |
| 47 | `locate_transition_state` | 反应路径、平衡与动力学 | ✅ `pysisyphus`<br>✅ `sella` |
| 48 | `trace_intrinsic_reaction_coordinate` | 反应路径、平衡与动力学 | ✅ `pysisyphus` |
| 49 | `calculate_chemical_equilibrium` | 反应路径、平衡与动力学 | ✅ `cantera` |
| 50 | `integrate_reaction_network` | 反应路径、平衡与动力学 | ✅ `scipy`<br>✅ `cantera` |
| 51 | `calculate_rate_constants` | 反应路径、平衡与动力学 | ✅ `rmg` |
| 52 | `calculate_tunneling_correction` | 反应路径、平衡与动力学 | ✅ `rmg` |
| 53 | `solve_master_equation` | 反应路径、平衡与动力学 | ✅ `mess`<br>✅ `mesmer` |
| 54 | `solve_microkinetic_model` | 反应路径、平衡与动力学 | ✅ `catmap` |
| 55 | `analyze_thermochemical_selectivity` | 反应路径、平衡与动力学 | ✅ `goodvibes` |
| 56 | `analyze_reaction_free_energy_profile` | 反应路径、平衡与动力学 | ✅ `goodvibes` |
| 57 | `minimize_system_energy` | 分子动力学、轨迹与自由能 | ✅ `openmm`<br>✅ `gromacs`<br>✅ `lammps`<br>✅ `hoomd`<br>✅ `namd`<br>✅ `amber_pmemd`<br>✅ `charmm` |
| 58 | `calculate_force_field_energy` | 分子动力学、轨迹与自由能 | ✅ `openmm`<br>✅ `hoomd` |
| 59 | `calculate_force_field_forces` | 分子动力学、轨迹与自由能 | ✅ `openmm`<br>✅ `hoomd` |
| 60 | `decompose_force_field_energy` | 分子动力学、轨迹与自由能 | ✅ `openmm` |
| 61 | `propagate_dynamics` | 分子动力学、轨迹与自由能 | ✅ `openmm`<br>✅ `gromacs`<br>✅ `lammps`<br>✅ `hoomd`<br>✅ `namd`<br>✅ `amber_pmemd`<br>✅ `charmm` |
| 62 | `calculate_trajectory_rmsd` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis`<br>✅ `mdtraj` |
| 63 | `calculate_radius_of_gyration` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis`<br>✅ `mdtraj` |
| 64 | `calculate_radial_distribution` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis` |
| 65 | `calculate_mean_squared_displacement` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis` |
| 66 | `calculate_contacts` | 分子动力学、轨迹与自由能 | ✅ `mdtraj` |
| 67 | `calculate_solvent_accessible_surface` | 分子动力学、轨迹与自由能 | ✅ `mdtraj` |
| 68 | `calculate_dihedral_distribution` | 分子动力学、轨迹与自由能 | ✅ `mdtraj`<br>✅ `mdanalysis` |
| 69 | `calculate_hydrogen_bonds` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis` |
| 70 | `calculate_principal_components` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis` |
| 71 | `calculate_dynamic_cross_correlation` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis` |
| 72 | `assign_secondary_structure` | 分子动力学、轨迹与自由能 | ✅ `mdtraj` |
| 73 | `cluster_trajectory` | 分子动力学、轨迹与自由能 | ✅ `mdtraj` |
| 74 | `evaluate_collective_variables` | 分子动力学、轨迹与自由能 | ✅ `plumed` |
| 75 | `estimate_free_energy_difference` | 分子动力学、轨迹与自由能 | ✅ `pymbar` |
| 76 | `estimate_thermodynamic_expectations` | 分子动力学、轨迹与自由能 | ✅ `pymbar` |
| 77 | `calculate_potential_of_mean_force` | 分子动力学、轨迹与自由能 | ✅ `pymbar` |
| 78 | `analyze_free_energy_convergence` | 分子动力学、轨迹与自由能 | ✅ `pymbar` |
| 79 | `parse_alchemical_energy_data` | 分子动力学、轨迹与自由能 | ✅ `alchemlyb` |
| 80 | `calculate_periodic_energy` | 周期电子结构、声子与热输运 | ✅ `quantum_espresso`<br>✅ `cp2k`<br>✅ `siesta`<br>✅ `dftbplus`<br>✅ `abinit`<br>✅ `vasp`<br>✅ `gpaw`<br>✅ `nequip`<br>✅ `allegro`<br>✅ `deepmd` |
| 81 | `calculate_periodic_forces` | 周期电子结构、声子与热输运 | ✅ `quantum_espresso`<br>✅ `cp2k`<br>✅ `siesta`<br>✅ `dftbplus`<br>✅ `abinit`<br>✅ `vasp`<br>✅ `gpaw`<br>✅ `nequip`<br>✅ `allegro`<br>✅ `deepmd` |
| 82 | `calculate_periodic_stress` | 周期电子结构、声子与热输运 | ✅ `quantum_espresso`<br>✅ `cp2k`<br>✅ `abinit`<br>✅ `vasp`<br>✅ `gpaw`<br>✅ `nequip`<br>✅ `allegro`<br>✅ `deepmd` |
| 83 | `relax_periodic_structure` | 周期电子结构、声子与热输运 | ✅ `quantum_espresso`<br>✅ `cp2k`<br>✅ `siesta`<br>✅ `dftbplus`<br>✅ `abinit`<br>✅ `vasp`<br>✅ `gpaw`<br>✅ `nequip`<br>✅ `allegro`<br>✅ `deepmd` |
| 84 | `calculate_electronic_band_structure` | 周期电子结构、声子与热输运 | ✅ `gpaw` |
| 85 | `calculate_density_of_states` | 周期电子结构、声子与热输运 | ✅ `gpaw` |
| 86 | `calculate_projected_density_of_states` | 周期电子结构、声子与热输运 | ✅ `gpaw`<br>✅ `lobster` |
| 87 | `analyze_periodic_bonding` | 周期电子结构、声子与热输运 | ✅ `lobster` |
| 88 | `calculate_charge_spilling` | 周期电子结构、声子与热输运 | ✅ `lobster` |
| 89 | `generate_displaced_supercells` | 周期电子结构、声子与热输运 | ✅ `phonopy`<br>✅ `phono3py` |
| 90 | `assemble_force_constants` | 周期电子结构、声子与热输运 | ✅ `phonopy`<br>✅ `phono3py` |
| 91 | `calculate_phonon_dispersion` | 周期电子结构、声子与热输运 | ✅ `phonopy`<br>✅ `phono3py` |
| 92 | `calculate_phonon_density_of_states` | 周期电子结构、声子与热输运 | ✅ `phonopy`<br>✅ `phono3py` |
| 93 | `calculate_harmonic_thermodynamics` | 周期电子结构、声子与热输运 | ✅ `phonopy`<br>✅ `phono3py` |
| 94 | `calculate_phonon_group_velocities` | 周期电子结构、声子与热输运 | ✅ `phonopy`<br>✅ `phono3py` |
| 95 | `calculate_lattice_thermal_conductivity` | 周期电子结构、声子与热输运 | ✅ `phono3py`<br>✅ `shengbte` |
| 96 | `dock_ligand` | 分子对接 | ✅ `vina`<br>✅ `gnina` |
| 97 | `search_compounds` | 外部化学数据源 | ✅ `pubchem` |
| 98 | `resolve_chemical_identity` | 外部化学数据源 | ❌ `pubchem` |
| 99 | `retrieve_compound_properties` | 外部化学数据源 | ❌ `pubchem` |
| 100 | `retrieve_compound_structure` | 外部化学数据源 | ❌ `pubchem` |
| 101 | `search_similar_compounds` | 外部化学数据源 | ❌ `pubchem` |
| 102 | `search_substructures` | 外部化学数据源 | ❌ `pubchem` |
| 103 | `search_protein_structures` | 外部化学数据源 | ✅ `rcsb_pdb` |
| 104 | `search_materials` | 外部化学数据源 | ✅ `materials_project` |
| 105 | `search_catalysis_records` | 外部化学数据源 | ✅ `catalysis_hub` |
| 106 | `lookup_nist_webbook_species` | 外部化学数据源 | ✅ `nist_webbook` |

## 5. 当前作为 Backend 使用的软件、程序库和数据接口

共注册 **76 个 BackendSpecs**；其中 75 个由外部程序、Python库或在线接口支撑，`internal_statistics` 是纯内部确定性实现。一个软件可对应多个 BackendSpec（例如 RDKit）。

| Backend ID | 软件/实现 | Runtime | 可执行文件/模块 | Action数 | 全组合结果 |
|---|---|---|---|---:|---|
| `qcelemental` | QCElemental | `workflows` | `qcelemental` | 2 | ✅ 2/2 |
| `cclib` | cclib | `workflows` | `cclib` | 1 | ✅ 1/1 |
| `rdkit` | RDKit | `core` | `rdkit` | 11 | ✅ 11/11 |
| `openbabel` | Open Babel | `quantum` | `obabel`, `openbabel` | 1 | ✅ 1/1 |
| `rdkit_etkdg` | RDKit ETKDG | `core` | `rdkit` | 1 | ✅ 1/1 |
| `crest` | CREST | `reaction` | `crest` | 1 | ✅ 1/1 |
| `internal_statistics` | ResearchChem deterministic statistics | `core` | — | 1 | ✅ 1/1 |
| `pdbfixer` | PDBFixer | `md` | `pdbfixer`, `openmm` | 2 | ✅ 2/2 |
| `pdb_tools` | pdb-tools | `core` | `pdb_selchain`, `pdb_reres`, `pdb_tidy`, `pdbtools` | 3 | ✅ 3/3 |
| `rdkit_gasteiger` | RDKit Gasteiger charges | `core` | `rdkit` | 1 | ✅ 1/1 |
| `openff_am1bcc` | OpenFF AM1-BCC | `openff` | `antechamber`, `sqm`, `openff.toolkit` | 1 | ✅ 1/1 |
| `openff` | OpenFF Toolkit/Interchange | `openff` | `openff.toolkit`, `openff.interchange` | 1 | ✅ 1/1 |
| `openmm_builder` | OpenMM system builder | `md` | `openmm` | 2 | ✅ 2/2 |
| `packmol` | Packmol | `md` | `packmol` | 1 | ✅ 1/1 |
| `spglib` | spglib | `workflows` | `spglib`, `numpy` | 2 | ✅ 2/2 |
| `pymatgen` | pymatgen | `workflows` | `pymatgen`, `numpy` | 4 | ✅ 4/4 |
| `xtb` | xTB | `quantum` | `xtb` | 7 | ✅ 7/7 |
| `pyscf` | PySCF | `quantum` | `pyscf` | 7 | ✅ 7/7 |
| `gpaw` | GPAW | `gpaw` | `gpaw`, `gpaw`, `ase`, `numpy` | 10 | ✅ 10/10 |
| `lobster` | LOBSTER | `lobster` | `lobster-5.1.0`, `pymatgen`, `numpy` | 3 | ✅ 3/3 |
| `nwchem` | NWChem | `nwchem` | `nwchem`, `qcengine`, `qcelemental`, `numpy` | 5 | ✅ 5/5 |
| `openmolcas` | OpenMolcas | `openmolcas` | `pymolcas` | 4 | ✅ 4/4 |
| `multiwfn` | Multiwfn | `multiwfn` | `Multiwfn_noGUI` | 2 | ✅ 2/2 |
| `critic2` | Critic2 | `critic2` | `critic2` | 3 | ✅ 3/3 |
| `psi4` | Psi4 | `psi4` | `psi4`, `psi4` | 5 | ✅ 5/5 |
| `tblite` | TBLite | `quantum` | `tblite`, `ase` | 5 | ✅ 5/5 |
| `mace` | MACE | `mlip` | `mace.calculators`, `ase` | 4 | ✅ 4/4 |
| `chgnet` | CHGNet | `mlip` | `chgnet`, `ase` | 4 | ✅ 4/4 |
| `deepmd` | DeePMD-kit | `deepmd` | `dp`, `deepmd`, `ase` | 8 | ✅ 8/8 |
| `nequip` | NequIP | `nequip` | `nequip-train`, `nequip`, `torch`, `e3nn`, `ase` | 4 | ✅ 4/4 |
| `allegro` | Allegro | `nequip` | `allegro`, `nequip`, `torch`, `e3nn`, `ase` | 4 | ✅ 4/4 |
| `orca` | ORCA | `quantum` | `orca` | 9 | ✅ 9/9 |
| `gaussian` | Gaussian 16 | `gaussian` | `g16`, `formchk` | 4 | ✅ 4/4 |
| `gamess` | GAMESS | `gamess` | `rungms` | 3 | ✅ 3/3 |
| `ase_emt` | ASE EMT | `core` | `ase.calculators.emt` | 4 | ✅ 4/4 |
| `internal_vibrations` | ResearchChem vibrational analysis | `core` | `ase`, `numpy` | 1 | ✅ 1/1 |
| `internal_spectroscopy` | ResearchChem spectrum builder | `core` | `numpy` | 2 | ✅ 2/2 |
| `internal_thermochemistry` | ResearchChem statistical thermochemistry | `core` | `ase`, `numpy` | 1 | ✅ 1/1 |
| `goodvibes` | GoodVibes | `goodvibes` | `goodvibes`, `goodvibes` | 6 | ✅ 6/6 |
| `geometric` | geomeTRIC | `nwchem` | `geometric`, `numpy` | 1 | ✅ 1/1 |
| `sella` | Sella | `sella` | `sella`, `ase`, `numpy` | 2 | ✅ 2/2 |
| `pysisyphus` | pysisyphus | `reaction` | `pysis`, `pysisyphus` | 2 | ✅ 2/2 |
| `cantera` | Cantera | `reaction` | `cantera` | 2 | ✅ 2/2 |
| `scipy` | SciPy | `reaction` | `scipy` | 1 | ✅ 1/1 |
| `rmg` | RMG-Py | `rmg` | `rmg.py`, `rmgpy` | 2 | ✅ 2/2 |
| `mess` | MESS | `mess` | `mess` | 1 | ✅ 1/1 |
| `mesmer` | MESMER | `mesmer` | `mesmer` | 1 | ✅ 1/1 |
| `catmap` | CatMAP | `reaction` | `catmap` | 1 | ✅ 1/1 |
| `openmm` | OpenMM | `md` | `openmm` | 5 | ✅ 5/5 |
| `gromacs` | GROMACS | `md` | `gmx` | 2 | ✅ 2/2 |
| `lammps` | LAMMPS | `md` | `lmp`, `lammps` | 2 | ✅ 2/2 |
| `hoomd` | HOOMD-blue | `free_energy` | `hoomd`, `numpy` | 4 | ✅ 4/4 |
| `namd` | NAMD 3 | `namd` | `namd3` | 2 | ✅ 2/2 |
| `amber_pmemd` | Amber 26 PMEMD | `amber` | `pmemd`, `pmemd.MPI`, `mpirun` | 2 | ✅ 2/2 |
| `charmm` | CHARMM c50b2 | `charmm` | `charmm` | 2 | ✅ 2/2 |
| `mdanalysis` | MDAnalysis | `md` | `MDAnalysis` | 8 | ✅ 8/8 |
| `mdtraj` | MDTraj | `workflows` | `mdtraj`, `numpy` | 7 | ✅ 7/7 |
| `plumed` | PLUMED | `md` | `plumed` | 1 | ✅ 1/1 |
| `pymbar` | PyMBAR | `free_energy` | `pymbar`, `numpy` | 4 | ✅ 4/4 |
| `alchemlyb` | alchemlyb | `free_energy` | `alchemlyb`, `pandas`, `numpy` | 1 | ✅ 1/1 |
| `quantum_espresso` | Quantum ESPRESSO | `qe` | `pw.x` | 4 | ✅ 4/4 |
| `cp2k` | CP2K | `cp2k` | `cp2k` | 4 | ✅ 4/4 |
| `siesta` | SIESTA | `periodic` | `siesta` | 3 | ✅ 3/3 |
| `dftbplus` | DFTB+ | `periodic` | `dftb+` | 3 | ✅ 3/3 |
| `abinit` | ABINIT | `abinit` | `abinit`, `numpy`, `pydantic`, `yaml` | 4 | ✅ 4/4 |
| `vasp` | VASP | `vasp` | `vasp_std` | 4 | ✅ 4/4 |
| `phonopy` | Phonopy | `phonons` | `phonopy`, `phonopy` | 6 | ✅ 6/6 |
| `phono3py` | Phono3py | `phonons` | `phono3py`, `phono3py` | 7 | ✅ 7/7 |
| `shengbte` | ShengBTE | `shengbte` | `ShengBTE` | 1 | ✅ 1/1 |
| `vina` | AutoDock Vina | `docking` | `vina`, `vina` | 1 | ✅ 1/1 |
| `gnina` | GNINA | `docking` | `gnina` | 1 | ✅ 1/1 |
| `pubchem` | PubChem PUG REST | `services` | `pubchempy` | 6 | ⚠️ 1成功 / 5失败 |
| `rcsb_pdb` | RCSB PDB Data API | `services` | `httpx` | 1 | ✅ 1/1 |
| `materials_project` | Materials Project | `services` | `httpx`, `mp_api` | 1 | ✅ 1/1 |
| `catalysis_hub` | Catalysis-Hub GraphQL | `services` | `httpx` | 1 | ✅ 1/1 |
| `nist_webbook` | NIST Chemistry WebBook SRD 69 CGI | `services` | `httpx` | 1 | ✅ 1/1 |

## 6. 已安装但没有被公共 Action 直接调用的软件

清单中共有 17 项标为 `runtime_only`。其中 QCEngine 被 NWChem Backend 间接使用；其余 **16 项**没有出现在任何 Action handler 中。

### 6.1 间接使用，不应误判为闲置

| 软件 | 状态 | 实际用途 |
|---|---|---|
| `QCEngine` | configured | NWChem Actions 通过 QCEngine/QCSchema harness 执行；不需要额外暴露通用 runner。 |

### 6.2 已安装/部分安装但当前没有 Action 调用

| 软件 | 配置状态 | Runtime | 当前未接入原因 | 建议 |
|---|---|---|---|---|
| `AiiDA` | configured | `workflows` | Profile researchchembench is initialized with SQLite under .software_cache/aiida; it remains infrastructure because exposing a fixed AiiDA workflow would hide the Agent's tool ordering and backend choices. | 保持为调度/溯源基础设施；若接入，应放在 MCP 下层管理作业，不要暴露固定科学 workflow。 |
| `atomate2` | configured | `workflows` | Installed as a library only; no fixed workflow is exposed as a public Action. | 只抽取可复用的原子材料操作，避免直接暴露预编排 Flow。 |
| `jobflow` | configured | `workflows` | A minimal add(2,3) local flow passed; Agent still chooses job ordering and inputs. | 可作为后台依赖图/重试执行层，不应替智能体决定科学步骤。 |
| `CENSO` | configured | `reaction` | CENSO is available in the reaction runtime; complete runs still require explicit CREST/ORCA/TURBOMOLE choices and inputs. | 拆成构象过滤、能量重排、自由能校正等独立 Actions，并要求显式选择量化后端。 |
| `autodE` | configured | `nwchem` | Library installed with NWChem support dependencies; no monolithic workflow Action is exposed. | 拆成反应物/产物复合物生成、TS 候选、路径验证等原子 Actions。 |
| `Wannier90` | configured | `qe` | Existing Quantum ESPRESSO runtime already provides wannier90.x. | 新增 `construct_wannier_functions`、插值能带和 Berry/拓扑性质 Actions。 |
| `Yambo` | configured | `yambo` | Yambo 5.3.0 binary is installed; no upstream wavefunction database or fixed input is generated. | 新增 GW 准粒子与 BSE 激子性质 Actions，并显式接收前序 DFT 产物。 |
| `Arkane` | partial | `rmg` | Shipped with RMG-Py, Arkane.py and the official database are present. Top-level import remains pathologically slow and a bundled H thermochemistry example exceeded a 300-second bound, so this stays partial until the runtime is repaired or a bounded real calculation passes. | 先解决导入/示例超时，再接热化学、速率和主方程输入构建的原子能力。 |
| `AutoMeKin` | configured | `automekin` | Official source was built in an isolated conda environment with the bundled MOPAC engine; a real water PM7 single-point job ended normally. Gaussian is configured independently, but AutoMeKin-to-Gaussian/Qcore coupling is not prewired or selected implicitly. | 拆成反应事件候选生成、路径筛选和网络扩展 Actions。 |
| `KinBot` | configured | `kinbot` | KinBot 2.2.2 and dependencies import successfully in a repaired NumPy 1.26 / JAX 0.4.35 runtime with no pip dependency conflicts; real PES execution requires explicit input and remains a workflow-level capability rather than a public monolithic runner. | 接入反应族候选、TS 猜测和单步验证，不暴露完整自动网络 workflow。 |
| `SHARC` | configured | `sharc` | SHARC4 core binaries and wfoverlap_ascii were compiled; PySHARC/NetCDF and full trajectories still require explicit electronic-structure interfaces and task inputs. | 新增初态采样、非绝热耦合和单段 surface-hopping 动力学 Actions。 |
| `Newton-X` | configured | `newtonx` | Newton-X New Series 3.5.3 is installed and the bundled analytical avoided-crossing test passed. It remains runtime-only until a typed nonadiabatic Action can expose states, couplings, hopping controls and an explicit electronic-structure interface without becoming a monolithic workflow runner. | 与 SHARC 类似，接入显式电子结构接口选择和单段非绝热传播。 |
| `TheoDORE` | configured | `theodore` | TheoDORE 2.5.0 imports and CLI starts; optional Orbkit/OpenBabel extensions are not installed. | 新增激发态特征、跃迁密度和电荷转移分析 Actions。 |
| `EasySpin` | partial | `easyspin` | EasySpin 6.0.12 toolbox files are staged and structurally validated. Official MATLAB R2018a installation media are now cached, but no licensed MATLAB executable exists yet; executable EasySpin validation remains blocked on a legitimate File Installation Key/license file or license server. | 在合法 MATLAB/兼容运行时就绪后新增 EPR 参数与谱模拟 Actions。 |
| `VMD` | configured | `vmd` | VMD 1.9.3 text-mode startup passed; GUI operation depends on DISPLAY/OpenGL. | 如 benchmark 需要视觉产物，可提供轨迹渲染/图像导出；否则保持人工可视化工具。 |
| `VESTA` | configured | `vesta` | Official VESTA 3.90.5a GTK3 x86_64 package is installed with locally extracted Ubuntu runtime libraries; an Xvfb headless launch remained healthy until the bounded smoke timeout. Interactive GUI use still requires DISPLAY/OpenGL, and redistribution is prohibited by the VESTA license. | 如 benchmark 需要材料图像，可提供结构/密度等值面渲染；否则无需进入科学 Action Catalog。 |

## 7. 尚未形成 Backend 的许可软件或数据接口

这些项目不能算“已安装但未使用”；它们当前缺许可证、有效安装或稳定接口。

| 项目 | 状态 | MCP暴露策略 | 原因/后续条件 |
|---|---|---|---|
| `Q-Chem` | manual_required | `disabled_by_operator_no_license` | Explicitly disabled by the operator because it is not needed and no license is available. It is absent from BackendSpecs and the MCP catalog; do not install or expose it unless the operator later reverses this decision and supplies a valid license. |
| `Molpro` | manual_required | `disabled_by_operator_no_license` | Explicitly disabled by the operator because it is not needed and no license is available. It is absent from BackendSpecs and the MCP catalog; re-enable only after a deliberate operator decision and valid license/site installation. |
| `TURBOMOLE` | manual_required | `disabled_by_operator_no_license` | Explicitly disabled by the operator because it is not needed and no license is available. It is absent from BackendSpecs and the MCP catalog; CENSO must not select it implicitly. |
| `CASTEP` | manual_required | `not_implemented` | Requires STFC academic/commercial license and a site build. |
| `CRYSTAL` | manual_required | `disabled_by_operator_no_license` | Explicitly disabled by the operator because it is not needed and no license is available. It is absent from BackendSpecs and the MCP catalog. |
| `WIEN2k` | manual_required | `disabled_by_operator_no_license` | Explicitly disabled by the operator because it is not needed and no license is available. It is absent from BackendSpecs and the MCP catalog. |
| `MATLAB` | manual_required | `not_exposed_host_runtime` | Both official MATLAB R2018a Linux ISO images are staged in .software_cache (DVD1 SHA-256 780717eeeaf11855a119ffe5e3e8be3443df4b1b79a2dcb04feb4c3ea7eb693e; DVD2 485467b9662b7d2f6bbf92b84b18b95fed93a9d6fc6ead4c806b1b67e9296997). The separately downloaded crack archive was deliberately not copied, opened or used. Installation and EasySpin execution require a legitimate MathWorks File Installation Key plus license file/server information. |
| `OpenEye` | manual_required | `disabled_by_operator_no_license` | Explicitly disabled by the operator because it is not needed and no license is available. It is absent from BackendSpecs and the MCP catalog; a conda package alone would not authorize use without a valid OpenEye license. |
| `Schrödinger` | manual_required | `not_exposed_missing_licensed_suite` | The supplied schroedinger-1.0.11-7 Arch package was identified from .PKGINFO as an ANSI C implementation of the Dirac video codec, not the commercial Schrödinger chemistry suite. It is retained only under .software_cache/schrodinger/rejected with SHA-256 41906fcce0eeb74edcaf50ee46635c2f336703692d956782dba7dd1f419187b7 and is not installed or exposed. A genuine Schrödinger Suite installer and site license are still required if this backend is wanted. |
| `NIST CCCBDB 接口` | manual_api_review | `disabled_no_documented_api` | CCCBDB has no public documented REST/JSON API and is suitable only for limited interactive single-molecule webpage use. It remains outside BackendSpecs and is not exposed through MCP; no brittle page scraping or bulk crawler is added. |

## 8. 推荐优化顺序

1. **本地5个组合已修复。** Psi4向量API、CP2K显式打印/版本化解析和GROMACS ensemble字段均已通过真实后端复测。
2. **优先排查 PubChem 出口状态。** 当前响应明确显示 `Retry-After: 30` 和 `too many requests per second or blacklisted`；需检查共享 NAT/代理出口，代码不得伪造成功或隐藏切换数据源。
3. **在线韧性代码已落地。** PubChem/Catalysis-Hub 使用有界重试、Retry-After、跨 worker PubChem 限速和 `retryable` 错误语义；Catalysis-Hub 已现场恢复成功。
4. **为每个 Backend capability 保留一个小型真实 smoke。** 将原65个矩阵用例和7个 GoodVibes 用例长期纳入夜间/发布前矩阵，不必每次跑昂贵全量体系。
5. **PubChem解除阻塞后重跑六个网络用例。** 目标是 `successful_action_backend_pairs=241`、`failed=0`、`unobserved=0`。

## 9. 收尾校验

- MCP Catalog 校验：`ok: 106 actions, 76 backends, full exposure, agent-required backend selection, no fallback`。
- 完整测试集：`186 passed in 413.69s`。
- 矩阵审计测试会验证65个补测用例与 Catalog 一致，并验证241个组合被成功集与失败集完整划分。
- 修复涉及脚本和 Backend 模块的 `py_compile` 均通过。

## 10. 复现命令

```bash
.toolbox_env/bin/python chemistry_toolbox/scripts/run_action_backend_matrix_smokes.py --resume
.toolbox_env/bin/python chemistry_toolbox/scripts/run_action_gap_smokes.py --network-only
.toolbox_env/bin/python chemistry_toolbox/scripts/run_goodvibes_action_smokes.py
.tool_envs/services/bin/python chemistry_toolbox/scripts/check_pubchem_connectivity.py --output chemistry_toolbox/config/pubchem_connectivity_status.json
.toolbox_env/bin/python chemistry_toolbox/scripts/audit_action_test_coverage.py
.toolbox_env/bin/python chemistry_toolbox/scripts/generate_action_backend_completion_report.py
.toolbox_env/bin/python -m chemistry_toolbox.mcp.tool_manager validate
.toolbox_env/bin/python -m pytest -q chemistry_toolbox/tests
```

相关基线：[`CHEMISTRY_TOOLBOX_DETAILED_AUDIT_REPORT_20260720.md`](CHEMISTRY_TOOLBOX_DETAILED_AUDIT_REPORT_20260720.md)、[`CHEMISTRY_TOOLBOX_REQUESTED_SOFTWARE_STATUS.md`](CHEMISTRY_TOOLBOX_REQUESTED_SOFTWARE_STATUS.md)。
