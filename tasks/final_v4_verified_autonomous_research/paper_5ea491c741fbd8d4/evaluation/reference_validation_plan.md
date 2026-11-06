# Scoring applicability — 2026-10-29

This document retains source/verification context. Only current scoring_rules.json controls scoring: independent semantic pass/fail final conclusions, without numerical target windows or author-workflow requirements. Historical scientific findings below are unchanged and are not new validation.

# Current V3 evidence status — 2026-10-28

Retain the authenticated isoxazole crystal-packing question. Eight final outcomes comprise five surface fractions, the directional contact network, quantitatively defined aromatic packing and a distinct interpretation of surface prevalence; no new energetic task or chemical identity is introduced.

Existing matched evidence is reused; the old acceptance does not automatically establish all V3 outcomes. Known limits: CE25.8/OCC is an evidenced substitute for CE17.5, not exact software/session identity; Deposited Z geometry conflicts with the source E name; centroid norm and source 3.3883 angstrom label conflict; Exact source hydrogen policy and crystallographic covariance are unavailable; no energy ranking or lattice thermodynamics follows; No new V3 semantic calibration or blind run. No new computation, semantic judge calibration or blind AR run was performed. See verified_computation_reference.md and reference_qualification.json for the current mapping.

## Historical validation plan (not current scoring instructions)

# 当前验证状态（2026-10-11）

**科学参考验证已完成：STRICT_PASS，限当前评估任务科学范围。** 完整实际计算链、源值对照、全部当前关键点/结论以及限制见 [verified_computation_reference.md](verified_computation_reference.md)。最终依据为 2026-10-11 逐篇严格复审；小数值偏差及来源冲突均在该文档保留。

下文是升级时的原验证计划，保留作历史来源。其当时的 `pending`、缺失计算、材料待补等表述不代表最新科学验证进度；是否已经完成以当前计算参考及其证据为准。语义 judge 校准、运行时隔离等工程状态没有因科学参考通过而自动更新。

---

## Existing crystal-distance evidence integrated (2026-09-30)

This is a readback of completed group_6 evidence, not a new scientific calculation. Exact source/artifact SHA256 values, JSON pointers and code lines are in `task_provenance/crystal_distance_definition_20260930.json` (evidence ID `crystal_distance_definition`). This current block supplements the dated source-input and historical records below.

Main PDF physical page 4, section 3.2 calls **3.3883(6) Å** the centroid-centroid distance between Cg(1) = C9/C10/N1/O2/C11 and Cg(2) = C2/C3/C4/C5/C6/C7, with `1-X,-1/2+Y,1/2-Z` applied to the second ring. The existing independent `mesh_audit_results.json` `/ring_audit/0` records centroid distance **3.7482107116485768 Å**, distance of the original isoxazole centroid to the transformed phenyl least-squares plane **3.3883651950048885 Å**, and the reverse centroid-to-plane projection **3.4702085265602602 Å**. The plane angle is 3.2498635023634437 degrees; the centroid-vector angles to the two normals are 22.20604817404553 and 25.311683282213288 degrees. These are preserved recorded digits, not new error bars.

Centroids are arithmetic means of the specified Cartesian atom positions; each least-squares plane passes through its centroid. The centroid norm and the two absolute normal projections are different quantities. The planes are tilted, so a single generic interplane separation is insufficient. Native `packing.json` for the isoxazole-inside pair uses `-x,y+1/2,-z+1/2` plus translation `[1,-1,0]`; its `plane_separation_A` projects onto the **inside** normal and therefore records 3.4702085 Å. It must not be relabelled as the 3.3883652 Å outside-plane projection. The independent ring audit records both projections explicitly.

The printed magnitude is close to the outside-plane projection, but that numerical proximity establishes neither the author's intent nor an authenticated erratum. Retain the source's centroid label and the independent results as a quantity-definition conflict. Do not change source coordinates to fit a printed number, make 3.3883 Å a hard centroid target, or use the source parenthesized uncertainty as a tolerance for another quantity. Cell/coordinate uncertainties were not propagated in the archived audit.

Applicability is limited to unchanged deposited **Z** coordinates and this atom-labelled ring/symmetry mapping. Historical E-labelled monomers are not interchangeable with this source object. Both modes may receive credit for an independently evidenced physical-label correction; other valid AR routes remain eligible and this ring pair is not a hidden mandatory investigation. Local geometry and existing finite surface evidence do not certify whole-question completion, causal stabilization or an interaction-energy ranking. Real semantic judge calibration and blind AR remain unperformed by this writeback.

For further reference review, reuse the listed immutable geometry artifacts and check submitted definitions, mappings and raw evidence against the claim actually made. This writeback does not request duplicate geometry or surface jobs. If a submission makes a quantitative uncertainty claim, require its own justified resolution or propagation; if it claims energy or causality, require the corresponding independent scientific evidence. Keep the source d_norm conflict and CE25.8 versus author CE17.5/session-comparability boundary separate from this distance issue. Existing group_6 surface acceptance remains partial and is not elevated here.

## Current source-input correction (2026-09-30)

