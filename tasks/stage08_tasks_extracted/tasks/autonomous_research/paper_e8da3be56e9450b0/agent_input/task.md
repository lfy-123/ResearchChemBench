# Scientific objective

Determine, by an independently planned periodic electronic-structure calculation, the relaxed spontaneous polarization of the neutral Zn/Co co-substituted BaTiO3 model supplied here, and test whether this co-substitution enhances ferroelectric polarization relative to the supplied undoped control. Report polarization in μC/cm² with its sign/branch convention, the relaxed structure, and the comparison.

# Public inputs and scientific boundaries

Use `data/inputs/structure_spec.json` as the authoritative identity, charge, multiplicity, periodic cell and substitution definition, `bzct_start.xyz` as the explicit 40-atom starting geometry, and `bto_reference.xyz` as the parent 5-atom basis to repeat 2×2×2 for the control. The BZCT formula is Ba7ZnTi7CoO24: one Zn replaces the Ba site in translated cell (0,0,0), and one Co replaces the Ti site in that same translated cell; no oxygen vacancies are allowed. The initial cell is 7.98×7.98×8.02 Å, orthogonal, and the supplied fractional basis defines the connectivity. The measured endpoint is the Berry-phase spontaneous polarization of the relaxed BZCT relative to a stated nonpolar/reference branch, plus the same quantity for the relaxed undoped control. Methods and software are your choice, but disclose them.

# Required scientific validation/investigation

Plan and execute a relaxation and polarization calculation for both named systems. Verify atom counts, composition, charge, periodic cell, substitution sites, and that the relaxed calculation reaches a documented stopping criterion. Establish a polarization branch/reference path and report how branch discontinuities were handled. Perform at least one numerical sensitivity check (for example k-point, cutoff, functional, supercell/reference-path discretization, or tighter relaxation), identify which observable it tests, and report the resulting change. A calculation is complete when both systems have a converged relaxed state, a reproducible polarization estimate, a branch convention, and a sensitivity result; if a required calculation cannot be completed, stop after documenting the attempted route, exact failure, partial outputs, and the scientifically justified limitation. Stop further exploration once these requirements are met or once additional checks no longer change the reported conclusion within the agent's stated uncertainty.

# Submission and outcome branches

Submit `report/results.json` using the schema. Set `outcome.kind` to `complete` only when both systems have the required relaxed-structure artifact, convergence evidence, branch-resolved polarization and sensitivity result. If either calculation cannot be completed, set `outcome.kind` to `bounded_failure`, include an exact `failure_report`, and report only measurements and artifacts actually obtained: unavailable polarization, comparison, or relaxed structure may be `null`; do not invent placeholders. In either branch, include two explicitly identified system records (`bzct_2x2x2_neutral` and `bto_2x2x2_control`) and state the coverage and limitation in `conclusion`.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus the referenced calculation logs/structures. Include object-specific validation evidence for BZCT and BTO, polarization values and units, uncertainty or sensitivity, the comparison, and a final conclusion. State the chosen route and branch convention. Do not report an invented discovery narrative.
