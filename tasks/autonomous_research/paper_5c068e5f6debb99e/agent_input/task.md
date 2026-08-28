# Scientific objective

Determine, without relying on a reported mechanism, which of two chemically defined initial sulfur-transfer events is kinetically more accessible for the fully specified reactants in this package. Establish validated transition-state candidates, comparable solution Gibbs barriers, and a defensible mechanistic explanation or explain why the available calculations cannot discriminate the events.

# Public inputs and scientific boundaries

The complete molecular identities, atom maps, charge, multiplicity, stoichiometry, base, solvent, temperature, and scope are in `data/inputs/system.json` and `data/inputs/structures.smi`. Atom 6 is transferred sulfur, atom 7 is the leaving-group nitrogen, atom 27 is candidate site O, and atom 23 is candidate site C. The only candidate endpoints are site_O: form 27–6 and cleave 6–7, and site_C: form 23–6 and cleave 6–7. Use a common balanced ensemble containing one reactant_A, one reactant_B, and at least one sodium counterion. The primary boundary is a closed-shell singlet solution model in DME at 213.15 K; subsequent cascade chemistry and experimental product yields are not evaluated.

# Required scientific validation/investigation

Formulate plausible ion-pair, tautomer, conformer, and transition-state hypotheses for both named endpoints, generate candidates, and deduplicate them using a stated structural criterion. Retain only candidates with the required atom-map connectivity. Validate minima by frequencies and transition states by one relevant imaginary mode plus an IRC or equivalent endpoint/path test. Use the same free-energy convention and common reference for both channels, disclose method and solvation choices, and report candidate coverage, rejected candidates, sensitivity, and limitations. Completion requires a validated candidate for both channels or a bounded failure that names the channel and documents the attempted search. Stop after the declared starting-ensemble and hypothesis space has been covered and new starts yield no distinct validated candidate under the stated criterion; otherwise report the achieved coverage and stop limitation.

# Deliverables

Submit `report/results.json` conforming to the schema. Include the independent hypotheses, candidate-level validation records, selected barriers if available, ordering/difference if both are available, evidence for the mechanistic explanation, and truthful bounded-failure branches when discovery or validation is incomplete.
