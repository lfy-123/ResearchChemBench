# Scientific objective

Independently determine how sodium/vacancy ordering in the supplied rhombohedral NASICON Na_xVTi(PO4)3 framework controls phase stability, sodium insertion voltage, and endpoint structural strain. Discover and discriminate plausible Na/vacancy configurations rather than assuming a favored ordering. Report compositions, unique structure identifiers, relaxed energies, formation energies, convex-hull membership, voltage plateaus, lattice parameters/volumes, and endpoint volume change.


## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that sodium insertion in Na_xVTi(PO4)3 can proceed through a sequence of stable composition states, producing multiple electrochemical plateaus, while involving successive changes in V and Ti redox activity. They also interpret the framework as retaining low structural strain between the desodiated and sodiated endpoints.

**Candidate route or mechanism.**
A useful proposed route to test is a sequence across the supplied compositions from x = 1 to x = 4 in which sodium/vacancy ordering selects successive stable states and the associated redox response progresses qualitatively through V4+/V3+, Ti4+/Ti3+, and V3+/V2+ regimes. Treat these as candidate explanations to compare against the enumerated orderings and computed phase energetics, rather than as assumed ground-state assignments.

**Discriminating evidence.**
Use duplicate-free ordering enumeration, relaxed relative and formation energies, convex-hull membership, and voltage differences between adjacent stable states to test the proposed sequence. Compare the relaxed endpoint lattice parameters and volumes to quantify strain, and use structural identity checks plus numerical convergence or cross-check tests to distinguish robust ordering and redox interpretations from artifacts of incomplete search or relaxation.

# Public inputs and scientific boundaries

Use every file under `data/inputs/`. `nasicon_seed.cif` is the supplied R-3c crystallographic seed: it identifies the Na1 6b and Na2 18e sites, V/Ti mixed 12c site, P 18e site and O 36f sites, with the displayed cell and fractional coordinates. Expand symmetry and resolve occupancies into explicit neutral Na_xVTi(PO4)3 candidates; state the expansion and atom-count convention. Investigate x = 1, 1.5, 2, 2.5, 3, 3.5 and 4. Use bulk bcc Na as the sodium reference and declare charge, spin/magnetic initialization, pseudopotentials/basis, functional, dispersion, correlation treatment, cutoff, k mesh and relaxation criteria. No paper, SI, general web or external result tables may be used.

# Required scientific validation/investigation

Define a finite candidate-generation rule for each x, including Na-site occupations and any framework ordering you choose to explore. Deduplicate by symmetry/structure comparison and retain a stable candidate ID and generation provenance. Relax each advanced candidate, document convergence or failure, and compare energies using one consistent normalization. Compute formation energies with the supplied formula, construct the lower convex hull across all required x, and derive voltages for every adjacent hull pair with the supplied formula. Relax or otherwise consistently evaluate x=1 and x=4 endpoints and calculate the signed percent volume change. Propose at least two chemically plausible ordering or phase-stability explanations where the data permit, then discriminate them using the computed energies, structures and validation tests. Completion requires either (a) all required compositions have at least one converged candidate, a hull and voltage/volume analysis, or (b) a bounded-failure report listing every missing state, attempted candidates, failure cause, and the strongest conclusion supported by completed states. Stop when the declared candidate-generation space is exhausted for each x or when a documented energy/structure convergence test shows no new distinct low-energy candidate under the chosen generation rule; report coverage and stopping rationale.

# Contract branch: if bounded failure occurs, set `completion_status` to `bounded_failure`, include `failure_report` with every missing state, attempted candidates and causes, and set unavailable phase, voltage, endpoint, hypothesis-comparison and final-conclusion fields to null. Do not fabricate values.

# Deliverables

Submit `report/results.json` and `report/methods.md`. `results.json` must contain candidate identities and validation status, phase/formation-energy records, hull membership, voltage plateau records, endpoint lattice/volume records, hypothesis comparison, completion status, limitations and a final conclusion. `methods.md` must make the calculation reproducible, including software, model choices, formulas, candidate generation/deduplication, convergence evidence and stopping rule. Numeric values must include units and energy normalization; do not silently omit failed or unsearched compositions.
