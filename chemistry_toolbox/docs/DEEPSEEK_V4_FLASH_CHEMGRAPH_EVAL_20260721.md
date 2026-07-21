# DeepSeek V4 Flash：5 个 ChemGraph 任务实测与工具调用审计

## 1. 执行信息

- 日期：2026-07-21（UTC）
- Agent：OpenCode
- 模型：`deepseek/deepseek-v4-flash`
- MCP：一个完整 Chemistry MCP server，向每个任务暴露相同的 101 个 Actions 和 76 个 Backends
- 评分：ResearchChemBench 内置的 ChemGraph-style LLM judge
- 执行配置：`eval_configs/deepseek_v4_flash_five.yaml`
- 批次目录：`workspaces/cli_runs/batch_20260721_101002_0e4070`
- 原始批次报告：`workspaces/cli_runs/batch_20260721_101002_0e4070/eval_report.md`

实际命令：

```bash
bash scripts/run_agent_eval.sh \
  --config eval_configs/deepseek_v4_flash_five.yaml \
  --opencode-model deepseek/deepseek-v4-flash \
  --opencode-base-url https://api.deepseek.com/v1
```

选择的任务覆盖名称解析、MACE 几何优化、GFN2-xTB 热化学、GFN2-xTB 偶极矩和多物种反应自由能，目的是检查不同 Action 与 Backend 的真实编排，而不是只运行五个相似的简单任务。

## 2. 总体结果

| Task | 科学任务 | 最终结果 | 时长 | MCP 调用 | Action 成功 | Action 失败/不支持 | Judge |
|---|---|---|---:|---:|---:|---:|---:|
| `ChemGraph_001` | sulfur dioxide 名称→SMILES | `O=S=O` | 22.934 s | 0 | 0 | 0 | 1 |
| `ChemGraph_005` | MACE sulfur dioxide 优化 | `-16.906153 eV` | 151.207 s | 6 | 3 | 3 | 1 |
| `ChemGraph_007` | CO2、800 K、GFN2-xTB Gibbs | `-281.72 eV` | 111.962 s | 10 | 6 | 4 | 1 |
| `ChemGraph_024` | CO、GFN2-xTB dipole | `0.635 D` | 37.192 s | 4 | 3 | 1 | 0 |
| `ChemGraph_032` | NH3 synthesis、400 K、GFN2-xTB ΔG | `-2.20 eV` | 389.963 s | 30 | 20 | 10 | 1 |

汇总：

- 5/5 Agent 进程正常结束并生成 `report/report.md`；
- 5/5 由 judge 成功评分；
- judge 总分 4/5，pass rate `0.8`；
- 总运行时长 713.258 秒；
- 共发生 50 次 MCP Action 调用；按 Action 返回体的真实状态统计，32 次成功，18 次为 `failed`、`unsupported` 或 `unavailable`；
- MCP server 和 worker 没有崩溃，复杂任务中的失败均返回了结构化结果，Agent 能够读取错误并多次自行修正。

因此当前工具箱的结论是：**运行基础设施稳定、主要计算链能够完成，但 Action 之间的数据契约和参数可发现性还不能称为完全正常；真实调用重试率偏高。**

## 3. 分任务审计

### 3.1 ChemGraph_001：正确，但没有测试到 MCP

Agent 直接凭模型知识写出 `O=S=O`，没有调用名称解析或 PubChem Action。Judge 认为答案正确并给 1 分。

这不是工具箱故障，但不能证明名称查询工具可用。若 benchmark 目标是评估工具调用能力，简单查询任务的评分规则应要求至少存在一次可观察的数据 Action，或者把“无需工具直接回答”单独计为另一类能力。

### 3.2 ChemGraph_005：MACE 成功，经历三次接口纠错

有效调用链：

```text
standardize_structure[success]
→ generate_3d_structure[success]
→ optimize_geometry[failed: ArtifactRef shorthand]
→ optimize_geometry[failed: model alias/local model]
→ optimize_geometry[failed: optimizer="ase"]
→ optimize_geometry[success: model="medium", optimizer="lbfgs"]
```

最终能量 `-16.906153 eV`，ground truth 为 `-16.815808 eV`，相对差约 0.54%，judge 给 1 分。

暴露的问题：

- 只传 `{"artifact_id": ...}` 会被当作完整 `ArtifactRef` 校验并缺少五个字段；
- `MACE-MP-0-medium` 没有匹配到本地模型，而上游别名 `medium` 可用；
- BackendSpec 只声明 `optimizer` 字段必需，没有向 Agent 暴露允许值 `bfgs/lbfgs/fire`，导致 `optimizer="ase"` 只能通过运行时报错学习。

