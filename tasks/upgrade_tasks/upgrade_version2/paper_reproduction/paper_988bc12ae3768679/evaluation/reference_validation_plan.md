# Reference validation and reuse

{
  "freeze_handoff": {
    "validation_group_not_authoring_batch": 5,
    "handoff_path": "docs/upgrade_tasks_v2_review_20260928/group_5/phase1/DEVELOPMENT_FREEZE_HANDOFF.json",
    "handoff_sha256": "b48a083f8b5cd4e6db80cf8adc372cf2b27b2e96143b1d7ca26108952729dc4b",
    "recorded_at_utc": "2026-09-28T15:05:46.703865+00:00",
    "scientific_disposition": "needs_work",
    "completed_evidence_summary": "六类原子映射候选各两套独立ETKDG/UFF初猜已生成并审查；12个UFF收敛仅属输入准备。首个水相CAM-B3LYP优化被平台中断，恢复01因checkpoint缺几何FileIO失败；恢复02保持原独立坐标和方法重新启动，已登记排队，未重复活跃作业。",
    "unfinished_scientific_or_input_work": [
      "酸碱不同位点/键型与构象的实际搜索、坍缩证据",
      "中性标定及所有保留候选DMSO NMR/水相UV",
      "配平质子热力学循环、溶剂/方法稳健性"
    ],
    "not_a_content_dispatch_gate": true,
    "job_status_refreshed_this_turn": false
  },
  "v1_reference_plan": "tasks/upgrade_tasks/upgrade_version1/autonomous_research/paper_988bc12ae3768679/evaluation/reference_validation_plan.md",
  "applicability": "十二个力场初猜只证明输入可构建；溶剂优化、光谱和质子循环参考仍待补，不把 UFF 收敛当科学最低点。",
  "new_scientific_calculations_performed": false
}

Source facts and author protocol were checked at the locations in source_scope_audit. Raw historical outputs remain read-only. Their stated conditions and unresolved validation issues govern reuse. New scientific runs were not performed for this content upgrade. No universal tolerance or full-reference PASS is asserted.

Minimum later validation: inspect the chosen route raw outputs, object/state/condition match and error model; test the criteria on genuine supported, refuted, partial and unresolved submissions. Actual semantic judge calibration is pending. Do not require the old matrix or restart all prior jobs.

Only candidate preparation and limited historical attempts exist; these are not physical minima or new spectra. Later validate at least one evidence-bearing route and semantic handling of acid NMR discrepancy and nonunique assignments. Source-specific errors must be calibrated, not taken from V1 narrow scalar tolerance.

## Content review addendum

Exact dated historical audit/raw locators and available file hashes: `task_provenance/evidence_reuse_inventory.json`. No new engine jobs or live job-status refresh occurred. The historical original matrices are not V2 mandatory operations.

Source-specific method, identity and scope restrictions remain in source_scope_audit and the current scientific rules.
