# 2026-09-29 修后维护审查：paper_1e3a1d290a02e5f0 / paper_reproduction

**状态：本轮已授权的任务修复和针对性复查完成，保留 verified_tasks；没有执行 final/hold 迁移。科学边界和待定项见下文，包检查通过不表示全部科学要求已获负责人验收。**

负责人最新指令：继续按流程处理这些论文，先留在 verified_tasks，汇报后等待确认再移动。该指令授权本轮常规修复，不授权改目标/放宽容差、新计算或迁移。

[实际计算与原始证据](../verified_computation_reference.md)；[本批集中报告第30节](../../../../MAINTENANCE_REPORT.md)；[提交/评分回归](../../../../maintenance_tools/repair_checks_20260929.json)；[文件与导出检查](../../../../maintenance_tools/final_checks_20260929.json)。

## 本轮实施的修复

- 公开三条主结果的 JY1/JY2/JY3 顺序，并将每个位置绑定完整行约束，拒绝只有身份或空 λ 的完成结果。
- 每模式从 3 条含混 numeric 规则补成 9 条身份明确的比较，保留原 JY1 rule ID；JY2/3 目标来自既有 KP，未改既有目标/容差。
- 将 LUMO 及过程关键点接回原有唯一科学结论；明确同一个四点 λ 物理量，公开 B3P86/6-311G(d,p) 比较背景，保留合理方法自由度。

共同处理：AR 四节、PR 五节；普通 limitations/uncertainty 可选且不计分，保留科学有效性和真实失败诊断；显式选用既有 scientific_results 策略。额外失败尝试不抹掉已完成主结果。

## 评分结构与当前逐项映射

关键点 5→5；结论记录 1→1。未另加 conclusion 权重或新 rubric。默认唯一科学结论仍可结合支持证据评价实际完成部分，不等于只允许 0/100。

- 修前 KP：pr_process_identity, pr_process_lambda, pr_homo, pr_lumo, pr_lambda
- 修后 KP：pr_process_identity, pr_process_lambda, pr_homo, pr_lumo, pr_lambda
- 修前结论：pr_final_trend
- 修后结论：pr_final_trend

| KP / 类型 | 论文/SI 定位（按现有 evidence_map） | 公开提交字段 / 评分职责 | 真实计算支持与差距 |
| --- | --- | --- | --- |
| pr_process_identity / process | Supplementary Information S1.1, Computational Details: B3P86/6-311G(d,p), no imaginary frequencies, and λh calculation boundary. | pr_r_identity: $.results[*].molecule_id, $.results[*].identity, $.results[*].validation | JY1/2/3中性最低点各300正频，0/1；阳离子+1/2也为最低点。 |
| pr_process_lambda / process | Supplementary Information S1.1, Computational Details: B3P86/6-311G(d,p), no imaginary frequencies, and λh calculation boundary. | pr_r_lambda_process: $.results[*].molecule_id, $.results[*].method.lambda_definition, $.results[*].method.energy_states | 四态能量式逐项复算，六组父子几何核对一致。 |
| pr_homo / result | Main paper Section 2.1: optimized structures and reported HOMO/LUMO values for JY1–JY3. | pr_r_homo1: $.results[0].homo_eV; pr_r_homo2: $.results[1].homo_eV; pr_r_homo3: $.results[2].homo_eV | 三HOMO由最后occupied轨道提取，均在原±0.15内。 |
| pr_lumo / result | Main paper Section 2.1: optimized structures and reported HOMO/LUMO values for JY1–JY3. | pr_r_lumo1: $.results[0].lumo_eV; pr_r_lumo2: $.results[1].lumo_eV; pr_r_lumo3: $.results[2].lumo_eV | 三LUMO由首virtual轨道提取，均在原±0.15内；修后已关联原有科学结论。 |
| pr_lambda / result | Main paper Section 2.1: reported λh values 0.191, 0.186 and 0.189 eV. | pr_r_lambda1: $.results[0].lambda_h_eV; pr_r_lambda2: $.results[1].lambda_h_eV; pr_r_lambda3: $.results[2].lambda_h_eV | 三λ=.213411/.198457/.211489 eV，均满足原±.03；JY2最小。 |

