# paper_c7217910ecbee1d9：逐篇V2方案

创建：2026-09-28T16:46:23.894155+00:00。此方案早于本篇V2复制/改写。

## paper_id

paper_c7217910ecbee1d9

## batch

6

## source_documents

[
  {
    "path": "papers/paper_c7217910ecbee1d9/documents/main.pdf",
    "sha256": "15a46fe1f07860776ac02e85707265593a747493fde6652f6eb7c32085ac1f87",
    "material_type": "article PDF",
    "read_scope": "PDF pp2–5全文相关段；p3实际Fig2/3图；p4 Fig4说明；PAl12 n0–2气相子问题，与p5 graphene区分"
  },
  {
    "path": "papers/paper_c7217910ecbee1d9/documents/supplementary_001.docx",
    "sha256": "b27d17f45ccc1f4d6de0567f4c939fc0ce1da8a12e000964a253908abb126671",
    "material_type": "actual supporting-information DOCX",
    "read_scope": "Computational details¶5–7；FigsS1–S4 captions及S2/S4实际图；S5–S9电子结构/稳定性说明；S10–S16与TableS1范围核对；无完整Cartesian表"
  }
]

## source_scope

{
  "question": "B(C6F5)3配体化是否及如何改变PAl12气相电子接受能力，所研究对象的结构/电子证据能支持何种解释。",
  "identity": "PAl12[B(C6F5)3]n，n=0/1/2；中性与单负离子。完整原子/配体图是体系身份，不把作者的icosahedral终态、para配位或特定自旋固定为答案。",
  "conditions": "孤立气相分子簇；作者Gaussian16/PBE0/def2-SVP为PR基线，AR自主选法并论证。",
  "scale": "仅PAl12及一个给定配体的n0–2子集；不含其他MAl12、Au、其他Lewis酸、graphene或器件。",
  "mapping": [
    {
      "fact": "配体化与电子接受能力研究问题",
      "source": "main pp2–4 Fig1–4及p5结论"
    },
    {
      "fact": "n0/1/2组成及原子身份",
      "source": "main p3 Fig2；SI FigS2、S4；总电子数由元素计数推导并标为账本"
    },
    {
      "fact": "相态和态的定义",
      "source": "SI Computational details¶5的分子计算与另列周期/AIMD段"
    },
    {
      "fact": "作者机理及方法为待检验参考",
      "source": "main pp3–4 Fig3/4；SI¶5–7"
    },
    {
      "fact": "外推边界",
      "source": "main p5 graphene是另外体系；仅气相PAl12不能检验跨shell家族普适性"
    }
  ]
}

## old_task_diagnosis

[
  {
    "file": "task.md; controls.json",
    "issue": "预给定位/弛豫两解释、vertical/frozen-core/density矩阵、先n2后其他路线；是指定执行。"
  },
  {
    "file": "system_specification.json",
    "issue": "固定doublet/quartet和singlet/triplet搜索下界；指定所有P–Al距离/图报告及配位接近方式。"
  },
  {
    "file": "submission_schema.json",
    "issue": "命名端点和固定控制分支，把自选证据锁为参考路线。"
  },
  {
    "file": "evaluation/scoring_rules.json",
    "issue": "按全部矩阵计完成；n2旧xTB失败曾误覆盖已有完整DFT证据。"
  }
]

## proposed_ar_problem

Determine whether and how B(C6F5)3 ligation changes electron acceptance by gas-phase PAl12 within the n = 0, 1 and 2 composition family. Develop and test an explanation consistent with the structures and electronic states actually investigated, and establish the scope and resolution of the resulting conclusions.

## agent_decisions

[
  "自定解释、预测与判别；不提示局域化/弛豫候选因果链。",
  "自选有物理依据的结构、自旋、配体排布、计算与分析；保持全部P/Al/配体原子账本。",
  "自选可说明电子接受能力的量及其几何/能量定义；不强制同时VEA、AEA、固定核。",
  "据实判断重构、解离或不可区分与可支持范围；有限搜索不能直接宣称不存在。"
]

## public_input_changes

[
  {
    "action": "retain",
    "file": "system_specification.json",
    "reason": "13/47/81原子、配体完整图、原子map、总电子数与电荷/自旋奇偶；这些是身份和物理约束。"
  },
  {
    "action": "remove",
    "file": "controls.json; development_gate.json; allowed_multiplicities; attachment",
    "reason": "删除固定核/两假设/搜索次序/完整矩阵和预选配位方式，改为版本及工具能力说明。"
  },
  {
    "action": "replace",
    "file": "electron_acceptance_conventions.json",
    "reason": "电子能量、ZPE或约束几何必须明确；给可换算定义，不给预期AEA/赢家。"
  },
  {
    "action": "private",
    "file": "source endpoint geometries, source article identifiers",
    "reason": "作者终态及全文路线不能进AR；SI缺Cartesian表，故使用公开完整图由agent自建初态，未虚构源坐标。"
  }
]

## submission_and_scoring

