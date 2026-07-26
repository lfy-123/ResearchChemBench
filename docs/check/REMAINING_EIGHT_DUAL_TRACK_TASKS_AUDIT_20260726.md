# 剩余八个双轨科研任务整理与可行性审计

日期：2026-07-26

## 1. 范围与结果

本次以已经完成的 GEOM 和 Electron Flexible 两对任务为模板，整理以下四对、共八个任务：

| 科学问题 | 自主科研任务 | 论文复现任务 |
|---|---|---|
| P(V) 质子化与势垒趋势 | `PV_Protonation_Barrier_Trend` | `PV_Protonation_Barrier_Trend_Reproduction` |
| BaO 高压相变与 5d 成键 | `BaO_Phase_Crossover_And_5d_Bonding` | `BaO_Phase_Crossover_And_5d_Bonding_Reproduction` |
| P(V) C-C/C-O 竞争选择性 | `PV_CC_CO_Pathway_Selectivity` | `PV_CC_CO_Pathway_Selectivity_Reproduction` |
| NHC/PdCu(111) 吸附与成键 | `NHC_Adsorption_Decomposition_Bonding` | `NHC_Adsorption_Decomposition_Bonding_Reproduction` |

八个任务均已迁移到当前 `dual_axis_100`：

```text
最终分数 = 科学结论分 C × 科研过程分 P / 100
```

- 每个任务有三条独立科学结论，总计 100 分；
- 自主科研和论文复现分别使用对应的 100 分过程 rubric；
- 旧的单项结论封顶和 `rubric_100` 已移除；
- 每个任务指令均增加在服务器资源允许时并行独立计算、充分使用 CPU 和内存的要求。

## 2. 各任务整理结果

### 2.1 P(V) 质子化势垒趋势

自主科研版保持方法隐藏，只提供 P0/P1/P2 的九个未优化反应物种子、分子身份、原子映射和实验条件。其三条隐藏结论为：

1. 势垒顺序为 P0 > P1 > P2；
2. 第一次质子化造成较大降幅，第二次继续降低且幅度较小，论文尺度约为 10 和 6 kcal/mol；
3. 三条反应总体均强放能，质子化主要改变动力学势垒，而不是显著改变反应热力学。

复现版保留论文重建方法：Gaussian `ωB97XD/6-31+G(d)/SMD(ethanol)` 几何与频率、ORCA `DLPNO-CCSD(T)/cc-pV(DT)Z` 口径单点，以及 GoodVibes 353.15 K、1 M 热化学。三条结论分别检查势垒顺序、30/20/14 kcal/mol 及其降幅、-39/-37/-38 kcal/mol 反应自由能尺度。

当前限制：候选集合没有经过 Gold Run 证明能形成三个完全可比的闭合主路径。任务结构已正确，但正式排名前仍需专家完成 P0/P1/P2 的 reactant–TS–product 对齐和新计算。

### 2.2 BaO 高压相变与 5d 成键

自主科研版只提供三个不透明 BaO 晶体候选和 0–80 GPa 范围，不公开 B1/B8/dB2 标签、体积网格、赝势和论文相变压力。三条隐藏结论为：

1. 相稳定顺序 B1 -> B8 -> dB2；
2. 两个交叉位于约 8–10 GPa 和 25 GPa；
3. 同一波函数上的投影对照支持 Ba 5d-O 成键对致密相的选择性贡献。

复现版提供三相体积网格、PBE/600 eV/VASP 设置、相应 k 点、EOS 路线，以及 LOBSTER 有/无 Ba 5d 的同波函数对照方法。评分分别检查相序、两个相变压力和投影/成键结论。

当前工具箱可通过周期 Action 运行 VASP，并允许直接原生执行 VASP/LOBSTER；LOBSTER 公共 Action 负责解析 COHP/PDOS 和 spilling。缺少专门的 LOBSTER 运行 Action 不再被视为客观不可执行，但正式发布前仍需完整 Gold Run 校准计算成本和压力容差。

### 2.3 P(V) C-C/C-O 路径选择性

自主科研版只提供三个未优化 P2 反应物种子、原子映射、酸性乙醇条件和四条实验约束，不提供产物、路径端点、TS、软件路线和论文势垒。三条隐藏结论为：

