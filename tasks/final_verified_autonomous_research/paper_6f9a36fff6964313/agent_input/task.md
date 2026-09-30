# Scientific objective

Determine, by an independent computational investigation, whether the specified bifunctional ionic-liquid system exhibits a reproducible electronic difference between its carbonyl site and quaternary-ammonium site relative to the specified reference models. Report four atom-specific Mulliken charges, the two paired differences and signs, and a carefully bounded scientific conclusion. Consider and discriminate plausible explanations for any observed differences, including model/conformer and charge-partitioning sensitivity, without asserting a mechanism beyond the calculations.

# Public inputs and scientific boundaries

Use `data/inputs/systems.json`. It uniquely defines [TMTFABA]OTf, [PTMA]OTf and TFAP by name, SMILES, formula, total charge, singlet multiplicity, solvent and atom environments. The OTf anion is included in the two ionic pairs. The physical boundary is these three isolated systems in an acetonitrile continuum. The measured quantity is Mulliken charge; no experimental result, author hypothesis, method, target value or candidate ranking is provided. You may construct 3D geometries and investigate conformers, but must report coverage and selection criteria.

# Required scientific validation/investigation

Propose and declare a reproducible computational protocol, then apply it consistently to all three systems. Generate a finite set of distinct starting conformers/ion-pair arrangements when relevant, deduplicate them by a stated structural criterion, optimize candidates, and advance only candidates with auditable convergence and minimum validation. If you use one starting geometry, justify that finite scope, report checks actually performed, and explicitly retain unresolved conformer/ion-pair uncertainty; do not claim untested broader coverage is immaterial. Identify the scored atoms by the supplied chemical environments, extract auditable Mulliken charges, and assess whether the paired trends survive your stated sensitivity checks. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result. Do not represent an unperformed sensitivity test as a calculated result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the independent protocol, candidate/coverage table, validation evidence, four charges, two differences, uncertainty/sensitivity assessment, conclusion. A bounded-failure branch must preserve attempted work and identify missing outputs. Numeric charges and differences use elementary-charge units.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
