# 论文复现任务修订与验证报告（2026-07-27）

## 1. 范围与结论

本轮检查并修订了 8 个论文复现任务：

- `PV_Protonation_Barrier_Trend_Reproduction`
- `PV_CC_CO_Pathway_Selectivity_Reproduction`
- `BaO_Phase_Crossover_And_5d_Bonding_Reproduction`
- `NHC_Adsorption_Decomposition_Bonding_Reproduction`
- `Heterobiaryl_PV_Reproduction_01_Protonation`
- `Heterobiaryl_PV_Reproduction_02_CC_Selectivity`
- `Heterobiaryl_PV_Reproduction_03_CC_vs_CO`
- `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step`

四个 Heterobiaryl 子任务与前两个 P(V) 任务共享同一套作者原始输出和热化学分析链，因此没有重复执行昂贵计算，而是用一套 P0/P1/P2 作者输出复算结果分别验证各任务结论。

修订后，8 个任务均可作为有明确证据边界的评估任务。这里的“可复现”包括三种模式：作者原始输出独立复算、真实新计算、公开论文数据的来源标注再分析。没有公开原始数据的结论不再被错误要求为 fresh calculation。

## 2. P(V) / Heterobiaryl 复现

### 数据与方法

论文作者在 Zenodo 1439888 公开了 P0、P1、P2 三套 Gaussian 频率输出和 ORCA DLPNO-CCSD(T) 单点输出。任务现已直接包含这三个官方归档，并通过 SHA-256、受限路径解压和文件清单校验。

使用 chemistry toolbox 的 `analyze_reaction_free_energy_profile` / GoodVibes 4.3.0 重新分析，条件为 353.15 K、1 M、Grimme 准谐波熵、DLPNO 单点修正，并显式传递 `--media ethanol`。

### 复算结果

| 状态 | Py-Py 第一步势垒 | Ph-Py 第一步势垒 | 单位 |
|---|---:|---:|---|
| P0 | 30.9134 | 37.3192 | kcal/mol |
| P1 | 19.8135 | 26.8607 | kcal/mol |
| P2 | 14.3004 | 25.5695 | kcal/mol |

P2 完整路径的准谐波相对自由能为：

- Py-Py：`0.000, 14.2937, -19.2054, -10.3901, -31.3526 kcal/mol`
- Ph-Py：`0.000, 22.3082, -12.8639, -9.3489, -35.1132 kcal/mol`

因此可以直接支持：

- 连续质子化将 Py-Py 偶联势垒从约 31 降至 20，再降至 14 kcal/mol。
- 三种质子化状态下 Py-Py 均比 Ph-Py 更有动力学优势。
- P2 路径的第一步 C-C 偶联为最高前向势垒，支持速率决定步骤判断。

### C-C 与 C-O 的证据边界

公开的 P2 作者归档包含 5 个 `TS-I`，结构审计显示它们都是 C-C 连接；没有 C-O 过渡态频率、IRC 或匹配的 DLPNO 输出。论文报告 C-C 为约 14 kcal/mol、C-O 为约 18 kcal/mol，但只能对 C-C 做作者输出复算。

因此两个 C-C/C-O 任务已改为混合证据任务：

- C-C：必须从公开作者输出重新计算，验证值为约 14.30 kcal/mol。
- C-O：18 kcal/mol 作为明确标注的论文公开比较值。
- 必须报告公开归档缺少 C-O 原始输出，禁止把文件名或构型标签当作 C-O 连通性证据。

## 3. BaO 高压相变与 5d 成键

### 真实计算结果

已完成并重新分析：

- 15 个 VASP PBE 相-体积点（B1、B8、dB2 各 5 个）。
- 10 个 B8/dB2 定体积内部坐标弛豫。
- Birch-Murnaghan EOS 拟合和压力焓交点计算。
- 2 个 LOBSTER 对照投影计算。

重新拟合得到：

- B1 -> B8：`6.023 GPa`
- B8 -> dB2：`28.909 GPa`

这复现了论文的 B1 -> B8 -> dB2 高压相序，且落在任务采用的合理区间 6-12 GPa 和 20-30 GPa 内。

### 不能等价 fresh 复现的部分

论文指出标准 LOBSTER 基组缺少碱土金属未占据 nd 轨道，采用 Sc 3d -> Ca、Y 4d -> Sr、La 5d -> Ba 的自定义投影。完整的 La-5d-on-Ba 基组文件未公开。

