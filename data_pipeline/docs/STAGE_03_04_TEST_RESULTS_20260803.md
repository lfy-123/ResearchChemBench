# Stage 03-04 最终测试结果（2026-08-03）

## 测试输入和输出

输入为 Stage 02 去重并去除补充材料后的 17 篇正式论文：

```text
runs/pdf_bundle_grobid_20260802/outputs/stage_02_grobid_extract/documents.jsonl
runs/pdf_bundle_main_papers/main_paper_corpus_manifest.json
```

最终监督运行输出：

```text
runs/stage03_04_full_flash_20260803_v4/outputs
```

Stage 04 测试模型为 `deepseek-v4-flash`。代码使用 OpenAI 兼容接口，不依赖具体
供应商，后续可以直接替换为本地模型。

## 总体结果

### Stage 03

| 决策 | 数量 |
|---|---:|
| `direct_covered` | 13 |
| `software_not_identified` | 3 |
| `unsupported` | 1 |
| `capability_equivalent` | 0 |

### Stage 04

13 篇 `direct_covered` 论文进入资源审查：

| 决策 | 数量 | 路由 |
|---|---:|---|
| `exceeds_limit` | 1 | 淘汰 |
| `within_limit` | 1 | 放行 |
| `ambiguous` | 10 | 默认放行 |
| `no_explicit_resource` | 1 | 默认放行 |

模型共调用 12 次；1 篇没有召回资源句，因此未调用模型。Token 用量为：

- prompt：17,967；
- completion：4,601；
- total：22,568。

所有调用均 `finish_reason=stop`，所有有效响应都在第一次校验通过，没有错误文件。

## Stage 03 逐篇结果

| 论文 | 核心软件 | 决策 |
|---|---|---|
| BaO高压多晶型 | VASP、LOBSTER | `direct_covered` |
| Electron iso-density surfaces | ORCA、Multiwfn、CREST | `direct_covered` |
| GEOM | ORCA、xTB、RDKit、CREST | `direct_covered` |
| Heterobiaryl synthesis | 未识别 | `software_not_identified` |
| Pd/Cu(111) single-atom alloy | TURBOMOLE、VASP、LOBSTER | `unsupported` |
| Macrocyclizations | ORCA | `direct_covered` |
| Nitrate in water | CP2K、ORCA | `direct_covered` |
| Absolute Binding Free Energies | 未识别 | `software_not_identified` |
| High-throughput MBPT | Quantum ESPRESSO、Yambo | `direct_covered` |
| Extractant metadynamics | Gaussian、LAMMPS、PLUMED | `direct_covered` |
| All You Need Is Water | GROMACS、PLUMED | `direct_covered` |
| MOF diffusion | VASP、DeePMD、LAMMPS、PLUMED | `direct_covered` |
| Aerosol precursor formation | Gaussian | `direct_covered` |
| Electron-transfer dynamics | SHARC、OpenMolcas | `direct_covered` |
| α-Amylase enhanced sampling | 未识别 | `software_not_identified` |
| Host-Guest OneOPES | Gaussian、GROMACS、PLUMED | `direct_covered` |
| Ethane microkinetics | CatMAP、Quantum ESPRESSO | `direct_covered` |

TURBOMOLE 不在当前 `available_identifiers` 中，因此 Pd/Cu 论文按“全部核心软件均需
覆盖”的规则淘汰。三个未识别软件的论文保留审计记录，但不进入 Stage 04。

## 两篇关键回归论文

### GEOM

Stage 03 为 `direct_covered`。Stage 04 正确整理出多组 4-54 核、0.04-6.3 小时
wall time，以及 CENSO 平均任务的 54 核和 `1 day and 4 hours = 28 hours`。
多组 core-hours/CPU-hours 作为 aggregate 记录，不与500核比较。

28小时超过12小时上限，因此结果为 `exceeds_limit`。触发淘汰的是
`runtime_hours=28`，不是 aggregate core-hours。

### High-throughput MBPT

Stage 03 正确识别 Quantum ESPRESSO 和 Yambo，均由工具箱直接覆盖。Yambo 由旧版
错误的 `unsupported` 修正为 `direct_covered`。

Stage 04 正确整理出：

- `cpu_cores=40`；
- `memory_gb=230`；
- `runtime_hours=6`；
- 总收敛 wallclock `<3 hours`，scope 为 aggregate。

`Xeon Gold 6230` 被正确保留为 CPU 型号，没有生成 6230 核。所有可比较资源均低于
500核、1000 GB和12小时上限，因此结果为 `within_limit`。

## 结果分析

### 已达到的目标

- Stage 03 已恢复为聚焦的软件覆盖硬门控。
- runtime/interface 软件不再因为没有 backend wrapper 而被误判不支持。
- Gaussian 和 AMBER/GAFF 的主要概念歧义已被过滤。
- 模型负责文本理解，Python负责证据校验、单位一致性和硬阈值比较。
- 所有候选句、GROBID Quantities 结果、模型输入、模型响应和最终决策均落盘。

### 剩余局限

1. Stage 03 采用高精度优先策略。软件只在补充材料或未明确命名时，论文会被标记为
   `software_not_identified` 并停止，例如 ABFE 和 α-Amylase 论文。
2. Stage 04 只处理论文明确写出的资源，不估算未报告成本。
3. 10 篇 `ambiguous` 论文主要只有平台、一般性描述或不可与 wall time 直接比较的
   信息，因此按设计放行。
4. GEOM 的28小时是论文报告的平均 CENSO job。如果未来 benchmark 只截取更小子任务，
   论文级硬淘汰可能偏保守；当前实现严格遵循配置规则。
5. 替换本地模型后仍需用 GEOM 和 MBPT 重新进行相同回归测试。

## 验证命令

```bash
ruff check src scripts tests
ruff format --check src scripts tests
PYTHONPATH=. python -m unittest discover -s tests -v
./scripts/run_stage03_04.sh config.json <stage2.jsonl> <manifest.json> <output>
```
