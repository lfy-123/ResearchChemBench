# Stage 03-05 重构测试结果分析

> 历史文档：该实现已于 2026-08-03 被 Stage 03-04 重构替代。旧文档中的 Yambo
> “不支持”结论源于只检查 backend 的代码缺陷。当前结果见
> `docs/STAGE_03_04_TEST_RESULTS_20260803.md`。

## 1. 报告范围

本文档记录按照
`docs/modifiy/STAGE_03_05_REDESIGN_PLAN.md` 完成的 Stage 03、Stage 04 和
Stage 05 重构、真实论文监督测试、问题修复及最终结果。

最终采用的运行目录为：

```text
runs/stage03_05_redesign_20260802_v5/outputs
```

测试输入不是原始 38 份文件，而是 Stage 01 已确认的 17 篇唯一正式论文。14 份
补充材料和其他附件、7 份重复正文均未进入本次 Stage 03-05 测试。

```text
Stage 02 记录：
runs/pdf_bundle_grobid_20260802/outputs/stage_02_grobid_extract/documents.jsonl

17 篇清单：
runs/pdf_bundle_main_papers/main_paper_corpus_manifest.json
```

## 2. 最终实现概览

### 2.1 Stage 03：核心软件覆盖门控

目标是确认论文实际使用的全部核心计算软件都被 ResearchChemBench 工具箱直接
覆盖。实现步骤为：

1. 将 Stage 02 保存的 GROBID TEI 文件提交给本地 Softcite。
2. 保存 Softcite 原始软件实体、版本、上下文和 used 分类。
3. 使用可编辑别名表归一化软件名和版本写法。
4. 对工具箱已知软件执行 TEI 词典补召回，并继续使用 Softcite 上下文接口判断
   作者是否实际使用。
5. 将提及分为核心、辅助和忽略三类。
6. 要求每个实际使用的核心软件均直接存在于 `assets/toolbox.json`。
7. 未识别到核心软件、存在任一未覆盖核心软件时拒绝。
8. 能力等价论文只进入备选清单，不进入 Stage 04；本批次没有此类记录。

Softcite 服务失败、DeLFT 模型初始化失败、请求失败均抛错停止流水线，不转化为
论文不合格，也不默认放行。

### 2.2 Stage 04：完整计算过程门控

Stage 04 只处理 Stage 03 的 `direct_covered` 论文。代码从 GROBID TEI 整理以下
内容，形成不超过配置长度的紧凑文本：

- 标题和摘要；
- Stage 03 的核心软件使用证据；
- 计算方法、计算结果、分析和结论相关段落；
- GROBID 段落索引和章节来源。

随后只调用一个 OpenAI 兼容模型 API。模型必须判断五个必要元素：计算对象、方法
设置、实际软件执行、计算结果、解释或结论。

- `complete`：通过；
- `incomplete`：淘汰；
- `uncertain`：淘汰；
- 未配置 API 或调用失败：记录 `skipped`/`skipped_error` 并放行，不使用规则回退；
- 结构化字段互相冲突：记录一致性警告，归一化为 `uncertain` 并淘汰。

本次测试并未部署本地小模型。运行脚本从 `../config.local.env` 读取
`JUDGE_API_BASE`、`JUDGE_API_KEY` 和 `JUDGE_MODEL_NAME`，实际调用的是
`https://api.deepseek.com/v1` 上的 `deepseek-v4-flash`。因此本报告的 Stage 04
结果只能证明 OpenAI 兼容接口和门控代码能够工作，不能证明本地模型已经部署或
本地模型会产生相同判断。

### 2.3 Stage 05：明确资源上限门控

Stage 05 只处理 Stage 04 通过或按配置跳过的论文。默认上限为：

| 资源 | 上限 |
| --- | ---: |
| CPU 核数 | 500 |
| GPU 数量 | 8 |
| 内存 | 1000 GB |
| 单次运行时间 | 12 小时 |

代码先用 CPU、GPU、core、node、memory、runtime、hour 等关键词召回句子，再同时
执行：

- GROBID Quantities 数值与单位抽取；
- 严格关键词解析器，对 CPU 核、GPU、内存和运行时间补抽取；
- 上下文绑定，区分本文实际计算、平台容量、物理模拟时长和歧义信息；
- 单位归一化和阈值比较。

