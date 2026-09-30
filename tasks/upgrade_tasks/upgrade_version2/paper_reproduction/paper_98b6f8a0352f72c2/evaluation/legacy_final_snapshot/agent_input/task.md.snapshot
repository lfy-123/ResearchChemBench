# Scientific objective

Determine, for the supplied neutral singlet compound 12a in a chloroform continuum, the vertical first-singlet excitation (S1) energy in eV, oscillator strength, and radiative lifetime in ns. The authors’ qualitative scientific hypothesis is that TD-DFT/NTO analysis can explain the photophysical behavior and that the lowest transition has internal charge-transfer character from the aromatic amine toward the phenazine framework. Independently plan and execute calculations that test this hypothesis; the winning numerical result, author model chemistry and ordered protocol are not prescribed.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that a ground-state electronic-structure calculation followed by a time-dependent excited-state analysis can account for the absorption behavior of 12a. They interpret the lowest transition as having internal charge-transfer character, with electron density moving from the aromatic amine substituent toward the phenazine framework and spreading over that framework.

**Candidate route or mechanism.**
A useful candidate interpretation is an amine-to-phenazine excitation within the isolated conjugated molecule, with the donor-side aromatic amine and acceptor-side phenazine unit forming the principal parts of the transition. The transition should be examined for both charge-transfer character and phenazine-framework delocalization rather than assigned from an oscillator strength alone.

**Discriminating evidence.**
Use excited-state transition analysis such as natural transition orbitals or an equivalent density-based decomposition to compare hole and electron locations and quantify or clearly document their spatial overlap and spread. Relate that analysis to the identified lowest singlet state and test its stability with the required independent conformer, implementation, or model-sensitivity validation.

# Public inputs and scientific boundaries

Use `data/inputs/compound_12a.json` as the complete system definition: 5-(4-(N,N-dimethylamino)phenyl)benzo[a]phenazine, formula C24H19N3, the explicit connectivity SMILES, charge 0 and multiplicity 1. Model an isolated molecule in a chloroform continuum (CHCl3); explicit solvent, counterions, aggregates and solid-state periodicity are outside scope. The measured/computed endpoints are the vertical S1 energy at the optimized ground-state geometry, its oscillator strength, and the radiative lifetime derived from that same transition. Do not use the paper, SI, general web or hidden evaluator references.

Primary radiative-lifetime definition: tau_rad(s) = 1.4999 / (f * wavenumber_cm_inverse**2), where f is dimensionless and wavenumber_cm_inverse is the numerical S1 excitation wavenumber in cm^-1; tau_rad(ns) = 1e9 * tau_rad(s). Use the energy and oscillator strength of the same identified vertical transition. This is the oscillator-strength-derived radiative lifetime, not the total lifetime including nonradiative decay. Do not add a refractive-index or local-field multiplier to this primary conversion; any different lifetime convention is a separate supplementary quantity. The excitation calculation itself includes the specified chloroform continuum.

# Required scientific validation/investigation

Generate and deduplicate at least one chemically valid 3D starting conformer and record how it was made. Optimize the ground-state structure, verify charge/multiplicity and an actual stationary/converged result, then compute enough singlet excited states to identify S1 unambiguously and report the state index, energy, oscillator strength and any transition character analysis used. Derive the lifetime using the primary equation and units defined above. Validate the conclusion with an independent check such as a second starting conformer, an independent implementation, or a clearly justified convergence/model sensitivity test; bind the check to the object and report whether it changes S1 selection or the conclusion. Completion requires a converged optimized structure, a converged excited-state calculation with S1 identified, all three requested observables with units, and validation evidence.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the final observables, method/software and solvent model, geometry and excited-state convergence evidence, state-selection evidence, validation records, calculation coverage, and a concise conclusion about the qualitative charge-transfer hypothesis. A bounded failure is allowed only when the corresponding status branch and evidence fields truthfully document what was and was not completed.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
