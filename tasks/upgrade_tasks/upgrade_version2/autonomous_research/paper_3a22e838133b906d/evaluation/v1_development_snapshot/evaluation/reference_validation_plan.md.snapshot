# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main pp1-3 Scheme1/Fig1, including Li2O2 paragraph p2; SI pp62,69 crystal data and p78 computation; old public model graphs are retained only as labeled truncation controls.

- `papers/paper_3a22e838133b906d/documents/main.pdf` SHA-256 `0b3a6429a4f8d324616b78c736daedf397971e63fdeff848f1b28058a39a1238`
- `papers/paper_3a22e838133b906d/documents/supplementary_001.pdf` SHA-256 `0179f85740483c73a9996ca3c5ef36fd4f0044eca862b18eadc90e03463a7235`

## Scientific definitions and original route

Use full source BCy2/o-phenyl phosphonate 2a and deethylated anion3, not only BMe2/OMe surrogate. Full anion is C20H31BO3P, charge-1 singlet; Li+ and MeCN are singlets. Source Li2O2 dimer has two anions, two Li and four MeCN (charge0 singlet). Each Li coordinates the exposed phosphoryl O of both anions and two MeCN N atoms; intramolecular O->B contact remains distinguishable. Use balanced 2 monomer -> dimer and MeCN association cycles. Dealkylation reaction is neutral+LiI -> Li.anion+EtI; do not subtract unlike neutral/anion total energies.

Main Fig1 shows an inversion-related Li2O2-bridged dimer with two MeCN ligands on each Li. Authors use Gaussian16 B3LYP-D3(BJ)/6-311++G(2d,p) on small neutral/anion models and explicitly acknowledge omitted Li coordination. Full molecular, solvent-coordination and dimer contrasts are new and require direct calculation; small-model agreement cannot certify the aggregate.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Validate full anion and neutral Li(MeCN)2 monomer, then pilot the minimum 2-anion/2-Li/4-MeCN dimer and its dissociation counterpart. Atom inventory/coordination follows Fig1; no fabricated crystal coordinates are supplied.

## Minimum complete reference

- coordination_layers: full_anion, Li_anion, Li_anion_2MeCN, crystal_supported_dimer. Maintain full Cy and OEt groups and distinguish dimer versus monomer identities; every geometry needs genuine convergence and frequency/constraint evidence.
- balanced_cycles: Li_association, MeCN_association, dimerization, deethylation. Recompute fragment/stoichiometry-balanced differences; explicit LiI/EtI or equivalent balanced deethylation accounting is required, never bare neutral-minus-anion energy.
- truncation_and_mechanism: small_vs_full, coordination_vs_aggregation. A full dimer is required for aggregation credit and paired small/full models for truncation. Local isolated-anion results do not explain the whole salt; no electrolyte performance claims.

## Available software and resource boundary

Gaussian/ORCA＋有限簇/构象工具. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

A smaller local-only version would need separate scope deletion of aggregation; the present first version retains a mandatory full dimer.
