# ResearchChemBench 化学工具箱能力目录

> 基于当前代码与本机运行时的实测目录快照，更新日期：2026-07-28。软件可用性会随许可证、环境变量、网络和服务器安装状态变化；实际运行前应再次调用目录探测工具。

## 1. 工具箱概览

| 项目 | 当前数量 | 说明 |
|---|---:|---|
| 预设科学 Action | 114 | 任务无关、带类型校验的标准科学行为 |
| 注册后端 | 77 | 其中 76 个当前可用于 Action，1 个因运行条件不满足而不可用 |
| 完整软件清单 | 107 | 93 个当前可用；包含 Action 后端、原生直调程序和已登记但未安装的软件 |
| 可编程分析运行时 | 42 | 隔离的 Python/软件环境，可运行智能体编写的分析程序 |
| 注册科学资源 | 27 | 赝势、参数集、模型权重和程序运行包；当前均已落盘 |

工具箱提供三层互补能力：

1. **预设科学 Action**：优先用于已覆盖的标准科研行为。Action 负责输入契约、参数校验、后端调用、结果类型和溯源记录，但不替智能体选择科学方法。
2. **原生软件直调**：当 Action 未覆盖某项功能时，智能体可查阅本地软件指南，编写原生输入文件并提交允许列表内的命令。
3. **可编程科学分析**：智能体可编写 Python 程序，选择已安装运行时，完成自定义解析、统计、作图或多个软件产物的组合分析。

三层均坚持同一原则：**后端、方法、模型、资源和科学参数由智能体显式选择；系统不自动重试、不静默降级，也不替换不可用方法。**

本目录的主要事实来源是 `chemistry_toolbox/src/catalog.py`、`chemistry_toolbox/config/native_software_guides.yaml` 和运行时健康探测，而不是任务说明或历史运行报告。

## 2. 科学 Action 能力分布

| 领域 | Action 数 | 能力范围 |
|---|---:|---|
| 科学数据交换 | 3 | QCSchema 规范化与校验、量化输出解析 |
| 结构与体系构建 | 19 | 分子/晶体标准化、三维结构、构象、质子化、力场、溶剂化与表面模型 |
| 化学信息学 | 6 | 描述符、指纹、相似性、子结构、互变异构与立体异构 |
| 分子电子结构 | 22 | 能量、力、Hessian、优化、轨道、电荷、电子密度、光谱与热化学 |
| 反应与动力学 | 14 | 过渡态、反应路径、IRC、坐标扫描、平衡、速率、主方程与微观动力学 |
| 分子动力学 | 23 | 体系最小化、动力学传播、轨迹分析、自由能与集体变量 |
| 周期体系与声子 | 16 | 周期能量/力/应力、结构弛豫、能带/DOS、成键、声子与热导率 |
| 分子对接 | 1 | 已准备受体和配体的显式搜索空间对接 |
| 外部科学数据 | 10 | PubChem、RCSB PDB、Materials Project、Catalysis-Hub 与 NIST WebBook |

### 2.1 Action 的使用契约

- 先用 `list_action_domains`、`search_actions` 查找候选 Action，再用 `inspect_action` 查看精确输入、可选后端、方法字段、资源和参数约束。
- 用 `inspect_backend` 检查后端的安装健康状态和对应 Action 的完整契约；涉及赝势或模型时，用 `search_resources`、`inspect_resource` 明确选择资源。
- 用 `execute_action` 执行。密集结果以带哈希和谱系的 `ArtifactRef` 保存，工具响应只返回必要摘要，避免大矩阵、轨迹或网格淹没上下文。
- CPU、内存和 GPU 可由智能体在评估器给定的资源上限内申请；超时由评估器的“计算类/快速类”策略统一控制，不作为智能体可调科学参数。

<details>
<summary><strong>完整 Action 目录（114 项）</strong></summary>

下表保留目录中的官方英文定义，避免翻译改变科学边界。`Providers` 是可显式选择的后端；同一 Action 的不同后端通常具有不同的方法与参数契约。

#### 科学数据交换（3）

| Action ID | 官方功能定义 | Providers | 主输出 |
|---|---|---|---|
| `normalize_qcschema_molecule` | Validate and normalize one supplied molecular structure into a QCSchema Molecule record without launching a calculation. | `qcelemental` | `QCSchemaMolecule` |
| `validate_qcschema_record` | Validate one explicit QCSchema/QCArchive record type and return a normalized record or structured validation errors without executing it. | `qcelemental` | `QCSchemaValidationResult` |
| `parse_quantum_chemistry_output` | Parse explicitly selected properties from one existing quantum-chemistry output file without rerunning the calculation. | `cclib` | `ParsedQuantumChemistryResult` |

#### 结构与体系构建（19）

| Action ID | 官方功能定义 | Providers | 主输出 |
|---|---|---|---|
| `standardize_structure` | Standardize one molecular representation without generating 3D coordinates or optimizing geometry. | `rdkit` | `AtomicStructure` |
| `generate_3d_structure` | Generate one explicit three-dimensional structure from a two-dimensional molecular representation. | `rdkit`, `openbabel` | `AtomicStructure` |
| `generate_conformer_ensemble` | Generate a conformer ensemble; it does not perform the later quantum refinement or final ranking workflow. | `rdkit_etkdg`, `crest` | `ConformerEnsemble` |
| `cluster_conformers` | Cluster an already supplied conformer ensemble by an explicit heavy/all-atom RMSD cutoff without generating or ranking conformers. | `rdkit` | `ConformerClusterResult` |
| `align_molecular_structures` | Rigidly align one supplied 3D probe structure to a reference using an explicit atom-to-atom map. | `rdkit` | `StructureAlignmentResult` |
| `rank_conformers_from_results` | Rank and weight conformers only from aligned energies or free energies already supplied by the agent. | `internal_statistics` | `ConformerEnsemble` |
| `enumerate_coordination_isomers` | Enumerate symmetry-distinct ligand-to-site assignments for an explicitly selected coordination geometry without inventing coordinates or ranking their energies. | `internal_reaction_analysis` | `CoordinationIsomerAssignments` |
| `repair_biomolecular_structure` | Repair missing biomolecular residues or atoms without choosing protonation, force field, solvent, or dynamics settings. | `pdbfixer` | `AtomicStructure` |
| `select_structure_subset` | Select explicit chains and/or models from one PDB structure, with an explicit choice about retaining heteroatom records. | `pdb_tools` | `AtomicStructure` |
| `renumber_biomolecular_structure` | Renumber PDB atom serials and residue identifiers from explicit starting values without changing coordinates or chemistry. | `pdb_tools` | `AtomicStructure` |
| `normalize_pdb_records` | Sort and format one PDB record stream under explicit ordering, chain-break, and hybrid-36 choices. | `pdb_tools` | `AtomicStructure` |
| `assign_protonation_states` | Assign explicit protonation states using the agent-selected backend and pH/rule settings. | `rdkit`, `pdbfixer` | `AtomicStructure` |
| `assign_partial_charges` | Assign named force-field or docking partial charges without parameterizing or solvating the system. | `rdkit_gasteiger`, `openff_am1bcc` | `ChargedStructure` |
| `assign_force_field_parameters` | Assign an explicitly selected force field to an already prepared molecular system. | `openff`, `openmm_builder` | `ParameterizedSystem` |
| `solvate_molecular_system` | Build the explicitly requested solvent/ion environment without minimizing or propagating dynamics. | `openmm_builder`, `packmol` | `ParameterizedSystem` |
| `analyze_crystal_symmetry` | Determine the crystallographic space group and symmetry-equivalent sites for one supplied periodic structure. | `spglib`, `pymatgen` | `CrystalSymmetryResult` |
| `standardize_crystal_structure` | Standardize one periodic structure in an explicitly selected primitive or conventional crystallographic setting. | `spglib`, `pymatgen` | `AtomicStructure` |
| `build_supercell` | Apply one explicit integer supercell transformation to a periodic structure. | `pymatgen` | `AtomicStructure` |
| `enumerate_surface_slabs` | Enumerate a bounded set of symmetry-distinct slabs for one explicit Miller index and slab/vacuum geometry. | `pymatgen` | `StructureCollection` |

