# Scientific objective

For the four fixed neutral phenanthroimidazole donor–acceptor molecules Ph-mP, Na-mP, An-mP and Py-mP, independently determine their low-lying singlet/triplet electronic structure and whether the available calculations support a mixed local-excitation/charge-transfer description and a higher-triplet (“hot”) pathway. Formulate and discriminate plausible explanations from your calculations; no author route or mechanism is provided.

# Public inputs and scientific boundaries

Use `data/inputs/molecular_identities.json`. It uniquely defines each connectivity, formula, terminal group, neutral charge (0), singlet multiplicity (1), and three fragments for optional charge-transfer analysis. The boundary is an isolated gas-phase molecule; solvent, crystal packing, aggregation, and experimental PL measurements are outside the required calculation. Starting 3D conformers and computational methods are investigator choices, but must be stated and justified. Do not treat the internal names as structures beyond the supplied systematic names and attachments.

# Required scientific validation/investigation

For each of the four named molecules, generate at least one chemically valid structure and optimize it with a stated method; document convergence and structure-generation choices. Compute a consistent low-lying singlet/triplet state set including S1/T1 and enough higher states to test candidate explanations. Validate charge, multiplicity, state labels, units, gap arithmetic, and per-molecule identity. Use NTO/fragment analysis or another explicit state-character diagnostic when available, binding every diagnostic to its molecule and state. Compare at least two plausible interpretations when the data permit, state what evidence discriminates them, and report uncertainty. Completion requires validated coverage of all four systems or a bounded, reproducible limitation for any missing system; for a limited molecule submit the failure reason and coverage note rather than fabricated numerical or structural results. Stop when that condition is met and no untested calculation is expected to change the stated conclusion within the chosen scope.

# Deliverables

Submit `report/results.json` and `report/methods_and_validation.md`. The JSON must contain per-molecule state results and validation context, the independently derived gap values, candidate interpretations and discriminating evidence, a final conclusion, and limitations. The markdown must make the search scope, method choices, validation, coverage, stopping decision, and reproducibility clear.
