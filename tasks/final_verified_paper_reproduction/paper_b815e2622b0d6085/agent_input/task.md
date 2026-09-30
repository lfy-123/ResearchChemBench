# Scientific objective

Test the authors' structural/electronic interpretation across three isostructural pyridinium lead bromide crystals (Cl, Br, I). Distinguish fundamental and framework-related interband electronic gaps, determine their separate trends and band character, and give an evidence-bounded structural explanation.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that substituent-dependent lattice geometry, particularly the crystallographic a-axis, is associated with the band-gap trend. They also discuss possible iodine/organic orbital mixing at the band edges.

**Candidate route or mechanism.**
For this solid-state comparison, test whether changes in the a-axis and related lattice geometry track the gap across the three isostructural crystals, and whether iodine-derived and organic states contribute differently at the band edges. Treat these as candidate explanations to compare with alternatives supported by the calculations.

**Discriminating evidence.**
Use converged periodic band structures together with projected density of states or orbital projections to locate the edges and assess their character. Compare a-axis (or a precisely defined structural proxy) against the computed gaps, while checking other structural and orbital descriptors and distinguishing direct parent-cell relativistic calculations from validated approximations.

# Public inputs and scientific boundaries

Use `data/inputs/crystal_records.json`, `data/inputs/electronic_observables.json` and the three supplied CIFs: CCDC 2499860 (Cl), 2499862 (Br), 2499861 (I). These are the 300 K P21/c, Z=4 experimental parent cells, not optimized computed answers. Preserve cell, coordinates, occupancy, composition and protonation during deterministic periodic conversion; do not generate substitute crystals. Each periodic cell is neutral. State and consistently apply spin and pseudopotential/basis choices. No database retrieval is required.

There are distinct observables: (1) the fundamental gap to the lowest unoccupied state of any character; (2) the component-resolved electronic gap to the lowest defensibly identified Pb-p-bearing inorganic-framework conduction manifold; and (3) the minimum same-k gap for each set. The second is not automatically an optical onset. Use the public definitions, inspect both organic and inorganic components, and derive their identities/order from calculations. A carbon-bound ring Br is organic, unlike chain bromides. Never select a band from its ordinal number or a desired energy.

The comparable primary branch is HSE06 (25% exact exchange, screening 0.2 A^-1), scalar-relativistic without SOC, at the supplied parent geometry. Choose your exploration and convergence strategy independently; other methods and optional SOC calculations/estimates must be reported separately. Do not read paper/SI, final computed band results, reference archives or evaluator values. No target energy, winning trend or final orbital assignment is supplied.

# Required scientific validation/investigation

For each crystal, document electronic convergence, occupations, spin, sampling/path and potentials/basis. Determine the fundamental edges without excluding any low unoccupied bands. Independently identify candidate organic and inorganic conduction manifolds with normalized atom/orbital projections or equivalent wavefunction evidence, retaining component atom lists and all lower candidate states. Use the target-independent criterion in `electronic_observables.json`: the lowest tracked manifold with Pb-p as its leading component/element/angular-momentum group at the edge. Follow states across k and discuss mixed-state sensitivity; a hybridized manifold need not have over 50% inorganic weight at every k. Nonzero Pb weight alone is insufficient. If the framework assignment cannot be established, report its candidate values and ambiguity rather than pretending success.

For each assigned set, separately calculate the independently extremized edge gap and the minimum same-k gap. Report fractional reciprocal edge coordinates, degenerate edge sets, spin and directness within the sampled domain; non-Gamma does not mean indirect. Demonstrate at least one numerical-stability comparison for each reported quantity with its signed change and nonnegative absolute change. Finite meshes or paths do not by themselves establish exact full-Brillouin-zone extrema.

Test a defined structural descriptor against the cross-crystal electronic results with explicit sign/identity and plausible alternatives. Interpret each gap's trend separately; do not substitute a framework trend for the fundamental trend. Optical allowedness remains `not_established` unless matrix-element or explicit symmetry/selection-rule evidence exists; projections alone do not prove it. Optional SOC must be distinguished from the primary no-SOC comparison and from reduced-model approximations. No extra optical or SOC calculation is compulsory merely to fill a missing claim.

Completion requires per-crystal validated primary fundamental and assigned framework electronic observables, stability and a bounded interpretation. Otherwise report the exact incomplete object/quantity, attempted evidence, reason and scientific consequence using `bounded_failure`; a well-documented failure is not a successful numerical result. Stop at the documented coverage/resource boundary without fabricating energies, assignments or claims.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, with separately named `scalar_relativistic.fundamental` and `scalar_relativistic.framework_interband` records, same-k gaps, mapped edges, assignment/stability evidence, optical-claim status, optional separate SOC results, structural comparison and limitations. Include cited input/output and projection/band artifacts. Do not use a single ambiguous `gap_eV` at the crystal-record level.
