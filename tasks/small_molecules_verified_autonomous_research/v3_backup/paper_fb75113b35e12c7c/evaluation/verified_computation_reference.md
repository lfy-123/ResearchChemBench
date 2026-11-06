# Round-one scope notice — 2026-11-03

Only PI1/PI2 and their stated reaction comparisons are scored. PI3 is outside scope. Supplied unranked candidate sites and structures do not determine a preferred outcome. Existing calculations below are historical evidence and apply only to matching current conclusions. Removed tasks are not required. No new QM or blind-agent validation was performed. Current scoring: `scoring_rules.json`; scope/provenance: `round1_review.json`.

---

## V3 scope and evidence reuse — 2026-10-27

The same three molecular graphs, cyclic-enone comparison, PI1 second-addition scope and source-free prediction boundary are retained. Seven independent final outcomes replace thirteen mixed intermediate/final V2 items; source energies have no hard windows. Existing G1/G7, alpha-TS and local gamma evidence is reused with its original limitations. Existing raw logs and historical notes below are preserved. This migration performs no new quantum computation or blind ARCHE run and does not inherit historical PASS. Current rules and per-outcome evidence coverage are in scoring_rules.json and reference_qualification.json.

# 当前科学分V2与完整计算参考 — 2026-10-24

当前状态为 **RESULTS_COMPLETE_NUMERIC_REVIEW**：现题必要结果完整，限定结论有支持；正式科学结果评分可用，严格数值验收及发布仍待专家。现行规则仅13项科学结果，中间60分、最终40分，无过程分、无精确数值窗。32组Opt/Freq+SP共64个有效日志，加R5局部释放与R6十二点扫描2段。此段覆盖下方历史INCOMPLETE/pending的当前状态，但不删除历史失败与过程记录。

- `V2_R5`：[main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_fb75113b35e12c7c/documents/main.pdf)，1-based PDF页序8, 9, 11；SHA-256 `9d011f8dd496becafeefe6025c2cc3a8f0c48fd9b8b62876da537807299495c4`。Schemes 12与R5方法敏感性、成环及二次加成限制；印刷1595–1596、1598。
- `V2_R6`：[main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_fb75113b35e12c7c/documents/main.pdf)，1-based PDF页序9, 10, 11；SHA-256 `9d011f8dd496becafeefe6025c2cc3a8f0c48fd9b8b62876da537807299495c4`。Schemes 13–14，R6两类成环可达性/稳定性和正文初始排序歧义；印刷1596–1598。
- `V2_SULF`：[main.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_fb75113b35e12c7c/documents/main.pdf)，1-based PDF页序10, 11；SHA-256 `9d011f8dd496becafeefe6025c2cc3a8f0c48fd9b8b62876da537807299495c4`。Scheme 15与Figure 5：Sulf阴离子、质子化产物及有限解释；印刷1597–1598。
- `V2_SI_METHOD`：[supplementary_001.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_fb75113b35e12c7c/documents/supplementary_001.pdf)，1-based PDF页序30, 31；SHA-256 `b244e20e86aefa2d1d747ca1117da9313c177d5338c8e8832f3802a5a6babf12`。方法1/7、RRHO和1 atm→1 M；S30–S31。
- `V2_SI_NETWORK`：[supplementary_001.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_fb75113b35e12c7c/documents/supplementary_001.pdf)，1-based PDF页序31, 32, 34；SHA-256 `b244e20e86aefa2d1d747ca1117da9313c177d5338c8e8832f3802a5a6babf12`。Table S4结构映射、Figure S8反应能网络；S31–S32、S34。
- `V2_SI_IDENTITY`：[supplementary_001.pdf](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/papers/paper_fb75113b35e12c7c/documents/supplementary_001.pdf)，1-based PDF页序4, 6, 39, 47, 51；SHA-256 `b244e20e86aefa2d1d747ca1117da9313c177d5338c8e8832f3802a5a6babf12`。底物合成身份及来源坐标，特别Sulf指定E appendage。

### 方法、模型参数及真实执行

正文Schemes 12–15在PDF第8–11页（印刷1595–1598），SI方法在PDF第30–31页，Table S4在第31–32页，Figure S8在第34页（与S页编号相同）。PI1=R5=1a，PI2=R6=1b，PI3=Sulf=1i；R5/R6的SMe1、SMe4、SMe6分别对应δ、α、β′加成。Sulf的SMe4_c13和SMe4_2是α加成的两个来源构象。Table S4给出中间体/产物标签，不能把文件名或标签本身作为身份验证。

|环节|作者方法/定义|实际验证与偏离|
|---|---|---|
|分子与电子态|指定三个完整底物，MeS−及MeSH；闭壳层单重态|保留完整图与指定烯烃构型。中性0、阴离子与相应TS−1，全部多重度1；源有序元素/连接图均保持|
|优化、频率|method1=B3LYP-D3BJ/def2-TZVP、CPCM氯仿；极小点0虚频，TS1虚频|ORCA 6.1.1；作者6.0.1。32组配对态中30极小点、2个α-TS；源坐标重新优化并频率验证|
|高层单点|method7=ωB97M-V/def2-TZVPD、SMD氯仿；DEFGRID3、RI/COSX|同一优化几何做method7，32组的单点与频率最终打印坐标逐坐标一致；def2/J、RIJCOSX；SCF恢复辅助设置已披露，未换泛函/基组追值|
|复合G|SI Eq.S1：高层电子能加method1零点、热/熵项|G7=E_SP7+(G1−E1)，RRHO 298.15 K；不得将单点E或扫描E冒充G|
|标准态|1 atm、298.15 K转1 M，每物种加RT ln(RT/(0.001 m³·101325 Pa))|独立重算为1.8943284455 kcal/mol；候选RT ln(24.46)=1.8941975683。双分子缔合的本次值比候选低0.0001308772，同分子数差不变|
|反应参照|阴离子相对底物+MeS−；中性加成物相对底物+MeSH；第二次加成相对单加成物+MeSH|逐项元素和电荷配平；不插入裸质子能量，不混用二次增量与总形成能|
|作者构象/高层扩展|改进CREST/xTB、GFN2/ALPB氯仿、BP86/dgauss-dzvp、COSMO-RS筛选，常取10个再优化；比较methods 2–9含DLPNO-CCSD(T)|本验证使用已公开选定来源构象及method1/7两模型，未声称复现全局构象搜索、所有方法或全部路径；这些也不是额外评分目标|
|路径|作者对除质子化/去质子化外路径用TS或扫描，部分解释使用IBO/Fukui|实际核对两个α-TS的频率/模式/源连接；补足R5局部γ释放及R6十二点γ受约束扫描，不宣称全IRC、精确γ-G势垒或全部初始加成无势垒|

1. 在已公开作者结构上执行method1优化/频率，再在其最终几何执行method7单点；原生日志与输入路径逐态列于下文。MeS−的频率来源为独立`local_preflight/native.log`，已纳入32组，未漏算。
2. 从日志重新提取E、G、频率、收敛判据、最终坐标，对照来源元素/键图及电荷；解析两个α-TS Hessian反应振型，核对开链→TS→闭环的目标C–O变化。四个历史失败单点均已有成功替代，失败值不进入计算。
3. 逐态重算G7，再按配平计量关系和统一标准态求反应能；对method1与method7的中性产物分别排序。32组G7与候选逐态完全相等，只有上述标准态常数造成0.0001308772 kcal/mol级的双分子反应差。
4. R5由来源中性环结构删H38，构造已披露的−1单重态局部种子并无约束释放；R6由有效环阴离子沿C5–O24做十二点反向扫描。下方保留有限路径和数值质量边界。本轮迁移只重用/审查既有结果，未新跑QC/HPC，亦不是信息受限的Agent盲测。

### 全部29项反应或局部比较

差值统一为本次−作者。作者数值取Figure S8和Schemes 12–15，R5第二次加成约−2；`—`表示本项未在审计中指定独立精确作者标量，不伪造残差。本次不是新量化计算，而是从既有原生日志按精确1 M常数重算。所有量均为298.15 K自由能，只有随后γ扫描表是电子能。以上及下表的数字是审查上下文，现行13项semantic规则没有精确命中窗口。

| 物理量/来源态（计量见下） | 定义 | 作者 kcal/mol | 本次 kcal/mol | 本次−作者 |
| --- | --- | --- | --- | --- |
| R5_SMe1_-1_1 anion formation | G7 | 2.400000 | 2.496105 | +0.096105 |
| R5_SMe4_-1_1 anion formation | G7 | -1.200000 | -1.094467 | +0.105533 |
| R5_SMe6_-1_1 anion formation | G7 | -5.400000 | -5.335140 | +0.064860 |
| R6_SMe1_-1_1 anion formation | G7 | 2.800000 | 2.870589 | +0.070589 |
| R6_SMe4_-1_1 anion formation | G7 | 0.900000 | 1.042967 | +0.142967 |
| R6_SMe6_-1_1 anion formation | G7 | -1.700000 | -1.579859 | +0.120141 |
| Sulf_SMe1_2_c80_-1_1 anion formation | G7 | -0.800000 | -0.644624 | +0.155376 |
| Sulf_SMe4_c13_-1_1 anion formation | G7 | -13.600000 | -13.446617 | +0.153383 |
| Sulf_SMe6_-1_1 anion formation | G7 | -6.300000 | -6.253699 | +0.046301 |
| Sulf_SMe4_2_-1_1 anion formation | G7 | -10.500000 | -10.389427 | +0.110573 |
| Sulf_SMe1_P2_0_1 neutral formation | G7 | -5.400000 | -5.246023 | +0.153977 |
| Sulf_SMe4_P2_0_1 neutral formation | G7 | -10.900000 | -10.657220 | +0.242780 |
| Sulf_SMe6_P2_0_1 neutral formation | G7 | -9.700000 | -9.504835 | +0.195165 |
| R6_SMe1_P2_0_1 neutral formation | G7 | -4.200000 | -3.969305 | +0.230695 |
| R6_SMe6_P2_0_1 neutral formation | G7 | -2.400000 | -2.184421 | +0.215579 |
| R6_SMe4_P1SS_0_1 neutral formation | G7 | -3.700000 | -3.461160 | +0.238840 |
| R6_SMe6_cyc2SP1_0_1 neutral formation | G7 | -7.400000 | -7.191506 | +0.208494 |
| R6_SMe6_cyc4P2_0_1 neutral formation | G7 | -17.300000 | -17.048414 | +0.251586 |
| R6_SMe6_cyc2P2_0_1 neutral formation | G7 | -17.500000 | -17.230963 | +0.269037 |
| R6 cyclic anion formation | G7 | 1.900000 | 1.983322 | +0.083322 |
| R6 cyclic2S minus addition anion6 | G7 | 3.600000 | 3.563182 | -0.036818 |
| R5 second thiol addition | G7 | -2.000000 | -2.141685 | -0.141685 |
| R5 ring4 local barrier at method1 | G1 | — | 37.264374 | — |
| R5 ring4 TS vs common reactants | G7 | 30.200000 | 30.066801 | -0.133199 |
| R6 ring4 local barrier at method1 | G1 | — | 28.278727 | — |
| R6 ring4 TS vs common reactants | G7 | 25.900000 | 25.717420 | -0.182580 |
| R5 alpha ring4 local method7 barrier | G7 | 35.600000 | 35.401941 | -0.198059 |
| R6 alpha ring4 local method7 barrier | G7 | 27.600000 | 27.297280 | -0.302720 |
| R5 cyclic4P2 minus simpledelta product | G7 | — | -1.469429 | — |

