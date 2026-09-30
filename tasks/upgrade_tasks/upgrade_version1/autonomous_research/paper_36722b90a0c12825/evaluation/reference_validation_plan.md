# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main PDF pp3-4 Figs3-5; coordinate SI1 pp2-8; SI2 pp6-7,15-16, Table S2 and DFT section.

- `papers/paper_36722b90a0c12825/documents/main.pdf` SHA-256 `ba5c030e4e408007aba517f664a257a4703fb5119f70452d93f1120cac8a0ee1`
- `papers/paper_36722b90a0c12825/documents/supplementary_001.pdf` SHA-256 `ddb684896fb0ac2f2a1eee1c681fb4ec4071a27834966f9f53342e1bf6603069`
- `papers/paper_36722b90a0c12825/documents/supplementary_002.pdf` SHA-256 `7357d277c10ad1081614f77286650c562c4ca7bc841ffd273c8d27cc232f95be`

## Scientific definitions and original route

Use the complete C48H26F12N14 host: E and Z each free (charge 0, singlet) and with one chloride (charge -1, singlet), plus Cl- (singlet). Ac means acetone, not acetonitrile. Primary solution boundary: acetone, 298.15 K, 1 M standard state; convert any 1 atm RRHO terms explicitly. Sum over distinct validated conformers within each E/Z family, not between photostationary E and Z populations. TBA+ is a counterion context; an explicit TBACl sensitivity must use balanced composition. A second host is a separately chosen optional transfer check.

The authors associate triazole preorganization and cavity accessibility with light-switchable chloride binding. They use Gaussian 16 B3LYP/6-31G*, D3(BJ), PCM acetone/UFF cavity, harmonic corrections at 298.15 K and counterpoise treatment of binding. Their (1,3)Ph titration constants overlap in uncertainty; the strong-switch claim must not be imposed on this host. The complete E/Z ensemble cycle and geometry/environment interventions below are benchmark extensions, not a claim that the source validated them.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Audit E/Z N=N stereochemistry, all 100 host atoms and chloride charge; independently reproduce one free/bound pair, then a host distortion term. Old G(open)-G(close) and electronic E(open)-E(close) are different observables and neither is a binding switch.

## Minimum complete reference

- species_ensembles: E_free, E_bound, Z_free, Z_bound, chloride. Validate minima and conformer coverage for all four chemical states; isolate electronic, ZPE, thermal and concentration corrections. Include conformer weights and all attempted structures in raw tables.
- binding_cycle: E_bind, Z_bind, Z_minus_E. Recompute G(host.Cl)-G(host)-G(Cl) for each family and DeltaDeltaG=DeltaGbind(Z)-DeltaGbind(E). Report interaction and distortion with compatible fragment geometry and BSSE conventions.
- intervention: frozen_host, solvent_or_ion_pair. At least one frozen/relaxed host contrast and one actual solvent/counterion sensitivity must challenge the interpretation. Do not use PSS as Boltzmann population.

## Available software and resource boundary

Gaussian/ORCA＋CREST＋GoodVibes. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

Complete titration fitting, exact PSS composition and device switching efficiency are optional and unscored.
