# 化学工具箱新旧版本差异

更新时间：2026-08-07

本文合并并替代原 `CHEMISTRY_TOOLBOX_ADJUSTMENT_LOG.md` 与
`CHEMISTRY_TOOLBOX_SOFTWARE_EXPANSION_LOG.md`。这里只保留最终差异，不再记录逐次报错、
临时测试和调试过程。当前代码、环境定义和缓存 README 是最终事实来源。

## 1. 总体变化

| 项目 | 整理前 | 当前版本 |
|---|---|---|
| 软件范围 | 混有不可用商业软件、缺依赖软件和仅有解析器的软件 | 不可启动的软件已移出活动清单；请求清单为 57 个已配置软件和 1 个 QCSchema 规范 |
| 工具接口 | Action、原生命令和软件说明之间对应关系不完整 | 形成“typed Action -> 可检索原生手册 -> 受控执行/分析接口”三层结构 |
| 软件扩展 | 十个评测方向存在结构搜索、非谐声子、自由能、多参考电子结构等缺口 | 新增并适配 10 个软件、27 个唯一 Action；另增强 4 个复杂计算 Action 和 5 个通用分析 Action |
| 运行配置 | 部分软件依赖、PATH、动态库和 MPI 组合不完整 | 每个软件由 runtime profile 声明命令、环境、库路径、限制和探针 |
| 软件文档 | 软件用法与 Action 目录相互独立 | 原生手册可检索，并显示软件支持的 Action、输入输出、正常结束标志和限制 |
| 缓存结构 | 安装包、源码、安装产物、测试证据和运行缓存混放 | `.software_cache`、`.model_cache`、`.runtime_cache`、`.envs` 分工明确 |
| 可迁移性 | 存在本机绝对路径和隐式环境依赖 | 项目路径由环境变量和 profile 推导；目标机按环境锁和缓存清单重建 |

## 2. 新增并适配的软件

以下 10 项是相对旧工具箱真正新增的软件能力。容量为当前 `.software_cache` 中对应软件
的实际占用，包含该软件的安装、源码、包、验证和状态文件，不包含共享 `.envs`。

| 软件 | 固定版本 | 新增能力 / Action | 当前缓存占用 |
|---|---|---|---:|
| AIRSS | 0.9.3 | 晶体候选生成、晶体格式转换（2） | 54.9 MiB |
| TDEP | 25.03 | 有效力常数拟合、热位移构型、温度相关声子色散（3） | 251.9 MiB |
| ACPYPE | 2023.10.27 | 小分子拓扑生成、AMBER 到 GROMACS 拓扑转换（2） | 1.09 GiB |
| pmx | develop `0dd5f0a` | 炼金突变、混合拓扑、配体原子映射（3） | 827.6 MiB |
| gmx_MMPBSA | 1.6.5 | 端点结合自由能、能量分解、结果汇总（3） | 607.0 MiB |
| SISSO | 3.5 | 稀疏符号描述符发现、评估、汇总（3） | 2.93 GiB |
| gplearn | 0.4.3 | 符号回归、跨随机种子稳定性、结果汇总（3） | 15.2 MiB |
| VASPKIT | 1.5.1 | VASP K 点网格、带隙提取，并扩展晶体对称性分析（2 个新 Action） | 488.9 MiB |
| PyFrag | 2019 / 1.0.0 | Activation Strain 分析、汇总、闭合校验（3） | 55.4 MiB |
| BAGEL | 1.2.2 | 多参考态能量、核梯度、非绝热耦合向量（3） | 518.0 MiB |

这 10 项合计约 **6.77 GiB** 软件缓存，对应 **27 个唯一 Action ID**。旧日志中的
“31”是定向回归测试数量，不是 Action 数；旧日志中的“约 13 GB”是缓存和环境重构前的
历史估算，不再作为当前容量依据。gmx_MMPBSA 的独立 Conda 环境及其他共享环境不计入上表。

## 3. 原有软件的修复与能力增强

