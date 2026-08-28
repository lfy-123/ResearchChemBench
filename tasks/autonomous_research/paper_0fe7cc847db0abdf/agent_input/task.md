# Scientific objective

Determine, by an independent computational investigation, the adiabatic S0–T1 energy gap for each of three explicitly supplied cationic Ir(III) complexes (Ir1, Ir2 and Ir3), and decide whether the resulting energetics are compatible with sensitization of singlet oxygen under the stated energetic criterion. Compare ligand-dependent trends only after computing and validating the states; do not assume a mechanism, ranking, or result direction in advance.

# Public inputs and scientific boundaries

`data/inputs/Ir1.xyz`, `Ir2.xyz`, and `Ir3.xyz` are XYZ geometries with element symbols and Cartesian coordinates in Å. Ir1 is [(η5-Cp*)Ir(1,10-phenanthroline)Cl]+; Ir2 contains 5-nitro-1,10-phenanthroline; Ir3 contains 5-amino-1,10-phenanthroline. The PF6− counterion is excluded and each cation has net charge +1. Use singlet multiplicity 1 for S0 and triplet multiplicity 3 for T1. The boundary is electronic-state energetics of these isolated cations, with any solvent treatment explicitly reported. Do not infer biological potency, photochemical yield, or a unique mechanism from the gap alone.

# Required scientific validation/investigation

Plan and execute an independent, reproducible search for the relevant S0 and T1 states for all three named molecules. Define the finite set of starting geometries, state optimizations and any conformer or spin checks; deduplicate equivalent structures and retain identity for every attempted state. Validate charge, multiplicity, convergence, minimum character when possible, and state assignment. Compute E(T1 minimum) − E(S0 minimum) in eV using a declared consistent convention. Test the 0.98 eV energetic criterion and discriminate plausible interpretations from the computed evidence rather than assuming one. Completion requires a gap or bounded failure record for each of Ir1–Ir3, full coverage and validation reporting, and a conclusion that states uncertainty. Stop when the declared starting-state/state search is exhausted or when additional attempts no longer change the assigned state under the documented convergence and deduplication rules; disclose any limitation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Provide per-complex candidates/attempts with identities, energies, validation evidence and selected states, numerical gaps when defensible, a comparison with the 0.98 eV criterion, and an independent conclusion. A bounded-failure branch is allowed and must state what was attempted and why a gap is not defensible. Include auditable report/log paths under `report/`.