### 3.3 ChemGraph_007：原子 Action 编排正确，输入契约需反复试探

最终有效科学链：

```text
RDKit 标准化和 3D 生成
→ xTB/GFN2-xTB 几何优化
→ xTB Hessian
→ internal_vibrations 正常模式
→ internal_thermochemistry RRHO
```

Agent 报告 `G(800 K) = -281.72 eV`，ground truth 为 `-281.9884 eV`，相对差约 0.095%，judge 给 1 分。这证明去掉 `run_ase` 后，Agent 确实能够自主拆分并编排优化、Hessian、振动和热化学 Actions。

10 次调用中有 4 次失败或不支持，主要来自：

- `ArtifactRef` 缩写不被接受；
- `derive_vibrational_modes` 的 Hessian/structure 输入形式不够直观；
- `FrequencyResult` 不能无歧义地直接传给 `derive_thermochemistry`，Agent 需要读取 Artifact 后重新拼装字段。

### 3.4 ChemGraph_024：0 分主要是单位契约和评分解释问题

Agent 使用 RDKit 生成结构，然后由 standalone xTB/GFN2-xTB 计算偶极矩。xTB 原始输出为：

```text
molecular dipole:
                 x           y           z       tot (Debye)
   full:       -0.250      -0.000       0.000       0.635
```

当前 adapter 返回：

```json
{
  "dipole": [-0.25, -0.0, 0.0],
  "magnitude": 0.635,
  "unit": "debye"
}
```

但向量范数 `0.25` 与 magnitude `0.635` 明显不在同一单位。两者正好相差约 `2.5417`，说明 x/y/z 是 atomic unit（`e·bohr`），最后一列才是 Debye。Adapter 把二者统一标为 Debye，属于单位契约错误。

Ground truth 的向量是 `-0.1278 e·Å`。其绝对值换算为 Debye 约为：

```text
0.1278 e·Å × 4.8032047 D/(e·Å) = 0.6138 D
```

xTB 的 `0.635 D` 与其相差约 3.45%，实际在 judge 的 5% 数值容差内。Judge 却把 `0.1278` 直接解释成 Debye，并据此给 0 分。因此本次 0 分很可能是 **adapter 混合单位 + judge 未做单位归一化造成的假阴性**，不能简单判定 xTB 计算失败。

### 3.5 ChemGraph_032：编排能力强，但 MCP-only 链尚不闭合

Agent 对 N2、H2、NH3 分别执行了：

```text
generate_3d_structure
→ optimize_geometry / xtb / GFN2-xTB
→ calculate_hessian / xtb / GFN2-xTB
→ derive_vibrational_modes
→ calculate_energy
→ derive_thermochemistry
```

最终报告：

```text
ΔG = 2 G(NH3) - G(N2) - 3 G(H2) = -2.20 eV
```

ground truth 为 `-2.162997 eV`，相对差约 1.71%，judge 给 1 分。

但是 30 次 MCP 调用中有 10 次失败/不支持。最关键的问题是：

- `derive_vibrational_modes` 首次收到 Artifact ID 时把字符串当成数值 Hessian；
- `internal_thermochemistry` 默认按 nonlinear molecule 处理，而 N2/H2 是 linear molecule；
- `linearity` 出现在 FrequencyResult 中时不会自动传递为 ASE `IdealGasThermo.geometry`；
- 结果出现 `entropy_ev_per_kelvin=null`、`gibbs_free_energy_ev=null`，而不是清晰失败；
- Agent 最终使用 shell 直接运行 xTB，并用自写 Python RRHO 计算补齐 N2/H2 的 Gibbs free energy。

所以该任务验证了 Agent 的自主恢复能力，但严格来说，不是仅靠 MCP Actions 完成。对于“评估 Agent 编排 MCP 科学工具”的 benchmark，这应在报告中单独标注。

## 4. 需要优先优化的问题

### P0：trace 成功/失败统计不真实

`chemistry_toolbox/mcp/tracing.py` 只在 Python/MCP 函数抛异常时把 event 记为失败。Action 正常返回 `{"status": "failed"}` 或 `{"status": "unsupported"}` 时，trace 外层仍记录 `status=success`。

因此本批次 `_meta.json` 错误地报告：

- 50 次成功；
- 0 次失败。

而读取 `_tool_results/*.json` 内层 Action 状态后，真实值是 32 成功、18 失败/不支持。这个问题会直接污染 benchmark 的过程指标和 judge 输入筛选，应最优先修复。

