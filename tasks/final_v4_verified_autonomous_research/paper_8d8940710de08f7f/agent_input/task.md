# Scientific question

Which conformations of neutral SNaft and SAntr are energetically preferred in vacuum and methanol, and what molecular interactions and torsional accessibility explain their stability and flexibility?

# Input files

- `data/inputs/systems.json` gives the complete mapped graphs of SNaft (C16H14N2O2S) and SAntr (C20H16N2O2S), each neutral and singlet.
- `data/inputs/problem_facts.json` specifies the physical meaning of energies, populations, constrained configurations and interaction evidence. No experimental conformer populations or optimized conformers are supplied.

# Scope

Study the two complete molecules in vacuum and methanol separately. Define atom correspondence, conformational descriptors and the solvent representation. Relative energies must use a consistent reference within each molecule and medium. Distinguish electronic energy from Gibbs energy; specify temperature, standard state and thermal treatment for free energies. Ionization equilibria, crystal packing, biological activity and membrane transport are outside the question.

# Required results

1. For each molecule in each medium, identify the relevant conformational families, their relative energies in kcal/mol and the energetic preference supported by the calculations. Compare the preference across the two media, retaining genuinely unresolved small splittings.
2. For each molecule, explain the role of intramolecular contacts in its conformational stability using structural and electronic/interaction evidence. Distinguish a local interaction estimate from the total conformational energy difference.
3. For each molecule, determine what torsional access between conformational families is supported and whether the preferred geometry is conformationally locked. Give quantitative energetic/path evidence for the flexibility conclusion and its relation to the local contacts. Distinguish a sampled constrained energy profile from a verified transition-state barrier or rate.

Choose and justify the computational models and methods. Define families by their physical geometry, not by the number of starting structures. Evidence requirements follow the final claim; no fixed scan mesh, conformer count, analysis software or trajectory protocol is prescribed.

# Submission

Submit `report/results.json` and `report/report.md` under the supplied schema and guide, with native structures, energies, inputs/outputs and reproducible analyses linked to each final result. Only final scientific propositions are scored. Use the supplied inputs and general scientific/software documentation; private references and prior verification archives are not inputs.
