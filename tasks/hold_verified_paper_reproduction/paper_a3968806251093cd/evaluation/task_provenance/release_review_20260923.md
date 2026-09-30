# paper_a3968806251093cd：修复完成与回头复核

日期：2026-09-23；模式：论文复现（PR）；group_2。

## 结论

用户批准的修订已落实。当前两个任务的指令、公开输入、提交格式及 evaluator 已同步；正确对象的既有成功计算支持修订后的几何比较任务，无需为此次修订新增 Opt/Freq。目录仍保留 HOLD，本轮不自动迁移到 final。此前本文件的“等待评分边界确认”已由本记录替代。

结论不是“任意初态都必然收敛”或“论文 SI 理论表逐数复现”。原始验证允许知晓作者路线；这里确认该科学子问题有真实计算解、输入可独立构建对象、评分不再误判合法构象。没有运行自动 LLM judge 或自主 agent 盲测。

## 修改落实

1. 正文 Fig.3、SI 与私有 CIF 共同支持正确取代位置的 E-imine/N5-H 7a。公开 mapped SMILES 补充 E 构型；未给 agent 提供最终二面角或任何坐标，未固定其他单键构象。
2. 保留 47 行实验观察及原子映射，实验 CSV/atom_map 与本轮前字节相同。新增公开 geometry_comparison.json，明确定义分单位 MAE/RMSE、有符号圆周二面角、每模型整个 11 行向量的整体反演选择和数值平局处理。它是 benchmark 比较约定，不冒充作者算法。
3. 保留两模式差别：AR 自选并论证至少两模型；PR 固定 B3LYP/CAM-B3LYP 与 6-311+G(d,p)。要求同一独立初始构象分别优化、提交实际输出和驻点证据；不新增全局构象搜索或实验 IR 比较。
4. 五个 evaluator 文件同步为 4 个实质关键点、1 个主要最终结论、5 条规则。真实完整结果支持的均匀优势、混合优劣或平局均可完成方法比较；缺少计算不是混合结果。PR 混合结果不能说成复现作者 CAM-wins 假设。旧强制 CAM 胜出及未定/混合混淆表述已移除。
5. 删除独立 limitation 结论/规则，使用框架已有 scientific_results 策略，不改全局评分逻辑。泛泛限制段落既不必交也不加分。保留对象、驻点和证据有效性检查；伪造/隐藏答案泄露仍按既有无效提交规则处理。
6. 重整 verified_computation_reference.md，仅把正确对象的两条成功链放入有效流程：来源、起点、实际方法和数值设置、日志、几何、频率、全部误差及比较均可追溯。旧混杂的 reference 原文存入本文件夹的 before_repair 快照，旧错异构体不得参与当前验证。

## 真实证据回查

四份 Gaussian 原始输出均正常完成优化/频率；各 132 个正频率。末态 XYZ 与日志最终坐标完全相同，完整元素标记连接图及每个重原子的氢分配与当前对象一致，E-imine/N5-H/0/1 均通过。每模型 47 项几何使用 numpy 与 RDKit 双实现核对。

- 来源 CIF 分支：B3LYP/CAM 二面角 MAE 8.241270836/5.521946286°，其余四项也支持 CAM；六项一致。
- 另一正确构象分支：B3LYP/CAM 二面角 MAE 4.678395135/5.544711005°，CAM 的键长/键角更好；构成完整混合比较。
- 四个实际端点在新增整体反演协议下均选择 +1；原验证的主要数值没有被改写。反演测试仅改变表示，不改变这些分单位误差或结论。

各模式重新执行只读脚本，26 项检查全部通过：真实链/格式/覆盖、整体镜像、刚体旋转平移、坐标重排并同步映射、圆周 ±180 边界、反演平局，以及漏行、重复行、错算误差、虚报赢家、错误映射、逐行翻转、错误整体符号和无效驻点的反例。反例均是本地测试变体，不冒充实际量化计算。

