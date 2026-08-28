# Scientific objective

Independently calculate and compare atom-specific Mulliken charges for [TMTFABA]OTf, [PTMA]OTf and TFAP to test the qualitative hypothesis that the bifunctional catalyst has electronically differentiated carbonyl and quaternary-ammonium sites. Report the carbonyl-carbon charge for [TMTFABA]OTf and TFAP, the quaternary-ammonium-nitrogen charge for [TMTFABA]OTf and [PTMA]OTf, the two pairwise differences, their signs, and a scope-limited interpretation. The author hypothesis being tested is that the two functional sites cooperate electronically; no numerical target or winning result is supplied.

# Public inputs and scientific boundaries

Use `data/inputs/systems.json`. It uniquely defines the three systems, connectivity, formulas, total charge, singlet multiplicity, solvent and atom environments. The OTf anion is part of each ionic pair. The physical boundary is the three isolated molecular systems in an acetonitrile continuum; do not model the full catalytic reaction, a transition state, or experimental NMR. You may construct 3D starting geometries and choose conformers, but must record the construction and conformer policy. The measured quantity is the Mulliken charge from your declared population analysis.

# Required scientific validation/investigation

Declare the electronic-structure method, basis, solvation treatment, software/version, geometry protocol and population-analysis protocol before reporting charges. Optimize each of the three systems and perform a stationary-point check; a frequency calculation or another scientifically defensible minimum-validation method is acceptable if its evidence is reported. Identify each scored atom by system, element and environment exactly as in the input. Extract charges from machine-readable or auditable output and retain provenance. The investigation is complete when all three systems have an auditable validated structure and all four requested charges and both differences are reported, or when a bounded computational failure is documented for a named system with the attempted protocol, evidence and limitation. Stop after this fixed three-system set and do not add unrequested candidate structures.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include a concise method and validation record, per-system structure/provenance records, the four charges, pairwise differences, qualitative conclusion and limitations. A failure branch must identify the affected system(s) and preserve all successful results. Numeric values must be in elementary-charge units.
