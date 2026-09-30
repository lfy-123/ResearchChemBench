# Scientific objective

Determine the gas-phase molecular dipole magnitudes of the five supplied isolated fragments—4-fluoroaniline, 4-butylaniline, bis(4-fluorophenyl)amine, (4-butylphenyl)-N-(4-fluorophenyl)amine, and bis(4-butylphenyl)amine—and establish what polarity pattern is supported by independent computation. Treat any qualitative explanation as a hypothesis to be tested from the calculations, not as a premise.

# Public inputs and scientific boundaries

Use `data/inputs/fragments.json` as the authoritative identity record. Each entry supplies a unique ID, name, SMILES connectivity, charge 0, and multiplicity 1. The research object is each isolated molecule in the gas phase. Generate 3D starting structures from the SMILES and preserve atom identity. The measured quantity is the total dipole magnitude in Debye at the reported optimized state. Do not model the full acceptors, crystal packing, solvent, blend, or device, and do not use the paper or general web as an input.

# Required scientific validation/investigation

For every named fragment, choose and justify a computational approach, then document structure construction, optimization convergence, method/basis/software, and the final dipole magnitude. Test at least one additional chemically reasonable starting conformer for each flexible fragment; deduplicate converged geometries by connectivity and a stated geometry criterion, and report how many were tested and retained. Validate each reported state as a minimum using a vibrational calculation with no imaginary frequencies, or report a bounded failure with the exact missing validation and the best available stationary-point evidence. Advance a candidate to the final table only when its identity, charge/multiplicity, convergence, and dipole extraction are documented. The investigation is complete when all five fragment IDs have either a validated result or an explicit bounded failure, all attempted conformers are listed, and aggregate metrics are computed when a complete numeric comparison is available (or explicitly marked unavailable when it is not). Stop after that condition; do not expand to full acceptors or literature searching.

# Deliverables

Submit `report/results.json` and any supporting files referenced by it. The JSON must include one record per supplied fragment ID, calculation provenance, conformer/validation evidence, dipole magnitude when available, a comparison-ready summary, the independently reasoned polarity conclusion, and limitations, while conforming to the local `submission_schema.json`. A bounded-failure branch is allowed but must identify the affected fragment(s), missing evidence, and what remains supported.