#### 化学信息学（6）

| Action ID | 官方功能定义 | Providers | 主输出 |
|---|---|---|---|
| `calculate_molecular_descriptors` | Calculate an explicitly selected set of graph-based molecular descriptors without generating coordinates or running electronic structure. | `rdkit` | `MolecularDescriptorResult` |
| `calculate_molecular_fingerprint` | Calculate one explicitly selected molecular fingerprint representation. | `rdkit` | `MolecularFingerprint` |
| `calculate_molecular_similarity` | Calculate one similarity value between two molecules using an explicit fingerprint and metric. | `rdkit` | `MolecularSimilarityResult` |
| `search_local_substructures` | Find atom-index matches for an explicit SMARTS or SMILES query in one supplied molecule. | `rdkit` | `SubstructureMatchResult` |
| `enumerate_tautomers` | Enumerate bounded tautomeric forms without selecting a preferred tautomer for the agent. | `rdkit` | `MoleculeCollection` |
| `enumerate_stereoisomers` | Enumerate bounded stereoisomers under explicit uniqueness and assignment rules. | `rdkit` | `MoleculeCollection` |

#### 分子电子结构（22）

| Action ID | 官方功能定义 | Providers | 主输出 |
|---|---|---|---|
| `calculate_energy` | Calculate one molecular or non-periodic scalar energy with the exact software and method selected by the agent. | `xtb`, `pyscf`, `psi4`, `tblite`, `gpaw`, `nwchem`, `openmolcas`, `mace`, `chgnet`, `deepmd`, `orca`, `gaussian`, `gamess`, `ase_emt` | `EnergyResult` |
| `calculate_forces` | Calculate atomic forces for one non-periodic structure or an aligned batch. | `xtb`, `pyscf`, `tblite`, `gpaw`, `nwchem`, `orca`, `mace`, `chgnet`, `deepmd`, `ase_emt` | `ForceResult` |
| `calculate_hessian` | Calculate one molecular Hessian without deriving modes, spectra, or thermochemistry. | `xtb`, `pyscf`, `psi4`, `tblite`, `nwchem`, `orca`, `gaussian`, `mace`, `chgnet`, `deepmd`, `ase_emt` | `Hessian` |
| `optimize_geometry` | Optimize one non-periodic geometry and return the optimized structure only as the primary result. | `xtb`, `tblite`, `gpaw`, `mace`, `chgnet`, `deepmd`, `orca`, `gaussian`, `gamess`, `ase_emt`, `geometric`, `sella` | `AtomicStructure` |
| `calculate_dipole_moment` | Calculate one molecular dipole moment with an explicitly chosen electronic method. | `xtb`, `tblite`, `pyscf`, `psi4`, `nwchem`, `openmolcas`, `orca`, `gaussian`, `gamess` | `DipoleResult` |
| `calculate_atomic_charges` | Calculate electronic-structure population-analysis charges without attaching force-field parameters. | `xtb`, `pyscf`, `psi4`, `nwchem`, `openmolcas`, `multiwfn`, `orca` | `AtomicChargeResult` |
| `calculate_orbitals` | Calculate orbital energies, occupations, and optional coefficient artifacts. | `pyscf`, `psi4`, `openmolcas`, `orca` | `OrbitalResult` |
| `calculate_correlated_electron_density` | Calculate and retain one explicitly selected molecular electron density, including SCF/DFT, relaxed MP2 or double-hybrid, and unrelaxed CCSD density sources, without silently substituting an unavailable density model. | `orca` | `ElectronDensityResult` |
| `export_electron_density_grid` | Export a previously calculated ORCA electron density to an explicitly selected WFN, WFX, or cube representation while preserving the named density source in provenance. | `orca` | `ElectronDensityExportResult` |
| `calculate_electron_isodensity_surface` | Calculate molecular electron-isodensity surface area and enclosed volume for an explicit list of density cutoffs using one supplied wavefunction or electron-density grid. | `multiwfn` | `ElectronIsodensitySurfaceResult` |
| `calculate_bond_orders` | Calculate atom-pair electronic bond-order indices using one explicitly selected population-analysis backend. | `xtb`, `multiwfn`, `orca` | `BondOrderResult` |
| `calculate_excited_states` | Calculate a bounded set of vertical electronic excited states without constructing a broadened spectrum or propagating dynamics. | `pyscf`, `orca` | `ExcitedStateResult` |
| `analyze_electron_density_topology` | Locate and characterize critical points in one supplied molecular or periodic electron-density field without generating that field or integrating atomic basins. | `critic2` | `ElectronDensityTopologyResult` |
| `calculate_atomic_basin_properties` | Integrate population, Laplacian, and available volume properties over atomic or attractor basins in one supplied scalar-field grid using an explicitly selected partition algorithm. | `critic2` | `AtomicBasinPropertyResult` |
| `calculate_bader_charges` | Calculate atomic Bader charges from one supplied electron-density grid using an explicitly selected Yu-Trinkle or Henkelman grid partition. | `critic2` | `AtomicChargeResult` |
| `derive_vibrational_modes` | Derive frequencies and normal modes from an existing Hessian and structure. | `internal_vibrations` | `FrequencyResult` |
| `derive_ir_spectrum` | Construct an IR spectrum from vibration results that already contain intensities. | `internal_spectroscopy` | `SpectrumResult` |
| `derive_uv_vis_spectrum` | Construct a deterministic broadened UV/visible spectrum from supplied transition energies and oscillator strengths. | `internal_spectroscopy` | `SpectrumResult` |
| `derive_thermochemistry` | Derive thermochemical quantities from supplied electronic energy and frequencies; no optimization or Hessian is hidden. | `internal_thermochemistry`, `goodvibes` | `ThermochemistryResult` |
| `scan_thermochemistry_temperature` | Evaluate thermochemical quantities for supplied quantum outputs at each explicitly listed temperature without rerunning electronic-structure calculations. | `goodvibes` | `ThermochemistryTemperatureSeries` |
| `analyze_thermochemical_ensemble` | Calculate per-structure thermochemistry and Boltzmann populations for an explicitly supplied conformer or structure ensemble. | `goodvibes` | `ThermochemicalEnsembleResult` |
| `validate_thermochemistry_inputs` | Check supplied quantum outputs for thermochemistry compatibility, calculation consistency, frequency issues, and possible duplicate structures. | `goodvibes` | `ThermochemistryValidationReport` |