评分框架原生环境适配通过：4 个关键点、1 个主结论（结论轴总分 100）、5 条规则、generic_commentary_scored=false。测试没有新增数值评分插件；生产评估仍使用原框架的证据审阅及语义评分。

## 文件与复现入口

- [任务包、评分适配和实际输入分发检查](package_validation_20260923.json)：均通过。HOLD 不参与默认任务发现，因此使用临时目录中的原样副本测试；没有移动正式目录。实际只分发 6 个公开文件，未分发 paper_route、私有 CIF、计算结果或维护记录；未授权的私有 reference 读取被拒绝。
- [当前成功计算参考](../verified_computation_reference.md)
- [本地检查结果](repair_validation_20260923.json)
- [只读复核脚本](recheck_repair_20260923.py)
- [CIF 分支的新协议后处理](cif_7a_20260920_reprocessed.json)
- [另一构象分支后处理](si_conformer_20260920_reprocessed.json)
- [修改前 reference 完整快照](verified_computation_reference_before_repair_20260923.md)

在仓库根目录运行 `python tasks/hold_verified_paper_reproduction/paper_a3968806251093cd/evaluation/task_provenance/recheck_repair_20260923.py` 可重查几何和原始日志，不写文件、不运行量化作业。运行环境需 numpy、RDKit 和 jsonschema。包/评分适配检查使用项目 `.envs/researchchembench/bin/python`；系统 Python 未装 jsonpath_ng，已切换已有项目环境，未安装或改环境。

修改前完整任务副本：`/tmp/a396_repair_before_aBADKMy3/paper_reproduction`。没有覆盖 docs/verification 原记录，没有改其他论文或全局评分代码。

最后回头检查：当前 reference/report 的本地文件链接均存在；公开实验 CSV、atom_map 和私有 CIF 原始字节保持不变；包契约、JSON、规则引用、manifest 可见性及差异空白检查均通过。本轮没有发现阻碍已批准“真实完整几何方法比较”目标的残留问题。是否迁出 HOLD/发布仍是独立操作；本轮未做目录迁移。

## 补充修复：部分结果与额外尝试的提交格式

用户确认后同步修复两个模式。此前 26 项检查覆盖真实成功链和选定数值反例，未覆盖“主比较完成＋额外尝试失败”和“仅有部分主结果”两类格式路径；本段补充它们的修复与复核，不能把此前检查描述成已经覆盖这两类情况。

- `models` 只保存主比较中确有几何/证据的结果，最多两条；`complete` 仍必须有两个有效主模型、94 项观测、六项指标及整体反演证据。额外模型/构象的结果不得混入主比较数组。
- 新增可选 `attempts`，记录失败/未启动的主计算、重试与额外尝试；失败/未启动记录须有原因，已完成的额外尝试须有实际产物引用。已有主计算成功后，其早期失败记录不使整个任务降为未完成。
- `bounded_failure` 可有零个、一个或两个现有主模型记录。没有可用坐标时可留空结果列表并用 `mapping: null`，不再要求虚构第二模型、映射、坐标或文件；一旦有主模型或数值观测，仍须给真实映射。未完成报告必须有 `failure_reason` 且总体比较是 `unresolved_incomplete`。允许提交不等于完成任务或获得全部科学分数。
- 同步 task.md 的提交说明。没有修改五个科学 evaluator JSON、公开分子/实验数据/几何比较协议、历史计算结果、verified_computation_reference.md 或全局框架代码。

[28 项格式回归测试及结果](submission_contract_validation_20260923.json)在两个模式均通过，逐例使用 JSON Schema 和 runner 共用的 `validate_output_contract` 双重检查；[测试脚本](test_submission_contract.py)可用项目 `.envs/researchchembench/bin/python` 直接运行。测试中的失败情形是临时构造的报告，不是新量化计算。原 26 项只读几何/原始日志核查也重新通过，两个真实结果仍分别为六项 CAM 占优和混合优劣。

此次修改前的完整副本位于 `/tmp/a396_submission_before_2D7Mts/paper_reproduction`。目录仍保留 HOLD，未自动迁移。
