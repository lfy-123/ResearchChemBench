## Scientific objective

Study the neutral, closed-shell singlet cis-α-(egan)IrCl and cis-β-(egan)IrCl complexes supplied as Cartesian geometries. The author hypothesis to test is that the two cis isomers can interconvert and have different relative stabilities; independently plan and execute calculations that determine whether each supplied structure relaxes to a minimum and which isomer is lower in gas-phase electronic energy. Do not assume the author's software or model chemistry.

## Public inputs and scientific boundaries

`data/inputs/cis_alpha_egan_IrCl.xyz` is the 58-atom cis-α complex and `cis_beta_egan_IrCl.xyz` is the 46-atom cis-β complex. XYZ element labels and coordinates are the complete molecular identity; each is neutral and singlet. The computational ligand is the hydrogen-substituted egan model represented by these files. The boundary is gas phase and electronic energy; solvent, crystal packing, free energy, kinetics and reaction barriers are outside scope.

## Required scientific validation/investigation

For each named file, choose and report a defensible optimization method, basis/ECP treatment, charge and multiplicity, convergence settings and software. Optimize the supplied geometry, then validate the resulting stationary point with harmonic frequencies or a scientifically justified equivalent. Report the number and sign of imaginary frequencies for each named object. Compute ΔE = E(cis-β) − E(cis-α) from energies evaluated consistently at the two final structures and convert it to kcal/mol. Completion requires both named objects to have a reported endpoint and validation result. Stop after both endpoints and validation checks are complete; do not invent placeholder values if a calculation cannot be completed.

## Deliverables

Submit `report/results.json` conforming to the schema. Include reproducibility metadata, per-isomer energies and validation, ΔE with units, the lower-energy identity, a concise conclusion about the author's qualitative stability hypothesis, and explicit limitations. Do not report paper values as if they were your calculations.
