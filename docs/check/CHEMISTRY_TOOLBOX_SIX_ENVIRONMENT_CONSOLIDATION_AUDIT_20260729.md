# Chemistry Toolbox 六环境合并与验证报告

日期：2026-07-29

分支：`codex/consolidate-toolbox-envs-20260729`

基线：`a85c520`（`feat: implement chemistry toolbox v3 reliability plan`）

## 1. 结论

原有 40 个 `.tool_envs` 工具环境已在**不删除、不覆盖旧环境**的前提下，重新组织为 6 个可重建的 Conda 环境。合并布局下：

- 114 个科学 Action 和 16 个开放执行工具均正常注册；
- 三层 MCP 调用链通过；
- 7 个跨环境代表性真实 Action 全部成功；
- 完整代码测试为 `428 passed`；
- 六份 Linux x86-64 精确 Conda 锁均可被 Mamba 正确解析；
- 原有 `.tool_envs` 40 个环境、`.toolbox_env` 和 `.venv` 均保留，尚未执行删除。

因此，六环境方案已经达到“可以替代原 40 个工具环境进行工具箱运行与迁移”的技术验证条件。建议先保留旧环境作为回退，待用户确认后再单独执行清理。

## 2. 六个合并环境

| 逻辑环境 | 实际目录 | Python | Conda 包数 | 磁盘占用 | 主要能力与兼容边界 |
|---|---|---:|---:|---:|---|
| general-modern-openmpi5 | `.tool_envs_merged/general-modern-openmpi5` | 3.11.15 | 367 | 13 GB | MCP、RDKit、ASE、Psi4、GPAW、NWChem、QE、声子、材料分析、MACE/CHGNet、OpenMPI 5 及多数原生软件入口 |
| molecular-simulation-openff | `.tool_envs_merged/molecular-simulation-openff` | 3.12.13 | 347 | 8.8 GB | OpenFF、AmberTools、OpenMM、GROMACS、HOOMD、自由能分析、对接；固定 NumPy 1.26 与 Pydantic 2.11.7 |
| reaction-kinetics | `.tool_envs_merged/kinetics-legacy` | 3.11.15 | 501 | 7.1 GB | RMG、Cantera、KinBot、Sella、CENSO、pysisyphus，以及采用 MPICH 4 的 ABINIT/LAMMPS |
| equivariant-ml | `.tool_envs_merged/equivariant-ml` | 3.11.15 | 220 | 6.5 GB | DeePMD、NequIP、Allegro、CPU Torch 2.10、e3nn |
| periodic-mpich | `.tool_envs_merged/periodic-mpich` | 3.10.20 | 113 | 2.5 GB | CP2K 2026.1、MPICH 5、libxc 7 |
| catmap-yambo-openmpi4 | `.tool_envs_merged/yambo-openmpi4` | 3.11.15 | 186 | 1.8 GB | CatMAP 0.3.1/ASE 3.17 与 Yambo 5.3/OpenMPI 4 的隔离兼容环境 |

合并环境总占用约 40 GB。包数为各前缀 `conda-meta` 记录数，不等于独立软件数量。

## 3. 为什么不能进一步无条件合并

六个边界不是按软件类别任意拆分，而是由实际 ABI 和依赖约束决定：

1. OpenFF/AmberTools 需要 NumPy 1.x，不能与通用环境的 NumPy 2.x 栈直接合并。
2. CatMAP 0.3.1 依赖旧 ASE 3.17，不能与现代 ASE 3.29 用户共存。
3. CP2K 2026.1 使用 MPICH 5/libxc 7；ABINIT 10.0.3 和当前 LAMMPS 组合使用 MPICH 4/libxc 4，二者曾在同环境中发生实际求解冲突。
4. Yambo 当前包使用 OpenMPI 4，而通用环境为 OpenMPI 5。
5. DeePMD/NequIP/Allegro 的 Torch、e3nn 和编译运行时较重，独立后可避免污染量化与 MCP 主运行时。
6. AmberTools 26 与独立 Packmol 的 Conda 依赖声明冲突，因此 Packmol 安装在通用环境，并通过受控的 PATH 前置方式提供给分子模拟环境。

继续压缩到四个环境会迫使至少一组上述互斥 ABI 或 Python 包版本共存，无法保证可重建性和运行稳定性。

## 4. 代码与迁移能力修改

### 4.1 运行时布局

- 新增 `config/merged_environments.yaml`，集中记录六个物理前缀和全部逻辑 runtime 映射。
- 新增 `environment_layout.py`，将逻辑 runtime 直接映射到项目 `.envs/` 下的六个工具环境，不保留旧布局选择或回退逻辑。
- 标准安装无需设置环境变量；仅当七个环境整体迁移到其他目录时，使用 `RESEARCHCHEMBENCH_ENV_ROOT=/path/to/envs` 重定位环境根目录。
- MCP profile、后端 runtime 和跨环境命令路径均通过统一解析器定位，不改变 Action ID、backend ID 或智能体调用协议。
- 增加 `prepend_path_entries`，用于明确控制共享命令优先级，而不是依赖宿主 PATH 的偶然顺序。

### 4.2 可重建环境定义

每个环境均提供：

- `environment.yml`：人工维护、适合跨主机重新求解的 Conda 依赖；
- `requirements.txt`：pip/VCS 依赖及版本；
- `locks/linux-64/*.explicit.txt`：本机验证过的精确 Conda artifact；
- `locks/linux-64/*.pip-freeze.txt`：已安装 Python 包快照；
- `locks/linux-64/manifest.json`：锁文件 SHA-256 和生成时间。