### R5正文与SI图中端点的补充直接核对

进一步直接查看正文PDF第8页Scheme 12及SI PDF第34页Figure S8，确认以下method7图示端点。前三个简单产物是同一套配平比较；不是从正文“约−4”反推具体值。后两项明确区分环/双加成总形成能与局部第二步增量。

|物理量（G7，298.15 K/1 M）|作者图值 kcal/mol|本次 kcal/mol|本次−图值 kcal/mol|
|---|---|---|---|
|R5 δ简单产物 R5_SMe1_P2A_0_1，相对R5+MeSH|−4.3|−4.076954|+0.223046|
|R5 α简单产物 R5_SMe4_P1SR_0_1，相对R5+MeSH|−4.1|−3.871675|+0.228325|
|R5 β′简单产物 R5_SMe6_P2_0_1，相对R5+MeSH|−3.4|−3.137208|+0.262792|
|R5假设环产物 R5_SMe6_cyc4P2_0_1，相对R5+MeSH|−5.8|−5.546383|+0.253617|
|R5双加成产物 R5_SMe1_P2A_SMe6S_P2，相对R5+2MeSH|−6.6|−6.218638|+0.381362|

正文对第二次加成用“约−2 kcal/mol”的近似描述，对照本次−2.141685的差为−0.141685；图示已舍入端点相减则为−6.6−(−4.3)=−2.3，对照差为+0.158315。二者并列保留，不能把来源近似表述当高精度目标，也不能将双加成总形成能−6.218638当第二次加成增量。图示环端点减简单δ产物为−1.5，本次−1.469429，差+0.030571；仅说明终点接近，不提供可达性证据。

### 各比较的计量定义

| 量 | 配平线性组合（正号产物，负号参照） |
| --- | --- |
| R5_SMe1_-1_1 anion formation | +1 R5_SMe1_-1_1; -1 R5_0_1; -1 SMe_-1_1 |
| R5_SMe4_-1_1 anion formation | +1 R5_SMe4_-1_1; -1 R5_0_1; -1 SMe_-1_1 |
| R5_SMe6_-1_1 anion formation | +1 R5_SMe6_-1_1; -1 R5_0_1; -1 SMe_-1_1 |
| R6_SMe1_-1_1 anion formation | +1 R6_SMe1_-1_1; -1 R6_0_1; -1 SMe_-1_1 |
| R6_SMe4_-1_1 anion formation | +1 R6_SMe4_-1_1; -1 R6_0_1; -1 SMe_-1_1 |
| R6_SMe6_-1_1 anion formation | +1 R6_SMe6_-1_1; -1 R6_0_1; -1 SMe_-1_1 |
| Sulf_SMe1_2_c80_-1_1 anion formation | +1 Sulf_SMe1_2_c80_-1_1; -1 Sulf_0_1; -1 SMe_-1_1 |
| Sulf_SMe4_c13_-1_1 anion formation | +1 Sulf_SMe4_c13_-1_1; -1 Sulf_0_1; -1 SMe_-1_1 |
| Sulf_SMe6_-1_1 anion formation | +1 Sulf_SMe6_-1_1; -1 Sulf_0_1; -1 SMe_-1_1 |
| Sulf_SMe4_2_-1_1 anion formation | +1 Sulf_SMe4_2_-1_1; -1 Sulf_0_1; -1 SMe_-1_1 |
| Sulf_SMe1_P2_0_1 neutral formation | +1 Sulf_SMe1_P2_0_1; -1 Sulf_0_1; -1 SMe_0_1 |
| Sulf_SMe4_P2_0_1 neutral formation | +1 Sulf_SMe4_P2_0_1; -1 Sulf_0_1; -1 SMe_0_1 |
| Sulf_SMe6_P2_0_1 neutral formation | +1 Sulf_SMe6_P2_0_1; -1 Sulf_0_1; -1 SMe_0_1 |
| R6_SMe1_P2_0_1 neutral formation | +1 R6_SMe1_P2_0_1; -1 R6_0_1; -1 SMe_0_1 |
| R6_SMe6_P2_0_1 neutral formation | +1 R6_SMe6_P2_0_1; -1 R6_0_1; -1 SMe_0_1 |
| R6_SMe4_P1SS_0_1 neutral formation | +1 R6_SMe4_P1SS_0_1; -1 R6_0_1; -1 SMe_0_1 |
| R6_SMe6_cyc2SP1_0_1 neutral formation | +1 R6_SMe6_cyc2SP1_0_1; -1 R6_0_1; -1 SMe_0_1 |
| R6_SMe6_cyc4P2_0_1 neutral formation | +1 R6_SMe6_cyc4P2_0_1; -1 R6_0_1; -1 SMe_0_1 |
| R6_SMe6_cyc2P2_0_1 neutral formation | +1 R6_SMe6_cyc2P2_0_1; -1 R6_0_1; -1 SMe_0_1 |
| R6 cyclic anion formation | +1 R6_SMe6_cyc2S_-1_1; -1 R6_0_1; -1 SMe_-1_1 |
| R6 cyclic2S minus addition anion6 | +1 R6_SMe6_cyc2S_-1_1; -1 R6_SMe6_-1_1 |
| R5 second thiol addition | +1 R5_SMe1_P2A_SMe6S_P2; -1 R5_SMe1_P2A_0_1; -1 SMe_0_1 |
| R5 ring4 local barrier at method1 | +1 R5_SMe6_cyc4RTS_-1_1; -1 R5_SMe6_-1_1 |
| R5 ring4 TS vs common reactants | +1 R5_SMe6_cyc4RTS_-1_1; -1 R5_0_1; -1 SMe_-1_1 |
| R6 ring4 local barrier at method1 | +1 R6_SMe6_cyc4RTS_-1_1; -1 R6_SMe6_-1_1 |
| R6 ring4 TS vs common reactants | +1 R6_SMe6_cyc4RTS_-1_1; -1 R6_0_1; -1 SMe_-1_1 |
| R5 alpha ring4 local method7 barrier | +1 R5_SMe6_cyc4RTS_-1_1; -1 R5_SMe6_-1_1 |
| R6 alpha ring4 local method7 barrier | +1 R6_SMe6_cyc4RTS_-1_1; -1 R6_SMe6_-1_1 |
| R5 cyclic4P2 minus simpledelta product | +1 R5_SMe6_cyc4P2_0_1; -1 R5_SMe1_P2A_0_1 |

### 实际两方法比较及全部排序数值

下表均相对各自底物+MeSH、298.15 K/1 M。R5作者正文仅概述简单产物约−4 kcal/mol和方法改序，未给本表method1逐态的精确比较标量；不以近似−4计算虚假的精确残差。method7精确图示对照见前面29项表及R5补充端点表。

| 体系 | 自由能模型 | 次序（低至高） | 状态 | 形成G kcal/mol |
| --- | --- | --- | --- | --- |
| Sulf | G1 | 1 | Sulf_SMe4_P2_0_1 | -7.692334 |
| Sulf | G1 | 2 | Sulf_SMe6_P2_0_1 | -7.072555 |
| Sulf | G1 | 3 | Sulf_SMe1_P2_0_1 | -1.282657 |
| Sulf | G7 | 1 | Sulf_SMe4_P2_0_1 | -10.657220 |
| Sulf | G7 | 2 | Sulf_SMe6_P2_0_1 | -9.504835 |
| Sulf | G7 | 3 | Sulf_SMe1_P2_0_1 | -5.246023 |
| R5 | G1 | 1 | R5_SMe6_P2_0_1 | -0.142002 |
| R5 | G1 | 2 | R5_SMe1_P2A_0_1 | 0.580487 |
| R5 | G1 | 3 | R5_SMe4_P1SR_0_1 | 1.214906 |
| R5 | G7 | 1 | R5_SMe1_P2A_0_1 | -4.076954 |
| R5 | G7 | 2 | R5_SMe4_P1SR_0_1 | -3.871675 |
| R5 | G7 | 3 | R5_SMe6_P2_0_1 | -3.137208 |
| R6 | G1 | 1 | R6_SMe6_cyc4P2_0_1 | -8.743249 |
| R6 | G1 | 2 | R6_SMe6_cyc2P2_0_1 | -7.347392 |
| R6 | G1 | 3 | R6_SMe6_P2_0_1 | 0.812747 |
| R6 | G1 | 4 | R6_SMe1_P2_0_1 | 1.251326 |
| R6 | G1 | 5 | R6_SMe4_P1SS_0_1 | 1.432419 |
| R6 | G7 | 1 | R6_SMe6_cyc2P2_0_1 | -17.230963 |
| R6 | G7 | 2 | R6_SMe6_cyc4P2_0_1 | -17.048414 |
| R6 | G7 | 3 | R6_SMe1_P2_0_1 | -3.969305 |
| R6 | G7 | 4 | R6_SMe4_P1SS_0_1 | -3.461160 |
| R6 | G7 | 5 | R6_SMe6_P2_0_1 | -2.184421 |