#### 反应与动力学（14）

| Action ID | 官方功能定义 | Providers | 主输出 |
|---|---|---|---|
| `locate_transition_state` | Locate one candidate transition-state structure without automatically running frequencies or IRC. | `pysisyphus`, `sella` | `AtomicStructure` |
| `search_reaction_path` | Run an explicitly selected double-ended chain-of-states search between supplied reactant and product structures without asserting that the highest image is a validated transition state. | `pysisyphus` | `ReactionPath` |
| `scan_reaction_coordinates` | Run one relaxed one-dimensional internal-coordinate scan from a supplied structure using explicit coordinate, range, optimizer, and calculator settings. | `pysisyphus` | `ReactionCoordinateScan` |
| `validate_reaction_path` | Check atom/state consistency, endpoint agreement, image continuity, and optional bond-change progress for an already calculated reaction path. | `internal_reaction_analysis` | `ReactionPathValidationResult` |
| `analyze_reaction_coordinate` | Convert supplied path images and aligned electronic energies into a normalized reaction-coordinate profile with relative energies and highest-image candidates. | `internal_reaction_analysis` | `ReactionCoordinateAnalysisResult` |
| `trace_intrinsic_reaction_coordinate` | Trace an IRC from an already supplied transition-state structure. | `pysisyphus` | `ReactionPath` |
| `calculate_chemical_equilibrium` | Calculate an equilibrium composition/state for an explicitly supplied mechanism and thermodynamic condition. | `cantera` | `EquilibriumResult` |
| `integrate_reaction_network` | Integrate one explicitly specified reaction network over time. | `scipy`, `cantera` | `KineticsTrajectory` |
| `calculate_rate_constants` | Evaluate an explicitly supplied Arrhenius, multi-Arrhenius, pressure-dependent Arrhenius, or Chebyshev kinetics model on explicit temperature/pressure points. | `rmg` | `RateConstantResult` |
| `calculate_tunneling_correction` | Calculate Wigner or Eckart transition-state tunneling correction factors at explicit temperatures. | `rmg` | `TunnelingCorrectionResult` |
| `solve_master_equation` | Solve an explicitly supplied gas-phase chemical master-equation model and extract pressure/temperature-dependent phenomenological rate coefficients without constructing or modifying the reaction model. | `mess`, `mesmer` | `MasterEquationResult` |
| `solve_microkinetic_model` | Solve one explicitly supplied microkinetic model without constructing the reaction model for the agent. | `catmap` | `MicrokineticResult` |
| `analyze_thermochemical_selectivity` | Calculate N-way thermodynamic selectivity from explicitly labeled structure ensembles, including two-label excess and delta-delta-G when applicable. | `goodvibes` | `ThermochemicalSelectivityResult` |
| `analyze_reaction_free_energy_profile` | Calculate relative electronic and thermochemical energies along explicitly defined reaction pathways, including stoichiometric sums and conformer ensembles. | `goodvibes` | `ReactionFreeEnergyProfileResult` |

#### 分子动力学（23）

| Action ID | 官方功能定义 | Providers | 主输出 |
|---|---|---|---|
| `minimize_system_energy` | Minimize an already parameterized system without automatically equilibrating or propagating dynamics. | `openmm`, `gromacs`, `lammps`, `hoomd`, `namd`, `amber_pmemd`, `charmm` | `ParameterizedSystem` |
| `calculate_force_field_energy` | Evaluate the total potential energy of an already parameterized system at explicitly selected stored coordinates/state without minimizing or propagating it. | `openmm`, `hoomd` | `ForceFieldEnergyResult` |
| `calculate_force_field_forces` | Evaluate atomic force-field forces for an already parameterized system at explicitly selected stored coordinates/state. | `openmm`, `hoomd` | `ForceResult` |
| `decompose_force_field_energy` | Decompose one OpenMM potential energy evaluation by the explicitly present Force objects without changing parameters or running dynamics. | `openmm` | `ForceFieldEnergyDecompositionResult` |
| `propagate_dynamics` | Propagate exactly one agent-defined dynamics segment and return its trajectory and final state. | `openmm`, `gromacs`, `lammps`, `hoomd`, `namd`, `amber_pmemd`, `charmm` | `Trajectory` |
| `calculate_trajectory_rmsd` | Calculate an RMSD time series for an explicitly selected trajectory atom group and reference. | `mdanalysis`, `mdtraj` | `TimeSeries` |
| `calculate_radius_of_gyration` | Calculate the radius-of-gyration time series for an explicitly selected atom group. | `mdanalysis`, `mdtraj` | `TimeSeries` |
| `calculate_radial_distribution` | Calculate one radial distribution function for two explicitly selected atom groups. | `mdanalysis` | `DistributionResult` |
| `calculate_mean_squared_displacement` | Calculate one mean-squared-displacement time series for an explicitly selected atom group. | `mdanalysis` | `TimeSeries` |
| `calculate_contacts` | Calculate inter-residue contact distances for an explicitly supplied residue-pair set and contact definition. | `mdtraj` | `ContactTimeSeries` |
| `calculate_solvent_accessible_surface` | Calculate solvent-accessible surface area per atom or residue for an existing trajectory. | `mdtraj` | `SurfaceAreaTimeSeries` |
| `calculate_dihedral_distribution` | Calculate dihedral-angle time series for explicitly supplied atom-index quartets. | `mdtraj`, `mdanalysis` | `DihedralTimeSeries` |
| `calculate_hydrogen_bonds` | Identify hydrogen-bond events in an existing trajectory using explicit donor, hydrogen, acceptor, distance, and angle definitions. | `mdanalysis` | `HydrogenBondResult` |
| `calculate_principal_components` | Calculate coordinate principal components and frame projections for an explicitly selected trajectory atom group. | `mdanalysis` | `PrincipalComponentResult` |
| `calculate_dynamic_cross_correlation` | Calculate an atom-wise dynamic cross-correlation matrix from explicitly selected and optionally aligned trajectory coordinates. | `mdanalysis` | `DynamicCrossCorrelationResult` |
| `assign_secondary_structure` | Assign per-residue secondary-structure labels for every frame of an existing protein trajectory. | `mdtraj` | `SecondaryStructureTimeSeries` |
| `cluster_trajectory` | Cluster explicitly selected trajectory frames by RMSD using a deterministic cutoff-based leader assignment. | `mdtraj` | `TrajectoryClusterResult` |
| `evaluate_collective_variables` | Evaluate explicitly defined collective variables on an existing trajectory. | `plumed` | `TimeSeries` |
| `estimate_free_energy_difference` | Estimate dimensionless pairwise free-energy differences from an explicitly supplied reduced-potential matrix and sample counts. | `pymbar` | `FreeEnergyDifferenceResult` |
| `estimate_thermodynamic_expectations` | Estimate state-resolved observable expectations from explicitly supplied samples and a reduced-potential matrix. | `pymbar` | `ThermodynamicExpectationResult` |
| `calculate_potential_of_mean_force` | Estimate a one-dimensional histogram free-energy profile from supplied uncorrelated samples; this does not integrate a mean-force trajectory or choose bins for the agent. | `pymbar` | `FreeEnergyProfileResult` |
| `analyze_free_energy_convergence` | Re-estimate one explicitly selected pairwise free-energy difference over supplied sample fractions without generating or decorrelating samples. | `pymbar` | `FreeEnergyConvergenceResult` |
| `parse_alchemical_energy_data` | Parse one or more explicitly identified engine output files into a normalized alchemical reduced-potential or derivative table. | `alchemlyb` | `AlchemicalEnergyData` |

