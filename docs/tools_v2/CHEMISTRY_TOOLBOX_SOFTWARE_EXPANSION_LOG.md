# Chemistry Toolbox Software Expansion Log

更新时间：2026-08-06

## 执行规则

- 软件按推荐顺序逐个处理；每项必须依次完成许可核对、固定版本下载、runtime 配置、原子 Action、单元测试和最小科学 smoke，之后才进入下一项。
- `.software_cache` 只保存本机软件源码、二进制和 smoke 证据，不进入 Git。可迁移的依赖声明、配置、Action 和测试进入仓库。
- 免费不等于允许再分发。需要申请、没有明确许可证或限制再分发的软件只记录状态，不绕过条款下载。
- Action 只封装边界清楚、参数显式、结果可评分的原子操作，不提供任意 shell runner 或完整论文路线。

## 官方来源与实施范围

| 软件 | 官方来源 | 许可核对 | 本轮处理 |
|---|---|---|---|
| AIRSS | [安装](https://airss-docs.github.io/getting-started/installation/)、[conda-forge](https://anaconda.org/conda-forge/airss) | GPL-2.0 | 安装与适配 |
| TDEP | [仓库](https://github.com/tdep-developers/tdep)、[安装](https://github.com/tdep-developers/tdep/blob/main/INSTALL.md) | MIT | 安装与适配 |
| ACPYPE | [仓库](https://github.com/alanwilter/acpype) | GPL-3.0-or-later | 安装与适配 |
| pmx | [仓库](https://github.com/deGrootLab/pmx)、[文档](https://degrootlab.github.io/pmx/) | 以下载版本 LICENSE 为准 | 安装与适配 |
| gmx_MMPBSA | [仓库](https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA)、[文档](https://valdes-tresanco-ms.github.io/gmx_MMPBSA/) | GPL-3.0 | 安装与适配 |
| SISSO | [仓库与用法](https://github.com/rouyang2017/SISSO) | Apache-2.0 | 安装与适配 |
| gplearn | [文档](https://gplearn.readthedocs.io/)、[仓库](https://github.com/trevorstephens/gplearn) | BSD-3-Clause | 安装与适配 |
| MultiWell | [官方分发页](https://multiwell.engin.umich.edu/downloads/) | 网页未明确列出许可证 | 下载前检查分发包条款 |
| VASPKIT | [安装与使用协议](https://vaspkit.com/installation.html) | 免费、限制用途的专有二进制 | 按条款评估本地安装，不进入 Git |
| PyFrag 2019 | [安装](https://pyfragdocument.readthedocs.io/en/latest/install.html) | 以源码仓库许可证为准 | 先核对再决定 |
| Progdyn | [公开仓库](https://github.com/DanielSingleton/Progdyn) | 未发现明确许可证 | 不下载、不适配，等待作者授权 |
| BAGEL | [仓库](https://github.com/qsimulate-open/bagel) | GPL-3.0-or-later | 评估构建并适配 |

CALYPSO、USPEX、CFOUR 和 FHI-aims 需要注册或签署许可，本轮不自动下载；NBO、AMS/ADF、TURBOMOLE、Q-Chem、TeraChem 和 COSMOtherm 为收费软件，本轮不添加。

## 逐项安装记录

### AIRSS

状态：通过，2026-08-05 完成。

- 固定版本：AIRSS 0.9.3，conda-forge 构建 `h8876d29_2`；默认命令名包构建 `ha770c72_2`。
- 缓存位置：`.software_cache/airss/0.9.3`，约 55 MB，不进入 Git。
- 下载包 SHA-256：`airss-0.9.3-h8876d29_2.conda` 为 `5b34b5c06d6f7bf130628119b8e5e9141f89c5ff651a70815187bc66178c312c`；`airss-with-default-names-0.9.3-ha770c72_2.conda` 为 `7ba0a9f0520417346b5f75087d94ea7f4d74be75cf303e63685eaaed41143081`。
- 运行依赖：AIRSS 包内补入 `libgfortran5 15.2.0`、`liblapack 3.11.0` 和 `libopenblas 0.3.33`，运行时只需把 `.software_cache/airss/0.9.3/lib` 加入 `LD_LIBRARY_PATH`；`ldd` 无缺失项。
- 配置：新增 `airss` runtime、requested-software 项、native guide/manual/example contract，并在 `general-modern-openmpi5/environment.yml` 声明 `airss-with-default-names=0.9.3`。
- 新增 Action：`generate_crystal_structure_candidates`（只生成、不松弛、不排序）和 `convert_crystal_structure_format`（显式 `cabal` 输入/输出格式）。
- 测试：`airss_version`、`buildcell --help`、官方 8 原子 Al `buildcell` 示例、`cell -> xyz` 转换、两个 Action 单测、Action Catalog handler 一致性以及统一 `execute_action` 一候选调用均通过。Action 定向测试结果为 `3 passed`。
- 测试输入：`chemistry_toolbox/examples/integration/airss/al8_seed.cell`；测试代码：`chemistry_toolbox/tests/test_airss_actions.py`。

### TDEP

状态：通过，2026-08-05 完成。

- 固定版本：TDEP `25.03`，官方 tag 对应 commit `d38f435d75f33e0e86629ce7b7059ce95fbc06c5`，MIT 许可证。
- 缓存位置：`.software_cache/tdep/25.03/source`，包含固定版本源码和本机编译产物，约 1.4 GB，不进入 Git。
- 构建依赖：MPICH 4、GNU Fortran、HDF5 Fortran、FFTW、OpenBLAS/LAPACK 和 h5py；依赖已写入 `reaction-kinetics/environment.yml`，runtime 使用 `.envs/kinetics-legacy`。
- 构建约束：该版本使用 `-O2` 时，`extract_forceconstants` 会在官方 Si fixture 的 prototype-tuplet 阶段段错误；按官方编译模板改用 `-O0` 全量重编译后，二阶/三阶及 polar 官方 fixture 均通过。因此可迁移构建必须保留 `-O0`，不能自行恢复优化级别。
- 动态链接：`extract_forceconstants`、`canonical_configuration` 和 `phonon_dispersion_relations` 在配置的 `LD_LIBRARY_PATH` 下均无缺失动态库。
- 配置：新增 `tdep` runtime、requested-software 项、native guide/manual/example contract，并生成本地原生手册。
- 新增 Action：`fit_effective_force_constants`、`generate_thermal_displacement_configurations` 和 `calculate_temperature_dependent_phonon_dispersion`。截断半径、对称性约束、polar 处理、统计系综、初始化来源、单位和路径均为显式参数。
- 软件测试：官方 `generate_structure` fixture 为 `1 passed`；官方 `canonical_configuration --modes` fixture 为 `1 passed`，并额外完成 400 K Debye 初始化的两构型真实生成；官方 polar 二阶/三阶 `extract_forceconstants` fixture 为 `2 passed`；官方 `phonon_dispersion_relations` fixture 为 `1 passed`。
- Action 测试：TDEP 三个 Action、AIRSS 回归和 handler 一致性合计 `6 passed`；统一 `execute_action` 调用真实生成一份热位移构型成功，版本返回 `25.03-d38f435`。
- 测试代码：`chemistry_toolbox/tests/test_tdep_actions.py`。

### ACPYPE

状态：通过，2026-08-05 完成。

- 固定版本：ACPYPE `2023.10.27`，官方 tag commit `8dbc6e8caabab3036696f8da6d1cd166170fdfac`，GPL-3.0-or-later。
- 缓存位置：`.software_cache/acpype/2023.10.27`，约 1.1 GB，包含官方源码、PyPI wheel 和 Open Babel 私有依赖前缀，不进入 Git。wheel SHA-256 为 `58690dac7ba83961ab84ca995b712d55ec799bab0e4bd4d4dac794e306acee9b`。
- 运行依赖：AmberTools 26、Open Babel 3.1.1、GROMACS 2025.4。首次 PDB smoke 明确报 `Missing OBABEL`，说明原环境缺少 Open Babel；已把 `openbabel=3.1.1` 和 `acpype==2023.10.27` 写入并安装到 `molecular-simulation-openff` runtime。
- 测试策略：官方 `FFF.pdb` 的 63 原子 AM1-BCC/SQM 任务单核耗时过长，不作为持续 smoke；改用官方 `benzene.mdl`、显式 gas charge、GAFF2 执行短而完整的参数化。AM1-BCC 仍为 Action 的显式能力，生产任务应单独给足 walltime。
- 软件测试：苯的 Antechamber、Parmchk、TLeap、Open Babel 与 ACPYPE 拓扑输出均通过；生成的 GROMACS `.top/.gro` 由 `gmx grompp -maxwarn 0` 成功预处理；同一 AMBER `prmtop/inpcrd` 的 `amb2gmx` 转换也通过。
- 新增 Action：`generate_small_molecule_topology` 和 `convert_amber_topology_to_gromacs`。前者要求显式 atom type、charge method、净电荷、自旋多重度、charge program、输出拓扑族和 charge walltime；后者只转换现有匹配文件，不重算电荷或参数。
- 配置：新增 `acpype` runtime、requested-software 项、native guide/manual/example contract，并生成原生手册；runtime 探针确认 `acpype`、`obabel`、`antechamber` 以及 `acpype/openbabel` Python 模块均可用。
- Action 测试：两个真实 Action、统一 `execute_action` 调度、GROMACS 验证及 handler 一致性合计 `7 passed`。测试代码：`chemistry_toolbox/tests/test_acpype_actions.py`。

### pmx

状态：通过，2026-08-05 完成。

- 固定版本：官方 Python 3 `develop` 分支 commit `0dd5f0a9cdf26109eff98bdfeb4ac4e55353aa76`，运行版本串 `0+untagged.1.g0dd5f0a`，LGPL-3.0-only。
- 风险边界：官方文档明确说明 Python 3 development version 尚不稳定；仓库只有旧 Python 2 稳定线。因此本工具箱固定 commit，不追踪 branch HEAD，并在 requested-software、backend spec 和原生手册中标明开发版风险。
- 缓存位置：`.software_cache/pmx`，约 828 MB，含固定源码、上游测试/基准和 CPython 3.12 Linux wheel。wheel SHA-256 为 `7dd1aee7e675be0e9d6a2379f933f5259b376e80fac5b88c15e045a02c7d59a4`；不同 Python ABI 或平台必须从固定源码重编译。
- 依赖修补：首次 `pmx atomMapping` 报缺少 RDKit，已安装并声明 RDKit 与 `future`；首次独立 `pmx gentop` 报 mutation forcefield path 不存在，已把 `GMXLIB` 显式配置为该 runtime 内的 `pmx/data/mutff`。
- 新增 Action：`mutate_biomolecular_residues_for_alchemy`、`generate_alchemical_hybrid_topology` 和 `map_alchemical_ligand_atoms`。突变记录、链/残基编号策略、force field、递归与 split 策略、dummy scaling、MCS/alignment、氢/环/手性过滤、距离阈值与 MCS timeout 均显式。
- 软件测试：上游 `test_alchemy.py` 和 import fixture 为 `3 passed`；官方 W2F topology fixture 成功生成含 B-state 的 hybrid topology；官方 PTP1B benchmark 配体 `23466 -> 23467` 映射得到 27 对原子及 dissimilarity `0.1818`。
- Action 测试：pmx 三个真实 Action、统一 `execute_action`、ACPYPE 回归和 handler 一致性合计 `11 passed`；runtime 探针确认 pmx、RDKit、命令入口、`CHEMGRAPH_PMX_COMMAND` 与 `GMXLIB` 全部可用。测试代码：`chemistry_toolbox/tests/test_pmx_actions.py`。
- 配置：更新 molecular-simulation-openff YAML，并新增 pmx runtime、requested-software、native guide/manual/example contract 和生成手册。

### gmx_MMPBSA

状态：通过，2026-08-05 完成。

- 固定版本：PyPI `gmx_MMPBSA 1.6.5`，GPL-3.0；wheel SHA-256 为 `9a21be091d8dade8862cd957c51e97c0d72fedd7927bb63105234e13ba257cfc`。
- 缓存位置：`.software_cache/gmx_mmpbsa/1.6.5`，约 5.6 GB，包含固定 wheel、隔离 runtime 和官方 smoke 示例，不进入 Git。
- 隔离原因：该版本要求 Python 3.11 和 AmberTools `<24`，不能装入现有 Python 3.12 / AmberTools 26 的 `molecular-simulation-openff` 环境。当前使用 `environment/merged/gmx-mmpbsa` 和 `.envs/gmx-mmpbsa`，固定 Python 3.11、AmberTools 23.6、GROMACS 2025.4、mpi4py 4.0.1、NumPy 1.26.4、pandas 1.5.3、Matplotlib 3.7.3、Seaborn 0.11.2、SciPy 1.14.1 和 ParmEd 4.3.1。
- benchmark worker 修补：首次统一调度失败是隔离环境缺少 `pydantic/PyYAML/python-dotenv`，已安装并写入可迁移 YAML；容器 root 下 OpenMPI 还需显式设置 `OMPI_ALLOW_RUN_AS_ROOT=1` 和 `OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1`，`AMBERHOME` 固定指向隔离前缀。
- 新增 Action：`calculate_end_state_binding_free_energy`、`calculate_end_state_energy_decomposition` 和 `summarize_end_state_free_energy_results`。完整 input deck、TPR/NDX/XTC/TOP、include 文件、受体/配体 group、模型、帧范围、熵和分解设置均由 Agent 显式提供；Action 不替用户选择科学路线。
- 解析修补：1.6.5 的 `FINAL_DECOMP_MMPBSA.csv` 是逐帧表而非预聚合统计表。适配器按体系、TDC/SDC/BDC 和残基跨帧聚合均值、样本标准差和标准误，并只返回用户指定上限的绝对贡献排序记录，同时保存完整 CSV。
- 软件测试：官方 protein-ligand 10 帧 GB 示例通过，复现 `ΔTOTAL=-15.02 kcal/mol`、样本标准差 `1.69 kcal/mol`；官方 decomposition 示例通过并产出完整分解文件。
- Action 测试：三个 Action 均通过；真实分解解析得到 153 个跨帧残基/分量记录；已有结果经统一 `execute_action` 调度复现 decomposition 示例的 `ΔTOTAL=-28.81 kcal/mol`。定向测试为 `3 passed`。
- runtime 验证：`gmx_MMPBSA`、`gmx`、`cpptraj`、`sander`，以及 `GMXMMPBSA`、ParmEd、mpi4py、NumPy、pandas 全部可用；`pip check` 无冲突，profile 探针为 `1/1 ready`。
- 配置：新增 runtime、auxiliary environment、requested-software 项、独立 environment YAML、native guide/manual/example contract 和生成手册。测试代码：`chemistry_toolbox/tests/test_gmx_mmpbsa_actions.py`。

### SISSO

状态：通过，2026-08-05 完成。

- 固定版本：官方 SISSO 3.5 当前 commit `bc18cae50e1e204cd72b2a9dfd6832225b0d8ccc`，Apache-2.0；源码缓存在 `.software_cache/sisso/3.5/source`。
- 编译器事实：官方 README 虽称其他 Fortran MPI 编译器可能可用，但现代 gfortran 14 对 `mpi_recv` 缓冲区接口报错，`-fallow-argument-mismatch` 也无效；官方 issue #29 同样记录开源编译器问题。官方仓库 PR #76 的安装指南说明 3.5 实际依赖 Intel Fortran Classic，并给出已测试版本。
- 工具链：从 Intel 官方地址缓存 Intel MPI 2021.15.0 安装器和 Intel Fortran Classic 2021.2.0 安装器，SHA-256 分别为 `d4ad297174ce3837444468645e13cfe78f11d9bf2ad9ade2057b2668cccd9385` 和 `a62e04a80f6d2f05e67cd5acb03fa58857ee22c6bd581ec0651c0ccd5bdec5a1`；silent 安装到 `.software_cache/sisso/3.5/toolchain/oneapi`，没有写系统目录。
- 构建：用官方推荐的 `mpiifort -fp-model precise` 顺序编译完整 3.5 源码；未修改科学算法。`SISSO` 二进制 SHA-256 为 `65cea3fd1982523232bfe053ea13d25851e86cfee0655fa964619ea5690c0029`。另用 ifort 编译官方 `SISSO_predict`。
- 运行依赖：`SISSO_predict` 内部调用 `bc -l`；首次预测 smoke 因缺少 `bc` 失败，已在 `reaction-kinetics/environment.yml` 声明并安装 `bc=1.07.1`。`SISSO_run` 包装器只执行 `ulimit -s unlimited` 后调用原始二进制。
- 缓存位置：`.software_cache/sisso/3.5`，约 3.0 GB，含源码、官方指南、二进制、完整 Intel 工具链、安装器、日志和 smoke 证据，不进入 Git。
- 新增 Action：`discover_sparse_symbolic_descriptor`、`evaluate_sparse_symbolic_descriptor` 和 `summarize_sparse_symbolic_descriptor_results`。CSV 列、训练/验证 ID、feature unit ranges、operators、descriptor dimension、complexity、SIS subspace、sparsifier、intercept、metric、模型数、MPI ranks 和输出边界全部显式；训练/验证 ID 重叠会直接拒绝。
- 科学 smoke：官方 5 样本回归模板完成 FC、SIS 和 DI，得到 `(feature1*feature2)` 模型；`SISSO_predict` 重算 RMSE `0.1288269420`、MaxAE `0.2270721533`，与 `SISSO.out` 一致。单进程和 Intel MPI 2-rank 运行均出现 `SISSO done successfully!`，stderr 为空。
- Action 测试：6 个显式训练样本精确恢复 `(f1*f2)`、系数 2、截距 1，两个 held-out 样本 RMSE 接近机器精度；独立 evaluation 对 8 样本通过并验证有界返回；summary 经统一 `execute_action` 调度通过。定向测试为 `3 passed`。
- runtime 验证：SISSO、SISSO_predict、bc、benchmark worker 模块和所有环境变量可用；profile 探针为 `1/1 ready`。复用 kinetics runtime 的三个已知遗留包元数据警告按原有精确规则忽略，没有忽略任何新依赖错误。
- 配置：新增 SISSO runtime、auxiliary environment、requested-software 项、native guide/manual/example contract、生成手册和测试数据；测试代码为 `chemistry_toolbox/tests/test_sisso_actions.py`。

### gplearn

状态：通过，2026-08-05 完成。

- 固定版本：PyPI `gplearn 0.4.3`，BSD-3-Clause；官方源码固定 commit `0390aea8639ce5f6c0b388400e07b58c05acad6a`。
- 缓存位置：`.software_cache/gplearn/0.4.3`，包含官方源码和 PyPI wheel，不进入 Git；wheel SHA-256 为 `e49838b57efa25dadf0e9b52df029254c826cf9bf6d1e8afd5f964ce8f213382`。
- 安装：安装到 `.envs/kinetics-legacy`，环境 YAML 增加 `gplearn==0.4.3`；运行组合为 Python 3.11、NumPy 1.26.4、scikit-learn 1.9.0 和 joblib 1.5.3。
- 接口边界：gplearn 是 Python 库，没有受支持的 CLI，因此不伪造原生命令。公共入口为类型化 Action；不提供任意 Python 执行，也不加载用户提供的 pickle/joblib 文件。
- 新增 Action：`fit_symbolic_regression_baseline`、`assess_symbolic_regression_seed_stability` 和 `summarize_symbolic_regression_results`。CSV 列、显式训练/验证 ID、函数集、metric、种群、代数、锦标赛、常数范围、初始化深度、简约系数、遗传操作概率、抽样比例、并行度和 seed 全部显式；划分重叠、超资源并行和非法概率直接拒绝。
- 上游测试：使用固定源码和当前依赖运行官方测试，结果 `54 passed`；三个 warning 仅为 scikit-learn 对 `SCIPY_ARRAY_API` estimator check 的跳过说明。
- Action 测试：固定 seed 重复拟合得到相同方程和 held-out RMSE；三 seed 运行返回每个方程、held-out metrics、唯一方程数、主方程比例以及 RMSE 均值/样本标准差；JSON summary 经统一 `execute_action` 调度通过。定向结果为 `3 passed`。
- runtime 验证：profile 探针为 `1/1 ready`；仅复用 kinetics runtime 已知的三个旧包元数据警告，没有忽略新依赖错误。

### 条件候选

#### MultiWell

状态：未加入，许可与下载前置条件不满足。

- 官网公开 MultiWell 2023.1 源码、示例和手册链接，但页面及可检索文档未提供明确的软件许可证或再分发授权；“可下载源码”不能等同于开源许可。
- 2026-08-05 从官网压缩包地址以普通请求、浏览器 User-Agent、Referer、查询参数和 TLS fallback 多次下载均返回 HTTP 403；未从不明镜像替代下载。
- 当前 MESS/MESMER 已覆盖基础主方程能力。未满足合法自动部署和可复现下载前，不注册 runtime、Backend 或 Action。

#### VASPKIT

状态：本机通过，2026-08-05 完成；禁止再分发。

- 固定版本：官方 SourceForge Linux x64 binary `1.5.1`；下载包 SHA-256 为 `41bbdc0759f72cd43ef7e2f541d228a639bd95dba2a549398b28f47d760d72b1`。
- 缓存位置：`.software_cache/vaspkit/1.5.1`，包含官方包、本机 `.vaspkit` 配置和 smoke，不进入 Git。
- 许可边界：包内 `license` 允许学术、科学、教育和非商业使用，但第 2 条禁止未经书面许可再分发任何分发文件。因此该缓存不能复制给另一用户/服务器，也不能上传 GitHub；迁移操作者必须从官方 SourceForge 重新下载。
- 配置：不修改真实用户 HOME。每个 Action 在自己的输出目录生成临时 `HOME/.vaspkit`，显式写入对称容差、角度容差或费米参考策略；不包含或自动选择 VASP POTCAR。
- 新增/扩展 Action：新增 `generate_vasp_kpoint_mesh` 和 `extract_vasp_band_gap`；已有 `analyze_crystal_symmetry` 增加 VASPKIT backend。K 网格分辨率/中心方式、结构容差、角度容差和费米零点策略均显式。
- 软件 smoke：官方 ZnO 示例得到 `12x12x5` Gamma 网格；空间群 `P6_3mc`（No.186）、12 个对称操作及两组等价原子；直接带隙 `0.7667 eV`、VBM/CBM band index 18/19。
- 已知边界：1.5.1 的 task 102 写完 KPOINTS 后仍尝试生成 INCAR/POTCAR，并在无授权势文件时报错但返回 0。Action 只在 `Written KPOINTS File` marker 和可解析 KPOINTS 同时存在时成功，并明确返回 `potcar_generated=false`。
- 测试：三个真实 Action（含统一 `execute_action`）以及原生文档/配置回归通过；定向结果 `16 passed`。runtime profile 为 `1/1 ready`，依赖检查无冲突。

PyFrag 和 BAGEL 继续按许可与构建条件处理；Progdyn 当前因缺少明确许可证而停止。

#### PyFrag

状态：通过，2026-08-05 完成。

- 固定版本：官方 LGPL-3.0 `v1.0.0`，commit `af2a122d7676ee1578ac895ac4f076fdecaccdf5`，软件运行标识为 PyFrag 2019.02；缓存位于 `.software_cache/pyfrag/2019`，约 56 MB，不进入 Git。
- 兼容修补：原始脚本的 `re.split(r'[ =,]*', ...)` 在 Python 3 会按字符拆分输入，且旧 ORCA 能量解析器会在 ORCA 6 输出上读取到字符串 `final`。仅修补为非空分隔符并优先解析 `FINAL SINGLE POINT ENERGY`；迁移补丁已保存为 `chemistry_toolbox/patches/pyfrag-v1.0.0-python3-orca6.patch`。修补后脚本 SHA-256 为 `6fc4c617ad81d5b01003d24c40828a6d57d460f8487b6ddab89cf7d04500fef6`。
- 运行边界：采用官方 standalone ORCA 路线，只做 activation-strain analysis；不宣称提供 ADF/AMS EDA。ORCA 6.1.1 是单独注册下载的软件，不随 LGPL PyFrag 再分发；匹配 OpenMPI 4.1.8 继续复用现有缓存。
- 新增 Action：`analyze_activation_strain_profile`、`summarize_activation_strain_profile`、`validate_activation_strain_profile`。路径格式/类型、片段名称和完整不重叠原子划分、两个片段参考能量、ORCA simple keywords、总电荷、自旋多重度、反应坐标、路径点上限、结果返回上限和闭合容差全部显式。
- 科学 smoke：官方两点 H4 ORCA 示例触发 2 个复合物和 4 个孤立片段单点，共 6 个输出均含 `ORCA TERMINATED NORMALLY`；得到两行 activation-strain table，并满足 `EnergyTotal = TotalIntEn + StrainTotal`，最大闭合误差小于 `0.001 kcal/mol`。
- 测试：真实 Action 计算、独立 summary、validation 和非法片段重叠前置拒绝为 `3 passed`；连同原生手册与软件清单回归为 `23 passed`。reaction runtime 探针为 `required_ok=true`，PyFrag 后端、命令、补丁证据、ORCA/OpenMPI 和三个既有精确忽略的旧包元数据警告均按预期。
- 配置：新增 PyFrag Backend、reaction runtime/auxiliary environment、requested-software 项、native guide/manual/example contract、生成手册和测试代码 `chemistry_toolbox/tests/test_pyfrag_actions.py`。现有环境 YAML 无需新增包：脚本只依赖 Python 标准库，ORCA/OpenMPI 已在 reaction runtime 声明。

#### Progdyn

状态：未加入，许可证与可移植性条件不满足。

- 官方 GitHub 仓库在 2026-08-05 可访问，但根目录和源码文件中未发现 LICENSE、COPYING、版权许可或明确的使用/再分发授权；公开可读源码不等于免费开源软件，因此没有复制到 `.software_cache`，也没有注册 runtime 或 Action。
- 仓库附带完整 Gaussian 16 输出示例，而主驱动明确依赖 Gaussian，并要求针对具体体系人工修改 `proganal`。在缺少软件许可且核心路线绑定商业 Gaussian 的情况下，不把它改称 ORCA 通用程序，也不把未经验证的重写加入工具箱。
- 后过渡态轨迹仍是十方向中的能力缺口；后续应在取得作者许可后固定 Progdyn 版本，或基于现有 ASE/ORCA 建立独立、可测试且许可证清晰的替代实现。

#### BAGEL

状态：通过，2026-08-05 完成。

- 固定版本：GPL-3.0-or-later 官方源码 tag `v1.2.2`，commit `bfceffea5725992c708a9ae03f26604e2fcc1b15`；执行文件采用 Ubuntu 22.04 `bagel_1.2.2-3ubuntu1_amd64.deb`，包 SHA-256 为 `5cc9c366c83dd7f3bbd2c656cfbcec9d8477d147c154ef4b6729a4d36924b29f`。
- 缓存位置：`.software_cache/bagel/1.2.2`，约 519 MB，包含精确源码、BAGEL 二进制、basis 数据、MPICH/Hydra 和完整非系统运行库闭包，不进入 Git。迁移必须复制整个版本目录，不能只复制 `BAGEL` 文件。
- 运行配置：`BAGEL` wrapper 从自身位置推导 runtime，解析 JSON 后只把用户显式给出的 basis 和 density-fitting basis 名称机械映射到缓存内绝对路径；`bagel-mpirun` 提供显式 rank 的 MPICH 调用。两者都不改系统目录或真实 HOME。
- 新增 Action：`calculate_multireference_state_energies`、`calculate_multireference_nuclear_gradient`、`calculate_nonadiabatic_coupling_vector`。结构、电荷、自旋、基组、闭壳层/活性轨道、态数、目标态、CASSCF/FCI 收敛阈值、XMS-CASPT2 shift/frozen-core/SSSR 和 MPI/OpenMP 布局均显式，并在执行前校验电子数与资源上限。
- 科学 smoke：官方 LiF 四态 SA-CASSCF/NAC 得到态间能隙 `2.2770111863 eV` 和完整耦合向量；官方 Li2 XMS-CASPT2 解析梯度及能量 `-14.8779135422 Eh`；HF/FCI 示例串行和 2-rank MPICH 均正常结束，stderr 为空。
- 测试：3 个真实科学 Action 和一个非法 active-space 前置拒绝均通过；连同原生文档和软件清单共 `24 passed`。`bagel` profile 探针为 `required_ok=true`，BAGEL、MPI wrapper、raw binary、basis directory 和依赖检查全部通过。
- 环境声明：没有修改共享 Conda 环境来满足 BAGEL；新增依赖都在 `.software_cache/bagel/1.2.2/runtime` 内，因此现有 `general-modern-openmpi5/environment.yml` 无新增 BAGEL 包。可迁移配置位于 runtime/auxiliary/requested-software、native guide/manual/example contract 和生成手册；测试为 `chemistry_toolbox/tests/test_bagel_actions.py`。

## 十方向 Action 补全

完成，2026-08-06。

| 方向 | 主要已有/本轮软件 Action | 本轮补充的通用质量门 | 结论 |
|---|---|---|---|
| 1 反应机理、势能面与选择性 | TS、路径、IRC、GoodVibes、PyFrag | `analyze_post_transition_state_trajectory_ensemble` | 对显式产品分类计算分支比、recrossing、失败率和 Wilson 区间；Progdyn 未合法接入，因此不伪装成轨迹生成器。 |
| 2 构象、热化学与性质 | CREST/CENSO、聚类、排序、GoodVibes | 无新增 | 已有生成、去重、优化后排名、Boltzmann 权重和热化学校验原子步骤。 |
| 3 周期表面吸附与成键 | QE/VASP/GPAW、VASPKIT、LOBSTER/Critic2 | `calculate_adsorption_energy` | 从显式吸附体系、洁净表面和带化学计量系数的参考能计算吸附能，保留符号约定。 |
| 4 电子密度、QTAIM 与成键 | ORCA、Multiwfn、Critic2、LOBSTER | 无新增 | 密度生成/导出、临界点、basin、Bader、电荷、键级和 COHP 已拆分。 |
| 5 动力学、主方程与微观动力学 | RMG/Arkane、MESS/MESMER、CatMAP、Cantera | 无新增 | `solve_master_equation` 已覆盖 MultiWell 拟补的主方程原子能力；不因软件数量重复实现。 |
| 6 激发态、光谱与光化学 | ORCA/OpenMolcas、SHARC/Newton-X、TheoDORE、BAGEL | `analyze_nonadiabatic_trajectory_ensemble` | 从归一化轨迹计算态布居、hop、初态存活、失败轨迹和置信区间；BAGEL 增加多参考能量/梯度/耦合。 |
| 7 高压结构与多相稳定性 | AIRSS、周期 DFT、Phonopy/TDEP | `construct_pressure_enthalpy_phase_diagram` | 在共同压力网格选择稳定相，并从两相焓差线性插值得到有 bracket 的转变压力。 |
| 8 声子、非谐性与热输运 | Phonopy/Phono3py、TDEP、ShengBTE | `assess_phonon_stability` | 以显式虚频、Gamma q 点和声学支容差区分动力学不稳定与数值小虚频。 |
| 9 MD、增强采样与自由能 | GROMACS/PLUMED、pmx/ACPYPE、PyMBAR/alchemlyb、gmx_MMPBSA | 无新增 | 已有能量解析、MBAR/PMF、收敛、混合拓扑、结合能和残基分解。 |
| 10 描述符发现与设计 | SISSO、gplearn、RDKit、ASE/pymatgen | 无新增 | 已有训练/验证显式划分、模型评估、跨 seed 稳定性和有界结果总结。 |

新增 5 个 Action 均为确定性结果分析，不运行或替代上游科学计算，也不隐藏参考态、相、产品标签、状态映射或容差。手算测试覆盖吸附能 `-1.0 eV`、两相交点 `5.0 GPa`、稳定/不稳定声子、`2:1:1` 后 TS 分支和含一条失败轨迹的三态非绝热布居；结果 `5 passed`。Action/handler 集合测试另为 `1 passed`。

## 最终验证

- 本轮实际加入缓存并适配 10 项：AIRSS、TDEP、ACPYPE、pmx、gmx_MMPBSA、SISSO、gplearn、VASPKIT、PyFrag、BAGEL，合计约 13 GB。VASPKIT 禁止再分发；其余各项的精确版本、源码 commit、包校验和及迁移边界见各软件条目。
- 未加入 2 项：MultiWell 和 Progdyn 均缺少可确认的软件许可证；没有从镜像或公开仓库可读性推导开源授权。
- 新增软件 Action 定向回归：AIRSS 2、TDEP 3、ACPYPE 3、pmx 4、gmx_MMPBSA 3、SISSO 3、gplearn 3、VASPKIT 3、PyFrag 3、BAGEL 4，合计 `31 passed`。
- 框架分组回归：参数公开 `6 passed`、渐进发现 `22 passed`、调度自治 `7 passed`、软件清单 `7 passed`、原生文档 `13 passed`、十方向通用分析 `5 passed`。
- 所有新增软件 Action 和十方向通用分析均经公共 `execute_action` 入口重新执行；动态覆盖清单达到 146 个 Action、89 个 Backend 和 282 个 Action/Backend 组合，`282/282` 组合均有运行证据，`89/89` Backend 均有成功证据，未观测组合为 0。
- 全工具箱回归按项目的多环境边界执行：主测试环境排除要求 Python 3.11 的 gplearn 后为 `456 passed`，gplearn 在 kinetics Python 3.11 环境为 `3 passed`，合计 `459 passed`、0 failed。不能用单一通用环境替代多环境验证；通用环境不包含 ACPYPE/alchemlyb 的分子模拟依赖，而旧主环境的 Python 3.10 不满足 gplearn 0.4.3 的 Python 版本要求。
- 重新生成请求软件状态后为 58 项：57 `configured`、1 `specification`，无 `partial`、`not_found` 或人工审查项。原生手册覆盖 63 个软件、生成 447 个文件。
- BAGEL 独立 profile 探针为 `required_ok=true`；本轮每个软件的 runtime/profile 和真实 smoke 结果记录在对应条目中。最终 `git diff --check` 无格式错误。

## 2026-08-06 第二轮：三层适配与真实复杂路径

### 本轮边界

- 按要求不处理 NAMD CUDA 和 Amber CUDA。
- AiiDA 本地 SQLite profile 可用于本地同步计算；RabbitMQ 只影响 daemon/异步队列，本轮不配置。
- 第一层只增加有明确输入、设置、输出和判定条件的 typed Action；第二层保留 Agent 编写原生输入的能力；不把论文路线或科学参数选择隐藏在 Action 内。

### PubChem 记录修复

- `config.local.env` 中已不存在 `RESEARCHCHEMBENCH_PUBCHEM_PROXY_URL`，当前测试直接访问 PubChem。
- `run_action_gap_smokes.py` 和 `run_data_source_smokes.py` 删除了已由 evaluator 控制的 `walltime_seconds`/`timeout_seconds`，避免请求在联网前被当前 Pydantic 契约拒绝。
- 最新记录：`search_compounds`、`resolve_chemical_identity`、`retrieve_compound_properties`、`retrieve_compound_structure`、`search_similar_compounds`、`search_substructures` 共 6 个 PubChem Action 全部成功。
- `data_source_smoke_status.json` 中 PubChem 为 `success`。该轮出现的 Materials Project 超时和 Catalysis-Hub `401` 已在后续认证与重试修复中解决，见文末数据源修复记录。

### 第一层 Action

| 软件 | 新增 Action | 真实验证 |
|---|---|---|
| Yambo 5.3.0 | `calculate_quasiparticle_corrections`、`calculate_bse_optical_spectrum` | 真实 Si `SAVE` 上完成最小 G0W0/BSE；解析 2 个 QP 状态和 50 个光谱点 |
| SHARC | `propagate_nonadiabatic_trajectory` | 官方 LVC 输入完成 30 fs、61 条记录；另完成 3 个独立 seed 的完整轨迹集合 |
| KinBot 2.2.2 | `explore_reaction_network` | 公共 `execute_action` 经本地 NWChem 进入真实反应搜索，返回 `pes_complete=true`、1 个井和 2 条 `SUCCESS` 反应记录 |

已有新增软件的 Action 数量：AIRSS 2、TDEP 3、ACPYPE 3、pmx 4、gmx_MMPBSA 3、SISSO 3、gplearn 3、VASPKIT 3、PyFrag 3、BAGEL 4。上述软件均保留通用、显式参数的原子能力，不提供任意 shell 或任意 Python 执行。

### 第二层可检索文档

- `generate_native_software_manuals.py` 现在从 BackendSpec 自动把对应 typed Action 写入每个软件的 `INDEX.md` 和 `COMMON_TASKS.md`，建立第一层与第二层之间的明确路由。
- AIRSS、TDEP、ACPYPE、pmx、gmx_MMPBSA、SISSO、VASPKIT、PyFrag、BAGEL、Yambo、SHARC 和 KinBot 均有 `INDEX/QUICKSTART/COMMON_TASKS/TROUBLESHOOTING` 四份生成手册。
- gplearn 没有受支持的原生 CLI，因此没有伪造命令；新增独立 Action-first 四份手册，`search_software_documentation(software_id="gplearn", ...)` 和 `inspect_software` 均可发现其 3 个 Action、输入契约、数据泄漏检查、seed 稳定性和资源限制。
- 生成手册更新了 Yambo/SHARC/KinBot 的真实版本、输入输出、正常结束标志、已知失败和科学收敛边界。
- `inspect_software` 现在把旧的原生命令 interface smoke 与新的 Action scientific smoke 分开合并；Yambo、SHARC、KinBot 均显示 `scientific_smoke_status=passed`，同时保留原始 interface 证据及新报告哈希。

### Yambo 真实 GW/BSE

- 证据目录：`.software_cache/yambo/smoke/qe_si_gw_bse`。
- G0W0 输出 `o-gw.qp`：band 4 修正 `0.714835 eV`，band 5 修正 `2.108043 eV`；最小示例的 KS gap 为 `2.556848 eV`，直接按两个状态计算的 QP gap 为 `3.950056 eV`。
- BSE 输出 `o-bse.eps_q1_diago_bse` 包含 50 个可解析点；首点 `epsilon_2=0.268508`。
- GW/BSE report 均含 `Game Over`。`auxiliary_environments.yaml` 的 smoke 路径已按真实文件名修正。
- 该任务只证明端到端路径与解析器；不能替代空带数、介电截断、k 网格、展宽和频率网格收敛。

### SHARC 完整轨迹集合

- 上游问题：未配置 LP-ZPE 列表时，`lpzpe_nah/lpzpe_nbc` 未初始化，gfortran 在写空 implied list 的 restart 时会段错误。
- 修补：初始化计数为 0，并对零长度 restart 列表写空行；可迁移补丁为 `chemistry_toolbox/patches/sharc-v3-gfortran-empty-restart-list.patch`，对当前缓存源码的反向应用检查通过。
- 证据目录：`.software_cache/sharc/smoke/lvc_ensemble/TRAJ_00001..00003`。三个 seed 均到达 `30.0000 fs`，每条 61 个记录；最终 diagonal state 分别为 5、8、5，状态变化次数分别为 0、3、0。
- runtime 增加已安装的 `pyscf==2.13.1` 声明；SHARC LVC/PySCF 接口和完整轨迹 smoke 均纳入环境检查。
- 3 条短轨迹是稳定执行 smoke，不是收敛的态布居、寿命或量子产率集合。

### KinBot 完整 PES

- 固定上游版本：tag 2.2.2，commit `2b530ad24a4dd6a52743a783752821d5d2560519`。
- 上游阻塞包括：`queuing=local` 只读取预计算结果、不执行子任务；`pes` 传入字面量 `&` 并用硬编码 root 进程表；NWChem 模板绑定旧 ASE/Python 2；当前 ASE 需要嵌套 `dft/driver`；长工具箱路径触发 NWChem `util_pname: pname too short for name.id`；通用模板把完成标志写入 `.log`，而 KinBot 的 NWChem 检查读取 `.out`；初始频率检查对小虚频的处理与参数门限不一致。
- 可迁移补丁：`chemistry_toolbox/patches/kinbot-v2.2.2-local-nwchem.patch`。补丁实现本地异步子进程、正确进程状态、Python 3 模板、当前 ASE-NWChem 参数转换、统一的 NWChem `.out` 完成标志、显式虚频门限、可配置 Sella 门限及短 `/tmp` scratch/permanent 根。反向应用检查通过。
- runtime 显式配置 KinBot/NWChem 命令、NWChem basis/NWPW library、通用 NWChem PATH/LD 路径和短工作根；Action 使用独立临时根并在结束后清理。
- 早期 77 秒和 98 秒的运行虽然出现外层 `PES search done!`，但子任务日志含 `Error with initial structure optimization.`，属于假成功，已从有效证据中排除。Action 现在同时检查外层完成标志、子任务日志、初始优化失败标志和 `Starting reaction search...`，请求反应搜索却未进入该阶段时直接失败。
- 最终公共 `execute_action` smoke 用时约 167 秒，证据位于 `.software_cache/kinbot/smoke/action_nonempty_pes_validated3`：返回 `pes_complete=true`、`well_count=1`、`reaction_record_count=2`，两条记录均为 `SUCCESS`（`hom_sci_1_2` 和 `hom_sci_1_3`）。该结果验证了本地调度、初始优化/频率、反应搜索和结果解析的非空 PES 路径。
- 本 smoke 使用 B3LYP/STO-3G 和为执行稳定性设置的 100 cm-1 小虚频容差，只用于软件编排回归，不代表生产级能垒或完整网络收敛。正式 benchmark 仍应使用文献级方法、已知参考网络，并检查 TS、IRC/连接性、能垒和搜索完备性。
- 完整 PES 回归为可选慢测试：设置 `RESEARCHCHEMBENCH_RUN_EXPENSIVE_KINBOT_PES=1` 后运行 `test_yambo_sharc_kinbot_actions.py`。

### 迁移要求

1. 按仓库 YAML 重建 `.envs/general-modern-openmpi5`、`.envs/kinetics-legacy` 和 `.envs/yambo-openmpi4`。
2. 将对应 `.software_cache/yambo`、`.software_cache/sharc`、`.software_cache/kinbot` 及 NWChem basis 缓存迁移到相同项目相对位置。
3. 对原始 SHARC 固定源码应用上述补丁并重新构建；KinBot 由 `build_merged_environments.sh` 自动固定提交、应用补丁并安装。
4. 运行 runtime 清单、补丁反向检查、四个软件扩展 Action smoke 和文档测试；不要只复制已经修改过的 site-packages。

### 覆盖结果

- 新增复杂路径记录：`chemistry_toolbox/config/software_expansion_action_smoke_status.json`，4/4 成功。
- 合并覆盖：150 个 Action、92 个 Backend、286 个 Action/Backend 组合；286/286 有成功运行证据，未观测组合为 0。
- 文档检索测试包含 gplearn Action-only 手册；Yambo/SHARC 真实 Action 测试和 KinBot 输入拒绝测试进入默认回归，KinBot 完整 PES 作为显式慢测试保留。
- 本轮最终聚焦回归为 `63 passed, 1 skipped`；跳过项仅为默认关闭的 KinBot 完整 PES 重算，测试会直接校验已保存的 2 条成功反应证据，设置 `RESEARCHCHEMBENCH_RUN_EXPENSIVE_KINBOT_PES=1` 可重新执行。
- 请求软件清单重新审计为 58 项：57 `configured`、1 `specification`、0 项待人工复核。原生手册生成检查为 63 个软件、447 个文件，无漂移。
- KinBot 与 SHARC 补丁均通过当前缓存源码的反向应用检查；`git diff --check` 通过。

## 2026-08-06 数据源重试与认证修复

- Materials Project 改为对超时、连接错误、HTTP 429 和 HTTP 5xx 进行有限重试；默认单次请求最多 25 秒，第一次瞬时失败后等待 3 秒，最多再请求一次。HTTP 400/401/403 等确定性客户端错误不会重试；结果 provenance 记录 `remote_attempts` 和 endpoint。
- Materials Project 的 25 秒单次预算、3 秒退避和最多一次重试可保证默认最坏路径不超过数据 Action 的 60 秒总预算。
- Catalysis Hub 现在要求 API key。BackendSpec 声明 `CATALYSIS_HUB_API_KEY`，请求通过 `X-API-Key` 发送；缺少密钥时直接返回明确的 `unavailable`。真实密钥只保存在被 Git 忽略的本机 `config.local.env`；公开仓库仅提交 `config.local.env.example`。
- Catalysis Hub 的认证请求曾连续返回两次 HTTP 500，因此补充为单次 15 秒、最多 3 次请求、2/4 秒指数退避；默认最坏路径为 51 秒，仍在 60 秒数据 Action 总预算内。HTTP 400/401/403 不重试。
- 参数目录为 Materials Project 和 Catalysis Hub 暴露 `max_retries` 与 `retry_backoff_seconds`；二者的 `max_retries` 上限分别为 1 和 2。
- 单元回归：Materials Project/Catalysis Hub 适配器、连续两次瞬时故障、认证缺失和参数公开测试共 `19 passed`。
- 最终公共 `execute_action` 联网 smoke：PubChem、RCSB PDB、Materials Project、Catalysis Hub、NIST WebBook 共 `5/5 success`。其中 Materials Project 返回 1 条记录，用时 2.99 秒；Catalysis Hub 返回 1 条记录，用时 3.32 秒。

## 2026-08-06 启动与全量回归修复

- 在 `mcp_profiles.yaml` 中注册 Yambo、SHARC、KinBot 三个已有 runtime，复用现有环境、缓存、命令变量和实算 smoke；92 个 BackendSpec 现均有且仅有一个 runtime，benchmark workspace 可正常创建。
- `check_mcp_tools.py` 直接复用服务端的 `ASYNC_ACTION_TOOL_NAMES`，全量清单为 150 个 Action、18 个开放执行工具和 2 个异步工具，不再维护遗漏异步工具的独立清单。
- 原生指南公开 Yambo `p2y`、SHARC `wfoverlap.x`、KinBot `kinbot` 等辅助命令；BackendSpec 只声明对应第一层 Action 实际依赖的 `yambo`、`sharc.x` 和 `pes`，避免层级耦合。
- SHARC 三轨迹 smoke 的最终时间列由错误的第一列改为第二列，三条轨迹均验证到达 30 fs；删除 AIRSS 指向不存在许可证文件的无效 smoke，保留真实 `airss_version` 运行检查。
- ACPYPE 依赖由 Conda `openbabel=3.1.1` 实际满足，Python 导入、`obabel` 和 ACPYPE smoke 均通过。未安装可能覆盖 Conda ABI 的 `openbabel-wheel`；共享 OpenFF runtime 的 profile 仅精确忽略该 PyPI 发行包名告警。TDEP 同样沿用 kinetics runtime 已有的三条旧包平台标签 allowlist。
- 生成状态已刷新：50/50 runtime ready；58 项 requested software 为 57 `configured`、1 `specification`，无人工审查或未配置项。
- 验证：MCP/profile 包级测试 `15 passed`；MCP 三层 smoke 通过；根级 benchmark `97 passed`；相关软件与原生执行测试 `24 passed, 1 skipped`；完整 toolbox verifier 及 7 个代表性科学 smoke 通过；全量化学工具箱 `467 passed, 1 skipped`。唯一跳过项是默认关闭的 KinBot 完整 PES 重算，保存证据与显式慢测试此前已通过。

## 2026-08-06 可迁移性收口

- `mcp_profiles.yaml` 统一为 50 个正式 `profiles`；删除没有运行时语义的 `support_environments` 分类和逐 profile `server_name`。`auxiliary_environments.yaml` 只保留 7 个无 BackendSpec 的原生/可编程运行时。
- `merged_environments.yaml` 完整覆盖全部 57 个运行时，`RESEARCHCHEMBENCH_ENV_ROOT` 对此前漏映射的软件同样生效。
- gmx_MMPBSA 改为第七个正式化学前缀 `.envs/gmx-mmpbsa`，新增可维护 YAML、pip requirements、`linux-64` explicit lock 和 pip inventory；`.software_cache/gmx_mmpbsa` 只保留安装包及实算夹具。
- 新增 `install_patched_kinbot.sh`。构建 reaction-kinetics 时固定 KinBot 2.2.2 commit `2b530ad24a4dd6a52743a783752821d5d2560519`，验证并幂等应用补丁，再安装到目标前缀；本机重复安装验证通过。
- BackendSpec 与第二层原生命令解耦：原生指南可公开辅助命令，BackendSpec 只声明 Action 所需可执行文件。
- `config.local.env` 从 Git 索引取消跟踪并在本机保留；新增无密钥的 `config.local.env.example`。持久化状态生成器会移除项目绝对路径。
- 删除已停用的 `chemistry_toolbox/environment/locks`（121 个旧 `.tool_envs` 锁）、孤立的 `mcp_profile_status.json` 和重复旧工具矩阵。当前构建只使用 `environment/merged/locks`。

### 可迁移性最终检查

- 持久化状态与原生 smoke 归档统一通过 `portable_report_value`/`portable_report_text` 删除项目绝对路径、存储用户前缀和主机名，并清除行尾空格；相关回归测试覆盖三类机器特有值。
- `run_native_smokes.py` 与 `run_native_interface_smokes.py` 支持幂等 `--refresh-hashes`。同时给出 `--refresh-hashes --verify` 时先刷新再校验，避免旧分支顺序导致只校验、不刷新的误判。
- 当前 v3 五项原生科学证据校验有效；当前 63 软件接口证据与原生指南 ID 完全一致，为 49 `passed`、14 `started_input_required`、0 `failed`、0 `skipped`，归档完整性校验通过。Arkane、RMG 和 VESTA 修复后的接口探针均为 `passed`，MATLAB/EasySpin 不再出现在活动证据中。旧 v2 仍如实保留当时 Gaussian 未完成状态，不作为当前有效基线。
- 根目录测试产物 `censo.log`、`gmx_MMPBSA_test.log`、`gmx_MMPBSA.log`、`kinbot.log`、`pes.log`、`timer.dat` 和 `_tool_trace.jsonl` 已加入根级忽略规则，并在最终测试后删除。
- 最终聚焦回归为 `103 passed`，根级 benchmark 为 `97 passed`；MCP 清单校验为 150 个 Action、18 个开放执行工具和 2 个异步工具。原生手册仍为 63 个软件、447 个生成文件且无漂移。
- 跟踪文件扫描未发现项目绝对路径、真实服务器名、用户存储标识或 Catalysis Hub 密钥；仅脱敏实现及其虚构路径测试保留 `/inspire/hdd/global_user` 匹配字面量。
