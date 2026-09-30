# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main pp8-10 Figs6-7; SI pp5-6 methods, pp144-149 coordinates, pp167-169 Lewis adduct discussion.

- `papers/paper_9f4c259696ad2f87/documents/main.pdf` SHA-256 `592534cc448b295773af43b0783196ac34170f0e847fb7412d873e8a6e98c2ba`
- `papers/paper_9f4c259696ad2f87/documents/supplementary_001.pdf` SHA-256 `f3436ca99f362b00e082f3bc28926ef30d56c7f4cfffaf92faa92708a24569ad`

## Scientific definitions and original route

Use PXX1 C43H28O3 and PXX2 C50H30O4, neutral singlets; acid is neutral B(C6F5)3. Each PXX has 0, 1 and 2 acid units; PXX1 has one carbonyl, so its second acid explores the available ether/carbonyl-site competition as a new candidate, not an asserted second independent ketone. PXX2 has two carbonyls. All whole complexes are neutral singlets. CH2Cl2 is the shared primary medium. Compare sequential acid association reactions, never bare total energies of different acid counts. Use 298.15 K and 1 M as explicit development thermochemistry conventions; no equilibrium population is inferred without concentration evidence.

The authors propose enhanced carbonyl acceptor strength and PXX-to-ketone/acid charge transfer. Gaussian 16 B3LYP/6-31G(d) PCM(CH2Cl2) is described in SI methods; the main Fig7 caption states 6-311G(d), which must be disclosed as a source discrepancy. SI p167 reports a single titration equivalence point for two-ketone compound 2 and explicitly leaves one/two site occupancy ambiguous. The full 0/1/2 matrix and frozen acid-removal controls below extend the source.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Pilot the largest two-acid model, verify carbonyl versus ether atom map and state tracking, then calibrate sequential association and fixed-geometry acid removal. Do not assume all large adducts are stable minima.

## Minimum complete reference

- stoichiometric_series: PXX1_acid0, PXX1_acid1, PXX1_acid2, PXX2_acid0, PXX2_acid1, PXX2_acid2. Require actual conformer/site attempts, stoichiometric identities and matched transition densities for every acid count; evidenced dissociation/collapse is reportable.
- balanced_binding: PXX1_step1, PXX1_step2, PXX2_step1, PXX2_step2. Recompute PXX.acid_n minus PXX.acid_(n-1) minus free acid with common thermochemistry and 1 M correction. Demonstrate composition balance and conformer effects.
- geometry_and_spectrum: PXX1_acid_removed, PXX2_acid_removed, titration_discrimination. Remove acid at the same PXX geometry and compare independently relaxed PXX; compare observed trend without forcing unique occupancy from similar spectra. Preserve digitization/concentration limits.

## Available software and resource boundary

Gaussian/ORCA TD＋Multiwfn＋CREST. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

FRET, full concentration dynamics and absolute emission efficiency are outside the core.
