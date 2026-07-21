# ResearchChemBench Actions 汇总

Action 总数：**101**

| 序号 | Action | 类别 | 可选 Backend | 作用 |
|---:|---|---|---|---|
| 1 | normalize_qcschema_molecule | 科学数据交换 | qcelemental | 校验并规范化一个分子结构，生成 QCSchema Molecule 记录，不启动计算。 |
| 2 | validate_qcschema_record | 科学数据交换 | qcelemental | 校验指定类型的 QCSchema 或 QCArchive 记录，返回规范化记录或结构化错误。 |
| 3 | parse_quantum_chemistry_output | 科学数据交换 | cclib | 从已有量子化学输出文件中解析指定性质，不重新运行计算。 |
| 4 | standardize_structure | 结构与体系 | rdkit | 标准化分子表示，不生成三维坐标或进行几何优化。 |
| 5 | generate_3d_structure | 结构与体系 | rdkit、openbabel | 从二维分子表示生成一个明确的三维结构。 |
| 6 | generate_conformer_ensemble | 结构与体系 | rdkit_etkdg、crest | 生成构象集合，不执行后续量子精修或最终排序。 |
| 7 | cluster_conformers | 结构与体系 | rdkit | 按指定重原子或全原子 RMSD 阈值对已有构象集合聚类。 |
| 8 | align_molecular_structures | 结构与体系 | rdkit | 根据明确的原子映射，将一个三维探针结构刚性对齐到参考结构。 |
| 9 | rank_conformers_from_results | 结构与体系 | internal_statistics | 根据已提供且对齐的能量或自由能，对构象进行排序和统计权重计算。 |
| 10 | repair_biomolecular_structure | 结构与体系 | pdbfixer | 修复生物分子中缺失的残基或原子，不自动选择质子化、力场或溶剂设置。 |
| 11 | select_structure_subset | 结构与体系 | pdb_tools | 从 PDB 中选择指定链或模型，并明确是否保留杂原子记录。 |
| 12 | renumber_biomolecular_structure | 结构与体系 | pdb_tools | 从指定起始值重新编号 PDB 原子序号和残基编号，不改变坐标与化学结构。 |
| 13 | normalize_pdb_records | 结构与体系 | pdb_tools | 按指定排序、链断裂和 hybrid-36 规则规范化 PDB 记录。 |
| 14 | assign_protonation_states | 结构与体系 | rdkit、pdbfixer | 使用指定后端及 pH 或规则设置分配质子化状态。 |
| 15 | assign_partial_charges | 结构与体系 | rdkit_gasteiger、openff_am1bcc | 分配指定类型的力场或对接部分电荷，不进行参数化或溶剂化。 |
| 16 | assign_force_field_parameters | 结构与体系 | openff、openmm_builder | 为已经准备好的分子体系分配明确选择的力场参数。 |
| 17 | solvate_molecular_system | 结构与体系 | openmm_builder、packmol | 构建指定的溶剂和离子环境，不执行能量最小化或动力学传播。 |
| 18 | analyze_crystal_symmetry | 结构与体系 | spglib、pymatgen | 分析周期结构的空间群及对称等价位点。 |
| 19 | standardize_crystal_structure | 结构与体系 | spglib、pymatgen | 将周期结构标准化为明确选择的原胞或常规晶胞表示。 |
| 20 | build_supercell | 结构与体系 | pymatgen | 对周期结构应用明确的整数超胞变换。 |
| 21 | enumerate_surface_slabs | 结构与体系 | pymatgen | 针对指定 Miller 指数、薄层厚度和真空层，枚举有限数量的对称不等价表面。 |
| 22 | calculate_molecular_descriptors | 化学信息学 | rdkit | 计算指定的图结构分子描述符，不生成坐标或运行电子结构计算。 |
| 23 | calculate_molecular_fingerprint | 化学信息学 | rdkit | 计算一种明确选择的分子指纹。 |
| 24 | calculate_molecular_similarity | 化学信息学 | rdkit | 使用指定指纹和相似度指标计算两个分子的相似度。 |
| 25 | search_local_substructures | 化学信息学 | rdkit | 在给定分子中查找明确 SMARTS 或 SMILES 查询对应的原子索引匹配。 |
| 26 | enumerate_tautomers | 化学信息学 | rdkit | 有界枚举互变异构体，不替智能体选择首选互变异构体。 |
| 27 | enumerate_stereoisomers | 化学信息学 | rdkit | 按指定唯一性和立体中心分配规则，有界枚举立体异构体。 |
| 28 | calculate_energy | 分子电子结构 | xtb、pyscf、psi4、tblite、gpaw、nwchem、openmolcas、mace、chgnet、deepmd、orca、gaussian、gamess、ase_emt | 使用智能体明确选择的软件和方法计算一个非周期体系的标量能量。 |
| 29 | calculate_forces | 分子电子结构 | xtb、pyscf、tblite、gpaw、nwchem、orca、mace、chgnet、deepmd、ase_emt | 计算一个非周期结构或对齐结构批次的原子力。 |
| 30 | calculate_hessian | 分子电子结构 | xtb、pyscf、psi4、tblite、nwchem、orca、gaussian、mace、chgnet、deepmd、ase_emt | 计算分子 Hessian，不自动推导振动模式、光谱或热化学量。 |
| 31 | optimize_geometry | 分子电子结构 | xtb、tblite、gpaw、mace、chgnet、deepmd、orca、gaussian、gamess、ase_emt、geometric、sella | 优化一个非周期体系的几何结构，并以优化后结构作为主要结果。 |
| 32 | calculate_dipole_moment | 分子电子结构 | xtb、tblite、pyscf、psi4、nwchem、openmolcas、orca、gaussian、gamess | 使用明确选择的电子结构方法计算分子偶极矩。 |
| 33 | calculate_atomic_charges | 分子电子结构 | xtb、pyscf、psi4、nwchem、openmolcas、multiwfn、orca | 使用电子结构布居分析计算原子电荷，不附加力场参数。 |
| 34 | calculate_orbitals | 分子电子结构 | pyscf、psi4、openmolcas、orca | 计算轨道能量、占据数及可选的轨道系数文件。 |
| 35 | calculate_bond_orders | 分子电子结构 | xtb、multiwfn、orca | 使用指定布居分析方法计算原子对之间的电子键级指标。 |
| 36 | calculate_excited_states | 分子电子结构 | pyscf、orca | 计算有限数量的垂直电子激发态，不生成展宽光谱或传播动力学。 |
| 37 | analyze_electron_density_topology | 分子电子结构 | critic2 | 在已有分子或周期电子密度场中定位和表征临界点。 |
| 38 | calculate_atomic_basin_properties | 分子电子结构 | critic2 | 使用指定分区算法，在标量场网格上积分原子或吸引子盆的布居、Laplacian 和体积性质。 |
| 39 | calculate_bader_charges | 分子电子结构 | critic2 | 从已有电子密度网格中，使用指定 Yu–Trinkle 或 Henkelman 分区计算 Bader 电荷。 |
| 40 | derive_vibrational_modes | 分子电子结构 | internal_vibrations | 根据已有 Hessian 和结构推导振动频率及简正模式。 |
| 41 | derive_ir_spectrum | 分子电子结构 | internal_spectroscopy | 根据已包含红外强度的振动结果构建 IR 光谱。 |
| 42 | derive_uv_vis_spectrum | 分子电子结构 | internal_spectroscopy | 根据跃迁能和振子强度构建确定性展宽的 UV/Vis 光谱。 |
| 43 | derive_thermochemistry | 分子电子结构 | internal_thermochemistry、goodvibes | 根据已有电子能和振动频率推导热化学量，不隐藏几何优化或 Hessian 计算。 |
| 44 | locate_transition_state | 反应与动力学 | pysisyphus、sella | 定位一个候选过渡态结构，不自动执行频率分析或 IRC。 |
| 45 | trace_intrinsic_reaction_coordinate | 反应与动力学 | pysisyphus | 从已有过渡态结构出发追踪内禀反应坐标。 |
| 46 | calculate_chemical_equilibrium | 反应与动力学 | cantera | 在明确给定的机理和热力学条件下计算平衡组成或状态。 |
| 47 | integrate_reaction_network | 反应与动力学 | scipy、cantera | 对明确指定的反应网络进行时间积分。 |
| 48 | calculate_rate_constants | 反应与动力学 | rmg | 在指定温度和压力点上计算 Arrhenius、多 Arrhenius、压强依赖 Arrhenius 或 Chebyshev 动力学模型的速率常数。 |
| 49 | calculate_tunneling_correction | 反应与动力学 | rmg | 在指定温度下计算 Wigner 或 Eckart 过渡态隧穿修正因子。 |
| 50 | solve_master_equation | 反应与动力学 | mess、mesmer | 求解给定的气相化学主方程模型并提取温压依赖的表观速率系数。 |
| 51 | solve_microkinetic_model | 反应与动力学 | catmap | 求解一个明确提供的微观动力学模型，不替智能体构建反应模型。 |
| 52 | minimize_system_energy | 分子动力学 | openmm、gromacs、lammps、hoomd、namd、amber_pmemd、charmm | 对已参数化体系进行能量最小化，不自动平衡或传播动力学。 |
| 53 | calculate_force_field_energy | 分子动力学 | openmm、hoomd | 在指定已有坐标或状态下计算已参数化体系的总势能。 |
| 54 | calculate_force_field_forces | 分子动力学 | openmm、hoomd | 在指定已有坐标或状态下计算已参数化体系的原子力场力。 |
| 55 | decompose_force_field_energy | 分子动力学 | openmm | 按 OpenMM 中明确存在的 Force 对象分解一次势能计算。 |
| 56 | propagate_dynamics | 分子动力学 | openmm、gromacs、lammps、hoomd、namd、amber_pmemd、charmm | 传播一个由智能体完整定义的动力学阶段，返回轨迹和最终状态。 |
| 57 | calculate_trajectory_rmsd | 分子动力学 | mdanalysis、mdtraj | 对指定轨迹原子组和参考结构计算 RMSD 时间序列。 |
| 58 | calculate_radius_of_gyration | 分子动力学 | mdanalysis、mdtraj | 计算指定原子组的回转半径时间序列。 |
| 59 | calculate_radial_distribution | 分子动力学 | mdanalysis | 计算两个指定原子组之间的径向分布函数。 |
| 60 | calculate_mean_squared_displacement | 分子动力学 | mdanalysis | 计算指定原子组的均方位移时间序列。 |
| 61 | calculate_contacts | 分子动力学 | mdtraj | 按明确的残基对和接触定义计算残基间接触距离。 |
| 62 | calculate_solvent_accessible_surface | 分子动力学 | mdtraj | 对已有轨迹计算逐原子或逐残基的溶剂可及表面积。 |
| 63 | calculate_dihedral_distribution | 分子动力学 | mdtraj、mdanalysis | 对明确给定的原子四元组计算二面角时间序列。 |
| 64 | calculate_hydrogen_bonds | 分子动力学 | mdanalysis | 使用明确的供体、氢、受体、距离和角度定义识别轨迹中的氢键事件。 |
| 65 | calculate_principal_components | 分子动力学 | mdanalysis | 对指定轨迹原子组计算坐标主成分及每帧投影。 |
| 66 | calculate_dynamic_cross_correlation | 分子动力学 | mdanalysis | 根据指定且可选对齐的轨迹坐标计算逐原子动态互相关矩阵。 |
| 67 | assign_secondary_structure | 分子动力学 | mdtraj | 为蛋白质轨迹每一帧分配逐残基二级结构标签。 |
| 68 | cluster_trajectory | 分子动力学 | mdtraj | 使用确定性的基于 RMSD 阈值的 leader 方法聚类指定轨迹帧。 |
| 69 | evaluate_collective_variables | 分子动力学 | plumed | 在已有轨迹上计算明确给定的集体变量。 |
| 70 | estimate_free_energy_difference | 分子动力学 | pymbar | 根据给定约化势矩阵和样本数估计无量纲两两自由能差。 |
| 71 | estimate_thermodynamic_expectations | 分子动力学 | pymbar | 根据样本和约化势矩阵估计各状态的可观测量期望值。 |
| 72 | calculate_potential_of_mean_force | 分子动力学 | pymbar | 根据已提供的不相关样本估计一维直方图自由能剖面，不替智能体选择分箱。 |
| 73 | analyze_free_energy_convergence | 分子动力学 | pymbar | 在指定样本比例上重复估计选定的两两自由能差，用于分析收敛性。 |
| 74 | parse_alchemical_energy_data | 分子动力学 | alchemlyb | 将指定模拟引擎输出文件解析为规范化的炼金约化势或导数数据表。 |
| 75 | calculate_periodic_energy | 周期体系与声子 | quantum_espresso、cp2k、siesta、dftbplus、abinit、vasp、gpaw、nequip、allegro、deepmd | 使用明确选择的电子结构后端计算周期体系能量。 |
| 76 | calculate_periodic_forces | 周期体系与声子 | quantum_espresso、cp2k、siesta、dftbplus、abinit、vasp、gpaw、nequip、allegro、deepmd | 计算一个周期结构或对齐位移结构批次的原子力。 |
| 77 | calculate_periodic_stress | 周期体系与声子 | quantum_espresso、cp2k、abinit、vasp、gpaw、nequip、allegro、deepmd | 计算周期体系应力张量，不进行结构弛豫。 |
| 78 | relax_periodic_structure | 周期体系与声子 | quantum_espresso、cp2k、siesta、dftbplus、abinit、vasp、gpaw、nequip、allegro、deepmd | 在明确的原子或晶胞约束下弛豫周期结构。 |
| 79 | calculate_electronic_band_structure | 周期体系与声子 | gpaw | 从已有收敛周期基态重启数据沿指定倒空间路径计算电子能带。 |
| 80 | calculate_density_of_states | 周期体系与声子 | gpaw | 从已有收敛周期基态重启数据在指定能量网格上计算总电子态密度。 |
| 81 | calculate_projected_density_of_states | 周期体系与声子 | gpaw、lobster | 从兼容的周期电子态数据计算或提取指定原子及轨道的投影态密度。 |
| 82 | analyze_periodic_bonding | 周期体系与声子 | lobster | 从已有 LOBSTER 输出提取指定的积分或能量分辨 COHP、COOP、COBI 成键信息。 |
| 83 | calculate_charge_spilling | 周期体系与声子 | lobster | 根据已有 lobsterout 和指定阈值评估波函数投影的电荷或总 spilling。 |
| 84 | generate_displaced_supercells | 周期体系与声子 | phonopy、phono3py | 根据指定超胞矩阵和位移幅度生成位移结构集合。 |
| 85 | assemble_force_constants | 周期体系与声子 | phonopy、phono3py | 根据给定位移集合和对齐的力数据组装力常数。 |
| 86 | calculate_phonon_dispersion | 周期体系与声子 | phonopy、phono3py | 根据已有力常数和指定 q 点路径计算声子色散。 |
| 87 | calculate_phonon_density_of_states | 周期体系与声子 | phonopy、phono3py | 根据已有力常数和指定 q 网格计算声子态密度。 |
| 88 | calculate_harmonic_thermodynamics | 周期体系与声子 | phonopy、phono3py | 在指定温度下计算谐振自由能、熵和定容热容。 |
| 89 | calculate_phonon_group_velocities | 周期体系与声子 | phonopy、phono3py | 沿指定 q 点路径计算逐声子模式的群速度向量。 |
| 90 | calculate_lattice_thermal_conductivity | 周期体系与声子 | phono3py、shengbte | 根据二阶、三阶力常数或完整 BTE 模型，在指定求解和散射设置下计算晶格热导率张量。 |
| 91 | dock_ligand | 分子对接 | vina、gnina | 在明确的搜索空间中，将已准备好的配体对接到已准备好的受体。 |
| 92 | search_compounds | 外部数据源 | pubchem | 根据明确的标识符和命名空间搜索 PubChem 化合物记录。 |
| 93 | resolve_chemical_identity | 外部数据源 | pubchem | 通过 PubChem 将一个明确化合物标识符解析为有界 ChemicalIdentity 记录。 |
| 94 | retrieve_compound_properties | 外部数据源 | pubchem | 从 PubChem 获取匹配化合物的指定且有界的性质集合。 |
| 95 | retrieve_compound_structure | 外部数据源 | pubchem | 从 PubChem 获取有界的二维或三维结构记录，由智能体指定维度和显式氢策略。 |
| 96 | search_similar_compounds | 外部数据源 | pubchem | 根据明确的结构标识符执行有界 PubChem 二维相似性搜索。 |
| 97 | search_substructures | 外部数据源 | pubchem | 根据明确的 SMILES、SMARTS、InChI 或 CID 执行有界 PubChem 子结构搜索。 |
| 98 | search_protein_structures | 外部数据源 | rcsb_pdb | 使用明确的结构 ID 或查询词搜索或获取 RCSB PDB 结构记录。 |
| 99 | search_materials | 外部数据源 | materials_project | 按材料 ID、化学式或明确查询字段搜索 Materials Project 记录。 |
| 100 | search_catalysis_records | 外部数据源 | catalysis_hub | 使用明确的反应物或产物过滤条件搜索 Catalysis-Hub 反应记录。 |
| 101 | lookup_nist_webbook_species | 外部数据源 | nist_webbook | 通过官方 CGI，按 CAS 号、精确名称或精确分子式查询有界的 NIST Chemistry WebBook 物种记录。 |
