# ResearchChemBench 当前化学工具箱能力目录

生成日期：2026-07-22  
Catalog hash：`624569cb8cc29310e5f1e078a4ac59751015fd755cff19ac4fb7cd1b470914dc`  
用途：帮助从计算化学论文中选择与当前工具箱能力匹配、同时又能评估 Agent 自主编排的软件和科学任务。

## 1. 当前规模与概念关系

- 预定义 Actions：**106**（Scientific 96，Data 10）。
- BackendSpecs：**76**。一个软件可因不同适配器/算法注册多个 Backend，一个 Backend 也可服务多个 Action。
- 软件、程序库、工作流组件和数据接口 inventory：**106**，当前探测可用 **92**。
- 其中直接注册 Backend 的 inventory 项：**76**；含 reviewed native command 的项：**56**。
- 可编程分析 runtime：**46**。
- 注册科学资源：**27**。
- 默认 MCP：20 个首屏工具；完整 Catalog 通过 progressive discovery 按需加载。

```text
论文科学步骤 ──> Action（做什么） ──> Backend（由谁实现）
                     │                    │
                     │                    ├─ Python 库/算法适配器
                     │                    ├─ 外部计算软件
                     │                    └─ 数据接口
                     ├─ 若已有 Action：execute_action
                     ├─ 若无 Action：软件原生输入 + submit_native_job
                     └─ 若需自定义分析：Agent 程序 + submit_analysis_program
```

因此本文档中的 Action 数、Backend 数和 software inventory 数不会相等，这是多对多关系，不是重复注册错误。

## 2. 按领域的 Action 覆盖与论文匹配建议

| 领域 | Action 数 | 主要用途 | 适合寻找的论文 | Action IDs |
|---|---:|---|---|---|
| `scientific_data_interchange` | 3 | Scientific records, schemas, and output parsing | 带 Gaussian/ORCA/NWChem 等输出、QCSchema 记录或需要统一解析/验证的论文 | `normalize_qcschema_molecule`<br>`validate_qcschema_record`<br>`parse_quantum_chemistry_output` |
| `structure_and_system` | 18 | Structure, conformers, charges, and system construction | 构象搜索、质子化、部分电荷、力场参数化、溶剂化、晶体/表面建模论文 | `standardize_structure`<br>`generate_3d_structure`<br>`generate_conformer_ensemble`<br>`cluster_conformers`<br>`align_molecular_structures`<br>`rank_conformers_from_results`<br>`repair_biomolecular_structure`<br>`select_structure_subset`<br>`renumber_biomolecular_structure`<br>`normalize_pdb_records`<br>`assign_protonation_states`<br>`assign_partial_charges`<br>`assign_force_field_parameters`<br>`solvate_molecular_system`<br>`analyze_crystal_symmetry`<br>`standardize_crystal_structure`<br>`build_supercell`<br>`enumerate_surface_slabs` |
| `cheminformatics` | 6 | Molecular descriptors, fingerprints, identifiers, and graph operations | 描述符、指纹、相似性、子结构和分子标识符数据集论文 | `calculate_molecular_descriptors`<br>`calculate_molecular_fingerprint`<br>`calculate_molecular_similarity`<br>`search_local_substructures`<br>`enumerate_tautomers`<br>`enumerate_stereoisomers` |
| `molecular_electronic` | 19 | Molecular electronic structure and derived properties | 分子 DFT/从头算、几何优化、频率、热化学、激发态、光谱和波函数分析论文 | `calculate_energy`<br>`calculate_forces`<br>`calculate_hessian`<br>`optimize_geometry`<br>`calculate_dipole_moment`<br>`calculate_atomic_charges`<br>`calculate_orbitals`<br>`calculate_bond_orders`<br>`calculate_excited_states`<br>`analyze_electron_density_topology`<br>`calculate_atomic_basin_properties`<br>`calculate_bader_charges`<br>`derive_vibrational_modes`<br>`derive_ir_spectrum`<br>`derive_uv_vis_spectrum`<br>`derive_thermochemistry`<br>`scan_thermochemistry_temperature`<br>`analyze_thermochemical_ensemble`<br>`validate_thermochemistry_inputs` |
| `reaction_and_kinetics` | 10 | Reaction paths, equilibrium, and kinetics | 反应路径、TS/IRC、自由能剖面、选择性、速率常数和反应网络论文 | `locate_transition_state`<br>`trace_intrinsic_reaction_coordinate`<br>`calculate_chemical_equilibrium`<br>`integrate_reaction_network`<br>`calculate_rate_constants`<br>`calculate_tunneling_correction`<br>`solve_master_equation`<br>`solve_microkinetic_model`<br>`analyze_thermochemical_selectivity`<br>`analyze_reaction_free_energy_profile` |
| `molecular_dynamics` | 23 | Molecular dynamics propagation and trajectory analysis | 经典/第一性原理/增强采样 MD、轨迹分析、自由能与输运论文 | `minimize_system_energy`<br>`calculate_force_field_energy`<br>`calculate_force_field_forces`<br>`decompose_force_field_energy`<br>`propagate_dynamics`<br>`calculate_trajectory_rmsd`<br>`calculate_radius_of_gyration`<br>`calculate_radial_distribution`<br>`calculate_mean_squared_displacement`<br>`calculate_contacts`<br>`calculate_solvent_accessible_surface`<br>`calculate_dihedral_distribution`<br>`calculate_hydrogen_bonds`<br>`calculate_principal_components`<br>`calculate_dynamic_cross_correlation`<br>`assign_secondary_structure`<br>`cluster_trajectory`<br>`evaluate_collective_variables`<br>`estimate_free_energy_difference`<br>`estimate_thermodynamic_expectations`<br>`calculate_potential_of_mean_force`<br>`analyze_free_energy_convergence`<br>`parse_alchemical_energy_data` |
| `periodic_and_phonons` | 16 | Periodic electronic structure and lattice dynamics | 周期 DFT、结构弛豫、能带/DOS、声子、热输运和多体材料计算论文 | `calculate_periodic_energy`<br>`calculate_periodic_forces`<br>`calculate_periodic_stress`<br>`relax_periodic_structure`<br>`calculate_electronic_band_structure`<br>`calculate_density_of_states`<br>`calculate_projected_density_of_states`<br>`analyze_periodic_bonding`<br>`calculate_charge_spilling`<br>`generate_displaced_supercells`<br>`assemble_force_constants`<br>`calculate_phonon_dispersion`<br>`calculate_phonon_density_of_states`<br>`calculate_harmonic_thermodynamics`<br>`calculate_phonon_group_velocities`<br>`calculate_lattice_thermal_conductivity` |
| `docking` | 1 | Molecular docking | 蛋白-配体对接、构象排序和结构准备论文 | `dock_ligand` |
| `data_sources` | 10 | External chemistry data sources | 需要 PubChem、NIST WebBook、Materials Project、PDB 等公开数据检索的任务 | `search_compounds`<br>`resolve_chemical_identity`<br>`retrieve_compound_properties`<br>`retrieve_compound_structure`<br>`search_similar_compounds`<br>`search_substructures`<br>`search_protein_structures`<br>`search_materials`<br>`search_catalysis_records`<br>`lookup_nist_webbook_species` |

## 3. 全部预定义 Actions

Action 是一个原子科学行为，不是固定 workflow。Agent 可自由组合、重复、分支或跳过。

