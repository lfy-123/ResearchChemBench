# 热化学数值口径与校准说明

## 为什么需要两套字段

论文 Figure 2/正文给出的是发表层面的整数自由能，例如 P2 的 pyridyl–pyridyl 与 phenyl–pyridyl 势垒约为 14 和 25 kcal/mol。论文引用 GoodVibes 2.0.1，但当前可访问的正文没有完整列出温度、低频处理、构象合并和标准态等所有后处理参数；官方补充材料入口又受到站点访问保护。

另一个由 GoodVibes 作者发布的后续示例记录 3674160，使用 GoodVibes 3.0.1 对该论文相关数据运行：

`--spc DLPNO --pes PhPy.yaml --graph PhPy.yaml -t 353.15 --imag --invertifreq -5 --media ethanol -c 1`

该示例明确采用 353.15 K、1 M、ethanol、100 cm⁻¹ Grimme 准谐近似和构象集合。在该口径下，示例输出的 P2 qh-G 势垒为：

| 路径 | qh-ΔG‡ / kcal mol⁻¹ | qh-ΔGreaction / kcal mol⁻¹ |
|---|---:|---:|
| Py 路径 | 14.29 | -31.35 |
| Ph 路径 | 22.31 | -35.11 |

它与论文 Figure 2 的 14/25 和约 -38/-41 并不完全相同。这不是自动说明某一方错误，而是表明软件版本、构象统计、低频与标准态处理会实质影响数值。

## Benchmark 评分口径

智能体输出应保留两类结果：

1. `paper_published_target`：论文 Figure 2/正文的发表整数，用于检验是否复现论文结论；
2. `recomputed_at_353K_1M`：智能体在本 benchmark 固定条件下的重新计算值，必须带完整 provenance。

不得要求重新计算值逐位等于发表整数。评分优先级为：

1. 电荷、自旋、驻点、Hessian 与 IRC 科学有效；
2. 竞争路径采用完全一致的能量和热化学口径；
3. 质子化与选择性排序正确；
4. 数值落在经独立基线运行校准的容差内；
5. 能解释与论文发表值的偏差来源。

## 当前可直接核验的文件

- `../../sources/GoodVibes_example_Goodvibes_output.dat`
- `../../sources/GoodVibes_example_PhPy.yaml`
- `../../sources/GoodVibes_example_Rxn_profile_PhPy.png`

在将本 pilot 用于正式模型排名前，应使用实际部署的 Backend 运行至少两次独立基线，并把 P0/P1/P2 全部重新计算值固化为版本化数值金标准。
