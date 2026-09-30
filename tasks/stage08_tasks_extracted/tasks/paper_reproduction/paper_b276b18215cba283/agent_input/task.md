# Scientific objective

Determine computationally whether the two supplied conformations of a simplified merocyanine chromophore exhibit a meaningful difference in their lowest singlet vertical excitation. Independently calculate the neutral-singlet S0→S1 excitation for the transoid and cisoid structures and the signed cisoid-minus-transoid difference in eV, then state what physical interpretation is and is not supported by this model.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that twisting the simplified merocyanine arm between transoid and cisoid conformations can lower the lowest singlet excitation, as a possible contributor to a red-shifted optical feature. This is a qualitative proposal for the conformer comparison in the stated model.

**Candidate route or mechanism.**
The candidate comparison is a conformational change from transoid to cisoid, with the cisoid structure proposed to have a lower-energy low-lying singlet excitation. The reported dominant excitation character is associated with the frontier-orbital transition, which can guide state-character analysis while remaining subject to independent verification.

**Discriminating evidence.**
Compare independently computed S0→S1 vertical excitation energies for the two supplied structures, together with oscillator strengths, dominant orbital contributions, state ordering and tracking, convergence evidence, and the signed energy difference. Assess whether the difference is resolved at the achieved uncertainty and whether the model supports the proposed interpretation.

# Public inputs and scientific boundaries

Use `data/inputs/transoid.xyz` and `data/inputs/cisoid.xyz`. Each is a 57-atom Cartesian structure for the same simplified single-arm chromophore, with neutral charge and singlet multiplicity as stated in the XYZ comment. The structures are S0 geometries. The isolated gas-phase molecule is the complete physical boundary; the measured quantities are converged S0→S1 vertical excitation energies, oscillator strengths, dominant orbital contributions, and their signed difference. Do not claim solution, membrane, kinetics, or experimental spectral behavior from this model alone.

# Required scientific validation/investigation

For each named structure, verify atom count, element sequence, charge and multiplicity; independently choose and justify the electronic-structure and excited-state treatment; document convergence criteria; and establish that the reported root is the lowest singlet excited state rather than relying only on root number. Use the supplied S0 geometry directly for the requested vertical excitation. If you additionally optimize a geometry as a sensitivity check, keep the vertical result at the supplied geometry identifiable and report optimization convergence and any frequency/stationarity check separately. Assign dominant orbital character and provide auditable state-tracking evidence. Compute `cisoid_S1 - transoid_S1` in eV with an explicit sign convention. Formulate at least two physically plausible interpretations of any computed difference, including the possibility that it is not meaningful at the achieved uncertainty, and compare them only to the extent the calculations discriminate them. The investigation is complete when both structures have auditable converged results. If either calculation cannot be completed, submit the bounded-failure outcome after both named structures have been attempted, identifying every failed object, any usable partial result, diagnostics, and the limit reached. Stop after both structures have been attempted and coverage, uncertainty, limitations, and method sensitivity are documented; do not search additional structures.

# Deliverables

Submit `report/results.json` following `submission_schema.json`. A successful submission includes provenance, explicit validation for each named structure, energies, oscillator strengths, orbital assignments, the signed shift, the compared interpretations, and an evidence-based, scope-limited conclusion. The bounded-failure branch does not require fabricated energies or a shift, but it does require both attempted objects, per-object status, every available partial result, concrete diagnostics, and a scope-limited statement of what remains unresolved.
