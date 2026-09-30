"""Write only batch6 delivery summary and immutable package/version index."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3]
IDS=['paper_5ea491c741fbd8d4','paper_72f60526b64ce1b6','paper_c7217910ecbee1d9']
validation=json.load(open(B/'validation_report.json'))
assert validation['status']=='passed'
records=[json.load(open(B/(pid+'_status.json'))) for pid in IDS]
for rec in records:
 rec['checks']={'official_package_validation':'passed','runtime_evaluator':'passed','scientific_weights':100,'AR_PR_scientific_parity':'passed','public_materialization_no_private_files':'passed','source_snapshot_and_hash':'passed','synthetic_output_contract_regression':'passed','scientific_reference_validation':'not_performed_blocked'}
 for p in rec['packages']:
  manifest=json.load(open(ROOT/p['path']/'package_manifest.json'))
  assert p['package_content_sha256']==manifest['package_content_sha256']
manifest={'date':'2026-09-27','batch':6,'scope':'Only assigned three normal-final papers; no hold papers.','development_packages_completed':6,'papers_completed_as_development':3,'scientifically_released_papers':0,'status':'development_complete_expanded_reference_pending','new_scientific_calculations_performed':False,'new_scientific_engine_launches':0,'short_work_performed':['RDKit graph/formula/mapping checks','SI coordinate-block atom-count checks','Recomputed historical endpoint P-Al distances','Read raw historical ORCA convergence messages'],'validation':{'path':'validation_report.json','sha256':hashlib.sha256((B/'validation_report.json').read_bytes()).hexdigest(),'checks':validation['checks'],'status':validation['status'],'repository':validation['repository']},'records':records,'entry_points':{'report':'REPORT.md','status':'STATUS.md','source_reviews':'source_review/','checker':'check_batch.py','builder':'build_batch.py + specs.py','source_audit':'review_sources.py'},'constraints':'No final/hold/original tasks/papers/verification/source guidance/common maintenance writes, no commit/reset/checkout; no child agents or quantum/HPC/paid service launches.'}
(B/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(B/'STATUS.md').write_text('''# 第6批最终开发状态

日期：2026-09-27。三篇均来自正常 final，非 hold。**3 篇、6 个 AR/PR 开发包已完成落地；科学发布为 0；两篇保留核心 blocked，簇体系历史 n=2 先导已恢复，扩展参考待算。**

| 论文 | 开发状态 | 核心阻塞 |
| --- | --- | --- |
| paper_5ea491c741fbd8d4 | 两模式任务、数据定义、schema、五份 evaluator、私有快照完成 | 未获得 CCDC 2445596 CIF；没有正确近邻与面积/能量先导 |
| paper_72f60526b64ce1b6 | 同上；补齐三种分子映射和五种结控制 | SI 中有结坐标，但无已允许并实际跑通的完整 NEGF 链和 ±V 收敛 |
| paper_c7217910ecbee1d9 | 同上；补齐 n=0/1/2 与电荷/冻结核矩阵 | 正式 SI 已在；历史完整 n=2 中性/阴离子 DFT 极小值已独立复核；垂直/密度、n=0/1、共同核与弥散敏感性待验证 |

'''+f'最终离线检查：**{validation["checks"]} 项通过**。新增科学引擎启动：**0**；未执行新的 LLM 科学评分，未生成新量化参考或容差。\n\n'+'''入口：`REPORT.md`（逐篇说明）、`manifest.json`（包路径/版本/缺口）、`validation_report.json`（检查明细）。每篇 `evaluation/task_provenance/upgrade_audit.json` 同时记录 `status: blocked` 与 `implementation_status: implemented_pending_expanded_reference`。任务格式通过不等于科学通过。
''')
report='''# 第6批论文开发升级报告

2026-09-27。范围仅含 assignment.json 的三篇正常 final 论文。已完成 **3 篇、6 个 AR/PR 开发包**，均按首版 **A→B 有界解释/假设检验**设计；不强行扩为 C。**两篇仍有核心阻塞；簇体系已解除历史 n=2 先导缺失的过时阻塞。0 篇可宣称新版科学已验证。** 这是用户授权的任务包开发交付，不是只保留方案，也不是扩大预算运行完整参考。

所有包均有任务正文、完整公开对象定义与控制矩阵、结构化提交契约、可读报告要求、五份同步科学 evaluator、参考验证计划、逐文件来源快照与哈希、更新的 task_info/paper_route/manifest。仅 PR 增加作者假设、原理和源路线；科学目标、可用对象、矩阵、schema、guide 和五份 evaluator 与 AR 一致。旧 scalar/旧 PASS 均不再构成新任务完成依据。

## 1. paper_5ea491c741fbd8d4：晶体接触面积与相互作用能

- AR：`../../autonomous_research/paper_5ea491c741fbd8d4/agent_input/task.md`
- PR：`../../paper_reproduction/paper_5ea491c741fbd8d4/agent_input/task.md`

**亲自核读的科学证据。** 正文 PDF pp2–4：XRD/Hirshfeld/DFT 方法、Table 1、源堆积的对称描述；p6 Fig.4/5 已渲染核看。Table 1 是 CCDC 2445596、P21/c、Z=4、C12H11NO3 的结构。SI 四页全部核读，确认为 checkCIF/PLATON 报告及椭球图，含 3 个 C 级、6 个 G 级警报，没有完整分数坐标与可重建源结构。不能从这个报告、晶胞参数或一幅 ORTEP 图伪造源 CIF。

**前提核查。** 对 CCDC 三个正常公开入口发起只读请求，均返回验证/CAPTCHA HTML，未取得 CIF；没有绕过验证。以 `rg --files --hidden --no-ignore` 枚举 papers/tasks/runs/workspaces/data_pipeline 共 146 个 CIF，未找到 2445596。初筛的数值子串匹配属于另一沉积号 2512981，已检查并排除。可复核记录是 `source_review/public_retrieval.json`、`local_cif_search.json` 和 `cif_paths_exhaustive.txt`。这里的结论是本次未取得可核验 CIF，不是声称世界上不存在该 CIF。

**已实质落地。** 公开 27 原子 E 异构体的映射图、完整化学计量/电荷/自旋，以及有出处的晶胞元数据。明确图标签不是未取得的 CIF 原子标签。新增控制以真实近邻为前提：用同一范德华半径表筛选至少一对原子满足半径和加 0.5 Å 的分子对，扩到加 1.0 Å 检查覆盖；这些是待先导检验的设计参数，不是源计算结果或误差容差。每个真正不等价二聚记录对称算符、平移、重数、54 原子配对和原子映射。面积按邻居及接触类型分别记录，不把接触次数冒充 Hirshfeld 面积。能量提交五个原始分量：二聚、两份单体本征基组及两份 ghost 基组；重算同几何 raw/CP 作用能，单独比较面积、距离和能量排名及有证据的并列。

**评估改动。** 晶体身份 15、面积/覆盖 20、作用能 25、排名/截断 20、可否证稳健性 10、结论 10，共 100。旧 HOMO/LUMO/gap 靶值退休。错误源结构、任意摆放二聚、错对称重数、松弛单体混入 frozen Eint、以有限二聚和声称晶格自由能均进入科学失败条件。SAPT 是可选；没有把它变为硬失败。

**现阶段限制与解除条件。** 缺真实 CIF→正确近邻和面积/能量代表先导→全矩阵及稳健性参考。Gaussian/ORCA 能做分子能量，但不能解决源坐标缺失；Hirshfeld/promolecular 面积实现也须实际展示，不假设 CrystalExplorer 已安装。包明确 blocked，不含虚构 CIF、二聚坐标、能量或新容差。

## 2. paper_72f60526b64ce1b6：桥型、分子极性与 Au 接触控制

- AR：`../../autonomous_research/paper_72f60526b64ce1b6/agent_input/task.md`
- PR：`../../paper_reproduction/paper_72f60526b64ce1b6/agent_input/task.md`

**亲自核读的科学证据。** 正文 PDF pp2–4 的 Fig.1、两阶段方法、偏压/电流定义和分子极性讨论；pp8–11 的传输解释、结论与方法出处。Fig.1 已渲染核对。A–D 是 acceptor–donor 标签，不是 A/B/C/D 四个物种；首版仅含 Group A 三种：无桥 AD、乙烯桥 ApiD、乙烷桥 AsigmaD。SI pp1–2 是三种孤立分子；pp5–10 确实包含 Group A 的含金结坐标；p16 是 Group B 尾部坐标。

**本轮纠正的输入判断。** SI 不是只有孤立分子。逐坐标块解析得孤立体系 22/26/28 原子；Group A 分子结 92/96/98 原子，均含 72 Au，分子部分比孤立分子少两个硫醇 H。RDKit 从孤立坐标核对连接图与化学计量；公开完整映射图、H21/H22 的移除定义和硫锚点。来源优化坐标留在私有 `evaluation/task_provenance/author_coordinate_blocks.json`，旧 AD 优化 XYZ 仅留私有 snapshot；AR/PR 都需自主生成起点，未泄露作者终态或排序。

**已实质落地。** 三种孤立中性单重态偶极为解释基线；新增五个明确结模型：AD_base、ApiD_base、AsigmaD_base、AD_reversed、AD_left_gap_plus_0p2A。每个必须有 −0.5/0/+0.5 V 的自洽 T(E,V)、I(V)、势降及原始积分证据。0.5 V、300 K 与左接触增距 0.2 Å 是本开发版的有限控制定义，不是捏造的新结果或容差。保持 Au(111)、统一横向超胞/接触定义、共同实验室左右坐标；反转分子时不偷换偏压方向。半无限 lead、中心区、赝势/基组/原子映射和 screening 仍必须形成实际可调用输入。定义 R=|I(+0.5)|/|I(−0.5)|，处理测得数值底噪及分母不可分辨性；孤立均匀电场或 U=−μ·E 不代替结偏压输运。

**评估改动。** 对象/允许链 15、真正 ±V/0 输运 30、桥/方向/接触对照 25、数值稳健性 10、解释 10、结论 10。契约硬拒缺桥成员、缺 reverse/contact、缺偏压符号、非自洽结果和反定义整流比；科学 evaluator 再核查实际 lead 与 T(E,V) 积分、费米参考和同对象条件。零场偶极不能得到新版通过。

**作者路线与新增部分。** PR 明确源文使用 Gaussian16 的两层 B3LYP 孤立路线、QuantumATK W-2024.09/PBE NEGF、SZP(Au)/DZP、4×4×130、75 Hartree 和固定 bulk/放松界面设置；没有把这些参数称作 SIESTA 已验证路线。统一反向/单侧接触控制是本次新增，未伪称作者已计算。源式的 Fermi 差排版问题已说明，以 f_L−f_R 物理定义为准。

**现阶段限制与解除条件。** `chemistry_toolbox` README、native guides、runtime config、src/evidence 检查只证明有 siesta 入口；未发现已审查完整 TranSIESTA/TBtrans 调用链或同结 ±V 实跑。源坐标不能替代 principal-layer、自能、赝势、restart 和收敛证据。需要工具负责人补正式链，完成一个 AD 的 0/±V 先导和 k/积分/电极层收敛，再做有限矩阵。没有修改公共配置、没有调用未授权子程序、没有宣称支持未证实的 NEGF。仍 blocked。

## 3. paper_c7217910ecbee1d9：完整 PAl12 核的电子接受与松弛

- AR：`../../autonomous_research/paper_c7217910ecbee1d9/agent_input/task.md`
- PR：`../../paper_reproduction/paper_c7217910ecbee1d9/agent_input/task.md`

**亲自核读的科学证据。** 正文 PDF pp2–5，p3 Fig.2/3 已渲染核看，p4 的轨道/电荷解释逐段检查。正式 DOCX SI 已存在，核读 Computational details、Figs S1–S9、Table S1，确认 Gaussian16/PBE0/def2-SVP、不同自旋/结合位点、频率与 ZPE、Hirshfeld/Multiwfn；VASP PBE-D3 与 300 K/10 ps AIMD 是不同的补充计算。SI 为图和文字，没有完整 Cartesian 表。缺口不是“SI 还没拿到”。

**旧证据的亲自复核。** 历史提交明确 bounded_failure。已读 `outputs/endpoints/analysis.json`，再从 neutral/anion XYZ 重算 P–Al 距离，得到旧 3.30 Å 诊断下分别 3/12、5/12，而非完整十二 Al 核；旧数据也显示 C–F 断裂。旧 3.30 Å 只是历史诊断，未升级为新容差。两份 ORCA job.out 最终明确写优化未收敛/达到最大步数。重构 GFN2-xTB 簇约 7.731 eV 不能替代原完整簇 AEA；频率通过不修复对象错误。证据见 `source_review/cluster_raw_recheck.json`。

**已实质落地。** n0/n1/n2 分别 13/47/81 原子；完整 PAl12、PAl12BC18F15、PAl12B2C36F30。明确核心 1–13、配体 A 14–47、B 48–81，逐个 B–C/芳环/C–F 键、完整配体组成、两电荷态与电子数奇偶性。新增六端点自由优化/态筛选和同层最低点证据，三份中性几何上的垂直阴离子，统一 bare-neutral n0 核坐标的冻结核控制；保留电子 VEA、电子 AEA、ZPE-修正 AEA 与阴离子松弛能的不同定义。固定核点不套用其它几何热修正，也不冒充自发稳定。每个配体数要求相同几何/网格附加电子密度与一致片段电荷交叉检查，再比较 n1−n0、n2−n1 的自由/垂直/冻结核差异。

**评估改动。** 完整身份/态 15、自由/垂直电子接受 25、共同核对照 20、密度/电荷 20、可否证性/敏感性 10、结论 10。原 AEA ±0.3 eV 规则未沿用，没有为扩展量伪造靶值。错误自旋奇偶性、未保核自由端点、混用 VEA/AEA/ZPE、不同核参考以及不同几何密度相减作为“纯加电子”均有明确拒绝条件。人口电荷与几何保留不能独自证明超原子壳层或“纯静电机制”；额外 CDA/角动量投影/场嵌入不列首版硬门槛。

**合理失败与坍缩。** 真实起点坍缩可记录，不强造不同极小值。对充分计算得到的 n2 模型排除提供带实际最终几何/Hessian/覆盖的结构化 partial 分支，invalid AEA 必须为 null，不能填重构簇数值。缺原定义 n2 完整中性/阴离子端点不能标 complete；n0/n1 小体系成功也不能解除原对象先导门。完成充分对照后得出的反驳或数值不可区分与支持作者同等评价。

**现阶段限制与解除条件。** 原定义完整 n2 的 DFT 最低点配对尚未成立；没有冻结核/垂直密度完整参考。必须先完成这个原对象先导，再扩大整个系列并校准弥散基组/自旋敏感性和真实不确定度。仅可用 n0/n1 作准备诊断，不以其替代门槛。仍 blocked。

## 4. 验证范围、版本与开发限制

最终 **CHECK_COUNT 项离线检查通过**，详情 `validation_report.json`：

- 六包 JSON 与 Draft 2020-12 schema、官方 `validate_task_package`、payload SHA-256；来源 final 每个文件与私有 `.snapshot` 哈希一致；来源正文/SI及指导文件 SHA 未漂移。
- 六包 `load_runtime_evaluation` 加载 flat scientific rubric，权重各为 100。三对模式公开数据/schema/guide、共同任务内容、五份 evaluator 字节级一致；PR 仅额外作者 guidance。
- 官方公开 materialize 的文件集合严格等于 agent_input；没有 evaluator、快照、paper_route 或来源优化 XYZ。
- 合成正常、反驳、不可区分、早期失败/partial、候选坍缩与证据化 n2 排除分支；负例覆盖旧标量、缺矩阵 panel、错 charge/spin、错源沉积号、缺 CP 能量、缺桥/接触/方向/偏压、错比值定义、错配体成员/核参考、虚频端点、越界证据路径、缺报告、全部作业失败/零引擎启动却标完整、缺原始产物索引。
- RDKit 核对三种输运分子及晶体单体的映射连接与分子式；簇配体逐原子计数和 36 键完整图、13/47/81 原子对应检查。

运行入口严格选择 `TaskRepository(roots=[Path('tasks/upgrade_tasks')])`，不改变正式库默认发现。其它批次并发写入时，全库有过哈希短暂不一致；检查器记录实际错误，并仅过滤候选目录到本批后调用相同的官方全部验证逻辑，没有跳过任何科学/包 validator。至少一次全库入口已成功；最新一次实际状态保存在 validation_report 的 repository 字段。

**合成样例只在临时目录使用并标明非科学数据。** 输出契约检验格式/字段，不能证明其引用的量化产物真实；科学 evaluator 明确需沿引用检查实际原始日志、几何、密度及算术。本轮没有运行新量子化学、周期或 NEGF 引擎，没有启动 HPC/子进程 agent/新付费服务，也没有执行新的 LLM 科学打分。短结构重算只复核旧失败，不生成新增参考或 PASS。全部新容差、正式参考和资源预算仍待实测。

维护重跑（仅本批脚本）：

```bash
PYTHONDONTWRITEBYTECODE=1 .envs/researchchembench/bin/python tasks/upgrade_tasks/coordination_20260927/batch6/check_batch.py
```

开发续写脚本在本批目录；已有包不会重新从 final 覆盖，快照先核验再续写。所有变更限定本批六包及 batch6 工作区；没有修改 final/hold/原始 task、paper 原文、verification、docs/evalution/update、公共 README 或公共维护脚本，没有 git reset/checkout/commit。

逐篇来源哈希、旧/新分类、状态和解除条件在各包 `evaluation/task_provenance/upgrade_audit.json`；批次精确路径/包哈希/检查摘要见 `manifest.json`。主进程可据这些入口逐篇亲自复核，不能把本报告当作三篇已获得科学通过。
'''.replace('CHECK_COUNT',str(validation['checks']))
(B/'REPORT.md').write_text(report)
print(json.dumps({'packages':6,'blocked':sum(r['status']=='blocked' for r in records),'checks':validation['checks'],'manifest':'manifest.json','report':'REPORT.md'},ensure_ascii=False))

# Preserve original author-history prose while making the supervisor correction explicit.
for filename in ['REPORT.md','STATUS.md']:
 p=B/filename
 if (B/'cluster_reference_update.py').exists():
  p.write_text(p.read_text()+'\n## 监督复核更正（2026-09-27）\n\n完整 n=2 历史 PBE0/def2SVP 极小值对已由 group_6 和 supervisor 独立复核。较晚 AR 失败不否定早期有效作者路线。旧“没有合法 n=2 对”的文字已被本更正取代。新增科学引擎仍为0；扩展垂直、密度、共同核和敏感性未通过。当前依据见包内 historical_n2_reaudit.json 及协调 ready 记录。\n')
