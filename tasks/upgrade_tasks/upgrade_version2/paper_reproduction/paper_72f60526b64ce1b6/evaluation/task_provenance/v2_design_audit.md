# V2 scientific design

{
  "old_task_diagnosis": [
    {
      "file": "task.md; controls.json",
      "issue": "直接提供偶极预测假设、桥型/反向/单侧接触解释轴及五结0/±0.5V矩阵。"
    },
    {
      "file": "submission_schema.json",
      "issue": "固定devices键、两假设、300K、比值方向及numerical_checks。"
    },
    {
      "file": "evaluation/scoring_rules.json",
      "issue": "按矩阵操作计结果信用而非agent自己证据能否判别桥型解释。"
    },
    {
      "file": "upgrade_audit.json; old ready",
      "issue": "旧仅siesta声明已过时；当前有工具链，真实有限偏压仍未校准。"
    }
  ],
  "question": "Determine whether and under what conditions the bridge changes rectification within the supplied Group A molecules in Au(111) junctions. Develop and test a molecular-level explanation for the response, and establish how far the evidence supports it within the stated junction and bias domain.",
  "agent_decisions": [
    "自己选择电子结构/输运解释和可证伪预测，不预给偶极或取向机制。",
    "选择结构/接触表示、研究顺序、偏压取样和验证；源三分子是研究域不是强制五结矩阵。",
    "定义可换算整流度量、可比性控制和不确定性；不靠固定±0.5V反向控制判定完成。",
    "决定哪些证据支持桥型而非其他混杂，必要时收缩结论。"
  ],
  "public_input_changes": [
    {
      "action": "retain",
      "file": "systems.json",
      "reason": "保留完整图/原子映射/端基计量，不泄露源优化坐标。"
    },
    {
      "action": "replace",
      "file": "controls.json;development_gate.json",
      "reason": "改Au(111)对象域和工具/输入现状；移除五结、0.2Å、0.5V、固定温度。"
    },
    {
      "action": "add",
      "file": "measurement_conventions.json",
      "reason": "固定单位/化学势差只是可复核约定，允许逆比值/方向经明确转换。"
    },
    {
      "action": "redact",
      "file": "task_info.paper",
      "reason": "源全文检索标识留私有，防止公共metadata提供作者路线。"
    }
  ],
  "submission_and_scoring": {
    "structured": "自由devices、transport_points、rectification_assessments，bias/current/temperature/mu、原始计算依赖与物种映射；无必做device名称。",
    "conditional": "声称整流需同一器件的正负响应或可核验等价证据；只给偶极不够。方法可以不同但必须真实输运且相应近似得到论证。",
    "fairness": "允许无显著整流、源趋势反转、充分未决和真实部分结果；错误参考/对象不能完成。",
    "weights": {
      "identity": 15,
      "transport_evidence": 30,
      "explanation": 25,
      "uncertainty": 20
    },
    "process": "实际open_research AR自主设计、PR披露协议复现；用managed event和文件判断，不按job数给分。"
  },
  "pr_alignment": "披露Gaussian16/B3LYP孤立两层计算及固定S；QuantumATK W2024.09 NEGF/PBE、Au111、SZP/DZP、4x4x130、75Eh、四层Au与0.05eV/A，源GroupA弱整流及作者桥型解释。源公式Fermi差排版异常需要物理解读。构建者反向/0.2Å为旧新增不再必做；不强迫结果重复作者。"
}