只有“属于本文实际计算”且数值明确超过上限时淘汰。没有资源信息、只有超算平台
名称、句义含糊或物理过程持续时间时默认放行。

## 3. 环境和第三方版本

所有 GitHub 第三方源码均位于 `data_pipeline/third_party`：

| 组件 | 目录 | 固定版本 |
| --- | --- | --- |
| Softcite | `third_party/software-mentions` | `c7c83852a3cad8f2d9d07ce3de6fbe852e23c19a` |
| GROBID Quantities | `third_party/grobid-quantities` | `d0d55592f4d0ddbe6a549e06613349adaa2d1cd7` |
| DeLFT | `third_party/delft` | `d8505592c38058b9b0abbde14d4ddedff3ad7d0f` |
| GROBID | `third_party/grobid` | `0.9.0` |

验证环境：Python 3.10.12、Transformers 4.57.3、Torch 2.6.0+cu124、NumPy
1.26.4、TensorFlow 2.17.1、`tf_keras` 2.17.0、JEP 4.3.1、OpenJDK 21。

Softcite 模型默认从以下镜像下载：

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

引导脚本会递归校验模型 HDF5 对象，避免文件大小正常但内部块损坏的情况。

## 4. 监督运行过程

### 4.1 v1：发现 Softcite 模型损坏

v1 在 Stage 03 处理到第 9 篇时，Softcite 日志报告 DeLFT 上下文模型初始化失败。
检查发现 `context_creation_bert/model_weights.hdf5` 内部 HDF5 块损坏。运行被主动
停止，没有把部分结果作为最终结果。

修复：增加递归 HDF5 完整性校验、强制重新下载和 Softcite 致命日志检测。

### 4.2 v2：发现 GROBID Quantities 请求格式错误

v2 完成 Stage 03 和 Stage 04，但 Stage 05 第一个请求返回 HTTP 415。第三方源码
中的 `@Consumes(MediaType.MULTIPART_FORM_DATA)` 和 REST 文档均表明接口要求
multipart 字段 `text`。

修复：客户端由 `application/x-www-form-urlencoded` 改为
`multipart/form-data`，增加请求体和 Content-Type 自动化测试。

### 4.3 v3：发现 Stage 03 过度淘汰

v3 首次全流程成功，漏斗为 `17 -> 6 -> 5 -> 5`。人工审计发现：

- `scripts`、`code`、`library`、`module` 被 Softcite 识别后错误视为核心软件；
- `optPBE-vdW` 是泛函，GAFF 是力场，不应作为核心计算软件；
- Hyperopt、pywindow、mpmath、AiiDA、MEPSA 属于辅助工具；
- `CP2K 8.2` 和 `QUANTUM ESPRESSO simulation package` 未正确归一化；
- 一个较早的 `used=false` 软件提及会阻断后续更明确的实际使用证据；
- `Gaussian basis` 和 `Gaussian kernels` 被词典补召回误认为 Gaussian 软件。

修复：完善角色表和别名表、版本后缀归一化、多证据恢复、强使用语句补充判断，
并对 Gaussian 的非软件上下文设置明确排除。

### 4.4 v4：发现 Stage 04 输出自相矛盾

v4 漏斗为 `17 -> 12 -> 10 -> 10`。软件门控结果经人工检查明显改善，但 GEOM
论文的模型响应同时给出：

- `decision=incomplete`；
- 五个必要条件全部为 `true`；
- 理由明确称论文包含 complete computational chemistry process。

修复：增加响应一致性校验。`complete` 与任一必要条件为假冲突，或 `incomplete`
与五项全真冲突时，统一归一化为 `uncertain` 并拒绝，同时保存警告。

### 4.5 v5：最终成功运行

最终运行从 2026-08-02 20:21:34 到 20:24:50，约 3 分 16 秒。Softcite 和
GROBID Quantities 都由脚本自动启动，阶段结束后自动停止。最终两个服务端口均已
释放。

## 5. 最终漏斗结果

