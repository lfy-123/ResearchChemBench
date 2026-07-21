# ResearchChemBench Action–Backend 全组合测试与软件接入审计

> 生成时间：`2026-07-21T05:56:17.595014+00:00`。
> 本报告合并 2026-07-20 已有证据与本轮 62 个缺口组合的真实统一分发调用；已测试组合不会重复运行。

## 1. 最终结论

| 指标 | 结果 |
|---|---:|
| 公开 Actions | 101 |
| BackendSpecs | 76 |
| Catalog Action–Backend 组合 | 233 |
| 有成功证据的组合 | **222** |
| 仅有失败证据的组合 | **11** |
| 尚未测试组合 | **0** |
| 本轮补测 | 57/62 通过，5 失败 |
| 至少有一个成功 Action 的 Backend | 75/76 |
| 当前无任何成功证据的 Backend | `catalysis_hub` |

结论：**233/233 个声明组合现在都有真实调用证据；222 个通过，11 个仍有问题。** 其中5个是本地适配器问题，6个是远端数据服务问题。

## 2. 本轮补测结果

| 分组 | 组合数 | 通过 | 失败 |
|---|---:|---:|---:|
| 分子电子结构与ML势 | 27 | 25 | 2 |
| 周期材料与弛豫 | 18 | 16 | 2 |
| 分子动力学与溶剂化 | 8 | 7 | 1 |
| 轨迹分析与反应 | 5 | 5 | 0 |
| 声子 | 4 | 4 | 0 |

证据文件：[`action_backend_matrix_smoke_status.json`](../config/action_backend_matrix_smoke_status.json)、[`action_test_coverage.json`](../config/action_test_coverage.json)。

## 3. 出现问题的 Backend 调用及修复建议

### 3.1 11个仅失败组合

| 优先级 | Backend | Action | 问题类型 | 根因 | 建议修复 |
|---|---|---|---|---|---|
| P0 | `cp2k` | `calculate_periodic_forces` | 输入生成+输出解析 | CP2K `ENERGY_FORCE` 在当前输出级别不打印原子力；即使显式打印，CP2K 2026 的行带 `FORCES\|` 前缀，现有正则仍无法匹配。 | 在 `FORCE_EVAL/PRINT` 中加入 `FORCES ON`；解析 `FORCES\| <atom> <fx> <fy> <fz>` 块并忽略 Sum/Total 行，保留 hartree/bohr 或显式转换到 eV/Å。 |
| P0 | `cp2k` | `calculate_periodic_stress` | 输入生成+版本化输出解析 | 适配器只设置 `STRESS_TENSOR ANALYTICAL`，但没有显式打印块；解析器还期待旧式 `STRESS TENSOR [GPa]`，本机 CP2K 2026 输出为 `STRESS\| Analytical stress tensor [bar]`。 | 加入 `FORCE_EVAL/PRINT/STRESS_TENSOR ON`；解析带 `STRESS\|` 前缀的 x/y/z 三行，并将 bar 乘 `1e-4` 转为 GPa，同时保留原始单位元数据。 |
| P0 | `gromacs` | `propagate_dynamics` | 输入生成逻辑 | NVE 分支虽然写 `tcoupl=no`，仍无条件写入 `ref-t` 和 `tau-t`，且没有 `tc-grps`；GROMACS 2026 因温控组数量为0而拒绝 `grompp`。 | NVE 分支完全省略 `ref-t/tau-t/tc-grps` 和压力耦合字段；NVT/NPT 分支增加显式 `temperature_coupling_groups`（或受控的 `System`），并分别验证 NVE/NVT/NPT MDP。 |
| P0 | `psi4` | `calculate_dipole_moment` | 适配器/API不兼容 | 当前适配器读取已在 Psi4 1.6 后废弃的 `SCF DIPOLE X/Y/Z` 标量变量；本机 Psi4 要求读取向量变量 `SCF DIPOLE`，且单位从 Debye 改为原子单位。 | 改为一次读取 `numpy.asarray(psi4.core.variable('SCF DIPOLE'))`，乘以 `2.541746473` 转成 Debye；补充水分子非零偶极和单位回归测试。 |
| P0 | `psi4` | `calculate_orbitals` | 适配器/对称分块解析 | `wavefunction.epsilon_a()` 是按不可约表示分块的 Psi4 Vector；水分子保留 C2v 对称性时有多个 irrep，不能直接 `numpy.asarray()`。 | 使用 `epsilon_a().to_array()`/`epsilon_b().to_array()` 逐 irrep 展平，并用 `nalphapi()`/`nbetapi()`生成对应占据数；若不需要对称信息，也可显式使用 `symmetry c1`，但前者更稳健。 |
| P1 | `catalysis_hub` | `search_catalysis_records` | 远端服务503/超时 | Catalysis-Hub GraphQL 在两次已有实测中分别返回503和读取超时；该 Backend 尚无成功调用证据。 | 增加 GraphQL 健康检查、有界重试/退避、分页缓存和可选的本地只读快照；远端不可用时向智能体返回 retryable 状态，不做隐藏 fallback。 |
| P1 | `pubchem` | `resolve_chemical_identity` | 远端服务503 | PubChem PUG REST 返回 `PUGREST.ServerBusy`，不是本地依赖缺失。 | 加入尊重 `Retry-After` 的指数退避、抖动、全局限速和查询缓存；将503标为 `retryable=true`，禁止静默切换数据源。 |
| P1 | `pubchem` | `retrieve_compound_properties` | 远端服务503 | PubChem PUG REST 返回 `PUGREST.ServerBusy`。 | 与其他 PubChem Actions 共用有界重试、速率限制、缓存和可重试错误模型。 |
| P1 | `pubchem` | `retrieve_compound_structure` | 远端服务503 | PubChem PUG REST 返回 `PUGREST.ServerBusy`。 | 与其他 PubChem Actions 共用有界重试、速率限制、缓存和可重试错误模型。 |
| P1 | `pubchem` | `search_similar_compounds` | 远端服务503 | PubChem fast similarity 端点返回503。 | 对异步/慢搜索端点设置独立超时与轮询上限，使用有界重试和缓存；不要自动降低阈值或改换算法。 |
| P1 | `pubchem` | `search_substructures` | 远端服务503 | PubChem fast substructure 端点返回503。 | 对结构搜索使用有界重试、限速和缓存，并把服务繁忙与无匹配结果严格区分。 |

