# Scientific objective

Independently test the authors' qualitative hypothesis that meta-amino substitution produces a stronger intramolecular charge-transfer (ICT) excitation than para-amino substitution by computing the hole–electron centroid distance (D-index) for the lowest singlet excitation of the specified neutral singlet m-NH2 dye. Report the D-index in Å, identify the state used, and explain whether this descriptor is consistent with/supports the authors' stronger-ICT interpretation within the paper's comparative context; an m-NH2-only calculation does not by itself establish a new m-NH2-versus-p-NH2 ordering. The target is the S0→S1 vertical excitation of 2-butyl-6-amino-1H-benzo[de]isoquinoline-1,3(2H)-dione in water treated as a continuum solvent.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors interpret the meta-amino substitution as producing stronger intramolecular charge-transfer (ICT) character than the para-amino analogue, with the hole–electron centroid distance (D-index) serving as the relevant qualitative descriptor.

**Candidate route or mechanism.**
A candidate way to test this claim is to optimize the ground-state geometry, calculate the low-lying singlet excitations of the isolated dye in continuum water, and analyze the S0→S1 excitation using hole–electron distributions. The comparative interpretation concerns whether the m-NH2 state exhibits the larger charge-separation descriptor relative to the corresponding para-substituted comparison.

**Discriminating evidence.**
Use a converged S0 geometry, unambiguous identification of the lowest singlet root, and hole–electron centroid analysis performed on that same excitation. Method, range-separation or tuning treatment, basis, solvent model, and numerical provenance should be recorded because each can affect the D-index; the result should be interpreted as evidence for or against the qualitative ICT claim within the comparative context.

# Public inputs and scientific boundaries

The only molecular input is `data/inputs/m_nh2_identity.json`. It defines m-NH2 as neutral, singlet 2-butyl-6-amino-1H-benzo[de]isoquinoline-1,3(2H)-dione (the n-butyl imide of 3-amino-1,8-naphthalic anhydride), formula C16H16N2O2, with an explicit connectivity SMILES. Use that molecule without changing protonation, charge, multiplicity, atom connectivity, or the amino substitution position. The electronic boundary is the isolated dye; water is a continuum environment. Explicit waters, aggregates, enzymes, experimental spectra, and acetylated analogues are outside the required endpoint. The measured quantity is the distance between the centroids of the hole and electron distributions for the S0→S1 excitation, in Å. The paper's qualitative route is disclosed as context: independently plan calculations to test catalyst-free electronic ICT using geometry optimization, an excited-state calculation, and hole–electron analysis. Do not use the paper/SI or general web as an input source.

# Required scientific validation/investigation

Plan and execute a reproducible electronic-structure workflow of your choice. It must include (i) a documented ground-state geometry preparation and convergence check, (ii) an excited-state calculation that unambiguously identifies the lowest singlet state used as S1, and (iii) a hole–electron analysis that yields one finite, positive D-index for that state. Record method, basis, dispersion, solvent treatment, range separation/tuning or its alternative, software versions, geometry provenance, state/root selection, and numerical settings. If a frequency check, alternative conformer, alternate functional, or other sensitivity test is performed, report it and explain its effect; these are validation evidence, not extra scored targets. Deduplicate any tested conformers by connectivity and geometric equivalence, and state which conformer was advanced and why. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. A successful submission must contain the validated workflow, state identity, D-index, units, method provenance, validation evidence, and a conclusion about whether the result supports the authors' proposed stronger-ICT interpretation. A bounded-failure submission must instead identify the failed stage, preserve all completed validation/provenance fields, explain why no final D-index is reported, and state what remains necessary for completion. Include paths to supporting logs or figures when available; do not include the paper, SI, or evaluator files.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
