# paper_5ea491c741fbd8d4：逐篇V2方案

创建：2026-09-28T16:19:36.225288+00:00。此方案早于本篇V2复制/改写。

## paper_id

paper_5ea491c741fbd8d4

## batch

6

## source_documents

[
  {
    "path": "papers/paper_5ea491c741fbd8d4/documents/main.pdf",
    "sha256": "7621bdebf4659fb6c1e67f15c6ceda8dccbb4442eec850819fd613db4bc8ba6a",
    "material_type": "article PDF",
    "read_scope": "PDF pp2–4 methods/Table1/§3.2–3.3 and pp5–6 Figs2–5; p3 basis inconsistency verified"
  },
  {
    "path": "papers/paper_5ea491c741fbd8d4/documents/supplementary_001.pdf",
    "sha256": "4d381cbbbbade30dc691faf5ca339844b62b609a221568ee0f9a7983b29299a5",
    "material_type": "checkCIF report PDF, not a source CIF",
    "read_scope": "All4pages; checkCIF/PLATON alerts and drawing, no fractional-coordinate loop"
  }
]

## source_scope

{
  "question": "对指定E-isoxazole 1a真实晶体的分子间作用及堆积解释进行证据检验。",
  "identity": "C12H11NO3；完整27原子中性单重态单体；300 K测定P21/c，CCDC2445596，Z=4。",
  "observations": "只保留Table1实测晶胞和物质身份；完整结构坐标缺失。源接触指派、指纹百分比和稳定化说法是作者推断，留PR/私有。",
  "scale": "真实单晶中的分子间作用；不能由单体gap推出晶格自由能、酶抑制或生物效力。",
  "mapping": [
    {
      "fact": "身份/晶胞/300K",
      "source": "main p3 Table1; p4 §3.1–3.2"
    },
    {
      "fact": "研究相互作用与堆积",
      "source": "main p4 §3.2–3.3; Figs2–5"
    },
    {
      "fact": "SI不足以恢复坐标",
      "source": "supplementary001 all4pages"
    }
  ]
}

## old_task_diagnosis

[
  {
    "file": "agent_input/task.md; data/inputs/controls.json",
    "issue": "预设面积/最短接触作为稳定化代理；两种固定邻居截断、Hirshfeld面积与五能量CP路线。"
  },
  {
    "file": "agent_input/submission_schema.json",
    "issue": "hypotheses.minItems=2及surface/neighbors/cutoff_control矩阵。"
  },
  {
    "file": "evaluation/scoring_rules.json",
    "issue": "强制old邻居集合、own/ghost能量与截断扰动，无效地排除能回答同一晶体问题的不同证据。"
  }
]

## proposed_ar_problem

What intermolecular interactions account for the observed packing of the specified isoxazole crystal, and how strongly can the available evidence distinguish their roles? Establish which interpretations are supported, contradicted or unresolved within the authenticated crystal and the limits of the chosen evidence.

## agent_decisions

[
  "自主提出或修正作用解释；不提供接触类型候选表。",
  "选择表示晶体的模型、抽取范围、计算/分析方法、判别量和验证。",
  "决定何种证据能支持几何、能量或因果层级主张及何时收缩结论；不规定CP/面积/截断。"
]

## public_input_changes

[
  {
    "action": "retain",
    "file": "data/inputs/system.json",
    "reason": "完整化学身份和映射必要，不含答案坐标。"
  },
  {
    "action": "rewrite",
    "file": "data/inputs/crystal_source_specification.json",
    "reason": "保留观测数据并加原报道误差，不提供接触赢家。"
  },
  {
    "action": "remove_from_active_public",
    "file": "controls.json; development_gate.json; data_provenance.json",
    "reason": "旧矩阵及操作顺序移入私有V1归档，改中性input_status/resource_limits。"
  },
  {
    "action": "redact",
    "file": "task_info.json",
    "reason": "paper标题/doi等检索线索不进入盲AR公共metadata；保留私有来源索引。"
  }
]

## submission_and_scoring

{
  "structured": "source_structure、自由命名systems/quantitative_observations/claims/research_record、artifact_index及readable report；source必须为2445596。",
  "conditional": "报告实测packing完成需authenticated CIF；面积、能量、周期模型等主张各要求相称原产物与参考，不规定所有人采用某法。",
  "fairness": "支持/反驳/有效不可识别可得结果信用；没有真实坐标只能诚实bounded_failure/partial，不能靠泛论complete。",
  "weights": {
    "identity": 20,
    "quantitative_support": 25,
    "scientific_interpretation": 25,
    "uncertainty_limits": 20,
    "conclusion": 10
  },
  "process": "open_research实际AR/PR不同过程标准；保留真实决策/工具事件引用，不请求内部思维链。"
}

## pr_alignment

PR披露C–H···O/芳环接触、CrystalExplorer17.5及H标准化、指纹比例；孤立Gaussian09 B3LYP与6-311+/6-31+歧义单列。强调论文未建立相互作用能唯一排名；V1 CP/两个截断不是作者原路线或V2必做。

## existing_evidence_reuse

[
  {
    "path": "tasks/upgrade_tasks/coordination_20260927/batch6/source_review/local_cif_search.json",
    "sha256": "466708cc0ad93416040c44f1b86ea3e45e7604689f6ad4d7192055cf00a9dbb6",
    "description": "原作者本地CIF检索",
    "can_support": "真实输入缺口",
    "cannot_support": "不能证明世界范围不存在CIF"
  },
  {
    "path": "docs/upgrade_tasks_verification/group_6/papers/paper_5ea491c741fbd8d4/report/current_package_blocker_audit.json",
    "sha256": "88f1c1e916c2a60afe8aa4e823e237fd15e96983771d84ded30f32da7e7236b1",
    "description": "后续175CIF及当前包阻塞审查",
    "can_support": "输入未解除",
    "cannot_support": "不能作为相互作用结果"
  },
  {
    "path": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_5ea491c741fbd8d4/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot",
    "sha256": "7bbf9ea6bc5df6d657b74dfb4eced00310ae3f8136094bd694d8ff8242cb01ad",
    "description": "旧单体电子性质",
    "can_support": "身份/方法诊断",
    "cannot_support": "不能当晶体机制或相互作用能参考"
  }
]

## planned_changes

[
  "逐篇复制V1两包，私有保存V1所有非历史payload快照与来源哈希。",
  "重写task/guide/schema/公共中性资源和metadata；五evaluator共同科学标准；source_scope/design/visibility/scoring审计。",
  "声明blocked_missing_authenticated_cif，参考/判卷/隔离pending；不启动科学作业。"
]

## acceptance_checks

[
  "官方validate_task_package及官方payload hash；runtime open_research两轴100。",
  "AR/PR除作者路线以外public/schema/五evaluator一致。",
  "无旧强制路线；单模型及不同证据方法正例，旧gap/空证据/伪造CIF/错单位/缺真实产物反例。",
  "真实公开导出严格agent_input；另记环境隔离pending。"
]

## limitations

[
  "真实CIF未获得；本轮禁止新科学作业，不能宣称源晶体任务可科学执行完成。",
  "离线格式/完整性检查不替代科学语义judge校准；需协调者审查。"
]
