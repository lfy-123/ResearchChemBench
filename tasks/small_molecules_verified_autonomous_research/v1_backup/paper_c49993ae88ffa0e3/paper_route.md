# Private author reference: bounded deoxygenation half-reaction

Current scope: author_deoxygenation_half_reaction_20261012. The public task uses experimentally preformed H2PQ and leaves electronic states, mechanisms and methods to the agent. This file is private reference material, not a public workflow. The approved scope excludes alcohol-driven preparation/regeneration and the complete catalytic cycle.

The author model uses parent H2PQ and pyridine N-oxide in acetonitrile. R=S1-H2PQ+PyO; I=ground-state HPQ radical+PyOH radical; F=ground-state PQ+PyOH2. PyOH2 denotes a Py-water aggregate, not a covalent N-O product or free Py and water summed separately. The second PT endpoint is PQ radical anion+PyOH2 radical cation; the second ET endpoint is HPQ cation+PyOH anion. The latter retains the author's dissociated N-O geometry. Precise labels, formulas, charges, multiplicities and all 66 XYZ memberships are in `evaluation/validation_plan.json`.

| Result (kcal/mol) | Dry | Two added waters | Reference/source |
|---|---|---|---|
| First PT / ET | -0.9 / -1.6 | -2.2 / -8.2 | R; Fig.2B, SI p.40 |
| Second PT / ET | +2.3 / +7.4 | -1.3 / -9.6 | I; Fig.2C, SI pp.40-41 |
| Complete first-transfer I | -43.9 | -41.7 | Cumulative from R; Fig.2A, SI p.40 |
| Final product F | -115.1 | -112.1 | Cumulative from R; Fig.2A, SI pp.40-41 |

All PDF page numbers are physical pages. The hydrated calculation attaches one solvent water to each fragment, conserving two added waters; the final PyOH2 also contains one generated water. The dry reaction inventory is C19H15NO3; the hydrated inventory is C19H19NO5. Do not enforce equal water-molecule counts before and after chemical formation, or add the final cumulative energy to the first-transfer energy. The derived second complete-transfer differences -71.2/-70.4 are unscored arithmetic checks.

SI pp.38-39: Gaussian M06-2X/6-31+G(d,p) optimizations/frequencies; M06-2X/def2-TZVPP same-geometry single points; SMD acetonitrile throughout. Use the source lowest-singlet TD total energies for S1 species and appropriate ground-state doublets/singlets elsewhere. Author postprocessing uses GoodVibes 3.0.2, 298.15 K, 1 M, scale 1.0, Grimme entropy interpolation at 100 cm^-1, symmetry and conformer corrections. The existing independently validated first-event replay used GoodVibes 4.3; retain its valid data and audit compatibility rather than discarding it solely for a version difference.

Maintain physical continuity and state identity, validated minima and matching single-point geometries, traceable ensemble membership and correct symmetry/deduplication. The author XYZ contains 29 records already used in the first-event reference and 37 further records covering the later families. Only missing required independent conformers need reproduction. No fixed search count is imposed on the evaluated agent.

First-event reference values -0.922739/-1.844559/-2.197728/-8.029374 are reusable. They do not validate the new second-stage/product scope. Existing dry +/-1.0 and hydrated ET +/-1.5 comparisons remain; hydrated PT uses its existing source-protocol publication-rounding/expert-review boundary. New numerical targets have explicit expert comparability review, no invented universal tolerance and no shifted source values. Scientific weights are 20 first-event dry, 20 first-event hydrated, 30 second-stage competition and 30 cumulative endpoints; final interpretation adds no points.

Experimental context: SI p.36 and main Fig.1E concern preformed H2PQ/H2PQ-CF3 with substituted 1b/1d in CD3CN. SI p.13 Table S2 instead uses PQ/alcohol A/1a at 30 C for 4 h. Those yields are not rates or parent-PyO observations. SI p.37 CF3 ON/OFF controls are not reattributed to the parent model.

The isolated-state analysis in SI pp.41-42 is supporting identity evidence. The 353.91 nm value at an optimized S1 geometry is not an established 450 nm absorption match. Fig.2B's aggregate orbital gap and Fig.S22's S1/S2 optimization histories lack corresponding aggregate/root definitions in the 66-record XYZ; they are absent from active scoring. Fig.S22 is not a barrier scan or TS/IRC. Fig.S23 is a proposed full cycle, not computational support for every arrow. No new preparation, regeneration, N-O-cleavage TS, PCET/HAT barrier, rate, quantum-yield, bulk-water optimum or descriptor calculation is required.

The task design is implemented; extended scientific verification and release remain pending. See `evaluation/qualification.json` and `evaluation/verified_computation_reference.md`.