| Action | 领域 | 功能 | 主输出 | 选择策略 | 必需输入 | 可选输入 | 可用 Backends |
|---|---|---|---|---|---|---|---|
| `normalize_qcschema_molecule` | `scientific_data_interchange` | Validate and normalize one supplied molecular structure into a QCSchema Molecule record without launching a calculation. | `QCSchemaMolecule` | `internal_deterministic` | `structure` | — | `qcelemental` (available) |
| `validate_qcschema_record` | `scientific_data_interchange` | Validate one explicit QCSchema/QCArchive record type and return a normalized record or structured validation errors without executing it. | `QCSchemaValidationResult` | `internal_deterministic` | `record` | — | `qcelemental` (available) |
| `parse_quantum_chemistry_output` | `scientific_data_interchange` | Parse explicitly selected properties from one existing quantum-chemistry output file without rerunning the calculation. | `ParsedQuantumChemistryResult` | `internal_deterministic` | `output_file` | — | `cclib` (available) |
| `standardize_structure` | `structure_and_system` | Standardize one molecular representation without generating 3D coordinates or optimizing geometry. | `AtomicStructure` | `agent_backend_required` | `structure` | — | `rdkit` (available) |
| `generate_3d_structure` | `structure_and_system` | Generate one explicit three-dimensional structure from a two-dimensional molecular representation. | `AtomicStructure` | `agent_backend_required` | `molecule` | — | `rdkit` (available)<br>`openbabel` (available) |
| `generate_conformer_ensemble` | `structure_and_system` | Generate a conformer ensemble; it does not perform the later quantum refinement or final ranking workflow. | `ConformerEnsemble` | `agent_backend_required` | `molecule` | `initial_structure` | `rdkit_etkdg` (available)<br>`crest` (available) |
| `cluster_conformers` | `structure_and_system` | Cluster an already supplied conformer ensemble by an explicit heavy/all-atom RMSD cutoff without generating or ranking conformers. | `ConformerClusterResult` | `agent_backend_required` | `ensemble` | — | `rdkit` (available) |
| `align_molecular_structures` | `structure_and_system` | Rigidly align one supplied 3D probe structure to a reference using an explicit atom-to-atom map. | `StructureAlignmentResult` | `agent_backend_required` | `reference`, `probe`, `atom_map` | — | `rdkit` (available) |
| `rank_conformers_from_results` | `structure_and_system` | Rank and weight conformers only from aligned energies or free energies already supplied by the agent. | `ConformerEnsemble` | `internal_deterministic` | `ensemble`, `scores` | — | `internal_statistics` (available) |
| `repair_biomolecular_structure` | `structure_and_system` | Repair missing biomolecular residues or atoms without choosing protonation, force field, solvent, or dynamics settings. | `AtomicStructure` | `agent_backend_required` | `structure` | — | `pdbfixer` (available) |
| `select_structure_subset` | `structure_and_system` | Select explicit chains and/or models from one PDB structure, with an explicit choice about retaining heteroatom records. | `AtomicStructure` | `internal_deterministic` | `structure` | — | `pdb_tools` (available) |
| `renumber_biomolecular_structure` | `structure_and_system` | Renumber PDB atom serials and residue identifiers from explicit starting values without changing coordinates or chemistry. | `AtomicStructure` | `internal_deterministic` | `structure` | — | `pdb_tools` (available) |
| `normalize_pdb_records` | `structure_and_system` | Sort and format one PDB record stream under explicit ordering, chain-break, and hybrid-36 choices. | `AtomicStructure` | `internal_deterministic` | `structure` | — | `pdb_tools` (available) |
| `assign_protonation_states` | `structure_and_system` | Assign explicit protonation states using the agent-selected backend and pH/rule settings. | `AtomicStructure` | `agent_backend_required` | `structure` | — | `rdkit` (available)<br>`pdbfixer` (available) |
| `assign_partial_charges` | `structure_and_system` | Assign named force-field or docking partial charges without parameterizing or solvating the system. | `ChargedStructure` | `agent_backend_required` | `structure` | — | `rdkit_gasteiger` (available)<br>`openff_am1bcc` (available) |
| `assign_force_field_parameters` | `structure_and_system` | Assign an explicitly selected force field to an already prepared molecular system. | `ParameterizedSystem` | `agent_backend_required` | `structure` | `charges` | `openff` (available)<br>`openmm_builder` (available) |
| `solvate_molecular_system` | `structure_and_system` | Build the explicitly requested solvent/ion environment without minimizing or propagating dynamics. | `ParameterizedSystem` | `agent_backend_required` | `system` | — | `openmm_builder` (available)<br>`packmol` (available) |
| `analyze_crystal_symmetry` | `structure_and_system` | Determine the crystallographic space group and symmetry-equivalent sites for one supplied periodic structure. | `CrystalSymmetryResult` | `agent_backend_required` | `structure` | — | `spglib` (available)<br>`pymatgen` (available) |
| `standardize_crystal_structure` | `structure_and_system` | Standardize one periodic structure in an explicitly selected primitive or conventional crystallographic setting. | `AtomicStructure` | `agent_backend_required` | `structure` | — | `spglib` (available)<br>`pymatgen` (available) |
| `build_supercell` | `structure_and_system` | Apply one explicit integer supercell transformation to a periodic structure. | `AtomicStructure` | `agent_backend_required` | `structure` | — | `pymatgen` (available) |
| `enumerate_surface_slabs` | `structure_and_system` | Enumerate a bounded set of symmetry-distinct slabs for one explicit Miller index and slab/vacuum geometry. | `StructureCollection` | `agent_backend_required` | `structure` | — | `pymatgen` (available) |
| `calculate_molecular_descriptors` | `cheminformatics` | Calculate an explicitly selected set of graph-based molecular descriptors without generating coordinates or running electronic structure. | `MolecularDescriptorResult` | `agent_backend_required` | `molecule` | — | `rdkit` (available) |
| `calculate_molecular_fingerprint` | `cheminformatics` | Calculate one explicitly selected molecular fingerprint representation. | `MolecularFingerprint` | `agent_backend_required` | `molecule` | — | `rdkit` (available) |
| `calculate_molecular_similarity` | `cheminformatics` | Calculate one similarity value between two molecules using an explicit fingerprint and metric. | `MolecularSimilarityResult` | `agent_backend_required` | `molecule_a`, `molecule_b` | — | `rdkit` (available) |
| `search_local_substructures` | `cheminformatics` | Find atom-index matches for an explicit SMARTS or SMILES query in one supplied molecule. | `SubstructureMatchResult` | `agent_backend_required` | `molecule`, `query` | — | `rdkit` (available) |
| `enumerate_tautomers` | `cheminformatics` | Enumerate bounded tautomeric forms without selecting a preferred tautomer for the agent. | `MoleculeCollection` | `agent_backend_required` | `molecule` | — | `rdkit` (available) |
| `enumerate_stereoisomers` | `cheminformatics` | Enumerate bounded stereoisomers under explicit uniqueness and assignment rules. | `MoleculeCollection` | `agent_backend_required` | `molecule` | — | `rdkit` (available) |
| `calculate_energy` | `molecular_electronic` | Calculate one molecular or non-periodic scalar energy with the exact software and method selected by the agent. | `EnergyResult` | `agent_backend_required` | `structure` | — | `xtb` (available)<br>`pyscf` (available)<br>`psi4` (available)<br>`tblite` (available)<br>`gpaw` (available)<br>`nwchem` (available)<br>`openmolcas` (available)<br>`mace` (available)<br>`chgnet` (available)<br>`deepmd` (available)<br>`orca` (available)<br>`gaussian` (available)<br>`gamess` (available)<br>`ase_emt` (available) |
| `calculate_forces` | `molecular_electronic` | Calculate atomic forces for one non-periodic structure or an aligned batch. | `ForceResult` | `agent_backend_required` | `structure` | — | `xtb` (available)<br>`pyscf` (available)<br>`tblite` (available)<br>`gpaw` (available)<br>`nwchem` (available)<br>`orca` (available)<br>`mace` (available)<br>`chgnet` (available)<br>`deepmd` (available)<br>`ase_emt` (available) |
| `calculate_hessian` | `molecular_electronic` | Calculate one molecular Hessian without deriving modes, spectra, or thermochemistry. | `Hessian` | `agent_backend_required` | `structure` | — | `xtb` (available)<br>`pyscf` (available)<br>`psi4` (available)<br>`tblite` (available)<br>`nwchem` (available)<br>`orca` (available)<br>`gaussian` (available)<br>`mace` (available)<br>`chgnet` (available)<br>`deepmd` (available)<br>`ase_emt` (available) |
| `optimize_geometry` | `molecular_electronic` | Optimize one non-periodic geometry and return the optimized structure only as the primary result. | `AtomicStructure` | `agent_backend_required` | `structure` | `constraints` | `xtb` (available)<br>`tblite` (available)<br>`gpaw` (available)<br>`mace` (available)<br>`chgnet` (available)<br>`deepmd` (available)<br>`orca` (available)<br>`gaussian` (available)<br>`gamess` (available)<br>`ase_emt` (available)<br>`geometric` (available)<br>`sella` (available) |
| `calculate_dipole_moment` | `molecular_electronic` | Calculate one molecular dipole moment with an explicitly chosen electronic method. | `DipoleResult` | `agent_backend_required` | `structure` | — | `xtb` (available)<br>`tblite` (available)<br>`pyscf` (available)<br>`psi4` (available)<br>`nwchem` (available)<br>`openmolcas` (available)<br>`orca` (available)<br>`gaussian` (available)<br>`gamess` (available) |
| `calculate_atomic_charges` | `molecular_electronic` | Calculate electronic-structure population-analysis charges without attaching force-field parameters. | `AtomicChargeResult` | `agent_backend_required` | `structure` | — | `xtb` (available)<br>`pyscf` (available)<br>`psi4` (available)<br>`nwchem` (available)<br>`openmolcas` (available)<br>`multiwfn` (available)<br>`orca` (available) |
| `calculate_orbitals` | `molecular_electronic` | Calculate orbital energies, occupations, and optional coefficient artifacts. | `OrbitalResult` | `agent_backend_required` | `structure` | — | `pyscf` (available)<br>`psi4` (available)<br>`openmolcas` (available)<br>`orca` (available) |
| `calculate_bond_orders` | `molecular_electronic` | Calculate atom-pair electronic bond-order indices using one explicitly selected population-analysis backend. | `BondOrderResult` | `agent_backend_required` | `structure` | — | `xtb` (available)<br>`multiwfn` (available)<br>`orca` (available) |
| `calculate_excited_states` | `molecular_electronic` | Calculate a bounded set of vertical electronic excited states without constructing a broadened spectrum or propagating dynamics. | `ExcitedStateResult` | `agent_backend_required` | `structure` | — | `pyscf` (available)<br>`orca` (available) |
| `analyze_electron_density_topology` | `molecular_electronic` | Locate and characterize critical points in one supplied molecular or periodic electron-density field without generating that field or integrating atomic basins. | `ElectronDensityTopologyResult` | `agent_backend_required` | `density_file` | `structure_file` | `critic2` (available) |
| `calculate_atomic_basin_properties` | `molecular_electronic` | Integrate population, Laplacian, and available volume properties over atomic or attractor basins in one supplied scalar-field grid using an explicitly selected partition algorithm. | `AtomicBasinPropertyResult` | `agent_backend_required` | `density_file` | `structure_file` | `critic2` (available) |
| `calculate_bader_charges` | `molecular_electronic` | Calculate atomic Bader charges from one supplied electron-density grid using an explicitly selected Yu-Trinkle or Henkelman grid partition. | `AtomicChargeResult` | `agent_backend_required` | `density_file` | `structure_file` | `critic2` (available) |
| `derive_vibrational_modes` | `molecular_electronic` | Derive frequencies and normal modes from an existing Hessian and structure. | `FrequencyResult` | `internal_deterministic` | `hessian`, `structure` | — | `internal_vibrations` (available) |
| `derive_ir_spectrum` | `molecular_electronic` | Construct an IR spectrum from vibration results that already contain intensities. | `SpectrumResult` | `internal_deterministic` | `vibrations` | — | `internal_spectroscopy` (available) |
| `derive_uv_vis_spectrum` | `molecular_electronic` | Construct a deterministic broadened UV/visible spectrum from supplied transition energies and oscillator strengths. | `SpectrumResult` | `internal_deterministic` | `excited_states` | — | `internal_spectroscopy` (available) |
| `derive_thermochemistry` | `molecular_electronic` | Derive thermochemical quantities from supplied electronic energy and frequencies; no optimization or Hessian is hidden. | `ThermochemistryResult` | `agent_backend_required` | — | `energy`, `frequencies`, `structure`, `output_file` | `internal_thermochemistry` (available)<br>`goodvibes` (available) |
| `scan_thermochemistry_temperature` | `molecular_electronic` | Evaluate thermochemical quantities for supplied quantum outputs at each explicitly listed temperature without rerunning electronic-structure calculations. | `ThermochemistryTemperatureSeries` | `agent_backend_required` | `output_files`, `temperatures_kelvin` | — | `goodvibes` (available) |
| `analyze_thermochemical_ensemble` | `molecular_electronic` | Calculate per-structure thermochemistry and Boltzmann populations for an explicitly supplied conformer or structure ensemble. | `ThermochemicalEnsembleResult` | `agent_backend_required` | `output_files` | — | `goodvibes` (available) |
| `validate_thermochemistry_inputs` | `molecular_electronic` | Check supplied quantum outputs for thermochemistry compatibility, calculation consistency, frequency issues, and possible duplicate structures. | `ThermochemistryValidationReport` | `agent_backend_required` | `output_files` | — | `goodvibes` (available) |
| `locate_transition_state` | `reaction_and_kinetics` | Locate one candidate transition-state structure without automatically running frequencies or IRC. | `AtomicStructure` | `agent_backend_required` | `initial_guess` | `reactant`, `product` | `pysisyphus` (available)<br>`sella` (available) |
| `trace_intrinsic_reaction_coordinate` | `reaction_and_kinetics` | Trace an IRC from an already supplied transition-state structure. | `ReactionPath` | `agent_backend_required` | `transition_state` | — | `pysisyphus` (available) |
| `calculate_chemical_equilibrium` | `reaction_and_kinetics` | Calculate an equilibrium composition/state for an explicitly supplied mechanism and thermodynamic condition. | `EquilibriumResult` | `agent_backend_required` | `composition` | `mechanism` | `cantera` (available) |
| `integrate_reaction_network` | `reaction_and_kinetics` | Integrate one explicitly specified reaction network over time. | `KineticsTrajectory` | `agent_backend_required` | `network`, `initial_state` | — | `scipy` (available)<br>`cantera` (available) |
| `calculate_rate_constants` | `reaction_and_kinetics` | Evaluate an explicitly supplied Arrhenius, multi-Arrhenius, pressure-dependent Arrhenius, or Chebyshev kinetics model on explicit temperature/pressure points. | `RateConstantResult` | `agent_backend_required` | `kinetics_model`, `temperatures_kelvin` | `pressures_pa` | `rmg` (available) |
| `calculate_tunneling_correction` | `reaction_and_kinetics` | Calculate Wigner or Eckart transition-state tunneling correction factors at explicit temperatures. | `TunnelingCorrectionResult` | `agent_backend_required` | `temperatures_kelvin`, `imaginary_frequency_cm1` | `reactant_energy_kj_mol`, `transition_state_energy_kj_mol`, `product_energy_kj_mol` | `rmg` (available) |
| `solve_master_equation` | `reaction_and_kinetics` | Solve an explicitly supplied gas-phase chemical master-equation model and extract pressure/temperature-dependent phenomenological rate coefficients without constructing or modifying the reaction model. | `MasterEquationResult` | `agent_backend_required` | `model_file` | `companion_files`, `model_relative_path` | `mess` (available)<br>`mesmer` (available) |
| `solve_microkinetic_model` | `reaction_and_kinetics` | Solve one explicitly supplied microkinetic model without constructing the reaction model for the agent. | `MicrokineticResult` | `agent_backend_required` | `model` | — | `catmap` (available) |
| `analyze_thermochemical_selectivity` | `reaction_and_kinetics` | Calculate N-way thermodynamic selectivity from explicitly labeled structure ensembles, including two-label excess and delta-delta-G when applicable. | `ThermochemicalSelectivityResult` | `agent_backend_required` | `output_files`, `label_groups` | — | `goodvibes` (available) |
| `analyze_reaction_free_energy_profile` | `reaction_and_kinetics` | Calculate relative electronic and thermochemical energies along explicitly defined reaction pathways, including stoichiometric sums and conformer ensembles. | `ReactionFreeEnergyProfileResult` | `agent_backend_required` | `output_files`, `profile_definition_file` | — | `goodvibes` (available) |
| `minimize_system_energy` | `molecular_dynamics` | Minimize an already parameterized system without automatically equilibrating or propagating dynamics. | `ParameterizedSystem` | `agent_backend_required` | `system` | — | `openmm` (available)<br>`gromacs` (available)<br>`lammps` (available)<br>`hoomd` (available)<br>`namd` (available)<br>`amber_pmemd` (available)<br>`charmm` (available) |
| `calculate_force_field_energy` | `molecular_dynamics` | Evaluate the total potential energy of an already parameterized system at explicitly selected stored coordinates/state without minimizing or propagating it. | `ForceFieldEnergyResult` | `agent_backend_required` | `system` | — | `openmm` (available)<br>`hoomd` (available) |
| `calculate_force_field_forces` | `molecular_dynamics` | Evaluate atomic force-field forces for an already parameterized system at explicitly selected stored coordinates/state. | `ForceResult` | `agent_backend_required` | `system` | — | `openmm` (available)<br>`hoomd` (available) |
| `decompose_force_field_energy` | `molecular_dynamics` | Decompose one OpenMM potential energy evaluation by the explicitly present Force objects without changing parameters or running dynamics. | `ForceFieldEnergyDecompositionResult` | `agent_backend_required` | `system` | — | `openmm` (available) |
| `propagate_dynamics` | `molecular_dynamics` | Propagate exactly one agent-defined dynamics segment and return its trajectory and final state. | `Trajectory` | `agent_backend_required` | `system` | — | `openmm` (available)<br>`gromacs` (available)<br>`lammps` (available)<br>`hoomd` (available)<br>`namd` (available)<br>`amber_pmemd` (available)<br>`charmm` (available) |
| `calculate_trajectory_rmsd` | `molecular_dynamics` | Calculate an RMSD time series for an explicitly selected trajectory atom group and reference. | `TimeSeries` | `agent_backend_required` | `trajectory`, `topology` | `reference` | `mdanalysis` (available)<br>`mdtraj` (available) |
| `calculate_radius_of_gyration` | `molecular_dynamics` | Calculate the radius-of-gyration time series for an explicitly selected atom group. | `TimeSeries` | `agent_backend_required` | `trajectory`, `topology` | — | `mdanalysis` (available)<br>`mdtraj` (available) |
| `calculate_radial_distribution` | `molecular_dynamics` | Calculate one radial distribution function for two explicitly selected atom groups. | `DistributionResult` | `agent_backend_required` | `trajectory`, `topology` | — | `mdanalysis` (available) |
| `calculate_mean_squared_displacement` | `molecular_dynamics` | Calculate one mean-squared-displacement time series for an explicitly selected atom group. | `TimeSeries` | `agent_backend_required` | `trajectory`, `topology` | — | `mdanalysis` (available) |
| `calculate_contacts` | `molecular_dynamics` | Calculate inter-residue contact distances for an explicitly supplied residue-pair set and contact definition. | `ContactTimeSeries` | `agent_backend_required` | `trajectory`, `topology`, `residue_pairs` | — | `mdtraj` (available) |
| `calculate_solvent_accessible_surface` | `molecular_dynamics` | Calculate solvent-accessible surface area per atom or residue for an existing trajectory. | `SurfaceAreaTimeSeries` | `agent_backend_required` | `trajectory`, `topology` | — | `mdtraj` (available) |
| `calculate_dihedral_distribution` | `molecular_dynamics` | Calculate dihedral-angle time series for explicitly supplied atom-index quartets. | `DihedralTimeSeries` | `agent_backend_required` | `trajectory`, `topology`, `atom_quartets` | — | `mdtraj` (available)<br>`mdanalysis` (available) |
| `calculate_hydrogen_bonds` | `molecular_dynamics` | Identify hydrogen-bond events in an existing trajectory using explicit donor, hydrogen, acceptor, distance, and angle definitions. | `HydrogenBondResult` | `agent_backend_required` | `trajectory`, `topology` | `between_selections` | `mdanalysis` (available) |
| `calculate_principal_components` | `molecular_dynamics` | Calculate coordinate principal components and frame projections for an explicitly selected trajectory atom group. | `PrincipalComponentResult` | `agent_backend_required` | `trajectory`, `topology` | — | `mdanalysis` (available) |
| `calculate_dynamic_cross_correlation` | `molecular_dynamics` | Calculate an atom-wise dynamic cross-correlation matrix from explicitly selected and optionally aligned trajectory coordinates. | `DynamicCrossCorrelationResult` | `agent_backend_required` | `trajectory`, `topology` | — | `mdanalysis` (available) |
| `assign_secondary_structure` | `molecular_dynamics` | Assign per-residue secondary-structure labels for every frame of an existing protein trajectory. | `SecondaryStructureTimeSeries` | `agent_backend_required` | `trajectory`, `topology` | — | `mdtraj` (available) |
| `cluster_trajectory` | `molecular_dynamics` | Cluster explicitly selected trajectory frames by RMSD using a deterministic cutoff-based leader assignment. | `TrajectoryClusterResult` | `agent_backend_required` | `trajectory`, `topology` | — | `mdtraj` (available) |
| `evaluate_collective_variables` | `molecular_dynamics` | Evaluate explicitly defined collective variables on an existing trajectory. | `TimeSeries` | `agent_backend_required` | `trajectory`, `topology`, `collective_variables` | — | `plumed` (available) |
| `estimate_free_energy_difference` | `molecular_dynamics` | Estimate dimensionless pairwise free-energy differences from an explicitly supplied reduced-potential matrix and sample counts. | `FreeEnergyDifferenceResult` | `agent_backend_required` | `reduced_potentials`, `samples_per_state` | — | `pymbar` (available) |
| `estimate_thermodynamic_expectations` | `molecular_dynamics` | Estimate state-resolved observable expectations from explicitly supplied samples and a reduced-potential matrix. | `ThermodynamicExpectationResult` | `agent_backend_required` | `reduced_potentials`, `samples_per_state`, `observables` | — | `pymbar` (available) |
| `calculate_potential_of_mean_force` | `molecular_dynamics` | Estimate a one-dimensional histogram free-energy profile from supplied uncorrelated samples; this does not integrate a mean-force trajectory or choose bins for the agent. | `FreeEnergyProfileResult` | `agent_backend_required` | `reduced_potentials`, `samples_per_state`, `target_reduced_potential`, `collective_variable` | — | `pymbar` (available) |
| `analyze_free_energy_convergence` | `molecular_dynamics` | Re-estimate one explicitly selected pairwise free-energy difference over supplied sample fractions without generating or decorrelating samples. | `FreeEnergyConvergenceResult` | `agent_backend_required` | `reduced_potentials`, `samples_per_state` | — | `pymbar` (available) |
| `parse_alchemical_energy_data` | `molecular_dynamics` | Parse one or more explicitly identified engine output files into a normalized alchemical reduced-potential or derivative table. | `AlchemicalEnergyData` | `agent_backend_required` | `files` | — | `alchemlyb` (available) |
| `calculate_periodic_energy` | `periodic_and_phonons` | Calculate one periodic-system energy with the explicitly selected electronic-structure backend. | `EnergyResult` | `agent_backend_required` | `structure` | — | `quantum_espresso` (available)<br>`cp2k` (available)<br>`siesta` (available)<br>`dftbplus` (available)<br>`abinit` (available)<br>`vasp` (available)<br>`gpaw` (available)<br>`nequip` (available)<br>`allegro` (available)<br>`deepmd` (available) |
| `calculate_periodic_forces` | `periodic_and_phonons` | Calculate periodic atomic forces for one structure or aligned displaced-structure batch. | `ForceResult` | `agent_backend_required` | `structure` | — | `quantum_espresso` (available)<br>`cp2k` (available)<br>`siesta` (available)<br>`dftbplus` (available)<br>`abinit` (available)<br>`vasp` (available)<br>`gpaw` (available)<br>`nequip` (available)<br>`allegro` (available)<br>`deepmd` (available) |
| `calculate_periodic_stress` | `periodic_and_phonons` | Calculate one periodic stress tensor without relaxing the structure. | `StressResult` | `agent_backend_required` | `structure` | — | `quantum_espresso` (available)<br>`cp2k` (available)<br>`abinit` (available)<br>`vasp` (available)<br>`gpaw` (available)<br>`nequip` (available)<br>`allegro` (available)<br>`deepmd` (available) |
| `relax_periodic_structure` | `periodic_and_phonons` | Relax a periodic structure under explicit atomic/cell constraints. | `AtomicStructure` | `agent_backend_required` | `structure` | — | `quantum_espresso` (available)<br>`cp2k` (available)<br>`siesta` (available)<br>`dftbplus` (available)<br>`abinit` (available)<br>`vasp` (available)<br>`gpaw` (available)<br>`nequip` (available)<br>`allegro` (available)<br>`deepmd` (available) |
| `calculate_electronic_band_structure` | `periodic_and_phonons` | Calculate electronic eigenvalue bands along one explicit reciprocal-space path from an existing converged periodic ground-state restart. | `ElectronicBandStructureResult` | `agent_backend_required` | `ground_state` | — | `gpaw` (available) |
| `calculate_density_of_states` | `periodic_and_phonons` | Calculate a total electronic density of states on an explicit energy grid from an existing converged periodic ground-state restart. | `DensityOfStatesResult` | `agent_backend_required` | `ground_state` | — | `gpaw` (available) |
| `calculate_projected_density_of_states` | `periodic_and_phonons` | Calculate or extract explicitly requested atom/orbital projected electronic densities of states from an existing compatible periodic electronic-state artifact. | `ProjectedDensityOfStatesResult` | `agent_backend_required` | `projections` | `ground_state`, `dos_file`, `structure_file` | `gpaw` (available)<br>`lobster` (available) |
| `analyze_periodic_bonding` | `periodic_and_phonons` | Extract explicitly selected integrated and optional energy-resolved COHP, COOP, or COBI bonding information from existing LOBSTER outputs. | `PeriodicBondingResult` | `agent_backend_required` | `integrated_bond_list` | `bond_curve_file` | `lobster` (available) |
| `calculate_charge_spilling` | `periodic_and_phonons` | Assess LOBSTER wavefunction-projection charge/total spilling against explicit acceptance thresholds from an existing lobsterout file. | `ProjectionQualityResult` | `agent_backend_required` | `lobster_output` | — | `lobster` (available) |
| `generate_displaced_supercells` | `periodic_and_phonons` | Generate a displacement set from an explicit supercell matrix and displacement amplitude. | `DisplacementSet` | `agent_backend_required` | `structure` | — | `phonopy` (available)<br>`phono3py` (available) |
| `assemble_force_constants` | `periodic_and_phonons` | Assemble force constants only from a supplied displacement set and aligned forces. | `ForceConstants` | `agent_backend_required` | `displacement_set`, `force_set` | — | `phonopy` (available)<br>`phono3py` (available) |
| `calculate_phonon_dispersion` | `periodic_and_phonons` | Calculate a phonon dispersion from existing force constants and an explicit q-point path. | `PhononDispersion` | `agent_backend_required` | `force_constants`, `structure` | — | `phonopy` (available)<br>`phono3py` (available) |
| `calculate_phonon_density_of_states` | `periodic_and_phonons` | Calculate a phonon density of states from existing force constants and an explicit q mesh. | `PhononDensityOfStates` | `agent_backend_required` | `force_constants`, `structure` | — | `phonopy` (available)<br>`phono3py` (available) |
| `calculate_harmonic_thermodynamics` | `periodic_and_phonons` | Calculate harmonic free energy, entropy, and constant-volume heat capacity at explicitly supplied temperatures. | `HarmonicThermodynamicsResult` | `agent_backend_required` | `force_constants`, `structure` | — | `phonopy` (available)<br>`phono3py` (available) |
| `calculate_phonon_group_velocities` | `periodic_and_phonons` | Calculate mode-resolved phonon group-velocity vectors along an explicitly supplied q-point path. | `PhononGroupVelocityResult` | `agent_backend_required` | `force_constants`, `structure` | — | `phonopy` (available)<br>`phono3py` (available) |
| `calculate_lattice_thermal_conductivity` | `periodic_and_phonons` | Calculate the lattice thermal-conductivity tensor from explicit second-/third-order force constants or a complete native BTE model under Agent-selected solution and scattering settings. | `LatticeThermalConductivityResult` | `agent_backend_required` | — | `second_order_force_constants`, `third_order_force_constants`, `structure`, `control_file`, `second_order_force_constants_file`, `third_order_force_constants_file`, `born_file`, `companion_files` | `phono3py` (available)<br>`shengbte` (available) |
| `dock_ligand` | `docking` | Dock an already prepared ligand into an already prepared receptor using an explicit search space. | `DockingResult` | `agent_backend_required` | `receptor`, `ligand`, `search_space` | `charges` | `vina` (available)<br>`gnina` (available) |
| `search_compounds` | `data_sources` | Search PubChem compound records by an explicit identifier and namespace. | `CompoundRecords` | `fixed_source` | `query` | — | `pubchem` (available) |
| `resolve_chemical_identity` | `data_sources` | Resolve one explicit compound identifier to a bounded ChemicalIdentity record through PubChem. | `ChemicalIdentity` | `fixed_source` | `query` | — | `pubchem` (available) |
| `retrieve_compound_properties` | `data_sources` | Retrieve an explicitly selected bounded property set for matching PubChem compounds. | `CompoundPropertyRecords` | `fixed_source` | `query` | — | `pubchem` (available) |
| `retrieve_compound_structure` | `data_sources` | Retrieve bounded PubChem 2D or 3D coordinate records while leaving coordinate dimensionality and explicit-hydrogen handling to the agent. | `StructureCollection` | `fixed_source` | `query` | — | `pubchem` (available) |
| `search_similar_compounds` | `data_sources` | Run one bounded PubChem 2D similarity search from an explicit structure identifier. | `CompoundRecords` | `fixed_source` | `query` | — | `pubchem` (available) |
| `search_substructures` | `data_sources` | Run one bounded PubChem substructure search from an explicit SMILES, SMARTS, InChI, or CID query. | `CompoundRecords` | `fixed_source` | `query` | — | `pubchem` (available) |
| `search_protein_structures` | `data_sources` | Search or retrieve RCSB PDB structure records using explicit identifiers or query terms. | `ProteinStructureRecords` | `fixed_source` | `query` | — | `rcsb_pdb` (available) |
| `search_materials` | `data_sources` | Search Materials Project records by material id, formula, or explicit query fields. | `MaterialRecords` | `fixed_source` | `query` | — | `materials_project` (unavailable) |
| `search_catalysis_records` | `data_sources` | Search Catalysis-Hub reaction records using explicit reactant/product filters. | `CatalysisRecords` | `fixed_source` | `query` | — | `catalysis_hub` (available) |
| `lookup_nist_webbook_species` | `data_sources` | Look up one bounded NIST Chemistry WebBook species query by explicit CAS number, exact name, or exact formula through the official CGI interface. | `NISTWebBookSpeciesRecords` | `fixed_source` | `query` | — | `nist_webbook` (available) |

