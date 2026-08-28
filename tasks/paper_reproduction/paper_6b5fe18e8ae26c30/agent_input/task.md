# Scientific objective

Determine the interaction enthalpy ΔH (kcal mol−1) for binding of the supplied neutral XHNBR carboxyl fragment to the supplied neutral (ZnO)12 cluster, and determine whether the optimized minimum supports proton transfer from the carboxyl OH group to a cluster oxygen. The author hypothesis to test is that carboxyl binding is organized by proton transfer and metal–oxygen coordination. Independently choose and justify a computational route; the author’s software, model chemistry and numerical result are not provided.

# Public inputs and scientific boundaries

Use `data/inputs/zno12.xyz` as the complete 24-atom neutral ZnO cluster and `data/inputs/xhnbr_carboxyl.xyz` as the complete 16-atom neutral carboxyl fragment. Atom order and element identities in these XYZ files are fixed; no atoms, protonation, charge or multiplicity may be changed. The target is a finite gas-phase molecular-cluster model, not a periodic surface or bulk solid. You may generate separated and complex starting geometries, conformers and wavefunctions. The scored endpoint is the lowest defensible bound minimum located for this model under your chosen method, with the isolated-fragment reference defined by the same method and thermochemical convention.

# Required scientific validation/investigation

Construct and optimize the isolated cluster, isolated fragment and at least two non-equivalent complex starting orientations. Verify each reported minimum by a frequency calculation or a clearly justified alternative stationary-point test, and retain enough information to identify atom order and the starting orientation. Deduplicate converged complexes by connectivity and geometry. For the selected bound minimum, report ΔH = H(complex) − H(cluster) − H(fragment), its method and thermal convention, and inspect the carboxyl OH hydrogen, nearby cluster oxygens, carboxyl C–O distances and Zn–O contacts. Call proton transfer present only when the hydrogen is bonded to a cluster oxygen in the optimized structure and the original carboxyl O–H bond is broken or substantially elongated; otherwise call it absent or unresolved. Completion requires a converged, validated minimum plus a reproducible energy decomposition and structural analysis. Stop after the required starts have been validated and additional starts no longer produce a distinct lower bound minimum, or report bounded failure with all failed starts and the limitation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the selected complex geometry (XYZ or equivalent), isolated-reference energies/enthalpies, ΔH in kcal mol−1, proton-transfer classification, measured structural descriptors, method, convergence/frequency evidence, all complex starts and deduplication/coverage notes. If no validated bound minimum is obtained, use the failure branch and provide the attempted starts, diagnostics and scientifically justified limitation.
