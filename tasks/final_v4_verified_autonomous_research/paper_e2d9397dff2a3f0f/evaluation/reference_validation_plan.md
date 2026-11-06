# Active V3 validation boundary — 2026-10-28

Historical status is USER_ACCEPTED_DEVIATION, not strict numerical replication. The retained opening RRHO barrier is 6.47915454585207 kcal/mol (target 6.2 ±0.5); documented thermal variants span 6.205814785–6.479287064. The matched-grid direct-attack result is 21.271705690975633 kcal/mol versus the unchanged Table S22-derived target 21.920259635394032 ±0.5: residual −0.648553944418399, FAIL for that numeric outcome. UltraFine gives 21.28054020860675, so the grid shift −0.0088345176311 does not explain the residual. Source-user acceptance of about 0.65 kcal/mol does not alter the current window. Native opening/direct saddles have one negative mode (−82.8205/−303.8323 cm−1) and mode/two-sided-descent evidence, not full IRC. The 15-point constrained-geometry electronic path in MeCN decreases by 30.6018173 kcal/mol over N–N 3.35→1.39 Å; it is not a solution free-energy path or proof of diffusion control. The optimized product has N–N 1.270210347 Å and ligand O–H 0.973232916 Å, with positive frequencies (minimum 31.5233 cm−1), supporting local N–N formation and oxygen proton acceptance. Source Figure S57 shows the corresponding H–N/H–O exchange. This evidence supports a local mechanistic comparison, not the whole experimental catalytic cycle.

当前局部解释可复用历史证据；直接进攻的严格数值复现仍需另行查明来源/模型差异，不能改窗。扩散控制或完整溶液自由能若另行主张需新证据，本版不要求且本轮不提交。 No new computation, blind run or online Judge calibration was performed. The historical plan and acceptance below are retained only as history.

---

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

# Reference validation plan — V2

Published bda/Py finite structures and TableS21/energy tables support model reconstruction and qualified source-baseline auditing. Existing local-mode work does not validate the old≈110i assignment or all new channels. Ligand constitutions and local inventories are sufficient public molecular inputs; source answer coordinates remain private.

## Source checked

- papers/paper_e2d9397dff2a3f0f/documents/main.pdf PDF pages [8, 9, 10, 11]; SHA256 c24bbaae86761a8d40104b001d415708990565d075c29789011a3c8104993875
- papers/paper_e2d9397dff2a3f0f/documents/supplementary_001.pdf PDF pages [25, 26, 47, 48, 69, 70, 71, 73, 78]; SHA256 1f4f524a63c1856d741bc9b9016079f9fe8ba2eea9117df6a2df9f72bd626975

## Reuse and gaps

- Independent local-state and N–N evidence and defensible numerical uncertainty remain pending.
- Source diffusion-control and global-RDS interpretations need stronger evidence than a monotonic electronic scan or local thermochemistry.
- Semantic calibration and isolation remain pending.

The exact existing evidence paths, hashes and limits are in task_provenance/existing_evidence_reuse.json. No new quantum, kinetic or HPC calculation was run for this content upgrade. A prior source value, successful execution or old PASS is not a V2 reference pass.

## Software and later validation

The repository chemistry_toolbox README defines Scientific/Data Actions, software-native jobs and agent-authored programs. The checked native guides include ORCA, Gaussian, xTB and CREST; numerical Python environments include NumPy/SciPy. These are capabilities, not compulsory methods or a promise of available allocation. Future calibration must first audit object/state/reference and raw evidence for a claim-relevant small case, then test an independently justified alternative or unresolved result if one is scientifically meaningful. Evaluate complete evidence for the chosen question, not the V1 fixed matrix. Resource/time feasibility and new numerical bounds require actual evidence; no new tolerances are invented.

Offline contract/linkage fixtures do not calibrate the semantic judge. Reference_status=pending; judge_calibration_status=pending; runtime_isolation_status=pending. This development round authorizes no scientific launches.
