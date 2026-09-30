# Scientific objective

Independently calculate and compare atom-specific Mulliken charges for [TMTFABA]OTf, [PTMA]OTf and TFAP to test the qualitative hypothesis that the bifunctional catalyst has electronically differentiated carbonyl and quaternary-ammonium sites. Report the carbonyl-carbon charge for [TMTFABA]OTf and TFAP, the quaternary-ammonium-nitrogen charge for [TMTFABA]OTf and [PTMA]OTf, the two pairwise differences, their signs, and an interpretation supported by the computed atomic charges.

# Author-provided scientific guidance

The author hypothesis being tested is that the two functional sites cooperate electronically; no numerical target or winning result is supplied.

# Public inputs and scientific boundaries

Use `data/inputs/systems.json`. It uniquely defines the three systems, connectivity, formulas, total charge, singlet multiplicity, solvent and atom environments. The OTf anion is part of each ionic pair. The physical boundary is the three isolated molecular systems in an acetonitrile continuum; do not model the full catalytic reaction, a transition state, or experimental NMR. You may construct 3D starting geometries and choose conformers, but must record the construction and conformer policy. The measured quantity is the Mulliken charge from your declared population analysis.

# Required scientific validation/investigation

Declare the electronic-structure method, basis, solvation treatment, software/version, geometry protocol and population-analysis protocol before reporting charges. Optimize each of the three systems and perform a stationary-point check; a frequency calculation or another scientifically defensible minimum-validation method is acceptable if its evidence is reported. Identify each scored atom by system, element and environment exactly as in the input. Extract charges from machine-readable or auditable output and retain provenance. The investigation is complete when all three systems have an auditable validated structure and all four requested charges and both differences are reported, or when a bounded computational failure is documented for a named system with the attempted protocol, evidence and failure cause.

The primary comparison protocol is B3LYP-D3(BJ)/6-31G(d,p), IEFPCM acetonitrile geometry optimization and frequency validation, followed on each corresponding optimized complete-system geometry by M06-2X-D3/def2-TZVP with SMD acetonitrile and Mulliken population analysis. Equivalent software implementations are allowed. Select conformers by a declared structural/energy policy, not their charge agreement. Other protocols are sensitivity results, not interchangeable primary reference charges.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include a concise method and validation record, per-system structure/provenance records, the four charges, pairwise differences, qualitative conclusion. A failure branch must identify the affected system(s) and preserve all successful results. Numeric values must be in elementary-charge units.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
