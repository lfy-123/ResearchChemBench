# 纯计算与完整工作流 500 篇缓存重放报告

日期：2026-08-07

## 结论

本次在既有 500 篇 Stage 02、Stage 04 和 Softcite 产物上重放新 Stage 03/05，不重新下载
或解析 PDF。旧严格口径最终保留 158/500；新口径 Stage 03 仅保留 13 篇纯计算研究，
Stage 05 最终保留 1 篇，占原始样本 0.2%。通过率大幅下降来自目标定义改变，不是运行失败。

## Stage 03

- 输入：500 篇；规则候选 329 篇；模型 `deepseek-v4-flash`。
- 输出上限：2048 tokens；329 次调用无截断、API 或 schema 错误。
- 结果：13 `strong_candidate`、291 `not_pure_computational`、194 `not_computational`、
  2 `llm_unconfirmed`。
- 模型研究类型：285 mixed、15 experimental-with-computational-support、14 pure、
  15 noncomputational；其余 171 篇没有进入模型。
- 14 篇 pure 中有 1 篇未同时满足文章角色、primary、置信度和证据门槛，因此只有 13 篇继续。

## Stage 05

13 篇纯计算候选中：

- 11 篇存在至少一个未覆盖工作流软件，例如 GPAW、PYXAID、VASPsol、VASPKIT、
  PyTorch Geometric、LASP/CATKINAS、GROMACS、CatMAP、DS-PAW 或自定义代码；
- 1 篇的补充材料状态不满足二元保留规则；
- 1 篇通过：`paper_bb29a73b418e4516`，题为 *Selective CO2 Reduction over
  gamma-Graphyne Supported Single-Atom Catalysts: Crucial Role of Strain Regulation*。
  论文被判定为纯计算，核心软件 VASP 具有 functional 验证，模型软件清单与 Softcite
  全文结果一致，所需方法族均存在功能级工具箱后端。

其中 11 篇复用了旧运行的 Softcite 论文级聚合；另 2 篇旧 Stage 03 未通过、没有旧
Softcite 聚合，但分别已被模型证实需要未覆盖的 PyTorch Geometric，或被 SI 二元规则
淘汰，因此不影响本次最终保留集合。正式新批次仍会按正常 Stage 04/05 顺序执行。

该 1 篇只是 Stage 06/Builder 候选，不等于 benchmark-ready。Builder 仍需检查输入、参数、
ground truth、科学意义和资源可行性。

## 产物

- Stage 03：`runs/redesigned_stage00_06_500_strict_flash_20260807/run/outputs/`
  `stage_03_pure_validation_v2_2048/`；
- Stage 05：同级 `stage_05_complete_workflow_validation_v2_2048/`。
