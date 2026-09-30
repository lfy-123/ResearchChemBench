# Scientific objective

Determine the relative stability of the two supplied neutral probe-A proton-placement states and explain the physically meaningful conclusion supported by computation. The research object is the two complete 73-atom structures (C35H33N3O2) in the public XYZ files; the scored endpoint is a consistently defined relative energy in kcal mol⁻¹. Develop and discriminate your own computational explanation of any ordering; no author route or proposed mechanism is provided.

# Public inputs and scientific boundaries

`data/inputs/probe_A_OH_N.xyz` and `data/inputs/probe_A_NH_O.xyz` are complete neutral-singlet probe-A Cartesian geometries in Å. The filenames identify the two proton-placement states: `A_OH_N` has an O-bound labile H and OH···N contact; `A_NH_O` has an N-bound labile H and NH···O contact. Atom order is part of each input identity. Use an isolated-molecule boundary, state all environmental and thermal assumptions, and do not infer experimental pH response, spectra, populations, or any unprovided structure.

# Required scientific validation/investigation

Independently choose and justify a calculation capable of comparing the two named states. You may generate conformers or alternative starting geometries, but retain candidate identity and explain coverage, deduplication, advancement, and why the final comparison is representative. Validate each reported minimum with frequencies or an equivalently justified stationarity test, and report failed or ambiguous cases. The investigation is complete when both named states have comparable validated energies and a mechanism-level interpretation is supported by the computed observables, or a bounded failure report identifies why that cannot be achieved. Stop after the two-state comparison, validation, coverage statement, and limitations are complete; do not search unrelated protonation states.

# Deliverables

Submit `report/results.json` and referenced supporting files. A successful result must identify both states using `A_OH_N` and `A_NH_O`, report each energy/validation status, the relative energy in kcal mol⁻¹ with its definition, your independently reasoned explanation, search coverage, and limitations. A failure branch is allowed only with concrete diagnostic evidence and no invented result; in that branch, do not provide fabricated success-only energies or conclusions.
