# Scientific objective

Independently characterize how E/Z isomerization of neutral E- and Z-1,2-bis(tetrazol-5-yl)ethylene (H2bte) changes molecular electronic structure and noncovalent-interaction descriptors. Generate and discriminate plausible explanations for any differences using optimized structures, ESP extrema, NCI features, and π-electron delocalization; do not assume a particular mechanism or explanatory ranking in advance.

# Public inputs and scientific boundaries

Use `data/inputs/system_manifest.json`, `data/inputs/e_h2bte.xyz`, and `data/inputs/z_h2bte.xyz`. Both structures are neutral singlets with formula C4H4N8 and explicitly labeled E/Z central-alkene stereochemistry; XYZ coordinates are starting guesses and must not be treated as results. The system is an isolated-molecule comparison, optionally with an explicitly reported methanol continuum; preserve the neutral singlet state and do not add other molecules or a crystal environment. Crystal packing, synthesis, irradiation, and experimental sensitivity values are outside the computed target and may only be discussed as clearly labeled external context. Use the supplied public inputs and your own calculations as the evidence for computed results. Every result must retain `E-H2bte` or `Z-H2bte` identity.

# Required scientific validation/investigation

For each named isomer, independently choose and justify a computational route, generate at least one optimized structure, and verify atom count, connectivity, E/Z identity, optimization convergence, and (where feasible) absence of imaginary frequencies. The submission must contain exactly two isomer records, in the manifest order `E-H2bte`, then `Z-H2bte`, with each record's `id` explicitly naming the object. Define a finite set of plausible explanations for observed descriptor differences, test the explanations with like-for-like ESP, NCI, and π-delocalization analyses, and report which are supported, contradicted, or unresolved. Report ESP extrema in kcal mol−1. Record grid/surface settings, units, software, and all method choices. Completion requires validated results for both isomers and an evidence-linked discrimination of explanations, or a bounded-failure report naming the missing calculation and remaining supportable claims. Stop when both isomers pass validation and each proposed explanation has been tested against the reported observables, or when a reproducible limitation prevents this; report coverage and do not silently substitute unvalidated values.

# Deliverables

Write `report/results.json` conforming to the local `submission_schema.json`. Include independent rationale, methods, per-isomer structure and validation records, ESP extrema, NCI and LOL-π observations, hypothesis/explanation tests, comparison, limitations, and conclusion. Include provenance sufficient for reproduction. A bounded failure must use the schema's failure branch and still report completed validation and limitations.
