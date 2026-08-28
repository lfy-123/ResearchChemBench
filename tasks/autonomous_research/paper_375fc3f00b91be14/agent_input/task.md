# Scientific objective

Independently determine whether aqueous thermodynamic basicity changes between the defined E,E-PyDIG and Z,Z-PyDIG photoisomers, and quantify pKa(E,E), pKa(Z,Z), and ΔpKa = pKa(Z,Z) − pKa(E,E). Explain what the computed thermochemistry does and does not establish about a basicity-driven pH-switch application. No mechanism, candidate route or expected direction is supplied; formulate and discriminate plausible thermochemical explanations from your calculations.

# Public inputs and scientific boundaries

Use `data/inputs/pydig_structures.json` as the authoritative identity for E,E-PyDIG and Z,Z-PyDIG neutral charge-0 singlets and their singly protonated charge+1 singlet conjugate acids. The proton is explicitly assigned in each record. `experimental_context.json` defines only aqueous ambient-temperature context and the reversible isomer pair. The object is isolated PyDIG acid–base thermochemistry in water; explicit solvent, GlyGly, CO2 kinetics, excited states and engineering performance are excluded. Do not consult the paper, SI or general web.

# Required scientific validation/investigation

Design and execute a reproducible investigation of conformers and thermochemical states. State candidate-generation, deduplication, optimization, frequency/minimum validation, E,E/Z,Z assignment, solvent and standard-state choices, proton and degeneracy conventions, and equations. Preserve identity and validation context for every retained candidate. Compare at least one plausible alternative explanation or sensitivity (for example conformer treatment, solvent model or proton bookkeeping) and explain its effect. Completion requires validated pKa estimates and ΔpKa with coverage and limitation evidence for both isomers, or a bounded-failure report naming completed states, diagnostics and next step. Stop at validated endpoint coverage plus sensitivity assessment, or at a reproducible resource/convergence boundary; report that boundary and do not invent a discovery story.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Provide per-isomer pKa estimates, ΔpKa, candidate/state validation records, independent method rationale, sensitivity/coverage, and a final conclusion with limitations. A bounded-failure branch is allowed when honestly documented. Do not report private reference values.