## 4. 全部 BackendSpecs

| Backend | 显示名称 | Runtime | 状态 | License | 能力数 | Python modules | Executables | 外部资源 |
|---|---|---|---|---|---:|---|---|---|
| `qcelemental` | QCElemental | `workflows` | available | open_source | 2 | qcelemental | — | — |
| `cclib` | cclib | `workflows` | available | open_source | 1 | cclib | — | — |
| `rdkit` | RDKit | `core` | available | open_source | 11 | rdkit | — | — |
| `openbabel` | Open Babel | `quantum` | available | open_source | 1 | openbabel | obabel | — |
| `rdkit_etkdg` | RDKit ETKDG | `core` | available | open_source | 1 | rdkit | — | — |
| `crest` | CREST | `reaction` | available | open_source | 1 | — | crest | — |
| `internal_statistics` | ResearchChem deterministic statistics | `core` | available | open_source | 1 | — | — | — |
| `pdbfixer` | PDBFixer | `md` | available | open_source | 2 | pdbfixer, openmm | — | — |
| `pdb_tools` | pdb-tools | `core` | available | open_source | 3 | pdbtools | pdb_selchain, pdb_reres, pdb_tidy | — |
| `rdkit_gasteiger` | RDKit Gasteiger charges | `core` | available | open_source | 1 | rdkit | — | — |
| `openff_am1bcc` | OpenFF AM1-BCC | `openff` | available | open_source | 1 | openff.toolkit | antechamber, sqm | — |
| `openff` | OpenFF Toolkit/Interchange | `openff` | available | open_source | 1 | openff.toolkit, openff.interchange | — | — |
| `openmm_builder` | OpenMM system builder | `md` | available | open_source | 2 | openmm | — | — |
| `packmol` | Packmol | `md` | available | open_source | 1 | — | packmol | — |
| `spglib` | spglib | `workflows` | available | open_source | 2 | spglib, numpy | — | — |
| `pymatgen` | pymatgen | `workflows` | available | open_source | 4 | pymatgen, numpy | — | — |
| `xtb` | xTB | `quantum` | available | open_source | 7 | — | xtb | — |
| `pyscf` | PySCF | `quantum` | available | open_source | 7 | pyscf | — | — |
| `gpaw` | GPAW | `gpaw` | available | open_source | 10 | gpaw, ase, numpy | gpaw | GPAW PAW setup datasets under .software_cache/gpaw/setups |
| `lobster` | LOBSTER | `lobster` | available | academic_license | 3 | pymatgen, numpy | lobster-5.1.0 | — |
| `nwchem` | NWChem | `nwchem` | available | open_source | 5 | qcengine, qcelemental, numpy | nwchem | NWChem basis libraries under .software_cache/nwchem/source/src/basis/libraries |
| `openmolcas` | OpenMolcas | `openmolcas` | available | open_source | 4 | — | pymolcas | OpenMolcas v25.10 basis_library managed under .software_cache/openmolcas/25.10 |
| `multiwfn` | Multiwfn | `multiwfn` | available | custom_open_source_citation_required | 2 | — | Multiwfn_noGUI | Agent-supplied fch/fchk/wfn/wfx/mwfn/Molden/47 wavefunction file; both required Multiwfn citations are returned in provenance |
| `critic2` | Critic2 | `critic2` | available | open_source | 3 | — | critic2 | Agent-supplied electron-density grid or compatible wavefunction file; an explicit separate structure file is required when the density file does not contain geometry |
| `psi4` | Psi4 | `psi4` | available | open_source | 5 | psi4 | psi4 | — |
| `tblite` | TBLite | `quantum` | available | open_source | 5 | tblite, ase | — | — |
| `mace` | MACE | `mlip` | available | open_source | 4 | mace.calculators, ase | — | — |
| `chgnet` | CHGNet | `mlip` | available | open_source | 4 | chgnet, ase | — | — |
| `deepmd` | DeePMD-kit | `deepmd` | available | open_source | 8 | deepmd, ase | dp | Explicit resource:// DeePMD model checkpoint; multitask checkpoints require a named model_branch and single-task checkpoints require model_branch=single_task |
| `nequip` | NequIP | `nequip` | available | open_source | 4 | nequip, torch, e3nn, ase | nequip-train | Explicit resource:// NequIP checkpoint or workspace model ArtifactRef |
| `allegro` | Allegro | `nequip` | available | open_source | 4 | allegro, nequip, torch, e3nn, ase | — | Explicit resource:// Allegro checkpoint or workspace model ArtifactRef |
| `orca` | ORCA | `quantum` | available | manual_license | 9 | — | orca | — |
| `gaussian` | Gaussian 16 | `gaussian` | available | commercial_license | 4 | — | g16, formchk | — |
| `gamess` | GAMESS | `gamess` | available | registration_license | 3 | — | rungms | — |
| `ase_emt` | ASE EMT | `core` | available | open_source | 4 | ase.calculators.emt | — | — |
| `internal_vibrations` | ResearchChem vibrational analysis | `core` | available | open_source | 1 | ase, numpy | — | — |
| `internal_spectroscopy` | ResearchChem spectrum builder | `core` | available | open_source | 2 | numpy | — | — |
| `internal_thermochemistry` | ResearchChem statistical thermochemistry | `core` | available | open_source | 1 | ase, numpy | — | — |
| `goodvibes` | GoodVibes | `goodvibes` | available | open_source | 6 | goodvibes | goodvibes | — |
| `geometric` | geomeTRIC | `nwchem` | available | open_source | 1 | geometric, numpy | — | — |
| `sella` | Sella | `sella` | available | open_source | 2 | sella, ase, numpy | — | — |
| `pysisyphus` | pysisyphus | `reaction` | available | open_source | 2 | pysisyphus | pysis | — |
| `cantera` | Cantera | `reaction` | available | open_source | 2 | cantera | — | — |
| `scipy` | SciPy | `reaction` | available | open_source | 1 | scipy | — | — |
| `rmg` | RMG-Py | `rmg` | available | open_source | 2 | rmgpy | rmg.py | — |
| `mess` | MESS | `mess` | available | open_source | 1 | — | mess | — |
| `mesmer` | MESMER | `mesmer` | available | open_source | 1 | — | mesmer | — |
| `catmap` | CatMAP | `reaction` | available | open_source | 1 | catmap | — | — |
| `openmm` | OpenMM | `md` | available | open_source | 5 | openmm | — | — |
| `gromacs` | GROMACS | `md` | available | open_source | 2 | — | gmx | — |
| `lammps` | LAMMPS | `md` | available | open_source | 2 | lammps | lmp | — |
| `hoomd` | HOOMD-blue | `free_energy` | available | open_source | 4 | hoomd, numpy | — | — |
| `namd` | NAMD 3 | `namd` | available | academic_registration | 2 | — | namd3 | — |
| `amber_pmemd` | Amber 26 PMEMD | `amber` | available | academic_registration | 2 | — | pmemd, pmemd.MPI, mpirun | — |
| `charmm` | CHARMM c50b2 | `charmm` | available | academic_registration | 2 | — | charmm | — |
| `mdanalysis` | MDAnalysis | `md` | available | open_source | 8 | MDAnalysis | — | — |
| `mdtraj` | MDTraj | `workflows` | available | open_source | 7 | mdtraj, numpy | — | — |
| `plumed` | PLUMED | `md` | available | open_source | 1 | — | plumed | — |
| `pymbar` | PyMBAR | `free_energy` | available | open_source | 4 | pymbar, numpy | — | — |
| `alchemlyb` | alchemlyb | `free_energy` | available | open_source | 1 | alchemlyb, pandas, numpy | — | — |
| `quantum_espresso` | Quantum ESPRESSO | `qe` | available | open_source | 4 | — | pw.x | Explicit ResourceRefs from qe_sssp_1_3_pbe_efficiency or qe_sssp_1_3_pbe_precision, one per element; workspace ArtifactRefs remain accepted |
| `cp2k` | CP2K | `cp2k` | available | open_source | 4 | — | cp2k | — |
| `siesta` | SIESTA | `periodic` | available | open_source | 3 | — | siesta | Explicit ResourceRefs from siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml, one per element; workspace ArtifactRefs remain accepted |
| `dftbplus` | DFTB+ | `periodic` | available | open_source | 3 | — | dftb+ | Explicit ResourceRef to dftb_3ob_3_1 or dftb_matsci_0_3 with all required directed element-pair SKF files; workspace directory ArtifactRefs remain accepted |
| `abinit` | ABINIT | `abinit` | available | open_source | 4 | numpy, pydantic, yaml | abinit | Explicit ResourceRefs from abinit_pseudo_dojo_nc_sr_pbe_standard_psp8, one per element; workspace ArtifactRefs remain accepted |
| `vasp` | VASP | `vasp` | available | commercial_license | 4 | — | vasp_std | One explicit POTCAR ResourceRef or workspace ArtifactRef per element; five operator-supplied production families expose exact directory-name variants and no family or variant is selected automatically |
| `phonopy` | Phonopy | `phonons` | available | open_source | 6 | phonopy | phonopy | — |
| `phono3py` | Phono3py | `phonons` | available | open_source | 7 | phono3py | phono3py | — |
| `shengbte` | ShengBTE | `shengbte` | available | open_source | 1 | — | ShengBTE | — |
| `vina` | AutoDock Vina | `docking` | available | open_source | 1 | vina | vina | — |
| `gnina` | GNINA | `docking` | available | open_source | 1 | — | gnina | — |
| `pubchem` | PubChem PUG REST | `services` | available | open_source | 6 | pubchempy | — | — |
| `rcsb_pdb` | RCSB PDB Data API | `services` | available | open_source | 1 | httpx | — | — |
| `materials_project` | Materials Project | `services` | unavailable | open_source | 1 | httpx, mp_api | — | — |
| `catalysis_hub` | Catalysis-Hub GraphQL | `services` | available | open_source | 1 | httpx | — | — |
| `nist_webbook` | NIST Chemistry WebBook SRD 69 CGI | `services` | available | nist_srd_terms | 1 | httpx | — | NIST Chemistry WebBook SRD 69 official CGI and its SRD copyright/licensing terms |