| 结论 ID | 支持关键点 | 实际规则读取 |
| --- | --- | --- |
| pr_final_trend | pr_process_identity, pr_process_lambda, pr_homo, pr_lumo, pr_lambda | pr_r_final: $.conclusion |

## 本包复查结果与科学判断

真实历史 report：通过。本包 14 个格式用例均符合预期，包含正常完成、缺少关键结果、诚实早期失败、成功附加失败尝试及身份/状态错误。实际 runtime policy 与所有评分 ID 关联已检查；没有悬空/standalone 规则。

通用数值 checker 只筛查已绑定标量，不验证化学身份、真实计算及协议可比性。ESIPT log-rate 另用本批离线公式核查；H₂PQ AR 动态身份、CBSCA 选中候选交叉关联及 Au 原歧义规则仍需语义/科学审查，不宣称 schema 已自动解决。

**审查建议与未闭合项：**九个验证值均满足原容差；不同方法与 B3P86 源靶是否可比仍须科学判断。现有源值/容差未放宽，也未将分子量推广为器件性能。 当前已实施的常规修复可以交负责人审阅；未决定的科学接受标准维持原状，不以包校验通过替代确认。

## 基线与未变内容

修前 Git `b6c0f50825638e9c6149595581734bb674fbd66c`；可恢复档 `.git/maintenance_backups/20260929_eight_papers_repair/before_repair.tar.gz`，格式阶段 `after_format.tar.gz`，修后档 `after_quality.tar.gz`。本轮仅改本批暂存包、集中报告及 maintenance_tools；canonical 218 个文件按修前哈希核对，原始计算/论文及 final/hold 未操作。Rh 作废片段仅改公开/私有位置，其余科学输入字节不变。没有提交 Git 或运行新的量化计算。

## 修前初审历史（以下不代表当前状态）

以下保留初审时的原记录；其中“待批准、未修复、旧策略”等已被本页修后部分覆盖。科学原始数值和未闭合问题仍可追溯。

状态：已有真实作者路线证据，已接收到 verified_tasks；本轮未修改 task/schema/evaluator，待具体修法确认，不批准 final/hold 迁移。

[完整计算参考与当前必评映射](../verified_computation_reference.md)；[本批集中报告第29节](../../../../MAINTENANCE_REPORT.md)。

### 初审历史：输入、模式和来源审查

molecules.json 唯一命名 JY1/2/3，电荷/态/元素式一致，JY3 是 3′,4′,5′ 三氟；无轨道能与 λ 答案。自由选方法且允许多种 λ 定义与隐藏四点靶存在协议歧义。

Gaussian 16 B3P86/6-311G(d,p)，气相。每个分子一个中性单重态及一个 +1 双重态最低点，再做 cation@neutral 和 neutral@cation 两个定几何单点，共 12 份真实日志。六个最低点均 102 原子、300 正频率。JY1/2/3 的 F 取代位分别 4′、3′/5′、3′/4′/5′；现有源输入身份正确。正文物理第 2 页 Figure 2、方法与第 3 页 Table 2；本地无 JY SI。源 G09 与本地 G16 不同，作者构象不能称全局最低。

### 初审历史：当前计分和提交契约

修改前/本轮后均为 5 个关键点、1 个现行结论记录；ID未变。运行策略仍为 `dual_axis_100.v1`；拟在获准清理后显式切换既有 `dual_axis_100.scientific_results.v1`，不改全局默认。

