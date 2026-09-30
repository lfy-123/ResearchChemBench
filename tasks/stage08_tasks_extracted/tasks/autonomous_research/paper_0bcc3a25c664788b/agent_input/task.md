# Scientific objective

Using the six supplied TPAAN molecular systems, determine computationally how substituent identity (OMe, H, or CHO) and solvent identity (n-hexane or chloroform) affect the S1 and T1 electronic energies. Develop and discriminate plausible explanations for any differing sensitivity of singlet and triplet states from your calculations; no author route or mechanism is supplied. The result must distinguish direct computed observables from interpretation.

# Public inputs and scientific boundaries

The directory `data/inputs/geometries` contains six uniquely named XYZ files. Each file identifies one molecule, one solvent label, and a neutral singlet S0 starting structure; coordinates are in ångström and atom order is fixed within each file. The complete matrix is TPAAN-OMe, TPAAN-H, and TPAAN-CHO in n-hexane and chloroform. Study the isolated molecule with a continuum representation of the named solvent; exclude explicit solvent molecules, sensitizers, aggregates, counterions, and experimental spectra. Report relaxed S1→S0 and S0-geometry S0→T1 energies in eV, together with oscillator strength and state/transition character when available. Choose the computational method and validation diagnostics independently.

# Required scientific validation/investigation

Attempt all six named cases and state the hypotheses you considered before selecting the explanation supported by the results. Record charge/multiplicity, geometry and state used for each observable, solvent treatment, convergence evidence, state identity, and diagnostics that distinguish the requested states from nearby states. Compare the six cases using an explicit table or equivalent structured analysis, and separate numerical results from mechanistic interpretation. Completion requires six validated pairs or a bounded-failure report naming each failed case, evidence for failure, and coverage of the remaining cases. Stop after the six-case matrix has been attempted and every successful record has a validation decision; do not search additional compounds or solvents.

# Deliverables

Write `report/results.json` following `submission_schema.json`. Include all six case IDs, successful numerical observables with units, per-case validation evidence, the hypotheses considered and discriminating observations, and a final conclusion about substituent and solvent sensitivity. If a calculation fails, use the bounded-failure branch with case-specific limitations; do not invent a value.