### 3.2 Backend级影响范围

| Backend | 已成功组合 | 失败组合 | 判断 |
|---|---:|---:|---|
| `catalysis_hub` | 0 | 1 | 唯一没有成功调用证据的 Backend，当前远端不可用。 |
| `cp2k` | 2 | 2 | 周期能量和结构弛豫可用；力和应力的打印/解析需修复。 |
| `gromacs` | 1 | 1 | 能量最小化可用；动力学 MDP 生成需修复。 |
| `psi4` | 3 | 2 | 能量、Hessian、原子电荷可用；偶极和轨道适配需修复。 |
| `pubchem` | 1 | 5 | 曾有成功证据，但本轮所有现场调用受远端503影响。 |

补充：`search_compounds/pubchem` 有历史成功证据，因此不属于“仅失败组合”；但最新现场 smoke 同样返回503，应与其他 PubChem Actions 一起按远端降级处理。

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
| 30 | `calculate_hessian` | 分子电子结构与派生性质 | ✅ `xtb`<br>✅ `pyscf`<br>✅ `psi4`<br>✅ `tblite`<br>✅ `nwchem`<br>✅ `orca`<br>✅ `gaussian`<br>✅ `ase_emt` |
| 31 | `optimize_geometry` | 分子电子结构与派生性质 | ✅ `xtb`<br>✅ `tblite`<br>✅ `gpaw`<br>✅ `mace`<br>✅ `chgnet`<br>✅ `deepmd`<br>✅ `orca`<br>✅ `gaussian`<br>✅ `gamess`<br>✅ `ase_emt`<br>✅ `geometric`<br>✅ `sella` |
| 32 | `calculate_dipole_moment` | 分子电子结构与派生性质 | ✅ `xtb`<br>✅ `tblite`<br>✅ `pyscf`<br>❌ `psi4`<br>✅ `nwchem`<br>✅ `openmolcas`<br>✅ `orca`<br>✅ `gaussian`<br>✅ `gamess` |
| 33 | `calculate_atomic_charges` | 分子电子结构与派生性质 | ✅ `xtb`<br>✅ `pyscf`<br>✅ `psi4`<br>✅ `nwchem`<br>✅ `openmolcas`<br>✅ `multiwfn`<br>✅ `orca` |
| 34 | `calculate_orbitals` | 分子电子结构与派生性质 | ✅ `pyscf`<br>❌ `psi4`<br>✅ `openmolcas`<br>✅ `orca` |
| 35 | `calculate_bond_orders` | 分子电子结构与派生性质 | ✅ `xtb`<br>✅ `multiwfn`<br>✅ `orca` |
| 36 | `calculate_excited_states` | 分子电子结构与派生性质 | ✅ `pyscf`<br>✅ `orca` |
| 37 | `analyze_electron_density_topology` | 分子电子结构与派生性质 | ✅ `critic2` |
| 38 | `calculate_atomic_basin_properties` | 分子电子结构与派生性质 | ✅ `critic2` |
| 39 | `calculate_bader_charges` | 分子电子结构与派生性质 | ✅ `critic2` |
| 40 | `derive_vibrational_modes` | 分子电子结构与派生性质 | ✅ `internal_vibrations` |
| 41 | `derive_ir_spectrum` | 分子电子结构与派生性质 | ✅ `internal_spectroscopy` |
| 42 | `derive_uv_vis_spectrum` | 分子电子结构与派生性质 | ✅ `internal_spectroscopy` |
| 43 | `derive_thermochemistry` | 分子电子结构与派生性质 | ✅ `internal_thermochemistry`<br>✅ `goodvibes` |
| 44 | `locate_transition_state` | 反应路径、平衡与动力学 | ✅ `pysisyphus`<br>✅ `sella` |
| 45 | `trace_intrinsic_reaction_coordinate` | 反应路径、平衡与动力学 | ✅ `pysisyphus` |
| 46 | `calculate_chemical_equilibrium` | 反应路径、平衡与动力学 | ✅ `cantera` |
| 47 | `integrate_reaction_network` | 反应路径、平衡与动力学 | ✅ `scipy`<br>✅ `cantera` |
| 48 | `calculate_rate_constants` | 反应路径、平衡与动力学 | ✅ `rmg` |
| 49 | `calculate_tunneling_correction` | 反应路径、平衡与动力学 | ✅ `rmg` |
| 50 | `solve_master_equation` | 反应路径、平衡与动力学 | ✅ `mess`<br>✅ `mesmer` |
| 51 | `solve_microkinetic_model` | 反应路径、平衡与动力学 | ✅ `catmap` |
| 52 | `minimize_system_energy` | 分子动力学、轨迹与自由能 | ✅ `openmm`<br>✅ `gromacs`<br>✅ `lammps`<br>✅ `hoomd`<br>✅ `namd`<br>✅ `amber_pmemd`<br>✅ `charmm` |
| 53 | `calculate_force_field_energy` | 分子动力学、轨迹与自由能 | ✅ `openmm`<br>✅ `hoomd` |
| 54 | `calculate_force_field_forces` | 分子动力学、轨迹与自由能 | ✅ `openmm`<br>✅ `hoomd` |
| 55 | `decompose_force_field_energy` | 分子动力学、轨迹与自由能 | ✅ `openmm` |
| 56 | `propagate_dynamics` | 分子动力学、轨迹与自由能 | ✅ `openmm`<br>❌ `gromacs`<br>✅ `lammps`<br>✅ `hoomd`<br>✅ `namd`<br>✅ `amber_pmemd`<br>✅ `charmm` |
| 57 | `calculate_trajectory_rmsd` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis`<br>✅ `mdtraj` |
| 58 | `calculate_radius_of_gyration` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis`<br>✅ `mdtraj` |
| 59 | `calculate_radial_distribution` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis` |
| 60 | `calculate_mean_squared_displacement` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis` |
| 61 | `calculate_contacts` | 分子动力学、轨迹与自由能 | ✅ `mdtraj` |
| 62 | `calculate_solvent_accessible_surface` | 分子动力学、轨迹与自由能 | ✅ `mdtraj` |
| 63 | `calculate_dihedral_distribution` | 分子动力学、轨迹与自由能 | ✅ `mdtraj`<br>✅ `mdanalysis` |
| 64 | `calculate_hydrogen_bonds` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis` |
| 65 | `calculate_principal_components` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis` |
| 66 | `calculate_dynamic_cross_correlation` | 分子动力学、轨迹与自由能 | ✅ `mdanalysis` |
| 67 | `assign_secondary_structure` | 分子动力学、轨迹与自由能 | ✅ `mdtraj` |
| 68 | `cluster_trajectory` | 分子动力学、轨迹与自由能 | ✅ `mdtraj` |
| 69 | `evaluate_collective_variables` | 分子动力学、轨迹与自由能 | ✅ `plumed` |
| 70 | `estimate_free_energy_difference` | 分子动力学、轨迹与自由能 | ✅ `pymbar` |
| 71 | `estimate_thermodynamic_expectations` | 分子动力学、轨迹与自由能 | ✅ `pymbar` |
| 72 | `calculate_potential_of_mean_force` | 分子动力学、轨迹与自由能 | ✅ `pymbar` |
| 73 | `analyze_free_energy_convergence` | 分子动力学、轨迹与自由能 | ✅ `pymbar` |
| 74 | `parse_alchemical_energy_data` | 分子动力学、轨迹与自由能 | ✅ `alchemlyb` |
| 75 | `calculate_periodic_energy` | 周期电子结构、声子与热输运 | ✅ `quantum_espresso`<br>✅ `cp2k`<br>✅ `siesta`<br>✅ `dftbplus`<br>✅ `abinit`<br>✅ `vasp`<br>✅ `gpaw`<br>✅ `nequip`<br>✅ `allegro`<br>✅ `deepmd` |
| 76 | `calculate_periodic_forces` | 周期电子结构、声子与热输运 | ✅ `quantum_espresso`<br>❌ `cp2k`<br>✅ `siesta`<br>✅ `dftbplus`<br>✅ `abinit`<br>✅ `vasp`<br>✅ `gpaw`<br>✅ `nequip`<br>✅ `allegro`<br>✅ `deepmd` |
| 77 | `calculate_periodic_stress` | 周期电子结构、声子与热输运 | ✅ `quantum_espresso`<br>❌ `cp2k`<br>✅ `abinit`<br>✅ `vasp`<br>✅ `gpaw`<br>✅ `nequip`<br>✅ `allegro`<br>✅ `deepmd` |
| 78 | `relax_periodic_structure` | 周期电子结构、声子与热输运 | ✅ `quantum_espresso`<br>✅ `cp2k`<br>✅ `siesta`<br>✅ `dftbplus`<br>✅ `abinit`<br>✅ `vasp`<br>✅ `gpaw`<br>✅ `nequip`<br>✅ `allegro`<br>✅ `deepmd` |
| 79 | `calculate_electronic_band_structure` | 周期电子结构、声子与热输运 | ✅ `gpaw` |
| 80 | `calculate_density_of_states` | 周期电子结构、声子与热输运 | ✅ `gpaw` |
| 81 | `calculate_projected_density_of_states` | 周期电子结构、声子与热输运 | ✅ `gpaw`<br>✅ `lobster` |
| 82 | `analyze_periodic_bonding` | 周期电子结构、声子与热输运 | ✅ `lobster` |
| 83 | `calculate_charge_spilling` | 周期电子结构、声子与热输运 | ✅ `lobster` |
| 84 | `generate_displaced_supercells` | 周期电子结构、声子与热输运 | ✅ `phonopy`<br>✅ `phono3py` |
| 85 | `assemble_force_constants` | 周期电子结构、声子与热输运 | ✅ `phonopy`<br>✅ `phono3py` |
| 86 | `calculate_phonon_dispersion` | 周期电子结构、声子与热输运 | ✅ `phonopy`<br>✅ `phono3py` |
| 87 | `calculate_phonon_density_of_states` | 周期电子结构、声子与热输运 | ✅ `phonopy`<br>✅ `phono3py` |
| 88 | `calculate_harmonic_thermodynamics` | 周期电子结构、声子与热输运 | ✅ `phonopy`<br>✅ `phono3py` |
| 89 | `calculate_phonon_group_velocities` | 周期电子结构、声子与热输运 | ✅ `phonopy`<br>✅ `phono3py` |
| 90 | `calculate_lattice_thermal_conductivity` | 周期电子结构、声子与热输运 | ✅ `phono3py`<br>✅ `shengbte` |
| 91 | `dock_ligand` | 分子对接 | ✅ `vina`<br>✅ `gnina` |
| 92 | `search_compounds` | 外部化学数据源 | ⚠️ `pubchem` |
| 93 | `resolve_chemical_identity` | 外部化学数据源 | ❌ `pubchem` |
| 94 | `retrieve_compound_properties` | 外部化学数据源 | ❌ `pubchem` |
| 95 | `retrieve_compound_structure` | 外部化学数据源 | ❌ `pubchem` |
| 96 | `search_similar_compounds` | 外部化学数据源 | ❌ `pubchem` |
| 97 | `search_substructures` | 外部化学数据源 | ❌ `pubchem` |
| 98 | `search_protein_structures` | 外部化学数据源 | ✅ `rcsb_pdb` |
| 99 | `search_materials` | 外部化学数据源 | ✅ `materials_project` |
| 100 | `search_catalysis_records` | 外部化学数据源 | ❌ `catalysis_hub` |
| 101 | `lookup_nist_webbook_species` | 外部化学数据源 | ✅ `nist_webbook` |

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
| `psi4` | Psi4 | `psi4` | `psi4`, `psi4` | 5 | ⚠️ 3成功 / 2失败 |
| `tblite` | TBLite | `quantum` | `tblite`, `ase` | 5 | ✅ 5/5 |
| `mace` | MACE | `mlip` | `mace.calculators`, `ase` | 3 | ✅ 3/3 |
| `chgnet` | CHGNet | `mlip` | `chgnet`, `ase` | 3 | ✅ 3/3 |
| `deepmd` | DeePMD-kit | `deepmd` | `dp`, `deepmd`, `ase` | 7 | ✅ 7/7 |
| `nequip` | NequIP | `nequip` | `nequip-train`, `nequip`, `torch`, `e3nn`, `ase` | 4 | ✅ 4/4 |
| `allegro` | Allegro | `nequip` | `allegro`, `nequip`, `torch`, `e3nn`, `ase` | 4 | ✅ 4/4 |
| `orca` | ORCA | `quantum` | `orca` | 9 | ✅ 9/9 |
| `gaussian` | Gaussian 16 | `gaussian` | `g16`, `formchk` | 4 | ✅ 4/4 |
| `gamess` | GAMESS | `gamess` | `rungms` | 3 | ✅ 3/3 |
| `ase_emt` | ASE EMT | `core` | `ase.calculators.emt` | 4 | ✅ 4/4 |
| `internal_vibrations` | ResearchChem vibrational analysis | `core` | `numpy` | 1 | ✅ 1/1 |
| `internal_spectroscopy` | ResearchChem spectrum builder | `core` | `numpy` | 2 | ✅ 2/2 |
| `internal_thermochemistry` | ResearchChem statistical thermochemistry | `core` | `ase`, `numpy` | 1 | ✅ 1/1 |
| `goodvibes` | GoodVibes | `reaction` | `goodvibes`, `goodvibes` | 1 | ✅ 1/1 |
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
| `gromacs` | GROMACS | `md` | `gmx` | 2 | ⚠️ 1成功 / 1失败 |
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
| `cp2k` | CP2K | `cp2k` | `cp2k` | 4 | ⚠️ 2成功 / 2失败 |
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
| `catalysis_hub` | Catalysis-Hub GraphQL | `services` | `httpx` | 1 | ❌ 0成功 / 1失败 |
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