#### 周期体系与声子（16）

| Action ID | 官方功能定义 | Providers | 主输出 |
|---|---|---|---|
| `calculate_periodic_energy` | Calculate one periodic-system energy with the explicitly selected electronic-structure backend. | `quantum_espresso`, `cp2k`, `siesta`, `dftbplus`, `abinit`, `vasp`, `gpaw`, `nequip`, `allegro`, `deepmd` | `EnergyResult` |
| `calculate_periodic_forces` | Calculate periodic atomic forces for one structure or aligned displaced-structure batch. | `quantum_espresso`, `cp2k`, `siesta`, `dftbplus`, `abinit`, `vasp`, `gpaw`, `nequip`, `allegro`, `deepmd` | `ForceResult` |
| `calculate_periodic_stress` | Calculate one periodic stress tensor without relaxing the structure. | `quantum_espresso`, `cp2k`, `abinit`, `vasp`, `gpaw`, `nequip`, `allegro`, `deepmd` | `StressResult` |
| `relax_periodic_structure` | Relax a periodic structure under explicit atomic/cell constraints. | `quantum_espresso`, `cp2k`, `siesta`, `dftbplus`, `abinit`, `vasp`, `gpaw`, `nequip`, `allegro`, `deepmd` | `AtomicStructure` |
| `calculate_electronic_band_structure` | Calculate electronic eigenvalue bands along one explicit reciprocal-space path from an existing converged periodic ground-state restart. | `gpaw` | `ElectronicBandStructureResult` |
| `calculate_density_of_states` | Calculate a total electronic density of states on an explicit energy grid from an existing converged periodic ground-state restart. | `gpaw` | `DensityOfStatesResult` |
| `calculate_projected_density_of_states` | Calculate or extract explicitly requested atom/orbital projected electronic densities of states from an existing compatible periodic electronic-state artifact. | `gpaw`, `lobster` | `ProjectedDensityOfStatesResult` |
| `analyze_periodic_bonding` | Extract explicitly selected integrated and optional energy-resolved COHP, COOP, or COBI bonding information from existing LOBSTER outputs. | `lobster` | `PeriodicBondingResult` |
| `calculate_charge_spilling` | Assess LOBSTER wavefunction-projection charge/total spilling against explicit acceptance thresholds from an existing lobsterout file. | `lobster` | `ProjectionQualityResult` |
| `generate_displaced_supercells` | Generate a displacement set from an explicit supercell matrix and displacement amplitude. | `phonopy`, `phono3py` | `DisplacementSet` |
| `assemble_force_constants` | Assemble force constants only from a supplied displacement set and aligned forces. | `phonopy`, `phono3py` | `ForceConstants` |
| `calculate_phonon_dispersion` | Calculate a phonon dispersion from existing force constants and an explicit q-point path. | `phonopy`, `phono3py` | `PhononDispersion` |
| `calculate_phonon_density_of_states` | Calculate a phonon density of states from existing force constants and an explicit q mesh. | `phonopy`, `phono3py` | `PhononDensityOfStates` |
| `calculate_harmonic_thermodynamics` | Calculate harmonic free energy, entropy, and constant-volume heat capacity at explicitly supplied temperatures. | `phonopy`, `phono3py` | `HarmonicThermodynamicsResult` |
| `calculate_phonon_group_velocities` | Calculate mode-resolved phonon group-velocity vectors along an explicitly supplied q-point path. | `phonopy`, `phono3py` | `PhononGroupVelocityResult` |
| `calculate_lattice_thermal_conductivity` | Calculate the lattice thermal-conductivity tensor from explicit second-/third-order force constants or a complete native BTE model under Agent-selected solution and scattering settings. | `phono3py`, `shengbte` | `LatticeThermalConductivityResult` |

#### 分子对接（1）

| Action ID | 官方功能定义 | Providers | 主输出 |
|---|---|---|---|
| `dock_ligand` | Dock an already prepared ligand into an already prepared receptor using an explicit search space. | `vina`, `gnina` | `DockingResult` |

#### 外部科学数据（10）

