# Scientific objective

For the fixed Cs/PEG-SrO model, determine how gas versus aqueous implicit solvation changes its electronic descriptors and whether the computed changes support a defensible statement about relative electronic stability and electrophilic reactivity. Compute dipole moment, HOMO, LUMO, gap, IP, EA, electronegativity, electrochemical potential, hardness, softness, electrophilicity, and Mulliken charges for oxygen XYZ rows 1, 4, and 6. Formulate the interpretation from the calculations and distinguish descriptor evidence from broader biological or catalytic claims.

# Public inputs and scientific boundaries

Use `data/inputs/cs_peg_sro.xyz` exactly as the canonical 12-atom, angstrom Cartesian model and `data/inputs/system_spec.json` for the neutral-singlet boundary, phases, atom ordering, and oxygen-row identities. The research object is an isolated cluster model; periodic solids, bulk composition, docking, experiments, and reaction pathways are outside scope. Choose and document an independent software/model-chemistry route and continuum-water treatment. Do not consult the paper, SI, general web, or unpinned external records.

# Required scientific validation/investigation

Verify the supplied structure, atom rows, charge, multiplicity, and coordinate integrity before calculation. Independently compute both phases, document settings and convergence or a bounded failure, extract every requested observable with units/signs, and verify descriptor formulae. Oxygen charges must retain row identity. Use the results to propose and discriminate at least one plausible interpretation of the phase change; support it with computed directionality and state what the model cannot establish. Completion requires two validated phase results and an evidence-linked conclusion, or a truthful bounded-failure branch listing attempted work and missing observables. Stop after identity/state checks, both phase calculations, extraction, comparison, and limitation analysis are complete; no candidate search or expansion to other structures is required.

# Deliverables

Write `report/results.json` and `report/methods_and_validation.md`, conforming to the local `submission_schema.json`. Include status, system identity, phase-specific methods/settings, all observables, oxygen-row charges, phase comparison, proposed interpretation, validation evidence, and limitations. A bounded-failure result must identify the failed phase/observable and attempted checks; do not fill missing scientific values with guesses.