The previously missing source coordinates were supplied by the user and integrated into both current V2 packages. See task_provenance/source_recovery_20260930.json for exact source and derivative hashes, retained/removed CIF fields and the input-only parser checks. CCDC 2445596 and SI 1a.cif are byte-distinct but match all retained scientific structure fields. The derivative preserves labels, coordinate/ADP uncertainty strings, occupancies, explicit symmetry, unit-cell metadata and constrained H rules. A graph-label bijection and input provenance are supplied. Original attribution/refinement/geometry payloads and supplementary ZIP/DOCX are available only to PR; checkCIF is provided to PR as page-labelled text because the official public package excludes PDFs; AR receives the same structure without precomputed geometry tables, author interpretation or SI answers.

The old missing-coordinate prerequisite is resolved at the package-input level. Source identity is supported by user-provided deposition metadata and independent SI consistency; the intake did not record a download URL and this integration did not perform live CCDC authentication. Source reception, syntax/identity validation, reproduction of a scientific node, whole-question scientific acceptance and real judge calibration remain distinct. No contact, Hirshfeld surface, energy, mechanism, or new scientific reference result was calculated by this integration. No old monomer PASS or surface fraction becomes an acceptance tolerance.

Group6 owns scientific validation. Its next useful reference must use the actual crystal and atom map, establish claim-appropriate validity/uncertainty, and assess coverage. PR retains the source d_norm range/unit conflict, intramolecular S(7) versus intermolecular R2^2(9), and the distinction between surface area/geometric proximity and stabilization energy. Neutron normalization must be explicit; the supplied H positions are the original constrained X-ray model. A full surface-engine/alternative-method acceptance and expanded reference remain pending here. No exact CrystalExplorer implementation is asserted installed or calibrated. Input availability is not a full capability-ranking or scientific PASS declaration.

Earlier dated audits, repair records and the historical sections below describe their recording times. Their missing-CIF statements are superseded by this correction, not erased; legacy snapshots remain immutable.


## Source stereochemistry correction (2026-09-30)

The supplied 1a crystal has Z geometry for benchmark 7=8 under CIP: at C9, C11(O,O,O) outranks C10(N,N,C); at C8, C5 outranks H8. The original CIF itself tabulates C11-C9-C8-C5 as 7.4(3) degrees. RDKit reassignment after clearing all stereo annotations and atom-map numbers independently returns Z. Article pp1 and4 use the name E; this is preserved as a source conflict. Only the current mapped SMILES identity is aligned to the physical input; no coordinates or originals were altered. Methyl atoms do not receive stereocenter annotations. Historical E-labelled isolated-monomer results cannot be assumed to be this configuration without inspecting their actual geometry and mapping; they are not crystal evidence.

## Preserved historical record — superseded input availability

# Source and reference plan

Read main PDF pp2–4 and pp5–6, Table1/§3.2–3.3/Figs2–5; checked all4pages of the real checkCIF SI. Source cell and graph are valid known facts; full coordinates are missing. Original isolated-molecule calculations do not calibrate crystal interaction claims. Historical source-acquisition audits remain evidence of the input gap, not proof that a deposition does not exist.

No reference workflow is compulsory. When an authorized source CIF becomes available, first authenticate composition, cell, labels, symmetry, occupancy and H conventions. A future smallest useful reference should demonstrate at least one source-linked representation with reproducible data of the kind claimed, and test its actual uncertainty. A broader reference should calibrate the scope claimed by the eventual investigation; do not prescribe the old 0.5/1.0-angstrom neighbor matrix. Managed molecular quantum tools may support selected energy analyses; an installed area or periodic analysis capability must be demonstrated separately. No new calculations are run in this content-upgrade phase.

This V2 development did not launch scientific jobs or a semantic judge. Future scientific calibration is a separate authorization/workstream. Existing evidence is listed with SHA256 in task_provenance/existing_evidence_reuse.json. No old narrow target interval is inherited. Alternative routes require method-appropriate uncertainty; source agreement alone is insufficient. Access-control isolation and actual judge calibration remain pending.

## Integrity repair reference handoff (2026-09-30)

Source anchors: Physical PDF pp2-3 methods (p3 continuation: d_norm -0.18 to 1.4, a.u.), p4 sections 3.2-3.3 (-0.676 to 1.415, angstrom; intra S(7)/inter R2^2(9)), pp5-6 Figs2-5 shape-index/curvedness; all four SI checkCIF pages contain no coordinate loop.

Existing isolated-monomer evidence remains reusable only for its molecular properties. The real SI checkCIF report does not provide fractional coordinates. Before any complete reference: obtain and authenticate CCDC2445596 CIF, reconcile disorder/occupancy and graph mapping, and then test the source intra/intermolecular and surface interpretation. Record the d_norm source conflict explicitly; do not invent a tolerance or infer stabilization energy from surface area. No authenticated CIF was added by this repair; exclude from complete capability ranking until the operator supplies it.

Named artifact SHA256 values and read timestamp: evaluation/task_provenance/integrity_repair_20260930.json. This bounded snapshot does not claim to be a live status monitor. Source agreement, syntax validation and local convergence do not certify the whole revised question. Real semantic calibration, scientific reference completion and runtime enforcement remain separate outstanding work.
