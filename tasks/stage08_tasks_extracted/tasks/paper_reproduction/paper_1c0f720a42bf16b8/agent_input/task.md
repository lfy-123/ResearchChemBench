# Scientific objective

For the isolated neutral singlet molecule C1 supplied in `data/inputs/c1_identity.json`, independently characterize its optimized ground and first singlet excited states and the low-energy electronic absorption response. Determine whether the computed electronic structure supports a predominantly local pi-to-pi-star excitation or a substantial donor-to-acceptor charge-transfer contribution. The measured quantities are energies/gaps (eV), wavelengths (nm), oscillator strengths (dimensionless), orbital-transition composition (%), dipoles (D), and explicitly defined dihedral angles (degrees).

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that C1's absorption is dominated by a bright first singlet excitation with predominantly HOMO-to-LUMO pi-to-pi-star character. They use geometry and dipole changes alongside orbital distributions to assess whether the excitation is localized or has a substantial charge-transfer contribution.

**Candidate route or mechanism.**
Test the HOMO-to-LUMO pi-to-pi-star assignment as the leading candidate, and compare it with a donor-to-acceptor charge-transfer interpretation. Examine the N,O-chelated BF2 chromophore and the donor-containing aryl portion when assigning localization and charge redistribution.

**Discriminating evidence.**
Use the vertical singlet excitation energies, oscillator strengths, orbital-transition percentages, HOMO/LUMO distributions, ground and first-excited-state dipoles, and selected chelate torsions. State how these observables support or weaken the competing localized-excitation and charge-transfer interpretations.

# Public inputs and scientific boundaries

The only molecular input is the explicit C1 SMILES, formula C17H16BF2N2O, neutral charge, and singlet multiplicity in `data/inputs/c1_identity.json`. It represents one isolated molecule in the gas phase. The scored system is the isolated molecule; do not add a host, solvent, counterion, aggregate, crystal, or experimental correction. You may generate 3-D geometries and use any available quantum-chemistry software. Define every atom ordering and dihedral used in your report from the supplied connectivity.

# Required scientific validation/investigation

Generate and deduplicate a documented set of starting conformers; state the generation method and coverage. Optimize the lowest-energy neutral singlet ground-state candidate and verify a stationary point with an appropriate frequency or equivalent curvature check. From that state, optimize the lowest relevant singlet excited state and document its state identity and convergence. Compute at least the first 10 singlet excitations (30 is encouraged), identify the lowest bright transition by a stated oscillator-strength rule, and report its wavelength, oscillator strength, dominant orbital transition and percentage. Report HOMO, LUMO, gap, GS/S1 dipoles, and at least two named chelate torsions. The calculation is complete when one candidate has passed geometry/state checks and all requested observables are extracted; stop after that plus a documented conformer search, or report bounded failure with the attempted coverage and the precise missing validation. If multiple plausible electronic interpretations remain, propose them, discriminate them with your computed orbital/transition evidence, and state the limitation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and `report/methods.md`. Include success or bounded-failure status, object identity, conformer coverage, convergence/stationary-point evidence, all observables (or an explicit unavailable list with reason), state/transition assignment, uncertainty or sensitivity discussion, and a concise evidence-based conclusion. Include paths to raw output files or hashes sufficient for audit. A result is complete only when the JSON and methods report are mutually consistent and the stopping condition is stated.
