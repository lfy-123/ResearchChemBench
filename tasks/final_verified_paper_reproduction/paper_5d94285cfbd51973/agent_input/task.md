# Scientific objective

For the supplied AZ9 identity, determine a validated gas-phase neutral-singlet minimum and report its HOMO energy, LUMO energy, HOMO–LUMO gap, vertical electronic dipole moment, and frontier-orbital-derived IP, EA, hardness, softness, chemical potential, electronegativity, and conventional electrophilicity index. These are computational descriptors, not experimental redox energies or evidence of biological mechanism.

# Author-provided scientific guidance

Independently test the authors' qualitative hypothesis that the isolated-molecule electronic structure and polarity of AZ9 can provide a defensible descriptor-level basis for discussing its interaction propensity.

# Public inputs and scientific boundaries

Use `data/inputs/system.json` and `data/inputs/AZ9.smi`. They uniquely define AZ9 as 1-(2-benzyl-6-chloro-3-oxo-2,3-dihydropyridazin-4-yl)-N-(2,4-dimethylphenyl)azetidine-3-carboxamide (C23H23ClN4O2), formal charge 0, multiplicity 1, with no specified configurational stereochemistry. Generate all 3D structures yourself. Treat one isolated molecule in the gas phase; do not add solvent, counterions, protein, protonation alternatives, or experimental calibration. Choose and justify the electronic-structure method and software independently. The authors' proposed scientific route is only that frontier-orbital and polarity descriptors may rationalize interaction propensity; no author model chemistry, protocol, conformer, or result is supplied.

# Required scientific validation/investigation

Generate a finite conformer set from the fixed connectivity, record the generation method, deduplicate by molecular graph and heavy-atom geometry, and advance every distinct low-energy basin that could plausibly change the reported dipole or orbital values. Refine candidates consistently and select the lowest electronic-energy structure at the final method. Verify the selected structure is a true minimum by a Hessian with zero imaginary frequencies; if numerical noise remains, tighten and repeat until the classification is unambiguous. Report the number generated, deduplicated, advanced, and frequency-validated, plus the final energy span. Validate numerical stability with at least one scientifically motivated sensitivity check (for example, a denser integration grid, tighter SCF/geometry criteria, or a second reasonable method/basis) and report changes in HOMO, LUMO, gap, and dipole. Compute IP=-EHOMO, EA=-ELUMO, η=(IP-EA)/2, σ=1/(2η), μ=-(IP+EA)/2, χ=(IP+EA)/2, and conventional ω=μ²/(2η), preserving signs and units. Completion requires a frequency-validated minimum, all requested values, internally consistent arithmetic, and the sensitivity result.

# Deliverables

Submit `report/results.json` matching the schema. Include method/software; conformer counts; one record for every deduplicated candidate with a unique identity, relative energy, advancement decision, and candidate-specific validation evidence; selected-structure coordinates as an XYZ string; stationarity evidence; energies/descriptors with units implicit from field names; sensitivity changes; and a conclusion based on the calculated descriptors and numerical-stability results.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.

# Partial or unsuccessful submission

Use `status: "partial"` or `status: "bounded_failure"` when required calculations or analyses remain unavailable. Retain all actual partial results in their original fields. Include `failure` with a nonempty `reason`, a nonempty `missing_observables` array naming the unavailable result fields, and an `evidence` array of existing input, output or diagnostic paths (empty only if no artifact was produced). Explain which calculation failed or was not attempted; do not invent output files.

For these two statuses, the schema permits `null` for the specified unavailable calculated values, selected structures, state assignments or output paths. Keep the known molecular identities, charges, multiplicities, units and attempted methods. Report actual counts, including zero generated/validated candidates when appropriate. An unavailable frequency result is `null`, not zero imaginary modes or an empty list claiming a completed frequency analysis. A genuinely computed zero or an established empty imaginary-mode list remains valid evidence. A missing comparison is not a zero difference or zero RMSE.

Other statuses, and omission of status where the original schema permits it, retain the complete-result format. Passing this format check does not establish scientific completion: uncomputed endpoints receive no completion credit, and existing scientific rules still assess the actual evidence. This reporting branch does not change the scientific target, required successful investigation, or numerical acceptance criteria.
