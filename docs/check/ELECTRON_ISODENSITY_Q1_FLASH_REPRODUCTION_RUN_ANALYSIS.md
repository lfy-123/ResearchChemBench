# Electron Isodensity Q1 Flash 复现运行与工具箱修复报告

日期：2026-07-24  
范围：仅 `Electron_Isodensity_Reproduction_01_Method_Selection`。按照用户最新要求，未提交 Q2–Q5。

## 1. 最终结论

- 当前化学工具箱已经能够端到端完成 Q1 所需的真实计算链：ORCA 相关电子密度计算、ORCA 密度导出、Multiwfn 等电子密度面面积扫描以及统计分析。
- 最终 DeepSeek V4 Flash 运行完成了 12 次 ORCA 密度计算、12 次密度导出和 12 次 Multiwfn 扫描；评估器未报告任何 `objective_issue_flags`。
- Q1 可行性分类为 `solvable`。
- 最终运行得分为 93/100。扣分来自模型没有填写 `report/tool_trace.jsonl`，以及 `quantum_calculations.csv` 中部分便捷路径没有对应真实导出路径；这两项属于智能体交付和溯源质量问题，不是化学工具箱计算失败。
- 在当前 ORCA 6.1.1 兼容复现条件下，真正导出的 CCSD MDCI 密度作为 CCSD(T) 密度代理时，三分子子集没有恢复论文中 DSD-PBEP86 最优的结论。最终计算得到 B3LYP 的平均 MUPE 最小。该差距需要解释为 CCSD 代替 CCSD(T)、WFN 与 cube 表示差异、软件版本以及有限子集共同造成的不确定性，不能伪装为完全数值复现。

## 2. 新增 Action 的通用性检查

新增的三个 Action 均表示通用科学行为，没有论文、任务或分子专用分支。

| Action | 通用科学语义 | 显式输入 | 当前后端边界 | 是否含 Q1 特判 |
|---|---|---|---|---|
| `calculate_correlated_electron_density` | 对任意分子计算并保留指定电子密度 | 结构、方法、基组、电荷、自旋、密度类型、SCF 和资源参数 | ORCA；已验证 `scf`、`relaxed_mp2`、`unrelaxed_ccsd` | 否 |
| `export_electron_density_grid` | 将已计算密度导出为后处理格式 | `ElectronDensityResult`、密度来源、WFN/WFX/cube | ORCA `orca_2aim`/`orca_plot` | 否 |
| `calculate_electron_isodensity_surface` | 对任意兼容波函数或密度网格计算多个等密度面的面积和体积 | WFN/WFX/FCHK/MWFN/Molden/47/cube、cutoff 列表、网格间距 | Multiwfn 2026.7.15 | 否 |

源码中没有 DOI、`ISO-M1`～`ISO-M3`、论文参考数值、固定 cutoff 网格或“选择 DSD-PBEP86”逻辑。测试结构使用通用水分子；论文方法和执行路线只存在于 reproduction task 数据中。

## 3. 修复的工具箱问题

### 3.1 ORCA CCSD/MDCI 长路径崩溃

现象：`calculate_correlated_electron_density` 在深层评估工作区内使用完整绝对输入路径调用 ORCA。ORCA 6.1.1 将该路径传播到 MDCI 模块内部基名，随后异常退出并生成 core 文件。

修复：在计算目录作为 `cwd` 的前提下，使用短且显式的相对输入路径 `./job.inp`。不能使用裸 `job.inp`，因为当前 ORCA 构建不接受没有目录分量的输入名。

验证：真实 ethane CCSD/def2-TZVPD Action 成功，能量为 `-79.686552386003 Eh`，并生成 GBW、`job.densities` 和 `job.densitiesinfo`。

提交：`7bb5aca Fix ORCA CCSD action path crash`

### 3.2 MDCI 密度导出缺失元数据并错误改名

现象：MDCI cube 导出只复制 GBW 和 `.densities`，没有复制 `.densitiesinfo`；同时将文件改名为 `density.*`。ORCA 的 GBW/密度元数据仍引用原始 `job.*` 基名，导致 `orca_plot` 报告 `CANNOT OPEN FILE ./job.densitiesinfo`。

修复：将 `job.gbw`、`job.densities`、`job.densitiesinfo` 作为一个不可拆分的文件束保留同一基名，再调用 `orca_plot job.gbw -i`。

