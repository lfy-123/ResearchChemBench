# Scientific objective

For the four fixed neutral molecules Ph-mP, Na-mP, An-mP and Py-mP, independently plan and execute calculations that test the authors' qualitative hypothesis that these donor–acceptor emitters have hybridized local/charge-transfer excited states and can access higher-triplet-to-singlet (“hot”) pathways. Report vertical singlet/triplet energies, ΔE(S1−T1), and state-character evidence. Do not assume the authors' numerical results or computational settings.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that these donor–acceptor emitters possess hybridized local-excitation and intramolecular charge-transfer character. They further propose that triplet excitons may be harvested through higher triplet states rather than only the lowest-triplet-to-lowest-singlet channel.

**Candidate route or mechanism.**
A candidate explanation is an HLCT-like pathway in which a higher triplet state with mixed local and charge-transfer character provides access to a singlet state, competing with a conventional T1-to-S1 route. Compare this with predominantly local or predominantly charge-transfer assignments and with pathways restricted to the lowest triplet.

**Discriminating evidence.**
Use vertical singlet/triplet energies, S1/T1 gap arithmetic, and state-character diagnostics such as NTOs or fragment-resolved charge analysis. Compare hole–electron overlap with donor-to-terminal-fragment separation for the relevant singlet and nearby higher triplet states, keeping molecule and state labels attached to every diagnostic.

# Public inputs and scientific boundaries

Use `data/inputs/molecular_identities.json`. It uniquely defines each connectivity, formula, terminal group, neutral charge (0), singlet multiplicity (1), and the three fragments that can be used for the required state-character analysis; each molecule also has a machine-readable connectivity SMILES so structure generation does not depend on a name-resolution service. The SMILES are fixed connectivity representations, not source coordinates or result-bearing conformers. The boundary is an isolated gas-phase molecule; solvent, crystal packing, aggregation, and experimental PL measurements are outside the required calculation. Starting 3D conformers may be generated independently. The author hypothesis is public only as a qualitative hypothesis; no author numerical result, winning conformer, method, or ordered protocol is supplied.

For each molecule, identify the relevant low singlet and nearby triplet roots and explain the energy-based choice of the compared Tn. Retain molecule, spin, state index and geometry for the corresponding NTO, IFCT or equivalent spatial analysis. A claim of mixed LE/CT within one electronic state requires evidence for both components in that same state; a CT-like S1 plus an LE-like T1 is not by itself a same-state decomposition. SOC and RISC rates are not required observables.

# Required scientific validation/investigation

For every named molecule, generate and retain at least one chemically valid starting structure, optimize it with a stated defensible method, and document convergence and the conformer/initial-geometry choice. Compute and identify a consistent set of low-lying singlet and triplet vertical states, including S1/T1 and enough higher states to test any proposed hot channel. Validate state labels, units, charge/multiplicity, and arithmetic for ΔE(S1−T1). Provide NTO/fragment analysis or equivalent spatial evidence for the relevant singlet and nearby Tn states; bind each result to its molecule and state and report any fragment definition. Compare plausible interpretations of mixed LE/CT versus predominantly LE or CT character. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` and `report/methods_and_validation.md`. The JSON must preserve molecule identity and per-state context, include numerical energies where computed, gap arithmetic, validation status/evidence, a final mechanism conclusion. The markdown must describe methods, convergence, structure generation, state assignment, validation and the states actually analyzed.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
