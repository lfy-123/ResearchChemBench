# Scientific question

How do molecular geometry and electronic structure control the competing thermal rearrangements of dibutadienylcyclopropane 3a?

# Input files

- `data/inputs/systems.json` defines the complete atom-mapped C11H14 graph and stereochemistry of neutral singlet 3a (25 atoms).
- `data/inputs/observations.json` states the available observational context; no measured rate or product distribution is supplied.
- `data/inputs/source_facts.json` defines the molecular and thermodynamic scope.

# Scope

Compare the [3,3] and [5,5] rearrangements in double-boat and double-chair geometries for this full molecule. These are candidate comparisons, not assignments of the favored route or its mechanism. Use an isolated-molecule model and define the electronic state, temperature, standard state and free-energy treatment. Reference all four forward Gibbs barriers to the same lowest reactant conformer established by your investigation, including any conformational preparation cost. Other bridged scaffolds, substituted derivatives and quantitative trajectory branching are outside this task.

# Required results

1. Determine the four forward Gibbs activation barriers in kcal/mol and the resulting static pathway preference. Identify the structures, bond changes and endpoint identities needed to make the barriers physically comparable. Distinguish electronic energy, free energy and a barrier relative to a higher-energy reactant conformer.
2. For each double-boat channel, determine the bond reorganization and product stereochemistry, and whether a concerted or stepwise account and closed-shell or open-shell character is supported. Substantiate the mechanism with connectivity and electronic evidence appropriate to that claim.
3. Explain the boat/chair barrier differences using the molecular organization and changes in geometry. Support the explanation with quantitative structural and energetic comparisons; distinguish an observed distortion from a separately established strain-energy decomposition.
4. Determine what the calculated forward pathways imply about reverse rearrangements. Distinguish an actual connected local product from a separately optimized lower-energy product conformer or stereoisomer. State which reverse claims are supported by those identities and references, and why a finite static comparison does or does not establish rates or product branching.

Choose and justify the computational methods and investigation. No fixed conformer count, path-search algorithm, electronic diagnostic or calculation sequence is prescribed. The evidence must establish the physical claims actually made.

# Submission

Submit `report/results.json` and `report/report.md` using the supplied schema and guide. Link final results to native inputs/outputs, mapped structures and reproducible analyses. Only final scientific propositions are scored. Use supplied inputs and general scientific/software documentation; private references and prior verification archives are not inputs.
