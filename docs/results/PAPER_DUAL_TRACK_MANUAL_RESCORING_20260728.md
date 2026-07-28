# 八项双轨任务人工复核结果

评分公式：`最终分数 = 科学结论分 × 科研过程分 ÷ 100`。八项运行的 Agent 和 Judge 均使用 `deepseek-v4-flash`。

## 主要结果

| 任务 | 模式 | Judge 过程/结论/最终 | 人工过程/结论/最终 | 时长（秒） | 工具调用（失败） | Agent / Judge / 总 Token | 人工结论摘要 |
|---|---|---:|---:|---:|---:|---:|---|
| `PV_Protonation_Barrier_Trend` | 自主 | 66 / 0 / 0 | 57 / 18 / **10.3** | 468.3 | 18（0） | 7,549,989 / 146,315 / 7,696,304 | 有名义上的 P0>P1>P2，但 P1/P2 未分辨、路径与热化学无效，未给出一致反应自由能。 |
| `PV_Protonation_Barrier_Trend_Reproduction` | 复现 | 81 / 80 / 64.8 | 73 / 52 / **38.0** | 462.3 | 28（0） | 6,597,996 / 127,392 / 6,725,388 | 复现强放热轮廓，但没有复现第二次质子化带来的进一步显著降垒。 |
| `BaO_Phase_Crossover_And_5d_Bonding` | 自主 | 71 / 100 / 71 | 63 / 60 / **37.8** | 1,019.0 | 38（9） | 3,953,749 / 91,248 / 4,044,997 | 计算数据支持 B1→B8→dB2，但最终提交的两个转变压力均错误并与自身焓表矛盾。 |
| `BaO_Phase_Crossover_And_5d_Bonding_Reproduction` | 复现 | 91 / 100 / 91 | 90 / 100 / **90.0** | 583.7 | 59（5） | 6,527,865 / 128,987 / 6,656,852 | 相序及 6.09、29.0 GPa 两个转变压力均成功复现。 |
| `Heterobiaryl_PV_02_CC_Selectivity` | 自主 | 77 / 0 / 0 | 57 / 0 / **0.0** | 412.9 | 14（0） | 3,744,594 / 151,205 / 3,895,799 | 把“没有 Py-Py 文件名”误判为没有 Py-Py 路径，得到与论文相反的 Ph-Py 优先结论。 |
| `Heterobiaryl_PV_Reproduction_02_CC_Selectivity` | 复现 | 53 / 0 / 0 | 41 / 0 / **0.0** | 609.3 | 27（0） | 9,355,855 / 141,888 / 9,497,743 | 同一个 TS 被同时用于 Py-Py 和 Ph-Py，未验证成键坐标或连通性，两个轮廓均无效。 |
| `Heterobiaryl_PV_05_Rate_Determining_Step` | 自主 | 78 / 0 / 0 | 66 / 13 / **8.6** | 383.4 | 14（0） | 4,244,855 / 116,742 / 4,361,597 | 正确重建部分下游轮廓，但把下游重排/偶联当作全反应决速步骤，只得到有限的选择性和不可逆性证据。 |
| `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step` | 复现 | 66 / 40 / 26.4 | 58 / 33 / **19.1** | 888.6 | 45（2） | 9,478,492 / 144,605 / 9,623,097 | 部分支持配体偶联控制选择性和后续强放热，但误判总决速步骤，并以 298 K 热校正替代 353.15 K。 |
| **合计/均值** | — | — / — / **31.7 均值** | — / — / **25.5 均值** | **4,827.5** | **243（16）** | **51,453,395 / 1,048,382 / 52,501,777** | — |

## 科研过程分项

过程指标依次为：P1 研究计划与问题定义，P2 方法选择或协议忠实度，P3 托管执行与产物流，P4 验证、证伪与不确定性，P5 失败诊断与恢复，P6 资源与执行效率，P7 溯源与可复现报告。

| 任务 | P1 /20 | P2 /15 | P3 /15 | P4 /20 | P5 /10 | P6 /10 | P7 /10 | 过程总分 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `PV_Protonation_Barrier_Trend` | 14 | 4 | 12 | 5 | 8 | 8 | 6 | **57** |
| `PV_Protonation_Barrier_Trend_Reproduction` | 17 | 10 | 13 | 8 | 10 | 7 | 8 | **73** |
| `BaO_Phase_Crossover_And_5d_Bonding` | 18 | 13 | 10 | 5 | 5 | 7 | 5 | **63** |
| `BaO_Phase_Crossover_And_5d_Bonding_Reproduction` | 18 | 15 | 14 | 17 | 10 | 8 | 8 | **90** |
| `Heterobiaryl_PV_02_CC_Selectivity` | 12 | 8 | 12 | 3 | 6 | 8 | 8 | **57** |
| `Heterobiaryl_PV_Reproduction_02_CC_Selectivity` | 5 | 4 | 12 | 2 | 6 | 5 | 7 | **41** |
| `Heterobiaryl_PV_05_Rate_Determining_Step` | 10 | 10 | 13 | 8 | 8 | 9 | 8 | **66** |
| `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step` | 8 | 7 | 11 | 10 | 8 | 6 | 8 | **58** |

