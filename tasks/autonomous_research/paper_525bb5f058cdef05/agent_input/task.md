# Scientific objective

Determine, from first-principles computational investigation, how hydration of hydronium affects gas-phase proton transfer to benzene across n=0,1,2. Identify and discriminate plausible encounter complexes and proton-transfer pathways, quantify thermochemical and barrier changes, and state what these imply for relative reaction kinetics. Do not assume any mechanism or conclusion in advance.

# Public inputs and scientific boundaries

Use the five XYZ files and manifest in `data/inputs/`. They uniquely specify neutral benzene (C6H6, charge 0, singlet), hydronium (H3O+, charge +1, singlet), its mono- and dihydrates (H3O+(H2O) and H3O+(H2O)2, each +1, singlet), and protonated benzene (C6H7+, +1, singlet) as starting geometries. Coordinates are starting guesses; optimize or replace them after checking connectivity. The boundary is gas-phase species and channels formed from these atoms, n=0–2, including hydration, association, proton transfer, and dissociation. Do not use the paper, SI, general web, or hidden reference files. Report energy units and thermal conditions explicitly.

# Required scientific validation/investigation

Propose hypotheses before selecting pathways. Generate a finite, explicitly described set of encounter orientations and proton-transfer routes for each n; deduplicate by connectivity and geometry; optimize minima and candidate saddle points (or a defensible alternative). Validate minima with no imaginary frequencies and TSs with one reaction-coordinate mode, or report bounded failure. Use sensitivity checks appropriate to your method and explain coverage. Completion requires either validated results for every n=0,1,2 or a truthful bounded-failure report for each missing object. Stop when the declared generation space is exhausted with no new distinct validated structures, or when computational limits prevent further search; report the stopping rule, coverage, and unresolved alternatives.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include hypotheses, candidate identities, per-candidate validation, thermochemistry/barriers or null with reasons, kinetic interpretation, and a final conclusion. Include at least one candidate record for each of n=0, 1 and 2; a record may truthfully report bounded failure and unresolved alternatives. A result is complete only when each n has a status and the report distinguishes computed facts from hypotheses and limitations.
