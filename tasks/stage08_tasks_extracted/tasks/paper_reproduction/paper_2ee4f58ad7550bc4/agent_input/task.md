# Scientific objective

Independently determine whether the two named thiocyanato-bridged Cu(II) systems differ in Cu-centered local electrophilicity, using a reproducible computational investigation of the finite-difference local Fukui function f_k+, and assess what that result does and does not imply for oxidation of 3,5-di-tert-butylcatechol (3,5-DTBC) to 3,5-di-tert-butylquinone (3,5-DTBQ).

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that Cu-centered local electrophilicity helps determine how strongly the Cu site can bind and activate 3,5-DTBC, and use that electronic distinction to interpret different catecholase behavior. Treat this as a focused structure–property hypothesis to test with the specified isolated-molecule calculations.

**Candidate route or mechanism.**
The proposed comparison is between the Cu sites in the brominated and chlorinated Schiff-base/NCS complexes, with substrate interaction centered at Cu and leading toward oxidation of the catechol substrate to the corresponding quinone. The relevant state change for the electronic comparison is electron addition to each isolated complex; do not infer a complete catalytic pathway from this comparison alone.

**Discriminating evidence.**
Discriminate the hypothesis by comparing consistently partitioned Cu atomic charges between the neutral and one-electron-reduced states, while checking charge, spin, geometry, and convergence evidence. Frontier-orbital or related electron-density localization around Cu may support the proposed Cu-centered interaction, but the Fukui comparison and its reproducibility are the primary test.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. Recover coordinates from CCDC records 2453268 (the C13H16BrCuN3OS system; public label system_1/1m) and 2453269 (the C13H16ClCuN3OS system; public label system_2/2m), using the stated deterministic extraction and chain-termination procedure. The scored systems are isolated monomeric molecules with one Cu, one deprotonated tridentate Schiff-base ligand, and one NCS group; do not add a host, solvent, or periodic polymer environment. Compute neutral formal-charge-0 triplets and one-electron-reduced formal-charge-(-1) doublets. The measured quantity is the dimensionless Cu atomic-charge difference f_k+ = q_Cu(neutral) − q_Cu(reduced), with one charge-partitioning scheme used consistently. Reaction context is aerobic methanolic oxidation of 3,5-DTBC to 3,5-DTBQ.

# Required scientific validation/investigation

Propose and execute a defensible route independently. Validate coordinate provenance, Cu identity, formal charge, spin multiplicity, electron-count change, SCF and geometry convergence (or report bounded failure), and charge-partitioning consistency. Report any chain-break edit, alternative conformers or failed states. Completion requires a traceable neutral/reduced pair for each named system and either a validated Cu f_k+ comparison or a scientifically justified bounded failure. Stop after the named systems and any finite, explicitly reported conformer/state checks are exhausted; do not expand to unrelated complexes. If multiple explanations for any observed difference are plausible, state and discriminate them using only computed evidence. Separate electronic evidence from claims of catalytic mechanism.

# Deliverables

Submit `report/results.json` conforming to the schema. Include object identity and provenance, state/convergence evidence, Cu charges and f_k+ values when available, validation status, any independently proposed interpretation, limitations, and a completion status. A bounded-failure branch must state what failed and preserve completed evidence.
