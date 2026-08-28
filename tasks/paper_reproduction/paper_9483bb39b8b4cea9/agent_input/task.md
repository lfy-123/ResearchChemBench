# Scientific objective

Determine whether a neutral 1:1 p-toluenesulfonyl chloride (TsCl)–tetrahydrofuran (THF) collision complex has an appreciably allowed low-energy charge-transfer vertical excitation consistent with visible absorption. The authors qualitatively propose solvent-oxygen organization at an electron-deficient TsCl site and CT into an S–Cl antibonding orbital; independently test that hypothesis. Report excitation wavelength, oscillator strength, transition character, and charge-transfer evidence.

# Public inputs and scientific boundaries

Use `data/inputs/system.json`, `tscl.smi`, and `thf.smi`. The system is one neutral singlet TsCl molecule plus one neutral singlet THF molecule, total charge 0 and multiplicity 1. Construct only noncovalent collision complexes; do not model a covalent reaction product, radical pair, bulk solvent, or time-dependent dynamics. The experimental comparison boundary is the reported visible absorption region 365–400 nm for TsCl in THF under irradiation. The scored state is a vertical excitation from the optimized complex ground state.

# Required scientific validation/investigation

Generate multiple chemically distinct initial arrangements by varying O···TsCl approach and relative orientations, optimize each with a documented method, and deduplicate using a stated geometry criterion. Retain only genuine minima (no imaginary frequency, or an equivalent defensible minimum test) and preserve each candidate's identity. Advance at least one representative candidate to an excited-state calculation that reports wavelength, oscillator strength, and orbital/state character. Validate CT by a stated population, density-difference, orbital, or equivalent analysis that distinguishes donor and acceptor fragments. Completion requires either a converged validated spectrum for at least one defensible minimum plus coverage and sensitivity discussion, or a bounded failure report explaining which step prevented completion. Stop when independent restarts no longer yield a new minimum within the stated search scope, or when the chosen computational budget is exhausted; in the latter case report the limitation and coverage.

# Deliverables

Submit `report/results.json` conforming to the schema. Include candidate identities and validation status, the selected candidate selector, computed excitation observables, transition/CT analysis, experimental comparison, method/convergence metadata, and a conclusion. Numeric values must be accompanied by units and provenance. A bounded-failure branch is allowed and must still state attempted scope, failure reason, and limitations.
