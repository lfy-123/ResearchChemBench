# Scientific objective

Independently determine how carbon-chain length changes the stability and preferred reaction pathway of the six explicitly identified linear alkyl carbocations in `data/inputs/carbocation_models.json`. Generate and discriminate the Agent's own plausible explanations for the observed behavior using computation and validation rather than an assumed mechanism.

# Public inputs and scientific boundaries

The public system is the six saturated, linear alkyl carbocations in the JSON file. Each record gives a unique connectivity, alpha/beta position, carbon count, charge +1 and doublet multiplicity. The measured quantities are optimized-minimum status, transition-state and intermediate energies on a clearly stated common reference, imaginary-frequency diagnostics, and IRC or an equivalently justified connectivity validation. The computational boundary is the molecular model selected by the Agent; state solvent, thermal and electronic-energy conventions. The scored system is the isolated molecule; do not add a host or solvent.

# Required scientific validation/investigation

Propose a finite candidate-generation rule before searching, enumerate and deduplicate all candidates produced under that rule, and retain candidate identity with its parent model and proposed products. Attempt optimization of relevant minima and transition states. Advance a candidate to comparison only with a stationary-point diagnostic and a connectivity check: a first-order saddle requires one relevant imaginary mode, and an IRC in both directions is preferred; if IRC is unavailable, provide a chemically specific alternative validation and its limitation. Record failures and report search coverage. Completion requires every six starting models to have a documented status and every advanced pathway to have validation evidence. Stop when the declared candidate-generation rule is exhausted, or when additional searches cease to produce distinct validated pathways; state unresolved alternatives and how they affect the conclusion.

# Deliverables

Submit `report/results.json` conforming to the schema. Include the candidate-generation rule, all attempted candidates and validation status, comparable energies/barriers with units and reference definition, competing hypotheses and evidence-weighted discrimination, and a conclusion. A bounded-failure or inconclusive result is valid only if the search, validation and limitations are fully documented.