R5的最低简单产物从method1的β′变成method7的δ；这直接支持来源报告的选择性不稳健。R6两方法都把环产物类别排在简单产物之前，但两个环终点内部次序改变；不能由最低端点单独选择动力学通道。Sulf的α/SMe6/SMe1中性产物次序在两个模型下保持，因此其有限模型下的方向比R5稳健；并非所有泛函/构象均已验证。

### α-TS与γ路径的身份、模式和数值

|对象|原生验证|源/本次对照与含义|
|---|---|---|
|R5 α-TS|唯一虚频−575.194738 cm⁻¹；C4–O8模式投影导数−0.957726|源open→本次TS→源closed键长4.370504→1.841545→1.456263 Å；G7局部35.401941对35.6，差−0.198059 kcal/mol|
|R6 α-TS|唯一虚频−537.688114 cm⁻¹；C15–O24投影+0.897947|4.168520→1.897219→1.446206 Å；G7局部27.297280对27.6，差−0.302720 kcal/mol|
|R5 γ释放|作者中性结构删C1上的H38，原C–H=1.089828 Å，前37原子坐标不变；这是重构阴离子种子|C2–O8从1.469834到2.762129 Å；返回有效open同图，重原子RMSD0.024198 Å，ΔE+0.026366、ΔG−0.014132 kcal/mol；0虚频且力判据通过|
|R6 γ路径|C5–O24从1.60791479扫到2.60000000 Å，十二个受约束点全部原生收敛|最高采样电子能相对共同open=9.564782，相对扫描自身open=9.855078；匹配method1 α电子势垒=29.132496 kcal/mol|

α-TS的虚频符号任意，反应模式和连接为依据；两个源连接图各仅多一根对应成环C–O键，未追加全IRC。R5局部开环与作者描述相符，但它不是作者已经优化的γ阴离子，不能证明所有γ途径不存在。R6扫描开环电子能单调下降，反向闭环是上坡；有限间距不能排除未采样窄峰，因此不是精确γ-ΔG‡或“γ闭环无势垒”证明。扫描末端与旧open同图但构象不同，重原子RMSD0.700980 Å、ΔE−0.290296 kcal/mol；不可忽略参照变化。

| 点 | C5–O24 / Å | 电子能 / Eh | 相对共同open / kcal/mol | 受约束原生收敛 |
| --- | --- | --- | --- | --- |
| 1 | 1.60791479 | -1357.324454543584 | 9.564782 | True |
| 2 | 1.69810435 | -1357.324468136610 | 9.556252 | True |
| 3 | 1.78829391 | -1357.325066057683 | 9.181051 | True |
| 4 | 1.87848348 | -1357.326771489465 | 8.110876 | True |
| 5 | 1.96867304 | -1357.329290744195 | 6.530020 | True |
| 6 | 2.05886262 | -1357.331893912023 | 4.896508 | True |
| 7 | 2.14905218 | -1357.334347373789 | 3.356937 | True |
| 8 | 2.23924175 | -1357.336523932442 | 1.991126 | True |
| 9 | 2.32943131 | -1357.338221848588 | 0.925667 | True |
| 10 | 2.41962087 | -1357.339390165329 | 0.192538 | True |
| 11 | 2.50981044 | -1357.340039983267 | -0.215229 | True |
| 12 | 2.60000000 | -1357.340159609387 | -0.290296 | True |

### 定性结论逐项对照及原生质量边界

|科学命题|作者结论|实际计算及可接受的限定|
|---|---|---|
|R5初始位点|所展示β′阴离子最低|β′/α/δ形成G=−5.335140/−1.094467/+2.496105，支持初始阴离子比较；不替代中性产物偏好|
|R5简单产物|method7下δ对应产物最低，能差小且换方法改序|method7 δ/α/β′=−4.076954/−3.871675/−3.137208；method1最低β′；不能可靠预测独占δ产物|
|R5简单/环化|α势垒高，γ局部结构回开链；假设环端点低也不保证可达|α局部35.401941；γ重构释放回open；假设cyc4P2比δ简单物低1.469429，仍不推出环化优先|
|R5二次加成|计算略有利，却不完全解释EtSH实验|MeSH第二步−2.141685，保留弱竞争和实验不符，不能把作者局限当缺算，也不从该数推出速率|
|R6初始位点|正文第11页说δ最低；图/SI所列β′最低|本次β′/α/δ=−1.579859/+1.042967/+2.870589；保留来源歧义，不以矛盾正文设唯一排序答案|
|R6终点稳定性|环化端点约−18，低于简单端点约−4|γ/α环端点−17.230963/−17.048414；简单最低−3.969305；两环端点内部次序可改，不改变类别差|
|R6相对可达性|γ方向比α方向容易，不能仅从端点选择|有限γ电子路径最高9.564782<匹配α电子势垒29.132496；环阴离子相对open的G7上升3.563182对作者3.6；不混E与G|
|Sulf位点和产物|α阴离子及α简单中性产物较稳定|两α阴离子−13.446617/−10.389427低于SMe6−6.253699及SMe1−0.644624；中性α偏好在method1/7保持|
|Sulf身份|指定E appendage，母体2Z/4E|C22H20O6S；dienoate/sulfonyl诊断二面角源−175.379251°、本次−175.351365°；Ph/sulfonyl源+7.656350°、本次+7.622698°；母体诊断约+1.958820°/+179.646621°|
|综合解释|稳定性和受限成环可达性共同解释三个体系，但R5预测较弱|三组结果与有限模型敏感性足够形成限定比较；未复现完整唯一动力学、所有初始进攻无势垒或作者约7–8 kcal/mol缔合自由能势垒|

**SCF必须独立审数值。** 选用日志全部正常终止并原生宣告SCF收敛，使用Total+1el-Energy，即ConvCheckMode 2。它以总能与单电子能检查，不能改写成“所有SCF阈值通过”，也不是ConvCheckMode 1。Sulf_SMe4_P2_0_1的method7在146轮结束，末次ΔE=7.1907×10⁻⁷ Eh（阈值10⁻⁶），但MAX/RMS density=0.22963/0.0072282（阈值10⁻⁵/10⁻⁶），DIIS=0.0059316，orbital gradient=0.00042272（阈值0.00005），rotation=0.00083656。其他来源态也有部分密度/DIIS残差超阈值；不能把方法原生宣布收敛理解为全判据轨道收敛。完整逐态残差在raw_arithmetic.json，现材料没有以改容差处理它们。

**更正small-step物种归属。** 使用原生small-step替代收敛的是中性母体R6_0_1：MAX gradient=0.0005810986>0.0003000000，RMS gradient=0.0000965836、RMS step=0.0004259295、MAX step=0.0013192807通过，零虚频。R6_SMe6_cyc2S_-1_1环阴离子四项均通过：RMS gradient=0.0000426384、MAX gradient=0.0002265130、RMS step=0.0003957531、MAX step=0.0021108073，零虚频。历史候选文字将它归给环阴离子有误；本说明采用独立审计更正。

本题必要结果完整不等于严格数值全一致，也不等于专家批准发布。未增设全Tight/ConvCheckMode 0门，未把R5弱选择性变成强选择性验收条件。方法、版本、有限构象、来源歧义和数值残差均留给专家评估。

### 逐态输入输出及原生核验位置

下列32组均为实际method1 Opt/Freq及method7 SP配对。输入和输出是服务器上的真实文件；SHA-256及完整频率、SCF残差、最终坐标由[raw_arithmetic.json](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/sulf_review/raw_arithmetic.json)逐态保存。四个历史失败单点位于其中`historical_failed_stages`，不用于本次数值。