验证：

- 真实 ethane MDCI cube 导出成功；
- 最终 Flash Q1 运行的三次 MDCI cube 导出全部成功；
- 未再出现缺失 `densitiesinfo` 或基名错误。

提交：`cc9ec92 Preserve ORCA MDCI density export bundle`

### 3.3 回归测试

- `chemistry_toolbox/tests/test_electron_density_surface_actions.py`：6 项测试全部通过；
- 包含短相对 ORCA 输入路径测试；
- 包含完整 MDCI 密度文件束与原始基名测试；
- 包含真实 ORCA → WFN → Multiwfn Action 链测试；
- 核心三个通用 Action 的初始实现提交为 `b0d32e6 Add typed electron density surface actions`。

## 4. 三轮 Q1 运行

Agent 与 judge 均为 `deepseek-v4-flash`，配置来自 `config.local.env`，提交入口为 `scripts/submit_electron_isodensity_reproduction.sh`。

| 轮次 | Run ID | 时长 | 分数 | 关键工具箱问题 | 处置 |
|---|---|---:|---:|---|---|
| 1 | `..._20260724_050910_21dd28` | 1032.160 s | 100 | 工具箱内置标准化 CCSD Action 在 MDCI 前崩溃；模型改用 native ORCA | 修复长绝对路径问题；该 100 分不能证明标准化 Action 无缺陷 |
| 2 | `..._20260724_053537_fc9117` | 3399.157 s | 96 | CCSD Action 已成功；MDCI 导出缺少 `densitiesinfo` 且文件束改名错误 | 修复 MDCI 三文件束和基名 |
| 3 | `..._20260724_063529_82fd84` | 2994.208 s | 93 | 无客观工具箱问题 | 作为最终修复后验证运行 |

最终运行目录：

`workspaces/electron_isodensity_reproduction/agent_deepseek-v4-flash__judge_deepseek-v4-flash/cli_runs/batch_20260724_063529_624364/Electron_Isodensity_Reproduction_01_Method_Selection_opencode_20260724_063529_82fd84`

## 5. 最终运行轨迹审计

### 5.1 成功的真实科学调用

| Action | 成功次数 | backend | 说明 |
|---|---:|---|---|
| `calculate_correlated_electron_density` | 12 | ORCA 6.1.1 | PBE/B3LYP/DSD-PBEP86/CCSD × ISO-M1～M3 |
| `export_electron_density_grid` | 12 | ORCA 6.1.1 | DFT/双杂化导出 WFN；MDCI 导出 cube |
| `calculate_electron_isodensity_surface` | 12 | Multiwfn 2026.7.15 | 每个方法/分子完成 18 个 cutoff |
| `submit_analysis_program` | 2 | core runtime | 统计与结构化报告整理 |

### 5.2 非成功调用的归因

| 调用 | 次数 | 原因 | 是否工具箱 bug |
|---|---:|---|---|
| `calculate_correlated_electron_density` `invalid_request` | 4 | Flash 将布尔参数传成字符串等 schema 错误 | 否，校验正确拒绝 |
| `calculate_correlated_electron_density` `failed` | 1 | 16 核、总内存 16 GB 被映射为每进程 1000 MB；ORCA 最低需要 1001.6 MB，随后模型用 8 核/32 GB 成功重试 | 否，属于资源组合不合理 |
| `export_electron_density_grid` `invalid_request` | 1 | 模型尝试把 MDCI 密度导出为 WFN；Action 正确阻止把普通 GBW 参考轨道误当成 MDCI 密度 | 否，科学防错规则生效 |

### 5.3 时间成本

最终运行约 49.9 分钟。主要原因不是 Action 阻塞，而是 Flash 对 ISO-M1、ISO-M2 和 ISO-M3 全部执行 CCSD，并对一次内存不足进行重试。协议允许在较大参考不可负担时只保留最小分子的高阶参考，因此当前耗时反映了模型的资源/停止策略，不是 Q1 完成所必需的最低成本。

## 6. 最终计算结果与论文差距

最终报告给出的三分子平均 MUPE 为：

| 方法 | 平均 MUPE（相对当前 CCSD 代理） |
|---|---:|
| B3LYP | 0.121% |
| PBE | 0.329% |
| DSD-PBEP86 | 0.784% |

