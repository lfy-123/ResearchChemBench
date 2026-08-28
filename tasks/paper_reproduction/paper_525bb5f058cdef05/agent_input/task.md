# Scientific objective

Test the authors' proposed qualitative picture for gas-phase proton transfer from H3O+(H2O)n (n=0,1,2) to benzene. Independently determine which reaction complexes/pathways are viable and whether hydration changes proton-transfer thermodynamics, barriers, and predicted kinetics relative to bare hydronium. The scored object is the benzene PT network, not an exact reproduction of a hidden rate table.

The authors' testable qualitative hypothesis is that hydration can promote ligand-switching through stable ion--benzene adducts and internal proton-transfer barriers, reducing turnover relative to bare hydronium; test this hypothesis independently and do not treat it as an asserted result.

# Public inputs and scientific boundaries

Use the five XYZ files and manifest in `data/inputs/`. They uniquely specify neutral benzene (C6H6, charge 0, singlet), hydronium (H3O+, charge +1, singlet), its mono- and dihydrates (H3O+(H2O) and H3O+(H2O)2, each +1, singlet), and protonated benzene (C6H7+, +1, singlet) as starting geometries. Coordinates are starting guesses; optimize or replace them after checking connectivity. Consider gas-phase species, n=0–2, proton transfer and hydration/adduct channels among these atoms. Do not use the paper, SI, general web, or hidden reference files. Report energy units and thermal conditions explicitly.

# Required scientific validation/investigation

State an independent method and search protocol. Generate and deduplicate plausible encounter complexes and proton-transfer pathways for each n; optimize minima and candidate saddle points (or a defensible alternative pathway method). Validate minima with no imaginary frequencies and TSs with one mode along the proposed reaction coordinate, or explicitly report bounded failure. Compare thermochemistry and barrier descriptors for bare versus hydrated cases, and if rates are computed, define the kinetic model and field/effective-temperature grid. Completion requires either validated results for every n or a transparent bounded-failure report identifying the unvalidated objects. Stop when the stated candidate-generation space has been exhausted and additional starting arrangements no longer yield distinct validated structures, or when computational limits prevent this; report coverage, deduplication and limitations.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include object identities (reactant/product species, charge and multiplicity, and a structural or atom-mapping description), methods, validation evidence, energies/barriers or null with failure explanations, qualitative comparison, and a final conclusion. Include at least one candidate record for each of n=0, 1 and 2; a record may truthfully report bounded failure and unresolved alternatives. A result is complete only when every n=0,1,2 entry has a status and the report states the stopping rule and limitations.
