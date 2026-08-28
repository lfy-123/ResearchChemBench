# Scientific objective

Determine the low-spin vertical UV–vis excitations of the supplied 65-atom first-coordination-sphere Fe(II) model of compound 1. Independently plan calculations that test the authors' qualitative proposal that metal-centered MLCT and Fe d–d states can overlap ligand fluorescence and promote nonradiative transfer. Report salient transition wavelengths, oscillator strengths, state assignments, and whether the computed spectrum supports that proposal.

# Public inputs and scientific boundaries

The only scientific input is `data/inputs/compound1_ls.xyz`: 65 atoms, Cartesian coordinates in Å, one Fe, N/C/H atoms, and the charge-neutral LS local model encoded by the supplied protonated cyanide hydrogens. Treat it as an isolated first-coordination-sphere model, not a periodic framework. The measured quantities are vertical excitation wavelength (nm), oscillator strength (dimensionless), and electronic character. You may generate conformers or relaxations, but must identify the submitted geometry and spin/charge assumptions. Do not use the paper, SI, general web, or unpinned databases.

# Required scientific validation/investigation

Choose and justify a reproducible electronic-structure route. Establish that the geometry, charge, multiplicity and excited-state calculation are converged or explain limitations. Examine enough low-energy states to cover 350–700 nm, deduplicate states by energy/character, and advance a band assignment only when wavelength and orbital/NTO or equivalent transition-density evidence support it. Validate at least one metal-centered and one ligand-centered assignment and compare the salient bands with the 400–650 nm fluorescence-relevant window. Completion requires a machine-readable result with status `success` or `bounded_failure`; every reported band must include a unique identifier, wavelength, oscillator strength, assignment, evidence, provenance and wavelength uncertainty. Stop when the stated spectral window is covered, convergence/validation checks are documented, and additional states or reasonable numerical settings no longer change the salient assignments; otherwise report bounded failure and the coverage limitation.

# Deliverables

Submit `report/results.json` and any supporting files declared there. The JSON must contain model/protocol, validation, a status, a coupling conclusion and limitations. A `success` result contains at least one validated band. A `bounded_failure` result may contain zero or more partially validated bands, but must include `failure_details` with attempted coverage, failed checks and coverage limitation; it must not fabricate missing numerical results.
