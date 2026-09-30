# Scientific objective

For the three explicitly identified neutral Cu2(AnCOO)4(4-RPy)2 molecular dimers (R = H, CH3, OCH3), independently determine the singlet–triplet exchange gap J (cm^-1), the triplet population at 300 K (%), and whether the substituent series exhibits a systematic relationship in the calculated coupling.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the electronics of the axial 4-substituted pyridines tune singlet–triplet magnetic exchange in these Cu(II) paddlewheel dimers, with more electron-donating substituents expected to strengthen antiferromagnetic coupling and modestly lower the thermally populated triplet fraction.

**Candidate route or mechanism.**
A useful candidate explanation is that substituent-dependent axial pyridine donation changes the electronic structure and Cu–Cu superexchange pathway while the anthracenecarboxylate paddlewheel framework remains the common bridge. Treat the three isolated dimers as a comparative series and test whether the coupling changes systematically across H, CH3, and OCH3.

**Discriminating evidence.**
Compare calculated singlet and triplet energies for every derivative using a defensible open-shell treatment and a common, explicitly stated sign convention. Use the triplet-reference structural approximation where appropriate, and distinguish the proposed trend with a justified sensitivity check involving the electronic-structure method, basis, geometry, or equivalent validation; evaluate the corresponding 300 K population from the stated thermodynamic expression.

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
