# 第一批自主科研与论文复现任务升级

实施日期：2026-09-27。**已完成 6 篇论文、12 个任务包的开发版升级。** 复制来源为现行 `tasks/final_verified_autonomous_research` 和 `tasks/final_verified_paper_reproduction`。每篇的科学问题、公开对象、提交契约与科学评分在两模式中保持一致；PR 额外提供作者假设、原理、机理解释和源计算路线。

**当前阶段是“任务实现完成，扩展范围待参考计算校准”。** 本轮没有新运行量子化学任务，没有生成扩展科学参考结果，也没有用旧 PASS 宣称新版验证通过。结构与格式测试证明包可被框架读取，不证明新科学问题已经通过验证。

## 1. 六篇具体升级

遵循各篇 2026-09-27 首版实施规格，本批为 **3 项 A→B、3 项弱 B→加强 B**。六篇首版均为 B 类有界解释／假设检验。有限对象上的竞争解释、干预和证据取舍符合用户接受的自主科研范围；没有把未校准的结构或完整机制搜索强行纳入 C 类。

| 论文 ID | 原类型 → 首版 | 新增的必需科学研究范围 | 可用软件范围 | 两模式指令 |
| --- | --- | --- | --- | --- |
| `paper_d83e607f125440cc` | 弱 B → 加强 B | H/Cl/Me/OMe/SMe 五系列；分开计算初始电子移除与苄位失 H；统一自旋分区；SMe/OMe 构象与共同介质对照；用保留成员检验描述符解释 | Gaussian/ORCA，Multiwfn；xTB/CREST 可辅助初猜 | [AR](autonomous_research/paper_d83e607f125440cc/agent_input/task.md) · [PR](paper_reproduction/paper_d83e607f125440cc/agent_input/task.md) |
| `paper_2f302589e5e9e420` | A → B | 两环氧片段的构象系综与 ⟨μ²⟩；OH 朝向与共同骨架干预；结合真实 OH 振动模式，区分氢键、取代电子效应与构象布居 | Gaussian/ORCA，CREST/xTB，GoodVibes/可审计 Python | [AR](autonomous_research/paper_2f302589e5e9e420/agent_input/task.md) · [PR](paper_reproduction/paper_2f302589e5e9e420/agent_input/task.md) |
| `paper_628af8d0bf0a1bfe` | 弱 B → 加强 B | 4a/4c 松弛与共同骨架控制；双环、双侧、多高度 NICS 张量投影；结合键长交替和方法敏感性，判断取代效应是否被几何或探针定义混淆 | Gaussian/ORCA 磁响应、约束优化；Python 张量/几何分析 | [AR](autonomous_research/paper_628af8d0bf0a1bfe/agent_input/task.md) · [PR](paper_reproduction/paper_628af8d0bf0a1bfe/agent_input/task.md) |
| `paper_9ec32e81e2826041` | A → B | 两构象族 × 有/无 D3；对角热化学与交叉几何电子能；TD/NTO 态追踪，分离直接色散、几何弛豫、吸收位移和亮度 | Gaussian/ORCA，Multiwfn，GoodVibes/Python | [AR](autonomous_research/paper_9ec32e81e2826041/agent_input/task.md) · [PR](paper_reproduction/paper_9ec32e81e2826041/agent_input/task.md) |
| `paper_2f0a4f80a37fbccd` | A → B | 同组成 eta1/eta2 硝酸根配位及几何候选；最低点和正常模参与度；统一缩放/残差规则比较实验 IR，检验是否能唯一判别模型 | Gaussian/ORCA，适当 Ir ECP/相对论处理；Python 谱与模式分析 | [AR](autonomous_research/paper_2f0a4f80a37fbccd/agent_input/task.md) · [PR](paper_reproduction/paper_2f0a4f80a37fbccd/agent_input/task.md) |
| `paper_0dcba54d6a1436bd` | 弱 B → 加强 B | 加入 PQCZCS；三分子的共同扭角与松弛几何比较；S1–S5 及必要扩根、NTO/CT 态追踪，分离受体、几何及态排序效应 | Gaussian/ORCA TDDFT，Multiwfn/等价转移密度分析 | [AR](autonomous_research/paper_0dcba54d6a1436bd/agent_input/task.md) · [PR](paper_reproduction/paper_0dcba54d6a1436bd/agent_input/task.md) |

