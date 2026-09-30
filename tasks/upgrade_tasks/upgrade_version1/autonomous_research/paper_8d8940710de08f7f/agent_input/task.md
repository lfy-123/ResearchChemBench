# Scientific objective

Determine whether dispersion, the aromatic C–H···O contact, or entropy/solvation explains the V(+), V(−), and Z conformational balance of SNaft and SAntr, using independent basin searches and paired fixed/relaxed interventions.

# Public inputs and scientific boundaries

Read `data/inputs/research_matrix.json` and its listed companion data. The mapped graphs, explicit control definitions and observations define the authorized objects in both task modes. Neutral singlet molecules only. Initialize CSNC torsions in V(+) 20–80°, V(−) −80 to −20°, and Z |torsion| 140–180°; these labels are starting basins, not guaranteed distinct minima. Compare free energies only within the same molecule/environment and electronic protocol. C–H···O, not an assumed N–H···O contact, is the source interaction at issue. All required comparisons are core; the optional extension listed below is not a completion condition. A documented failure is a valid submission but is not scientific completion. Evidence-supported collapse of an initialized basin, or inability to distinguish explanations after completing the core matrix, is scientifically admissible. An unattempted core comparison cannot be replaced by an uncertainty statement.

This is a development task with an expanded scientific contract; no supplied coordinate is a validated expanded reference.

# Required scientific validation/investigation

1. **Environment- and dispersion-resolved basin coverage.** Attempt all three initial basins for both molecules in vacuum and methanol with dispersion on/off. Validate each retained minimum, deduplicate merged endpoints, and report E/G/weights on one convention. A documented collapse is admissible and must not create duplicated statistical weight.

2. **Electronic dispersion and contact counterfactuals.** Supply matched D3 on/off single points and separately relaxed contrasts. Define the mapped PAH C-H donor and S=O acceptor; document the restrained contact-disfavoring control and its strain/nonadditivity. Do not assign constrained points equilibrium G or isolate a hydrogen-bond energy by assumption.

3. **Electronic versus entropy/solvent attribution.** Reconstruct ΔG from ΔE and thermal terms; test low-frequency treatment and methanol effects. Check whether nominal mirror-like V basins are numerically or entropically distinct at the resolution achieved. Reward a supported near-degeneracy rather than a forced ordering.

Validate identity and convergence before interpreting results. Report at least two falsifiable competing explanations and an explicit numerical sensitivity comparison. Retain native inputs, full outputs, mapped final geometries and executable analysis with all intermediate tables. Report what would overturn your interpretation. Do not equate a constrained point, an SCF energy or a process return code with a local minimum.

Optional, not required: Different protonation states, charges and antifungal pharmacology must not be mixed into the same ensemble.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. See `submission_guide.md` for units, coverage and raw-evidence requirements. A bounded failure or blocked submission must identify attempted work, missing endpoints, raw diagnostics and a concrete recovery condition.