## 科学结论分项

| 任务 | C1 | C2 | C3 | 结论总分 |
|---|---:|---:|---:|---:|
| `PV_Protonation_Barrier_Trend` | 质子化势垒顺序 10/40 | 分步降垒尺度 8/35 | 动力学与热力学区分 0/25 | **18** |
| `PV_Protonation_Barrier_Trend_Reproduction` | 质子化势垒顺序 15/40 | 分步降垒尺度 12/35 | 动力学与热力学区分 25/25 | **52** |
| `BaO_Phase_Crossover_And_5d_Bonding` | 相序 40/40 | 第一次转变压力 10/30 | 第二次转变压力 10/30 | **60** |
| `BaO_Phase_Crossover_And_5d_Bonding_Reproduction` | 相序 40/40 | 第一次转变压力 30/30 | 第二次转变压力 30/30 | **100** |
| `Heterobiaryl_PV_02_CC_Selectivity` | Py-Py 势垒优先 0/40 | 动力学选择性 0/35 | 质子化下保持选择性 0/25 | **0** |
| `Heterobiaryl_PV_Reproduction_02_CC_Selectivity` | Py-Py 势垒优先 0/40 | 动力学选择性 0/35 | 质子化下保持选择性 0/25 | **0** |
| `Heterobiaryl_PV_05_Rate_Determining_Step` | 醇加成决速 0/40 | 配体偶联控制选择性 5/35 | 偶联后坍塌不可逆 8/25 | **13** |
| `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step` | 醇加成决速 0/40 | 配体偶联控制选择性 18/35 | 偶联后坍塌不可逆 15/25 | **33** |

## 逐项分析

### `PV_Protonation_Barrier_Trend`

运行进行了托管分析，但使用的比较路径和热化学处理不足以建立可比的 P0/P1/P2 势垒。报告的 38.73、24.50、24.29 kcal/mol 只能弱支持名义顺序，P1 与 P2 实际未分辨，也没有三条一致参考态反应自由能，因此结论轴仅给 18 分。

### `PV_Protonation_Barrier_Trend_Reproduction`

运行遵循了大部分公开协议并给出两组势垒及强放热反应自由能，但 P1→P2 仅降低约 0.5 kcal/mol，另一组甚至升高，未复现论文尺度的第二次降垒。过程记录较完整，结论轴因动力学趋势不完整降至 52 分。

### `BaO_Phase_Crossover_And_5d_Bonding`

真实 VASP 和焓数据支持 B1→B8→dB2；但最终报告写成 3.1 和 17.65 GPa，均不在允许区间，且与产物中的约 6 和 29 GPa 交叉证据矛盾。相序给满分，两个压力只按底层数据给予有限部分分。

### `BaO_Phase_Crossover_And_5d_Bonding_Reproduction`

运行完成结构检查、VASP 能量、定体积内部弛豫、EOS 拟合及模型不确定性比较，最终给出 6.09±0.5 和 29.0±1.0 GPa。三项科学结论均满足量表，是八项中唯一接近完整复现的运行。

### `Heterobiaryl_PV_02_CC_Selectivity`

计划和托管脚本较完整，但路径识别依赖文件名字符串，没有按原子映射检查形成键、断裂键或 IRC。报告还出现 TS 明明具有约 -420 cm⁻¹ 虚频、汇总却记为零虚频的矛盾，并把“归档中没有字面 Py-Py TS 文件名”当作不存在该路径，故三个结论项均为零。

### `Heterobiaryl_PV_Reproduction_02_CC_Selectivity`

虽然成功提取 Gaussian/ORCA 能量并生成轮廓，但同一个 `[TS-I]-Py,Ph` 被同时指定给 Py-Py 和 Ph-Py，两个路径还共享相同的后续驻点。没有成键距离、断键距离、虚频模式或双向连通性证明，且声称的 353.15 K 准谐处理未通过 GoodVibes 实际完成，因此过程分和结论分都应明显低于表面产物完整度。

### `Heterobiaryl_PV_05_Rate_Determining_Step`

运行有效解析了作者 P2 归档，得到下游 Int-I→TS-I→Int-II→TS-II→Int-III 轮廓，但明确承认归档不含上游醇加成势垒，却仍把下游 TS-I 指定为全反应决速步骤。它对不同轴向组合和下游放热性提供了一些选择性及不可逆性线索，因此结论轴给予 13 分而非零分。

### `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step`

运行完成较多托管解析和驻点频率检查，正确识别第一配体偶联步骤对产物选择性的作用，并以约 -31.4 kcal/mol 总放热及实验观测支持后续过程难逆。但它把同一步同时判为总决速和选择性决定步骤，没有得到醇加成决速结论；GoodVibes 调用失败后采用 298 K Gaussian 热校正，偏离要求的 353.15 K、1 M 准谐协议，故人工最终分为 19.1。
