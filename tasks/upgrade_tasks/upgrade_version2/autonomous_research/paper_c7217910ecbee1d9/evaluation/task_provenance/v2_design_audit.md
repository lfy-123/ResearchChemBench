# V2 scientific design

{
  "old_task_diagnosis": [
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
  ],
  "question": "Determine whether and how B(C6F5)3 ligation changes electron acceptance by gas-phase PAl12 within the n = 0, 1 and 2 composition family. Develop and test an explanation consistent with the structures and electronic states actually investigated, and establish the scope and resolution of the resulting conclusions.",
  "agent_decisions": [
    "自定解释、预测与判别；不提示局域化/弛豫候选因果链。",
    "自选有物理依据的结构、自旋、配体排布、计算与分析；保持全部P/Al/配体原子账本。",
    "自选可说明电子接受能力的量及其几何/能量定义；不强制同时VEA、AEA、固定核。",
    "据实判断重构、解离或不可区分与可支持范围；有限搜索不能直接宣称不存在。"
  ],
  "public_input_changes": [
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
  ],
  "submission_and_scoring": {
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
  },
  "pr_alignment": "披露作者电子能级下移/电荷转移/保留superatomic态解释与AEA参考，Gaussian16 PBE0/def2-SVP自旋位点搜索、频率/ZPE和Multiwfn分析。PR需复现基线或论证替代，新增研究仍自主。明确VASP/AIMD和graphene为论文其他验证而非本题必做。"
}
