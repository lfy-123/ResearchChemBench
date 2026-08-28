# Scientific objective

Independently test the authors' qualitative hypothesis that the divalent DED2+ cation binds propylene carbonate (PC) more strongly than the monovalent TEA+ cation and can therefore compete for PC in a solvent-limited electrolyte. Compute signed electronic binding energies for the explicitly named DED2_PC, TEA_PC and BF4_PC pairs and determine the DED2_PC versus TEA_PC ordering. The benchmark concerns isolated gas-phase ion–PC pairs, not bulk solvation free energies.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. It uniquely defines the four molecular graphs, formal charges, singlet multiplicities, atom-element lists, pair identities, and the binding-energy equation. You must generate 3-D starting geometries; the supplied connectivity is authoritative. PC is racemic/unspecified at its ring stereocenter, so do not claim an enantiopure result. Report kcal/mol, preserve the stated atom identities, and do not use the paper or general web as an input. No electrode, continuum-solvent, bulk concentration, or experimental value is part of the scored calculation.

# Required scientific validation/investigation

For each of the three named pairs, generate at least two chemically distinct initial ion–PC orientations, optimize the complex and both isolated components with a defensible electronic-structure method, and verify every retained minimum by frequencies or an equivalently justified minimum test. Deduplicate converged structures using a stated structural criterion, retain the identity and provenance of every candidate, and compute binding energies by explicit energy bookkeeping from the same component convention. Perform at least one sensitivity check (different conformer, orientation, dispersion treatment, basis, or validated alternative) and explain its effect on the DED2_PC/TEA_PC ordering. The investigation is complete when every named pair has at least one validated retained minimum, all reported energies are traceable to component calculations, and the sensitivity result and limitations are recorded. Stop after those conditions are met and no additional tested orientation changes the selected ordering; otherwise report bounded failure, the tested coverage, and the unresolved limitation rather than fabricating a result.

# Deliverables

Submit `report/results.json` with the required schema. Include method and sign convention, per-pair candidate identity, energies and validation evidence, the cross-pair ordering, sensitivity outcome, and a concise source-independent scientific conclusion. A bounded-failure branch is allowed and must identify which pair or validation condition prevented completion.
