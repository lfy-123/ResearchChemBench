# Scientific objective


Determine, without relying on a reported mechanism, which of two chemically defined initial sulfur-transfer events is kinetically more accessible for the fully specified reactants in this package. Establish validated transition-state candidates, comparable solution Gibbs barriers, and a defensible mechanistic explanation or explain why the available calculations cannot discriminate the events.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that sulfur transfer from the specified N-thiophthalimide to the hydroxylamine substrate can proceed through competition between O-site and C-site initial substitution, with the C-site event supported by favorable sodium-associated and aromatic interactions.

**Candidate route or mechanism.**
Examine a base-associated, closed-shell pathway in which the substrate engages the sulfur reagent through either its hydroxylamine oxygen or its activated 1,3-dicarbonyl carbon, while the sulfur–nitrogen bond breaks. Treat these as candidate channels to test rather than established outcomes; later cascade chemistry is outside the objective.

**Discriminating evidence.**
Use validated minima and transition states, common-reference solution Gibbs barriers, endpoint/path connectivity checks, and structural or interaction analysis focused on sodium association and aromatic contacts to distinguish the channels. Compare the interaction evidence with electronic descriptors rather than assuming any single descriptor explains the ordering.

# Public inputs and scientific boundaries

The complete molecular identities, atom maps, charge, multiplicity, stoichiometry, base, solvent, temperature, and scope are in `data/inputs/system.json` and `data/inputs/structures.smi`. Atom 6 is transferred sulfur, atom 7 is the leaving-group nitrogen, atom 27 is candidate site O, and atom 23 is candidate site C. The only candidate endpoints are site_O: form 27–6 and cleave 6–7, and site_C: form 23–6 and cleave 6–7. Use a common balanced ensemble containing one reactant_A, one reactant_B, and at least one sodium counterion. The primary boundary is a closed-shell singlet solution model in DME at 213.15 K; subsequent cascade chemistry and experimental product yields are not evaluated.

# Required scientific validation/investigation

Generate and test independent ion-pair, tautomer, conformer, and transition-state hypotheses for both named endpoints, and deduplicate them using a stated structural criterion. Retain only candidates with the required atom-map connectivity. Validate minima by frequencies and transition states by one relevant imaginary mode plus an IRC or equivalent endpoint/path test. Use the same free-energy convention and common reference for both channels, disclose method and solvation choices, and report candidate coverage, rejected candidates, sensitivity, and limitations. Completion requires a validated candidate for both channels or a bounded failure that names the channel and documents the attempted search. Stop after the declared starting-ensemble and hypothesis space has been covered and new starts yield no distinct validated candidate under the stated criterion; otherwise report the achieved coverage and stop limitation.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. Include the independent hypotheses, candidate-level validation records, selected barriers if available, ordering/difference if both are available, evidence for the mechanistic explanation, and truthful bounded-failure branches when discovery or validation is incomplete. Ensure all required result keys and types in the local schema are satisfied.