建议让 tracing 在返回值为 ActionResult mapping 时继承其 `status`，并让 `normalized_tool_calls` 同时保留失败调用及结构化错误，而不是只看 transport 是否抛异常。

### P0：修正 xTB dipole 的单位

可选择以下任一稳定契约：

1. 把 x/y/z 从 `e·bohr` 乘 `2.541746473` 转为 Debye，再与 magnitude 一起返回；
2. 同时返回 `dipole_atomic_unit` 和 `magnitude_debye`，不使用一个 `unit` 覆盖两种数值；
3. 统一转成 `e·Å`，并让所有 dipole Backends 使用相同单位。

评分前还应按单位归一化 ground truth 与 Agent 结果。

### P1：允许 ArtifactRef 的自然缩写

当前 `ArtifactStore.load()` 对 dict 一律执行完整 `ArtifactRef.model_validate()`，导致 `{"artifact_id": "art_..."}` 失败；但直接字符串 ID 又可以通过 `find()`。

建议显式支持三种等价输入：

```text
"art_..."
{"artifact_id": "art_..."}
完整 ArtifactRef
```

这样不会替 Agent 选择工作流，只是降低原子 Action 之间的机械连接成本。

### P1：给 BackendSpec 增加可发现的参数 schema

当前 MACE、xTB、internal thermochemistry 等 BackendSpec 的 `method_schema` 都为空，只列出必需字段名，没有枚举、单位、范围、默认值和示例。

至少应补全：

- MACE `model` 的有效别名、对应缓存文件和下载策略；
- optimizer 的 `bfgs/lbfgs/fire` 枚举；
- xTB method、optimization level 和输出单位；
- thermochemistry 的 `geometry=linear/nonlinear/monatomic`、symmetry number、spin、pressure unit；
- Hessian、FrequencyResult 和 ThermochemistryResult 的可直接连接示例。

这些信息是让 Agent 自主选择所必需的元数据，不会构成固定工作流。

### P1：保证相邻 Actions 的输出可直接作为输入

应增加端到端契约测试：

```text
generate_3d_structure.output_artifacts[AtomicStructure]
  → optimize_geometry.inputs.structure

calculate_hessian.output_artifacts[Hessian]
  → derive_vibrational_modes.inputs.hessian

derive_vibrational_modes.output_artifacts[FrequencyResult]
  → derive_thermochemistry.inputs.frequencies
```

测试应覆盖直接结构化 result、字符串 artifact ID、缩写 dict 和完整 ArtifactRef 四种形式。

### P1：修复 linear molecule 热化学

`internal_thermochemistry` 应读取或推断 FrequencyResult 的 linearity，并把它映射到 ASE `IdealGasThermo.geometry`。对于 non-finite entropy/Gibbs，必须返回结构化失败或明确警告，不能静默序列化为 `null`。

### P2：更新 ChemGraph ground truth 与 benchmark 隔离策略

- Ground truth 仍以旧 `molecule_name_to_smiles`、`smiles_to_coordinate_file`、`run_ase` 为 expected calls，与当前有意设计的原子 Actions 不一致；
- 建议把 expected sequence 改为允许等价 Action DAG，而不是旧工具名的线性流程；
- `ChemGraph_001` 在 0 MCP 调用时仍得 1 分，不利于评估工具调用；
- OpenCode 可使用 unrestricted bash。本次 `ChemGraph_032` 在 MCP 热化学失败后直接运行 xTB 和自写 Python，因此应同时报告 `task_pass` 与 `mcp_only_pass`；
- `run_agent_eval.sh --help` 仍显示“40 Scientific + 5 Data Actions”，实际已是 101 Actions，应同步更新。

## 5. 最终判断

从本批次可以确认：

- 一个完整 MCP server 能稳定启动并承载连续的多后端调用；
- RDKit、MACE、standalone xTB、internal vibrations 和 internal thermochemistry 的主要路径能够实际运行；
- Agent 能在没有固定 `run_ase` 流程工具的情况下，自主组合优化、Hessian、振动、热化学和反应算术；
- 复杂任务即使出现结构化错误，DeepSeek V4 Flash 也能多次纠错并得到正确答案。

但当前还不能说“所有工具调用完全正常”。在把本工具箱用于正式 benchmark 前，至少应先处理 trace 状态、xTB dipole 单位、ArtifactRef 缩写、相邻 Action 契约以及 linear molecule thermochemistry；否则过程指标会失真，Agent 会消耗大量调用做接口试探，并可能产生错误的 0 分。