- `SMe_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/SMe_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/SMe_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/SMe_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/SMe_0_1/method7.log)。
- `R5_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/R5_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/R5_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/R5_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/R5_0_1/method7.log)。
- `R6_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/R6_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/R6_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_0_1/method7.log)。
- `Sulf_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T2343Z/targeted_repair/Sulf_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T2343Z/targeted_repair/Sulf_0_1/method7.log)。
- `R5_SMe1_P2A_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe1_P2A_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe1_P2A_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe1_P2A_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe1_P2A_0_1/method7.log)。
- `R5_SMe6_P2_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe6_P2_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe6_P2_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe6_P2_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe6_P2_0_1/method7.log)。
- `R5_SMe4_P1SR_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe4_P1SR_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe4_P1SR_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe4_P1SR_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe4_P1SR_0_1/method7.log)。
- `R5_SMe1_P2A_SMe6S_P2`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe1_P2A_SMe6S_P2/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe1_P2A_SMe6S_P2/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe1_P2A_SMe6S_P2/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe1_P2A_SMe6S_P2/method7.log)。
- `R5_SMe6_cyc4P2_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe6_cyc4P2_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe6_cyc4P2_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe6_cyc4P2_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe6_cyc4P2_0_1/method7.log)。
- `R6_SMe1_P2_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe1_P2_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe1_P2_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe1_P2_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe1_P2_0_1/method7.log)。
- `R6_SMe6_P2_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_P2_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_P2_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_P2_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_P2_0_1/method7.log)。
- `R6_SMe4_P1SS_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe4_P1SS_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe4_P1SS_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe4_P1SS_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe4_P1SS_0_1/method7.log)。
- `R6_SMe6_cyc4P2_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_cyc4P2_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_cyc4P2_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_cyc4P2_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_cyc4P2_0_1/method7.log)。
- `R6_SMe6_cyc2P2_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_cyc2P2_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_cyc2P2_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_cyc2P2_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_cyc2P2_0_1/method7.log)。
- `Sulf_SMe1_P2_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_SMe1_P2_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_SMe1_P2_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/sulf_product_repair_bundle/calculation/Sulf_SMe1_P2_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/sulf_product_repair_bundle/calculation/Sulf_SMe1_P2_0_1/method7.log)。
- `Sulf_SMe4_P2_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_SMe4_P2_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_SMe4_P2_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1550Z/new44_group_01/papers/paper_fb75113b35e12c7c/sulf_sme4_soscf_activation/calculation/Sulf_SMe4_P2_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1550Z/new44_group_01/papers/paper_fb75113b35e12c7c/sulf_sme4_soscf_activation/calculation/Sulf_SMe4_P2_0_1/method7.log)。
- `Sulf_SMe6_P2_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_SMe6_P2_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_SMe6_P2_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_SMe6_P2_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_SMe6_P2_0_1/method7.log)。
- `SMe_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/local_preflight/preflight.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/local_preflight/native.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/SMe_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/SMe_-1_1/method7.log)。
- `R5_SMe1_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe1_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe1_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe1_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe1_-1_1/method7.log)。
- `R5_SMe4_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe4_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe4_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe4_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe4_-1_1/method7.log)。
- `R5_SMe6_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe6_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe6_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe6_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe6_-1_1/method7.log)。
- `R6_SMe1_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe1_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe1_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe1_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe1_-1_1/method7.log)。
- `R6_SMe4_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe4_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe4_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe4_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe4_-1_1/method7.log)。
- `R6_SMe6_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_-1_1/method7.log)。
- `Sulf_SMe1_2_c80_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe1_2_c80_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe1_2_c80_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe1_2_c80_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe1_2_c80_-1_1/method7.log)。
- `Sulf_SMe4_c13_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe4_c13_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe4_c13_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe4_c13_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe4_c13_-1_1/method7.log)。
- `Sulf_SMe6_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe6_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe6_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe6_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe6_-1_1/method7.log)。
- `Sulf_SMe4_2_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe4_2_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe4_2_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe4_2_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe4_2_-1_1/method7.log)。
- `R5_SMe6_cyc4RTS_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe6_cyc4RTS_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe6_cyc4RTS_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0140Z/new44_group_01/papers/paper_fb75113b35e12c7c/ring_TS_missing_method7/calculation/R5_SMe6_cyc4RTS_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0140Z/new44_group_01/papers/paper_fb75113b35e12c7c/ring_TS_missing_method7/calculation/R5_SMe6_cyc4RTS_-1_1/method7.log)。
- `R6_SMe6_cyc4RTS_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_cyc4RTS_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_cyc4RTS_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0140Z/new44_group_01/papers/paper_fb75113b35e12c7c/ring_TS_missing_method7/calculation/R6_SMe6_cyc4RTS_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0140Z/new44_group_01/papers/paper_fb75113b35e12c7c/ring_TS_missing_method7/calculation/R6_SMe6_cyc4RTS_-1_1/method7.log)。
- `R6_SMe6_cyc2S_-1_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_cyc2S_-1_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_cyc2S_-1_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_cyc2S_-1_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_cyc2S_-1_1/method7.log)。
- `R6_SMe6_cyc2SP1_0_1`：[Opt/Freq输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_cyc2SP1_0_1/optfreq.inp)；[Opt/Freq日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_cyc2SP1_0_1/optfreq.log)；[SP输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_cyc2SP1_0_1/method7.inp)；[SP日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_cyc2SP1_0_1/method7.log)。
- `R5_gamma`：[输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_01/papers/paper_fb75113b35e12c7c/gamma_accessibility_source_checks/calculation/R5_gamma_deprotonated_source_release/optfreq.inp)；[原生日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_01/papers/paper_fb75113b35e12c7c/gamma_accessibility_source_checks/calculation/R5_gamma_deprotonated_source_release/optfreq.log)；SHA-256 `21ebf4843c2c82bb148a9193fa13a52c9ff8ede125e02c7a7388d2cc0ec628cb`。
- `R6_gamma`：[输入](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_01/papers/paper_fb75113b35e12c7c/gamma_accessibility_source_checks/calculation/R6_gamma_source_opening_scan/gamma_ring_opening_scan.inp)；[原生日志](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_01/papers/paper_fb75113b35e12c7c/gamma_accessibility_source_checks/calculation/R6_gamma_source_opening_scan/gamma_ring_opening_scan.log)；SHA-256 `1bddf99dd35a96a18ceb2e2ac7b8ce66c092de469509449d86ddef6ae3ab895c`。

[独立重算脚本](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/sulf_review/recompute.py)；[机器可读审计](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/sulf_review/audit.json)；[独立审计全文](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/sulf_review/audit.md)。

[父级更正后作者比较](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/new44_group_01/papers/paper_fb75113b35e12c7c/author_comparison.json)；[现行覆盖矩阵](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/new44_group_01/papers/paper_fb75113b35e12c7c/verification_matrix.json)；[更正后gamma收据](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/new44_group_01/papers/paper_fb75113b35e12c7c/gamma_accessibility_receipt.json)；[标准态常数对照](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/new44_group_01/papers/paper_fb75113b35e12c7c/standard_state_reconciliation.json)。


---

# 历史计算记录（保留原文，非当前状态或计分规则）

# Independent computation verification — 2026-10-22 follow-up

Current shared AR/PR status: **INCOMPLETE**; completed components do not establish a whole-question pass.

Assigned original snapshot: `e03f12d65e1f06333d9e097b896da1e543aee9cf27af596383443341dd24d23b`. Evidence directory: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T2343Z`.

R6 method7 repaired successfully. Sulf Opt/Freq and three R5 monoaddition optfreq/SP pairs also completed. Sulf method7 diverged and reached controlled3h bound; only that SP is being repaired. Healthy predecessor continues missing products. Composite G is method7 electronic energy plus matching B3LYP thermal correction; balanced1M corrections required. Current final conclusions including accessibility/anion/cyclization remain incomplete.

Native completed stages (final-state validity only; TS reaction interpretation and minima identity are separate):

| Case | Stage | Electronic energy / Eh | Native RRHO G / Eh | Imaginary modes | Wall seconds |
|---|---|---:|---:|---:|---:|
| SMe_0_1 | optfreq | -438.662176240826 | -438.64074149 | 0 | 39.88 |
| SMe_0_1 | method7 | -438.678367995805 | — | — | 7.68 |
| R5_0_1 | optfreq | -879.84905807132 | -879.64489978 | 0 | 517.15 |
| R5_0_1 | method7 | -879.978395557855 | — | — | 295.30 |
| R6_0_1 | optfreq | -919.154640838453 | -918.92224801 | 0 | 581.28 |
| R6_0_1 | method7 | -919.285089357228 | — | — | 633.37 |
| Sulf_0_1 | optfreq | -1699.736806312661 | -1699.41542314 | 0 | 2149.28 |
| R5_SMe1_P2A_0_1 | optfreq | -1318.533069777864 | -1318.2816974 | 0 | 767.85 |
| R5_SMe1_P2A_0_1 | method7 | -1318.686021123952 | — | — | 772.43 |
| R5_SMe6_P2_0_1 | optfreq | -1318.53652809156 | -1318.28284876 | 0 | 826.45 |
| R5_SMe6_P2_0_1 | method7 | -1318.686830498476 | — | — | 700.01 |
| R5_SMe4_P1SR_0_1 | optfreq | -1318.532542271273 | -1318.28068639 | 0 | 788.23 |
| R5_SMe4_P1SR_0_1 | method7 | -1318.686177495238 | — | — | 710.09 |

Author comparison (calculated minus author; numerical tolerances unmodified):

| Quantity | Author | Calculated | Signed difference | Absolute difference | Units |
|---|---:|---:|---:|---:|---|

Frozen computational provenance:

- Job `hpc-job-ec3cb818-8eca-4fb5-92af-ff63029cf47f`: `STOPPED` at `2026-10-22T23:53:24.545156+00:00`; frozen spec `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/job_spec.json`; native audit `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T2343Z/job_audits/hpc-job-ec3cb818-8eca-4fb5-92af-ff63029cf47f/native_audit.json`.
- Job `hpc-job-a2441722-1602-4082-bacc-366b4b923ce1`: `RUNNING` at `2026-10-22T23:53:19.960376+00:00`; frozen spec `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/job_spec.json`; native audit `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T2343Z/job_audits/hpc-job-a2441722-1602-4082-bacc-366b4b923ce1/native_audit.json`.
- Job `hpc-job-e3432927-f0bc-4db0-828d-a10403cb399f`: `CREATING` at `2026-10-22T23:53:20.377435+00:00`; frozen spec `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T2343Z/targeted_repair/job_spec.json`; native audit `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T2343Z/job_audits/hpc-job-e3432927-f0bc-4db0-828d-a10403cb399f/native_audit.json`.

Completed application logs:

- SMe_0_1/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/SMe_0_1/optfreq.log`, SHA256 `e3872ad63c9a17906df398013edd82b5fa415912554ec511849fda904e910e92`; return code `0`, normal termination `True`.
- SMe_0_1/method7: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/SMe_0_1/method7.log`, SHA256 `b39b1b4c8a1220ad559278344adb53b6ca3265e45bcf0a707c2997446034b7d3`; return code `0`, normal termination `True`.
- R5_0_1/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/R5_0_1/optfreq.log`, SHA256 `3055e79ec63844e7673a366a28ea94c88358641ad506112094c2d9457726ec31`; return code `0`, normal termination `True`.
- R5_0_1/method7: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/R5_0_1/method7.log`, SHA256 `4e42931a6926a212c759da2d1351ad4c4bcf1c0eecb2745f57d931180f04847b`; return code `0`, normal termination `True`.
- R6_0_1/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/new44_20261022/calculation/R6_0_1/optfreq.log`, SHA256 `9428fb96019add5fc21f3e98fc19c2fdd9ae6a5874ef1ba4548eb544674db033`; return code `0`, normal termination `True`.
- R6_0_1/method7: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_0_1/method7.log`, SHA256 `ccad49efd1e961c11774fc3eaf8b9e5fcb68135edb373ed1a466122f627d88fc`; return code `0`, normal termination `True`.
- Sulf_0_1/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_0_1/optfreq.log`, SHA256 `aefc51dc32bd2ba7dfdec2ff2cd4625f5b6494b5ccd5754b4e51752ad2d6fc77`; return code `0`, normal termination `True`.
- R5_SMe1_P2A_0_1/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe1_P2A_0_1/optfreq.log`, SHA256 `6175f1a8a536bfb026582c9df4da458bf12c43e315c4cf37b88c7b9943501eb5`; return code `0`, normal termination `True`.
- R5_SMe1_P2A_0_1/method7: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe1_P2A_0_1/method7.log`, SHA256 `b90bffbbaa124e176cef047086ea63894b16cd08918c758af15345b16676cc96`; return code `0`, normal termination `True`.
- R5_SMe6_P2_0_1/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe6_P2_0_1/optfreq.log`, SHA256 `77c0bd4c01a3c1d806d141a5eaafadda0c5e24e78dc8073dc2129bd6eab65bc3`; return code `0`, normal termination `True`.
- R5_SMe6_P2_0_1/method7: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe6_P2_0_1/method7.log`, SHA256 `474c8cee7b4e82e0b282ea6ead980c014b9eff4caecdcaf4dfa36adc931149b3`; return code `0`, normal termination `True`.
- R5_SMe4_P1SR_0_1/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe4_P1SR_0_1/optfreq.log`, SHA256 `c4e40e493de82ee5da21eab40e8621a427558f5d02abbc3438f141dd26c72e66`; return code `0`, normal termination `True`.
- R5_SMe4_P1SR_0_1/method7: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe4_P1SR_0_1/method7.log`, SHA256 `7c99540769d1fcf94784bd315164cbc320361fac53b445ba09f1645008a95bfb`; return code `0`, normal termination `True`.