### 4.1 Backend 到 Action 的完整映射

#### `qcelemental` — QCElemental

- 说明：QCElemental 0.50.4 schema models and physical-data normalization without calculation execution.
- Runtime：`workflows`；状态：`available`；License：`open_source`。
- Actions（2）：`normalize_qcschema_molecule`, `validate_qcschema_record`
- Conda：qcelemental=0.50.4；Pip：—。
- 安装说明：—

#### `cclib` — cclib

- 说明：cclib 1.8.1 parser for extracting selected properties from existing quantum-chemistry output files.
- Runtime：`workflows`；状态：`available`；License：`open_source`。
- Actions（1）：`parse_quantum_chemistry_output`
- Conda：cclib=1.8.1；Pip：—。
- 安装说明：—

#### `rdkit` — RDKit

- 说明：Cheminformatics structure standardization, hydrogen handling, and 3D embedding.
- Runtime：`core`；状态：`available`；License：`open_source`。
- Actions（11）：`standardize_structure`, `generate_3d_structure`, `assign_protonation_states`, `cluster_conformers`, `align_molecular_structures`, `calculate_molecular_descriptors`, `calculate_molecular_fingerprint`, `calculate_molecular_similarity`, `search_local_substructures`, `enumerate_tautomers`, `enumerate_stereoisomers`
- Conda：rdkit；Pip：—。
- 安装说明：—

#### `openbabel` — Open Babel

- 说明：Open Babel 3D coordinate generation.
- Runtime：`quantum`；状态：`available`；License：`open_source`。
- Actions（1）：`generate_3d_structure`
- Conda：openbabel；Pip：—。
- 安装说明：—

#### `rdkit_etkdg` — RDKit ETKDG

- 说明：RDKit ETKDG conformer generation with agent-selected sampling settings.
- Runtime：`core`；状态：`available`；License：`open_source`。
- Actions（1）：`generate_conformer_ensemble`
- Conda：rdkit；Pip：—。
- 安装说明：—

#### `crest` — CREST

- 说明：CREST conformer search from an explicit starting geometry.
- Runtime：`reaction`；状态：`available`；License：`open_source`。
- Actions（1）：`generate_conformer_ensemble`
- Conda：crest, xtb；Pip：—。
- 安装说明：—

#### `internal_statistics` — ResearchChem deterministic statistics

- 说明：Deterministic sorting, degeneracy handling, and Boltzmann weighting of supplied scores.
- Runtime：`core`；状态：`available`；License：`open_source`。
- Actions（1）：`rank_conformers_from_results`
- Conda：—；Pip：—。
- 安装说明：—

#### `pdbfixer` — PDBFixer

- 说明：Biomolecular structure repair and explicit pH-based hydrogen addition.
- Runtime：`md`；状态：`available`；License：`open_source`。
- Actions（2）：`repair_biomolecular_structure`, `assign_protonation_states`
- Conda：pdbfixer, openmm；Pip：—。
- 安装说明：—

#### `pdb_tools` — pdb-tools

- 说明：Composable pdb-tools 2.7.0 record transformations exposed as bounded typed structure actions.
- Runtime：`core`；状态：`available`；License：`open_source`。
- Actions（3）：`select_structure_subset`, `renumber_biomolecular_structure`, `normalize_pdb_records`
- Conda：—；Pip：pdb-tools==2.7.0。
- 安装说明：—

#### `rdkit_gasteiger` — RDKit Gasteiger charges

- 说明：Gasteiger partial-charge assignment on a fixed molecular graph.
- Runtime：`core`；状态：`available`；License：`open_source`。
- Actions（1）：`assign_partial_charges`
- Conda：rdkit；Pip：—。
- 安装说明：—

#### `openff_am1bcc` — OpenFF AM1-BCC

- 说明：OpenFF AM1-BCC partial-charge assignment through the AmberTools toolkit wrapper.
- Runtime：`openff`；状态：`available`；License：`open_source`。
- Actions（1）：`assign_partial_charges`
- Conda：openff-toolkit, ambertools；Pip：—。
- 安装说明：—

#### `openff` — OpenFF Toolkit/Interchange

- 说明：OpenFF force-field parameter assignment and interchange serialization.
- Runtime：`openff`；状态：`available`；License：`open_source`。
- Actions（1）：`assign_force_field_parameters`
- Conda：openff-toolkit, openff-interchange；Pip：—。
- 安装说明：—

#### `openmm_builder` — OpenMM system builder

- 说明：OpenMM force-field assignment and explicit solvent/ion construction.
- Runtime：`md`；状态：`available`；License：`open_source`。
- Actions（2）：`assign_force_field_parameters`, `solvate_molecular_system`
- Conda：openmm；Pip：—。
- 安装说明：—

#### `packmol` — Packmol

- 说明：Packmol construction of an explicitly specified molecular environment.
- Runtime：`md`；状态：`available`；License：`open_source`。
- Actions（1）：`solvate_molecular_system`
- Conda：packmol；Pip：—。
- 安装说明：—

#### `spglib` — spglib

- 说明：Crystallographic symmetry detection and cell standardization using explicit numerical tolerances.
- Runtime：`workflows`；状态：`available`；License：`open_source`。
- Actions（2）：`analyze_crystal_symmetry`, `standardize_crystal_structure`
- Conda：spglib, numpy；Pip：—。
- 安装说明：—

#### `pymatgen` — pymatgen

- 说明：Materials structure, symmetry, supercell, and surface-slab operations with all structural choices supplied by the Agent.
- Runtime：`workflows`；状态：`available`；License：`open_source`。
- Actions（4）：`analyze_crystal_symmetry`, `standardize_crystal_structure`, `build_supercell`, `enumerate_surface_slabs`
- Conda：pymatgen, numpy；Pip：—。
- 安装说明：—

#### `xtb` — xTB

- 说明：Standalone xTB GFN energy, derivative, optimization, dipole, and population-analysis calculations.
- Runtime：`quantum`；状态：`available`；License：`open_source`。
- Actions（7）：`calculate_energy`, `calculate_forces`, `calculate_hessian`, `optimize_geometry`, `calculate_dipole_moment`, `calculate_atomic_charges`, `calculate_bond_orders`
- Conda：xtb；Pip：—。
- 安装说明：—

#### `pyscf` — PySCF

- 说明：PySCF molecular Hartree-Fock and density-functional energies, analytic derivatives, and electronic properties.
- Runtime：`quantum`；状态：`available`；License：`open_source`。
- Actions（7）：`calculate_energy`, `calculate_forces`, `calculate_hessian`, `calculate_dipole_moment`, `calculate_atomic_charges`, `calculate_orbitals`, `calculate_excited_states`
- Conda：—；Pip：pyscf。
- 安装说明：—

#### `gpaw` — GPAW

- 说明：GPAW real-space, LCAO, or plane-wave DFT with explicit representation, PAW setup, k-point, spin, and convergence choices.
- Runtime：`gpaw`；状态：`available`；License：`open_source`。
- Actions（10）：`calculate_energy`, `calculate_forces`, `optimize_geometry`, `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure`, `calculate_electronic_band_structure`, `calculate_density_of_states`, `calculate_projected_density_of_states`
- Conda：gpaw=25.7.0, ase, numpy；Pip：—。
- 安装说明：—

#### `lobster` — LOBSTER

- 说明：LOBSTER 5.1.0 periodic bonding, projected-DOS, and projection-quality postprocessing from explicit existing output Artifacts.
- Runtime：`lobster`；状态：`available`；License：`academic_license`。
- Actions（3）：`analyze_periodic_bonding`, `calculate_projected_density_of_states`, `calculate_charge_spilling`
- Conda：pymatgen；Pip：—。
- 安装说明：Operator-supplied LOBSTER 5.1.0 is cached locally with its User Guide and FAQ. These public actions parse bounded existing outputs and do not expose arbitrary lobsterin execution.

#### `nwchem` — NWChem

- 说明：NWChem single-geometry QCSchema calculations through QCEngine with explicit method, basis, convergence, and population/property requests.
- Runtime：`nwchem`；状态：`available`；License：`open_source`。
- Actions（5）：`calculate_energy`, `calculate_forces`, `calculate_hessian`, `calculate_dipole_moment`, `calculate_atomic_charges`
- Conda：nwchem=7.3.1, qcengine=0.50.0, qcelemental=0.50.4, cclib；Pip：—。
- 安装说明：—

#### `openmolcas` — OpenMolcas

- 说明：OpenMolcas v25.10 molecular HF/Kohn-Sham SCF energy, dipole, Mulliken-charge, and orbital-property calculations from typed structures and explicit SCF controls.
- Runtime：`openmolcas`；状态：`available`；License：`open_source`。
- Actions（4）：`calculate_energy`, `calculate_dipole_moment`, `calculate_atomic_charges`, `calculate_orbitals`
- Conda：—；Pip：—。
- 安装说明：Locally compiled OpenMolcas v25.10 serial/OpenMP build with built-in Libxc.

#### `multiwfn` — Multiwfn

- 说明：Multiwfn 2026.7.15 noGUI wavefunction post-processing for explicit Mulliken/Lowdin atomic charges and Mayer/Wiberg-Lowdin/Mulliken bond-order definitions.
- Runtime：`multiwfn`；状态：`available`；License：`custom_open_source_citation_required`。
- Actions（2）：`calculate_atomic_charges`, `calculate_bond_orders`
- Conda：—；Pip：—。
- 安装说明：Official 2026.7.15 Linux noGUI binary is managed under .software_cache/multiwfn; the adapter uses fixed version-specific menu sequences and accepts no arbitrary menu script.

#### `critic2` — Critic2

- 说明：Critic2 1.2.1081 QTAIM critical-point search and typed grid-basin integration over Agent-supplied fields.
- Runtime：`critic2`；状态：`available`；License：`open_source`。
- Actions（3）：`analyze_electron_density_topology`, `calculate_atomic_basin_properties`, `calculate_bader_charges`
- Conda：—；Pip：—。
- 安装说明：The locally compiled GPL-3.0 development build is managed under .software_cache/critic2/install-conda. The adapter exposes typed AUTO/CPREPORT controls and never accepts an arbitrary Critic2 command script.

#### `psi4` — Psi4

- 说明：Psi4 molecular electronic-structure calculations.
- Runtime：`psi4`；状态：`available`；License：`open_source`。
- Actions（5）：`calculate_energy`, `calculate_hessian`, `calculate_dipole_moment`, `calculate_atomic_charges`, `calculate_orbitals`
- Conda：psi4；Pip：—。
- 安装说明：—

#### `tblite` — TBLite

- 说明：TBLite GFN calculator through its Python/ASE interface.
- Runtime：`quantum`；状态：`available`；License：`open_source`。
- Actions（5）：`calculate_energy`, `calculate_forces`, `calculate_hessian`, `optimize_geometry`, `calculate_dipole_moment`
- Conda：—；Pip：tblite==0.4.0。
- 安装说明：—

#### `mace` — MACE

- 说明：MACE machine-learned interatomic potential with explicit model/device selection.
- Runtime：`mlip`；状态：`available`；License：`open_source`。
- Actions（4）：`calculate_energy`, `calculate_forces`, `calculate_hessian`, `optimize_geometry`
- Conda：—；Pip：mace-torch==0.3.16。
- 安装说明：—

#### `chgnet` — CHGNet

- 说明：CHGNet machine-learned interatomic potential with explicit model/device selection.
- Runtime：`mlip`；状态：`available`；License：`open_source`。
- Actions（4）：`calculate_energy`, `calculate_forces`, `calculate_hessian`, `optimize_geometry`
- Conda：—；Pip：chgnet。
- 安装说明：—

#### `deepmd` — DeePMD-kit

- 说明：DeePMD inference from an exact registered checkpoint and an explicit multitask branch; the adapter never chooses or downloads a model.
- Runtime：`deepmd`；状态：`available`；License：`open_source`。
- Actions（8）：`calculate_energy`, `calculate_forces`, `calculate_hessian`, `optimize_geometry`, `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure`
- Conda：—；Pip：deepmd-kit==3.2.0b0, ase, e3nn。
- 安装说明：—

#### `nequip` — NequIP

- 说明：NequIP inference from the exact checkpoint and species mapping selected by the Agent.
- Runtime：`nequip`；状态：`available`；License：`open_source`。
- Actions（4）：`calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure`
- Conda：—；Pip：nequip==0.19.0。
- 安装说明：—

#### `allegro` — Allegro

- 说明：Allegro inference through the NequIP integration using the exact checkpoint and species mapping selected by the Agent.
- Runtime：`nequip`；状态：`available`；License：`open_source`。
- Actions（4）：`calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure`
- Conda：—；Pip：nequip-allegro==0.8.3, nequip==0.19.0。
- 安装说明：—

#### `orca` — ORCA

- 说明：Operator-provided ORCA 6.1.1 electronic-structure executable with an isolated OpenMPI 4.1.8 runtime.
- Runtime：`quantum`；状态：`available`；License：`manual_license`。
- Actions（9）：`calculate_energy`, `calculate_forces`, `calculate_hessian`, `optimize_geometry`, `calculate_dipole_moment`, `calculate_atomic_charges`, `calculate_orbitals`, `calculate_bond_orders`, `calculate_excited_states`
- Conda：—；Pip：—。
- 安装说明：Configured from the operator-downloaded ORCA 6.1.1 installer under .software_cache/orca/6.1.1 with OpenMPI 4.1.8.

#### `gaussian` — Gaussian 16

- 说明：Operator-provided Gaussian 16 C.01 SCF/DFT jobs rendered from typed molecular structures and explicit method settings.
- Runtime：`gaussian`；状态：`available`；License：`commercial_license`。
- Actions（4）：`calculate_energy`, `calculate_hessian`, `optimize_geometry`, `calculate_dipole_moment`
- Conda：—；Pip：—。
- 安装说明：Configured from the operator-provided Gaussian 16 C.01 distribution under .software_cache/gaussian/g16; the adapter accepts no arbitrary route deck.

#### `gamess` — GAMESS

- 说明：Operator-registered GAMESS 15 Jul 2024 R2 Patch 1 molecular SCF/DFT calculations through a typed input renderer.
- Runtime：`gamess`；状态：`available`；License：`registration_license`。
- Actions（3）：`calculate_energy`, `optimize_geometry`, `calculate_dipole_moment`
- Conda：—；Pip：—。
- 安装说明：The registered source distribution is compiled under .software_cache/gamess/2024-r2-p1 with a sockets DDI build and isolated compiler/runtime libraries.

#### `ase_emt` — ASE EMT

- 说明：ASE bundled EMT reference calculator, mainly for validation and small supported element sets.
- Runtime：`core`；状态：`available`；License：`open_source`。
- Actions（4）：`calculate_energy`, `calculate_forces`, `calculate_hessian`, `optimize_geometry`
- Conda：—；Pip：ase。
- 安装说明：—

#### `internal_vibrations` — ResearchChem vibrational analysis

