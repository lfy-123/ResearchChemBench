# Scientific objective

Independently determine the fundamental anharmonic O–H stretching frequency (cm⁻¹) and dimensionless oscillator strength for neutral TFE···benzene, TFE···toluene, TFE···o-xylene, TFE···m-xylene, and TFE···p-xylene complexes, and infer how aromatic methyl count and positional isomerism affect those observables.  The research object is the explicitly named complex and its validated O–H fundamental transition; do not substitute an overtone, monomer, binding energy, or equilibrium constant.

# Public inputs and scientific boundaries

Read `data/inputs/systems.json`.  It uniquely specifies TFE and each aromatic partner by name and SMILES, with neutral charge and singlet multiplicity, and defines the five pairings.  Construct neutral noncovalent complexes without changing connectivity, protonation, charge, multiplicity, or substitution pattern.  Generate and label three-dimensional candidates independently.  Experimental gas/matrix spectra may be consulted only as clearly identified contextual measurements, not as calculated targets.  The task gives no author route, preferred mechanism, conformer ranking, software, or model chemistry; choose and justify a route.

# Required scientific validation/investigation

Propose plausible structural/model hypotheses, generate a scientifically justified candidate set for each named complex, deduplicate it, and report coverage.  Optimize advanced candidates and show minimum/stationarity evidence or record a bounded failure.  Compute the fundamental O–H anharmonic frequency and oscillator strength with a stated, reproducible model and convergence evidence.  Validate each reported system using an independent check (for example, repeat/model sensitivity, alternate retained conformer, or an identified experimental environment), preserving candidate identity and validation context.  Completion requires five system-level statuses, with validated results or explicit scientifically justified bounded failures, plus a conclusion that distinguishes observed calculation from interpretation.  Stop when the proposed candidate/model space has been sampled and further candidates do not alter the conclusion, or report a limitation and stop with partial status; do not claim global exhaustiveness without coverage evidence.

# Deliverables

Write `report/results.json` using the submission schema.  Include hypotheses considered, candidate provenance and structures, validation evidence, per-system fundamental frequency and oscillator strength when available, status, coverage/stopping information, cross-system trend, uncertainty/limitations, and the final scientific conclusion.  The JSON is authoritative; an additional readable report is optional.