| 阶段 | 输入 | 通过/继续 | 拒绝或备选 | 结果 |
| --- | ---: | ---: | ---: | --- |
| Stage 03 | 17 | 12 | 5 | 12 `direct_covered`，5 `unsupported` |
| Stage 04 | 12 | 10 | 2 | 10 `complete`，1 `uncertain`，1 `incomplete` |
| Stage 05 | 10 | 10 | 0 | 10 `no_explicit_resource` |

最终有 10 篇论文进入后续 MinerU 阶段。

## 6. Stage 03 逐篇结果

| 论文 | 核心软件 | 辅助/忽略 | 判定 | 说明 |
| --- | --- | --- | --- | --- |
| 5d Orbital Covalency Controls the High-Pressure Polymorphism of BaO | VASP, LOBSTER | 无 | 直接覆盖 | 两个核心软件均在工具箱中 |
| Electron iso-density surfaces provide a thermodynamically consistent representation of atomic and molecular surfaces | ORCA, Multiwfn, CREST | 忽略 scripts | 直接覆盖 | 修复前被通用词 scripts 误伤 |
| GEOM, energy-annotated molecular conformations for property prediction and molecular generation | ORCA, xTB, RDKit, CREST | Hyperopt 辅助；code 忽略 | 直接覆盖 | 核心生成和量化软件均覆盖 |
| Heterobiaryl synthesis by contractive C-C coupling via P(V) intermediates | 未识别 | 无 | 不支持 | 按方案，未识别核心软件默认拒绝 |
| Density Functional Theory Investigation of Simple N-Heterocyclic Carbenes Adsorbed on the Pd/Cu(111) Single-Atom Alloy Surface | TURBOMOLE, VASP, LOBSTER | 忽略 optPBE-vdW | 不支持 | TURBOMOLE 是实际核心软件且工具箱未覆盖 |
| Organocatalyst-Controlled Stereoselective Head-to-Tail Macrocyclizations | ORCA | 无 | 直接覆盖 | 软件门控通过，完整性由 Stage 04 再判断 |
| Revealing the Photochemical Pathways of Nitrate in Water through First-Principles Simulations | CP2K, ORCA, Gaussian | MEPSA 辅助 | 直接覆盖 | CP2K 8.2 正确归一化；Gaussian 来自 `Gaussian envelopes`，人工复核为误报 |
| Absolute Binding Free Energies with OneOPES | AMBER/pmemd | 无 | 直接覆盖 | 当前证据只是 Amber ff14SB/ff19SB 力场，映射到 pmemd 属于误报；TEI 的数据可用性段另有 GROMACS/PLUMED 输入文件证据，但当前 Stage 03 未恢复 |
| Towards high-throughput many-body perturbation theory: efficient algorithms and automated workflows | Quantum ESPRESSO, Yambo | AiiDA 辅助；YamboRestart 忽略 | 不支持 | Yambo 执行 GW-BSE，是未覆盖核心软件 |
| Using Metadynamics to Reveal Extractant Conformational Free Energy Landscapes | AMBER/pmemd, Gaussian, LAMMPS, PLUMED | 无 | 直接覆盖 | Gaussian、LAMMPS、PLUMED 有执行证据；AMBER/pmemd 仅来自 GAFF2 力场文字，属于额外误报但不改变通过结果 |
| All You Need Is Water: Converging Ligand Binding Simulations with Hydration Collective Variables | GROMACS, PLUMED | 无 | 直接覆盖 | 从明确的生产模拟语句恢复实际使用证据 |
| Modeling Diffusion in Metal-Organic Frameworks using On-the-fly Probability Enhanced Sampling-based Machine Learning Potentials | VASP, DeePMD, LAMMPS, PLUMED | pywindow 辅助 | 直接覆盖 | 修复后不再被 pywindow 误伤 |
| Nitric oxide can enhance secondary aerosol precursor formation from aromatic carbonyls | Gaussian | 无 | 直接覆盖 | Gaussian 16 有明确计算执行证据 |
| Few-femtosecond electron transfer dynamics in photoionized donor-π-acceptor molecules | OpenMolcas, SHARC | 无 | 不支持 | SHARC 是实际核心动力学软件且未覆盖 |
| How and When Does an Enzyme React? Unraveling a-Amylase Catalytic Activity with Enhanced Sampling Techniques | 未识别 | 无 | 不支持 | 主文 TEI 未识别到作者实际使用的核心软件，按方案拒绝 |
| Host-Guest Binding Free Energies a la Carte: An Automated OneOPES Protocol | GROMACS, PLUMED | 忽略 GAFF；Gaussian kernel 未作为软件 | 直接覆盖 | 从“simulations are run with”证据恢复 GROMACS/PLUMED |
| First Principles Micro-kinetic Model of Catalytic Non-oxidative Dehydrogenation of Ethane over Close-packed Metallic Facets | Quantum ESPRESSO, CatMAP | mpmath 辅助；library/module 忽略 | 直接覆盖 | DFT 和微观动力学核心软件均覆盖 |