1. C-C 和 C-O 两条路径均得到有效且可比的计算证据；
2. C-C 动力学占优，C-O 势垒高约 4 kcal/mol；
3. C-O 是可达但受抑制的次要路径，而不是完全不可能。

复现版提供候选结构、Gaussian/ORCA/GoodVibes 方法以及 pysisyphus 路径搜索路线。已修正原协议中的后端错误：xTB 6.7 不支持 `ALPB ethanol`，因此低成本路径搜索改为显式的 `ALPB methanol` 近似，正式势垒仍必须采用论文规定的 ethanol 高层级口径。

当前限制：可见候选尚未由专家验证为一一对应的主 C-C/C-O 闭合路径。工具后端可以搜索、TS、频率、IRC、单点和热化学，但正式排名前仍需端点映射与完整路径 Gold Run。

### 2.4 NHC/PdCu(111) 吸附、分解与成键

自主科研版只提供两套匹配的洁净 PdCu(111) 表面和两个孤立 NHC 配体种子，不提供吸附位点或论文吸附结构。三条隐藏结论为：

1. NHC4 总体上只比 NHC1 略强吸附；
2. NHC4 的局域 Pd-C 成键指标更强；
3. 表面/配体形变和参考态贡献削弱总体吸附能差，因此局域键强度不能单独解释吸附能。

复现版提供论文吸附起始结构、匹配洁净表面、孤立配体、optPBE-vdW 设置、冻结片段能量定义和 LOBSTER 分析路线。三条结论分别检查吸附能及排序、Pd-C 距离/ICOHP/ICOBI 排序，以及闭合的形变—相互作用能量分解。

当前工具箱没有专用吸附放置和逐原子 Selective Dynamics Action，但允许智能体直接编写 pymatgen/ASE 程序并生成原生 VASP 输入；VASP 和 LOBSTER 均有原生运行入口。因此这是 Action 便利性不足，不是软件能力完全缺失。正式发布前仍需要一次吸附搜索、约束弛豫、匹配参考、分解和 LOBSTER 的 Gold Run。

## 3. 数据边界检查

| 模式 | 可见内容 | 明确隐藏内容 |
|---|---|---|
| 自主科研 | 科学问题、原始身份/结构、必要条件和实验约束 | 论文软件路线、固定参数、作者中间体、TS、优化吸附结构和论文数值 |
| 论文复现 | 原始/候选结构、论文重建方法、工作流和验证门槛 | 作者完成的量化输出、能量、势垒、相变压力、成键数值和最终答案 |

八个任务的输入目录均为正常文件，不含 ZIP、符号链接或完成的 `.log/.out/.gbw/.wfn/.WAVECAR` 结果。输入 manifest 记录每个文件的大小和 SHA-256，隐藏 ground truth 保存 manifest 哈希。

## 4. 验证

- 八个任务共 44 个 JSON 文件全部解析成功；
- 每个任务的科学结论分合计 100，过程分合计 100；
- 自主科研输入泄漏测试、复现数值隐藏测试、manifest 哈希和目录合同测试通过；
- 任务、评分、schema 回归选择：`28 passed`；
- `git diff --check` 通过；
- 全仓库测试仍存在与本次任务无关的既有失败：提交脚本 dry-run 未打印测试要求的模型名称。

## 5. 发布建议

| 任务对 | 当前建议 |
|---|---|
| P(V) Protonation | 保持 pre-release；先完成三质子化状态闭合路径 Gold Run |
| BaO | 可进行 native-execution pilot；完成 VASP EOS 与 LOBSTER Gold Run 后发布 |
| P(V) C-C/C-O | 保持 pre-release；先锁定两条可比端点、TS 与连接关系 |
| NHC adsorption | 可进行 native-execution pilot；完成吸附搜索和能量分解 Gold Run 后发布 |

本次完成的是任务结构、输入边界、评分和已知参数兼容性整理。未通过放宽结论要求掩盖尚未完成的专家参考计算；在 Gold Run 完成之前，相关状态仍明确保留在隐藏 feasibility baseline 中。
