# Scientific objective

Determine the singlet–triplet exchange gap J (cm^-1) and the triplet population at 300 K (%) for the three explicitly identified neutral Cu2(AnCOO)4(4-RPy)2 molecular dimers (R = H, CH3, OCH3). In this reproduction mode, the authors' qualitative hypothesis is that changing pyridine electronics changes Cu–Cu exchange; independently plan and perform calculations that test that hypothesis. Do not assume a paper numerical result.

# Public inputs and scientific boundaries

Use `data/inputs/model_systems.json`. It uniquely identifies each system, ligand SMILES, assembly, charge, reference triplet multiplicity, target states, and units. Construct 3-D geometries from the supplied connectivity. The boundary is the isolated dimer, not the periodic MOF or experiment. Report the sign convention used for J and define how the singlet–triplet energy difference maps to it.

# Required scientific validation/investigation

For each of the three named systems, generate and deduplicate at least one chemically valid geometry, optimize or otherwise establish a defensible triplet reference, and calculate the lowest singlet and triplet energies with a method capable of treating the open-shell dimer. Record convergence, spin/state identity, and any imaginary-frequency or stability check performed. Validate at least one methodological sensitivity (basis, functional, geometry, or equivalent justified check). Completion requires all three systems having a traceable gap and population or a documented bounded failure with diagnostic evidence. Stop after all three systems are covered and the sensitivity check is complete; report any unresolved limitation.

# Completion and allowed outcomes

Submit a successful result only when all three named systems have the requested gap and
population plus the required validation records. If a system or the sensitivity check cannot
be completed after the attempted scope, submit the bounded-failure branch with the covered
systems, attempted calculations, diagnostics, and the specific missing result; do not invent
numeric values or placeholder structures.

# Deliverables

Submit `report/results.json` containing per-system identity, geometry provenance, J, population at 300 K, units, method, validation records (including sign convention and population expression), coverage/status, and a conclusion. A bounded-failure branch is allowed when diagnostics and attempted scope are reported.
