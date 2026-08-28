## Scientific objective

Independently test the authors' qualitative proposal that conformationally distinct close (folded) and open (unfolded) arrangements of the E-AB-mTTA-(1,3)Ph chloride complex can both be relevant. Compute and compare the relative Gibbs free energy of the two explicitly named starting structures, and state whether your validated calculation supports near-degeneracy within the limitations of your chosen model. The measured quantity is the open-minus-close relative Gibbs free energy for this one chloride complex.

## Public inputs and scientific boundaries

The public inputs are `data/inputs/e_ab_mtta_13ph_cl_close.xyz` and `data/inputs/e_ab_mtta_13ph_cl_open.xyz`. Each is an XYZ structure for the same E-AB-mTTA-(1,3)Ph host with one chloride atom, charge -1 and singlet multiplicity; the second-line metadata identifies the system. Preserve atom identities and coordinates as supplied. You may generate conformers and choose computational methods, but do not use the paper, SI or general web. The boundary is the isolated molecular complex represented by these coordinates; report solvent, temperature, electronic-structure method, thermochemical convention and any constraints.

## Required scientific validation/investigation

Optimize both named structures or provide a scientifically justified alternative that evaluates both without changing their identity. Validate each reported endpoint as a minimum with a frequency calculation or an explicitly documented alternative validation; report any imaginary modes and whether they invalidate the endpoint. Use one common energy reference and units, and compute open-minus-close from the same protocol. Perform at least one method, conformer, or numerical-sensitivity check and explain its effect. The calculation is complete when both named endpoints have reproducible energies/free energies or a bounded failure is documented with attempted steps and evidence. Stop after both endpoints are validated and the sensitivity check is reported; if a defensible minimum cannot be obtained, stop and submit the bounded-failure branch rather than inventing a value.

## Deliverables

Write `report/results.json` conforming to the submission schema. Include method provenance, endpoint identities, convergence/frequency evidence, the signed open-minus-close value in eV when available, sensitivity findings, interpretation, and limitations. A bounded failure must identify the endpoint, attempted computation, observed failure, and next scientifically meaningful limitation.
