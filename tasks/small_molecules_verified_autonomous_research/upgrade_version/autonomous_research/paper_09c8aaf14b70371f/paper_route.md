# Current scope and scoring — 2026-11-03

Using computational chemistry evidence, estimate the relative reduction tendency and cathodic peak-potential ordering of the five supplied E-chalcones, compare it with the measured ordering, and explain agreements or departures in terms of molecular structural differences and solvent effects. This is an explanation task: the measured peak potentials are given; the computational relationship and its physical interpretation are to be established.

The existing scientific scope is retained.

Only the following independently supported outcomes receive points:

- series_3_5: Substituent-dependent reduction relationship for compounds 3–5 (25 points).
- hydroxy_departure: Applicability of the computed reduction relationship to compounds 1 and 2 (20 points).
- acn_dmso: Scale of the ACN/DMSO solvent effect across all five compounds (15 points).
- dcm_comparison: Direction of the compound-3 DCM/polar-solvent comparison (10 points).
- bounded_relationship: Molecular hypothesis for the peak-potential differences and its evidential limits (30 points).

Original evidence and historical qualification are retained below. They do not impose deleted work or automatically certify the revised task. No new quantum jobs or blind-agent runs were performed.

<details>
<summary>Historical paper route before this revision (not active requirements)</summary>

# Active scoring revision — 2026-10-29

Only independently weighted final scientific conclusions in scoring_rules.json are active (100 total; semantic pass/fail only). No numeric target/tolerance, author-node completion or process gate is active. Historical route descriptions and older scoring allocations below are source context only. Original scientific scope, real computational-evidence requirements and historical scientific acceptance are unchanged.

# Private source and V3 result map: chalcone reduction relationships

The public task is explanatory. All five mapped E identities and all supplied CV measurements are retained. Active rules are r_series_3_5 (25), r_hydroxy_departure (20), r_acn_dmso (15), r_dcm_comparison (10), and r_bounded_relationship (30). The last rule scores a computed molecular hypothesis, not repetition of the first four comparisons.

Sources directly checked: main PDF p.2 §2.3 (B3LYP/6-311+G(2df,2p), Gaussian16, IEF-PCM, neutral/reduced states); p.7 Table4 (experimental and orbital values); p.10 Table6 (2/E1 minimizes G while E2 minimizes E); pp.12–14 Figs.11–14 and discussion; SI pp.1–3 chemical names/characterization and pp.24–27 coordinate blocks. SI lacks a unique solvent/state/conformer label for its coordinate sets. Do not guess the exact Table4 compound-2 conformer.

Table4 neutral LUMOs in ACN/DMSO (eV), source context only: 1 −2.537/−2.540; 2 −2.493/−2.496; 3 −2.538/−2.540; 4 −2.470/−2.473; 5 −2.293/−2.298. Compound3 DCM: −2.508. The source prose '<0.004 eV' conflicts with Table4's 0.005 eV for 5 and is not a hard gate. No active numerical tolerance is added.

Native review: docs/verification/small_molecules_autonomous_research/dispatch_core7_20261012T190159Z/continuation_20261015T014600Z/review_09c8_native_checks.json and parent_09c8_native_crosscheck.json, with original log/fchk paths. ACN 3/4/5 are −2.669734/−2.606143/−2.424953 eV; 1 differs from 3 by +0.005490 eV despite +0.163 V Epc. Compound2 SI-A and ring-B-rotated B both depart from this neutral-LUMO relationship; this is not an exact author E1/E2 assignment. Compound3 DCM→ACN/DMSO stabilization: 0.029032/0.031293 eV. The local absolute offset is preserved, not fitted away.

All intermediate orbitals, geometries, frequencies and optional spin cubes are evidence, not scored workflow stages. No absolute redox cycle, whole electrochemical mechanism, exhaustive conformer ensemble or unique causal hydroxyl attribution is established by the present evidence. Historical E/Z failures remain historical; none is converted to PASS.

The hydroxy applicability rule evaluates the submitted model, including a genuinely supported common relationship. The reference LUMO failure is descriptor-specific. Independent native calculations, consistent physical definitions and an appropriate relation to Epc are required; fitting the supplied potentials is insufficient. Compound 5 contains 4-aminophenyl and 6-methoxynaphthalen-2-yl groups, not two para-substituted phenyl groups. Its source orbital comparison does not isolate donation from extended conjugation.

</details>