1. **P0：先修5个本地组合。** Psi4向量API、CP2K显式打印与版本化解析、GROMACS ensemble分支都属于确定性代码问题，修复后可离线回归。
2. **P1：统一在线数据后端韧性。** 为 PubChem/Catalysis-Hub 增加限速、缓存、Retry-After、指数退避和 `retryable` 错误语义，但保持数据源选择权属于智能体。
3. **为每个 Backend capability 保留一个小型真实 smoke。** 将本轮62个用例长期纳入夜间/发布前矩阵，不必每次跑昂贵全量体系。
4. **按科学价值接入 runtime-only 软件。** 优先 Wannier90/Yambo、SHARC/Newton-X、TheoDORE；工作流框架保持为执行基础设施，不公开固定流程工具。
5. **修复后重新生成覆盖文件。** 目标是 `successful_action_backend_pairs=233`、`failed=0`、`unobserved=0`；在线服务故障应单列为环境状态而非伪装成本地成功。

## 9. 收尾校验

- MCP Catalog 校验：`ok: 101 actions, 76 backends, full exposure, agent-required backend selection, no fallback`。
- 完整测试集：`144 passed in 392.60s`。
- 新增矩阵审计测试会验证62个补测用例与历史缺口完全一致，并验证233个 Catalog 组合被成功集与失败集完整划分。
- `git diff --check` 与三个新增/修改脚本的 `py_compile` 均通过。

## 10. 复现命令

```bash
.toolbox_env/bin/python chemistry_toolbox/scripts/run_action_backend_matrix_smokes.py --resume
.toolbox_env/bin/python chemistry_toolbox/scripts/audit_action_test_coverage.py
.toolbox_env/bin/python chemistry_toolbox/scripts/generate_action_backend_completion_report.py
.toolbox_env/bin/python -m chemistry_toolbox.mcp.tool_manager validate
.toolbox_env/bin/python -m pytest -q chemistry_toolbox/tests
```

相关基线：[`CHEMISTRY_TOOLBOX_DETAILED_AUDIT_REPORT_20260720.md`](CHEMISTRY_TOOLBOX_DETAILED_AUDIT_REPORT_20260720.md)、[`CHEMISTRY_TOOLBOX_REQUESTED_SOFTWARE_STATUS.md`](CHEMISTRY_TOOLBOX_REQUESTED_SOFTWARE_STATUS.md)。
