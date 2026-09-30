# Scientific objective

For the fixed neutral boron-bridged B2N6 hexazene molecule specified by the public input, independently compute and validate the dominant singlet vertical UV-vis excitation energy and oscillator strength in a dichloromethane continuum. The research object is the molecule and its electronic excited states; crystal packing, emission, electrochemistry and experimental spectra are outside the scored endpoint. Propose and justify a defensible computational route without relying on an author-provided mechanism or protocol.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that substituents at the boron atoms modulate the N6-centred pi-conjugated electronic system of boron-bridged hexazenes, with the B2N6 scaffold contributing electron-accepting character. For compound 1, the principal optical transition is expected to involve the delocalized B2N6/N6 pi framework, while boron substitution changes the frontier orbital energies and optical response.

**Candidate route or mechanism.**
Treat the dominant absorption as a vertical singlet excitation from the optimized ground state and test whether its principal orbital character is concentrated on the conjugated B2N6/N6 framework. A useful comparison is the frontier-orbital transition against neighboring low-lying singlet states, while considering whether the tolyl substituents materially mix into the transition.

**Discriminating evidence.**
Use a converged ground-state geometry, a dichloromethane continuum treatment, and a sufficiently broad low-lying singlet-state calculation. Distinguish the proposal using oscillator strengths, excitation energies, neighboring-state ordering, and orbital or transition-density character, with optional population or spatial analyses that directly establish N6/B2 involvement.

# Public inputs and scientific boundaries

The only molecular input is `data/inputs/ccdc_record.json`: retrieve CCDC record 2512981 from the controlled Cambridge Structural Database/CCDC connector. It identifies the neutral boron-bridged B2N6 hexazene target with two tolyl substituents and expected formula C18H26B2N6; use charge 0 and singlet multiplicity 1. Extract one covalent molecular component, remove only symmetry-generated duplicates and noncovalently associated crystallographic solvent, and document any hydrogen completion or other deterministic preprocessing. Verify formula, connectivity and B2N6 core before calculation. The target endpoint is a vertical singlet excitation energy (eV) and oscillator strength from the optimized ground-state molecule with dichloromethane represented by a stated continuum or equivalent solvation treatment. Do not consult the paper, SI or general web for computational answers.

# Required scientific validation/investigation

Design and report an independent route, including software/model choices and why they are suitable. Establish molecular identity, charge and multiplicity; show optimization convergence and state whether a frequency/Hessian check was performed. Generate enough low-lying singlet states to identify the state carrying the dominant visible oscillator strength, retain its energy, wavelength if available, oscillator strength and principal orbital-transition character, and show neighboring states or another reproducible basis for calling it dominant. The calculation is complete when the optimized structure passes the stated convergence test and the reported state list makes dominant-state selection reproducible. Stop after this endpoint and validation are complete; if it cannot be completed, submit a bounded-failure report naming the failed stage, evidence, attempted remedies and remaining uncertainty. Report conformer/starting-structure coverage and material limitations.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. It must contain either a completed result with identity, route, convergence, state evidence, dominant excitation and limitations, or a truthful bounded-failure branch with stage-specific diagnostics and no fabricated endpoint values. Include provenance for CCDC retrieval and deterministic preprocessing.
