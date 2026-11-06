# Scientific question

How do molecular geometry and electronic structure control the competing thermal rearrangements of dibutadienylcyclopropane 3a?

# Input files

- `data/inputs/systems.json` defines the complete atom-mapped C11H14 graph and stereochemistry of neutral singlet 3a (25 atoms).
- `data/inputs/observations.json` states the available observational context; no measured rate or product distribution is supplied.
- `data/inputs/source_facts.json` defines the molecular and thermodynamic scope.

# Scope

Compare the [3,3] and [5,5] rearrangements in double-boat and double-chair geometries for this full molecule. These are candidate comparisons, not assignments of the favored route or its mechanism. Use an isolated-molecule model and define the electronic state, temperature, standard state and free-energy treatment. Reference all four forward Gibbs barriers to the same lowest reactant conformer established by your investigation, including any conformational preparation cost. Other bridged scaffolds, substituted derivatives and quantitative trajectory branching are outside this task.

# Disclosed reproduction baseline

Main p4 Figure 5 and SI p2 Figure S1 report double-boat [3,3]/[5,5] forward Gibbs barriers of 23.5/26.2 kcal/mol and double-chair barriers of 38.2/36.9 kcal/mol. The author attributes the comparison to cyclopropane strain and geometric organization. The baseline is Gaussian 16, ωB97X-D/def2-SVP optimization/frequencies and def2-TZVPP single-point energies, with xTB-CREST conformer sampling and GoodVibes Grimme quasi-RRHO entropy corrections (SI p6). The reviewed methods do not uniquely specify thermochemical temperature or low-frequency cutoff; declare and justify those choices. Wavefunction stability and unrestricted calculations address proposed radical character. Solvent comparisons in SI p5 concern other scaffolds. The paper's dynamics, pancake bonding and negative-activation-energy examples for those systems are outside this 3a question.

# Required results

1. Determine the four forward Gibbs activation barriers in kcal/mol and the resulting static pathway preference. Identify the structures, bond changes and endpoint identities needed to make the barriers physically comparable. Distinguish electronic energy, free energy and a barrier relative to a higher-energy reactant conformer.
2. For each double-boat channel, determine the bond reorganization and product stereochemistry, and whether a concerted or stepwise account and closed-shell or open-shell character is supported. Substantiate the mechanism with connectivity and electronic evidence appropriate to that claim.
3. Explain the boat/chair barrier differences using the molecular organization and changes in geometry. Support the explanation with quantitative structural and energetic comparisons; distinguish an observed distortion from a separately established strain-energy decomposition.
4. Determine what the calculated forward pathways imply about reverse rearrangements. Distinguish an actual connected local product from a separately optimized lower-energy product conformer or stereoisomer. State which reverse claims are supported by those identities and references, and why a finite static comparison does or does not establish rates or product branching.

Reproduce and assess the disclosed baseline, or justify physically comparable substitutions and their consequences. No fixed conformer count, path-search algorithm, electronic diagnostic or calculation sequence is prescribed. The evidence must establish the physical claims actually made.

# Submission

Submit `report/results.json` and `report/report.md` using the supplied schema and guide. Link final results to native inputs/outputs, mapped structures and reproducible analyses. Only final scientific propositions are scored. Use supplied inputs and general scientific/software documentation; private references and prior verification archives are not inputs.
