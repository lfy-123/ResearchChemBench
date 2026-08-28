# Scientific objective

Determine the ground-state electronic torsion-energy profile of organoboron ester 1 for rotation about the bond joining boron to the 3,5-dimethylphenyl ring. The authors qualitatively propose that steric shielding by the meta methyl substituents restricts this rotation; independently test that hypothesis with a defensible computational calculation. Report relative E(theta), the minimum and maximum scan energies, and the implications and limitations of the result for non-radiative rotational relaxation and photostability.

# Public inputs and scientific boundaries

Use the pinned Cambridge Structural Database record CCDC 2441197 in `data/inputs/ccdc_record.json` to obtain one complete molecule of compound 1. Preserve its connectivity, stereochemistry, neutral charge and singlet state; document any deterministic hydrogen completion. The scanned coordinate is the B–ipso-carbon bond to the 3,5-dimethylphenyl ring, with a fixed ordered four-atom dihedral and atom IDs retained at every point. The requested observable is the ground-state electronic energy relative to the lowest point, in kJ/mol, at angles 0, 15, ..., 345 degrees. This is an isolated-molecule rigid-rotor electronic-energy model: do not interpret it as a solvent free energy, rate, photobleaching quantum yield, or excited-state surface.

# Required scientific validation/investigation

Choose and justify an electronic-structure method, basis, charge/state, geometry treatment, convergence criteria and energy-unit conversion independently. Optimize the starting structure or otherwise justify its use, and provide evidence that the optimized structure is a minimum or clearly label a bounded failure. Generate all 24 fixed-angle structures from one consistent atom mapping, evaluate each point, remove duplicate/missing angles, reference energies to the lowest submitted point, and check continuity and periodic closure between 345 and 0 degrees. The calculation is complete when all 24 angles have converged energies and the validation checks are reported; if this cannot be achieved, stop after the failed points and submit the bounded-failure branch with attempted coverage, causes and a scientifically meaningful limitation.

# Deliverables

Submit `report/results.json` conforming to the schema. Include the profile, scan identity and validation evidence, method and convergence details, minimum/maximum metrics, conclusion, and either successful completion or a truthful bounded-failure record. State the stopping condition and the actual angular coverage.
