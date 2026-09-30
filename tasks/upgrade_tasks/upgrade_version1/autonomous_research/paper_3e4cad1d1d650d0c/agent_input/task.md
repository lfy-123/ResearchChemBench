# Scientific objective

Test whether frontier-orbital ranking explains the excited-state reducing ability of 1a and 1e in DMSO by calculating their oxidation free-energy difference, combining it with measured E00, and challenging electron-transfer thermodynamics with 4-chloroanisole and an independent quenching observation.

# Public inputs and scientific boundaries

Read `data/inputs/research_matrix.json` and its listed companion data. The mapped graphs, explicit control definitions and observations define the authorized objects in both task modes. Use isolated ions without counterions, q=-1 singlet donors and q=0 doublet oxidized radicals. All redox potentials are volts versus SCE, n=1. E00 is an absorption/emission crossing energy, not a HOMO-LUMO gap. A favorable driving force is not a prediction of cleavage kinetics or product yield. All required comparisons are core; the optional extension listed below is not a completion condition. A documented failure is a valid submission but is not scientific completion. Evidence-supported collapse of an initialized basin, or inability to distinguish explanations after completing the core matrix, is scientifically admissible. An unattempted core comparison cannot be replaced by an uncertainty statement.

This is a development task with an expanded scientific contract; no supplied coordinate is a validated expanded reference.

# Required scientific validation/investigation

1. **Matched anion/radical free-energy cycle.** Calculate and minimum-validate all four donor/radical states in DMSO; record electronic/thermal terms, radical spin contamination and a common solution standard state. Recompute the anchored relative cycle and compare its ordering with HOMO ordering. Never use gas ΔSCF directly as a solution potential.

2. **E00 and real-acceptor driving force.** Use the measured crossings and one-electron convention to compute Eox* and ΔGET for both donors with the same acceptor and SCE zero. Distinguish electrochemical uncertainty, dissociative reduction and equilibrium free energies.

3. **Independent mechanistic challenge.** Freeze the redox cycle before evaluating the intensity/lifetime challenge. Use the supplied original Figure3 crop to test dynamic and static/association explanations. A numerical lifetime-change upper bound must explicitly be a plot-resolution estimate, with axis/marker calibration and analysis evidence; it is not an instrument uncertainty. If a quantitative bound cannot be justified, submit lifetime_evidence_kind=qualitative_only and lifetime_change_fraction=null with the supported qualitative challenge and its resolution limit. Raw individual lifetime measurements and errors are unavailable and must not be invented. Favorable ΔGET does not settle the quenching mechanism or yield.

Validate identity and convergence before interpreting results. Report at least two falsifiable competing explanations and an explicit numerical sensitivity comparison. Retain native inputs, full outputs, mapped final geometries and executable analysis with all intermediate tables. Report what would overturn your interpretation. Do not equate a constrained point, an SCF energy or a process return code with a local minimum.

Optional, not required: Complete C–Cl dissociation, substrate yields and the full catalytic cycle are outside this version.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. See `submission_guide.md` for units, coverage and raw-evidence requirements. A bounded failure or blocked submission must identify attempted work, missing endpoints, raw diagnostics and a concrete recovery condition.
