# Scientific objective

For the closed model system 1a + [1.1.1]propellane (2) + thioxanthone (TXT), independently plan and execute a computational investigation of the reaction mechanism. The authors qualitatively propose sulfur-ylide formation, an intramolecular rearrangement, catalyst-assisted aromatization, and deamination; test this proposed route rather than accepting it. Determine the validated sequence of stationary points, relative solvent free energies, activation free energies for the principal catalysed and uncatalysed alternatives, and the step that controls the largest barrier.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the reaction proceeds through sulfur-ylide formation followed by an intramolecular [2,3]-Wittig rearrangement. They further interpret thioxanthone as assisting an aromatization event and assign deamination as the product-forming step requiring particular scrutiny.

**Candidate route or mechanism.**
Examine a route beginning with sulfur attack on [1.1.1]propellane to form a sulfur ylide, followed by the proposed intramolecular rearrangement, TXT-assisted Alder-type aromatization, and deamination to the sulfur-substituted methylenecyclobutane product. Include the corresponding uncatalysed aromatization alternative as a comparison hypothesis.

**Discriminating evidence.**
Use optimized stationary points, harmonic frequency character, IRC or equivalent connectivity checks, and solvent-corrected relative and activation free energies to test each proposed event. Compare the TXT-containing and TXT-free aromatization pathways and inspect which validated step presents the controlling barrier.

# Public inputs and scientific boundaries

`data/inputs/reactants.json` uniquely defines neutral singlet 1a (N-(4-bromophenyl)-S-phenyl sulfenamide), neutral singlet [1.1.1]propellane 2, and neutral singlet TXT (thioxanthone), with toluene and 298.15 K as the environmental context. You may generate 3-D conformers and computational models, but do not use the paper, SI, general web, or hidden coordinate/energy records. The measured quantities are stationary-point frequency character, connectivity, relative free energies in kcal/mol, activation free energies from explicitly stated reference states, and mechanistic interpretation. Alternative conformers or failed searches are allowed if documented.

Primary thermochemical definition: G_solution = E_solution_SP + H_corr - 0.5*(H_corr - G_corr), where H_corr and G_corr are the matching gas-frequency thermal corrections at 298.15 K. Apply the same half-entropy convention, atom-balanced stoichiometry and common reference to every state and pathway comparison. Distinguish this quantity from an unmodified full-entropy Gibbs energy and record the electronic-structure/dispersion implementation actually used.

# Required scientific validation/investigation

Define a finite candidate record for every proposed minimum or transition state, retaining an unambiguous label, geometry provenance, connectivity, frequency evidence, and the reactant/product states it connects. Deduplicate candidates by chemical connectivity and conformational equivalence, then advance only candidates whose structures and charge/multiplicity are chemically consistent. A minimum must have zero imaginary frequencies; a transition state must have one chemically relevant imaginary mode and an IRC or equivalent downhill connectivity check. Build a connected profile from separated reactants through product and make separate, explicit attempts for a TXT-containing route and a no-TXT comparison. For every reported barrier, use an explicit comparison label (for example `initial_attack`, `uncatalyzed_aromatization`, `TXT-assisted_aromatization`, or `deamination`), identify its transition-state candidate, state the reference state, and report kcal/mol. If a route is not validated, record its failed search and use the bounded-failure branch rather than silently omitting the comparison. Report the number and scope of conformers/pathways examined, unsuccessful searches, numerical settings, and uncertainty. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to the schema. It must contain method provenance, candidate records, validation outcomes, profile/barrier values with units and reference states, catalyst comparison, conclusion, and search coverage. A bounded-failure branch must still identify attempted candidates and the scientifically limiting missing result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
