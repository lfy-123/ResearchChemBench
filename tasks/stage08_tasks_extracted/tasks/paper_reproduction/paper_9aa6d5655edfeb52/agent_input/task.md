# Scientific objective

Independently compute and interpret the frontier-orbital and low-energy singlet optical properties of neutral singlet compound 2a from the supplied structure. Determine the HOMO and LUMO energies, their gap, and the lowest reported vertical singlet excitation energy and wavelength, then assess what the computed transition contributions support about the electronic origin of the absorption.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the arene-fusion pattern controls acceptor-orbital stabilization and the frontier-orbital gap. Their structure–property interpretation links the naphthyl C–B fusion in 2a to these electronic effects.

**Candidate route or mechanism.**
Test the proposed assignment of the lowest-energy singlet absorption as principally a HOMO→LUMO excitation, using the computed orbital character and contributions to assess that assignment.

**Discriminating evidence.**
The authors use ground-state DFT orbital energies and electron-density distributions together with TD-DFT vertical singlet energies, oscillator strengths, and orbital-configuration contributions. Relating the frontier gap to the lowest singlet excitation and inspecting the contributing orbitals provides evidence for assessing the proposed absorption origin.

# Public inputs and scientific boundaries

The object is C(1),B(3)-(naphthalene-1,8-diyl)-C(2)-phenyl-1,2-dicarba-closo-dodecaborane (2a), formula C18H20B10, charge 0, multiplicity 1. Use `data/inputs/2a.xyz` exactly as the starting ordered Cartesian structure and `data/inputs/system.json` for identity and boundary. The calculation concerns an isolated molecule; implicit solvent is optional, but solvent/model choices must be stated. Do not infer solid-state packing, experimental emission, or a different protonation/isotopologue. The measured quantities are orbital energies/gap and vertical singlet excitation energies, wavelengths, oscillator strengths, and dominant orbital contributions.

# Required scientific validation/investigation

Generate and test your own explanations of the electronic origin of the absorption using the computed transition contributions. Choose and disclose software, electronic-structure method, basis, solvent treatment, geometry protocol, and excited-state protocol. Optimize the ground state (or justify a fixed-geometry alternative), verify charge/multiplicity and absence of an obvious optimization failure, and establish that the reported excitation is a vertical singlet from the stated reference geometry. Deduplicate repeated states and identify the state by energy, wavelength, oscillator strength, and transition contributions rather than by an arbitrary internal label. Report convergence evidence and at least one sensitivity or uncertainty check. The calculation is complete when a reproducible output contains the requested observables, state identity, transition analysis, and validation evidence; stop after the chosen protocol and its declared check(s) are complete, and report limitations if convergence or state assignment cannot be established.

# Deliverables

Write `report/results.json` conforming to the local `submission_schema.json`. Include the structure identity, method, geometry/convergence evidence, orbital energies and gap, an array of singlet excitations with energy/wavelength/oscillator strength and contributions, the selected lowest-singlet record, validation checks, an independent electronic-origin interpretation, conclusion, and limitations. Include units for every numerical quantity and enough provenance to reproduce the calculation.
