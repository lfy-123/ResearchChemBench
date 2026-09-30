# Scientific objective

For the closed model system 1a + [1.1.1]propellane (2) + thioxanthone (TXT), determine by independent computation which reaction pathway(s) are chemically plausible and energetically competitive. Establish a validated stationary-point network, compare TXT-containing and TXT-free explanations where supported by the chemistry, quantify the principal activation free energies, and state what controls the overall barrier. Treat mechanistic proposals as hypotheses to discriminate, not as given facts.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the reaction proceeds through sulfur-ylide formation followed by an intramolecular [2,3]-Wittig rearrangement. They further interpret thioxanthone as assisting an aromatization event and assign deamination as the product-forming step requiring particular scrutiny.

**Candidate route or mechanism.**
Examine a route beginning with sulfur attack on [1.1.1]propellane to form a sulfur ylide, followed by the proposed intramolecular rearrangement, TXT-assisted Alder-type aromatization, and deamination to the sulfur-substituted methylenecyclobutane product. Include the corresponding uncatalysed aromatization alternative as a comparison hypothesis.

**Discriminating evidence.**
Use optimized stationary points, harmonic frequency character, IRC or equivalent connectivity checks, and solvent-corrected relative and activation free energies to test each proposed event. Compare the TXT-containing and TXT-free aromatization pathways and inspect which validated step presents the controlling barrier.

# Public inputs and scientific boundaries

`data/inputs/reactants.json` uniquely defines neutral singlet 1a (N-(4-bromophenyl)-S-phenyl sulfenamide), neutral singlet [1.1.1]propellane 2, and neutral singlet TXT (thioxanthone), with toluene and 298.15 K as the environmental context. The scored system is the isolated molecule set defined by these reactants; do not add a host or solvent molecule to the molecular system. You may generate 3-D conformers and computational models, but do not use the paper, SI, or general web. Measure frequency character, connectivity, relative free energies in kcal/mol, activation free energies from explicitly stated reference states, and evidence-weighted mechanistic conclusions. Alternative pathways, conformers, and bounded failures are valid outcomes.

# Required scientific validation/investigation

Propose and discriminate plausible hypotheses for bond-making, rearrangement, catalyst participation, and product-forming steps. Define finite candidate records with unique labels, geometry provenance, connectivity, frequency evidence, and connected states. Deduplicate by connectivity and conformational equivalence; advance only chemically consistent candidates. Validate minima with zero imaginary frequencies and transition states with one relevant imaginary mode plus IRC or equivalent connectivity evidence. Report pathway/conformer coverage, failed searches, method sensitivity, uncertainty, and why the stopping boundary is adequate. Completion requires a connected validated pathway network and a reasoned comparison of at least one catalyst-involving and one catalyst-independent hypothesis, or a bounded-failure report that identifies and evidences the limiting missing state. Stop after the declared candidate-generation families and independent validation checks are exhausted; do not claim global exhaustiveness.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. It must contain proposed hypotheses, candidate and validation records, profile/barrier values with units and reference states, comparative conclusion, limitations, and search coverage. A bounded-failure branch must identify attempted candidates and the scientifically limiting missing result.
