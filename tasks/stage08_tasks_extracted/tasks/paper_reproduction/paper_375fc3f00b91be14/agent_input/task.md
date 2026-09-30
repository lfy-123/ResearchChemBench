# Scientific objective

Independently determine whether aqueous thermodynamic basicity changes between the defined E,E-PyDIG and Z,Z-PyDIG photoisomers, and quantify pKa(E,E), pKa(Z,Z), and ΔpKa = pKa(Z,Z) − pKa(E,E). Explain what the computed thermochemistry does and does not establish about a basicity-driven pH-switch application. No mechanism, candidate route or expected direction is supplied; formulate and discriminate plausible thermochemical explanations from your calculations.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that photoisomerization from E,E to Z,Z changes PyDIG's aqueous basicity through conformational and electronic reorganization, potentially producing a useful pH swing. Their interpretation is that the basicity difference may arise chiefly from altered relative stabilization of the neutral and singly protonated isomer families, rather than from a kinetic photochemical effect.

**Candidate route or mechanism.**
Treat the proposed explanation as a thermodynamic comparison of neutral and conjugate-acid E,E/Z,Z families. In particular, examine whether conformational free-energy differences, including possible destabilization of neutral Z,Z relative to its protonated form, can account for the isomer-dependent deprotonation free energy. Use the authors' comparison of low-energy solution conformers as one candidate state-selection hypothesis while retaining the broader conformational landscape for checking.

**Discriminating evidence.**
Discriminate the proposal with validated neutral and conjugate-acid conformers for each isomer, their relative free energies in an aqueous thermochemical cycle, and sensitivity to conformer coverage and state-selection choices. Frequency/minimum checks, preserved E,E/Z,Z and protonation identities, and an explicit comparison of neutral-versus-protonated contributions are the relevant evidence; the calculation bears on equilibrium basicity, not photochemical rates or CO2-transfer kinetics.

# Public inputs and scientific boundaries

Use `data/inputs/pydig_structures.json` as the authoritative identity for E,E-PyDIG and Z,Z-PyDIG neutral charge-0 singlets and their singly protonated charge+1 singlet conjugate acids. The proton is explicitly assigned in each record. `experimental_context.json` defines aqueous ambient-temperature context and the reversible isomer pair. The scored system is the isolated PyDIG molecule in water; do not add a host, explicit solvent molecules, GlyGly, or CO2. The claim concerns acid–base thermochemistry only, so do not infer excited-state behavior, CO2 kinetics, or engineering performance.

# Required scientific validation/investigation

Design and execute a reproducible investigation of conformers and thermochemical states. State candidate-generation, deduplication, optimization, frequency/minimum validation, E,E/Z,Z assignment, solvent and standard-state choices, proton and degeneracy conventions, and equations. Preserve identity and validation context for every retained candidate. Compare at least one plausible alternative explanation or sensitivity (for example conformer treatment, solvent model or proton bookkeeping) and explain its effect. Completion requires validated pKa estimates and ΔpKa with coverage and limitation evidence for both isomers, or a bounded-failure report naming completed states, diagnostics and next step. Stop at validated endpoint coverage plus sensitivity assessment, or at a reproducible resource/convergence boundary; report that boundary and do not invent a discovery story.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. Provide per-isomer pKa estimates, ΔpKa, candidate/state validation records, method rationale, sensitivity/coverage, and a final conclusion with limitations. A bounded-failure branch is allowed when honestly documented.
