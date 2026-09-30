# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New quantum-chemical calculations performed in this development turn: **0**. Graph/count checks and schema fixtures are not scientific reference validation.

## Source material inspected

Main pp2-3 Scheme1 thermochemistry and contact discussion; SI pp6-7 geometry and pp11-18 Gibbs calculation details/coordinates.

- `papers/paper_86a0b654270a8ce7/documents/main.pdf` SHA-256 `b19110f192c994ade2406a46c6cc62346d465b27568db22c2b86df46f3af5879`
- `papers/paper_86a0b654270a8ce7/documents/supplementary_001.pdf` SHA-256 `59edd5baf1ea3027779a0ba8fef20348da233372dfdccdaf0ea2fa1f3f5886fb`

## Scientific definitions and original route

Both complete IrC60H63N4O2 isomers are neutral singlets, in THF at 339 K. Preserve Ir coordination identity; report E, solvent contribution, ZPE/thermal and low-frequency correction separately with one standard state. The source predicts a preference, but a contrary converged method is not discarded. Contact-separation restraints measure interaction plus deformation and must not be called pure pi-stacking energies.

The authors use Gaussian16 B3LYP/def2SVP SMD(THF), 339 K and propose isomer2 stabilization from intramolecular stacking. Their isolated yield ratio was compared to a Boltzmann ratio, but without demonstrated interconversion that is not an equilibrium validation. The new ensemble, contact-intervention and method controls test rather than assume the source interpretation.

## Reusable legacy evidence

`legacy_final_snapshot/` contains byte-exact original tasks, public input and evaluator snapshots with source hashes. Only like-defined original object checks, measured input data and documented baseline methods may be reused. Historic PASS and old tolerances do not establish expanded coverage. Consult the source-guide record in `task_provenance/upgrade_audit.json` for baseline discrepancies.

## Minimum pilot

Resolve the old reversed ranking with exact isomer labels and E/G decomposition. Pilot a released conformer of each plus a fixed-contact intervention; preserve negative method results.

## Minimum complete reference

- isomer_ensembles: isomer1, isomer2. Use low-energy conformer coverage and frequency evidence with identical 339 K convention; reconstruct ensemble G and document degeneracy.
- stacking_intervention: isomer1_contact, isomer2_contact. Submit mapped aromatic ring atoms and frozen/released contacts, controlling other geometry. Distortion cannot be removed by merely labeling the difference stacking.
- ranking_robustness: method_change, thermal_model_change. Quantify sign and interval under actual methods and thermal treatment; unresolved ranking after complete data is acceptable. Isolated yields are not a scored equilibrium ratio.

## Available software and resource boundary

Gaussian/ORCA＋GoodVibes. Capability is based on chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. Gaussian/ORCA native input is allowed where a specialized Action is absent; CREST/xTB is a preparation aid, not a replacement DFT endpoint. Check exact functional, dispersion, ECP/solvent and analysis conventions. No new software installation, paid service, long scientific job or HPC was launched. Pilot costs and complete expanded reference costs remain unmeasured.

## Reference gap and release gate

All expanded matrix energies/properties, validated stationary states/paths, alternate-method or conformer uncertainty and independent agent trial remain to be calculated. Numerical acceptance intervals must be frozen from actual matched references, convergence, conformer/model variability and experimental extraction error. Absolute and relative observables need separate calibration. Do not inherit a narrow legacy +/- range or set a new range to make failing objects pass. Before release run complete positive, refutation/indistinguishability, old-only, missing-core, wrong-object/spin/zero and false-completion replays using genuine artifacts. Current batch tests only exercise package, schema and export boundaries.

## Optional boundary

Complete interconversion networks and exact isolated yields are optional.
