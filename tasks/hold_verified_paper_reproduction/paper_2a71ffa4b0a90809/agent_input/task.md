# Scientific objective

Determine the rotational free-energy profile and barrier for neutral singlet perfluoroiodoarene XB donor 1a (C18F12I2), using the supplied 1a-syn Cartesian structure as the starting state. The measured endpoint is the maximum/endpoint Gibbs free-energy difference along the defined ring–linker dihedral rotation, in kcal mol−1.

# Author-provided scientific guidance

The authors qualitatively interpret this donor as a rigid, atropisomeric structure arising from steric crowding by I and F; independently test that hypothesis computationally.

# Public inputs and scientific boundaries

The public input `data/inputs/1a_syn.xyz` is an XYZ file with 32 atoms, neutral charge and singlet multiplicity. Its atom order is the order in the file and its coordinates are in Å. The molecule is C18F12I2: 18 carbon atoms, 12 fluorine atoms and 2 iodine atoms. The scan uses the substituent-defined signed F–C–C–I torsion across the ring–linker bond: the middle carbon atoms form the biaryl rotation axis, while F is a substituent on the central linker and I is a substituent on the rotating outer ring. F and I are not required to be bonded directly to the two axis carbons. In the supplied atom order, one source-consistent definition is F27–C10–C13–I28; report and verify the actual angle and preserve the atom mapping. The supplied free-donor structure represents the syn starting conformer and its starting dihedral is expected to be near 69°, but you must measure and report it. The physical boundary is an isolated molecule in implicit THF at 193.15 K; no experimental rate or catalytic yield is requested. You may generate conformers and choose software/model chemistry, but disclose all choices, units, charge, multiplicity and convergence settings.

# Required scientific validation/investigation

Independently optimize the supplied structure and establish a defensible relaxed constrained profile while varying the defined dihedral toward 0°. Generate a finite, explicitly reported set of scan states that covers the interval from the measured starting angle to 0°; deduplicate repeated/failed states, record failures, and identify whether the largest relative Gibbs free energy is an endpoint or an interior state. Validate the unconstrained starting minimum with zero imaginary frequencies. For constrained scan states, report free-coordinate convergence, preserved connectivity, actual dihedral, and all imaginary modes found in a full Hessian; do not confuse constrained stationarity with an unconstrained minimum or reject expected negative torsional curvature merely because the torsion is held fixed. Report the thermal treatment, including how negative and low-frequency modes enter the thermochemistry. Report at least one sensitivity or robustness check (for example nearby starting geometries, scan spacing, or a defensible alternative model) and explain its effect. Completion requires an auditable profile with at least five distinct converged states including the starting and near-zero/end state, a stated energy reference, and a reproducible barrier extraction. Report the quantitative sensitivity of the extracted barrier to the control you performed; a generic disclaimer is not a sensitivity calculation. Do not claim an experimental activation free energy.

# Deliverables

Submit `report/results.json` and `report/README.md`. `results.json` must contain the declared fields for status, system, scan states, barrier, validation, sensitivity and conclusion. A bounded-failure submission is allowed only when it includes the attempted states, failure reasons, achieved coverage and the specific reason it is incomplete; do not fabricate energies. README must give the exact computational commands/workflow, atom-index convention and units.