Stage 03 的五篇拒绝中，三篇有明确未覆盖核心软件，另外两篇未识别到核心软件。
拒绝侧与设计文档的保守门控规则一致，但通过侧仍存在至少三处人工确认的提取问题：
`Gaussian envelopes -> Gaussian`、`Amber force field -> amber_pmemd` 两次。第一处和
其中一处 AMBER 误报不改变其他已覆盖核心软件支撑的路由；`Absolute Binding Free
Energies with OneOPES` 当前则依赖错误的 AMBER 映射通过，虽然 TEI 中确有
GROMACS/PLUMED 输入文件被使用的证据。该论文的软件清单和直接覆盖结论需要修复
Stage 03 后重跑，不能把当前软件抽取视为完全准确。

## 7. Stage 04 逐篇结果

| 论文 | 判定 | 主要理由 |
| --- | --- | --- |
| 5d Orbital Covalency Controls the High-Pressure Polymorphism of BaO | complete | 对象、VASP/LOBSTER 方法、计算结果和高压相解释完整 |
| Electron iso-density surfaces provide a thermodynamically consistent representation of atomic and molecular surfaces | complete | 定义分子表面、执行量化计算、报告误差并解释密度阈值 |
| GEOM | uncertain | 模型 decision 与五项布尔条件和理由冲突；按不确定拒绝 |
| Organocatalyst-Controlled Stereoselective Head-to-Tail Macrocyclizations | incomplete | 有 DFT 环张力结果，但模型认为实际软件执行细节不足 |
| Revealing the Photochemical Pathways of Nitrate in Water through First-Principles Simulations | complete | AIMD、增强采样、TDDFT、结果和光解路径解释完整 |
| Absolute Binding Free Energies with OneOPES | complete | 体系、力场和 CV 设置、模拟结果及实验比较完整 |
| Using Metadynamics to Reveal Extractant Conformational Free Energy Landscapes | complete | DFT/MD 设置、自由能面结果和萃取机理解释完整 |
| All You Need Is Water | complete | GROMACS/PLUMED 设置、结合自由能结果和收敛解释完整 |
| Modeling Diffusion in Metal-Organic Frameworks | complete | VASP、DeePMD、LAMMPS/PLUMED 链条和扩散机理完整 |
| Nitric oxide can enhance secondary aerosol precursor formation | complete | 分子体系、速率计算、势垒和实验关联完整 |
| Host-Guest Binding Free Energies a la Carte | complete | 力场、增强采样、结合自由能结果和力场性能解释完整 |
| First Principles Micro-kinetic Model of Catalytic Non-oxidative Dehydrogenation of Ethane | complete | Quantum ESPRESSO 与 CatMAP 计算、速率/选择性和机理解释完整 |

Stage 04 的所有 API 调用均成功，没有 `skipped` 或 `skipped_error`。每篇论文的
模型输入、结构化响应、原始响应字符串、模型名、token 使用量和耗时均已保存。

GEOM 的结果体现了保守策略：从语义上看模型理由倾向 complete，但结构化输出自相
矛盾，因此不能称为“明确认定完整”，最终以 uncertain 淘汰。该记录适合后续人工
复核或使用更稳定的本地模型重新判断。

## 8. Stage 05 结果分析

10 篇输入全部判定为 `no_explicit_resource`。这不表示论文计算便宜，而只表示正文
中没有抽取到满足以下全部条件的资源记录：

1. 数值和单位明确；
2. 属于 CPU、GPU、内存或实际运行时间；
3. 明确绑定到本文实际计算；
4. 可与配置上限直接比较。

