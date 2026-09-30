# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main PDF pp3-8 computational details, Fig3 energy distribution and reaction PES; SI p2 Table S1 and pp3-15 CBS-QB3 coordinates/energies.

- `papers/paper_9455a82229de2427/documents/main.pdf` SHA-256 `cb6a4cf501837f252e2ceced551eefe8bcab8ca315fc4577e9daeb0d334476a1`
- `papers/paper_9455a82229de2427/documents/supplementary_001.pdf` SHA-256 `27409af9dd2e70aae498d28aec9956049b2fc88bfcd5fa7439d57583ab67edbb`

## Scientific definitions and original route

Reactants SiN (0, doublet) and isoprene C5H8 (0, singlet) produce SiNC5H7 (0, singlet) plus H (0, doublet). Doublet SiNC5H8 addition/rearrangement structures share the reactant atom map. Use separated reactants as zero for E0=Eelectronic+ZPE at 0 K. Collision energy 25±1 kJ/mol and experimental channel exoergicity -162±27 kJ/mol are observations, not computed answers. Enumerate terminal-C1/C4 attack by Si and N, then at least ring closure and H-loss alternatives. Declare explored bond edits and remaining search limits.

The source uses Gaussian 16 CBS-QB3 and a finite reaction PES; terminal addition, rearrangement, ring closure and H elimination motivate cyclic products. Published channels include two methylazasilacyclohexadienylidenes. They are hypotheses for PR, not compulsory winners. The benchmark additionally requires a main and an energetically competitive connected route with equal zero and explicit spin bookkeeping; full scattering/RRKM is not assumed.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Validate one atom-conserving doublet route and H-loss asymptote with endpoints before freezing any barrier threshold. A TS requires mode and bidirectional connection, and a barrierless route requires a continuous converged path.

## Minimum complete reference

- candidate_space: terminal_C1_Si, terminal_C4_Si, terminal_C1_N, terminal_C4_N. Provide mapped graph-edit enumeration, attempted structures, state validity and products for the four attack families. Multiple seeds collapsing to one product are legitimate only with raw mapped evidence; no requirement for four distinct products.
- connected_routes: main_route, competitor_route. Submit ordered mapped nodes/edges, optimized endpoints, TS and IRC files or continuous no-barrier path evidence. Recompute all nodes relative to SiN+isoprene, including the free H atom.
- accessibility: thermodynamic_vs_kinetic, method_sensitivity. Separate lowest-energy product, channel exoergicity and accessible barrier. Compare collision margins and demonstrate method/ZPE sensitivity; no 298 K equilibrium abundance or branching ratio inference.

## Available software and resource boundary

Gaussian复合方法或ORCA＋pysisyphus/IRC. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

Full scattering, exact branching ratios and a complete RRKM network are optional.
