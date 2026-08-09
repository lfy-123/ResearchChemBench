# Stage 03 软件覆盖筛选 R13 验证报告

日期：2026-08-10

## 目标

本轮只调整当前 V2 `Stage 03` 的软件清单和工具箱覆盖判定，不引入更强模型，也不改变
Stage 02 的计算化学内容判定。筛选策略以 precision 为优先：论文必要计算流程中只要存在当前
工具箱目录未收录的程序、扩展、服务或作者代码，即不作为 `software_covered` 放行；证据不足时
进入 `software_inventory_unconfirmed`，不默认放行。

## 修改内容

### 1. 强化模型输出合同

- 将 `program/library/service/extension/custom_code` 与方法、算法、模型、数据库和数据集分开。
- 提示词明确列出 RASSCF、QSAR、CCCDB、ChEMBL、VASPsol 等正反例。
- 软件、workflow 和 step 必须使用对象数组，禁止用字符串数组代替结构化清单。
- 对截断或结构错误响应执行紧凑重试；重试仅重排原响应，不重新猜测论文内容。
- 缩小证据和 prompt 上限，使 Qwen3-30B-A3B 的输入输出稳定落在 16k context 内。

### 2. 收紧确定性软件补漏规则

- 保留明确的 `software/program/code/library/module/extension` 实际使用证据，用于补回模型遗漏。
- VASPsol 始终作为 VASP 之外的独立扩展检查，不能因名称相似而映射到 VASP。
- 模型给出的 `normalized_hint` 不再作为工具箱覆盖依据；覆盖只由冻结的软件别名表确定。
- 支持 `ORCA 4.2.1` 等版本后缀归一化，但不将 QVina2 错映射到 Vina。
- 过滤 RASSCF、QSAR、GNN、PIP-NN、RPMD 等方法或模型名。
- 过滤 CCCDB、ChEMBL、ZINC、UniProt 等数据资源。
- 过滤 `Online program`、`color code`、`COORDINATIONNUMBER` 等版式短语或输入关键字。
- 修复 `Materials Studio package` 只抽到 `Studio` 的问题。
- 保留 TcESTIME 等明确命名的作者代码，并按 `custom_code` 审计。

### 3. 强制 workflow 与软件清单一致

模型可能在 workflow step 中写出软件，却漏填 `software_mentions`。现在每个 step 中命名的软件
都会按别名归一后合并进统一软件清单，再执行工具箱覆盖 gate。新增来源标记
`workflow_step_contract` 和告警 `workflow_software_promoted_to_inventory`。

本批次因此补回了 `pymatgen`、`MDTraj`、SO3krates、HMMER、AlphaFold-Multimer、
qiskit-nature 等遗漏项。前两者已在工具箱中，不改变通过结论；其余缺失项会维持淘汰。

## 测试过程

### 重点 16 篇

重点样本最终为 2 篇通过、14 篇淘汰：

- 通过：`paper_2b5f254d7a98422b`（ORCA、OpenMolcas、Multiwfn）；
  `paper_e300e76b3b6d1452`（VASP，论文中的 PIP-NN/RPMD 是模型和方法，不冒充软件）。
- 淘汰项均有明确缺失程序，包括 fpocket、Smina、MolVoxel、PharmacoNet、sGDML、Q-Chem、
  DP-GEN、HoleMass CPMD、QVina2、Mordred、LightGBM、VASPsol、qiskit 和 TcESTIME 等。

### 全部 76 篇增量复跑

输入为 2000 篇历史任务中通过计算内容阶段的 76 篇论文，部署模型仍为
`Qwen3-30B-A3B-Instruct-2507`。最终产物位于：

`data_pipeline/runs/v2_stage03_r13g_validated76_20260810/`

| 判定 | 数量 | 比例 |
|---|---:|---:|
| `software_covered` | 18 | 23.7% |
| `core_software_uncovered` | 52 | 68.4% |
| `software_inventory_unconfirmed` | 6 | 7.9% |
| `processing_failed` | 0 | 0% |

旧结果曾把仅出现 `Online` 的 `paper_97070aa2ed98af38` 判为软件不覆盖；修复后该论文进入
`software_inventory_unconfirmed`，因为正文没有给出实际 MD/自由能软件。这是预期的保守结果，
不会误放行。

18 篇通过论文的必要软件均能由当前冻结目录解析。通过项中 VMD 等只用于可视化的非必要软件
不会阻断核心计算任务；通用后处理允许由工具箱第三层 Python 完成。Stage 03 只判断软件目录
覆盖，不替代后续 Stage 05 对完整科研流程、输入、结果和任务可构建性的审查。

## 验证

- 重点软件规则和合同测试：49 passed。
- 数据管线完整测试：302 passed，8 subtests passed；V2 定向测试为 165 passed。
- 最终 76 篇运行：76/76 完成，模型缓存命中 76/76，规则和 gate 使用最新代码重新计算。
- 最终结果中未再出现 Online、Color、UniProt、CCCDB、RASSCF、QSAR、GNN 或
  COORDINATIONNUMBER 作为软件淘汰理由。

## 已知边界

- 软件目录判定依赖 `toolbox_capabilities.json` 和 `software_aliases.json` 的冻结快照；新增软件后
  必须重新同步快照再运行。
- 作者没有报告所用程序时，本阶段保持 `software_inventory_unconfirmed`，不会依据软件常识猜测。
- 论文自定义模型或可用 Python 重写的通用后处理不会仅因没有独立软件名而淘汰，后续
  Stage 05 仍需判断它们是否能形成完整、可执行且有科学意义的任务。