| rule ID | 参考ID | 当前实际读字段 | 责任与诊断 |
| --- | --- | --- | --- |
| pr_r_identity | pr_process_identity | $.results[].molecule_id; $.results[].identity; $.results[].validation | semantic / expert semantic comparison |
| pr_r_lambda_process | pr_process_lambda | $.results[].molecule_id; $.results[].method.lambda_definition; $.results[].method.energy_states | semantic / expert semantic comparison |
| pr_r_homo1 | pr_homo | $.results[].molecule_id; $.results[].homo_eV | numeric / absolute difference with molecule identity retained |
| pr_r_lumo1 | pr_lumo | $.results[].molecule_id; $.results[].lumo_eV | numeric / absolute difference with molecule identity retained |
| pr_r_lambda1 | pr_lambda | $.results[].molecule_id; $.results[].lambda_h_eV | numeric / absolute difference with molecule identity retained |
| pr_r_final | pr_final_trend | $.conclusion | semantic / expert semantic comparison |

standalone 规则：pr_r_identity, pr_r_lambda_process, pr_r_lumo1。standalone 可能仍由过程/语义检查评估，不一律当作完全未评分。多字段/通配/自然语言条件的 numeric 在当前 checker 返回 requires_semantic_review，非自动 PASS；本轮人工重提数值对照与它分开。

| 实测样例 | runner valid | 意义 |
| --- | --- | --- |
| historical_report | True | 仅格式可提交，不代表科学成功 |

AR 缺事前假设不得编造；

### 初审历史：当前每项科学证据及差距

| KP / 类型 | 源文与计算支持 | 提交/计分职责 |
| --- | --- | --- |
| pr_process_identity / process | JY1/2/3中性最低点各300正频，0/1；阳离子+1/2也为最低点。 | pr_r_identity: $.results[].molecule_id, $.results[].identity, $.results[].validation |
| pr_process_lambda / process | 四态能量式逐项复算，六组父子几何核对一致。 | pr_r_lambda_process: $.results[].molecule_id, $.results[].method.lambda_definition, $.results[].method.energy_states |
| pr_homo / result | 三HOMO由最后occupied轨道提取，均在原±0.15内。 | pr_r_homo1: $.results[].molecule_id, $.results[].homo_eV |
| pr_lumo / result | 三LUMO由首virtual轨道提取，均在原±0.15内；现有成果关联有缺口。 | pr_r_lumo1: $.results[].molecule_id, $.results[].lumo_eV |
| pr_lambda / result | 三λ=.213411/.198457/.211489 eV，均满足原±.03；JY2最小。 | pr_r_lambda1: $.results[].molecule_id, $.results[].lambda_h_eV |

结果数值、每个结论 ID、具体原始日志和正文/SI位置见完整计算参考；reference 不替换上述当前计分规则。

### 初审历史：建议修改（尚未实施）

1. 两模式 scoring_rules 为 HOMO/LUMO/λ 显式绑定 JY1/2/3 的稳定 ID，补齐源中已存在的 JY2/3 数值绑定；当前只有 JY1 标量 target 搭配通配数组，自动 checker 交语义审查，不能声称九个自动数值已比较。数值/容差不改。
2. LUMO 结果关键点目前 standalone，不关联最终结论；提出完整分子性质结果的部分成果计分或在现有结论关联中补接 LUMO，具体权重/结论改动先确认。身份/能量循环过程仍保留。
3. 明确主比较采用原四点 λ 定义；task 可选 adiabatic/其他定义与 gold 不等价。若限制方法或比较职责，须批准后再改公共协议，不向 AR 注入作者答案。

共同修订范围建议：先按流程分离 PR Author-provided scientific guidance，再作已批输入/契约修复；递归清除普通免责声明的必填、独立得分和漏写即失败，同时保留身份/电子态/收敛/频率/路径/标准态及真实敏感性。完成/部分/失败/额外尝试分支按真实证据验证；不扩大科学范围或改变目标/容差。

### 初审历史：基线与处理范围

Git `238d70c4d9fd21b9e4669fcc149637ae704e4ca1`，本批修前可恢复 tar：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.git/maintenance_backups/20260929_eight_papers/before_reference_and_copy.tar.gz`。canonical 仅新增用户要求的 reference 并更新 manifest；本工作包完整复制（含隐藏文件），新增本维护记录，其他科学文件保持源字节。本批代码/测试记录位于 maintenance_tools；核查结果集中写入报告。没有对 docs/verification 或论文、原始日志写入，没有新QM/HPC或完整LLM评价。
