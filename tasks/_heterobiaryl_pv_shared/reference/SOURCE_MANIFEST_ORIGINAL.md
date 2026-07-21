# 来源清单

## 论文

- DOI：https://doi.org/10.1126/science.aas8961
- Oxford University Research Archive 接受稿：Hilton_2018_accepted_manuscript.pdf
- PMC 全文：https://pmc.ncbi.nlm.nih.gov/articles/PMC6814017/
- 本地 PMC 快照：PMC6814017_fulltext.html

## 补充材料

- 官方 PMC 入口：https://pmc.ncbi.nlm.nih.gov/articles/instance/6814017/bin/NIHMS1054600-supplement-SI_File.pdf
- Science 入口：http://www.sciencemag.org/content/362/6416/799/suppl/DC1
- 自动下载受到 PMC proof-of-work/Science 站点访问保护，未通过绕过访问控制的方式抓取。论文正文列出补充材料包含 Materials and Methods、Figures S1–S26、Tables S1–S22、NMR spectra、References 和 Movies S1–S2。

## 论文专属计算数据

- Zenodo：https://zenodo.org/records/1439888
- DOI：https://doi.org/10.5281/zenodo.1439888
- 许可：MIT，依据 Zenodo 元数据
- 本地文件：README_original.txt、Int-I_unprotonated.zip、Int-I_H_plus.zip、Int-I_2H_2plus.zip

Zenodo README 表明压缩包包含 Gaussian .log 和 ORCA .out，覆盖 Int-I、TS-I、Int-II、TS-II、Int-III 和最终产物，并按 freq、QZ、DLPNO 分层。它们是输出文件，不应默认等同于完整原始输入文件。

## 相关代码

- GoodVibes 2.0.1：https://github.com/patonlab/GoodVibes/tree/2.0.1
- 本地快照：GoodVibes-2.0.1.tar.gz
- GoodVibes 后续示例记录：https://zenodo.org/records/3674160
- 本地示例：zenodo_3674160_metadata.json、GoodVibes_example_Goodvibes_output.dat、GoodVibes_example_PhPy.yaml、GoodVibes_example_Rxn_profile_PhPy.png
- 注意：后续示例使用 GoodVibes 3.0.1，并展示了该论文相关数据在 353.15 K、1 M、ethanol 条件下的处理；它用于交叉核验温度、标准态和物种顺序，不等同于论文当年使用的 GoodVibes 2.0.1 快照。
- PyMOL 可视化辅助脚本：https://zenodo.org/records/1435047
- 本地文件：pymol_style.py；它仅用于绘图，不是端到端计算工作流。

## 图像证据

- Figure_1.jpg 至 Figure_4.jpg 来自 PMC 页面指向的 NCBI CDN 文件。
- Figure 2 同时包含计算势垒、IRC 键级、结构、相对速率和 EtONa 条件结果，是本 pilot 的核心论文级参考图。

## 完整性验证

文件大小、Zenodo MD5、SHA-256 和压缩包测试结果见 `DOWNLOAD_VALIDATION.md`。
归档内文件数量、阶段分布和任务侧派生结构数量见 `DATASET_INVENTORY.md`。
