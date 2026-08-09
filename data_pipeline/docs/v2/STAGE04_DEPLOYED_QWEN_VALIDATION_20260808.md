# Stage04 部署 Qwen 验证报告

更新时间：2026-08-08

## 验证设置

- 模型：`Qwen3-30B-A3B-Instruct-2507`，H200 单卡，经 rlaunch + vLLM 部署；
- prompt：`v2-stage04-software-inventory-20260808-r11-unbiased-software-extraction`；
- 输入：16 篇 Stage03 通过论文，每篇正文和一份已知 SI，共 32 个 Stage02 GROBID 文档；
- 并发：4；`max_tokens=6144`；
- Softcite：复用前次同一批论文已保存的原始 Softcite mentions，未重新调用 Softcite 服务；
- MinerU：关闭，本次只验证 Stage04 软件清单和覆盖判定；
- 模型 cache：全新目录，16 次请求全部 `cache_hit=false`。

先执行 r10 真调用确认三层软件判定，再针对 catalog 对模型抽取的支持状态偏置执行 r11 真调用。r11
不向模型提供候选工具箱软件表，模型只抽取实际使用软件，确定性 resolver 再依据活动 backend catalog
判定覆盖。

## 最终结果

```text
papers:                         16
software_covered:                3
core_software_uncovered:        10
software_inventory_unconfirmed:  3
processing_errors:               0
人工金标逐篇一致率:              16/16
```

| paper_id | 人工金标 | r11 部署模型结果 | 关键依据 |
|---|---|---|---|
| `paper_03db136b9dfeeae1` | `software_inventory_unconfirmed` | 一致 | 核心 continuum/MHC 实现未命名 |
| `paper_1027f6b6495227bb` | `core_software_uncovered` | 一致 | TURBOMOLE 缺失 |
| `paper_229398bc7d4dd935` | `core_software_uncovered` | 一致 | Molpro 缺失 |
| `paper_2d5323da0eb4aeee` | `software_covered` | 一致 | Materials Project、VASP、TDEP 均存在 |
| `paper_3d1ec7be672a5bac` | `core_software_uncovered` | 一致 | Turbomole、Tinker-HP 等缺失 |
| `paper_4b4df409feb16caa` | `core_software_uncovered` | 一致 | ChemShell、DL_POLY 等缺失 |
| `paper_576b22eb9fbcfdef` | `core_software_uncovered` | 一致 | PySAGES、通用 ASE 缺失 |
| `paper_5b16a392cdac5456` | `software_inventory_unconfirmed` | 一致 | 回归实现未命名 |
| `paper_6797331f736c6743` | `software_covered` | 一致 | CP2K 存在，Action 缺失不再拒绝 |
| `paper_67a927de6363bbb5` | `software_covered` | 一致 | Gaussian、Multiwfn 均存在 |
| `paper_70fb431035f2bf9a` | `software_inventory_unconfirmed` | 一致 | ai-GCMC 实现未命名 |
| `paper_71e1f79eeb72bc40` | `core_software_uncovered` | 一致 | ChemShell、Turbomole、DL_POLY 缺失 |
| `paper_804bc3f1be133124` | `core_software_uncovered` | 一致 | VASPsol 扩展缺失 |
| `paper_921f3425c5e8797d` | `core_software_uncovered` | 一致 | PERTURBO 缺失 |
| `paper_96a0a765d1651f87` | `core_software_uncovered` | 一致 | 必需 in-house code 不可用 |
| `paper_b2ba8ce344632b5d` | `core_software_uncovered` | 一致 | WWL-GPR/Scikit-learn 工作流未覆盖 |

16 个请求均为 `finish_reason=stop`，没有 truncation retry。模型调用累计耗时约 352 秒；4 并发下从
首个请求开始到最终产物约 98 秒。

## 运行中发现并修正的问题

1. r10 prompt 向模型提供候选 catalog 后，模型会把不在候选表的 TURBOMOLE、ChemShell 等写入
   `unresolved`，而不是正式软件清单。r11 删除候选表，明确 support-agnostic extraction。
2. Stage04 不再让模型抽取资源和复杂度字段；这些字段固定为空，资源不参与本阶段 decision。清洗
   warning 从 r10 的约 145 条降到 r11 的 40 条。
3. 明确引用编号常被模型从 quote 中省略。清洗器现在从模型引用的 evidence block 确定性恢复包含
   软件名称和实际使用动词的原文上下文，不接受模型改写作为证据。
4. `Atomic Simulation Environment (ASE)` 曾被规则截为 `Atomic`，现已规范为完整名称和 `ase` hint。
5. Stage04 能力资产此前只导出 backend display name，未导出 `BackendSpec.executables`。现在唯一原生
   executable 会作为 backend alias 导出，例如 `Antechamber -> openff_am1bcc`；通用 `mpirun` 被排除。
6. 方法/算法 `DLPNO-CCSD(T)`、graph clustering、Python runtime 等不会作为缺失化学软件淘汰论文。

## 残余风险

- 16 篇属于专项校准集，不能替代跨期刊、跨软件的独立 holdout；
- GUI、可视化和普通预处理程序的 `required_*` 角色仍可能被模型判得过严；
- Python 环境中存在但没有独立 BackendSpec 的模块尚未形成完整的第二层软件索引；
- 自研代码只能在论文给出足够算法和输入信息时由第三层重写，不能默认视为覆盖。

最终真调用产物：

`runs/v2_stage04_r11_deployed_qwen_16_20260808/stage_04_toolbox_resource_gate/`