- 说明：Mass-weighted Hessian diagonalization with explicit units and linearity handling.
- Runtime：`core`；状态：`available`；License：`open_source`。
- Actions（1）：`derive_vibrational_modes`
- Conda：—；Pip：ase, numpy。
- 安装说明：—

#### `internal_spectroscopy` — ResearchChem spectrum builder

- 说明：Deterministic line/broadened spectrum construction from supplied frequencies and intensities.
- Runtime：`core`；状态：`available`；License：`open_source`。
- Actions（2）：`derive_ir_spectrum`, `derive_uv_vis_spectrum`
- Conda：—；Pip：numpy。
- 安装说明：—

#### `internal_thermochemistry` — ResearchChem statistical thermochemistry

- 说明：Ideal-gas rigid-rotor/harmonic-oscillator thermochemistry from supplied results.
- Runtime：`core`；状态：`available`；License：`open_source`。
- Actions（1）：`derive_thermochemistry`
- Conda：—；Pip：ase, numpy。
- 安装说明：—

#### `goodvibes` — GoodVibes

- 说明：GoodVibes 4.3.0 post-processing for explicit Gaussian, ORCA, NWChem, Q-Chem, xTB, or ASE-extxyz outputs: RRHO/quasi-harmonic thermochemistry, temperature analysis, conformer populations, selectivity, consistency checks, and reaction free-energy profiles. It never runs or chooses the upstream quantum calculation.
- Runtime：`goodvibes`；状态：`available`；License：`open_source`。
- Actions（6）：`derive_thermochemistry`, `scan_thermochemistry_temperature`, `analyze_thermochemical_ensemble`, `validate_thermochemistry_inputs`, `analyze_thermochemical_selectivity`, `analyze_reaction_free_energy_profile`
- Conda：—；Pip：goodvibes[full]==4.3.0。
- 安装说明：Pinned GoodVibes 4.3.0 with full JSON/CSV/Parquet/plot dependencies; official v4.3.0 source and examples are cached under .software_cache/goodvibes/4.3.0/source.

#### `geometric` — geomeTRIC

- 说明：geomeTRIC 1.1.1 molecular geometry optimization driven by the exact energy/force backend and settings selected in component_backends.calculator.
- Runtime：`nwchem`；状态：`available`；License：`open_source`。
- Actions（1）：`optimize_geometry`
- Conda：—；Pip：geometric==1.1.1。
- 安装说明：—

#### `sella` — Sella

- 说明：Sella 2.5.0 order-0 minimum optimization and order-1 transition-state search driven by the exact energy/force backend and settings selected in component_backends.calculator.
- Runtime：`sella`；状态：`available`；License：`open_source`。
- Actions（2）：`optimize_geometry`, `locate_transition_state`
- Conda：—；Pip：sella==2.5.0。
- 安装说明：—

#### `pysisyphus` — pysisyphus

- 说明：pysisyphus transition-state and IRC algorithms using explicit endpoint/calculator settings.
- Runtime：`reaction`；状态：`available`；License：`open_source`。
- Actions（2）：`locate_transition_state`, `trace_intrinsic_reaction_coordinate`
- Conda：—；Pip：pysisyphus==1.0.0。
- 安装说明：—

#### `cantera` — Cantera

- 说明：Cantera equilibrium and mechanism-based kinetic integration.
- Runtime：`reaction`；状态：`available`；License：`open_source`。
- Actions（2）：`calculate_chemical_equilibrium`, `integrate_reaction_network`
- Conda：cantera；Pip：—。
- 安装说明：—

#### `scipy` — SciPy

- 说明：SciPy integration of an explicitly supplied mass-action network.
- Runtime：`reaction`；状态：`available`；License：`open_source`。
- Actions（1）：`integrate_reaction_network`
- Conda：—；Pip：scipy。
- 安装说明：—

#### `rmg` — RMG-Py

- 说明：RMG-Py 4.0.0 typed kinetics-model evaluation and Wigner/Eckart tunneling factors without mechanism generation or hidden database selection.
- Runtime：`rmg`；状态：`available`；License：`open_source`。
- Actions（2）：`calculate_rate_constants`, `calculate_tunneling_correction`
- Conda：rmg=4.0.0；Pip：—。
- 安装说明：—

#### `mess` — MESS

- 说明：MESS 2020.1.24 multi-well gas-phase master-equation solution from an Agent-supplied native model, with structured finite/high-pressure rate-table extraction.
- Runtime：`mess`；状态：`available`；License：`open_source`。
- Actions（1）：`solve_master_equation`
- Conda：—；Pip：—。
- 安装说明：Locally compiled PAPR MESS 2020.1.24 runtime and official manual/examples.

#### `mesmer` — MESMER

- 说明：MESMER 7.1 energy-grained master-equation solution from an Agent-supplied XML model, with structured first- and second-order phenomenological rate extraction.
- Runtime：`mesmer`；状态：`available`；License：`open_source`。
- Actions（1）：`solve_master_equation`
- Conda：—；Pip：—。
- 安装说明：Locally compiled official MESMER 7.1 SourceForge release and manual/examples.

#### `catmap` — CatMAP

- 说明：CatMAP 0.3.x microkinetic solver through an allow-listed typed model adapter that generates a controlled setup file and returns structured descriptor maps.
- Runtime：`reaction`；状态：`available`；License：`open_source`。
- Actions（1）：`solve_microkinetic_model`
- Conda：—；Pip：git+https://github.com/SUNCAT-Center/catmap.git。
- 安装说明：—

#### `openmm` — OpenMM

- 说明：OpenMM force/energy evaluation, force-object decomposition, minimization, and one-segment dynamics propagation.
- Runtime：`md`；状态：`available`；License：`open_source`。
- Actions（5）：`minimize_system_energy`, `propagate_dynamics`, `calculate_force_field_energy`, `calculate_force_field_forces`, `decompose_force_field_energy`
- Conda：openmm；Pip：—。
- 安装说明：—

#### `gromacs` — GROMACS

- 说明：GROMACS execution from typed ParameterizedSystem artifacts and explicit segment settings.
- Runtime：`md`；状态：`available`；License：`open_source`。
- Actions（2）：`minimize_system_energy`, `propagate_dynamics`
- Conda：gromacs；Pip：—。
- 安装说明：For propagate_dynamics, generate_velocities=true also requires an explicit random_seed. NVT/NPT additionally require explicit temperature_coupling_groups; no coupling group is chosen implicitly.

#### `lammps` — LAMMPS

- 说明：LAMMPS execution from typed ParameterizedSystem artifacts and explicit segment settings.
- Runtime：`md`；状态：`available`；License：`open_source`。
- Actions（2）：`minimize_system_energy`, `propagate_dynamics`
- Conda：lammps；Pip：—。
- 安装说明：—

#### `hoomd` — HOOMD-blue

- 说明：HOOMD-blue typed particle simulations with explicit device, reduced-unit force field, integration method, and segment controls.
- Runtime：`free_energy`；状态：`available`；License：`open_source`。
- Actions（4）：`minimize_system_energy`, `propagate_dynamics`, `calculate_force_field_energy`, `calculate_force_field_forces`
- Conda：hoomd=7.1.0, numpy；Pip：—。
- 安装说明：—

#### `namd` — NAMD 3

- 说明：NAMD 3.0.2 execution of exactly one minimization or dynamics segment from an explicitly supplied CHARMM-format system.
- Runtime：`namd`；状态：`available`；License：`academic_registration`。
- Actions（2）：`minimize_system_energy`, `propagate_dynamics`
- Conda：—；Pip：—。
- 安装说明：The AVX-512 multicore and CUDA bundles are cached under .software_cache/namd/3.0.2. The public backend selects the validated CPU AVX-512 binary only; CUDA is never chosen implicitly.

#### `amber_pmemd` — Amber 26 PMEMD

- 说明：Amber 26 PMEMD CPU serial or Agent-sized MPI execution of one typed minimization/dynamics segment.
- Runtime：`amber`；状态：`available`；License：`academic_registration`。
- Actions（2）：`minimize_system_energy`, `propagate_dynamics`
- Conda：—；Pip：—。
- 安装说明：Licensed PMEMD26 CPU serial and MPI binaries are built under .software_cache/amber/26. AmberTools 26 remains independently available in the OpenFF runtime.

#### `charmm` — CHARMM c50b2

- 说明：CHARMM c50b2 execution of one typed minimization or NVE/NVT dynamics segment from a pre-parameterized PSF/coordinate system.
- Runtime：`charmm`；状态：`available`；License：`academic_registration`。
- Actions（2）：`minimize_system_energy`, `propagate_dynamics`
- Conda：—；Pip：—。
- 安装说明：The operator-provided CHARMM c50b2 source is compiled as a serial/OpenMP GNU build under .software_cache/charmm/50b2; arbitrary CHARMM input scripts are not accepted.

#### `mdanalysis` — MDAnalysis

- 说明：Trajectory analysis with explicit atom selections and analysis parameters.
- Runtime：`md`；状态：`available`；License：`open_source`。
- Actions（8）：`calculate_trajectory_rmsd`, `calculate_radius_of_gyration`, `calculate_radial_distribution`, `calculate_mean_squared_displacement`, `calculate_dihedral_distribution`, `calculate_hydrogen_bonds`, `calculate_principal_components`, `calculate_dynamic_cross_correlation`
- Conda：—；Pip：MDAnalysis。
- 安装说明：—

#### `mdtraj` — MDTraj

- 说明：Trajectory I/O and explicit geometric analyses using atom/residue indices supplied by the Agent.
- Runtime：`workflows`；状态：`available`；License：`open_source`。
- Actions（7）：`calculate_trajectory_rmsd`, `calculate_radius_of_gyration`, `calculate_contacts`, `calculate_solvent_accessible_surface`, `calculate_dihedral_distribution`, `assign_secondary_structure`, `cluster_trajectory`
- Conda：mdtraj, numpy；Pip：—。
- 安装说明：—

#### `plumed` — PLUMED

- 说明：PLUMED driver evaluation of supplied collective-variable definitions; optional action_settings box_angstrom, timestep_ps, and trajectory_stride provide explicit metadata when the trajectory does not contain it.
- Runtime：`md`；状态：`available`；License：`open_source`。
- Actions（1）：`evaluate_collective_variables`
- Conda：plumed；Pip：—。
- 安装说明：—

#### `pymbar` — PyMBAR

- 说明：Multistate Bennett estimation, observable reweighting, and explicit-prefix convergence analysis from supplied reduced potentials; no simulation or state selection is hidden.
- Runtime：`free_energy`；状态：`available`；License：`open_source`。
- Actions（4）：`estimate_free_energy_difference`, `estimate_thermodynamic_expectations`, `calculate_potential_of_mean_force`, `analyze_free_energy_convergence`
- Conda：pymbar, numpy；Pip：—。
- 安装说明：—

#### `alchemlyb` — alchemlyb

- 说明：Engine-aware parsing and normalization of alchemical energy outputs without choosing an estimator or discarding samples implicitly.
- Runtime：`free_energy`；状态：`available`；License：`open_source`。
- Actions（1）：`parse_alchemical_energy_data`
- Conda：alchemlyb=2.5.0, pandas, numpy；Pip：—。
- 安装说明：—

#### `quantum_espresso` — Quantum ESPRESSO

- 说明：Quantum ESPRESSO pw.x periodic calculations rendered from typed structures/settings.
- Runtime：`qe`；状态：`available`；License：`open_source`。
- Actions（4）：`calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure`
- Conda：qe；Pip：—。
- 安装说明：—

#### `cp2k` — CP2K

- 说明：CP2K periodic calculations rendered from typed structures/settings.
- Runtime：`cp2k`；状态：`available`；License：`open_source`。
- Actions（4）：`calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure`
- Conda：cp2k；Pip：—。
- 安装说明：—

#### `siesta` — SIESTA

- 说明：SIESTA calculations rendered from typed structures/settings.
- Runtime：`periodic`；状态：`available`；License：`open_source`。
- Actions（3）：`calculate_periodic_energy`, `calculate_periodic_forces`, `relax_periodic_structure`
- Conda：siesta；Pip：—。
- 安装说明：—

#### `dftbplus` — DFTB+

- 说明：DFTB+ calculations rendered from typed structures/settings.
- Runtime：`periodic`；状态：`available`；License：`open_source`。
- Actions（3）：`calculate_periodic_energy`, `calculate_periodic_forces`, `relax_periodic_structure`
- Conda：dftbplus；Pip：—。
- 安装说明：—

#### `abinit` — ABINIT

- 说明：ABINIT calculations rendered from typed structures/settings.
- Runtime：`abinit`；状态：`available`；License：`open_source`。
- Actions（4）：`calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure`
- Conda：abinit；Pip：—。
- 安装说明：—

#### `vasp` — VASP

- 说明：Locally licensed VASP 6.3.2 periodic calculations with explicit POTCAR ResourceRefs, INCAR controls, k-point mesh, and convergence settings.
- Runtime：`vasp`；状态：`available`；License：`commercial_license`。
- Actions（4）：`calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure`
- Conda：—；Pip：—。
- 安装说明：VASP 6.3.2 was built locally from the operator-provided source. The operator-supplied local POTCAR archive is registered as five explicit variant collections; treat it as licensed, non-redistributable data.

#### `phonopy` — Phonopy

- 说明：Second-order lattice-dynamics operations on explicit displacement/force artifacts.
- Runtime：`phonons`；状态：`available`；License：`open_source`。
- Actions（6）：`generate_displaced_supercells`, `assemble_force_constants`, `calculate_phonon_dispersion`, `calculate_phonon_density_of_states`, `calculate_harmonic_thermodynamics`, `calculate_phonon_group_velocities`
- Conda：phonopy；Pip：—。
- 安装说明：—

#### `phono3py` — Phono3py

- 说明：Third-order-capable lattice-dynamics operations on explicit displacement/force artifacts.
- Runtime：`phonons`；状态：`available`；License：`open_source`。
- Actions（7）：`generate_displaced_supercells`, `assemble_force_constants`, `calculate_phonon_dispersion`, `calculate_phonon_density_of_states`, `calculate_harmonic_thermodynamics`, `calculate_phonon_group_velocities`, `calculate_lattice_thermal_conductivity`
- Conda：phono3py；Pip：—。
- 安装说明：—

#### `shengbte` — ShengBTE

- 说明：ShengBTE source revision b0d2090 solution of an explicitly supplied native phonon-BTE model, with structured RTA or iterative conductivity-tensor extraction.
- Runtime：`shengbte`；状态：`available`；License：`open_source`。
- Actions（1）：`calculate_lattice_thermal_conductivity`
- Conda：—；Pip：—。
- 安装说明：Locally compiled official ShengBTE source; the bundled Test-RTA calculation passed.

#### `vina` — AutoDock Vina

- 说明：AutoDock Vina docking using prepared structures and an explicit search box.
- Runtime：`docking`；状态：`available`；License：`open_source`。
- Actions（1）：`dock_ligand`
- Conda：vina；Pip：—。
- 安装说明：—

#### `gnina` — GNINA

- 说明：GNINA docking using prepared structures and an explicit search box/model.
- Runtime：`docking`；状态：`available`；License：`open_source`。
- Actions（1）：`dock_ligand`
- Conda：—；Pip：—。
- 安装说明：Configured from registered GNINA 1.3.3 CUDA 12.8 binary; rerun chemistry_toolbox/scripts/configure_toolbox_resources.py to verify/relink.

#### `pubchem` — PubChem PUG REST

- 说明：PubChem compound lookup through PubChemPy/PUG REST.
- Runtime：`services`；状态：`available`；License：`open_source`。
- Actions（6）：`search_compounds`, `resolve_chemical_identity`, `retrieve_compound_properties`, `retrieve_compound_structure`, `search_similar_compounds`, `search_substructures`
- Conda：—；Pip：pubchempy==1.0.5。
- 安装说明：Live PUG REST access uses cross-worker rate limiting and bounded retries. Optional mechanical controls are max_retries, retry_backoff_seconds, minimum_request_interval_seconds, timeout_seconds, max_poll_attempts, and poll_interval_seconds. Existing proxy variables take priority; otherwise PubChem loads proxy-only values from the ignored config.local.env file. No alternate data source is selected implicitly.

