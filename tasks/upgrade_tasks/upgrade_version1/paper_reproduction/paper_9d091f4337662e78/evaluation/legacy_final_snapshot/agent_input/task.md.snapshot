# Scientific objective

Independently plan and execute a computational test of the authors' qualitative conformer-population route for neutral singlet compound 1. For the three conformer classes represented by initial structures 1-1, 1-2 and 1-3, determine optimized-minimum status, gas-phase relative Gibbs free energy at 298.15 K, and Boltzmann population. The authors' qualitative route is conformer thermochemistry used to weight downstream ECD; do not assume their numerical outcome or software/model chemistry.

# Author-provided scientific guidance

**Author hypothesis or claim.** The authors treat conformer thermochemistry as the population-weighting foundation for a downstream Boltzmann-averaged ECD calculation used in their structural assignment. For this task, the relevant claim is that the relative gas-phase Gibbs energies of the named conformers provide their thermodynamic weights at 298.15 K.

**Candidate route or mechanism.** The authors' candidate route is to optimize each conformer with dispersion-aware density-functional theory, characterize the optimized structure by frequencies, refine its electronic energy with a larger basis treatment, and combine that energy with thermal corrections to obtain conformer Gibbs energies. Those Gibbs energies are then converted into Boltzmann populations over the conformer set.

**Discriminating evidence.** Test this route using convergence to distinct optimized endpoints, frequency evidence for true local minima, consistently evaluated Gibbs energies, and normalized Boltzmann populations. Sensitivity to the electronic-structure model, thermal treatment, and low-frequency modes helps determine whether the inferred ordering is robust.

# Public inputs and scientific boundaries

The files `data/inputs/conformer_1-1.xyz`, `conformer_1-2.xyz`, and `conformer_1-3.xyz` are Cartesian coordinates in Å for the complete 54-atom neutral singlet structures of compound 1. Atom order is the order in each XYZ file; no atoms may be added, removed, remapped, protonated, or stereochemically inverted. The thermochemical boundary is isolated gas-phase compound 1 at T=298.15 K. The scored object is only this named three-conformer set; additional conformers may be reported separately from the primary three-member normalization. You may generate computational models and reoptimize structures, but must state method, software, thermal treatment, and any frequency scaling or low-frequency treatment.

# Required scientific validation/investigation

The supplied XYZ files are unoptimized, independently generated initial structures, not stationary-point results. `data/inputs/starting_geometry_definition.json` defines the molecular graph, stereochemistry, atom identities and coarse initial conformer classes. Its angular windows are initialization guidance, not final torsion targets or optimization constraints.

Keep initial-attempt identities separate from optimized endpoint identities. Attempt all three named initial classes and record their outcomes in `initial_attempts`. Assign each distinct optimized endpoint its own `id`, retain its contributing `initial_ids`, and supply `endpoint_evidence` containing the final geometry, atom mapping and distinguishing conformational features. A filename or a matching energy does not establish conformer identity. Report basin changes explicitly. If multiple initial structures converge to the same endpoint, list that endpoint only once and point the corresponding attempts to that same ID.

Optimize and characterize the endpoints with a justified common gas-phase thermochemical convention, including true-minimum evidence and Gibbs corrections at 298.15 K. You may try alternative unoptimized starts within the same three declared chemical/conformational classes to recover a missing member; an unrestricted conformer search is not required. Record the starting attempts and distinct validated endpoint identities. A complete result requires three distinct validated members of the specified conformer set, not just three finished calculations. If fewer members are obtained or identity remains unresolved, report `partial`, state the missing/ambiguous member and retain real available energies without inventing missing results. In that branch use `null` for full-set populations, population sum and most-populated member.

For a complete set, calculate relative Gibbs energies and Boltzmann populations at 298.15 K using one explicit common reference and normalize over the three distinct endpoints only. Specify the method and low-frequency treatment used for the Gibbs energies. Do not use the percentages of an unavailable larger ensemble or count the same endpoint twice. The evaluator matches final conformational identity using geometry and mapping, not array order, starter filename or energy proximity.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include initial-attempt records, deduplicated final conformer identity and geometry evidence, optimization/minimum evidence, relative Gibbs energy in kcal/mol when available, population in percent when available, method provenance, normalization, the most-populated named conformer when all required values are available (otherwise `null`), and a conclusion about the bounded three-conformer result. Include honest failure records for any conformer that cannot be completed; failed records must not contain fabricated numeric values.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