| Action ID | 官方功能定义 | Providers | 主输出 |
|---|---|---|---|
| `search_compounds` | Search PubChem compound records by an explicit identifier and namespace. | `pubchem` | `CompoundRecords` |
| `resolve_chemical_identity` | Resolve one explicit compound identifier to a bounded ChemicalIdentity record through PubChem. | `pubchem` | `ChemicalIdentity` |
| `retrieve_compound_properties` | Retrieve an explicitly selected bounded property set for matching PubChem compounds. | `pubchem` | `CompoundPropertyRecords` |
| `retrieve_compound_structure` | Retrieve bounded PubChem 2D or 3D coordinate records while leaving coordinate dimensionality and explicit-hydrogen handling to the agent. | `pubchem` | `StructureCollection` |
| `search_similar_compounds` | Run one bounded PubChem 2D similarity search from an explicit structure identifier. | `pubchem` | `CompoundRecords` |
| `search_substructures` | Run one bounded PubChem substructure search from an explicit SMILES, SMARTS, InChI, or CID query. | `pubchem` | `CompoundRecords` |
| `search_protein_structures` | Search or retrieve RCSB PDB structure records using explicit identifiers or query terms. | `rcsb_pdb` | `ProteinStructureRecords` |
| `search_materials` | Search Materials Project records by material id, formula, or explicit query fields. | `materials_project` | `MaterialRecords` |
| `search_catalysis_records` | Search Catalysis-Hub reaction records using explicit reactant/product filters. | `catalysis_hub` | `CatalysisRecords` |
| `lookup_nist_webbook_species` | Look up one bounded NIST Chemistry WebBook species query by explicit CAS number, exact name, or exact formula through the official CGI interface. | `nist_webbook` | `NISTWebBookSpeciesRecords` |

</details>

## 3. 后端软件与程序

### 3.1 Action 后端

当前注册 77 个后端。状态以 Action 运行时健康探测为准；`materials_project` 的接口代码已安装，但当前缺少有效服务凭据，因此其 Action 状态为不可用。

<details>
<summary><strong>完整后端清单（77 项）</strong></summary>

| Backend ID | 软件/实现 | 运行时 | 状态 | 原生命令 | 覆盖 Action 数 |
|---|---|---|---|---|---:|
| `abinit` | ABINIT | `abinit` | 可用 | `abinit` | 4 |
| `alchemlyb` | alchemlyb | `free_energy` | 可用 | — | 1 |
| `allegro` | Allegro | `nequip` | 可用 | — | 4 |
| `amber_pmemd` | Amber 26 PMEMD | `amber` | 可用 | `pmemd`, `pmemd.MPI`, `mpirun` | 2 |
| `ase_emt` | ASE EMT | `core` | 可用 | — | 4 |
| `cantera` | Cantera | `reaction` | 可用 | — | 2 |
| `catalysis_hub` | Catalysis-Hub GraphQL | `services` | 可用 | — | 1 |
| `catmap` | CatMAP | `reaction` | 可用 | — | 1 |
| `cclib` | cclib | `workflows` | 可用 | — | 1 |
| `charmm` | CHARMM c50b2 | `charmm` | 可用 | `charmm` | 2 |
| `chgnet` | CHGNet | `mlip` | 可用 | — | 4 |
| `cp2k` | CP2K | `cp2k` | 可用 | `cp2k` | 4 |
| `crest` | CREST | `reaction` | 可用 | `crest` | 1 |
| `critic2` | Critic2 | `critic2` | 可用 | `critic2` | 3 |
| `deepmd` | DeePMD-kit | `deepmd` | 可用 | `dp` | 8 |
| `dftbplus` | DFTB+ | `periodic` | 可用 | `dftb+` | 3 |
| `gamess` | GAMESS | `gamess` | 可用 | `rungms` | 3 |
| `gaussian` | Gaussian 16 | `gaussian` | 可用 | `g16`, `formchk` | 4 |
| `geometric` | geomeTRIC | `nwchem` | 可用 | `geometric-optimize` | 1 |
| `gnina` | GNINA | `docking` | 可用 | `gnina` | 1 |
| `goodvibes` | GoodVibes | `goodvibes` | 可用 | `goodvibes` | 6 |
| `gpaw` | GPAW | `gpaw` | 可用 | `gpaw` | 10 |
| `gromacs` | GROMACS | `md` | 可用 | `gmx` | 2 |
| `hoomd` | HOOMD-blue | `free_energy` | 可用 | — | 4 |
| `internal_reaction_analysis` | ResearchChem reaction/coordination analysis | `core` | 可用 | — | 3 |
| `internal_spectroscopy` | ResearchChem spectrum builder | `core` | 可用 | — | 2 |
| `internal_statistics` | ResearchChem deterministic statistics | `core` | 可用 | — | 1 |
| `internal_thermochemistry` | ResearchChem statistical thermochemistry | `core` | 可用 | — | 1 |
| `internal_vibrations` | ResearchChem vibrational analysis | `core` | 可用 | — | 1 |
| `lammps` | LAMMPS | `md` | 可用 | `lmp` | 2 |
| `lobster` | LOBSTER | `lobster` | 可用 | `lobster-5.1.0` | 3 |
| `mace` | MACE | `mlip` | 可用 | — | 4 |
| `materials_project` | Materials Project | `services` | 不可用 | — | 1 |
| `mdanalysis` | MDAnalysis | `md` | 可用 | — | 8 |
| `mdtraj` | MDTraj | `workflows` | 可用 | — | 7 |
| `mesmer` | MESMER | `mesmer` | 可用 | `mesmer` | 1 |
| `mess` | MESS | `mess` | 可用 | `mess` | 1 |
| `multiwfn` | Multiwfn | `multiwfn` | 可用 | `Multiwfn_noGUI` | 3 |
| `namd` | NAMD 3 | `namd` | 可用 | `namd3` | 2 |
| `nequip` | NequIP | `nequip` | 可用 | `nequip-train` | 4 |
| `nist_webbook` | NIST Chemistry WebBook SRD 69 CGI | `services` | 可用 | — | 1 |
| `nwchem` | NWChem | `nwchem` | 可用 | `nwchem` | 5 |
| `openbabel` | Open Babel | `quantum` | 可用 | `obabel` | 1 |
| `openff` | OpenFF Toolkit/Interchange | `openff` | 可用 | — | 1 |
| `openff_am1bcc` | OpenFF AM1-BCC | `openff` | 可用 | `antechamber`, `sqm` | 1 |
| `openmm` | OpenMM | `md` | 可用 | — | 5 |
| `openmm_builder` | OpenMM system builder | `md` | 可用 | — | 2 |
| `openmolcas` | OpenMolcas | `openmolcas` | 可用 | `pymolcas` | 4 |
| `orca` | ORCA | `quantum` | 可用 | `orca` | 11 |
| `packmol` | Packmol | `md` | 可用 | `packmol` | 1 |
| `pdb_tools` | pdb-tools | `core` | 可用 | `pdb_selchain`, `pdb_reres`, `pdb_tidy` | 3 |
| `pdbfixer` | PDBFixer | `md` | 可用 | — | 2 |
| `phono3py` | Phono3py | `phonons` | 可用 | `phono3py` | 7 |
| `phonopy` | Phonopy | `phonons` | 可用 | `phonopy` | 6 |
| `plumed` | PLUMED | `md` | 可用 | `plumed` | 1 |
| `psi4` | Psi4 | `psi4` | 可用 | `psi4` | 5 |
| `pubchem` | PubChem PUG REST | `services` | 可用 | — | 6 |
| `pymatgen` | pymatgen | `workflows` | 可用 | — | 4 |
| `pymbar` | PyMBAR | `free_energy` | 可用 | — | 4 |
| `pyscf` | PySCF | `quantum` | 可用 | — | 7 |
| `pysisyphus` | pysisyphus | `reaction` | 可用 | `pysis` | 4 |
| `qcelemental` | QCElemental | `workflows` | 可用 | — | 2 |
| `quantum_espresso` | Quantum ESPRESSO | `qe` | 可用 | `pw.x` | 4 |
| `rcsb_pdb` | RCSB PDB Data API | `services` | 可用 | — | 1 |
| `rdkit` | RDKit | `core` | 可用 | — | 11 |
| `rdkit_etkdg` | RDKit ETKDG | `core` | 可用 | — | 1 |
| `rdkit_gasteiger` | RDKit Gasteiger charges | `core` | 可用 | — | 1 |
| `rmg` | RMG-Py | `rmg` | 可用 | `rmg.py` | 2 |
| `scipy` | SciPy | `reaction` | 可用 | — | 1 |
| `sella` | Sella | `sella` | 可用 | — | 2 |
| `shengbte` | ShengBTE | `shengbte` | 可用 | `ShengBTE` | 1 |
| `siesta` | SIESTA | `periodic` | 可用 | `siesta` | 3 |
| `spglib` | spglib | `workflows` | 可用 | — | 2 |
| `tblite` | TBLite | `quantum` | 可用 | — | 5 |
| `vasp` | VASP | `vasp` | 可用 | `vasp_std` | 4 |
| `vina` | AutoDock Vina | `docking` | 可用 | `vina` | 1 |
| `xtb` | xTB | `reaction` | 可用 | `xtb` | 7 |

