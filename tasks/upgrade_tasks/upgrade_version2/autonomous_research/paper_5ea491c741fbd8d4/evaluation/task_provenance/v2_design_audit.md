# V2 scientific design

{
  "old_task_diagnosis": [
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
  ],
  "question": "What intermolecular interactions account for the observed packing of the specified isoxazole crystal, and how strongly can the available evidence distinguish their roles? Establish which interpretations are supported, contradicted or unresolved within the authenticated crystal and the limits of the chosen evidence.",
  "agent_decisions": [
    "自主提出或修正作用解释；不提供接触类型候选表。",
    "选择表示晶体的模型、抽取范围、计算/分析方法、判别量和验证。",
    "决定何种证据能支持几何、能量或因果层级主张及何时收缩结论；不规定CP/面积/截断。"
  ],
  "public_input_changes": [
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
  ],
  "submission_and_scoring": {
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
  },
  "pr_alignment": "PR披露C–H···O/芳环接触、CrystalExplorer17.5及H标准化、指纹比例；孤立Gaussian09 B3LYP与6-311+/6-31+歧义单列。强调论文未建立相互作用能唯一排名；V1 CP/两个截断不是作者原路线或V2必做。"
}
