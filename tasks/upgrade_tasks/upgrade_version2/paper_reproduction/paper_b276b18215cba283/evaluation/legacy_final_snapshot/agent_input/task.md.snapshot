# Scientific objective

Test the authors' qualitative proposal that twisting the simplified merocyanine arm between transoid and cisoid conformations can lower the lowest singlet excitation and thereby help explain a red-shifted optical feature. Independently calculate the neutral-singlet S0→S1 vertical excitation for both supplied structures and the signed cisoid-minus-transoid difference in eV.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that twisting the simplified merocyanine arm between transoid and cisoid conformations can lower the lowest singlet excitation, as a possible contributor to a red-shifted optical feature. This is a qualitative proposal for the conformer comparison in the stated model.

**Candidate route or mechanism.**
The candidate comparison is a conformational change from transoid to cisoid, with the cisoid structure proposed to have a lower-energy low-lying singlet excitation. The reported dominant excitation character is associated with the frontier-orbital transition, which can guide state-character analysis while remaining subject to independent verification.

**Discriminating evidence.**
Compare independently computed S0→S1 vertical excitation energies for the two supplied structures, together with oscillator strengths, dominant orbital contributions, state ordering and tracking, convergence evidence, and the signed energy difference. Assess whether the difference is resolved at the achieved uncertainty and whether the model supports the proposed interpretation.

# Public inputs and scientific boundaries

Use `data/inputs/transoid.xyz` and `data/inputs/cisoid.xyz`. Each is a 57-atom Cartesian structure for the same simplified single-arm chromophore, with neutral charge and singlet multiplicity as stated in the XYZ comment. The structures are S0 geometries; no transition state, selected conformer, absolute reference energy, or target value is provided. The physical boundary is an isolated gas-phase molecule. The measured quantities are converged S0→S1 vertical excitation energies, oscillator strengths, dominant orbital contributions, and their signed difference. Do not infer solution, membrane, kinetics, or experimental wavelength from this calculation alone.

This is a fixed-structure property track: the supplied coordinates are public inputs for the named property comparison, not a scored structure discovery answer. Do not claim that the input geometry itself was rediscovered; report any optimization or conformer search separately.

# Required scientific validation/investigation

For each named structure, verify atom count, element sequence, charge and multiplicity; document and justify the electronic-structure method, excited-state treatment and convergence criteria; and establish that the reported root is the lowest singlet excited state rather than relying only on root number. Use the supplied S0 geometry directly for the requested vertical excitation. If you additionally optimize a geometry as a sensitivity check, keep the vertical result at the supplied geometry identifiable and report optimization convergence and any frequency/stationarity check separately. Assign the dominant orbital character and report enough state-tracking evidence to make that assignment auditable. Compute `cisoid_S1 - transoid_S1` in eV with an explicit sign convention. The calculation is complete when both structures have auditable converged results. If either calculation cannot be completed, submit the bounded-failure outcome after both named structures have been attempted, identifying every failed object, any usable partial result, diagnostics, and the limit reached.

# Deliverables

Submit `report/results.json` following `submission_schema.json`. A successful submission includes calculation provenance, explicit validation for each named structure, energies, oscillator strengths, orbital assignments, the signed shift, and a conclusion about whether the computed excitation shift and orbital assignments support the qualitative proposal. The bounded-failure branch does not require fabricated energies or a shift, but it does require both attempted objects, per-object status, every available partial result, concrete diagnostics, and an identification of the required results that remain unresolved.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