本地对照实算中，即使在 `lobsterin` 请求 Ba 5d，LOBSTER 实际仍只建立 `Ba 5s 6s 5p`。两次结果的最大 charge spilling 均为 3.95%，`ICOHPLIST.lobster` 哈希完全相同。因此不能把标准基组运行声称为论文的 5d 消融复现。

任务已改为：相变部分要求真实 VASP 计算；5d 部分要求审计论文公开的自定义基组映射、投影结果和任何本地运行实际实现的基组。fresh 5d 消融仅作为获得完整自定义基组后的可选扩展。

## 4. NHC/PdCu(111) 吸附

### 结构复算

chemistry toolbox 通过 pymatgen 解析论文 SI 的 NHC1/NHC4 周期结构，并从坐标直接计算最近周期性 Pd-C 距离：

| 系统 | 金属原子数 | 坐标复算 Pd-C | 论文 Pd-C |
|---|---:|---:|---:|
| NHC1 | 48 | 2.0570 Å | 2.061 Å |
| NHC4 | 36 | 2.0430 Å | 2.043 Å |

### 论文表格再分析

从论文 Table 3、Table 4 和 SI spilling 数据独立重算：

- `BE(NHC4) - BE(NHC1) = -1.1 kcal/mol`
- NHC1 总变形项：`0.68 + 1.61 = 2.29 kcal/mol`
- NHC4 总变形项：`0.86 + 1.16 = 2.02 kcal/mol`
- `ICOHP(NHC4) - ICOHP(NHC1) = -0.908 eV`
- `ICOBI(NHC4) - ICOBI(NHC1) = 0.276`

结论是 NHC4 具有更强的局部 Pd-C 成键指标，但总结合能仅比 NHC1 有利 1.1 kcal/mol。成对 ICOHP 不能等同于总吸附能，必须同时考虑表面/吸附体变形、横向作用及其他总能贡献。

完整 9x9x1 optPBE-vdW VASP-to-LOBSTER 重算成本较高，并非验证上述结构和表格结论所必需，现作为可选高预算扩展。

## 5. 工具箱修复

本轮发现并修复三个会影响这些任务的工具问题：

1. GoodVibes 后端新增 `method_spec.media_solvent` 到 `--media` 的映射，并注册到参数和后端规格。
2. VASP POTCAR 拼接只在源数据末尾没有换行时补换行，避免在多元素 POTCAR 数据集边界插入额外空行。
3. 周期结构文件对 `.vasp`、`.poscar`、`POSCAR`、`CONTCAR` 优先使用 pymatgen 解析，避免 pymatgen 运行环境缺少 ASE 时无法读取任务输入。

## 6. 任务修订原则

- 作者公开原始输出直接加入任务输入，并配置运行器自动校验和解压。
- 新计算值、作者输出复算值和论文公开值在任务文本、协议、rubric 和 ground truth 中分开标注。
- 删除“缺少公开输入却必须 fresh 计算”的判分要求。
- 对 BaO 自定义基组和 P(V) C-O 过渡态设置明确的资源边界与反伪造 gate。
- 保留昂贵全量计算为可选扩展，不再让它阻塞可验证的核心论文结论。

## 7. 验证状态

- 8 个任务均可通过 `TaskInfo` / ground-truth 模型加载。
- 8 个 input manifest 的文件大小和 SHA-256 全部匹配。
- 12 个作者归档引用（去重后 3 个文件）均通过 SHA-256 与 ZIP 内容检查。
- chemistry toolbox 与任务测试共 `42 passed`。
- `git diff --check` 通过。

## 8. 主要来源

- P(V) 作者计算输出：<https://zenodo.org/records/1439888>
- P(V) 论文开放全文：<https://pmc.ncbi.nlm.nih.gov/articles/PMC6362047/>
- BaO 论文开放稿：<https://escholarship.org/content/qt9zm8k4cq/qt9zm8k4cq.pdf>
- BaO 期刊页面：<https://onlinelibrary.wiley.com/doi/10.1002/chem.202501536>
- NHC/PdCu(111) 论文：<https://pubs.acs.org/doi/10.1021/acsomega.4c11197>

## 9. 复现产物

本轮最终数值摘要位于：

- `workspaces/previous_results/paper_reproduction_recovery_20260727/final_validation/pv_reproduction_summary.json`
- `workspaces/previous_results/paper_reproduction_recovery_20260727/final_validation/bao_reproduction_summary.json`
- `workspaces/previous_results/paper_reproduction_recovery_20260727/final_validation/nhc_reproduction_summary.json`

完整工具返回和原始计算目录保留在 `workspaces/previous_results/paper_reproduction_recovery_20260727` 与 `workspaces/previous_results/manual_reproduction_validation_20260727/bao`。
