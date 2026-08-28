# Scientific objective

Independently determine the relative nucleophilic reactivity of ODA, 6FODA and PFMB toward TMC using reproducible electronic-structure calculations. Select and justify descriptors that can discriminate the three diamines, report their values and ordering, and report optimized inter-benzene dihedral angles. If descriptors disagree, analyze the disagreement and state which interpretation is supported within the stated model.

# Public inputs and scientific boundaries

Use only `data/inputs/monomers.json`. It explicitly supplies unique IDs, names, SMILES connectivity, neutral charge, singlet multiplicity and role for ODA (4,4'-diaminodiphenyl ether), 6FODA (4,4'-oxybis[3-(trifluoromethyl)aniline]), PFMB (2,2'-bis(trifluoromethyl)benzidine) and TMC (trimesoyl chloride). The scored object is the isolated gas-phase molecular comparison. Do not infer polymer coordinates, solvent effects, membrane performance, experimental rate constants or an author mechanism. Preserve connectivity, protonation, charge and multiplicity.

# Required scientific validation/investigation

Construct a finite and explicitly described conformer set for each diamine, deduplicate it with a stated rule, optimize the retained structures and document convergence/stationarity. Choose at least one local reactivity descriptor, define it mathematically, map it to the amine atom(s), give units, and explain why it is chemically relevant to reaction with TMC. Validate charge 0, multiplicity 1, connectivity, equivalent-site treatment and the dihedral selector C1–C2–X–C3 (X=O for ODA/6FODA; X=C for PFMB). Report method sensitivity or limitation when feasible. Completion requires auditable results for all three diamines or a scientifically justified bounded failure branch. Stop when the supplied four-molecule set and declared conformer/sensitivity scope are exhausted; no web or literature search is allowed.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the independent method plan, per-molecule descriptor and dihedral records, candidate/conformer coverage, validation evidence, ordering or bounded-failure status, and a conclusion limited to the computed model.
