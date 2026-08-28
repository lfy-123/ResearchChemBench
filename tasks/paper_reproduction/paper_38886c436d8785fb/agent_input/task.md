# Scientific objective

Test the authors' qualitative proposal that an ionic-liquid environment can strengthen association between 1,3,5-triformylbenzene (Tb) and p-phenylenediamine (Pa). Independently plan and perform calculations on the public isolated molecular systems, determine interaction energies for the binary Tb·Pa and ionic-liquid-containing C8-IL·Tb·Pa complexes, and assess whether the computed change supports the proposed mechanism. The research object is the electronic interaction energy, not a crystallization transition state or membrane property.

# Public inputs and scientific boundaries

`data/inputs/molecular_system.json` defines unique SMILES, charge and singlet multiplicity for Tb, Pa, the 1-octyl-3-methylimidazolium cation, and the bis(trifluoromethylsulfonyl)imide anion; it defines 1:1 Tb·Pa and 1:1:1:1 C8MIm/NTf2/Tb/Pa stoichiometries and the interaction-energy convention. Treat the ionic liquid as its explicitly supplied ion pair. You may generate 3-D conformers and complex arrangements, but must not use a paper-provided geometry. The boundary is isolated complexes in the gas phase or another explicitly stated model; no periodic COF, solvent bath, polymer, membrane, or crystallization barrier is scored.

# Required scientific validation/investigation

Describe the independent computational method, geometry generation, charge treatment, and energy convention. Generate and deduplicate chemically distinct starting arrangements for each complex; optimize them and retain only structures with a documented stationary-point check. Report how many arrangements were attempted, the deduplication criterion, which advanced, and why the search stopped. At minimum, provide a frequency-based minimum check or a scientifically justified alternative and state any imaginary modes. Compute component and complex energies consistently, convert to kJ/mol, and report sensitivity/limitations when conformer or ion-pair choices are not exhaustively converged. Completion requires both target complexes to have at least one validated retained structure and both interaction energies plus their difference. Stop when additional independently generated arrangements either reproduce already retained structures under the stated deduplication rule or the reported coverage/compute limitation is reached; a bounded failure must identify the missing target and evidence.

# Deliverables

Submit `report/results.json` conforming to the schema. For each target, identify the target object and every retained candidate by a neutral structure description, and give its validation status and raw energy; report candidate counts, the selected interaction energy, methods, energy change, uncertainty/limitations, and the conclusion. A truthful bounded-failure branch is allowed when a target cannot be validated; in that branch report the missing target and evidence without fabricated energies.
