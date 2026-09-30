# Scientific objective

Using the mapped reactants, their explicitly defined neutral azide tautomers, and the four supplied connectivity-plus-tautomer candidate identities, independently determine the thermodynamic ordering of the resulting azide–alkyne adducts and the kinetic ordering of their formation pathways under a neutral, closed-shell isolated-molecule computational model. Explain which computed observables support the final selectivity conclusion.

# Public inputs and scientific boundaries

Use `data/inputs/reactants_and_candidate_definitions.json`. It defines explicit heavy-atom maps, neutral azide tautomers, charge 0, multiplicity 1, and the complete four-member set Pdt1–Pdt4. C1/C2 are the terminal/substituted alkyne carbons; N13/N14/N15 are the proximal/central/distal azide nitrogens. Preserve these identities, the original C16–N17–C18–N19–N20 ring, and the specified N–H position. Use each candidate's matching neutral azide tautomer; any proton-transfer process must be identified separately, never hidden by atom remapping. The boundary excludes explicit copper, solvent, and counterions unless separately explored and labelled. No paper route, candidate preference, product/TS coordinates, reference values or rankings are provided; do not claim an intramolecular reaction or a broader catalytic mechanism than this two-reactant organic model supports.

# Required scientific validation/investigation

Propose and discriminate plausible structural/pathway explanations within Pdt1–Pdt4. Choose and justify a computational approach appropriate to the neutral isolated-molecule objective. Generate and deduplicate reasonable conformers, optimize representatives, and report coverage. A product is accepted only with zero imaginary frequencies and preserved candidate connectivity. Locate a TS for each candidate pathway and accept it only with exactly one imaginary frequency and a chemically consistent reaction coordinate (IRC or justified alternative). Completion requires validated product and TS evidence for all four candidates; stop when coverage is reported, all four candidates have been attempted, and further searches no longer alter the selected representatives, or provide a bounded-failure/limitation report that identifies the missing validation.

# Deliverables

Submit `report/results.json` conforming to the schema. Include per-candidate identity and validation context, energies and activation energies in kcal/mol, both orderings when all required observables are available, the proposed discriminating explanation, computational method, method justification and thermochemical convention, coverage, and a conclusion with limitations. Do not invent an experimental or literature-discovery narrative. If any candidate cannot be validated, use the bounded-failure branch and identify the missing validation; do not fabricate energies, orderings, or structures.