Source/method deviations remain in the frozen specs and `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T2343Z/author_comparison.json`. For optimized final geometries, graph checks, atom maps and hashes see `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T2343Z/completed_verified_stages.json`. Whole-question coverage and pending work: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/short_job_followup_20261022T2343Z/new44_group_01/coverage.json`. No task text, scoring, tolerances, expert packages or global counts were modified.

## Follow-up 2026-10-23T0033Z — new returned evidence

Current whole-question status remains **INCOMPLETE**. 新完成R5双加成产物Opt/Freq及method7单点（1201.34/1537.27秒），另一个R5环化极小值Opt/Freq完成（826.54秒）；零虚频、源完整键图一致。使用method7电子能+B3LYP热校正，并对2→1结合加−RTln(24.46)=−1.894198kcal/mol，双加成相对P2A单加成+MeSH的ΔG1M=−2.141554kcal/mol，作者约−2，差−0.141554。对另外两个已算单加成参考为−3.081299/−2.346832；这支持温和热力学驱动，不是反应势垒或速率。Sulf既有SP修复与原剩余产物继续；DIIS转SOSCF后有能量回跳、尚未收敛，详见active_native_progress.json，仍在原有界作业内，未重复提交。

| Case | Stage | Electronic E / Eh | Native RRHO G / Eh | Imaginary count | Wall seconds |
|---|---|---:|---:|---:|---:|
| R5_SMe1_P2A_SMe6S_P2 | optfreq | -1757.220488002557 | -1756.91884039 | 0 | 1201.34 |
| R5_SMe1_P2A_SMe6S_P2 | method7 | -1757.393623791039 | — | — | 1537.27 |
| R5_SMe6_cyc4P2_0_1 | optfreq | -1318.533985819831 | -1318.27847134 | 0 | 826.54 |

All new stages have native return code0 and normal termination; optimization, frequencies and formula/connectivity checks were separately inspected.

- `hpc-job-a2441722-1602-4082-bacc-366b4b923ce1`, R5_SMe1_P2A_SMe6S_P2/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe1_P2A_SMe6S_P2/optfreq.log`, SHA256 `94c2499046a65ed932f8257040dbfe3eefc6871ff2b5f7cfbf1f936ca215f858`.
- `hpc-job-a2441722-1602-4082-bacc-366b4b923ce1`, R5_SMe1_P2A_SMe6S_P2/method7: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe1_P2A_SMe6S_P2/method7.log`, SHA256 `3ba08ed21f086e1f2c192669255258177cd99d00a821df07c52e30ae58fba7ab`.
- `hpc-job-a2441722-1602-4082-bacc-366b4b923ce1`, R5_SMe6_cyc4P2_0_1/optfreq: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe6_cyc4P2_0_1/optfreq.log`, SHA256 `7693b2085431b5caf5219ff55fdcc976a95c4ce480cb2da9e0d6f9e3edcc600c`.

