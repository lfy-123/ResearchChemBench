# Expanded reference validation plan

Status: **reviewed finite inputs; numerical calibration pending**. The original development turn performed no quantum calculations; subsequent raw verification attempts are tracked privately by Group 3. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main p2 Fig1 and pp3-4 interactions; SI pp3,5 molecular characterization and FigS3; no atom-resolved PM6/BTP-eC9 fragment coordinate/cap list was found in these materials.

- `papers/paper_a0f6b899582cb9f7/documents/main.pdf` SHA-256 `536dd808e61410cb46b94a17eccf128122c410866a2933ca90121a7d20de81f0`
- `papers/paper_a0f6b899582cb9f7/documents/supplementary_001.pdf` SHA-256 `706d864d2d7eedd3257f86c9d9a4510612c0d6cc5fcdf10b3198f784fbd006ae`

## Scientific definitions and original route

M3 is neutral singlet 2,5-di(thiophen-2-yl)pyrazine C12H8N2S2. Use the independently reviewed builder-defined finite graphs PM6_BDD_T2_Me (C20H12O2S4), BTP_eC9_core_Me (C22H14N4S5), and BTP_eC9_full_pi_Me (C48H18F4N8O2S5), all neutral singlets. Their atom-indexed bonds and exact cut/cap boundaries are supplied in objects.json and fragment_models/. BTP core atoms 1–31 map identically into the larger model; added/removed caps and hydrogens must be explicitly mapped in paired comparisons. These are bounded source-grounded models, not recovered author coordinates or complete PM6/BTP-eC9 materials. No arbitrary fragment replacement is authorized.

The authors propose a planar N...S-locked quadrupolar additive with affinity for donor BDD and acceptor BTP-eC9 regions. Main Fig1 shows pair models; source M3 DFT is B3LYP/6-31G. Pair energy decomposition and matched truncation controls are new. The printed quadrupole unit D is not a canonical quadrupole unit; use a declared origin and e angstrom squared or properly converted atomic units.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Use the reviewed capped graphs and enlarged counterpart, then verify the paired contact and decomposition calculations. An alternative decomposition requires a stated, calibrated definition, not renaming unlike components.

## Minimum complete reference

- contact_models: PM6_face, PM6_edge, BTP_core_face, BTP_core_edge. Each pair requires complete graph, contact map and several starting orientations at fixed composition; compare released versus frozen fragments.
- decomposition: PM6_pair, BTP_pair. Use a single justified decomposition and identical fragmentation; terms are model-dependent, not unique causal observables. Recompute total and residual terms.
- truncation_and_tensor: larger_fragment, M3_tensor. At least one actual larger-fragment pair is core. Report all six independent tensor components with origin/axes; Qzz alone cannot prove dual binding or PCE.

## Available software and resource boundary

Gaussian/ORCA＋Psi4 SAPT或明确片段分解. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Remaining scientific gate

The finite fragment graph definitions and cap rules are now materialized after independent source review. Actual contact, decomposition, truncation and tensor validation remains mandatory; topology review alone is not scientific completion.

## Optional boundary

Bulk blend morphology and device simulations are optional.

Metric applicability clarification: For the isolated M3_tensor row, primary_interaction_kJ_mol and control_interaction_kJ_mol are null with metric_applicability_reason because no partner is present. The full quadrupole tensor, declared origin/axes and numeric quadrupole_zz_eA2 remain mandatory. The larger_fragment row still requires both real interaction energies, a mapped larger-fragment pair and the shared M3 tensor; null cannot waive that truncation comparison. The reviewed finite fragment identities remain mandatory; the truncation-pair calculation cannot be waived.