#### `rcsb_pdb` — RCSB PDB Data API

- 说明：RCSB PDB entry/search APIs.
- Runtime：`services`；状态：`available`；License：`open_source`。
- Actions（1）：`search_protein_structures`
- Conda：—；Pip：httpx>=0.28。
- 安装说明：—

#### `materials_project` — Materials Project

- 说明：Materials Project summary REST API requiring an MP_API_KEY for live access; bounded HTTP timeouts avoid unbounded client initialization.
- Runtime：`services`；状态：`unavailable`；License：`open_source`。
- Actions（1）：`search_materials`
- Conda：mp-api；Pip：—。
- 安装说明：—

#### `catalysis_hub` — Catalysis-Hub GraphQL

- 说明：Catalysis-Hub GraphQL reaction lookup.
- Runtime：`services`；状态：`available`；License：`open_source`。
- Actions（1）：`search_catalysis_records`
- Conda：—；Pip：httpx>=0.28。
- 安装说明：Live GraphQL calls use bounded retry/backoff controls (max_retries, retry_backoff_seconds) and return retryable remote-service errors without hidden fallback.

#### `nist_webbook` — NIST Chemistry WebBook SRD 69 CGI

- 说明：Bounded single-species lookup through the official parameterized WebBook CGI; this is not represented as a REST/JSON API and does not perform bulk crawling.
- Runtime：`services`；状态：`available`；License：`nist_srd_terms`。
- Actions（1）：`lookup_nist_webbook_species`
- Conda：—；Pip：httpx>=0.28。
- 安装说明：No local dataset is mirrored. Name/formula wildcards and responses over 2 MiB are rejected; formula isotope/ion choices remain explicit Agent settings.

## 5. 软件、程序库、工作流组件和数据接口 Inventory

该表不仅包含独立计算软件，也包含 Python 库、工作流系统、可视化程序和外部数据接口。`backend_registered=false` 不等于无用：它仍可能通过 native command 或 Agent-authored Python 程序使用。

| Software ID | 名称 | 可用 | Backend registered | Runtime | 版本 | Actions | Native commands | 本地文档 |
|---|---|---|---|---|---|---|---|---|
| `abinit` | ABINIT | yes | yes | `abinit` | 10.0.3 | `calculate_periodic_energy`<br>`calculate_periodic_forces`<br>`calculate_periodic_stress`<br>`relax_periodic_structure` | `abinit` (available) | yes |
| `aiida` | AiiDA | yes | no | `workflows` | — | — | `verdi` (available) | yes |
| `alchemlyb` | alchemlyb | yes | yes | `free_energy` | 2.5.0 | `parse_alchemical_energy_data` | — | yes |
| `allegro` | Allegro | yes | yes | `nequip` | — | `calculate_periodic_energy`<br>`calculate_periodic_forces`<br>`calculate_periodic_stress`<br>`relax_periodic_structure` | — | no |
| `amber_pmemd` | Amber 26 PMEMD | yes | yes | `amber` | — | `minimize_system_energy`<br>`propagate_dynamics` | `pmemd` (available)<br>`pmemd.MPI` (available)<br>`mpirun` (missing) | yes |
| `arkane` | Arkane | yes | no | `rmg` | 4.0.0 | — | `Arkane.py` (available) | yes |
| `ase_emt` | ASE EMT | yes | yes | `core` | — | `calculate_energy`<br>`calculate_forces`<br>`calculate_hessian`<br>`optimize_geometry` | — | no |
| `atomate2` | atomate2 | yes | no | `` | 0.1.5 | — | — | yes |
| `autode` | autodE | yes | no | `` | 1.4.5 | — | — | yes |
| `automekin` | AutoMeKin | yes | no | `automekin` | — | — | `amk.sh` (available)<br>`mopac` (available)<br>`bbfs.exe` (available) | yes |
| `cantera` | Cantera | yes | yes | `reaction` | — | `calculate_chemical_equilibrium`<br>`integrate_reaction_network` | — | no |
| `castep` | CASTEP | no | no | `` | — | — | — | yes |
| `catalysis_hub` | Catalysis-Hub GraphQL | yes | yes | `services` | — | `search_catalysis_records` | — | no |
| `catmap` | CatMAP | yes | yes | `reaction` | 0.3.1 | `solve_microkinetic_model` | — | yes |
| `cclib` | cclib | yes | yes | `workflows` | 1.8.1 | `parse_quantum_chemistry_output` | — | yes |
| `censo` | CENSO | yes | no | `reaction` | — | — | `censo` (available) | yes |
| `charmm` | CHARMM c50b2 | yes | yes | `charmm` | — | `minimize_system_energy`<br>`propagate_dynamics` | `charmm` (available) | yes |
| `chgnet` | CHGNet | yes | yes | `mlip` | — | `calculate_energy`<br>`calculate_forces`<br>`calculate_hessian`<br>`optimize_geometry` | — | no |
| `cp2k` | CP2K | yes | yes | `cp2k` | 2026.1 | `calculate_periodic_energy`<br>`calculate_periodic_forces`<br>`calculate_periodic_stress`<br>`relax_periodic_structure` | `cp2k` (available) | yes |
| `crest` | CREST | yes | yes | `reaction` | — | `generate_conformer_ensemble` | `crest` (available) | no |
| `critic2` | Critic2 | yes | yes | `critic2` | 1.2.1081 | `analyze_electron_density_topology`<br>`calculate_atomic_basin_properties`<br>`calculate_bader_charges` | `critic2` (available) | yes |
| `crystal` | CRYSTAL | no | no | `` | — | — | — | yes |
| `deepmd` | DeePMD-kit | yes | yes | `deepmd` | 3.2.0b0 | `calculate_energy`<br>`calculate_forces`<br>`calculate_hessian`<br>`calculate_periodic_energy`<br>`calculate_periodic_forces`<br>`calculate_periodic_stress`<br>`optimize_geometry`<br>`relax_periodic_structure` | `dp` (available) | yes |
| `dftbplus` | DFTB+ | yes | yes | `periodic` | — | `calculate_periodic_energy`<br>`calculate_periodic_forces`<br>`relax_periodic_structure` | `dftb+` (available) | no |
| `easyspin` | EasySpin | no | no | `easyspin` | 6.0.12 | — | `matlab` (missing) | yes |
| `gamess` | GAMESS | yes | yes | `gamess` | — | `calculate_dipole_moment`<br>`calculate_energy`<br>`optimize_geometry` | `rungms` (available) | no |
| `gaussian` | Gaussian 16 | yes | yes | `gaussian` | — | `calculate_dipole_moment`<br>`calculate_energy`<br>`calculate_hessian`<br>`optimize_geometry` | `g16` (available)<br>`formchk` (available) | yes |
| `geometric` | geomeTRIC | yes | yes | `nwchem` | 1.1.1 | `optimize_geometry` | `geometric-optimize` (available) | yes |
| `gnina` | GNINA | yes | yes | `docking` | — | `dock_ligand` | `gnina` (available) | no |
| `goodvibes` | GoodVibes | yes | yes | `goodvibes` | 4.3.0 | `analyze_reaction_free_energy_profile`<br>`analyze_thermochemical_ensemble`<br>`analyze_thermochemical_selectivity`<br>`derive_thermochemistry`<br>`scan_thermochemistry_temperature`<br>`validate_thermochemistry_inputs` | `goodvibes` (available) | no |
| `gpaw` | GPAW | yes | yes | `gpaw` | 25.7.0 | `calculate_density_of_states`<br>`calculate_electronic_band_structure`<br>`calculate_energy`<br>`calculate_forces`<br>`calculate_periodic_energy`<br>`calculate_periodic_forces`<br>`calculate_periodic_stress`<br>`calculate_projected_density_of_states`<br>`optimize_geometry`<br>`relax_periodic_structure` | `gpaw` (available) | yes |
| `gromacs` | GROMACS | yes | yes | `md` | — | `minimize_system_energy`<br>`propagate_dynamics` | `gmx` (available) | no |
| `hoomd` | HOOMD-blue | yes | yes | `free_energy` | — | `calculate_force_field_energy`<br>`calculate_force_field_forces`<br>`minimize_system_energy`<br>`propagate_dynamics` | — | no |
| `hoomd_blue` | HOOMD-blue | no | no | `` | 7.1.0 | `calculate_force_field_energy`<br>`calculate_force_field_forces`<br>`minimize_system_energy`<br>`propagate_dynamics` | — | yes |
| `internal_spectroscopy` | ResearchChem spectrum builder | yes | yes | `core` | — | `derive_ir_spectrum`<br>`derive_uv_vis_spectrum` | — | no |
| `internal_statistics` | ResearchChem deterministic statistics | yes | yes | `core` | — | `rank_conformers_from_results` | — | no |
| `internal_thermochemistry` | ResearchChem statistical thermochemistry | yes | yes | `core` | — | `derive_thermochemistry` | — | no |
| `internal_vibrations` | ResearchChem vibrational analysis | yes | yes | `core` | — | `derive_vibrational_modes` | — | no |
| `jobflow` | jobflow | yes | no | `` | 0.1.19 | — | — | yes |
| `kinbot` | KinBot | yes | no | `kinbot` | 2.2.2 | — | `kinbot` (available)<br>`pes` (available) | yes |
| `lammps` | LAMMPS | yes | yes | `md` | 2025.07.22-update4 | `minimize_system_energy`<br>`propagate_dynamics` | `lmp` (available) | yes |
| `lobster` | LOBSTER | yes | yes | `lobster` | 5.1.0 | `analyze_periodic_bonding`<br>`calculate_charge_spilling`<br>`calculate_projected_density_of_states` | `lobster-5.1.0` (available) | no |
| `mace` | MACE | yes | yes | `mlip` | — | `calculate_energy`<br>`calculate_forces`<br>`calculate_hessian`<br>`optimize_geometry` | — | no |
| `materials_project` | Materials Project | yes | yes | `services` | — | `search_materials` | — | no |
| `matlab` | MATLAB | no | no | `matlab` | — | — | `matlab` (missing) | no |
| `mdanalysis` | MDAnalysis | yes | yes | `md` | 2.9.0 | `calculate_dihedral_distribution`<br>`calculate_dynamic_cross_correlation`<br>`calculate_hydrogen_bonds`<br>`calculate_mean_squared_displacement`<br>`calculate_principal_components`<br>`calculate_radial_distribution`<br>`calculate_radius_of_gyration`<br>`calculate_trajectory_rmsd` | — | yes |
| `mdtraj` | MDTraj | yes | yes | `workflows` | 1.11.1 | `assign_secondary_structure`<br>`calculate_contacts`<br>`calculate_dihedral_distribution`<br>`calculate_radius_of_gyration`<br>`calculate_solvent_accessible_surface`<br>`calculate_trajectory_rmsd`<br>`cluster_trajectory` | — | yes |
| `mesmer` | MESMER | yes | yes | `mesmer` | 7.1 | `solve_master_equation` | `mesmer` (available) | yes |
| `mess` | MESS | yes | yes | `mess` | 2020.1.24 | `solve_master_equation` | `mess` (available) | no |
| `molpro` | Molpro | no | no | `` | — | — | — | yes |
| `multiwfn` | Multiwfn | yes | yes | `multiwfn` | 2026.7.15 | `calculate_atomic_charges`<br>`calculate_bond_orders` | `Multiwfn_noGUI` (available) | yes |
| `namd` | NAMD 3 | yes | yes | `namd` | 3.0.2 | `minimize_system_energy`<br>`propagate_dynamics` | `namd3` (available) | yes |
| `nequip` | NequIP | yes | yes | `nequip` | 0.19.0, 0.8.3 | `calculate_periodic_energy`<br>`calculate_periodic_forces`<br>`calculate_periodic_stress`<br>`relax_periodic_structure` | `nequip-train` (available) | yes |
| `newton_x` | Newton-X | yes | no | `newtonx` | 3.5.3 | — | `nx_geninp` (available)<br>`nx_moldyn` (available)<br>`nx_test` (available) | yes |
| `nist_cccbdb` | NIST CCCBDB 接口 | no | no | `` | — | — | — | yes |
| `nist_chemistry_webbook` | NIST Chemistry WebBook 接口 | no | no | `` | — | — | — | yes |
| `nist_webbook` | NIST Chemistry WebBook SRD 69 CGI | yes | yes | `services` | — | `lookup_nist_webbook_species` | — | no |
| `nwchem` | NWChem | yes | yes | `nwchem` | 7.3.1 | `calculate_atomic_charges`<br>`calculate_dipole_moment`<br>`calculate_energy`<br>`calculate_forces`<br>`calculate_hessian` | `nwchem` (available) | yes |
| `openbabel` | Open Babel | yes | yes | `quantum` | — | `generate_3d_structure` | `obabel` (available) | no |
| `openeye` | OpenEye | no | no | `` | — | — | — | yes |
| `openff` | OpenFF Toolkit/Interchange | yes | yes | `openff` | — | `assign_force_field_parameters` | — | no |
| `openff_am1bcc` | OpenFF AM1-BCC | yes | yes | `openff` | — | `assign_partial_charges` | `antechamber` (available)<br>`sqm` (available) | no |
| `openmm` | OpenMM | yes | yes | `md` | 8.5.2 | `calculate_force_field_energy`<br>`calculate_force_field_forces`<br>`decompose_force_field_energy`<br>`minimize_system_energy`<br>`propagate_dynamics` | — | yes |
| `openmm_builder` | OpenMM system builder | yes | yes | `md` | — | `assign_force_field_parameters`<br>`solvate_molecular_system` | — | no |
| `openmolcas` | OpenMolcas | yes | yes | `openmolcas` | 25.10 | `calculate_atomic_charges`<br>`calculate_dipole_moment`<br>`calculate_energy`<br>`calculate_orbitals` | `pymolcas` (available) | yes |
| `orca` | ORCA | yes | yes | `quantum` | 6.1.1 | `calculate_atomic_charges`<br>`calculate_bond_orders`<br>`calculate_dipole_moment`<br>`calculate_energy`<br>`calculate_excited_states`<br>`calculate_forces`<br>`calculate_hessian`<br>`calculate_orbitals`<br>`optimize_geometry` | `orca` (available) | yes |
| `packmol` | Packmol | yes | yes | `md` | — | `solvate_molecular_system` | `packmol` (available) | no |
| `pdb_tools` | pdb-tools | yes | yes | `core` | 2.7.0 | `normalize_pdb_records`<br>`renumber_biomolecular_structure`<br>`select_structure_subset` | `pdb_selchain` (available)<br>`pdb_reres` (available)<br>`pdb_tidy` (available) | yes |
| `pdbfixer` | PDBFixer | yes | yes | `md` | — | `assign_protonation_states`<br>`repair_biomolecular_structure` | — | no |
| `phono3py` | Phono3py | yes | yes | `phonons` | 4.3.3 | `assemble_force_constants`<br>`calculate_harmonic_thermodynamics`<br>`calculate_lattice_thermal_conductivity`<br>`calculate_phonon_density_of_states`<br>`calculate_phonon_dispersion`<br>`calculate_phonon_group_velocities`<br>`generate_displaced_supercells` | `phono3py` (available) | yes |
| `phonopy` | Phonopy | yes | yes | `phonons` | — | `assemble_force_constants`<br>`calculate_harmonic_thermodynamics`<br>`calculate_phonon_density_of_states`<br>`calculate_phonon_dispersion`<br>`calculate_phonon_group_velocities`<br>`generate_displaced_supercells` | `phonopy` (available) | no |
| `plumed` | PLUMED | yes | yes | `md` | 2.9.2 | `evaluate_collective_variables` | `plumed` (available) | yes |
| `psi4` | Psi4 | yes | yes | `psi4` | — | `calculate_atomic_charges`<br>`calculate_dipole_moment`<br>`calculate_energy`<br>`calculate_hessian`<br>`calculate_orbitals` | `psi4` (available) | no |
| `pubchem` | PubChem PUG REST | yes | yes | `services` | pubchempy-1.0.5 | `resolve_chemical_identity`<br>`retrieve_compound_properties`<br>`retrieve_compound_structure`<br>`search_compounds`<br>`search_similar_compounds`<br>`search_substructures` | — | yes |
| `pymatgen` | pymatgen | yes | yes | `workflows` | 2026.5.4 | `analyze_crystal_symmetry`<br>`build_supercell`<br>`enumerate_surface_slabs`<br>`standardize_crystal_structure` | — | yes |
| `pymbar` | PyMBAR | yes | yes | `free_energy` | 4.2.0 | `analyze_free_energy_convergence`<br>`calculate_potential_of_mean_force`<br>`estimate_free_energy_difference`<br>`estimate_thermodynamic_expectations` | — | yes |
| `pyscf` | PySCF | yes | yes | `quantum` | 2.13.1 | `calculate_atomic_charges`<br>`calculate_dipole_moment`<br>`calculate_energy`<br>`calculate_excited_states`<br>`calculate_forces`<br>`calculate_hessian`<br>`calculate_orbitals` | — | yes |
| `pysisyphus` | pysisyphus | yes | yes | `reaction` | — | `locate_transition_state`<br>`trace_intrinsic_reaction_coordinate` | `pysis` (available) | no |
| `q_chem` | Q-Chem | no | no | `` | — | — | — | yes |
| `qcelemental` | QCElemental | yes | yes | `workflows` | 0.50.4 | `normalize_qcschema_molecule`<br>`validate_qcschema_record` | — | yes |
| `qcengine` | QCEngine | yes | no | `workflows` | 0.50.0 | — | `qcengine` (available) | yes |
| `qcschema` | QCSchema | no | no | `` | — | — | — | yes |
| `quantum_espresso` | Quantum ESPRESSO | yes | yes | `qe` | 7.5 | `calculate_periodic_energy`<br>`calculate_periodic_forces`<br>`calculate_periodic_stress`<br>`relax_periodic_structure` | `pw.x` (available) | yes |
| `rcsb_pdb` | RCSB PDB Data API | yes | yes | `services` | — | `search_protein_structures` | — | no |
| `rdkit` | RDKit | yes | yes | `core` | 2023.09.6 | `align_molecular_structures`<br>`assign_partial_charges`<br>`assign_protonation_states`<br>`calculate_molecular_descriptors`<br>`calculate_molecular_fingerprint`<br>`calculate_molecular_similarity`<br>`cluster_conformers`<br>`enumerate_stereoisomers`<br>`enumerate_tautomers`<br>`generate_3d_structure`<br>`generate_conformer_ensemble`<br>`search_local_substructures`<br>`standardize_structure` | — | yes |
| `rdkit_etkdg` | RDKit ETKDG | yes | yes | `core` | — | `generate_conformer_ensemble` | — | no |
| `rdkit_gasteiger` | RDKit Gasteiger charges | yes | yes | `core` | — | `assign_partial_charges` | — | no |
| `rmg` | RMG-Py | yes | yes | `rmg` | 4.0.0 | `calculate_rate_constants`<br>`calculate_tunneling_correction` | `rmg.py` (available) | yes |
| `schr_dinger` | Schrödinger | no | no | `` | 1.0.11-7, 1.0.11-7-x86_64.pkg.tar.zst | — | — | yes |
| `scipy` | SciPy | yes | yes | `reaction` | — | `integrate_reaction_network` | — | no |
| `sella` | Sella | yes | yes | `sella` | 2.5.0 | `locate_transition_state`<br>`optimize_geometry` | — | yes |
| `sharc` | SHARC | yes | no | `sharc` | 4.1 | — | `sharc.x` (available)<br>`wfoverlap.x` (available) | yes |
| `shengbte` | ShengBTE | yes | yes | `shengbte` | source-b0d2090 | `calculate_lattice_thermal_conductivity` | `ShengBTE` (available) | yes |
| `siesta` | SIESTA | yes | yes | `periodic` | — | `calculate_periodic_energy`<br>`calculate_periodic_forces`<br>`relax_periodic_structure` | `siesta` (available) | no |
| `spglib` | spglib | yes | yes | `workflows` | 2.7.0 | `analyze_crystal_symmetry`<br>`standardize_crystal_structure` | — | yes |
| `tblite` | TBLite | yes | yes | `quantum` | — | `calculate_dipole_moment`<br>`calculate_energy`<br>`calculate_forces`<br>`calculate_hessian`<br>`optimize_geometry` | — | no |
| `theodore` | TheoDORE | yes | no | `theodore` | 2.5.0 | — | `theodore` (available) | yes |
| `turbomole` | TURBOMOLE | no | no | `` | — | — | — | yes |
| `vasp` | VASP | yes | yes | `vasp` | 6.3.2 | `calculate_periodic_energy`<br>`calculate_periodic_forces`<br>`calculate_periodic_stress`<br>`relax_periodic_structure` | `vasp_std` (available) | yes |
| `vesta` | VESTA | yes | no | `vesta` | 3.90.5a | — | `VESTA` (available) | yes |
| `vina` | AutoDock Vina | yes | yes | `docking` | — | `dock_ligand` | `vina` (available) | no |
| `vmd` | VMD | yes | no | `vmd` | 1.9.3 | — | `vmd` (available) | yes |
| `wannier90` | Wannier90 | yes | no | `qe` | — | — | `wannier90.x` (available) | yes |
| `wien2k` | WIEN2k | no | no | `` | — | — | — | no |
| `xtb` | xTB | yes | yes | `quantum` | 6.7.1 | `calculate_atomic_charges`<br>`calculate_bond_orders`<br>`calculate_dipole_moment`<br>`calculate_energy`<br>`calculate_forces`<br>`calculate_hessian`<br>`optimize_geometry` | `xtb` (available) | yes |
| `yambo` | Yambo | yes | no | `yambo` | 5.3.0 | — | `p2y` (available)<br>`yambo` (available) | yes |

