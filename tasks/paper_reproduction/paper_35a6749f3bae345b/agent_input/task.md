# Scientific objective

Independently test the authors' qualitative proposal that the DBC core and para-aryl-substituted N-phenyl unit form a moderately twisted chromophore with predominantly DBC-localized occupied orbitals and aryl-extended accepting orbitals. For the named neutral singlets DBC-Ph and DBC-Nap, calculate S0 and first-singlet S1 geometries, the two explicitly defined inter-ring dihedrals, and vertical singlet transitions on the optimized states. Compare substituents and state whether the calculations support the proposal.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json` and its two complete XYZ files (DBC-Ph C32H21N, 54 atoms; DBC-Nap C36H23N, 60 atoms). The XYZ atom order is authoritative; do not infer identity from an internal label. Both molecules are neutral, closed-shell singlets initially. The physical boundary is one isolated molecule in implicit toluene, S0 and the first singlet S1, with vertical electronic transitions evaluated at optimized geometries. Report wavelengths in nm, oscillator strengths dimensionless, and dihedrals in degrees. You choose and disclose method, basis, solvent implementation, convergence settings and any conformer generation. The public files contain no target values.

# Required scientific validation/investigation

Plan and execute a reproducible route for both molecules: validate connectivity and charge, optimize S0 and S1 (or provide a scientifically justified bounded-failure explanation), and compute transitions at both optimized states. For each molecule, explicitly identify the four atom indices for each dihedral and verify state optimization/convergence and singlet character. Report at least the five lowest singlet transitions or all transitions in the requested window, with wavelength, oscillator strength and dominant configuration where available. Compare orbital localization on DBC versus aryl fragments using a disclosed population or visual criterion. Completion requires either validated results for both molecules or a bounded-failure report that identifies the failed state, attempted settings and limitation; stop after the declared conformer/state attempts are exhausted and no additional validated state changes the reported conclusion.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include calculation provenance, geometries or paths to them, convergence/state checks, per-molecule dihedrals and transitions, orbital-localization evidence, a Ph-versus-Nap comparison, an explicit conclusion about support for the qualitative proposal, and limitations. Numeric values must be your calculations, not copied from the paper.
