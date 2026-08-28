# Scientific objective

For the closed model system 1a + [1.1.1]propellane (2) + thioxanthone (TXT), independently plan and execute a computational investigation of the reaction mechanism. The authors qualitatively propose sulfur-ylide formation, an intramolecular rearrangement, catalyst-assisted aromatization, and deamination; test this proposed route rather than accepting it. Determine the validated sequence of stationary points, relative solvent free energies, activation free energies for the principal catalysed and uncatalysed alternatives, and the step that controls the largest barrier.

# Public inputs and scientific boundaries

`data/inputs/reactants.json` uniquely defines neutral singlet 1a (N-(4-bromophenyl)-S-phenyl sulfenamide), neutral singlet [1.1.1]propellane 2, and neutral singlet TXT (thioxanthone), with toluene and 298.15 K as the environmental context. You may generate 3-D conformers and computational models, but do not use the paper, SI, general web, or hidden coordinate/energy records. The measured quantities are stationary-point frequency character, connectivity, relative free energies in kcal/mol, activation free energies from explicitly stated reference states, and mechanistic interpretation. Alternative conformers or failed searches are allowed if documented.

# Required scientific validation/investigation

Define a finite candidate record for every proposed minimum or transition state, retaining an unambiguous label, geometry provenance, connectivity, frequency evidence, and the reactant/product states it connects. Deduplicate candidates by chemical connectivity and conformational equivalence, then advance only candidates whose structures and charge/multiplicity are chemically consistent. A minimum must have zero imaginary frequencies; a transition state must have one chemically relevant imaginary mode and an IRC or equivalent downhill connectivity check. Build a connected profile from separated reactants through product and include an explicit TXT-containing route and a no-TXT comparison where your search finds one. Report the number and scope of conformers/pathways examined, unsuccessful searches, numerical settings, and uncertainty. Completion requires either a connected, frequency-validated profile with both comparisons or a bounded-failure report that identifies the missing state and demonstrates the searches attempted. Stop when the stated candidate-generation families and independent validation checks are exhausted; do not claim global exhaustiveness.

# Deliverables

Submit `report/results.json` conforming to the schema. It must contain method provenance, candidate records, validation outcomes, profile/barrier values with units and reference states, catalyst comparison, conclusion, limitations, and search coverage. A bounded-failure branch must still identify attempted candidates and the scientifically limiting missing result.
