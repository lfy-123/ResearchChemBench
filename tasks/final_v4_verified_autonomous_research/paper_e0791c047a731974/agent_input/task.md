# Scientific question

What molecular electronic evidence can explain the different triplet sensitization behavior of IR780, Cy1 and Cy2, and what does it establish about their energetic compatibility with rubrene in chloroform?

# Input files

- `data/inputs/problem_context.json` supplies the observed triplet-yield summaries, emission context, solution conditions and data limitations. These observations are facts to explain, not predictions to reproduce by quotation.
- The four `data/inputs/*_identity.json` files supply complete atom-indexed graphs, mapped SMILES, formulas and charges for IR780 (C36H44ClN2+), Cy1 (C34H38ClI2N2+), Cy2 (C27H29N2O2Se2+) and neutral rubrene (C42H28). Construct and justify geometries from these identities.

# Scope

Use the complete molecules without counterions. The experimental mixtures contain 10 μM sensitizer and 1.5 mM rubrene in argon-saturated chloroform. Relate molecular calculations to this context without treating them as measurements of the full solution system. The sensitizers also differ in molecular framework; they are not an otherwise identical atom-substitution series.

The question concerns low-lying molecular electronic states and donor–acceptor energy compatibility. Cy3, films, the full upconversion mechanism, absolute ISC or transfer rates and prediction of upconversion efficiency are outside the required results. Choose appropriate electronic models and heavy-element treatments, and state their applicability.

# Required results

1. Establish a state-resolved energy diagram for each sensitizer: vertical S1, T1 and T2 excitation energies at its S0 minimum, in eV relative to the electronic S0 energy at that same geometry. Identify the states and distinguish these energies from relaxed triplet gaps and experimental absorption maxima.
2. Determine the electronic adiabatic T1 gap for each of the four molecules, in eV: the electronic energy difference between separately relaxed T1 and S0 minima in the same solvent treatment. Report this electronic quantity separately from any zero-point or thermal correction.
3. Explain the sensitization contrast using newly calculated molecular electronic evidence. Assess what the excited-state character and heavy-element involvement imply, and whether the relative singlet–triplet energy gaps alone account for the supplied contrast. Distinguish electronic participation, molecular coupling and kinetic rates; identify which causal inferences your evidence supports.
4. For each sensitizer, calculate the signed donor-minus-rubrene adiabatic triplet energy difference under matched definitions. Explain the resulting energy compatibility, compare the three margins, and assess the sensitivity of that conclusion to the energy convention and method limitations. State what the comparison can establish about transfer in solution; do not assume cancellation of donor and acceptor errors.

# Submission

Submit `report/results.json` and `report/report.md` under the schema and guide. Link actual native calculations and reproducible analyses supporting the energy diagram, electronic explanation and donor–acceptor inference. State molecular identity, geometry, charge, state, solvent and energy reference for each result. A copied observation or target is not computational evidence; report unresolved results and their specific limitations.
