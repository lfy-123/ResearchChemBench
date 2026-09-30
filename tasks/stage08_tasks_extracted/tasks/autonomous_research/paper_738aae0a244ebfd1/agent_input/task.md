# Scientific objective

Determine the gas-phase electronic structure of the neutral AMP-TFA ion pair defined in the public input. Report an optimized structure, whether it is a true minimum, the HOMO and LUMO energies and gap, and the dominant vertical singlet excitation with wavelength, oscillator strength, and orbital assignment. The scientific endpoint is an independently supported electronic-structure characterization, not a periodic-solid or experimental measurement.

# Public inputs and scientific boundaries

Use `data/inputs/amp_tfa_ion_pair.json` as the complete chemical identity: its two component SMILES, component charges, total charge 0, multiplicity 1, formula C6H12F3NO3, and isolated gas-phase boundary are authoritative. The ion pair is one AMP cation, [(CH3)2C(NH3+)CH2OH], plus one trifluoroacetate anion, [CF3COO−]. You may generate 3-D conformers and choose computational models, but must state them. The measured quantities are the optimized molecular geometry, harmonic vibrational frequencies, frontier-orbital energies and gap in eV, and vertical singlet excitations in nm with oscillator strengths and orbital contributions. Do not claim a periodic band gap, solvent property, or experimental spectrum.

# Required scientific validation/investigation

Generate at least one chemically valid starting conformer, remove duplicate starting geometries by a stated structural/RMSD criterion, and optimize each advanced conformer with a documented electronic-structure method. Advance a structure only if the calculation converges and its connectivity and charge state remain intact. Validate the reported candidate minimum with a harmonic frequency calculation and explicitly report the number and values/signs of imaginary modes. From a vertical-excitation calculation on the validated optimized structure, identify the dominant transition by a stated rule using oscillator strength and/or reported intensity, retaining its wavelength and orbital contribution. Completion requires a converged optimized structure, documented minimum validation, and a completed excitation list with a selected dominant transition; if resources prevent this, report bounded failure with the exact completed stages and limitation. Stop after all generated starting conformers have been processed or after a documented resource/time boundary, and report coverage, discarded duplicates, failed jobs, and sensitivity across retained conformers.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method, software, convergence evidence, structure identity, minimum-validation evidence, the gap, excitation list/selection, and a concise conclusion about the electronic structure. Include paths to any coordinate, frequency, and excitation output files that support the claims. A bounded-failure branch is allowed only when the completed stages and limitation fields are filled truthfully.