## 6. Reviewed 软件原生命令指南

以下软件可由 Agent 在查看 `inspect_software` 后编写原生输入并显式执行。表中只是命令入口，不代表固定科学流程。

| Software | 用途 | 命令 | Synopsis | 输入模式 |
|---|---|---|---|---|
| `openbabel` | Convert, filter, and manipulate molecular file formats with Open Babel. | `obabel` | `obabel -i<input_format> input -o<output_format> -O output [options]` | `arguments` |
| `crest` | Perform CREST conformer searches and related xTB-driven sampling from an Agent-authored structure and options. | `crest` | `crest input.xyz --gfn2 --T <threads> [sampling options]` | `arguments` |
| `pdb_tools` | Apply individual pdb-tools text transformations to PDB records. | `pdb_selchain` | `pdb_selchain -<chain_ids> input.pdb` | `arguments` |
| `pdb_tools` | Apply individual pdb-tools text transformations to PDB records. | `pdb_reres` | `pdb_reres -<first_residue_number> input.pdb` | `arguments` |
| `pdb_tools` | Apply individual pdb-tools text transformations to PDB records. | `pdb_tidy` | `pdb_tidy input.pdb` | `arguments` |
| `openff_am1bcc` | Run AmberTools charge-generation components used by explicit OpenFF/AM1-BCC preparation. | `antechamber` | `antechamber -i input -fi <format> -o output -fo <format> -c bcc -nc <charge> [options]` | `arguments` |
| `openff_am1bcc` | Run AmberTools charge-generation components used by explicit OpenFF/AM1-BCC preparation. | `sqm` | `sqm -O -i sqm.in -o sqm.out` | `arguments` |
| `packmol` | Pack molecules into an Agent-defined simulation cell from a native Packmol input deck. | `packmol` | `packmol < packmol.inp` | `stdin_file` |
| `xtb` | Execute native xTB single points, properties, optimization, frequencies, dynamics, and related modes selected by the Agent. | `xtb` | `xtb structure.xyz --gfn <level> [--sp\|--opt\|--hess\|--md] [explicit options]` | `arguments` |
| `gpaw` | Run an Agent-authored GPAW Python program using the GPAW command wrapper. | `gpaw` | `gpaw python program.py [program arguments]` | `arguments` |
| `lobster` | Analyze bonding from compatible electronic-structure outputs using a native LOBSTER input. | `lobster-5.1.0` | `lobster-5.1.0` | `fixed_files` |
| `nwchem` | Execute an Agent-authored NWChem input deck for molecular or periodic calculations supported by the installed build. | `nwchem` | `nwchem input.nw` | `arguments` |
| `openmolcas` | Execute an Agent-authored OpenMolcas input deck for multireference and spectroscopy calculations. | `pymolcas` | `pymolcas input.inp [driver options]` | `arguments` |
| `multiwfn` | Run Multiwfn analyses using an explicit wavefunction file and menu-command stream. | `Multiwfn_noGUI` | `Multiwfn_noGUI wavefunction_file < commands.txt` | `arguments_and_stdin_file` |
| `critic2` | Run Critic2 topology and field analysis from an Agent-authored native input. | `critic2` | `critic2 input.cri` | `arguments` |
| `psi4` | Execute a complete Agent-authored Psi4 input file. | `psi4` | `psi4 input.dat output.dat [options]` | `arguments` |
| `deepmd` | Invoke a specific DeePMD-kit command selected by the Agent. | `dp` | `dp <train\|freeze\|test\|compress\|show\|convert-backend> [subcommand options]` | `arguments` |
| `nequip` | Train a NequIP model from a complete Agent-authored configuration. | `nequip-train` | `nequip-train config.yaml` | `arguments` |
| `orca` | Execute a complete ORCA 6.1 input deck. | `orca` | `orca input.inp` | `arguments` |
| `gaussian` | Execute Gaussian 16 input and convert checkpoint files with formchk. | `g16` | `g16 < input.com` | `stdin_file` |
| `gaussian` | Execute Gaussian 16 input and convert checkpoint files with formchk. | `formchk` | `formchk input.chk output.fchk` | `arguments` |
| `gamess` | Execute a GAMESS input through the installed rungms launcher. | `rungms` | `rungms job_name [version] [ncores]` | `arguments` |
| `goodvibes` | Apply GoodVibes 4.3.0 thermochemistry, ensemble, selectivity, consistency, and reaction-profile analysis to explicit completed quantum-chemistry outputs. | `goodvibes` | `goodvibes OUTPUT... --temp K [state/scaling/qh options] [analysis option] --json result.json` | `arguments` |
| `pysisyphus` | Execute a complete pysisyphus workflow configuration authored by the Agent. | `pysis` | `pysis config.yaml` | `arguments` |
| `rmg` | Generate reaction mechanisms from a complete Agent-authored RMG-Py input file. | `rmg.py` | `rmg.py input.py` | `arguments` |
| `mess` | Solve an Agent-authored MESS master-equation model. | `mess` | `mess input.inp` | `arguments` |
| `mesmer` | Solve an Agent-authored MESMER master-equation XML model. | `mesmer` | `mesmer input.xml -o output.xml [options]` | `arguments` |
| `gromacs` | Invoke one explicit GROMACS subcommand against staged topology, coordinate, trajectory, or run-input files. | `gmx` | `gmx <subcommand> [subcommand options]` | `arguments` |
| `lammps` | Execute a complete LAMMPS input script. | `lmp` | `lmp -in input.lammps [command-line variables]` | `arguments` |
| `namd` | Execute a complete NAMD configuration. | `namd3` | `namd3 +p<threads> input.conf` | `arguments` |
| `amber_pmemd` | Execute Amber PMEMD serial or MPI molecular dynamics from explicit control/topology/state files. | `pmemd` | `pmemd -O -i mdin -o mdout -p topology.prmtop -c input.rst7 -r output.rst7 -x trajectory.nc` | `arguments` |
| `amber_pmemd` | Execute Amber PMEMD serial or MPI molecular dynamics from explicit control/topology/state files. | `pmemd.MPI` | `pmemd.MPI -O -i mdin -o mdout -p topology.prmtop -c input.rst7 -r output.rst7 -x trajectory.nc` | `arguments` |
| `amber_pmemd` | Execute Amber PMEMD serial or MPI molecular dynamics from explicit control/topology/state files. | `mpirun` | `mpirun <program> [arguments]` | `arguments` |
| `charmm` | Execute a complete CHARMM input script. | `charmm` | `charmm -i input.inp -o output.out` | `arguments` |
| `plumed` | Run an explicit PLUMED subcommand for enhanced sampling support or trajectory analysis. | `plumed` | `plumed <subcommand> [options]` | `arguments` |
| `quantum_espresso` | Execute an Agent-authored Quantum ESPRESSO pw.x input deck. | `pw.x` | `pw.x -in input.in` | `arguments` |
| `cp2k` | Execute a complete CP2K input deck for molecular, periodic, dynamics, spectroscopy, or other supported calculations. | `cp2k` | `cp2k -i input.inp -o output.out` | `arguments` |
| `siesta` | Execute a complete SIESTA input deck. | `siesta` | `siesta < input.fdf` | `stdin_file` |
| `dftbplus` | Execute a complete DFTB+ calculation from native fixed-name input. | `dftb+` | `dftb+` | `fixed_files` |
| `abinit` | Execute a complete ABINIT input deck. | `abinit` | `abinit input.abi` | `arguments` |
| `vasp` | Execute a VASP calculation from the standard Agent-prepared input set. | `vasp_std` | `vasp_std` | `fixed_files` |
| `phonopy` | Invoke an explicit Phonopy command for displacement generation, force-constant construction, or phonon analysis. | `phonopy` | `phonopy [mode/options] [configuration files]` | `arguments` |
| `phono3py` | Invoke an explicit Phono3py command for third-order force constants and lattice thermal transport. | `phono3py` | `phono3py [mode/options] [configuration files]` | `arguments` |
| `shengbte` | Solve lattice thermal transport from an Agent-authored ShengBTE CONTROL and force constants. | `ShengBTE` | `ShengBTE` | `fixed_files` |
| `vina` | Run AutoDock Vina docking or scoring with explicitly selected receptor, ligand, box, and search settings. | `vina` | `vina --receptor receptor.pdbqt --ligand ligand.pdbqt --center_x X --center_y Y --center_z Z --size_x X --size_y Y --size_z Z --out poses.pdbqt [options]` | `arguments` |
| `gnina` | Run GNINA docking/rescoring with explicitly selected receptor, ligand, box, CNN model, and search settings. | `gnina` | `gnina -r receptor.pdbqt -l ligand.sdf --center_x X --center_y Y --center_z Z --size_x X --size_y Y --size_z Z -o poses.sdf [options]` | `arguments` |
| `qcengine` | Invoke the QCEngine command-line interface on an Agent-authored QCSchema input and explicitly selected program. | `qcengine` | `qcengine run <program> input.json [CLI options]` | `arguments` |
| `aiida` | Inspect and operate the configured AiiDA profile with explicit verdi subcommands. | `verdi` | `verdi <status\|profile\|code\|computer\|process\|...> [subcommand options]` | `arguments` |
| `censo` | Run CENSO ensemble refinement from an Agent-selected conformer ensemble and explicit settings. | `censo` | `censo -i conformers.xyz [explicit CENSO options]` | `arguments` |
| `geometric` | Run the geomeTRIC command-line optimizer against an explicitly selected engine and Agent-authored input. | `geometric-optimize` | `geometric-optimize [optimizer options] input.xyz --engine <engine>` | `arguments` |
| `wannier90` | Preprocess and execute Wannier90 from an Agent-authored seedname.win and upstream interface files. | `wannier90.x` | `wannier90.x [-pp] seedname` | `arguments` |
| `arkane` | Run Arkane thermochemistry, kinetics, pressure-dependence, or statmech jobs from a complete input file. | `Arkane.py` | `Arkane.py input.py [CLI options]` | `arguments` |
| `automekin` | Invoke individual AutoMeKin and bundled MOPAC entry points from explicit native inputs. | `amk.sh` | `amk.sh <Agent-prepared AutoMeKin input> [explicit options]` | `arguments` |
| `automekin` | Invoke individual AutoMeKin and bundled MOPAC entry points from explicit native inputs. | `mopac` | `mopac input.mop` | `arguments` |
| `automekin` | Invoke individual AutoMeKin and bundled MOPAC entry points from explicit native inputs. | `bbfs.exe` | `bbfs.exe [AutoMeKin component arguments]` | `arguments` |
| `kinbot` | Run KinBot species/reaction or PES searches from an Agent-authored JSON input. | `kinbot` | `kinbot input.json` | `arguments` |
| `kinbot` | Run KinBot species/reaction or PES searches from an Agent-authored JSON input. | `pes` | `pes input.json` | `arguments` |
| `sharc` | Execute SHARC surface-hopping dynamics or wavefunction-overlap analysis from complete native inputs. | `sharc.x` | `sharc.x input` | `arguments` |
| `sharc` | Execute SHARC surface-hopping dynamics or wavefunction-overlap analysis from complete native inputs. | `wfoverlap.x` | `wfoverlap.x < overlap.inp` | `stdin_file` |
| `newton_x` | Generate and run Newton-X nonadiabatic dynamics from Agent-authored control files. | `nx_geninp` | `nx_geninp [explicit generator options]` | `arguments_or_stdin` |
| `newton_x` | Generate and run Newton-X nonadiabatic dynamics from Agent-authored control files. | `nx_moldyn` | `nx_moldyn` | `fixed_files` |
| `newton_x` | Generate and run Newton-X nonadiabatic dynamics from Agent-authored control files. | `nx_test` | `nx_test <test_id> [options]` | `arguments` |
| `theodore` | Run TheoDORE excited-state and transition-density analyses from explicit subcommands and quantum-chemistry files. | `theodore` | `theodore <subcommand> [subcommand options]` | `arguments` |
| `matlab` | Execute an Agent-authored MATLAB R2018a script when a legitimate local MATLAB installation and license are available. | `matlab` | `matlab -nodisplay -nosplash -nodesktop -r "run('analysis.m'); exit"` | `arguments` |
| `easyspin` | Execute an Agent-authored MATLAB script using the staged EasySpin 6.0.12 toolbox when MATLAB is licensed and available. | `matlab` | `matlab -nodisplay -nosplash -nodesktop -r "addpath('<EasySpin path>'); run('analysis.m'); exit"` | `arguments` |
| `yambo` | Convert compatible upstream databases and run Agent-authored Yambo MBPT/GW/BSE calculations. | `p2y` | `p2y [conversion options]` | `arguments` |
| `yambo` | Convert compatible upstream databases and run Agent-authored Yambo MBPT/GW/BSE calculations. | `yambo` | `yambo -F input.in -J job_name [explicit options]` | `arguments` |
| `vmd` | Run an Agent-authored VMD/Tcl trajectory, structure, selection, measurement, or rendering script in text mode. | `vmd` | `vmd -dispdev text -e analysis.tcl [structure/trajectory options]` | `arguments` |
| `vesta` | Open or convert crystal/volumetric structure data with the installed VESTA GUI runtime. | `VESTA` | `VESTA structure_file` | `arguments` |

