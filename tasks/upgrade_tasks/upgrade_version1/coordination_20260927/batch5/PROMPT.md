你是 ResearchChemBench 本批论文升级实施负责人。用户已明确授权：启动五个 Codex 进程，均用 gpt-6-astra、max 推理强度，完成剩余第2至第6批论文的升级，然后由主进程亲自复核。你是其中一个独立进程，必须把本批全部论文的 AR 和 PR 开发版任务包实质完成，不要只写计划或仅汇报。不再启动子进程/子agent，不问许可。

最终目标：基于现行 final 包，复制至 tasks/upgrade_tasks/{autonomous_research,paper_reproduction}/paper_id，按逐篇升级方案把科学问题提升至首版规格的 B/C 范围，保持原任务组织形式，并同步科学 evaluator。重点是可否证解释、对照、候选/路径判别和稳健性，而非仅增加作业或假设文字。用户接受 B 类自主科研，不强行把所有论文做成 C。

【只写你的范围】
- 仅可写本批论文在 tasks/upgrade_tasks/autonomous_research 和 paper_reproduction 下的目录；以及 tasks/upgrade_tasks/coordination_20260927/batchN/ 下的脚本、审查、状态、测试和总结。
- 不修改任何 final、hold、原始 tasks、自身批次外论文、papers 原文、verification 结果、docs/evalution/update 方案或公共 README/维护脚本。仓库已有大量其他工作改动，不 reset/checkout、不提交git、不清理别人的文件。
- 可以读取全仓库及已有 source PDF/text/run evidence。不存在的目标才复制，重启时检查现状后续写，不覆盖已有进展。

【必须先读】
1. docs/evalution/update/upgrade_implementation_guide_20260927.md
2. docs/evalution/update/upgrade_guidance_review_20260927.md 和同名 manifest JSON 中本批记录
3. 各 docs/evalution/update/paper_id.md 顶部首版实施规格和正文/SI/历史证据链接；逐篇查看对应论文正文/SI 的相关实质段落/图表，不仅转述方案。
4. 本批 final AR/PR task、public data、schema、evaluator。
5. tasks/upgrade_tasks/README.md、第一批任意两个完整包、maintenance/check_batch1.py；它们是结构和质量参照，不可将其化学细节复制给别篇。

【逐篇必须落地】
- 从 final 复制 AR/PR 两包，记录来源 hash；原包内容存私有 evaluation/legacy_final_snapshot/*.snapshot，原始证据/旧PASS不得成为新任务的完成声明。
- agent_input/task.md 保留 Scientific objective、Public inputs and scientific boundaries、Required scientific validation/investigation、Deliverables 等原格式，科学英语；PR 在 Author-provided scientific guidance 中给出作者假设、原理、机理、源方法，准确区分作者原研究和本次新增对照；AR 不泄露作者赢家、终态归属、待预测值。
- 两模式同科学目标、相同可用对象/数据、同提交契约、同完成标准和五份科学 evaluator（key_points、conclusions、scoring_rules、critical_failures、evidence_map），唯作者路线信息差异允许。严格控制论文规模，顶部 optional 不成为硬性失败条件。
- 提供足够可实施的新增物种身份、连接关系、化学计量、电荷/自旋、原子对应和控制定义，必要时补公开源数据；不能用一句“加更多候选”替代具体输入。公开实验观测可用，答案坐标/作者终态/参考输出留私有。写出处和页/图/表证据。
- submission_schema.json 与 submission_guide.md 要实质表达新增研究矩阵和可审计数字、原始证据文件，不只是一个任意自由文本对象。必须要求 report/results.json 和可读 report/report.md。合理失败允许提交但不等于科学通过；缺核心对照不能用“不确定”替代完成。允许实证的构象坍缩或科学不可区分性。
- 重写 evaluator 的中间关键点、最终结论与权重绑定新提交字段/真实原始产物；参考定义和科学误差边界清楚，奖励计算推理而不是复述作者。对支持、反驳及证据充分的不可区分结论保持公平。至少拒绝仅旧标量、缺新增比较、错误对象/态/能量基准、失败冒充完成。
- task_info.json、paper_route.md 如存在、package_manifest.json 同步新范围；所有 payload hashes 用 evaluation.contracts.task_package 的官方函数刷新。运行时采用 TaskRepository(roots=[Path('tasks/upgrade_tasks')])，不改默认正式库发现机制。
- evaluation/reference_validation_plan.md 写已查正文/SI、旧参考可复用部分、新增参考缺口、可调用软件和最低先导/完整验证步骤；evaluation/task_provenance/upgrade_audit.json 记录 source、source docs、old/new class、status、new_scientific_calculations_performed。

【科学真实性】
当前请求承接第一批的“任务包开发升级”，不是无预算运行65篇完整量化验证。不启动长时间量化计算/HPC或新付费服务；可做短结构检查/已有数据计算。未完成新增科学参考时状态明确为 implemented_pending_expanded_reference；不得伪造新数值/容差，不机械沿用旧狭窄目标 ± 范围，更不能声称新版已验证通过。合理的方法/软件范围以 chemistry_toolbox README/config/native guides 和真实证据为准。局部分子属性不能声称证明产率/器件/体相结论。
输入或方法确实阻塞：亲自核查，做本批可完成的开发和证据定义，包和批次报告显式 blocked，缺项和解除条件具体。不能凭空生成源CIF、未支持的NEGF或有效极小点。不要假装阻塞已解除；不要只为覆盖数把不能实施的任务宣称就绪。

【验证与交付】
逐篇同步后用 .envs/researchchembench/bin/python 检查：JSON/schema有效性、validate_task_package、load_runtime_evaluation、权重、公开materialize不导出evaluator/快照、AR/PR科学和public/schema一致、源快照hash、论文特异的正反例提交契约。参照官方 output_contract 做负例，必要写 batchN/check_batch.py；测试不得绕过科学失败或靠放宽schema通过。合成样例仅在临时目录且标明非科学数据。边做边更新 batchN/STATUS.md，明确已完成/进行中/阻塞。
最终写 batchN/REPORT.md（中文逐篇科学升级、正文/SI依据、评估改动、可行性、限制）与 batchN/manifest.json（全部论文、两个包路径、状态、新参考缺口、检查摘要）、batchN/validation_report.json。主进程稍后亲自检查，不要写公共汇总。
每篇结束保存，不能等全批结束才写文件。确保本批每篇都有确切、可审查的结果。最终答复给出完成数量、阻塞和文件入口，不要以仅计划结束。

【你的唯一批次】第 5 批：高级方法、实验数据与专门接口；共 15 篇。
本批工作区 tasks/upgrade_tasks/coordination_20260927/batch5/。
全部论文 ID：
paper_0cd74ae20ab933f3
paper_2c439196c2f349c9
paper_3316e45a74258fb7
paper_3d1d9b7f6df049da
paper_72822e4ddb5d9b11
paper_80441aced6051d86
paper_94b0a8ae694590ea
paper_988bc12ae3768679
paper_a21b91f97ce3c68f
paper_b5c446c7067dd511
paper_c23cfabbd34b087f
paper_d8e5490cd9942f4f
paper_e0791c047a731974
paper_e31cc7bc7b21b610
paper_eda19e7c8edd4b39
完整记录在该工作区 assignment.json。