New evidence and comparison: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T0033Z/new44_group_01/new_results.json`, `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0033Z/author_comparison.json`. Current per-paper required coverage: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T0033Z/new44_group_01/coverage.json`. Objective-blocker accounting: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T0033Z/new44_group_01/blocker_inventory.json`. Existing failure/successor lineage is preserved. No source physics, evaluator or numerical tolerance changed.

## Service recovery 2026-10-23T0149Z — returned Sulf evidence

Current whole-question status: **INCOMPLETE; no acceptance candidate**. 本节用新返回原生日志更新0033轮的Sulf运行状态；此前记录保留为历史。

Sulf原后继 `hpc-job-e3432927-f0bc-4db0-828d-a10403cb399f` 平台SUCCEEDED，returncode=0、144次SCF后正常收敛、ORCA正常终止；method7最终E=-1699.959077405263 Eh，6530.54秒（108.84min）。成功Opt/Freq的几何与GBW完全复用，哈希与前序及冻结spec一致。物理方法不变。

日志明确使用Total+1el-Energy默认收敛：能量变化7.2342e−7 Eh，小于1e−6；MAX/RMS密度变化1.9045e−2/5.2560e−4、轨道梯度1.0241e−4，未达到各自打印阈值。最小重叠本征值2.194e−7，无基函数被删除。[ORCA官方手册](https://www.faccts.de/docs/orca/6.1/manual/contents/essentialelements/scf.html#convergence-tolerances)说明该判据使用总能量与单电子能量变化，小重叠本征值下密度残差可未过阈值。据此接收既定精度的能量结果并披露限制，不宣称所有残差收敛、TightSCF或全局波函数稳定性认证，不加自设收紧门槛。从SCF轨迹到最终能量的偏移由原生NL、最终交换积分与SMD CDS项解释，详见sulf_receipt.json。

另新核收R5环化SP、两个R6简单产物Opt/Freq和SP；两个新极小值零虚频，完整键图与作者种子一致。保留作者物理方法，ORCA6.1.1替代作者6.0.1的既有差异继续披露。

| Case | Stage | E / Eh | Native RRHO G / Eh | Wall seconds |
|---|---|---:|---:|---:|
| R5_SMe6_cyc4P2_0_1 | method7 | -1318.692504910337 | — | 706.13 |
| R6_SMe1_P2_0_1 | optfreq | -1357.837423692959 | -1357.55797658 | 971.29 |
| R6_SMe1_P2_0_1 | method7 | -1357.992383571753 | — | 1394.13 |
| R6_SMe6_P2_0_1 | optfreq | -1357.839486817685 | -1357.5586755 | 969.19 |
| R6_SMe6_P2_0_1 | method7 | -1357.990903383855 | — | 624.97 |
| Sulf_0_1 | method7 | -1699.959077405263 | — | 6530.54 |

复用method7 E+B3LYP热校正、298.15K及每分子RTln24.46标准态修正。新增部分终点比较：R5环化cyc4P2−R5简单SMe6P2为−2.409174 kcal/mol；R6 SMe6P2−SMe1P2为+1.784883 kcal/mol；两个R6简单产物相对R6+MeSH分别−3.969174和−2.184290 kcal/mol。均经组成/电荷平衡检查；没有把它们当势垒、完整位点排序或未配准的作者数值。此前第二次加成−2.141554 kcal/mol（作者约−2）继续复用。

健康批次继续R6剩余简单/环化终点和Sulf三种中性产物；当前批次不覆盖全部必要负离子位点排序、可达性与结论稳健性证据，不能据11个有效终点判整题通过。 健康批次当前在R6_SMe4_P1SS_0_1频率计算。新增客观来源阻碍0；本轮无必要重投、无CreateJob。

- `R5_SMe6_cyc4P2_0_1/method7`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R5_SMe6_cyc4P2_0_1/method7.log`; SHA256 `5415c615358ab0e5423e384af761eb00705506f5020cbecf499e787d40b29ef6`.
- `R6_SMe1_P2_0_1/optfreq`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe1_P2_0_1/optfreq.log`; SHA256 `f5de56e79ecdb6458aec20b695ea784b73eb3b8dd3886d07b0ea652a7eb7d8d3`.
- `R6_SMe1_P2_0_1/method7`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe1_P2_0_1/method7.log`; SHA256 `f4a66b182e8f9aa1d6f310504f915638f2a612b406cc7e5bac146466a128cdf6`.
- `R6_SMe6_P2_0_1/optfreq`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_P2_0_1/optfreq.log`; SHA256 `8a83a7a5075600611ec8ca1f4ea0029753d2d3c6e932047c46702e44f6e80dac`.
- `R6_SMe6_P2_0_1/method7`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_P2_0_1/method7.log`; SHA256 `5e841810afe45d3e41f1dca6142e661a753f4c34edff570a724ef46acf89f6de`.
- `Sulf_0_1/method7`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T2343Z/targeted_repair/Sulf_0_1/method7.log`; SHA256 `8c5485a5cd1791d2a0b4f2f27f7caba611e63c506f2c3d04cdaf52fdaafb2d45`.

Evidence: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/service_recovery_20261023T0149Z/sulf_receipt.json`, `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/service_recovery_20261023T0149Z/author_comparison.json`, `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/service_recovery_20261023T0149Z/coverage.json`. Handoff: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T0033Z/service_recovery_20261023T0149Z/new44_group_01/handoff.md`. Original question, evaluator, weights and tolerances unchanged.

## Follow-up 2026-10-23T0647Z — new evidence and bounded successors

Current whole-question status: **INCOMPLETE; no new acceptance candidate**.

新核R6第三简单产物、两种环化产物的Opt/Freq与method7，以及Sulf_SMe1产物Opt/Freq；各极小值零虚频、源完整键图匹配。主要R6环化终点ΔG1M=−17.230832kcal/mol，对FigureS8−17.5差+0.269168；另一环化为−17.048283，对−17.3差+0.251717。主要环化比简单SMe1P2低13.261658kcal/mol。2CPU本地预检实际完成MeS− Opt/Freq（83.68秒），成功段已复用；后继已完成其SP（14.40秒）及R5_SMe1负离子Opt/Freq（734.68秒，零虚频、源键图一致），继续作者TableS4缺失负离子/代表性环化节点。新返回Sulf_SMe1单点TRAH超时仅修该段，复用已完成Opt/Freq；Sulf反应物既有成功单点不重算。

保留中性产物批次继续Sulf_SMe4/Sulf_SMe6；Sulf_SMe1单点另行有界修复；作者TableS4负离子位点比较、R5/R6竞争环化TS与代表性中间体在新批次。尚需有效模式、平衡比较及当前必要稳健性解释；不要求全文/全部IRC/全部构象。

| Case | Stage | E / Eh | Native RRHO G / Eh | Seconds |
|---|---|---:|---:|---:|
| R6_SMe4_P1SS_0_1 | optfreq | -1357.838530001591 | -1357.55768799 | 953.78 |
| R6_SMe4_P1SS_0_1 | method7 | -1357.992968690457 | — | 794.06 |
| R6_SMe6_cyc4P2_0_1 | optfreq | -1357.857085700874 | -1357.57390395 | 989.55 |
| R6_SMe6_cyc4P2_0_1 | method7 | -1358.016961097521 | — | 595.43 |
| R6_SMe6_cyc2P2_0_1 | optfreq | -1357.854438346436 | -1357.57167951 | 1003.00 |
| R6_SMe6_cyc2P2_0_1 | method7 | -1358.016829092702 | — | 1040.17 |
| Sulf_SMe1_P2_0_1 | optfreq | -2138.425572487369 | -2138.05518987 | 2844.04 |
| SMe_-1_1 | method7 | -438.179202345941 | — | 14.40 |
| R5_SMe1_-1_1 | optfreq | -1318.02127383805 | -1317.78422916 | 734.68 |
| SMe_-1_1 | optfreq | -438.158398980718 | -438.14586267 | 83.68 |

Native result provenance:

- `R6_SMe4_P1SS_0_1/optfreq`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe4_P1SS_0_1/optfreq.log`; SHA256 `92dd7002a8d129ad1b79fb35d823b245a10fff394ecb6f67dc692cccb9e136f7`.
- `R6_SMe4_P1SS_0_1/method7`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe4_P1SS_0_1/method7.log`; SHA256 `6226cedff026775dd4c336e5c146f81a05dc5dd65c9da8b66375789d60eb2ade`.
- `R6_SMe6_cyc4P2_0_1/optfreq`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_cyc4P2_0_1/optfreq.log`; SHA256 `1a4c6bab037660dd5fe5fde3902c9159c3c123c1d13a8327fd23ab2b79d456e0`.
- `R6_SMe6_cyc4P2_0_1/method7`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_cyc4P2_0_1/method7.log`; SHA256 `207bd7a7b955ca64eeea3520319425b20be94b265a74011842b41daaefebae45`.
- `R6_SMe6_cyc2P2_0_1/optfreq`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_cyc2P2_0_1/optfreq.log`; SHA256 `67843d8aa2744b38c49526db0231e44f0c493f584ef73b92fe776d6583613274`.
- `R6_SMe6_cyc2P2_0_1/method7`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/R6_SMe6_cyc2P2_0_1/method7.log`; SHA256 `d22b226b27f9ab0837f12a699050227e4b2ff473d10b903924ea87e765fb937e`.
- `Sulf_SMe1_P2_0_1/optfreq`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_SMe1_P2_0_1/optfreq.log`; SHA256 `17e6ed39139a041624cfffbfe3b310617b4dd6d975ef38c3c94ce4af8c5f4628`.
- `SMe_-1_1/method7`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/SMe_-1_1/method7.log`; SHA256 `eca329fd8307b15e7c66e739703fed3803254a569203dc53acf8bf5e344567c5`.
- `R5_SMe1_-1_1/optfreq`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe1_-1_1/optfreq.log`; SHA256 `696d5ea4fc6969f9d0474bc002700d6743883e59d44f449af6cfddad8a96232a`.
- `SMe_-1_1/optfreq`: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/local_preflight/native.log`; SHA256 `33eccd58fcc646f8da523fe1d827d4ae46de7ee89abf8e6a1c9127b6515993e7`.
- New job `hpc-job-ac50b197-f527-49ca-b614-27a804450ae7`: frozen spec `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/job_spec.json`, native first check `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/job_audits/hpc-job-ac50b197-f527-49ca-b614-27a804450ae7/native_audit.json`.
- New job `hpc-job-790f0fed-23c3-4108-aa1a-6242ad759cc2`: frozen spec `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/sulf_product_repair_bundle/calculation/job_spec.json`, native first check `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/job_audits/hpc-job-790f0fed-23c3-4108-aa1a-6242ad759cc2/native_audit.json`.

Author comparison: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/author_comparison.json`. Remaining coverage: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/coverage.json`. Failure lineage: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T0647Z/new44_group_01/repair_lineage.json`. New objective source blockers:0. Physical model, task statement, evaluator, tolerances and weights unchanged. Existing source/software-version/temperature assumptions remain disclosed; no completed component is a whole-question pass.

## Verification target correction 2026-10-23 — required results and author geometries

Status: **INCOMPLETE_REQUIRED_EVIDENCE**. No new acceptance candidate. Standard SHA256: `85c52de6f6299b911939cd0636229a1249e4fdf387748f1fa0c6ad75617fbf02`.

Current task requirements, author sources and methods, actual inputs/logs, signed differences, missing evidence and minimal next steps: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/verification_target_correction_20261023/verification_matrix.json`; readable table: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/verification_target_correction_20261023/verification_matrix.md`.

- Received `Sulf_SMe4_P2_0_1/optfreq`: rc=0, native normal termination, 3320.637s; log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_SMe4_P2_0_1/optfreq.log`; SHA256 `e9f8f96ff9091b8478fab3c523ee43680602de4a54acd7d0d8a1e9a952fbce56`.
- Received `R5_SMe1_-1_1/method7`: rc=0, native normal termination, 962.809s; log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe1_-1_1/method7.log`; SHA256 `2cb856394cc6ed99c2a2c202d0a2cfbd7c8270eac2052b3b6d9ed1ecfd3ce35b`.
- Received `R5_SMe4_-1_1/optfreq`: rc=0, native normal termination, 799.976s; log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe4_-1_1/optfreq.log`; SHA256 `4bade8d439ac2bee65f88df20e9a3f3313aafa094e8b8e6cd330396960bd40d0`.
- Received `R5_SMe4_-1_1/method7`: rc=0, native normal termination, 777.211s; log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe4_-1_1/method7.log`; SHA256 `91dde7091ef7b7bfa9aece6745c36ede08c46ebdb837e283cdf4b2f165bf1757`.
- Received `R5_SMe6_-1_1/optfreq`: rc=0, native normal termination, 743.999s; log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe6_-1_1/optfreq.log`; SHA256 `b6f818acdcf960d2c5f390d7b85b20103bd524e5fbace2b21a99b14af06e3d92`.
- Received `R5_SMe6_-1_1/method7`: rc=0, native normal termination, 594.828s; log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R5_SMe6_-1_1/method7.log`; SHA256 `bb2ed8f10ac1eb2fe864297ace41448f88e1cee422348352b9197514cf8d0027`.
- Received `R6_SMe1_-1_1/optfreq`: rc=0, native normal termination, 917.686s; log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe1_-1_1/optfreq.log`; SHA256 `07882f0b5b3adab6a0db75d8d363d3bcbf8aa968013deed5878ad346c935d140`.
- Received `R6_SMe1_-1_1/method7`: rc=0, native normal termination, 1054.738s; log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe1_-1_1/method7.log`; SHA256 `eebec9c994d36a811d863f4b02d7bd1adf8b0976be74999ccd3ec469d56ac1c4`.
- Received `R6_SMe4_-1_1/optfreq`: rc=0, native normal termination, 954.570s; log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe4_-1_1/optfreq.log`; SHA256 `998786996a2739592997bd553e9e69ea5c5720b562bbd7219f962feeb31bb35f`.
- Received `Sulf_SMe1_P2_0_1/method7`: rc=0, native normal termination, 2135.278s; log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/sulf_product_repair_bundle/calculation/Sulf_SMe1_P2_0_1/method7.log`; SHA256 `b31c33d4d51e1b22ce8d1fda38359fafcdb724a83d638a12ce0de81330d652ae`.

