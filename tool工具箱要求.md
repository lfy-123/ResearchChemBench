一、项目背景与目标

化学工具箱构建的最终目标是：

1. 尽可能安装所有能够在当前 Linux 环境中合法、自动、可复现安装的计算化学软件、化学工具和相关 Python 包。
2. 将这些软件整合到 ChemGraph 的工具体系中。
3. 通过统一、稳定的 MCP 接口供智能体调用。
4. 保留每个实际计算后端的身份，不能把后端选择隐藏起来。
5. 无法自动安装的软件不要阻塞整个任务，记录原因和人工操作步骤，留给用户后续处理。
6. 所有成功安装的软件都必须至少完成“可用性检测 + 版本检测 + 最小 smoke test”；仅仅执行了安装命令不算完成。
7. 所有完成代码集成的软件，都必须有 Schema、核心函数、MCP 包装、错误处理、测试和文档。

“安装完成”的判定标准是：软件安装在一个可复现的项目环境或容器中，能够被检测到版本，并成功运行一个最小示例。

“工具集成完成”的判定标准是：智能体可以通过 MCP 工具调用该软件，得到结构化结果或明确、结构化的失败信息。

二、需要处理的软件范围

请建立机器可读的工具注册表，例如：

config/toolbox_registry.yaml

每个条目至少记录：

- name
- category
- capabilities
- official_url
- license_class
- install_method
- pinned_version
- python_module
- executable
- environment_or_container
- adapter_module
- mcp_tools
- availability_check
- smoke_test
- status
- failure_reason
- manual_action

状态统一使用：

- planned
- installing
- installed
- verified
- integrated
- blocked_license
- blocked_credentials
- blocked_download
- failed_build
- unsupported_platform
- manual_required

需要优先尝试自动安装和集成的软件如下。

A. 数据、结构与互操作

- RDKit
- Open Babel
- ASE
- QCSchema
- QCElemental
- QCEngine
- cclib
- pymatgen
- spglib
- OpenFF Toolkit
- OpenFF Interchange
- Packmol
- MDAnalysis
- ParmEd
- MDTraj
- AiiDA
- jobflow
- atomate2

B. 构象、分子量子化学与热化学

- tblite
- xTB
- CREST
- CENSO
- Psi4
- PySCF
- NWChem
- GoodVibes
- autodE
- pysisyphus
- geomeTRIC
- Sella
- Critic2
- Multiwfn：先核查官方下载和再分发限制；不确定时转 manual_required
- GAMESS：如果需要注册或人工许可，转 manual_required

保留并验证 ChemGraph 现有的：

- EMT
- TBLite/GFN1-xTB/GFN2-xTB
- ORCA adapter
- NWChem
- MACE
- FAIRChem
- AIMNet2

C. 周期体系、材料、表面、声子与输运

- Quantum ESPRESSO
- CP2K
- GPAW
- DFTB+
- SIESTA
- ABINIT
- Phonopy
- phono3py
- Wannier90
- Yambo
- ShengBTE
- CatMAP

D. 分子动力学和自由能

- GROMACS
- OpenMM
- LAMMPS
- PLUMED
- HOOMD-blue
- pymbar
- alchemlyb
- MDAnalysis
- MDTraj
- ParmEd
- Packmol
- OpenFF Toolkit/Interchange

E. 反应网络与动力学

- RMG-Py
- Arkane
- Cantera
- AutoMeKin
- KinBot
- MESMER
- MESS：先核查获取和许可条件
- CatMAP
- 通用微观动力学求解模块

F. 激发态、光谱和非绝热动力学

- OpenMolcas
- TheoDORE
- SHARC
- Newton-X
- 能够合法安装时再处理相关光谱分析工具

G. 对接和结构生物信息学

- AutoDock Vina
- GNINA
- PDBFixer
- pdb-tools

H. 机器学习原子势

- MACE
- NequIP
- DeePMD-kit
- CHGNet
- FAIRChem/UMA
- AIMNet2

I. 外部科学数据服务

- PubChem PUG-REST
- RCSB PDB API
- Materials Project API
- Catalysis-Hub
- NIST CCCBDB/Chemistry WebBook：仅在存在稳定、允许使用的程序化接口时接入，不要通过脆弱或违反条款的网页抓取实现

J. ChemGraph 已有专业工具

检查并保留现有的：

- gRASPA
- FDMNES/XANES
- Parsl/HPC 工具
- data_analysis_mcp.py

以下软件不要尝试未经授权的自动下载。为它们建立 adapter、可用性检测、安装说明和挂载接口即可：

- ORCA
- Gaussian
- VASP
- Q-Chem
- Molpro
- TURBOMOLE
- AMBER 正式版
- CHARMM
- AMS/ADF
- CASTEP
- CRYSTAL
- WIEN2k
- Schrödinger
- OpenEye
- EasySpin/Matlab
- LOBSTER
- 其他需要账号、许可证或人工同意条款的软件

对于这些软件，统一通过环境变量指定，例如：

- CHEMGRAPH_ORCA_COMMAND
- CHEMGRAPH_VASP_COMMAND
- CHEMGRAPH_GAUSSIAN_COMMAND
- CHEMGRAPH_QCHEM_COMMAND
- CHEMGRAPH_MOLPRO_COMMAND
- CHEMGRAPH_LICENSE_DIR

如果软件不可用，返回结构化的 unavailable 状态和人工操作说明，不能在模块导入阶段直接崩溃。



三、ASE 后端

能够自然作为 ASE calculator 工作的软件，优先按照现有方式扩展。

但是不要把所有软件都伪装成 ASE calculator。

适合能量、力、优化、振动等 calculator 语义的软件可以接入 run_ase；构象搜索、MD 工作流、声子、对接、反应网络和动力学等应建立独立工具。

四、首批统一 MCP 工具（这个工具名称只是举例）

至少实现或注册以下逻辑工具。一个逻辑工具可以支持多个显式 backend：

1. query_pubchem
2. query_rcsb_pdb
3. query_materials_project
4. query_catalysis_hub
5. list_toolbox_capabilities
6. check_backend_availability
7. standardize_molecule
8. convert_structure
9. generate_3d_structure
10. generate_conformers_rdkit
11. generate_conformers_crest
12. refine_ensemble_censo
13. run_xtb
14. run_ase
15. run_orca
16. run_psi4
17. run_pyscf
18. analyze_wavefunction
19. find_transition_state
20. run_irc
21. compute_thermochemistry
22. run_quantum_espresso
23. run_cp2k
24. run_periodic_calculation
25. run_catmap
26. prepare_md_system
27. run_gromacs
28. run_openmm
29. run_lammps
30. run_plumed
31. analyze_md_trajectory
32. run_phonopy
33. run_reaction_kinetics
34. run_cantera
35. run_docking
36. run_mlip
37. validate_computation
38. extract_output_json