</details>

### 3.2 主要软件家族及适用场景

| 科研环节 | 可选软件/实现 | 典型用途 |
|---|---|---|
| 分子构建与化学信息学 | RDKit、Open Babel、CREST、PDBFixer、pdb-tools、OpenFF、Packmol、pymatgen、spglib | 结构清理、3D/构象、质子化、电荷/力场、溶剂化、晶体和表面构建 |
| 分子量子化学 | xTB、TBLite、PySCF、Psi4、ORCA、Gaussian 16、GAMESS、NWChem、OpenMolcas、GPAW | 能量、梯度、Hessian、结构优化、轨道、电荷、激发态与电子密度 |
| 波函数与热化学后处理 | Multiwfn、Critic2、GoodVibes、cclib、内部振动/光谱/热化学模块 | 等密度面、QTAIM/Bader、频率、热化学、光谱和结果解析 |
| 机器学习势 | MACE、CHGNet、DeePMD-kit、NequIP、Allegro、ASE EMT | 分子或周期体系的能量、力、应力和结构优化 |
| 反应路径与动力学 | pysisyphus、Sella、geomeTRIC、Cantera、RMG-Py、MESS、MESMER、CatMAP、SciPy | TS、NEB/链式路径、IRC、坐标扫描、速率、主方程和微观动力学 |
| 分子动力学与自由能 | OpenMM、GROMACS、LAMMPS、HOOMD-blue、NAMD、Amber PMEMD、CHARMM、PLUMED、MDAnalysis、MDTraj、PyMBAR、alchemlyb | 最小化、MD、增强采样、轨迹分析和自由能估计 |
| 周期电子结构与晶格动力学 | Quantum ESPRESSO、CP2K、SIESTA、DFTB+、ABINIT、VASP、GPAW、LOBSTER、Phonopy、Phono3py、ShengBTE | 周期能量/力/应力、能带、DOS、成键、声子和热输运 |
| 分子对接 | AutoDock Vina、GNINA | 显式搜索盒中的受体—配体对接 |
| 在线数据服务 | PubChem、RCSB PDB、Materials Project、Catalysis-Hub、NIST Chemistry WebBook | 化合物、蛋白结构、材料、催化反应和物性数据检索 |

当前探测到的代表性版本包括：ORCA 6.1.1、Gaussian 16 C.01、xTB 6.7.1、PySCF 2.13.1、NWChem 7.3.1、OpenMolcas 25.10、GPAW 25.7.0、Quantum ESPRESSO 7.5、CP2K 2026.1、ABINIT 10.0.3、VASP 6.3.2、LOBSTER 5.1.0、OpenMM 8.5.2、Multiwfn 2026.7.15 和 GoodVibes 4.3.0。完整版本与可执行路径应以 `inspect_software` 的当次返回为准。

### 3.3 可原生直调但尚无预设 Action 的程序

这些程序已安装或已配置运行时，可通过 `inspect_software` 获取命令和本地文档，再经 `validate_native_job` / `submit_native_job` 调用。它们不代表工具箱会自动生成正确输入，科学路线仍由智能体负责。

| Software ID | 软件 | 运行时 | 允许的原生命令 |
|---|---|---|---|
| `aiida` | AiiDA | `workflows` | `verdi` |
| `arkane` | Arkane | `rmg` | `Arkane.py` |
| `atomate2` | atomate2 | — | Python/API |
| `autode` | autodE | — | Python/API |
| `automekin` | AutoMeKin | `automekin` | `amk.sh`, `mopac`, `bbfs.exe` |
| `censo` | CENSO | `censo` | `censo` |
| `jobflow` | jobflow | — | Python/API |
| `kinbot` | KinBot | `kinbot` | `kinbot`, `pes` |
| `newton_x` | Newton-X | `newtonx` | `nx_geninp`, `nx_moldyn`, `nx_test` |
| `qcengine` | QCEngine | `workflows` | `qcengine` |
| `sharc` | SHARC | `sharc` | `sharc.x`, `wfoverlap.x` |
| `theodore` | TheoDORE | `theodore` | `theodore` |
| `vesta` | VESTA | `vesta` | `VESTA` |
| `vmd` | VMD | `vmd` | `vmd` |
| `wannier90` | Wannier90 | `qe` | `wannier90.x` |
| `yambo` | Yambo | `yambo` | `p2y`, `yambo` |

覆盖的软件包括工作流编排（AiiDA、atomate2、jobflow、QCEngine）、自动反应探索（AutoMeKin、KinBot、autodE、Arkane、CENSO）、非绝热/激发态分析（Newton-X、SHARC、TheoDORE）、周期后处理与可视化（Wannier90、Yambo、VESTA、VMD）。