R5 anion formation Gibbs energies (method7,298.15K,1M): +2.496236 / -1.094336 / -5.335009 kcal/mol versus author +2.4 / -1.2 / -5.4; signed differences +0.096236 / +0.105664 / +0.064991. Independent method1/method7 neutral-site ordering differs, supporting the limited robustness of the R5 assignment. Sulf_SMe1 product energy converged in30 SCF cycles and35.59min; balanced reaction ΔG=-5.245893 versus FigureS8 -5.4 (difference+0.154107). ORCA energy criterion is satisfied but MAX/RMS density changes0.071768/0.0016859 and orbital gradient0.00011399 exceed their printed targets; no claim of all-residual convergence. Receipt and remaining required products/anions/accessibility: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/verification_target_correction_20261023/sulf_product_receipt.json`.

Remaining required evidence:

- FB_R5: 核当前负离子/TS批次；用现有method1/7评估实际方法依赖。
- FB_R6: 保留当前后继，核TS模式与代表性环化中间体。
- FB_Sulf: 当前健康批次完成后核同组成位点/构象排序，不新增PI3二次加成网。
- FB_integrated: 继续当前节点后组合结论；作者文字及几何描述不替代缺的能量/可达性证据。

Physical models, task statement, evaluator, tolerances and weights unchanged. No new objective source blocker. Prior healthy jobs retained. Component completion is not whole-question completion.

## Native job follow-up 2026-10-23 10:44 UTC

Status: **INCOMPLETE_REQUIRED_EVIDENCE**. No new acceptance candidate. Standard SHA256: `2743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379`.

Updated claim-by-claim verification matrix and signed comparisons: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T1044Z/verification_matrix.json`; readable table `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T1044Z/verification_matrix.md`. Native receipt: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1044Z/new44_group_01/native_return_review.json`.

- `R6_SMe4_-1_1/method7` completed normally, rc0, 858.68s; native log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe4_-1_1/method7.log` (SHA256 `075f4b32a0a9e7a6409b295b62bf7e1bd17a7a090a51df4a8bba365647ab3fd7`). This certifies only this stage.
- `R6_SMe6_-1_1/optfreq` completed normally, rc0, 947.63s; native log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_-1_1/optfreq.log` (SHA256 `47f23ef0d6018cdfd7dd18bf2dd82cc68869427294bcbbf0aa12afe686a6e4da`). This certifies only this stage.
- `R6_SMe6_-1_1/method7` completed normally, rc0, 649.09s; native log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/R6_SMe6_-1_1/method7.log` (SHA256 `ee6f8926233173b956ec9e49798fe7b1176f1f3b7c42168f629ceee75591a7d9`). This certifies only this stage.
- `Sulf_SMe1_2_c80_-1_1/optfreq` completed normally, rc0, 2660.08s; native log `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe1_2_c80_-1_1/optfreq.log` (SHA256 `a185b03700814815420fd44771c898755c05dd685f0bd3a7681483a379f576c2`). This certifies only this stage.

R6 anion formation free energies versus R6+MeS- are+2.870720/+1.043098/-1.579728kcal/mol, versus FigureS8+2.8/+0.9/-1.7; differences+0.070720/+0.143098/+0.120272. Site ordering agrees. Sulf c80 anion Opt/Freq completed with zero imaginary frequencies and matching source bond graph; its SP is pending. Prior Sulf product SP and its residual disclosure are reused, not newly counted. Accessibility and the full Sulf comparison remain incomplete.

Remaining required evidence:

- FB_R5: 核当前负离子/TS批次；用现有method1/7评估实际方法依赖。
- FB_R6: 保留当前后继，核TS模式与代表性环化中间体。
- FB_Sulf: 当前健康批次完成后核同组成位点/构象排序，不新增PI3二次加成网。
- FB_integrated: 继续当前节点后组合结论；作者文字及几何描述不替代缺的能量/可达性证据。

Healthy jobs and successful stages retained. No new objective source blocker; no task, evaluator, weights, tolerances or expert materials modified.

## Native job follow-up 2026-10-23 12:21 UTC

Status: **INCOMPLETE_REQUIRED_EVIDENCE**. No acceptance candidate. Standard SHA256: `2743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379`.

New Sulf_SMe6 product Opt/Freq and method7SP completed normally, source bond graph preserved and zeroimaginary. Atom/charge-balanced formationG(method7+ownG1-E1,298.15K/1M)=-9.504704 versus author-9.7kcal/mol, difference+0.195296. FirstSulf c80 anionSP complete, formationG=-0.644493 versus-0.8, difference+0.155507. PriorSulf reactant/SMe1 product successfulSPs and residual disclosures reused. NewSMe4 productSP reached3h bound with divergentTRAH, no convergence; targetedNoTRAH/SOSCF/shift recovery uses its own successfulOpt/Freq geometry/orbitals at unchanged physical model. Startup root-path error repaired once; effective successor active. Remaining anions/TS accessibility and combined conclusions incomplete.

