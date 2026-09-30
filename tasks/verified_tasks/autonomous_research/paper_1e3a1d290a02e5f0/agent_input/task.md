# Scientific objective

Calculate and compare the neutral-singlet ground-state geometries, HOMO and LUMO energies, and internal hole reorganization energies of the three explicitly named fluorinated carbazole–diphenylamine HTMs JY1, JY2, and JY3. Form an evidence-based conclusion about how the defined fluorination patterns affect these molecular observables; no author route or expected ranking is supplied.

# Public inputs and scientific boundaries

`data/inputs/molecules.json` is the complete system definition: each systematic name, formula, charge, multiplicity, identifier, and fluorine count is explicit. Build starting geometries yourself. The measured objects are isolated molecules only; do not score crystal packing, perovskite adsorption, optical spectra, hopping pathways, mobility, or device performance. Report energies in eV and retain atom identity/connectivity in every geometry artifact.

Numerical comparison context: the reference molecular orbital and reorganization calculations use B3P86/6-311G(d,p) for isolated molecules. This discloses the method-dependent comparison context, without prescribing starting geometries, software, search choices or outcomes. Other defensible methods remain allowed, with their method and quantity definitions reported for scientific comparability review; do not relabel a different quantity as the requested reorganization energy.

# Required scientific validation/investigation

Before calculation, formulate and justify a computational approach and any meaningful alternative route or validation strategy, comparing their scientific adequacy. For each named molecule, generate at least one connectivity-preserving 3-D starting structure, optimize a neutral singlet ground state, and compute a vibrational Hessian or equivalent minimum test. Advance only structures whose identity and electronic state are preserved and whose minimum test has no imaginary mode, or document a bounded technical failure. Extract HOMO/LUMO from each validated state. Compute internal hole reorganization energy from the documented neutral/cation reorganization cycle defined below, retaining all states used. Completion requires all three molecules to have either validated values or a bounded, technically justified failure record; a failed molecule must report attempted approaches and its reason rather than fabricated values. The required comparison covers the three named systems and their validation; additional trials are allowed but do not replace a missing primary result. Report search coverage, convergence settings, software, model, conformer handling, failures.

Use exactly three primary rows in `results`, in the explicit order JY1, JY2, JY3, and retain each `molecule_id`; put extra trials in `attempts`. The internal reorganization quantity compared here is λh = [E+(R0) − E+(R+)] + [E0(R+) − E0(R0)], with separately optimized neutral and cation geometries and cross-geometry energies. An equivalent algebraic evaluation is acceptable; a single adiabatic ionization energy is not this quantity. Other method-dependent observables must be labelled separately. A failed row may omit unavailable computational settings and successful properties while retaining identity, attempted methods and its actual failure reason.

Generic limitations or uncertainty prose is optional and unscored. Keep the required scientific identities, computed evidence, coverage and actual failure diagnostics. Additional scientifically motivated calculations are allowed and should be separated from the primary results; optional work not performed needs no disclaimer.

# Deliverables

Submit `report/results.json` conforming to the schema. Include per-molecule geometry identity, optimization/minimum evidence, HOMO/LUMO, λh (or an explicit bounded-failure branch), methods and an independently reasoned comparative conclusion.
