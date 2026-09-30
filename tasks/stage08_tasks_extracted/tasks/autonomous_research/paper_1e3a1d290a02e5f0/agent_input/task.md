# Scientific objective

Calculate and compare the neutral-singlet ground-state geometries, HOMO and LUMO energies, and internal hole reorganization energies of the three explicitly named fluorinated carbazole–diphenylamine HTMs JY1, JY2, and JY3. Form an evidence-based conclusion about how the defined fluorination patterns affect these molecular observables. Generate and test your own explanations for the computed differences.

# Public inputs and scientific boundaries

`data/inputs/molecules.json` is the complete system definition: each systematic name, formula, charge, multiplicity, identifier, and fluorine count is explicit. Build starting geometries yourself. The measured objects are isolated molecules only; do not add a host or solvent; do not score crystal packing, perovskite adsorption, optical spectra, hopping pathways, mobility, or device performance. Report energies in eV and retain atom identity/connectivity in every geometry artifact.

# Required scientific validation/investigation

Before calculation, formulate and justify a computational approach and any meaningful alternative route or validation strategy, comparing their scientific adequacy. For each named molecule, generate at least one connectivity-preserving 3-D starting structure, optimize a neutral singlet ground state, and compute a vibrational Hessian or equivalent minimum test. Advance only structures whose identity and electronic state are preserved and whose minimum test has no imaginary mode, or document a bounded technical failure. Extract HOMO/LUMO from each validated state. Compute internal hole reorganization energy from clearly documented neutral/cation adiabatic or four-point energies, defining the convention and all states used. Completion requires all three molecules to have either validated values or a bounded, technically justified failure record; a failed molecule must report attempted approaches and its reason rather than fabricated values. Stop after the three named systems and all required validation attempts are covered; do not expand to unlisted analogues. Report search coverage, convergence settings, software, model, conformer handling, failures, and limitations.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. Include per-molecule geometry identity, optimization/minimum evidence, HOMO/LUMO, λh (or an explicit bounded-failure branch), methods and an independently reasoned comparative conclusion.
