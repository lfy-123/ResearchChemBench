# Scientific objective

Determine computationally how converting the supplied Schiff base HL from its neutral form to its singly protonated azomethine-N form changes frontier-orbital energetics and localization, and assess whether that electronic change can account for an acid-induced red shift. Report validated optimized structures, HOMO/LUMO energies, gaps in eV, localization evidence, and a bounded conclusion. Do not assume a mechanism beyond what your calculations support.

# Public inputs and scientific boundaries

Use `data/inputs/hl_system.json`. It uniquely defines E-HL and the protonated azomethine-N state (the N directly bonded to the -CH- group in -CH=N-N=C(fluorenylidene)), including SMILES, connectivity, stereochemistry, charge and singlet multiplicity. CCDC 2483407 is provenance for an optional crystal geometry only; no CIF is supplied or required, and CCDC database retrieval is not required or scored. Generate the evaluated isolated-molecule geometries from the supplied SMILES. The model boundary is isolated molecules without explicit solvent, acid, counterion or crystal packing. Observables are optimized geometry, HOMO/LUMO energies, HOMO–LUMO gap in eV, and qualitative orbital-density localization. The experimental boundary is only the question of support for an acid-induced red shift; do not claim a spectrum from a ground-state gap alone.

# Required scientific validation/investigation

Select and justify an independent computational route. Build and validate at least one geometry for each state, verify protonation, charge and multiplicity, and perform an orbital calculation on each stationary/converged structure. State how orbitals were assigned and units converted. Compare the states and discriminate plausible explanations using the computed evidence; separate direct results from interpretation. Completion requires validated results for both states or a bounded-failure report with attempted scope, failure cause and limitation. Stop after both states are validated and additional reasonable starting geometries no longer alter the qualitative comparison, or when a documented resource/software barrier prevents that; report coverage and stopping basis.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, with method, per-state validation and orbital results, comparison, independently reasoned conclusion, limitations and any bounded failure.
