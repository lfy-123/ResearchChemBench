# Scientific objective

Independently test the authors' qualitative proposal that acid/base protonation of phenolic dye 2a changes its electronic absorption profile. Calculate vertical low-lying singlet excitations for the supplied 2a-acid and 2a-base S0 geometries, report excitation energies (eV) and oscillator strengths, identify the brightest state in each four-state set, and explain whether the profiles support a bathochromic acid/base switch. The author hypothesis is disclosed only as a qualitative route: protonation/deprotonation changes the electronic structure and hence the absorption; do not assume any numerical result or state ordering.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that changing phenolic protonation in dye 2a changes its electronic structure and thereby its absorption profile, providing a qualitative acid/base optical switch.

**Candidate route or mechanism.**
Compare the doubly protonated phenolic acid form with the doubly deprotonated phenolate base form through their low-lying singlet electronic excitations. The proposed interpretation is that protonation-driven changes in the conjugated azobenzene/iso-diketopyrrolopyrrole electronic system can alter the character and energy of the prominent transitions, including π–π* and charge-transfer contributions.

**Discriminating evidence.**
Use gas-phase vertical excited-state calculations on the supplied ground-state structures, retaining S1–S4 energies, oscillator strengths, and state identities. Compare the complete profiles and the oscillator-strength-selected bright transitions; orbital or transition-character analysis may help distinguish a change in electronic character from a simple uniform spectral shift.

# Public inputs and scientific boundaries

Use `data/inputs/2a-acid.xyz` and `data/inputs/2a-base.xyz`. Each is an XYZ file in angstroms containing the complete SI S0 geometry: 62 atoms for 2a-acid and 58 atoms for 2a-base. Treat acid as formal charge +2, singlet multiplicity 1, and base as formal charge −2, singlet multiplicity 1. The systems are isolated molecules in the gas phase. The endpoint is vertical electronic excitation from these supplied geometries; do not add solvent, counterions, vibronic structure, experimental band fitting, or NMR calculations to the scored endpoint. You may optimize or verify geometries, but must disclose any change. The measured objects are S1–S4 singlet excitation energies and dimensionless oscillator strengths for each named structure.

This is a fixed-structure property track: the supplied coordinates are public inputs for the named property comparison, not a scored structure discovery answer. Do not claim that the input geometry itself was rediscovered; report any optimization or conformer search separately.

Result identity contract: use name="2a-acid" and name="2a-base", each exactly once in the structures array. Array order is arbitrary; all state tables and brightest-state selectors are matched by name, never by array position. Keep each record with its own charge, multiplicity and source geometry.

# Required scientific validation/investigation

Plan and execute a defensible electronic-structure calculation, independently choosing software and model chemistry and disclosing them. Validate atom count, element order, charge, multiplicity, geometry provenance, convergence, and that at least four singlet states were computed for each named structure. Select the brightest state as the member of that structure's S1–S4 set having the largest oscillator strength; retain state labels and per-state evidence rather than reporting only an aggregate. Compare the two profiles and state whether the calculated evidence supports the qualitative switching hypothesis, distinguishing gas-phase vertical excitation from experiment. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus any referenced calculation outputs or scripts under `report/`. The JSON must include method disclosure, per-structure validation, four-state results when available, brightest-state selectors, comparison/conclusion. Do not copy the paper or SI into the report.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
