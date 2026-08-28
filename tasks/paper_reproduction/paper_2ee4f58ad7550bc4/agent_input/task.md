# Scientific objective

Test, by an independent electronic-structure calculation, whether the Cu sites in the two deposited thiocyanato-bridged Cu(II) systems have different local electrophilicity as measured by the finite-difference local Fukui function f_k+ and whether that electronic comparison can support the reported difference in oxidation of 3,5-di-tert-butylcatechol (3,5-DTBC) to 3,5-di-tert-butylquinone (3,5-DTBQ). The authors' qualitative hypothesis is that Cu-centered electrophilicity helps explain the activity difference; do not assume its direction or numerical value.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. Recover coordinates from CCDC records 2453268 (complex 1, Br ligand; public label 1m) and 2453269 (complex 2, Cl ligand; public label 2m), using the stated deterministic extraction and chain-termination procedure. The objects are isolated monomeric units containing one Cu, one deprotonated tridentate Schiff-base ligand, and one NCS group. Compute neutral formal-charge-0 triplets and one-electron-reduced formal-charge-(-1) doublets. The measured quantity is the dimensionless Cu atomic-charge difference f_k+ = q_Cu(neutral) − q_Cu(reduced), using one charge-partitioning scheme consistently. The reaction context is aerobic methanolic oxidation of 3,5-DTBC to 3,5-DTBQ; do not model a substrate-bound transition state unless separately justified. Do not use the paper, SI, general web, or unpinned structures as scientific input.

# Required scientific validation/investigation

Independently choose and document a defensible computational method, then generate both charge states for both named systems. Validate coordinate provenance, atom identity of Cu, formal charge, spin multiplicity, electron-count change, SCF and geometry convergence (or clearly report bounded failure), and consistency of the charge partitioning. Report any chain-break edit, alternative conformers or failed states. The investigation is complete when both systems have a traceable neutral/reduced pair and either a validated Cu f_k+ comparison or a scientifically justified bounded failure for one or more systems. Stop after the named two systems and any finite, explicitly reported conformer/state checks are exhausted; do not expand to unrelated complexes. Interpret the comparison cautiously and distinguish electronic support from proof of catalytic mechanism.

# Deliverables

Submit `report/results.json` conforming to the schema. Include system identity and provenance, state/convergence evidence, Cu charges and f_k+ values when available, validation status, optional orbital localization evidence, a comparison, an interpretation relative to the reaction context, limitations, and a completion status. A bounded-failure branch must state what failed and preserve all completed evidence.
