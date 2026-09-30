# Scientific objective

For the three explicitly identified neutral Cu2(AnCOO)4(4-RPy)2 molecular dimers (R = H, CH3, OCH3), independently determine the singlet–triplet exchange gap J (cm^-1), the triplet population at 300 K (%), and whether the substituent series exhibits a systematic relationship in the calculated coupling.

# Public inputs and scientific boundaries

Use `data/inputs/model_systems.json`, which uniquely identifies the three derivatives, component SMILES, paddlewheel assembly, charge, reference triplet multiplicity, target states, and units. Construct 3-D geometries from the connectivity. The boundary is the isolated dimer, not the periodic MOF or experimental measurement. Define the J sign convention and the energy-to-population expression used.

# Required scientific validation/investigation

For each named system, generate and deduplicate at least one valid geometry, establish a triplet reference, and calculate the lowest singlet and triplet energies with a defensible open-shell method. Record convergence, spin/state identity, and any stability or frequency check. Perform at least one justified sensitivity check and explain why the three-system coverage is sufficient for the stated relationship (or state what cannot be inferred). Completion requires traceable results for all three systems or a diagnostic bounded-failure record. Stop when all systems and the sensitivity check are covered; report limitations and alternative interpretations rather than inventing a discovery story.

# Completion and allowed outcomes

Submit a successful result only when all three named systems have the requested gap and
population plus the required validation records and series interpretation. If a system or the
sensitivity check cannot be completed after the attempted scope, submit the bounded-failure
branch with the covered systems, attempted calculations, diagnostics, and the specific missing
result; do not invent numeric values or placeholder structures.

# Deliverables

Submit `report/results.json` with per-system identity, geometry provenance, J, 300 K population, units, method, validation (including sign convention and population expression), coverage/status, and conclusion. A bounded-failure branch is valid only with attempted scope and diagnostics.
