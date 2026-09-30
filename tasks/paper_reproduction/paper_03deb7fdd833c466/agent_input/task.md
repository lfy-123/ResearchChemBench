# Scientific objective

Independently plan and execute calculations on the supplied HL pair to test the authors' qualitative hypothesis that protonation of the azomethine nitrogen changes frontier-orbital energetics and localization in a way relevant to acid-induced red-shifted fluorescence. Report the optimized neutral singlet HL and singly protonated singlet HL structures, HOMO and LUMO energies, gaps in eV, localization evidence, and a bounded interpretation. The author hypothesis is only qualitative; do not assume the direction or magnitude of any result or a winning computational protocol.

# Public inputs and scientific boundaries

Use `data/inputs/hl_system.json`. HL is the explicitly defined E Schiff base in that file; its SMILES, connectivity, stereochemistry, neutral charge and singlet multiplicity are fixed. The second state is the same connectivity with one proton on the aldehyde-derived azomethine N directly bonded to the -CH- group in -CH=N-N=C(fluorenylidene), charge +1 and singlet multiplicity. CCDC 2483407 is provenance for an optional crystal geometry only; no CIF is supplied or required, and CCDC database retrieval is not required or scored. Generate the evaluated isolated-molecule geometries from the supplied SMILES. No solvent, acid, counterion or crystal packing is required. The measured quantities are converged optimized geometries, HOMO/LUMO energies and their difference in eV, plus qualitative spatial localization. Do not use the paper, SI or general web as a source of hidden answers.

# Required scientific validation/investigation

Choose and justify an independent electronic-structure route. Generate at least one chemically intact starting geometry per state, preserve state identity and protonation, and document charge/multiplicity. A result is advanced only after an optimization convergence/frequency or equivalent stationarity check and an orbital calculation on the validated geometry. Extract HOMO and LUMO unambiguously and state sign/unit conventions. Compare both states, report any alternate conformers or failed jobs, and explain whether the observed gap/localization change supports the qualitative hypothesis. Completion requires either validated results for both states or a truthful bounded-failure report containing the attempted scope, failure cause, and the most defensible limitation. Stop when both states have validated results and further reasonable starting-geometry trials no longer change the qualitative comparison, or when resources/software prevent that test; report the stopping basis and coverage.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method, state-specific validation, orbital energies/gaps, localization observations, comparison, conclusion, limitations, and any bounded failure. Values must be your calculations, not copied reference values.