## 7. 可编程分析 Runtimes

| Runtime | 可用 | Python | Modules | Commands | 关联 Backends |
|---|---|---|---|---|---|
| `abinit` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/abinit/bin/python` | numpy, pydantic, yaml | abinit | abinit |
| `amber` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/amber/bin/python` | — | mpirun, pmemd, pmemd.MPI | amber_pmemd |
| `automekin` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/automekin/bin/python` | ase, networkx, numpy, scipy | amk.sh, bbfs.exe, mopac | — |
| `charmm` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/charmm/bin/python` | — | charmm | charmm |
| `core` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.toolbox_env/bin/python` | pdbtools | — | rdkit, rdkit_etkdg, rdkit_gasteiger, internal_statistics, ase_emt, internal_vibrations, internal_spectroscopy, internal_thermochemistry, pdb_tools |
| `cp2k` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/cp2k/bin/python` | — | cp2k | cp2k |
| `critic2` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/deepmd/bin/python` | — | critic2 | critic2 |
| `deepmd` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/deepmd_models/bin/python` | deepmd | dp | deepmd |
| `docking` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/docking/bin/python` | vina | gnina, vina | vina, gnina |
| `easyspin` | no | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/easyspin/6.0.12/bin/python` | — | matlab | — |
| `free_energy` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/free_energy/bin/python` | alchemlyb, hoomd, pymbar | — | pymbar, alchemlyb, hoomd |
| `gamess` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/gamess/bin/python` | — | rungms | gamess |
| `gaussian` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/gaussian/bin/python` | cclib | formchk, g16 | gaussian |
| `goodvibes` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/goodvibes/bin/python` | goodvibes, numpy, pandas, pyarrow, yaml | goodvibes | goodvibes |
| `gpaw` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/gpaw/bin/python` | gpaw | gpaw | gpaw |
| `kinbot` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/kinbot/bin/python` | jax, kinbot, openbabel, sella | kinbot, pes | — |
| `lobster` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/lobster/bin/python` | pymatgen | lobster-5.1.0 | lobster |
| `matlab` | no | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/matlab/R2018a/install/bin/python` | — | matlab | — |
| `md` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/md/bin/python` | MDAnalysis, lammps, openmm, pdbfixer | gmx, lmp, packmol, plumed | pdbfixer, openmm_builder, packmol, openmm, gromacs, lammps, mdanalysis, plumed |
| `mesmer` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/mesmer/bin/python` | pydantic, yaml | mesmer | mesmer |
| `mess` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/mess/bin/python` | pydantic, yaml | mess | mess |
| `mlip` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/mlip/bin/python` | ase, chgnet, mace, mace.calculators, torch | — | mace, chgnet |
| `multiwfn` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/multiwfn/bin/python` | pydantic, yaml | Multiwfn_noGUI | multiwfn |
| `namd` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/namd/bin/python` | — | namd3 | namd |
| `nequip` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/nequip/bin/python` | e3nn, nequip, torch | nequip-train | nequip, allegro |
| `newtonx` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/newtonx/bin/python` | — | nx_geninp, nx_moldyn, nx_test | — |
| `nwchem` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/nwchem/bin/python` | autode, cclib, geometric, qcelemental, qcengine | nwchem | nwchem, geometric |
| `openff` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/openff/bin/python` | openff.interchange, openff.toolkit | antechamber, sqm | openff_am1bcc, openff |
| `openmolcas` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/deepmd/bin/python` | pydantic, yaml | pymolcas | openmolcas |
| `periodic` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/periodic/bin/python` | — | dftb+, siesta | dftbplus, siesta |
| `phonons` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/phonons/bin/python` | phono3py, phonopy | phono3py-init, phonopy-init | phonopy, phono3py |
| `psi4` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/psi4/bin/python` | psi4 | psi4 | psi4 |
| `qe` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/qe/bin/python` | — | pw.x | quantum_espresso |
| `quantum` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/quantum/bin/python` | ase, mace, mace.calculators, pyscf, tblite, torch | mpirun, orca, xtb | openbabel, xtb, pyscf, tblite, orca |
| `reaction` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/reaction/bin/python` | cantera, catmap, pysisyphus, pyscf, scipy | crest, mpirun, orca, pysis, xtb | crest, pysisyphus, cantera, scipy, catmap |
| `rmg` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/rmg/bin/python` | arkane, rmgpy | rmg.py | rmg |
| `sella` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/sella/bin/python` | sella | — | sella |
| `services` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/services/bin/python` | httpx | — | pubchem, rcsb_pdb, materials_project, catalysis_hub, nist_webbook |
| `sharc` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/deepmd/bin/python` | — | sharc.x, wfoverlap.x | — |
| `shengbte` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/deepmd/bin/python` | pydantic, yaml | ShengBTE | shengbte |
| `theodore` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/theodore/bin/python` | cclib, theodore | theodore | — |
| `vasp` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/vasp/bin/python` | ase | mpirun, vasp_std | vasp |
| `vesta` | no | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/vesta/bin/python` | — | VESTA | — |
| `vmd` | no | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/vmd/bin/python` | — | vmd | — |
| `workflows` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/workflows/bin/python` | aiida, atomate2, cclib, jobflow, mdtraj, pymatgen, qcelemental, qcengine, spglib | — | qcelemental, cclib, pymatgen, spglib, mdtraj |
| `yambo` | yes | `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/yambo/bin/python` | — | p2y, yambo | — |

## 8. 注册科学资源

| Resource | Kind | 版本 | 格式 | 可用 | 兼容 Backend | 选择语法 |
|---|---|---|---|---|---|---|
| `qe_sssp_1_3_pbe_efficiency` | `element_file_collection` | 1.3.0 | UPF | yes | quantum_espresso | `resource://qe_sssp_1_3_pbe_efficiency/<Element>` |
| `qe_sssp_1_3_pbe_precision` | `element_file_collection` | 1.3.0 | UPF | yes | quantum_espresso | `resource://qe_sssp_1_3_pbe_precision/<Element>` |
| `siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml` | `element_file_collection` | nc-sr-05 standard | PSML 1.1 | yes | siesta | `resource://siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml/<Element>` |
| `abinit_pseudo_dojo_nc_sr_pbe_standard_psp8` | `element_file_collection` | standard | PSP8 | yes | abinit | `resource://abinit_pseudo_dojo_nc_sr_pbe_standard_psp8/<Element>` |
| `dftb_3ob_3_1` | `slater_koster_parameter_set` | 3.1.0 | Slater-Koster SKF | yes | dftbplus | `resource://dftb_3ob_3_1` |
| `dftb_matsci_0_3` | `slater_koster_parameter_set` | 0.3.0 | Slater-Koster SKF | yes | dftbplus | `resource://dftb_matsci_0_3` |
| `gnina_1_3_3_cuda12_8_linux_x86_64` | `backend_executable` | 1.3.3 | Linux x86_64 executable | yes | gnina | `` |
| `orca_6_1_1_linux_x86_64_shared_openmpi418_avx2` | `backend_executable` | 6.1.1 | Linux x86-64 AVX2 executable bundle | yes | orca | `` |
| `openmpi_4_1_8_orca_runtime` | `backend_executable` | 4.1.8 | Linux x86-64 shared MPI runtime | yes | orca | `` |
| `nequip_oam_s_0_1` | `model_checkpoint` | 0.1 | NequIP compiled model archive | yes | nequip | `resource://nequip_oam_s_0_1` |
| `nequip_oam_m_0_1` | `model_checkpoint` | 0.1 | NequIP compiled model archive | yes | nequip | `resource://nequip_oam_m_0_1` |
| `nequip_oam_l_0_1` | `model_checkpoint` | 0.1 | NequIP compiled model archive | yes | nequip | `resource://nequip_oam_l_0_1` |
| `nequip_oam_xl_0_1` | `model_checkpoint` | 0.1 | NequIP compiled model archive | yes | nequip | `resource://nequip_oam_xl_0_1` |
| `nequip_mp_l_0_1` | `model_checkpoint` | 0.1 | NequIP compiled model archive | yes | nequip | `resource://nequip_mp_l_0_1` |
| `allegro_oam_l_0_1` | `model_checkpoint` | 0.1 | NequIP compiled Allegro model archive | yes | allegro | `resource://allegro_oam_l_0_1` |
| `allegro_mp_l_0_1` | `model_checkpoint` | 0.1 | NequIP compiled Allegro model archive | yes | allegro | `resource://allegro_mp_l_0_1` |
| `deepmd_dpa_3_1_3m` | `model_checkpoint` | DPA-3.1-3M | DeePMD PyTorch frozen multitask model | yes | deepmd | `resource://deepmd_dpa_3_1_3m` |
| `deepmd_dpa_3_2_5m` | `model_checkpoint` | DPA-3.2-5M | DeePMD PyTorch frozen multitask model | yes | deepmd | `resource://deepmd_dpa_3_2_5m` |
| `deepmd_dpa_3_3_1m` | `model_checkpoint` | DPA-3.3-1M | DeePMD PyTorch frozen multitask model | yes | deepmd | `resource://deepmd_dpa_3_3_1m` |
| `deepmd_dpa_2_4_7m` | `model_checkpoint` | DPA-2.4-7M | DeePMD PyTorch frozen multitask model | yes | deepmd | `resource://deepmd_dpa_2_4_7m` |
| `deepmd_dpa3_omol_large` | `model_checkpoint` | DPA3-Omol-Large | DeePMD PyTorch frozen single-task model | yes | deepmd | `resource://deepmd_dpa3_omol_large` |
| `vasp_uspp_lda_legacy` | `variant_file_collection` | potpaw54 archive label; exact upstream revision unverified | VASP POTCAR / ultrasoft pseudopotential | yes | vasp | `resource://vasp_uspp_lda_legacy/<Variant>` |
| `vasp_uspp_gga_legacy` | `variant_file_collection` | potpaw54 archive label; exact upstream revision unverified | VASP POTCAR / ultrasoft pseudopotential | yes | vasp | `resource://vasp_uspp_gga_legacy/<Variant>` |
| `vasp_paw_lda_54` | `variant_file_collection` | potpaw54 archive label; exact upstream revision unverified | VASP POTCAR / PAW | yes | vasp | `resource://vasp_paw_lda_54/<Variant>` |
| `vasp_paw_pw91_54` | `variant_file_collection` | potpaw54 archive label; exact upstream revision unverified | VASP POTCAR / PAW | yes | vasp | `resource://vasp_paw_pw91_54/<Variant>` |
| `vasp_paw_pbe_54` | `variant_file_collection` | potpaw54 archive label; exact upstream revision unverified | VASP POTCAR / PAW | yes | vasp | `resource://vasp_paw_pbe_54/<Variant>` |
| `vasp_6_3_2_testsuite_si_potcar` | `single_file_resource` | VASP 6.3.2 testsuite | VASP POTCAR | yes | vasp | `resource://vasp_6_3_2_testsuite_si_potcar` |

## 9. 用该目录筛选论文的建议

### 9.1 优先选择

1. 提供原始输入/输出、结构、轨迹或补充数据，可在隔离环境中重算或重新解析。
2. 包含 3–15 个相互依赖的科学步骤，既能调用已有 Action，也需要 Agent 在原生软件或 Python 层补充分析。
3. 关键软件位于第 5/6 节且当前 available，或者论文数据足以只做后处理和验证。
4. 参考答案能拆成过程 rubric：输入审计、方法选择、计算、验证、结论和不确定性。
5. 有竞争假设、路径或模型，避免只靠一次查询即可回答。

### 9.2 谨慎选择

1. 依赖未提供 license、专有势函数或不可获得训练数据的论文。
2. 单次计算需要超出 benchmark 节点预算的大规模周期 DFT、长时间 MD 或高阶多参考计算。
3. 关键结论只存在于图片、人工判断或未公开脚本中，无法形成可核查 reference。
4. 所有步骤都被一个专用脚本完全封装，无法评价 Agent 的编排决策。

### 9.3 推荐的论文任务形状

- 构象生成 → 多级量化优化/频率 → GoodVibes 热化学 → 反应自由能/选择性；
- 反应物/TS/产物记录解析 → IRC/键变化验证 → 速率常数与实验趋势整合；
- 晶体结构标准化 → 周期弛豫 → 能带/DOS/声子 → 稳定性或输运结论；
- 系统构建 → MD/增强采样 → 轨迹/自由能分析 → 机理结论；
- 蛋白/配体准备 → docking → pose/score 分析 → 与实验活性比较；
- 公共数据库检索 → 结构/性质标准化 → 计算验证 → 数据驱动结论。

## 10. 相关现有详细文档

- [工具/Backend/资源矩阵](../../chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md)
- [软件能力矩阵](../../chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_SOFTWARE_CAPABILITY_MATRIX.md)
- [当前健康状态](../../chemistry_toolbox/docs/TOOLBOX_STATUS.md)
- [渐进式发现与 token 报告](../../chemistry_toolbox/docs/PROGRESSIVE_TOOL_DISCOVERY_REFACTOR_REPORT_20260722.md)
