# Scientific question

How does replacing the two axial pyridines by 4-methylpyridine or 4-methoxypyridine affect magnetic exchange in neutral Cu2(AnCOO)4(4-RPy)2 dimers? Determine the exchange values, whether the substitution differences are resolved, and what electronic explanation the molecular evidence supports.

# Input files

- `data/inputs/molecular_identities.json` specifies the three axial ligands, four 9-anthracenecarboxylate bridges, Cu2 paddlewheel connectivity and charge. It defines molecular identity, not an optimized structure or spin ground state.
- `data/inputs/problem_context.json` gives the question, molecular boundary and input limitations.

# Scope

Study the three complete, neutral molecular dimers with four anionic bridges and two axial ligands. Construct and validate the geometries and electronic states needed for the comparison. Define exchange as J=E(S)−E(T) in cm^-1, or explicitly convert an equivalent Hamiltonian convention. State the geometry, environment and energy reference; compare the three members under matched conditions. The molecular model does not include a bulk lattice. No material thermochromism, photoconversion, thermal population curve or bulk magnetic ordering is required.

# Required results

1. Calculate J for each of H, Me and OMe and determine the relative singlet/triplet energies and electronic character from actual state-resolved evidence.
2. Determine J(Me)−J(H) and J(OMe)−J(Me), reporting whether each signed difference is resolved relative to demonstrated numerical and state ambiguity. Absolute-J agreement alone cannot establish a small differential effect.
3. Explain the substitution dependence using the calculated coupled-state electronic character. Identify what the evidence supports about ligand-to-core association and which geometric/electronic contributions remain inseparable. An exchange ranking alone is insufficient as an explanation.

Choose the research methods independently. Use the supplied inputs and general scientific/software documentation.

# Submission

Submit `report/results.json` and `report/report.md` using the supplied schema and guide. Link the genuine inputs, outputs and analysis supporting each conclusion; evidence requirements should match the claim. Report incomplete or unresolved work explicitly. Intermediate calculation completion earns no independent points.
