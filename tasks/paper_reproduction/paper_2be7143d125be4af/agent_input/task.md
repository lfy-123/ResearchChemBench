# Scientific objective

Independently calculate the neutral, closed-shell Azo-pNO2 and Azo-pCN molecules in `data/inputs/azo_targets.json`. For each, report an optimized structure, the electrostatic charge on the alpha azo nitrogen (the nitrogen attached to the para-substituted phenyl ring), and the homolytic dissociation energy of the mapped azo N=N bond. The authors hypothesized that substituents modulate azo electrophilicity and reduction behavior; test that qualitative hypothesis without assuming its numerical outcome.

# Public inputs and scientific boundaries

Use only the two molecules, canonical SMILES, charge 0, multiplicity 1, atom-role mapping, and BDE definition in the JSON input. The physical boundary is an isolated molecule; solvent, enzyme, and photophysics are outside scope. You may generate conformers and choose software/model chemistry, but disclose them. Do not use the paper or general web. The observables are charge in e and BDE in kJ/mol.

# Required scientific validation/investigation

Generate and deduplicate at least one chemically valid conformer per molecule, preserve the named azo atom mapping, optimize each, and demonstrate a stationary-point or equivalent convergence check. Validate the charge extraction by identifying the alpha atom in the submitted structure and state the charge-partitioning scheme. Validate each BDE with explicit parent and two neutral-fragment energies, consistent spin states, units, and sign convention. Compare the two molecules and report sensitivity to conformer or method choices if tested. Completion requires both identities to have auditable optimized geometries and both observables or a clearly documented bounded failure. Stop when both molecules pass the checks; if a molecule cannot be completed, stop after documenting the cause, attempted alternatives, and the resulting limitation.

# Deliverables

Submit `report/results.json` plus an auditable report or calculation archive referenced from it. Keep one record for each input ID (Azo-pNO2 and Azo-pCN), in input order, and identify the mapped alpha atom explicitly; the array order is not a scientific ranking. A complete record includes structure, method, convergence/stationarity evidence, charge scheme/value, parent and fragment energies, BDE, uncertainty/limitations, and a conclusion comparing pNO2 with pCN. If completion is not possible for one molecule, use the bounded-failure record for that molecule: identify it by ID, state the cause and attempted alternatives, and preserve all available validation evidence. Do not fabricate numerical values or structures to satisfy the complete branch.