同时新增：

- `scripts/build_merged_environments.sh`：从依赖定义或精确锁创建/更新环境；
- `scripts/capture_merged_environment_locks.sh`：环境变更后重新生成锁和哈希；
- `environment/merged/system-requirements.txt`：VESTA 等 GUI/原生程序的宿主动态库要求；
- portable lock/bootstrap 对 `.tool_envs_merged`、`prepend_path_entries` 和可重定位前缀的支持。

### 4.3 合并过程中修复的问题

- CatMAP 从通用 reaction runtime 中拆出，避免 ASE 版本冲突。
- LAMMPS 从 MD/OpenFF runtime 中拆至 MPICH 4 环境，避免 AmberTools 的 nompi FFTW/HDF5 依赖破坏 LAMMPS/ABINIT。
- Psi4 从 1.9.1 更新到 1.11，修复 `libint` SONAME 不匹配。
- OpenFF Interchange 固定 Pydantic 2.11.7，修复序列化失败。
- RDKit 2026 同时兼容 ETKDG 的 `maxAttempts`/`maxIterations` 参数名称。
- GNINA 静态可执行文件补充稳定入口链接，并由构建脚本重建。
- GoodVibes 的帮助/版本探测允许不提供科学输入，避免原生接口 lint 误判。
- VESTA 补齐 Xvfb、XAuth、GTK 和 xkbcommon 宿主依赖，可在无显示服务器上启动。
- CENSO 使用可重放的精确 Conda artifact URL，避免当前 channel 索引已删除旧版本导致无法重建。

## 5. 验证结果

| 验证层级 | 结果 | 说明 |
|---|---|---|
| 完整 pytest | `428 passed in 532.62s` | 运行全部项目和工具箱测试 |
| runtime/profile 审计 | 38/38 ready | 全部正式 profile 和 support runtime 可解析、环境存在、健康检查通过 |
| Action/backend profile 测试 | 66/66 available | 114 个 Action 所涉及的 profile 后端均可用 |
| MCP 三层烟雾测试 | PASS | 注册 114 Actions、16 open-execution tools；Action、软件手册、Agent 程序、后台作业、Artifact 和 trace 链路通过 |
| 真实 Action 烟雾测试 | 7/7 success | RDKit 标准化/3D、ASE/EMT 能量、SciPy 反应网络、OpenFF AM1-BCC/参数化、Packmol 溶剂化 |
| 语义检索 | PASS | 114 个 Action 文档完成索引，状态为 `available` |
| 原生软件接口 | 41 pass、11 started/input-required、2 skip、2 timeout | 绝大部分软件完成真实启动；MATLAB/EasySpin 因许可证跳过；RMG/Arkane 的 CLI 帮助探测超过监督时限 |
| 精确锁解析 | 6/6 parse-ok | 六份 explicit lock 均通过 `mamba create --dry-run --file` |
| 重建脚本 | PASS | 两个 shell 脚本通过 `bash -n`；portable bootstrap 新目录安全检查和布局测试通过 |

“started/input-required”表示程序已真实启动并进入需要科学输入的阶段，不把缺少任务输入误判为安装失败。

## 6. 已知限制

1. **RMG/Arkane CLI 探测较慢**：`rmgpy` 模块和对应 runtime/profile 正常，但 `rmg.py --help` 与 `Arkane.py --help` 在受限烟雾测试中超过 60–180 秒。这是旧 RMG 启动/导入路径的已知性能问题，不影响本次 114 Action 注册和 profile 可用性判断，但尚不能声明这两个原生 CLI 的快速启动测试通过。
2. **许可证软件不能完全自动复现**：MATLAB/EasySpin、Gaussian、VASP 等仍依赖操作者许可证或已有受控资产；环境锁不会复制许可证和闭源程序。
3. **精确锁是平台特定的**：`*.explicit.txt` 仅面向 Linux x86-64；迁移到不同平台应使用 `environment.yml` 重新求解并重新验证。
4. **外部资源独立管理**：模型权重、赝势、闭源二进制和大型数据继续由 `.software_cache`、`.model_cache` 及资源注册表管理，不应打包进 Conda 环境。

## 7. 重建与切换命令

```bash
# 从可维护规格构建六个环境
bash chemistry_toolbox/scripts/build_merged_environments.sh all

# 在同平台按精确锁重放
bash chemistry_toolbox/scripts/build_merged_environments.sh --from-lock all

# 可选：把七个前缀整体放到其他磁盘
export RESEARCHCHEMBENCH_ENV_ROOT=/path/to/researchchem-envs

# 刷新精确锁
bash chemistry_toolbox/scripts/capture_merged_environment_locks.sh

# 验证
.envs/researchchembench/bin/python -m pytest -q
.tool_envs_merged/general-modern-openmpi5/bin/python \
  chemistry_toolbox/scripts/check_mcp_tools.py --smoke
.tool_envs_merged/general-modern-openmpi5/bin/python \
  chemistry_toolbox/scripts/verify_toolbox.py --smoke --no-write
```

## 8. 旧环境处理建议

当前仍保留：

- `.tool_envs/` 下 40 个环境；
- `.toolbox_env`；
- `.venv`；
- `.tool_envs_merged/` 下新建的 6 个环境。

本轮没有删除任何旧环境。建议用户确认本报告后，再执行一次磁盘目标核对和旧目录清单确认，然后单独进行删除；删除动作应与本次功能修改分开提交，便于审计和回滚。
