# Scientific objective

Independently test the authors' qualitative proposal that Li+ can be stabilized by complementary Li–O and Li–F contacts in TFPM by computing the gas-phase electronic binding energy of one Li+ ion and one neutral TFPM molecule. Determine an optimized complex, its binding energy Eb, and whether it is a true minimum. The hypothesis is qualitative only: do not assume a winning geometry, contact distances, ring size, or result direction.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that Li+ is stabilized in TFPM through complementary coordination involving the ether oxygen and a fluorine site, producing a chelating complex.

**Candidate route or mechanism.**
Prioritize testing candidate arrangements in which Li+ can contact both O and F, including geometries that could close a chelate-like ring, while retaining competing arrangements with only one principal contact for comparison. Treat these as candidate explanations to test during the search.

**Discriminating evidence.**
Use optimized relative electronic energies and binding energies, stationary-point validation by harmonic frequencies or an equivalent check, and direct geometric analysis of Li–O and Li–F contacts and ring topology to distinguish the proposed dual-contact arrangement from alternatives.

# Public inputs and scientific boundaries

Use `data/inputs/tfpm_system.json`. TFPM is the neutral molecule represented by the supplied SMILES `COCCC(F)(F)F`; Li is a +1 singlet ion; the complex is charge +1, singlet. The object is an isolated gas-phase two-species complex. No counterion, bulk solvent, periodic cell, experimental observable, or free-energy correction is included. Compute Eb using the supplied formula and state units and sign convention. The paper, SI, and general web are unavailable; software and model chemistry are your choice.

# Required scientific validation/investigation

Generate a finite, explicitly described set of chemically distinct starting orientations/conformers, including alternatives that do and do not place Li near O or F. Deduplicate optimized structures using a stated structural criterion, and report all candidates advanced to final comparison. Optimize the complex and isolated TFPM, calculate the isolated Li+ energy consistently, and validate the selected stationary point with frequencies or a justified equivalent. A calculation is complete when the reported candidate set has been optimized, deduplicated, checked for convergence and stationary-point character, and the binding-energy comparison is stable under the stated coverage.

# Deliverables

Submit `report/results.json` conforming to the schema. Include candidate identities and validation status, complex/fragment energies, Eb in eV, selected candidate rationale, geometry/contact interpretation, method/software details, coverage statement. Do not copy private paper values or claim agreement without performing the calculation.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
