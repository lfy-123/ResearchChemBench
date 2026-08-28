# Scientific objective

Determine, by an independently planned electronic-structure calculation, the relative nucleophilic reactivity of the four explicitly supplied neutral singlet molecules (ODA, 6FODA, PFMB and TMC), focusing on the three diamine amine sites as reactants toward TMC. Report at least one quantitatively defined local reactivity descriptor for each diamine, the resulting ordering, and optimized inter-benzene dihedral angles for ODA, 6FODA and PFMB. The author hypothesis to test is that a multi-descriptor analysis of the diamines supports a common reactivity order toward TMC; do not assume that hypothesis is correct.

# Public inputs and scientific boundaries

Use only `data/inputs/monomers.json`. It gives unique IDs, names, SMILES connectivity, neutral charge, singlet multiplicity and chemical role for ODA (4,4'-diaminodiphenyl ether), 6FODA (4,4'-oxybis[3-(trifluoromethyl)aniline]), PFMB (2,2'-bis(trifluoromethyl)benzidine) and TMC (trimesoyl chloride). The scored system is the isolated-molecule gas-phase comparison; no polymer fragment, solvent, membrane, transport property or experimental rate constant is part of the target. Preserve the supplied connectivity and protonation. You may generate conformers and choose a defensible electronic-structure method, but must state all choices and atom/site mapping.

# Required scientific validation/investigation

Plan and execute calculations for all three diamines and, where needed to define the reaction context, TMC. Generate a finite, deduplicated conformer set or justify a single starting conformer; optimize geometries and establish convergence/stationarity using a documented criterion. Define the descriptor mathematically, identify the amine atom(s) used, report units and uncertainty/sensitivity. Validate that all molecules retain charge 0 and multiplicity 1, that the connectivity is unchanged, and that the dihedral selector is C1–C2–X–C3 with X=O for ODA/6FODA and X=C for PFMB. Compare equivalent terminal sites and explain any asymmetry. The investigation is complete when every supplied diamine has a converged, auditable descriptor and geometry result, or when a documented bounded failure explains why one cannot be obtained. Stop after the supplied four-molecule set and the stated conformer/sensitivity analysis are exhausted; do not expand to literature or additional molecules.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include methods, identity-bound records for ODA, 6FODA, PFMB and TMC, descriptor and dihedral results for each diamine, ordering or bounded-failure status, validation evidence, and a concise conclusion that explicitly distinguishes a computed result from an experimental kinetic claim. If a diamine cannot be completed, use its per-molecule bounded-failure branch and do not fabricate numerical fields. Report enough intermediate provenance for an evaluator to reproduce the actual calculation.