{
  "structured": "动态state_records（组成、电荷、自旋、几何、map、状态证据），动态attachment_assessments与quantitative_observations；允许独立定义物理量和后续修正。",
  "conditional": "声称AEA须正确中性/阴离子态、适用驻点/最低性证据；声称vertical须同几何；声称电荷/轨道解释须相应文件与适用性；并非四种分析全做。",
  "fairness": "非作者机制、重构或充分未决按证据评分；不存在固定n2赢家或统一数值容差。若仅检查n2，不能回答全家族趋势。",
  "weights": {
    "identity_states": 20,
    "acceptance_evidence": 25,
    "explanation": 25,
    "uncertainty_scope": 20
  },
  "enforcement": "host仅schema/required_files；author checker查ID/hash；实际科学与judge校准pending，不能混称自动拒绝。"
}

## pr_alignment

披露作者电子能级下移/电荷转移/保留superatomic态解释与AEA参考，Gaussian16 PBE0/def2-SVP自旋位点搜索、频率/ZPE和Multiwfn分析。PR需复现基线或论证替代，新增研究仍自主。明确VASP/AIMD和graphene为论文其他验证而非本题必做。

## existing_evidence_reuse

[
  {
    "path": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_c7217910ecbee1d9/evaluation/task_provenance/historical_n2_reaudit.json",
    "sha256": "d76f849f9a15e070197611079cf01b07218966083660255dd08b55ab5f0f699e",
    "description": "冻结V1的完整n2原生日志/图审计",
    "can_support": "PBE0/def2SVP气相81原子局部驻点可行性；电子与ZPE能量定义",
    "cannot_support": "非全局最低证明，非全n系列校准，也非现运行生成产物"
  },
  {
    "path": "docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_anion_m1_nonclashing_optfreq_20260916_20260916T224848Z/stdout.log",
    "sha256": "2e6a023a1ea77881664309e08d1ba227180db0ad6a2d34fcd7313e63dc68b02a",
    "description": "既有选中n2原生opt/freq日志；态=[-1, 1]",
    "can_support": "源方法、81原子计量、驻点/频率及条件性能量参考",
    "cannot_support": "不自动证明充分自旋/位点搜索；低频及SCF/弥散敏感性需独立审查"
  },
  {
    "path": "docs/verification/group_2/paper_c7217910ecbee1d9/provenance/qzcli_hpc/author_PAl12_BLA2_opposite_neutral_m2_nonclashing_optfreq_20260916_20260917T232712Z/stdout.log",
    "sha256": "fed8f6c4c9db933546a3347985b5e6a66191560ab638631ba2c208e37a54d5b0",
    "description": "既有选中n2原生opt/freq日志；态=[0, 2]",
    "can_support": "源方法、81原子计量、驻点/频率及条件性能量参考",
    "cannot_support": "不自动证明充分自旋/位点搜索；低频及SCF/弥散敏感性需独立审查"
  },
  {
    "path": "docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/report/n2_vertical_results.json",
    "sha256": "62f3c9f8c06c2534d75c887000194decaf36a6697c73b3eea9856df5477e5220",
    "description": "已存在n2固定中性几何能量与密度审计",
    "can_support": "相同几何下电子附着定义、历史参考原始日志路径及hash",
    "cannot_support": "后续稳定性/基组与新题整体语义尚未校准；其旧固定矩阵remaining不是V2必做项"
  },
  {
    "path": "docs/upgrade_tasks_verification/group_6/papers/paper_c7217910ecbee1d9/report/n1_stable_vertical_pair_audit.json",
    "sha256": "7ff6ae08e4702a3a830a14c2c02d03de0c63653369e46efc12785b005fdf0e3e",
    "description": "已存在n1双重态中性与单/三重态阴离子垂直对",
    "can_support": "特定几何与方法的稳定SCF及垂直量可行性",
    "cannot_support": "不等于自由阴离子AEA；同报告fixed-core量不是VEA"
  },
  {
    "path": "tasks/upgrade_tasks/coordination_20260927/batch6/source_review/cluster_raw_recheck.json",
    "sha256": "fbc212119c8214c8da26355471d1f7ba12dd081f0fc1ba388cf10cdd5cb1dbe6",
    "description": "旧xTB端点独立结构复核",
    "can_support": "原始失败/重构负例与身份误报防线",
    "cannot_support": "不得据此断言完整DFT对象不存在"
  }
]

## planned_changes

[
  "完成本篇方案后才复制两V1包；保留旧final和V1私有快照。",
  "将n0–2作为研究域，评分取决于主张覆盖，非固定端点矩阵。",
  "更新全部题面/公开图/metadata/schema/5evaluator/溯源与官方hash。"
]

## acceptance_checks

[
  "官方package/hash/runtime/export，AR/PR共同科学标准与过程策略有别。",
  "电荷/自旋奇偶、13/47/81完整计量和总电子数反例；高于旧枚举的合理自旋允许。",
  "仅旧3.93标量、失败冒充极小点、错能量定义/虚构证据不能科学通过；格式fixture与实际judge严格区分。",
  "复核已有原生日志hash，保持所有历史文件只读。"
]

## limitations

[
  "现有n2原始端点的Gaussian negligible-forces终止不意味着四个最后位移/力阈值全通过；参考需保留该细节。",
  "已有部分垂直和密度证据不构成V2全域验证；实际judge、全任务校准和运行隔离pending。",
  "不新提交、不控制也不终止任何既有科学作业；完整电子壳层结论只能按主张充分验证，不能从几何推断。"
]
