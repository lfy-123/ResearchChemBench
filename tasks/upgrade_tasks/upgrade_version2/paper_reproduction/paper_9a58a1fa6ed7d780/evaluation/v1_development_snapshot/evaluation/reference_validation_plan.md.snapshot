# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main pp2-4 Figs2-3; SI p3 methods, Tables S11/S14 and pp49-51 Tables S21-S22.

- `papers/paper_9a58a1fa6ed7d780/documents/main.pdf` SHA-256 `aeebf1cd58e33932312c18720a87e7fddd1c12d72f39a5afb963baaa5ce4ca92`
- `papers/paper_9a58a1fa6ed7d780/documents/supplementary_001.pdf` SHA-256 `dcd192b5e3b92b087855114bacea08f5316e4de2d8a105fa4af949b8459531fe`

## Scientific definitions and original route

BN-AkFlu 5a is C22H14B2N2 (40 atoms in the supplied actual graph), not the H15 typo in an old route. CC-AkFlu 5b is C26H14, 40 atoms, from SI Table S22. Both are neutral singlets in gas phase. Use each relaxed geometry and cross-evaluate on a common mapped heavy-atom scaffold; replacing B/N by C is a chemical intervention with changed nuclear charges. Track physical states via NTO/density overlap, not root numbers alone; retain six vertical roots and descriptors for the first four source baseline roots.

The authors use Gaussian 16 B3LYP/6-311G(d,p) and Multiwfn to associate internal BN doping with changed frontier levels, weak low-energy absorption and higher bright states. SI Tables S11/S14/S21/S22 provide descriptors, transitions and geometries. Frozen cross-scaffold comparisons and analysis convergence controls are new benchmark tests. Existing S1-S4 Sr fields were present; old S1 energy/S4 overlap disagreement is a calibration issue.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Recheck BN stoichiometry, S1 energy, S4 Sr, root mapping and full TD amplitudes; compare normalized hole/electron grids before expanding the all-carbon control.

## Minimum complete reference

- relaxed_states: BN_relaxed, CC_relaxed. Preserve full S1-S6 table and S1-S4 density-analysis raw data. Sr is integral sqrt(rho_h*rho_e) over space for normalized densities; D is centroid separation.
- common_scaffold: BN_on_CC, CC_on_BN. Map the common framework and show both cross geometries. Frozen points are not optimized minima. Use NTO/transition-density mapping to avoid claiming a root switch as a direct chemical shift.
- attribution: chemical_effect, geometry_effect, analysis_convergence. Recalculate paired changes and analysis-grid/amplitude sensitivity independently of excitation-energy convergence. Accept a mixed or unresolved BN effect if all controls are computed.

## Available software and resource boundary

Gaussian/ORCA TDDFT＋Multiwfn. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

New-molecule screening, quantum yield, charge mobility and bulk packing claims are excluded.

## Phase1 completion 2026-09-28T07:41:48.616630+00:00

The development-only zero-calculation statement above is historical. The finite seven-row matrix is now completed with the actual references and bounded conclusion documented in verified_computation_reference.md and scientific_reference/. Source S11 disagreement, six-state-window ambiguity and functional uncertainty remain explicit. No blind-agent trial or universal numeric interval is asserted.
