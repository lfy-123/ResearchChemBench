# Scientific objective

Independently test the authors' qualitative proposal that Li+ can be stabilized by complementary Li–O and Li–F contacts in TFPM by computing the gas-phase electronic binding energy of one Li+ ion and one neutral TFPM molecule. Determine an optimized complex, its binding energy Eb, and whether it is a true minimum. The hypothesis is qualitative only: do not assume a winning geometry, contact distances, ring size, or result direction.

# Public inputs and scientific boundaries

Use `data/inputs/tfpm_system.json`. TFPM is the neutral molecule represented by the supplied SMILES `COCCC(F)(F)F`; Li is a +1 singlet ion; the complex is charge +1, singlet. The object is an isolated gas-phase two-species complex. No counterion, bulk solvent, periodic cell, experimental observable, or free-energy correction is included. Compute Eb using the supplied formula and state units and sign convention. The paper, SI, and general web are unavailable; software and model chemistry are your choice.

# Required scientific validation/investigation

Generate a finite, explicitly described set of chemically distinct starting orientations/conformers, including alternatives that do and do not place Li near O or F. Deduplicate optimized structures using a stated structural criterion, and report all candidates advanced to final comparison. Optimize the complex and isolated TFPM, calculate the isolated Li+ energy consistently, and validate the selected stationary point with frequencies or a justified equivalent. A calculation is complete when the reported candidate set has been optimized, deduplicated, checked for convergence and stationary-point character, and the binding-energy comparison is stable under the stated coverage. Stop when no new distinct starting arrangement remains in the declared generation scheme; if convergence or minimum validation fails, report bounded failure and the limitation rather than inventing a result.

# Deliverables

Submit `report/results.json` conforming to the schema. Include candidate identities and validation status, complex/fragment energies, Eb in eV, selected candidate rationale, geometry/contact interpretation, method/software details, coverage and stopping statement, and limitations. Do not copy private paper values or claim agreement without performing the calculation.
