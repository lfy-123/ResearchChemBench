# Source scope audit

{
  "paper_id": "paper_3c058fa17fa7c54e",
  "source_documents": [
    {
      "role": "main",
      "path": "papers/paper_3c058fa17fa7c54e/documents/main.pdf",
      "sha256": "38002008855a03bf3bd90f3315f0008ae9fff275c1305e6fca20494ff3850e86",
      "material_type": "primary_article",
      "pdf_pages_1_based": [
        2,
        3,
        4
      ],
      "sections_figures_tables": "PDF2 Fig1/Scheme1 structures; PDF3 theoretical calculations; PDF4 Table1 dilute-toluene photophysics and singlet/triplet discussion."
    },
    {
      "role": "si",
      "path": "papers/paper_3c058fa17fa7c54e/documents/supplementary_001.pdf",
      "sha256": "01140712f70bcc77d7c656fcc6c211bc78e72aaac4e90d1d37e3b22b7a7162cd",
      "material_type": "actual_supporting_information",
      "pdf_pages_1_based": [
        2
      ],
      "sections_figures_tables": "PDF2 instrumentation and B3LYP/6-31G(d,p) Gaussian16 method."
    }
  ],
  "source_scope": "原文研究两个含饱和σ连接单元的蒽发光体、分子电子结构与溶液/器件光物理。V2截取两真实分子的激发态/溶液子问题；删除V1新乙炔桥材料，不要求重新证明器件设计。",
  "objective_source_mapping": {
    "main": "PDF2 Fig1/Scheme1 structures; PDF3 theoretical calculations; PDF4 Table1 dilute-toluene photophysics and singlet/triplet discussion.",
    "si": "PDF2 instrumentation and B3LYP/6-31G(d,p) Gaussian16 method."
  },
  "facts_and_constraints": [
    {
      "statement": "Measurements below are room-temperature toluene solution observations at 1e-5 mol/L; fluorescence lifetimes follow deoxygenation.",
      "source": "Main PDF4 Table1 footnotes a,b,g"
    },
    {
      "statement": "No raw replicate errors or triplet energy measurements are supplied. These observations do not themselves determine a microscopic emission mechanism.",
      "source": "Availability boundary of extracted main PDF4 Table1"
    }
  ],
  "identity_provenance": "Main PDF p2 Figure1/Scheme1 identifies the two full parent structures; V1 valence-checked mapped connectivity is retained without its added bridge models or terminal coordinates.",
  "decisions_open": [
    "agent决定哪些激发态/构象/介质表示能回答问题及何时追加证据",
    "自主提出两分子差异的解释、选择能否区分的比较，不给桥或扭角干预清单",
    "自主判断是否能支持TTA能量相容性与不可推断的动力学边界"
  ],
  "removed_v1_requirements": [
    "删除两个乙炔桥反事实及其三重态物种；原文未合成这些新材料。",
    "删除60°扭角、匹配臂地图和固定垂直/绝热全矩阵；不将其移入新私有评分。",
    "删除task_info的作者论文标题/DOI等可公开答案定位元数据；来源保留私有审计。",
    "统一两假设/三面板改为自主记录和按主张触发证据。"
  ],
  "out_of_scope": "Study only the two supplied covalent identities, with neutral singlet ground-state composition. States and conformations of these identities are open to investigation. Room-temperature dilute toluene solution is the observational context; a different computational representation must state its relation to that context. This task asks about molecular photophysics and energy compatibility, not OLED efficiency, film packing, TTA rate or quantum yield. No new bridge material is part of the target chemical space.",
  "feasibility": "Source main/SI gives a feasible molecular Gaussian route; chemistry_toolbox native Gaussian/ORCA manuals document molecule, geometry/frequency and excited-state capabilities. The existing parent graph audit passed. A solver may choose a defensible state calculation/analysis route; no new pilot was run and no CPU/accuracy guarantee is asserted.",
  "limitations": "V2 numerical reference accuracy and alternative-route semantic judging remain pending; source state/method wording is ambiguous. Molecular calculations cannot validate device or population kinetics. Runtime private-file access isolation is a separate pending framework check.",
  "source_scope_verified": true,
  "review_type": "Local relevant primary-text/figure review with explicit page mapping; no new scientific calculation."
}