因此最终运行没有恢复论文中 DSD-PBEP86 最接近 CCSD(T) 的方法选择。需要保留以下限制：

1. ORCA 6.1 不提供真正的 CCSD(T) 一粒子密度，本任务使用 unrelaxed CCSD MDCI 密度；
2. DFT/双杂化密度通过 WFN 输入 Multiwfn，而 CCSD 密度通过 cube 输入，表示与离散化路径不同；
3. 论文软件版本为 ORCA 5.0.3，当前为 6.1.1；
4. 可见任务只有三个分子，不是论文完整集合；
5. 当前比较基组为 def2-TZVPD，而论文生产密度使用 DSD-PBEP86/def2-QZVPD。

工具箱现状应表述为：能够执行 Q1 规定的兼容复现路线并产生真实可审计结果，但不能声称当前 ORCA 代理与混合表示路径已经实现论文 CCSD(T) 密度比较的严格数值同一性。

## 7. 复现 Q1 与自主科研 Q1 的区别

| 维度 | 自主科研 `Electron_Isodensity_01_Method_Selection` | 复现 `Electron_Isodensity_Reproduction_01_Method_Selection` |
|---|---|---|
| 评估目标 | 在不给方法和路线的情况下，自主设计电子密度方法选择研究 | 按论文重建的方法层级和流程，检验能否重新执行论文复现 |
| `task_mode` | `open_discovery` | `guided_reproduction` |
| 任务指令 | 从中性分子身份出发，自主生成结构、选择候选方法/高阶参考、cutoff 和停止策略；禁止寻找源论文 | 明确要求用论文方法层级，在 ISO-M1～M3 上比较 PBE、B3LYP、DSD-PBEP86 与可行 CCSD(T) 参考，基组为 def2-TZVPD |
| 方法披露 | `none` | `paper_reconstructed_protocol` |
| 路线披露 | `none` | `paper_execution_route` |
| 分子身份 | ethane、furan、pyridine；SMILES、式、原子数、电荷和多重度 | 完全相同 |
| 三维结构 | 不提供；智能体必须生成并处理构象 | 提供论文 Supplementary Data 2 的三个公开 XYZ 构象 |
| 构象生成要求 | `structure_or_conformer_generation` 为必需 | 非必需；主复现路线直接使用提供的作者构象 |
| 软件信息 | 不规定 | 给出 ORCA 5.0.3 或兼容新版、Multiwfn 及版本兼容说明 |
| 方法层级 | 智能体自主选择至少三种可负担方法和一个高阶参考 | 明确 PBE/B3LYP/DSD-PBEP86/CCSD(T)，并说明 ORCA 6.1 下以 CCSD unrelaxed density 兼容替代 |
| 基组与双杂化设置 | 智能体自主选择并论证 | 给出 def2-TZVPD 比较层级，以及 DSD-PBEP86 生产设置的 def2-QZVPD、辅助基组、D3BJ、NoFrozenCore、PModel、relaxed density 等论文信息 |
| cutoff 路线 | 不提供；只要求多于一个 cutoff | 明确 0.0008–0.0025 au、步长 0.0001、网格间距 0.1 |
| 输入模板 | 无 | 提供 ORCA、ORCA 6 兼容模板、CCSD 密度模板、orca_plot 和 Multiwfn 菜单模板 |
| 工作流要求 | 无预设路线 | 提供 `workflow_requirements.json`，列明构象验证、方法矩阵、密度导出、完整 cutoff 网格和参考比较 |
| 作者计算结果 | 不提供 | 同样不提供；只有方法/路线和原始构象，不含作者能量、波函数、表面积或参考答案 |
| 智能体自由度 | 高：结构、软件、方法、基组、cutoff、参考层级和停止路径均需自主决定 | 中低：执行路线已给定，主要考察正确调用工具、版本适配、失败修复和结果解释 |
| 主要能力测量 | 科研问题分解、方法设计、证据选择和自主停止 | 协议理解、软件执行、参数忠实度、版本兼容和复现审计 |
| 输出文件与评分 rubric | 与复现任务相同 | 与自主任务相同 |

两类任务的关键边界是：复现任务披露“怎么做”，但仍不提供作者算好的答案；自主科研任务只给“研究什么”和原始分子身份，要求智能体自己决定“怎么做”。
