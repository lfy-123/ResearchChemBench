# Scientific objective

Determine computationally how replacing the terminal phenyl ring of DBC-Ph with a 1-naphthyl group in DBC-Nap changes ground- and first-singlet-excited-state geometry, vertical singlet spectroscopy and frontier-orbital localization in toluene. Establish whether the calculated differences provide a defensible structure–property explanation within the stated model boundary.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that moderate twisting between the DBC core and the para-aryl-substituted N-phenyl unit permits predominantly local excitation with partial intramolecular charge transfer. Their structure–property interpretation associates occupied frontier orbitals mainly with DBC and accepting orbitals extending onto the substituted N-phenyl unit.

**Candidate route or mechanism.**
Test the proposed low-energy excitation from a DBC-centered occupied orbital into an orbital shared by the DBC and substituted N-phenyl fragments: a locally excited π–π* contribution combined with partial charge transfer from DBC toward the aryl unit. Consider how inter-ring twisting and relaxation from S0 to S1 affect this interpretation in the Ph-versus-Nap comparison.

**Discriminating evidence.**
The authors used DFT state optimizations and TD-DFT vertical transitions, together with frontier-orbital plots and fragment contributions. Relate the two inter-ring dihedrals to occupied/accepting orbital overlap and fragment localization, and use transition configurations and oscillator strengths at the optimized states to assess whether the proposed local-excitation/partial-charge-transfer picture is supported.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json` and its two XYZ files. The XYZ atom order is authoritative; do not infer identity from an internal label. Both molecules are neutral, closed-shell singlets initially. The physical boundary is one isolated molecule in implicit toluene, S0 and the first singlet S1, with vertical electronic transitions evaluated at optimized geometries. Choose and disclose method, basis, solvent implementation, convergence settings and any conformer generation.

# Required scientific validation/investigation

Independently formulate and execute a reproducible computational comparison for both molecules: validate connectivity and charge, optimize S0 and S1 (or provide a scientifically justified bounded-failure explanation), and compute transitions at both optimized states. Explicitly identify the four atom indices for each dihedral and verify state optimization/convergence and singlet character. Report at least the five lowest singlet transitions or all transitions in the requested window, with wavelength, oscillator strength and dominant configuration where available. Use a disclosed population or visual criterion to assess orbital localization. Completion requires either validated results for both molecules or a bounded-failure report identifying the failed state, attempts and limitation; stop after the declared conformer/state attempts are exhausted and no additional validated state changes the conclusion. Propose and discriminate at least one plausible explanation for any substituent-dependent difference.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include provenance, geometries or paths, convergence/state checks, per-molecule dihedrals and transitions, orbital-localization evidence, the independent Ph-versus-Nap comparison, a final conclusion and limitations. Do not claim experimental or literature validation beyond what you compute and explicitly identify.
