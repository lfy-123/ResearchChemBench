# 已验证成功计算参考 — paper_0cd74ae20ab933f3 / paper_reproduction

整理日期：2026-09-23。本文件只记录既有成功的科学计算链，属于 evaluator 私有档案，不是评分规则，也不是 agent 必须照做的脚本。未在本次维护中新增量化计算；失败/重试不计入下列成功结果。

## 1. 来源与实际范围（Group 6）

正文 PDF p6；SI PDF pp5–6方法、p35敏感性、p36表。

[论文正文](../../../../papers/paper_0cd74ae20ab933f3/documents/main.pdf)；[当前成功结果与证据索引](../../../../runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260918_closure/report/results.json)。
[补充材料 supplementary_001.pdf](../../../../papers/paper_0cd74ae20ab933f3/documents/supplementary_001.pdf)

## 2. 真实有效计算流程

1. 从正式 SI triplet 几何取 R_H/R_CH3/R_OCH3 三个孤立中性 Cu2(AnCOO)4(4-RPy)2；验图连接和元素，128/134/136原子。历史在 author geometries 上求能，不声称从当前 public connectivity 新优化或做频率。
2. PySCF2.13.1/forge B3LYP/def2-SVP、def2-svp-jkfit density fitting；UKS triplet Sz=1，grid3、20 collinear samples，final SCF1e−9，SF10 roots1e−5。保留真实 PySCF logs/checkpoints，而非 Gaussian终止标记。
3. 用各 spin-flipped roots 的 S²独立赋 lowest singlet/triplet，以 J=(ES−ET)×219474.63136314 cm⁻¹；TDA 不拿 UKS reference 代替其 triplet root。J=−334.373525/−341.412046/−344.582322。
4. 按 triplet三重简并，P=100×3exp[J/(kBT)]/[1+3exp[J/(kBT)]]，300K 得37.636230/36.847290/36.49420%。H full-SF 实算控制 J=−344.221852/P=36.534274；这是一项方法敏感性，不谎称 Me/OMe 也做 full-SF。

## 3. 有效产物与原始输入/输出

- [results.json（20260918_closure）](../../../../runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260918_closure/report/results.json)
- [results.json（20260921_acceptance）](../../../../runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260921_acceptance/report/results.json)

下列日志/后处理由上述有效链索引。输入取同目录 input.com/input.inp（存在时直链）；路径本身不是通过判据，科学量与步骤见第2节。

- [production/R_CH3/pyscf.log](../../../../runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_CH3/pyscf.log)
- [production/R_H/pyscf.log](../../../../runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_H/pyscf.log)
- [production/R_OCH3/pyscf.log](../../../../runs/hold_verification/group_6/paper_0cd74ae20ab933f3/20260915_author_xyz/production/R_OCH3/pyscf.log)

## 4. 当前 evaluator 对应关系

以下对应是证据核对，不是本轮运行 LLM judge 的评分，也不宣称复现了 AR 的自主探索过程。

| 项目 | 当前要求 | 本参考支持方式 |
|---|---|---|
| `kp_proc` | The investigation treats the three named Cu2 dimers as neutral paddlewheel models, uses a triplet reference for the open-shell calculation, and reports a traceable singlet–triplet gap protocol for every derivative. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_j` | The calculated singlet–triplet gaps are approximately −335, −342, and −345 cm^-1 for R=H, CH3, and OCH3, respectively. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_pop` | The calculated 300 K triplet populations are 37.6%, 36.8%, and 36.4% for R=H, CH3, and OCH3. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `kp_trend` | The calculated series shows increasingly negative J and decreasing triplet population from H to CH3 to OCH3. | 第2节的身份、有效计算、观测量及第3节原始证据；只认已完成量，不用免责声明替代。 |
| `con_final` | The independent calculation supports the reported qualitative hypothesis that electron-donating axial pyridine substituents modestly strengthen antiferromagnetic exchange in this isolated model series, with calculated J becoming more negative and the 300 K triplet population decreasing across H, CH3, OCH3. | 上述关键点与实际数值/物理解释共同支持；源值和验证值不混写。 |

## 5. 不能扩大解释的地方

只支持当前三个孤立模型的 gap/热布居和系列关系；原作者数据与实验对比不取代真实量化。公开没有原作者 triplet endpoint。

参考使用作者知情路线和可能的作者端点，能支持此科学子问题存在真实可行计算链；不要求向被评 agent 公开端点，也不证明任意方法、初猜都必然收敛。任务的公开身份和必要定义须另行自包含核对。普通 limitation 不作为评估成果；本段只是维护档案的事实说明。
