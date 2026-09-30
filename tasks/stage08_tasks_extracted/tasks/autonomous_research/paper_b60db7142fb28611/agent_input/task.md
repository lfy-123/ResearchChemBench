# Scientific objective

Using the two mapped reactants and the four supplied CuAAC connectivity classes, independently determine the thermodynamic ordering of the resulting adducts and the kinetic ordering of their formation pathways under a neutral, closed-shell isolated-molecule computational model. Explain which computed observables support the final selectivity conclusion.

# Public inputs and scientific boundaries

Use `data/inputs/reactants_and_candidate_definitions.json`. It uniquely defines reactant identity, atom preservation, charge 0, multiplicity 1, and the complete four-member candidate set Pdt1–Pdt4. Interpret each immutable definition by the named atom roles (the two alkyne carbons, the two terminal azide nitrogens, and the azide ring atom), and preserve those identities in every product and pathway record. The scored system is the neutral, closed-shell isolated organic molecules; do not add explicit copper, solvent, or counterions. Do not claim a broader catalytic mechanism than the calculation supports.

# Required scientific validation/investigation

Propose and discriminate plausible structural/pathway explanations within Pdt1–Pdt4. Choose and justify a computational approach appropriate to the neutral isolated-molecule objective. Generate and deduplicate reasonable conformers, optimize representatives, and report coverage. A product is accepted only with zero imaginary frequencies and preserved candidate connectivity. Locate a TS for each candidate pathway and accept it only with exactly one imaginary frequency and a chemically consistent reaction coordinate (IRC or justified alternative). Completion requires validated product and TS evidence for all four candidates; stop when coverage is reported, all four candidates have been attempted, and further searches no longer alter the selected representatives, or provide a bounded-failure/limitation report that identifies the missing validation.

# Deliverables

Submit `report/results.json` conforming to the schema. Include per-candidate identity and validation context, energies and activation energies in kcal/mol, both orderings when all required observables are available, computational method, method justification and thermochemical convention, coverage, and a conclusion with limitations. Do not invent an experimental or literature-discovery narrative. If any candidate cannot be validated, use the bounded-failure branch and identify the missing validation; do not fabricate energies, orderings, or structures.