软件列表示现有工具支持的参考开发路线。不同程序中同名基组、溶剂、色散或分析量仍需核对；软件可调用不等于新增研究矩阵已经完成或成本已确认。xTB 初猜不能直接代替要求的电子结构结果。

## 2. 已同步的任务组成

每篇两模式均沿用现有任务包组织形式：

- `agent_input/task.md`：保留 Scientific objective、Public inputs and scientific boundaries、Required scientific validation/investigation、Deliverables 标题。PR 增加原有 Author-provided scientific guidance 位置，明确“作者主张—候选路线/机理—有区分力的证据”。
- `agent_input/data/inputs/`：提供完整身份、允许使用的起始对象及实验观测；两模式一致。
- `agent_input/submission_schema.json` 与 `submission_guide.md`：记录真实作业、对象/态、能量、各篇特定结果矩阵、假设检验、敏感性和结论。支持真实早期失败、部分结果及有证据的构象塌缩。
- `evaluation/` 五份科学参考/评分文件：关键点、结论、规则、证据映射和严重科学错误均按新范围改写。两模式使用相同科学 evaluator；PR 的作者路线信息用于复现过程。
- `evaluation/reference_validation_plan.md`：逐篇说明正文/SI 来源、当前参考缺口、先导工作和科学验收条件。
- `evaluation/task_provenance/upgrade_audit.json`：来源哈希、状态、公开数据来源和升级记录。
- `evaluation/legacy_final_snapshot/`：保存复制时原包全部文件的逐字节 `.snapshot` 历史快照。**快照中的旧题、旧规则与旧 PASS 不在新任务中生效。** 历史文件里的相对路径需按记录的原来源目录解释。
- `task_info.json` 与 `package_manifest.json`：同步难度、交付物、可见性和所有现行文件哈希。

提交仍使用 `report/results.json`，同时明确要求可读的 `report/report.md`，由报告引用实际引擎输出与科学产物。主结果不允许仅以推测文本填满计算字段。

## 3. 科学边界与来源纠正

1. **苄醇：** Iₑ 与 Dₑ 均为约定的电子能差，不混入 ZPE/G，不把气相电离当绝对电极电位。单一 H 原子参考必须一致。检验预测可为数值或排序；已经看过结果时如实采用回顾检验，不能补造盲预测历史。
2. **环氧片段：** 作者方法段是 B3LYP-D3(BJ)，图注出现 CAM-B3LYP 的不一致已在 PR 中披露。以方法段为复现基线、其他层级单独列。分子偶极不等于树脂 Dk；对任意取向偶极向量求和不能代替 ⟨μ²⟩。
3. **并环戊搭烯：** NICS 使用完整张量对分子法向投影。源文正文和 SI 的响应基组不一致，PR 明确采用 SI 基线并披露差异。冻结骨架控制不能冒充自由极小值。
4. **锌配合物：** 对角 G 和交叉几何电子能分开；允许真实构象塌缩，不强造四个不同极小值。后 SCF D3 的同几何开关不能被解释成直接电子密度干预。红移与增强振子强度分开判断。
5. **铱硝酸根：** 从公开输入移出直接揭示 eta2 的旧 X-ray 参数，改为不固定金属—硝酸根连接的组成定义和未指派 IR。PR 将 eta2 作为作者假设提供。1532/1261/1223/802 与另含 1561 cm⁻¹ 的两套观测均需比较；源文没有明确通用数值缩放因子，不能冒称作者给定。
6. **发色团：** 补入 PQCZCS 的完整身份；其与 AQ 是同分异构体，不可混为一物；SI `[M+H]+` 分子式不作为中性计算式。AR 不预先提供特定分子的 CT/局域态赢家；PR 作者解释与新增共同扭角设计分开。

