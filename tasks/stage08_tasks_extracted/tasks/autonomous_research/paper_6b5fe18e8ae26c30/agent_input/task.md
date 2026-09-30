# Scientific objective

Determine the interaction enthalpy ΔH (kcal mol−1) for binding of the supplied neutral XHNBR carboxyl fragment to the supplied neutral (ZnO)12 cluster, and determine the optimized binding motif, including whether proton transfer occurs. Independently formulate plausible binding explanations and discriminate them with calculations and structural/electronic evidence; no literature mechanism or candidate route is supplied.

# Public inputs and scientific boundaries

Use `data/inputs/zno12.xyz` as the complete 24-atom neutral ZnO cluster and `data/inputs/xhnbr_carboxyl.xyz` as the complete 16-atom neutral carboxyl fragment. Atom order and element identities are fixed; no atoms, protonation, charge or multiplicity may be changed. The target is a finite gas-phase molecular-cluster model, not a periodic surface or bulk solid. You may generate separated and complex starting geometries, conformers and wavefunctions. The scored endpoint is the lowest defensible bound minimum located for this model under your chosen method, with isolated references computed consistently.

# Required scientific validation/investigation

Propose at least two chemically distinct starting hypotheses (for example, coordination through either carboxyl oxygen, intact hydrogen bonding, or proton-transfer binding) and construct at least two non-equivalent starts for each hypothesis. Optimize the isolated species and all selected complexes, verify minima by frequencies or a justified stationary-point test, and deduplicate by connectivity and geometry. Report how candidates were generated, which were advanced, and why the search is adequate. For the selected bound minimum, calculate ΔH = H(complex) − H(cluster) − H(fragment), inspect the carboxyl hydrogen and oxygen/Zn contacts, and classify proton transfer as present, absent or unresolved using explicit structural evidence. Completion requires a validated minimum and reproducible energy/structure analysis; stop when all proposed hypotheses have been tested and additional starts no longer yield a distinct lower bound minimum, or report bounded failure with coverage and limitations.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include hypotheses, candidate identities and validation context, selected complex geometry, isolated-reference energies/enthalpies, ΔH in kcal mol−1, proton-transfer classification, structural descriptors, method, convergence/frequency evidence, and coverage/stopping notes. If no validated bound minimum is obtained, use the failure branch and provide attempted candidates, diagnostics and limitations.
