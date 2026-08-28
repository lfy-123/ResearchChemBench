# Scientific objective

For the supplied anionic 36-atom two-state molecular system, independently determine the Gibbs free-energy separation ΔG = G(triplet) − G(singlet), in kcal/mol, between the specified singlet and triplet electronic states, and determine whether the excited-state electronic density exhibits spatially separated donor and acceptor character. Report a scientifically bounded interpretation of what these calculations do and do not establish.

# Public inputs and scientific boundaries

`data/inputs/L-1_L2_ground.xyz` is the complete Cartesian geometry of the system in the singlet state (36 atoms; charge −1, multiplicity 1). `data/inputs/L-1_L2_triplet.xyz` is the complete Cartesian geometry of the same system in the triplet state (36 atoms; charge −1, multiplicity 3). Coordinates are in Å and atom order is part of the system identity. The target is the complex represented by each file, not isolated fragments. Acetonitrile is the stated solvent context, but you must select and justify the computational model. No author mechanism, candidate route or paper software/protocol is supplied or required.

# Required scientific validation/investigation

Design a reproducible calculation for both states and justify the treatment of open-shell thermochemistry and solvent. Report charge, multiplicity, geometry provenance, thermal convention and energy units. Establish a stationary structure for each state and report frequency/stationarity evidence; a minimum requires no imaginary modes, and a failed state must be identified rather than silently accepted. Derive the Gibbs gap transparently and perform one documented consistency or sensitivity check. Use an independent electronic-density diagnostic to test whether the triplet has spatially distinct donor and acceptor regions; identify those regions only from your analysis, or report that the assignment is unresolved. Completion requires auditable state calculations, validation for both states, a reproducible gap and a supported or bounded electronic interpretation. Stop after endpoint validation plus one consistency/sensitivity check; do not claim exhaustive conformer or mechanism discovery.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include protocol, state thermochemistry, gap, validation evidence, independently inferred charge-transfer assessment, limitations and complete/bounded-failure status. If a state or diagnostic fails, use the failure branch with diagnostics and omit unsupported numerical or semantic claims.
