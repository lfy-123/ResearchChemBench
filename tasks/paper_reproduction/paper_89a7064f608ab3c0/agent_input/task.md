# Scientific objective

Determine computationally whether the oxidative radical-cation cycloreversion of the supplied BN-benzvalene radical cation [2a]•+ can proceed through the authors' proposed qualitative route: first C5-C6 bond cleavage to a prefulvene-like Int-1, then C3-C4 cleavage to Int-2, followed by reduction to the known C4-aryl 1,2-azaborine product 3a. Quantify the Gibbs activation free energies for the two sequential cleavage events and test the proposed C4-over-C5 selectivity against the alternative C3-C6 cleavage route. The research objects are the named states and pathways, not an assumed paper geometry.

# Public inputs and scientific boundaries

`data/inputs/radical_cation_2a.xyz` is a 65-atom Cartesian structure for [2a]•+, with charge +1 and multiplicity 2. `data/inputs/product_3a.xyz` is the known C4-aryl product endpoint (neutral singlet) and is provided for connectivity/product identity only. Coordinates are in Å; element symbols identify atoms, but no paper atom numbering is required. The calculation boundary is the listed molecular system in gas phase or an explicitly reported solvent model, with electronic energies, vibrational thermochemistry, relative Gibbs energies, and transition-state connectivity as observables. Do not use the paper, SI or general web as an input source.

# Required scientific validation/investigation

Independently generate and examine candidate structures for [2a]•+, Int-1, TS-1, TS-2, Int-2, 3a, and the alternative C3-C6 TS. Deduplicate candidates by connectivity and report which candidates were advanced. Validate every claimed minimum with a frequency calculation showing zero imaginary modes and every claimed TS with exactly one chemically relevant imaginary mode. Validate TS-1 and TS-2 connectivity with IRC or an explicitly justified equivalent two-sided displacement/connectivity analysis. Define completion as having at least one validated candidate for each required state or a documented bounded failure, with all energies and validation evidence traceable to submitted files. Stop when this condition is met; if it cannot be met, stop after reporting the attempted candidate generation, failed validations and the limiting resource/method issue. Report coverage and sensitivity checks rather than silently selecting a favorable structure.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus referenced calculation logs/geometries and a concise human-readable report. The JSON must include the selected candidate identities, Gibbs barriers (or a truthful bounded-failure branch), C4/C5 pathway comparison, frequency counts, connectivity checks, computational method/solvent/temperature, and a final conclusion tied to evidence paths. A result is complete only when every required JSON field is populated or the bounded-failure branch truthfully documents the missing state and limitation.
