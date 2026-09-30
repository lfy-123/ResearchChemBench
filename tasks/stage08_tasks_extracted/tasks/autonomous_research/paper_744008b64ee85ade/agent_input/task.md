# Scientific objective

Independently establish the gas-phase reaction kinetics and product selectivity of acetyl-peroxy radical CH3C(O)O2 reacting with HO2 at 1 atm, with emphasis on whether an acid-forming channel is kinetically relevant in the 500–800 K cool-flame interval. Formulate and discriminate plausible explanations on the singlet and triplet surfaces from calculations and report the 520 K acetic-acid kinetic-model observable.

# Public inputs and scientific boundaries

Use `data/inputs/reactants.json` as the authoritative identity, mapping, charge, multiplicity, pressure and temperature input. The scored system is the isolated acetyl-peroxy + HO2 bimolecular gas-phase reaction; do not add a host or solvent. Generate atom-balanced product structures and track them with explicit spin and channel labels. You may generate conformers and computational models.

# Required scientific validation/investigation

Propose a finite candidate-generation rule for encounter complexes, stationary points and product channels on both total-spin surfaces. Deduplicate by stated connectivity and geometry criteria. For every advanced candidate, provide optimization and frequency evidence; validate minima by zero imaginary frequencies and transition states by one imaginary frequency plus a reaction-mode check, or give a justified alternative. Compute or estimate channel rates and branching at all listed temperatures, including the 520 K validation condition, and quantify uncertainty. Generate and test your own explanations or pathways, and use the computed evidence to assess acid-channel relevance. Completion requires either a converged model that classifies all generated candidates and supports a defensible conclusion or a bounded-failure report with unresolved candidate identities and coverage. Stop when the stated generation rule is exhausted and a further independent search produces no new distinct candidate, or when a clearly documented computational limitation prevents completion; report the stopping condition and limitations.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. Include candidate structures and validation context, rate/branching tables with units, the 520 K acetic-acid mole-fraction test, the hypotheses considered and discriminating evidence, coverage, conclusion and limitations. A bounded failure is acceptable only if all required fields in the failure branch are populated.