| 软件或数据源 | 相对旧版本的变化 | 当前边界 |
|---|---|---|
| RMG / Arkane | 固定兼容依赖，CLI、最小机理生成和热化学计算可运行 | 长任务仍应使用显式资源上限 |
| AiiDA | 增加 SQLite profile，本地同步 workflow 可运行 | 未配置 RabbitMQ/daemon，不影响本地同步使用 |
| CENSO | 建立独立 runtime，使用 ORCA、xTB 和匹配 OpenMPI | 不再依赖已移除的 TURBOMOLE |
| SHARC | 补齐 Python/接口依赖，修复空 restart 列表，加入完整短轨迹 Action | 已验证 ORCA 接口和多 seed 轨迹；短 smoke 不代表统计收敛 |
| Newton-X | 配置 ORCA、OpenMPI 和 CIOVERLAP | 已验证短 TDDFT 非绝热轨迹 |
| Wannier90 | 用源码构建替代会段错误的二进制 | 已验证 QE -> pw2wannier90 -> Wannier90 链路 |
| Yambo | 配置 QE `p2y` 数据链，并增加真实最小 GW/BSE Action | 最小 smoke 不替代空带数、k 点和截断收敛 |
| LOBSTER | 补齐 QE-COHP 测试链和输出解析证据 | 软件本身的获取仍遵循其分发条件 |
| Critic2 | 完成源码构建和 QTAIM 路径 | 可通过原生命令和对应分析接口使用 |
| Multiwfn | 配置 noGUI 波函数分析 | 不依赖交互式 GUI |
| VESTA | 补齐 GTK/Cairo/OpenGL 运行库 | 可命令启动；交互 GUI 仍需要显示环境 |
| KinBot | 修复本地 NWChem 调度、输出判定和 Python 3 模板 | `explore_reaction_network` 已验证非空 PES 路径 |
| PubChem | 取消代理变量，直接访问 PUG REST | 6 个联网 Action 已验证 |
| Materials Project | 增加超时后的退避重试 | 仍受外部服务和凭据状态影响 |
| Catalysis Hub | 接入 API key，并增加认证/重试处理 | API key 只放本地环境文件，不进入 Git |
| NIST WebBook | 保留受控参考数据查询 Action | CCCBDB 无稳定 API，未接入且不是执行型软件 |

原有复杂路线新增 4 个 Action：

- Yambo：`calculate_quasiparticle_corrections`、`calculate_bse_optical_spectrum`
- SHARC：`propagate_nonadiabatic_trajectory`
- KinBot：`explore_reaction_network`

## 4. 十个方向补充的通用分析能力

新增 5 个不替代上游科学计算的确定性分析/质量门 Action：

| 方向 | Action | 用途 |
|---|---|---|
| 反应机理与选择性 | `analyze_post_transition_state_trajectory_ensemble` | 统计产物分支、回穿、失败率和置信区间 |
| 表面吸附 | `calculate_adsorption_energy` | 按显式参考态和化学计量计算吸附能 |
| 激发态与光化学 | `analyze_nonadiabatic_trajectory_ensemble` | 统计态布居、跃迁和失败轨迹 |
| 高压相稳定性 | `construct_pressure_enthalpy_phase_diagram` | 构建稳定相区间并插值相变压力 |
| 声子稳定性 | `assess_phonon_stability` | 区分真实动力学不稳定与容差内小虚频 |

其余方向复用已有的构象/热化学、QTAIM/成键、主方程、自由能和描述符 Action，避免按
软件重复实现同一种科学操作。

## 5. 从活动工具箱移除或未接入的项目

已移除：MATLAB、EasySpin、Q-Chem、Molpro、TURBOMOLE、CASTEP、CRYSTAL、WIEN2k、
OpenEye、Schrodinger Suite。工具箱可能仍保留通用输出解析能力，但不再声称可以启动这些软件。

未接入：

- NIST CCCBDB：无稳定公开 API，参考数据查询由 NIST WebBook 覆盖。
- MultiWell、Progdyn：未确认可自动部署和再分发的许可条件，因此没有注册 runtime 或 Action。
- CALYPSO、USPEX、CFOUR、FHI-aims：需注册或签署许可，未自动安装。
- NBO、AMS/ADF、TeraChem、COSMOtherm 等收费软件：只作为能力缺口记录，未加入活动工具箱。

## 6. 当前结构与规模

当前三层结构为：

1. **Action 层**：150 个公开 Action，使用显式输入 schema、资源限制、结果结构和质量门。
2. **软件知识层**：原生软件手册支持语义检索，并把软件命令、Action、输入输出和限制关联起来。
3. **执行层**：92 个 BackendSpec 负责受控调用原生软件或确定性分析，不暴露任意 shell runner。

当前还包括 50 个 runtime profile；软件缓存管理清单为 37/37 installed，受管资源探针为
27/27 passed。最近一次完整工具箱回归为 **495 passed、1 skipped**。

## 7. 缓存与迁移差异

- `.software_cache`：软件安装产物、安装包、源码、共享资源、构建状态和验证证据。
- `.model_cache`：只保存模型权重、来源和校验信息。
- `.runtime_cache`：语义索引、Matplotlib、Mesa、pip 等可删除并重建的运行缓存。
- `.envs`：由仓库中的环境 YAML、requirements 和 lock/freeze 重建的执行环境。

软件缓存不是跨任意系统的通用二进制发行包。迁移到兼容的 Linux、CPU 架构和 libc 系统时，
仍应按 [`.software_cache/README.md`](../../.software_cache/README.md) 重建或验证环境；缓存管理架构见
[`SOFTWARE_CACHE_MANAGEMENT_V2.md`](SOFTWARE_CACHE_MANAGEMENT_V2.md)。项目不再依赖当前服务器的
绝对根路径，运行位置由 `RESEARCHCHEMBENCH_SOFTWARE_ROOT`、模型/运行缓存变量和 runtime profile 推导。
