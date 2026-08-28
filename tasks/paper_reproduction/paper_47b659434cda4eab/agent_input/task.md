# Scientific objective

Determine how carbon-chain length changes the stability and preferred reaction pathway of the six explicitly identified linear alkyl carbocations in `data/inputs/carbocation_models.json`. Test the qualitative hypothesis that chain length changes competition among direct dehydrogenation to an olefin, rearrangement/quenching chemistry and bond cleavage. Report stationary-point evidence and a mechanistic conclusion; do not assume that an optimized structure or transition state exists.

# Public inputs and scientific boundaries

The public system is the six saturated, linear alkyl carbocations in the JSON file. Each record gives a unique connectivity, alpha/beta position, carbon count, charge +1 and doublet multiplicity. The measured quantities are optimized-minimum status, transition-state and intermediate energies on a clearly stated common reference, imaginary-frequency diagnostics, and IRC or an equivalently justified connectivity validation. The computational boundary is the molecular model selected by the Agent; state solvent, thermal and electronic-energy conventions. The source paper's precise optimized coordinates and numerical barriers are not public inputs and are not required.

# Required scientific validation/investigation

For each named model, generate a finite, explicitly enumerated set of chemically plausible pathways and deduplicate equivalent structures. Attempt optimization of the relevant minima and transition states. Advance a candidate to comparison only with a stationary-point diagnostic and a connectivity check: a first-order saddle requires one relevant imaginary mode, and an IRC in both directions is preferred; if IRC is unavailable, provide a chemically specific alternative validation and its limitation. Record failed optimizations rather than silently dropping them. Completion requires every six starting models to have a documented status and every advanced pathway to have validation evidence. Stop when the declared candidate set has been exhausted, or when additional searches cease to produce distinct validated pathways; state coverage and unresolved alternatives.

# Deliverables

Submit `report/results.json` conforming to the schema. Include one record for each of the six named models, all attempted candidates and their validation status, comparable energies/barriers with units and reference definition, and a conclusion addressing chain-length effects. A bounded-failure result is valid only if missing stationary points, attempted searches and scientific limitations are fully documented.
