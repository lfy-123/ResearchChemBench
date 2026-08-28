# Scientific objective

For the supplied periodic AB, BA and AC Fe5GeTe2 bilayers, determine whether lateral interlayer displacement produces opposite polar magnetic states and quantify the switching barrier, out-of-plane polarization, and net magnetic moments. Establish the conclusion independently from calculations; do not presume a mechanism, state ordering, or sign of any result.

# Public inputs and scientific boundaries

Use `data/inputs/AB.vasp`, `BA.vasp`, and `AC.vasp`. Each is a periodic 16-atom Fe10Ge2Te4 bilayer with explicit lattice vectors and c-axis vacuum; `magnetic_initialization.json` defines the supplied A-type AFM starting pattern (parallel Fe1–Fe5, parallel Fe6–Fe10, opposite between layers). Measure total-energy differences along an AB-to-BA path, out-of-plane polarization relative to the supplied c axis, and total spin moment per cell. Choose and disclose computational methods and settings. Do not use the paper, SI, general web search, or hidden reference values. Transport, Curie temperature and unsupplied stackings are outside scope.

# Required scientific validation/investigation

Relax AB, BA and AC and report convergence. Explore and state at least one alternative magnetic ordering or an equivalent quantitative stability test for AB and AC. Generate a finite, explicitly described continuous AB-to-BA path, deduplicate equivalent images, and identify the maximum relative energy with its state identity; test whether AC is on or near that path. Validate energy symmetry, polarization sign relation, magnetic-moment sign relation, and AC compensation using reported uncertainties. Perform at least one sensitivity check for each observable. Completion means all three structures, a defined path, all requested observables, and uncertainty/limitation statements are reported. Stop once those checks are converged; otherwise stop at a documented bounded scope and use the bounded-failure branch with partial results and a scientific limitation.

# Deliverables

Submit `report/results.json` matching `submission_schema.json`. Include methods, object identities, convergence evidence, magnetic test, path image table, barrier, signed polarizations and moments, uncertainties, evidence-based conclusion and limitations. Every candidate path state must retain its identity and energy context. A bounded-failure submission must include attempted scope, available partial observables, failure reason and limitation.
