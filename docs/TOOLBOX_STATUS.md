# ResearchChemBench 工具箱状态报告

> 历史说明：本文件是 2026-07-17 对单一 `.toolbox_env` 的验证快照。当前运行架构已改为
> 依赖隔离的多 MCP profile；请以 [MCP_PROFILE_STATUS.md](MCP_PROFILE_STATUS.md) 为当前
> 安装状态。本文件保留用于追踪改造前后的差异。

- 生成时间：2026-07-17T16:00:10.353332+00:00
- Python：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.toolbox_env/bin/python`
- 验证 workspace：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/workspaces/toolbox_verification/20260717_155950`
- MCP 工具数：41
- 正常工作：26
- 未配置/未完成真实 smoke：15
- 未正常工作：0

## MCP 工具状态

| Tool | Category | Backend | Status | Detail |
|---|---|---|---|---|
| analyze_md_trajectory | molecular_dynamics | MDAnalysis | 正常工作 | Minimal functional smoke test succeeded |
| analyze_wavefunction | wavefunction_analysis | cclib | 正常工作 | Minimal functional smoke test succeeded |
| calculator | utility | NumExpr | 正常工作 | Minimal functional smoke test succeeded |
| check_backend_availability | toolbox_management | ResearchChemBench registry/runtime probe | 正常工作 | Minimal functional smoke test succeeded |
| compute_thermochemistry | thermochemistry | GoodVibes | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| convert_structure | data_structure | ASE | 正常工作 | Minimal functional smoke test succeeded |
| extract_output_json | result_io | ChemGraph | 正常工作 | Minimal functional smoke test succeeded |
| find_transition_state | reaction_path | pysisyphus | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| generate_3d_structure | cheminformatics | RDKit | 正常工作 | Minimal functional smoke test succeeded |
| generate_conformers_crest | conformer_search | CREST/xTB | 正常工作 | Minimal functional smoke test succeeded |
| generate_conformers_rdkit | conformer_search | RDKit ETKDG/MMFF | 正常工作 | Minimal functional smoke test succeeded |
| list_toolbox_capabilities | toolbox_management | ResearchChemBench registry | 正常工作 | Minimal functional smoke test succeeded |
| molecule_name_to_smiles | cheminformatics | ChemGraph/PubChem | 正常工作 | Minimal functional smoke test succeeded |
| prepare_md_system | molecular_dynamics | PDBFixer/OpenMM | 正常工作 | Minimal functional smoke test succeeded |
| query_catalysis_hub | external_data | Catalysis-Hub GraphQL API | 正常工作 | Minimal functional smoke test succeeded |
| query_materials_project | external_data | Materials Project mp-api | 未配置/未完成真实 smoke | MP_API_KEY is not configured |
| query_pubchem | external_data | PubChem PUG-REST via PubChemPy | 正常工作 | Minimal functional smoke test succeeded |
| query_rcsb_pdb | external_data | RCSB PDB Data API | 正常工作 | Minimal functional smoke test succeeded |
| refine_ensemble_censo | conformer_search | CENSO | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| run_ase | simulation | ChemGraph/ASE | 正常工作 | Minimal functional smoke test succeeded |
| run_cantera | reaction_kinetics | Cantera | 正常工作 | Minimal functional smoke test succeeded |
| run_catmap | catalysis | CatMAP | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| run_cp2k | periodic_dft | CP2K | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| run_docking | docking | AutoDock Vina/GNINA | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| run_gromacs | molecular_dynamics | GROMACS | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| run_irc | reaction_path | pysisyphus | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| run_lammps | molecular_dynamics | LAMMPS | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| run_mlip | mlip | MACE/CHGNet | 正常工作 | Minimal functional smoke test succeeded |
| run_openmm | molecular_dynamics | OpenMM | 正常工作 | Minimal functional smoke test succeeded |
| run_orca | quantum_chemistry | ORCA | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| run_periodic_calculation | periodic_dft | QE/CP2K/DFTB+/SIESTA/ABINIT | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| run_phonopy | phonons | Phonopy/Phono3py | 正常工作 | Minimal functional smoke test succeeded |
| run_plumed | enhanced_sampling | PLUMED | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| run_psi4 | quantum_chemistry | Psi4 | 未配置/未完成真实 smoke | psi4 is not installed |
| run_pyscf | quantum_chemistry | PySCF | 正常工作 | Minimal functional smoke test succeeded |
| run_quantum_espresso | periodic_dft | Quantum ESPRESSO pw.x | 未配置/未完成真实 smoke | Adapter is registered, but no safe automated real smoke input is defined |
| run_reaction_kinetics | reaction_kinetics | SciPy solve_ivp | 正常工作 | Minimal functional smoke test succeeded |
| run_xtb | quantum_chemistry | xTB | 正常工作 | Minimal functional smoke test succeeded |
| smiles_to_coordinate_file | cheminformatics | ChemGraph/RDKit/ASE | 正常工作 | Minimal functional smoke test succeeded |
| standardize_molecule | cheminformatics | RDKit | 正常工作 | Minimal functional smoke test succeeded |
| validate_computation | validation | ResearchChemBench deterministic validator | 正常工作 | Minimal functional smoke test succeeded |

