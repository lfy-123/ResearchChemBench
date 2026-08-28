# Scientific objective

Independently determine the adiabatic singlet–triplet gap between the singlet ground state S0 and the lowest triplet state T1 for each explicitly identified cationic complex Ir1, Ir2 and Ir3. Test the authors' qualitative hypothesis that these half-sandwich Ir(III) photosensitizers can sensitize singlet oxygen through a type-II energy-transfer route. The scored observables are one gap in eV for each named complex and the evidence-based energetic interpretation; no paper numerical answer or author protocol is supplied.

# Public inputs and scientific boundaries

`data/inputs/Ir1.xyz`, `Ir2.xyz`, and `Ir3.xyz` are XYZ geometries with element symbols and Cartesian coordinates in Å. Ir1 is [(η5-Cp*)Ir(1,10-phenanthroline)Cl]+; Ir2 is the same cation with 5-nitro-1,10-phenanthroline; Ir3 is the same cation with 5-amino-1,10-phenanthroline. The PF6− counterion is excluded. Each molecule has net charge +1. Treat S0 as singlet (multiplicity 1) and T1 as triplet (multiplicity 3). You may generate conformers or refine geometries, but must identify which public geometry and state each reported number uses. The scientific boundary is electronic-state energetics of the isolated cations, optionally with a stated solvent model; do not claim that a gap alone proves antibacterial activity or an absolute singlet-oxygen yield.

# Required scientific validation/investigation

For every named complex, define a reproducible calculation for S0 and T1, obtain or justify a lowest-state assignment, and compute the adiabatic gap as E(T1 minimum) − E(S0 minimum), using a consistent energy convention and units. Validate S0 and T1 structures as minima when possible (for example by vibrational analysis), check charge/multiplicity and atom identity, and report any failed or approximate validation. Explain how the computed gap bears on the 0.98 eV energetic criterion for oxygen sensitization, without treating that criterion as a complete mechanistic proof. The investigation is complete when all three complexes have either a validated gap or a transparently documented bounded failure, all attempted states and convergence outcomes are recorded, and no additional candidate conformer/state changes the reported assignment under the stated search. Stop after the declared conformer/state set has been exhausted or after a reproducible convergence/validation failure prevents a defensible value; report coverage and limitations.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include a per-complex record for Ir1, Ir2 and Ir3, numerical gaps when obtained, state energies and units, geometry/minimum validation, method summary, and a conclusion tied to the 0.98 eV criterion. Include failed-case records instead of inventing values if a calculation cannot be completed. Also include `report/` evidence or log paths sufficient to audit the calculation.