## 4. 原生执行与可编程分析

### 4.1 原生软件执行流程

1. `list_software`：按名称、状态或能力筛选完整软件目录。
2. `inspect_software`：查看精确版本、运行时、命令模板、输入模式、必要文件、本地手册和 Action 覆盖。
3. `search_software_documentation`：在缓存的官方文档中检索关键词，避免凭记忆猜命令。
4. `write_workspace_text`：把智能体编写的输入文件或脚本写入任务工作区。
5. `validate_native_job`：只做命令允许列表、路径、文件映射和资源约束校验，不替智能体检查科学方法是否合理。
6. `submit_native_job`：以 `shell=false` 异步提交到隔离作业目录；随后用 `get_execution_job` 查看状态，用 `collect_execution_job` 收集带 SHA-256 的输出。
7. 必要时用 `cancel_execution_job` 终止作业，并用 `declare_scientific_artifact` 登记重要产物及其父级谱系。

### 4.2 可编程分析运行时

`submit_analysis_program` 可在选定运行时中执行智能体编写的 `.py` 文件。脚本、输入、标准输出、标准错误、资源使用和产物统一进入持久作业记录。当前运行时如下：

<details>
<summary><strong>完整运行时清单（42 项）</strong></summary>

| Runtime | 用途 | 关联后端 |
|---|---|---|
| `abinit` | Isolated ABINIT executable used only when the Agent selects backend_id=abinit. | `abinit` |
| `amber` | Amber 26 licensed PMEMD CPU serial and OpenMPI executables. | `amber_pmemd` |
| `automekin` | AutoMeKin source build with its bundled MOPAC engine and isolated Python/compiler dependencies. | 原生程序专用 |
| `charmm` | Academic CHARMM c50b2 serial/OpenMP GNU source build. | `charmm` |
| `core` | Core runtime for cheminformatics and deterministic analysis backends. | `rdkit`, `rdkit_etkdg`, `rdkit_gasteiger`, `internal_statistics`, `ase_emt`, `internal_vibrations`, `internal_spectroscopy`, `internal_thermochemistry`, `internal_reaction_analysis`, `pdb_tools` |
| `cp2k` | Isolated CP2K runtime. | `cp2k` |
| `critic2` | Critic2 1.2.1081 typed QTAIM critical-point analysis runtime. | `critic2` |
| `deepmd` | DeePMD-kit 3.2.0b0 CPU inference runtime for the downloaded DPA multitask and OMol checkpoints. | `deepmd` |
| `docking` | Protein-ligand docking binaries and model-specific docking tools. | `vina`, `gnina` |
| `free_energy` | Explicit statistical free-energy estimation and alchemical analysis runtime. | `pymbar`, `alchemlyb`, `hoomd` |
| `gamess` | Registered GAMESS 15 Jul 2024 R2 Patch 1 sockets-DDI source build. | `gamess` |
| `gaussian` | Licensed Gaussian 16 C.01 executable and formatted-checkpoint runtime. | `gaussian` |
| `goodvibes` | Isolated GoodVibes 4.3.0 thermochemistry, ensemble, selectivity, validation, and reaction-profile runtime. | `goodvibes` |
| `gpaw` | GPAW 25.7.0 molecular and periodic PAW-DFT runtime with locally managed setup datasets. | `gpaw` |
| `kinbot` | KinBot 2.2.2 with Sella/JAX and geometry dependencies. | 原生程序专用 |
| `lobster` | Licensed LOBSTER 5.1.0 periodic bonding and projected-DOS postprocessing runtime. | `lobster` |
| `md` | Molecular dynamics preparation, execution, enhanced sampling, and analysis. | `pdbfixer`, `openmm_builder`, `packmol`, `openmm`, `gromacs`, `lammps`, `mdanalysis`, `plumed` |
| `mesmer` | MESMER 7.1 master-equation runtime for an Agent-supplied XML reaction model. | `mesmer` |
| `mess` | MESS 2020.1.24 master-equation runtime for an Agent-supplied native reaction model. | `mess` |
| `mlip` | Machine-learning interatomic potentials and model-isolated runtimes. | `mace`, `chgnet` |
| `multiwfn` | Multiwfn 2026.7.15 noGUI typed wavefunction, density-grid, and electron-isodensity-surface analysis runtime. | `multiwfn` |
| `namd` | NAMD 3.0.2 multicore AVX-512 runtime; the CUDA bundle is cached but not selected automatically. | `namd` |
| `nequip` | NequIP 0.19.0 and Allegro 0.8.3 inference runtime with explicitly registered local checkpoints. | `nequip`, `allegro` |
| `newtonx` | Newton-X New Series 3.5.3 nonadiabatic dynamics and input-generation runtime. | 原生程序专用 |
| `nwchem` | NWChem 7.3.x single-geometry QCSchema runtime with local official basis libraries. | `nwchem`, `geometric` |
| `openff` | Isolated modern OpenFF Toolkit, Interchange, and AmberTools runtime. | `openff_am1bcc`, `openff` |
| `openmolcas` | OpenMolcas v25.10 molecular SCF runtime with typed HF/DFT property adapters. | `openmolcas` |
| `periodic` | DFTB+ and SIESTA backend runtime; ABINIT remains separately isolated. | `dftbplus`, `siesta` |
| `phonons` | Isolated Phonopy and Phono3py runtime. | `phonopy`, `phono3py` |
| `psi4` | Isolated Psi4 Python runtime. | `psi4` |
| `qe` | Isolated Quantum ESPRESSO runtime. | `quantum_espresso` |
| `quantum` | Molecular quantum chemistry and ASE calculation tools, including typed ORCA 6.1.1 correlated-density generation and density export; Psi4 remains isolated. | `openbabel`, `pyscf`, `tblite`, `orca` |
| `reaction` | Conformer refinement, reaction paths, and kinetics. | `xtb`, `crest`, `pysisyphus`, `cantera`, `scipy`, `catmap` |
| `rmg` | RMG-Py 4.0.0 typed kinetics and tunneling runtime. | `rmg` |
| `sella` | Sella 2.5.0 composite minimum/transition-state optimizer using an Agent-selected calculator backend. | `sella` |
| `services` | Remote scientific data services and authenticated materials lookup. | `pubchem`, `rcsb_pdb`, `materials_project`, `catalysis_hub`, `nist_webbook` |
| `sharc` | SHARC4 core source build plus the ASCII wfoverlap executable. | 原生程序专用 |
| `shengbte` | ShengBTE source revision b0d2090 for Agent-supplied phonon-BTE models. | `shengbte` |
| `theodore` | TheoDORE 2.5.0 excited-state analysis runtime with cclib. | 原生程序专用 |
| `vasp` | Locally compiled VASP 6.3.2 standard executable with OpenMPI and an explicit-POTCAR atomic adapter. | `vasp` |
| `workflows` | Crystal structure, symmetry, and lightweight trajectory-analysis libraries. | `qcelemental`, `cclib`, `pymatgen`, `spglib`, `mdtraj` |
| `yambo` | Yambo 5.3.0 single-process executable and p2y interface. | 原生程序专用 |

