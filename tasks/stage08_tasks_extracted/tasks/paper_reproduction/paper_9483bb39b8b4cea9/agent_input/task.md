# Scientific objective

Determine whether a neutral 1:1 p-toluenesulfonyl chloride (TsCl)–tetrahydrofuran (THF) collision complex has an appreciably allowed low-energy charge-transfer vertical excitation consistent with visible absorption. Report excitation wavelength, oscillator strength, transition character, and charge-transfer evidence, and discriminate plausible electronic explanations using independent computation.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the TsCl–THF collision complex can support a solvent-to-substrate charge-transfer excitation relevant to the visible absorption, with electron density transferred from THF toward an electron-deficient TsCl site and into an S–Cl antibonding orbital. Treat this as the author’s proposed interpretation to test within the stated isolated-complex objective.

**Candidate route or mechanism.**
Prioritize candidate noncovalent arrangements in which the THF oxygen approaches the sulfur-centered electron-deficient region of TsCl, and examine whether the resulting low-energy excitation has donor character from THF and acceptor character associated with S–Cl antibonding orbitals. Compare this proposal with at least one plausible non-charge-transfer explanation or alternative arrangement.

**Discriminating evidence.**
Use independent electronic-structure calculations together with transition-orbital or orbital-character analysis and fragment-resolved population, density-difference, or equivalent charge-transfer analysis. Changes in excited-state polarity or fragment charge may support the interpretation, while geometry, minimum validation, and method sensitivity should be used to assess whether the assignment is robust.

# Public inputs and scientific boundaries

Use `data/inputs/system.json`, `tscl.smi`, and `thf.smi`. The system is one neutral singlet TsCl molecule plus one neutral singlet THF molecule, total charge 0 and multiplicity 1. Construct only noncovalent collision complexes; do not model a covalent reaction product, radical pair, bulk solvent, or time-dependent dynamics. The experimental comparison boundary is the reported visible absorption region 365–400 nm for TsCl in THF under irradiation. The scored state is a vertical excitation from the optimized complex ground state. No author mechanism, selected conformer, software, model chemistry, or numerical answer is supplied.

# Required scientific validation/investigation

Propose and test plausible arrangements and electronic explanations for the visible excitation. Generate multiple chemically distinct initial arrangements by varying donor/acceptor contacts and orientations, optimize each with a documented method, and deduplicate using a stated geometry criterion. Retain only genuine minima (no imaginary frequency, or an equivalent defensible minimum test) and preserve each candidate's identity. Advance at least one representative candidate to an excited-state calculation that reports wavelength, oscillator strength, and orbital/state character. Validate CT by a stated population, density-difference, orbital, or equivalent analysis that distinguishes donor and acceptor fragments, and compare against at least one non-CT alternative or explain why it was not computationally accessible. Completion requires either a converged validated spectrum for at least one defensible minimum plus coverage and sensitivity discussion, or a bounded failure report explaining which step prevented completion. Stop when independent restarts no longer yield a new minimum within the stated search scope, or when the chosen computational budget is exhausted; in the latter case report the limitation and coverage.

# Deliverables

Submit `report/results.json` conforming to the schema. Include candidate identities and validation status, the selected candidate selector, computed excitation observables, transition/CT analysis, comparison with the experimental band, alternative-hypothesis analysis, method/convergence metadata, and a conclusion. Numeric values must be accompanied by units and provenance. A bounded-failure branch is allowed and must still state attempted scope, failure reason, and limitations.
