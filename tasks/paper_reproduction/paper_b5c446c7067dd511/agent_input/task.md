# Scientific objective

For the four fixed neutral molecules Ph-mP, Na-mP, An-mP and Py-mP, independently plan and execute calculations that test the authors' qualitative hypothesis that these donor–acceptor emitters have hybridized local/charge-transfer excited states and can access higher-triplet-to-singlet (“hot”) pathways. Report vertical singlet/triplet energies, ΔE(S1−T1), and state-character evidence. Do not assume the authors' numerical results or computational settings.

# Public inputs and scientific boundaries

Use `data/inputs/molecular_identities.json`. It uniquely defines each connectivity, formula, terminal group, neutral charge (0), singlet multiplicity (1), and the three fragments for optional charge-transfer analysis; each molecule also has a machine-readable connectivity SMILES so structure generation does not depend on a name-resolution service. The SMILES are fixed connectivity representations, not source coordinates or result-bearing conformers. The boundary is an isolated gas-phase molecule; solvent, crystal packing, aggregation, and experimental PL measurements are outside the required calculation. Starting 3D conformers may be generated independently. The author hypothesis is public only as a qualitative hypothesis; no author numerical result, winning conformer, method, or ordered protocol is supplied.

# Required scientific validation/investigation

For every named molecule, generate and retain at least one chemically valid starting structure, optimize it with a stated defensible method, and document convergence and the conformer/initial-geometry choice. Compute and identify a consistent set of low-lying singlet and triplet vertical states, including S1/T1 and enough higher states to test any proposed hot channel. Validate state labels, units, charge/multiplicity, and arithmetic for ΔE(S1−T1). If using NTO/fragment analysis, bind each result to a molecule and state and report the fragment definition. Compare plausible interpretations of mixed LE/CT versus predominantly LE or CT character. Completion requires all four molecules to have either a validated result set or a bounded, explicitly documented failure; for a failed molecule submit the failure reason and coverage note instead of fabricated energies or character. Stop when all four systems and the chosen state set have been validated, or when a reproducible computational limitation prevents completion; report coverage and the limitation rather than silently substituting data.

# Deliverables

Submit `report/results.json` and `report/methods_and_validation.md`. The JSON must preserve molecule identity and per-state context, include numerical energies where computed, gap arithmetic, validation status/evidence, a final mechanism conclusion, and limitations. The markdown must describe methods, convergence, structure generation, state assignment, validation, and stopping/coverage.