</details>

这层适合完成 Action 之外的通用工作，例如：批量读取结果、能量单位换算、构象排序、Bootstrap/回归、曲线拟合、误差统计、表格汇总和科研作图。它不能绕过软件允许列表、工作区路径和任务资源上限。

## 5. 科学资源

资源必须通过明确的 `resource_id` 选择，工具箱不替智能体决定赝势家族、模型大小或参数集。

| Resource ID | 内容 | 格式 | 适用后端 |
|---|---|---|---|
| `qe_sssp_1_3_pbe_efficiency` | SSSP 1.3.0 PBE efficiency | UPF | `quantum_espresso` |
| `qe_sssp_1_3_pbe_precision` | SSSP 1.3.0 PBE precision | UPF | `quantum_espresso` |
| `siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml` | PseudoDojo NC-SR-05 PBE standard PSML | PSML 1.1 | `siesta` |
| `abinit_pseudo_dojo_nc_sr_pbe_standard_psp8` | PseudoDojo NC-SR PBE standard PSP8 | PSP8 | `abinit` |
| `dftb_3ob_3_1` | DFTB+ 3ob 3.1 | Slater-Koster SKF | `dftbplus` |
| `dftb_matsci_0_3` | DFTB+ matsci 0.3 | Slater-Koster SKF | `dftbplus` |
| `gnina_1_3_3_cuda12_8_linux_x86_64` | GNINA 1.3.3 CUDA 12.8 static binary | Linux x86_64 executable | `gnina` |
| `orca_6_1_1_linux_x86_64_shared_openmpi418_avx2` | ORCA 6.1.1 Linux x86-64 AVX2 (shared OpenMPI 4.1.8) | Linux x86-64 AVX2 executable bundle | `orca` |
| `openmpi_4_1_8_orca_runtime` | OpenMPI 4.1.8 runtime for ORCA | Linux x86-64 shared MPI runtime | `orca` |
| `nequip_oam_s_0_1` | NequIP OAM-S 0.1 | NequIP compiled model archive | `nequip` |
| `nequip_oam_m_0_1` | NequIP OAM-M 0.1 | NequIP compiled model archive | `nequip` |
| `nequip_oam_l_0_1` | NequIP OAM-L 0.1 | NequIP compiled model archive | `nequip` |
| `nequip_oam_xl_0_1` | NequIP OAM-XL 0.1 | NequIP compiled model archive | `nequip` |
| `nequip_mp_l_0_1` | NequIP MP-L 0.1 | NequIP compiled model archive | `nequip` |
| `allegro_oam_l_0_1` | Allegro OAM-L 0.1 | NequIP compiled Allegro model archive | `allegro` |
| `allegro_mp_l_0_1` | Allegro MP-L 0.1 | NequIP compiled Allegro model archive | `allegro` |
| `deepmd_dpa_3_1_3m` | DeePMD DPA-3.1-3M | DeePMD PyTorch frozen multitask model | `deepmd` |
| `deepmd_dpa_3_2_5m` | DeePMD DPA-3.2-5M | DeePMD PyTorch frozen multitask model | `deepmd` |
| `deepmd_dpa_3_3_1m` | DeePMD DPA-3.3-1M | DeePMD PyTorch frozen multitask model | `deepmd` |
| `deepmd_dpa_2_4_7m` | DeePMD DPA-2.4-7M | DeePMD PyTorch frozen multitask model | `deepmd` |
| `deepmd_dpa3_omol_large` | DeePMD DPA3-Omol-Large | DeePMD PyTorch frozen single-task model | `deepmd` |
| `vasp_uspp_lda_legacy` | VASP legacy USPP LDA potentials (operator-supplied potpaw54 archive) | VASP POTCAR / ultrasoft pseudopotential | `vasp` |
| `vasp_uspp_gga_legacy` | VASP legacy USPP GGA potentials (operator-supplied potpaw54 archive) | VASP POTCAR / ultrasoft pseudopotential | `vasp` |
| `vasp_paw_lda_54` | VASP PAW LDA 5.4-family potentials (operator-supplied) | VASP POTCAR / PAW | `vasp` |
| `vasp_paw_pw91_54` | VASP PAW PW91 5.4-family potentials (operator-supplied subset) | VASP POTCAR / PAW | `vasp` |
| `vasp_paw_pbe_54` | VASP PAW PBE 5.4-family potentials (operator-supplied) | VASP POTCAR / PAW | `vasp` |
| `vasp_6_3_2_testsuite_si_potcar` | VASP 6.3.2 bundled testsuite Si POTCAR | VASP POTCAR | `vasp` |

资源主要分为四类：

- **周期计算赝势/参数**：Quantum ESPRESSO SSSP、SIESTA PseudoDojo、ABINIT PSP8、VASP 多套 POTCAR。
- **DFTB 参数**：3ob 3.1 与 matsci 0.3 Slater–Koster 集。
- **机器学习势权重**：NequIP、Allegro 与 DeePMD 多个模型检查点。
- **程序运行包**：ORCA/OpenMPI 和 GNINA 的受控本地运行资源。

## 6. 结果、可复现性与能力边界

- 每次调用都保留请求、选定后端、方法参数、资源、运行状态、标准输出/错误、文件哈希和产物谱系，便于审计与复跑。
- “后端已安装”不等于“任意科学问题都能自动完成”：反应物/产物映射、初始构象、TS 猜测、力场适用性、赝势选择、收敛判据和结果解释仍属于智能体的科研决策。
- 原生直调能扩展尚未预设为 Action 的软件功能，但不会自动补齐缺失输入，也不会保证输入方法与论文一致。
- 在线数据源受网络、配额和凭据影响；商业或学术许可软件只在本机授权范围内可用。
- 目录状态是运行时快照。对外演示或正式评测前，建议重新执行后端健康检查，并记录当次软件版本和资源清单。

## 7. 推荐介绍方式

对外可将本工具箱概括为：

> 一个面向自主化学科研的分层执行环境：以 114 个类型化科学 Action 提供稳定接口，以 77 个注册后端覆盖分子量子化学、反应动力学、分子动力学、周期材料、声子热输运、对接和科学数据检索；同时保留受控的原生软件调用与 Python 可编程分析能力，并对输入、资源、执行和产物进行全程溯源。