## 软件/服务状态

状态统计：`blocked_credentials`=1, `blocked_license`=13, `installed`=34, `integrated`=3, `manual_required`=10, `planned`=38

| Software | Category | Status | Module/Executable | Detail | Manual action |
|---|---|---|---|---|---|
| RDKit | data_structure | installed | rdkit | Runtime dependency detected |  |
| Open Babel | data_structure | installed | openbabel | Runtime dependency detected |  |
| ASE | data_structure | installed | ase | Runtime dependency detected |  |
| QCSchema | data_structure | installed | qcelemental | Runtime dependency detected |  |
| QCElemental | data_structure | installed | qcelemental | Runtime dependency detected |  |
| QCEngine | quantum_chemistry | installed | qcengine | Runtime dependency detected |  |
| cclib | analysis | installed | cclib | Runtime dependency detected |  |
| pymatgen | materials | installed | pymatgen | Runtime dependency detected |  |
| spglib | materials | installed | spglib | Runtime dependency detected |  |
| OpenFF Toolkit | molecular_simulation | installed | openff.toolkit | Runtime dependency detected |  |
| OpenFF Interchange | molecular_simulation | installed | openff.interchange | Runtime dependency detected |  |
| Packmol | molecular_simulation | installed | packmol | Runtime dependency detected |  |
| MDAnalysis | molecular_dynamics | installed | MDAnalysis | Runtime dependency detected |  |
| ParmEd | molecular_dynamics | installed | parmed | Runtime dependency detected |  |
| MDTraj | molecular_dynamics | installed | mdtraj | Runtime dependency detected |  |
| AiiDA | workflow | planned | aiida | Install the backend in .toolbox_env. |  |
| jobflow | workflow | planned | jobflow | Install the backend in .toolbox_env. |  |
| atomate2 | workflow | planned | atomate2 | Install the backend in .toolbox_env. |  |
| EMT | atomistic_calculator | installed | ase.calculators.emt | Runtime dependency detected |  |
| TBLite | quantum_chemistry | installed | tblite | Runtime dependency detected |  |
| xTB | quantum_chemistry | installed | xtb | Runtime dependency detected |  |
| CREST | conformer_search | installed | crest | Runtime dependency detected |  |
| CENSO | conformer_search | planned | censo | Install the backend in .toolbox_env. |  |
| Psi4 | quantum_chemistry | planned | psi4 | Install Psi4 in a dedicated compatible environment, then expose its Python module or executable. | Install Psi4 in a dedicated compatible environment, then expose its Python module or executable. |
| PySCF | quantum_chemistry | installed | pyscf | Runtime dependency detected |  |
| NWChem | quantum_chemistry | planned | nwchem | Install NWChem in a dedicated environment and add its executable to PATH. | Install NWChem in a dedicated environment and add its executable to PATH. |
| GoodVibes | thermochemistry | planned | goodvibes | Install the backend in .toolbox_env. |  |
| autodE | reaction_path | planned | autode | Install the backend in .toolbox_env. |  |
| pysisyphus | reaction_path | planned | pysisyphus | Install the backend in .toolbox_env. |  |
| geomeTRIC | optimization | installed | geometric | Runtime dependency detected |  |
| Sella | reaction_path | installed | sella | Runtime dependency detected |  |
| Critic2 | wavefunction_analysis | planned | critic2 | Install the backend in .toolbox_env. |  |
| Multiwfn | wavefunction_analysis | manual_required | Multiwfn | Redistribution and download terms require manual review. | Download from the official site after reviewing its terms, then set CHEMGRAPH_MULTIWFN_COMMAND. |
| GAMESS | quantum_chemistry | manual_required | remote/manual | Registration and acceptance of distribution terms are required. | Obtain GAMESS manually and configure its launcher outside the repository. |
| Quantum ESPRESSO | periodic_dft | planned | pw.x | Install Quantum ESPRESSO in a dedicated environment and add pw.x to PATH. | Install Quantum ESPRESSO in a dedicated environment and add pw.x to PATH. |
| CP2K | periodic_dft | planned | cp2k | Install CP2K in a dedicated environment and add cp2k to PATH. | Install CP2K in a dedicated environment and add cp2k to PATH. |
| GPAW | periodic_dft | planned | gpaw | Install the backend in .toolbox_env. |  |
| DFTB+ | periodic_dft | planned | dftb+ | Install DFTB+ in a dedicated environment and add dftb+ to PATH. | Install DFTB+ in a dedicated environment and add dftb+ to PATH. |
| SIESTA | periodic_dft | planned | siesta | Install the backend in .toolbox_env. |  |
| ABINIT | periodic_dft | planned | abinit | Install the backend in .toolbox_env. |  |
| Phonopy | phonons | installed | phonopy | Runtime dependency detected |  |
| phono3py | phonons | installed | phono3py | Runtime dependency detected |  |
| Wannier90 | electronic_transport | planned | wannier90.x | Install the backend in .toolbox_env. |  |
| Yambo | excited_state | planned | yambo | Install the backend in .toolbox_env. |  |
| ShengBTE | thermal_transport | planned | ShengBTE | Install the backend in .toolbox_env. |  |
| CatMAP | catalysis | planned | catmap | Install the backend in .toolbox_env. |  |
| GROMACS | molecular_dynamics | planned | gmx | Install GROMACS in a dedicated environment and add gmx to PATH. | Install GROMACS in a dedicated environment and add gmx to PATH. |
| OpenMM | molecular_dynamics | installed | openmm | Runtime dependency detected |  |
| LAMMPS | molecular_dynamics | planned | lammps | Install LAMMPS in a dedicated environment and add lmp to PATH. | Install LAMMPS in a dedicated environment and add lmp to PATH. |
| PLUMED | enhanced_sampling | planned | plumed | Install PLUMED in a dedicated environment and add plumed to PATH. | Install PLUMED in a dedicated environment and add plumed to PATH. |
| HOOMD-blue | molecular_dynamics | planned | hoomd | Install the backend in .toolbox_env. |  |
| pymbar | free_energy | installed | pymbar | Runtime dependency detected |  |
| alchemlyb | free_energy | installed | alchemlyb | Runtime dependency detected |  |
| RMG-Py | reaction_kinetics | planned | rmgpy | Install the backend in .toolbox_env. |  |
| Arkane | reaction_kinetics | planned | arkane | Install the backend in .toolbox_env. |  |
| Cantera | reaction_kinetics | installed | cantera | Runtime dependency detected |  |
| AutoMeKin | reaction_network | planned | amk | Install the backend in .toolbox_env. |  |
| KinBot | reaction_network | planned | kinbot | Install the backend in .toolbox_env. |  |
| MESMER | reaction_kinetics | planned | mesmer | Install the backend in .toolbox_env. |  |
| MESS | reaction_kinetics | manual_required | remote/manual | Distribution and use conditions require manual review. | Obtain MESS from its official distributor and configure it outside this repository. |
| OpenMolcas | excited_state | planned | pymolcas | Install the backend in .toolbox_env. |  |
| TheoDORE | excited_state | planned | theodore | Install the backend in .toolbox_env. |  |
| SHARC | nonadiabatic_dynamics | manual_required | remote/manual | Register and install SHARC according to the official instructions. | Register and install SHARC according to the official instructions. |
| Newton-X | nonadiabatic_dynamics | manual_required | remote/manual | Install Newton-X from its official distribution and configure its launcher before adding a production adapter. | Install Newton-X from its official distribution and configure its launcher before adding a production adapter. |
| AutoDock Vina | docking | installed | vina | Runtime dependency detected |  |
| GNINA | docking | planned | gnina | Install the backend in .toolbox_env. |  |
| PDBFixer | structural_bioinformatics | installed | pdbfixer | Runtime dependency detected |  |
| pdb-tools | structural_bioinformatics | installed | pdbtools | Runtime dependency detected |  |
| MACE | mlip | installed | mace | Runtime dependency detected |  |
| NequIP | mlip | planned | nequip | Install the backend in .toolbox_env. |  |
| DeePMD-kit | mlip | planned | deepmd | Install the backend in .toolbox_env. |  |
| CHGNet | mlip | installed | chgnet | Runtime dependency detected |  |
| FAIRChem/UMA | mlip | planned | fairchem | Install the backend in .toolbox_env. |  |
| AIMNet2 | mlip | planned | aimnet2calc | Install the backend in .toolbox_env. |  |
| PubChem PUG-REST | external_data | integrated | pubchempy | Remote API adapter is present; live status is reported by the corresponding MCP tool. |  |
| RCSB PDB API | external_data | integrated | remote/manual | Remote API adapter is present; live status is reported by the corresponding MCP tool. |  |
| Materials Project API | external_data | blocked_credentials | mp_api | The API client/key combination is not configured in the current environment. | Set MP_API_KEY with a Materials Project API key. |
| Catalysis-Hub | external_data | integrated | remote/manual | Remote API adapter is present; live status is reported by the corresponding MCP tool. |  |
| NIST Chemistry WebBook/CCCBDB | external_data | manual_required | remote/manual | No stable general-purpose API was selected; fragile scraping is intentionally excluded. | Integrate only a documented programmatic interface whose terms permit automated use. |
| gRASPA | adsorption | planned | graspa | Install the backend in .toolbox_env. |  |
| FDMNES/XANES | spectroscopy | manual_required | fdmnes | manual_required |  |
| Parsl | workflow | planned | parsl | Install the backend in .toolbox_env. |  |
| ChemGraph data_analysis_mcp | analysis | installed | chemgraph | Runtime dependency detected |  |
| ORCA | licensed_quantum_chemistry | manual_required | orca | Install ORCA manually and set CHEMGRAPH_ORCA_COMMAND. | Install ORCA manually and set CHEMGRAPH_ORCA_COMMAND. |
| Gaussian | licensed_quantum_chemistry | blocked_license | remote/manual | Mount a licensed installation and set CHEMGRAPH_GAUSSIAN_COMMAND. | Mount a licensed installation and set CHEMGRAPH_GAUSSIAN_COMMAND. |
| VASP | licensed_periodic_dft | blocked_license | remote/manual | Mount a licensed installation and set CHEMGRAPH_VASP_COMMAND. | Mount a licensed installation and set CHEMGRAPH_VASP_COMMAND. |
| Q-Chem | licensed_quantum_chemistry | blocked_license | remote/manual | Mount a licensed installation and set CHEMGRAPH_QCHEM_COMMAND. | Mount a licensed installation and set CHEMGRAPH_QCHEM_COMMAND. |
| Molpro | licensed_quantum_chemistry | blocked_license | remote/manual | Mount a licensed installation and set CHEMGRAPH_MOLPRO_COMMAND. | Mount a licensed installation and set CHEMGRAPH_MOLPRO_COMMAND. |
| TURBOMOLE | licensed_quantum_chemistry | blocked_license | remote/manual | blocked_license |  |
| AMBER | licensed_molecular_dynamics | manual_required | remote/manual | manual_required |  |
| CHARMM | licensed_molecular_dynamics | blocked_license | remote/manual | blocked_license |  |
| AMS/ADF | licensed_quantum_chemistry | blocked_license | remote/manual | blocked_license |  |
| CASTEP | licensed_periodic_dft | blocked_license | remote/manual | blocked_license |  |
| CRYSTAL | licensed_periodic_dft | blocked_license | remote/manual | blocked_license |  |
| WIEN2k | licensed_periodic_dft | blocked_license | remote/manual | blocked_license |  |
| Schrodinger | licensed_cheminformatics | blocked_license | remote/manual | blocked_license |  |
| OpenEye | licensed_cheminformatics | blocked_license | remote/manual | blocked_license |  |
| EasySpin/Matlab | licensed_spectroscopy | blocked_license | remote/manual | blocked_license |  |
| LOBSTER | licensed_bonding_analysis | manual_required | remote/manual | manual_required |  |

## 判定说明

- `正常工作`：实际执行了最小功能输入并得到结构化成功结果。
- `未配置/未完成真实 smoke`：wrapper 已注册，但缺少程序、凭据、模型、许可证，或尚无安全的自动 smoke 输入。
- `未正常工作`：后端存在或工具被调用，但最小测试抛出异常或返回错误。
- 软件表中的 `installed` 只表示检测到模块/可执行文件；是否完成计算以 MCP 工具表的真实 smoke 为准。