## 4. 科学评分和完成标准

科学评分总分为 100：对象/有效性 10，三项各篇特定研究端点合计 65，实际假设检验和定量稳健性 15，有证据的结论 10。新增对照、能量分解、系综或态匹配都进入评分，旧标量加一段机制文字不足以完成新版。

评分规则要求从原始文件核对定义、覆盖、数值相减、权重、张量投影、谱残差或态对应。对于拓展范围，现阶段使用有具体证据要求的条件/语义规则；**尚未伪造新的数值参考和容差**。源文数值及旧实际结果仅作为相同定义的基线参考；完整新增参考和方法敏感性建立后，才可冻结可接受数值范围。

计算支持作者、反驳作者，或完成充分对照后仍存在不可区分性，都可构成有效科学结论。少算一个必需端点、一次不收敛或没有执行对照，不等于完成了“不可识别性”研究。`bounded_failure` 可被提交格式接受，但不自动获得科学通过。

## 5. 已执行检查与限制

离线检查最终 **500 项通过**。检查详情：[离线验证报告](batch1_validation_report.json)；来源完整性：[source integrity](batch1_source_integrity.json)；版本清单：[implementation manifest](batch1_implementation_manifest.json)。

- 12 包通过官方包校验、内容哈希核验、运行时 evaluator 加载及公开文件导出。
- 6 对任务的科学指令、公开对象、schema 与五份科学 evaluator 一致；只保留必要的模式/作者指导信息差。
- 合成格式样例测试完整提交、真实早期失败分支及受支持的构象塌缩分支；负例覆盖缺新 panel、缺科学比较轴、错误电荷/自旋、旧标量提交、全部作业失败却标 complete、缺报告、私有/越界证据路径。
- 公开导出不含私有历史快照、evaluator 或 PDF；检查了旧关键数值泄露及特定态归属提示。
- RDKit 核对新增五苄醇 SMILES/分子式；重新统计保留五份 XYZ 原子组成，与本次任务定义相符。
- 对原始 final、hold、`docs/verification/all_verified_tasks/` 共 2,775 个文件核对哈希，全部未变；这些目录无新增文件。

合成样例仅用于验证契约，**不是模拟或真实科学结果**。本轮未运行 LLM 科学打分或新的量化计算，没有证明语义评分已校准，也没有声明 6 篇新版均已科学通过。

## 6. 下一阶段：逐篇先导和参考验证

建议仍按下表逐篇推进；不同论文可以独立完成，不要求阻塞论文拖住整批。

| 论文 | 最关键先导 | 开放/发布前必须补齐 |
| --- | --- | --- |
| d83 | 复核正确失 H 片段及一个新增取代三态 | 五系列、介质/构象和独立检验的完整证据及容差 |
| 2f302 | EPI2 OH 干预和释放，统一源方法口径 | 系综、低频处理、真实正常模和等价对照 |
| 628 | 一个共同骨架与探针网格 | 完整张量矩阵、几何/方法敏感性及残余混淆 |
| 9ec32 | 无 D3 优化、交叉单点与代表态追踪 | 各族实际端点、热化学/TD 敏感性及态对应 |
| 2f0 | 全配体 eta1/eta2 候选与正常模 | 候选覆盖、共同谱策略和实验可区分性 |
| 0dcba | PQ 身份、共同扭角和 CT 方法检查 | 三分子控制矩阵、态交叉和方法依赖 |

资源按实际科学引擎启动次数、分配 CPU 核数、墙钟小时、CPU 核时分别统计；分析工作包和后处理不算引擎运行次数。独立试运行和完整原始证据确认后，再决定正式发布和科学通过状态。

实施计划与完成记录：[BATCH1_PLAN.md](BATCH1_PLAN.md)。维护重查入口：[maintenance/README.md](maintenance/README.md)。