资源关键词召回数量为 0 到 5 条。人工检查确认主要噪声包括：

- `core orbitals` 中的 core，不是 CPU 核；
- MOF 结构中的 linker node，不是计算节点；
- 大气反应物寿命 `10 h`，不是任务运行时间；
- Gaussian 基组 `6-31G`，不是 GPU 或内存；
- 能量截断 `500 eV`，不是资源数值。

GROBID Quantities 对这些句子抽取了时间、能量、长度等普通物理量，但 Stage 05
只接受资源类型和实际计算绑定，因而没有误拒绝。原始响应仍全部保存，便于审计。

本批次没有真实的超限样本，所以超过 500 CPU 核、8 GPU、1000 GB 内存或 12 小时
运行时间的拒绝分支主要由单元测试覆盖。测试同时验证：501 核和 13 小时拒绝，8
GPU 与 900 GB 放行，平台支持 2048 核和实验反应 24 小时不被误拒绝。

## 9. 输出文件

### 9.1 总日志和汇总

```text
runs/stage03_05_redesign_20260802_v5/outputs/stage_03_05.log
runs/stage03_05_redesign_20260802_v5/outputs/summary.json
```

### 9.2 Stage 03

```text
stage_03_software_coverage/software_coverage_documents.jsonl
stage_03_software_coverage/direct_covered_pdf_paths.jsonl
stage_03_software_coverage/capability_equivalent_pdf_paths.jsonl
stage_03_software_coverage/softcite_raw/*.json
stage_03_software_coverage/softcite_service.log
stage_03_software_coverage/summary.json
```

### 9.3 Stage 04

```text
stage_04_computation_completeness/computation_completeness_documents.jsonl
stage_04_computation_completeness/model_inputs/*.txt
stage_04_computation_completeness/model_responses/*.json
stage_04_computation_completeness/selected_pdf_paths.jsonl
stage_04_computation_completeness/summary.json
```

### 9.4 Stage 05

```text
stage_05_resource_limits/resource_screened_documents.jsonl
stage_05_resource_limits/grobid_quantities_raw/*.json
stage_05_resource_limits/grobid_quantities.log
stage_05_resource_limits/selected_pdf_paths.jsonl
stage_05_resource_limits/summary.json
```

PDF 清单只保存原始 PDF 路径，不复制 PDF。

## 10. 自动化验证

最终代码执行：

```bash
python -m ruff check src scripts/run_stage03_05.py tests
python -m unittest discover -s tests -v
```

结果：Ruff 通过，53 个单元测试全部通过。测试覆盖：

- Stage 03 三类路由、辅助/背景软件、版本和别名、多证据恢复、Gaussian 歧义；
- Softcite 模型初始化致命错误；
- Stage 04 complete/incomplete/uncertain、API 失败放行、响应一致性；
- GROBID Quantities multipart 请求格式；
- Stage 05 CPU/GPU/内存/时间边界、平台容量、物理时长和实验时长排除；
- 重构后 Stage 06 只接收 Stage 05 通过记录。

## 11. 结论和剩余边界

重构方案的主要要求已经实现：原 Stage 03-05 已从语料主流程删除并由三个职责
单一、可审计的门控替代；第三方服务可由 shell 脚本自动部署、启动和停止；所有
阶段均保存输入证据、原始服务响应、结构化决定和 PDF 路径。

最终结果符合当前保守策略，但仍有三项需要在扩大语料后持续维护：

1. Softcite 的软件 used 分类并非绝对准确，软件别名、辅助角色和歧义规则需要随
   新语料扩展。
2. Stage 04 的质量取决于配置的通用模型。代码已经处理调用失败和结构化冲突，
   但边界论文仍可能需要人工复核。
3. 本批次没有明确超限资源样本。Stage 05 的真实拒绝精度需要在包含 CPU/GPU/
   walltime 记录的更大论文集上继续验证。

在当前 17 篇正式论文测试集上，流水线最终将 10 篇标记为满足三个门控条件。但因
Stage 03 仍存在上述软件误报，尤其是 `Absolute Binding Free Energies with
OneOPES` 的 AMBER/pmemd 错误映射，这一数字是当前代码输出，不应解释为已经人工
确认的 10 篇完全可靠结果。