Claim matrix: [paper_fb75113b35e12c7c](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1221Z/new44_group_01/papers/paper_fb75113b35e12c7c/verification_matrix.md); numerical/native comparison: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1221Z/new44_group_01/papers/paper_fb75113b35e12c7c/author_comparison.json`; native return receipt: `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1221Z/new44_group_01/native_return_review.json`.

New native stages:

- `Sulf_SMe6_P2_0_1/optfreq`: rc0, normal termination, 3273.19s; `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_SMe6_P2_0_1/optfreq.log` SHA256 `5acd3a8ff779ee36f0e40626903f80a773f854ff4778086f87c9653748750942`. Stage scope only.
- `Sulf_SMe6_P2_0_1/method7`: rc0, normal termination, 839.60s; `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/short_job_followup_20261022T1743Z/SCF_recovery/Sulf_SMe6_P2_0_1/method7.log` SHA256 `91382070a852622fc095ba1338d4e19eb874b644281badb4ddb70b2be258f189`. Stage scope only.
- `Sulf_SMe1_2_c80_-1_1/method7`: rc0, normal termination, 5595.76s; `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe1_2_c80_-1_1/method7.log` SHA256 `2d10259560b563b2899b9b509877b9515177aad007cf8b73663ef19326d18dd0`. Stage scope only.

Remaining necessary results:

- FB_R5: 核当前负离子/TS批次；用现有method1/7评估实际方法依赖。
- FB_R6: 保留当前后继，核TS模式与代表性环化中间体。
- FB_Sulf: 核本轮SMe4单点修复与既有阴离子/TS批次，完成位点/构象排序；不新增PI3二次加成网。
- FB_integrated: 继续当前节点后组合结论；作者文字及几何描述不替代缺的能量/可达性证据。

Healthy batches retained; no new source blocker. Physical methods, task/scoring/weights/tolerances and expert materials unchanged.

## Native job follow-up 2026-10-23 13:27 UTC

Status: **INCOMPLETE_REQUIRED_EVIDENCE**. No whole-question candidate. StandardSHA256 `2743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379`.

NewSulf_SMe4_c13_-1_1 Opt/Freq completed normally,zeroimaginary and sourceconnectivity retained (3521.84s). Ownmethod7SP remainsactive, so no newmethod7formationG is claimed. e726SulfSMe4productSP remainsactive; oldSulf/reactant/SMe1/SMe6/c80successes reused. Required remainingSulfsite/conformercomparisons andR5/R6TSaccessibility stillincomplete; nativecompletion of oneminimum is notwholequestionvalidation.

[Current claim matrix](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1327Z/new44_group_01/papers/paper_fb75113b35e12c7c/verification_matrix.md); signed numeric/native comparisons `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1327Z/new44_group_01/papers/paper_fb75113b35e12c7c/author_comparison.json`; native return review `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261023T1327Z/new44_group_01/native_return_review.json`.

New normal native outputs (stationarity gaps explicitly excluded from accepted thermochemistry):

- `Sulf_SMe4_c13_-1_1/optfreq` rc0,normal,3521.84s; `/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_fb75113b35e12c7c/job_followup_20261023T0647Z/necessary_anions_accessibility/Sulf_SMe4_c13_-1_1/optfreq.log` SHA256 `7720aa1551034b23a55082ba58feca09dec67f3f24eb96c4aa56ff7f83c87f53`.

Remaining required evidence:

- FB_R5: 核当前负离子/TS批次；用现有method1/7评估实际方法依赖。
- FB_R6: 保留当前后继，核TS模式与代表性环化中间体。
- FB_Sulf: 保留健康e726产品单点及ac50阴离子/TS批次，匹配SP返回后组装位点/构象排序；不重复SMe4-c13频率。
- FB_integrated: 继续当前节点后组合结论；作者文字及几何描述不替代缺的能量/可达性证据。

No new objective sourceblocker; task/scoring/weights/tolerances and expertmaterials unchanged.

## Native job follow-up 2026-10-23 15:50 UTC

New SMe4-c13 anion Opt/Freq remains valid with zero imaginary and preserved graph. The previous SMe4 product method7 attempt `hpc-job-e7267885-8531-4c7b-a6fb-6195ec4f79f0` failed at 3 h after 249 DIIS iterations; SOSCFStart 0.001 never activated (DIIS error crossed 0.01 but not 0.001 before density excursions). One bounded changed successor `hpc-job-38e23c70-ac21-48b9-9065-e1c88ca3a7f8` changes only SOSCFStart to the ORCA-supported 0.01, reuses the valid Opt/Freq GBW/XYZ and was first checked RUNNING. Method7 result is not yet claimed; Sulf integrated accessibility and site comparison remain incomplete.

Source SHA256 policy `2743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379`; this is a current native evidence note. It does not change task text, evaluator, tolerances, expert materials, or acceptance status.

## Verification follow-up 2026-10-24 01:40 UTC — native evidence amendment

SMe4 method7 successor38e23c70 normalrc0 andSCF146cycles, E=-2138.680057898237Eh, wall10708.574s (not timeout). ORCA energy-check convergence has deltaE7.1907e-7 but maxdensity0.22963/RMSdensity0.0072282/DIIS0.0059316; these residuals are disclosed, not all-threshold convergence. Four balanced Sulf anionsG7=-0.644493/-13.446486/-6.253568/-10.389296vs-0.8/-13.6/-6.3/-10.5; three neutral products=-5.245893/-10.657089/-9.504704vs-5.4/-10.9/-9.7kcal/mol, all with ownG1-E1 and1M correction. R5/R6 ring4 TSs actually optimized normally with final singleimag-575.19/-537.69 and force checks passing. Historical runner counted initial+final Hessians and wrongly skipped method7; corrected receipt preserves both raw sections. Source ring-forming bondsC4-O8/C15-O24 match final modes. Only missing twoSPs submitted0273b5db, no repeated optimization. Method1 local barriers37.264374/28.278727 are not mislabeled as matched method7. New R6cyc2S andcyc2SP1 thermals received, but endpoints do not prove barrierless access. Selected two-method product rankings analyzed; overall accessibility/robustness still incomplete.

Current evidence: [paper_fb75113b35e12c7c author comparison](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0140Z/new44_group_01/papers/paper_fb75113b35e12c7c/author_comparison.json); [itemized verification matrix](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0140Z/new44_group_01/papers/paper_fb75113b35e12c7c/verification_matrix.json); [native receipts](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0140Z/new44_group_01/papers/paper_fb75113b35e12c7c/native_receipts.json); [reaction mode and source bond mapping](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0140Z/new44_group_01/transition_mode_review.json). Current standard SHA2562743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379. No new whole-task candidate; no task/scoring/tolerance change. Prior raw records retained; latest native receipts supersede stale parser/completion interpretations.

## Verification follow-up 2026-10-24 03:38 UTC — native evidence amendment

Returned0273 supplies both missing alphaTS method7SPs with normalrc0/nativeSCF convergence. R5/R6 E=-1318.129359687949/-1357.442641467313Eh; wall617.8456/1100.7176s. Own optimizedXYZ/GBW hashes matched, ownthermal corrections and final singleimag-575.19/-537.69 reused; forces pass and source C4-O8/C15-O24 forming modes verified. Matched G7=SP7+(ownG1-ownE1),298.15K/1M gives local TS-minus-anion35.401941/27.297280vs35.6/27.6 (delta-0.198059/-0.302720), common separated-reactant ordinates30.066932/25.717551vs30.2/25.9. ORCA native energy/orbital convergence is disclosed:27/54cycles and deltaE1.2944e-7/2.4914e-7Eh, while MAXdensity0.0064599/0.023977,RMSdensity0.00017840/0.00067608,DIIS0.00097485/0.00085977 exceed their printed thresholds; these are not claimed all-density-threshold results. Necessary gamma-accessibility remains. One bounded successoraca6aa01 nowRUNNING after both90s local native preflights: R5 published neutralcyc2SP1 minus terminalH38 is an explicitly reconstructed anion release seed, not a claimed authoroptimizedanion; R6 reuses successfulcyc2S geometry/GBW for12point C5-O24 reverse relaxed scan1.60791479-to2.60Angstrom. FirstcheckR5cycle5 withoutnativeerrors. Reopening may be expected outcome; constrained potential-energy scan is not exact Gibbsbarrier/global barrierlessproof. Whole-question incomplete.

Current evidence: [author comparison](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_01/papers/paper_fb75113b35e12c7c/author_comparison.json); [itemized verification matrix](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_01/papers/paper_fb75113b35e12c7c/verification_matrix.json); [native receipts](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_01/papers/paper_fb75113b35e12c7c/native_receipts.json); [source mapping and reaction modes](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0338Z/new44_group_01/transition_mode_review.json). Standard SHA2562743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379. No whole-question acceptance candidate; no task/scoring/tolerance change. Prior raw records retained; this amendment supersedes stale completion interpretations only.

## Verification follow-up 2026-10-24 07:52 UTC — native evidence amendment

Newgammajobaca6aa01 nativeR5OptFreq andR6twelvepointscan bothnormalrc0. R5source-mappeddeprotonatedcyclicseedspontaneouslyopensC2-O8from1.469834to2.762128Angstrom;zeronegativefreqandmax/RMSgradient0.000275598/0.0000537965pass. Finalopengraphmatchesexistinganion,heavyRMSD0.024198Angstrom,deltaE+0.026366/deltaG-0.014132kcal/mol. Thisconfirmsreportedlocalreversion,notglobalnonexistence. R6C5-O24reverse12pointscanhasallconstrainedpointsconverged andonlysourceC-Obondchange; sampledopeningEdeclinesmonotonically. Relative tosameexistingopenanion:gammapathmaximum9.564782kcal/molvs matchedmethod1alphaTS electronicbarrier29.132496. Openingendpoint isnearbyconformer,heavyRMSD0.700980Angstrom,deltaE-0.290296,samegraph/tetrahedralorientations;gamma pathspan9.855078relative toitself. FiniteconstrainedpotentialpathisnotexactGammatransitionstate/freeenergybarrier orglobalbarrierlessproof. ExistingG7cyclicintermediate+3.563182vs+3.6 andlowcyclicproducts,allsite/mono-/secondaddition/twomethodrankings,alphaTSownFreq/SP7comparisonsreused. R5cyclic4P2minussimpledelta=-1.469429;secondaddition-2.141554vsroundedsource-2.0. R5smallgaps/methodrankchangesandexperimentaldiscrepancyarepreservedauthorqualifiedconclusions;R6initialanionprose/figureambiguityretained. Currentrequiredsource-baselineresults/conclusionscomplete: proposeRESULTS_COMPLETE_NUMERIC_REVIEW forparentindependentreview,notalreadyaccepted. ORCAversion/SCFresidualandconstrainedscanlimitsstayexplicit.No furthernewQCnecessaryforcurrentbaseline.

Current evidence: [author comparison](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0752Z/new44_group_01/papers/paper_fb75113b35e12c7c/author_comparison.json); [itemized verification matrix](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0752Z/new44_group_01/papers/paper_fb75113b35e12c7c/verification_matrix.json); [native receipts](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0752Z/new44_group_01/papers/paper_fb75113b35e12c7c/native_receipts.json); [source mapping and reaction modes](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/job_followup_20261024T0752Z/new44_group_01/transition_mode_review.json). Standard SHA2562743e7ca8939e7f5e6b44cbf6d6a2316c3bd1e7b920cef65bc5ac38b93ed8379. Sulf has a RESULTS_COMPLETE_NUMERIC_REVIEW candidate, requiring parent independent review; Cu/Ir remain incomplete. No task/scoring/tolerance change. Prior raw records retained; this amendment supersedes stale completion interpretations only.

## Evidence closeout 2026-10-24 08:42 UTC — parent registration and species correction

父级已于2026-10-24T09:03:07.440710+00:00将当前两模式共同科学问题C1–C4登记为 **RESULTS_COMPLETE_NUMERIC_REVIEW**：必要结果完整、限定结论支持，不等于专家严格数值批准、自动满分或发布。无需新增QC，本轮只做证据收尾。

**明确更正历史文字的物种归属：** 原gamma收据及此前摘要将small-step替代收敛归给环阴离子，是记录错误。原生日志显示中性母体 **R6_0_1** 的MAXgradient0.0005810986超过0.0003000000，RMSgradient0.0000965836及RMSstep0.0004259295/MAXstep0.0013192807通过，原生small-step宣告收敛且零虚频。**R6_SMe6_cyc2S_-1_1** 环阴离子四项全部通过：RMSgradient0.0000426384、MAXgradient0.0002265130、RMSstep0.0003957531、MAXstep0.0021108073；零虚频。此更正覆盖旧摘要的含糊/错误归属；历史原文和失败日志保留，不更改原生日志。

专家审查边界：

- 原生SCF采用 Total+1el-Energy（父级审计确认ConvCheckMode2），正常终止和原生收敛不等于所有density/DIIS/orbital阈值同时通过；数值质量由专家审查，不自动追加全Tight门。
- Sulf_SMe4_P2_0_1 method7共146轮；deltaE7.1907e-7Eh/阈值1e-6，MAX/RMSdensity0.22963/0.0072282，DIIS0.0059316，orbitalgradient0.00042272、rotation0.00083656；密度和轨道残差超过打印阈值，完整原日志保留。
- 收敛归属更正：中性R6_0_1采用small-step替代收敛，MAXgradient0.0005810986>0.0003000000，其余三项通过、零虚频；环阴离子R6_SMe6_cyc2S_-1_1四项均通过、零虚频。
- ORCA实际6.1.1、作者6.0.1；原泛函/基组/色散/溶剂/电荷/多重度保留，已披露SCF数值辅助不同，选定作者构象不冒充全局搜索。
- R5简单产物能差小且method1/method7最低项改序；第二次MeSH加成略有利与EtSH实验不完全吻合，是保留的作者限定结论，不能写成可靠的独占选择性或计算/实验等同。
- R6初始阴离子排序有来源歧义：正文delta最低与图/SI及执行能量beta-prime最低不一致；不制造唯一初始排序。
- R6 gamma为12点受约束method1电子能扫描；开环采样能下降、闭环上坡，有限间距不能排除窄峰。仅与同方法同参照alpha电子势垒比较，不能称精确gamma自由能势垒或全局无势垒。
- R5 gamma种子从作者中性结构删H38重构，并非作者优化阴离子；释放结果仅支持该源附近种子开环，不证明所有gamma途径不存在。
- 1atm→1M精确理想气体常数与RTln24.46每物种差0.000130877169692kcal/mol；双分子缔合精确值低该量，同分子数比较不变。两套算术并列保留，不重算QC。

父级独立复核32组Opt/Freq+method7SP共64个有效日志，加R5释放/R6扫描2段，共66段；四个失败单点有成功替代，旧失败不删除、不参与有效值。alphaG7局部35.401941/27.297280对35.6/27.6；gamma采样电子路径9.564782对匹配alpha电子势垒29.132496，不混G势垒。逐态G7与独立审计完全相等；1M常数仅导致双分子反应0.000130877169692kcal/mol差，无需重算QC。

[父级登记](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/parent_acceptance_review.json)；[独立审计](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/sulf_review/audit.md)；[当前逐项矩阵](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/new44_group_01/papers/paper_fb75113b35e12c7c/verification_matrix.json)；[更正后的gamma收据](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/new44_group_01/papers/paper_fb75113b35e12c7c/gamma_accessibility_receipt.json)；[逐行原生更正证据](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/new44_group_01/evidence_correction.json)；[1M常数解释](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/verification_coverage_20261024T0842Z/new44_group_01/papers/paper_fb75113b35e12c7c/standard_state_reconciliation.json)。题面、评分、容差不改，专家包/全局总表由父级维护。
