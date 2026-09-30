# Scientific objective

Determine, by an independent computational investigation, whether the specified bifunctional ionic-liquid system exhibits a reproducible electronic difference between its carbonyl site and quaternary-ammonium site relative to the specified reference models. Report four atom-specific Mulliken charges, the two paired differences and signs, and a carefully bounded scientific conclusion. Consider and discriminate plausible explanations for any observed differences, including model/conformer and charge-partitioning sensitivity, without asserting a mechanism beyond the calculations.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the bifunctional ionic-liquid catalyst electronically differentiates its two functional sites: the trifluoroacetyl carbonyl site is less electrophilic than the corresponding TFAP model, while the quaternary-ammonium site is more positively charged than the corresponding [PTMA]OTf model. They use these opposing charge shifts as evidence that the sites can cooperate electronically in epoxide activation and selectivity.

**Candidate route or mechanism.**
The relevant comparison is a paired electronic perturbation: compare the carbonyl-carbon charge in [TMTFABA]OTf with TFAP, and compare the quaternary-ammonium-nitrogen charge in [TMTFABA]OTf with [PTMA]OTf. Treat reduced carbonyl electrophilicity together with increased ammonium-site positive character as the proposed explanation to test, while considering whether geometry, ion-pair arrangement, conformer, or population-analysis choices could produce the pattern.

**Discriminating evidence.**
Use optimized structures and auditable atom-resolved Mulliken populations for all three systems, with stationary-point validation and explicit coverage of constructed conformers or ion-pair arrangements. The paired charge differences, their signs, and sensitivity across the declared computational checks discriminate the proposed site differentiation from model or charge-partitioning artifacts.

# Public inputs and scientific boundaries

Use `data/inputs/systems.json`. It uniquely defines [TMTFABA]OTf, [PTMA]OTf and TFAP by name, SMILES, formula, total charge, singlet multiplicity, solvent and atom environments. The OTf anion is included in the two ionic pairs. The physical boundary is these three isolated systems in an acetonitrile continuum. The measured quantity is Mulliken charge; no experimental result, author hypothesis, method, target value or candidate ranking is provided. You may construct 3D geometries and investigate conformers, but must report coverage and selection criteria.

# Required scientific validation/investigation

Propose and declare a reproducible computational protocol, then apply it consistently to all three systems. Generate a finite set of distinct starting conformers/ion-pair arrangements when relevant, deduplicate them by a stated structural criterion, optimize candidates, and advance only candidates with auditable convergence and minimum validation. If you use one starting geometry, justify why broader coverage is immaterial for this fixed comparison. Identify the scored atoms by the supplied chemical environments, extract auditable Mulliken charges, and assess whether the paired trends survive your stated sensitivity checks. Completion requires either validated results for all three systems and a coverage/stopping statement, or a bounded-failure report naming the missing system and evidence. Stop when the fixed systems are covered and additional conformers no longer change the reported scientific conclusion under your stated criterion; report residual uncertainty rather than inventing certainty.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the independent protocol, candidate/coverage table, validation evidence, four charges, two differences, uncertainty/sensitivity assessment, conclusion, and limitations. A bounded-failure branch must preserve attempted work and identify missing outputs. Numeric charges and differences use elementary-charge units.
