# Scientific question

How does arm conformation affect the molecular absorption spectrum of the supplied dye and its single-arm analogue, and how far can those finite-molecule results explain the additional long-wavelength band in dye-loaded quatsomes?

# Input files

- `data/inputs/objects.json`: chemical identities, atom mapping and any supplied starting structures. These do not establish stable states or pathways.
- `data/inputs/observations.json`: known observations; these are context to explain, not new predictions.

# Scope

Use the neutral singlet single-arm C26H27NO3 model and full three-arm C66H69N3O3 chromophore defined in `objects.json`. Compare transoid and cisoid arrangements of the conjugated arm, identified by the neutral torsion definitions in that file; neither arrangement is assumed to be a stable free minimum or the experimental photoproduct. The optical comparison is vertical singlet absorption from S0 at the declared molecular geometry in the gas phase. Report any constraints and distinguish conditional geometries from freely relaxed states. Known observations are an additional approximately 700 nm absorption band, its persistence after ethanol dilution (1:30 v/v), and its increase under ambient light. Finite molecular spectra do not establish vesicle structure, irreversible photochemical kinetics, two-photon brightness or imaging performance.

# Required results

1. Report the S0→S1 vertical absorption energy (eV) and dimensionless oscillator strength for each single-arm conformational candidate. For each three-arm candidate, report the corresponding quantities for S1–S4, assigning roots by energy and checking physical state correspondence.
2. Explain the conformational spectral change using calculated state character and assess its relation to the approximately 700 nm observation. Distinguish a possible contribution from quantitative reproduction or unique identification of the band origin, and state the implications of the molecular geometry actually represented.
3. Explain which single-arm optical behavior transfers to the full dye and which requires the full chromophore, using comparative transition/state evidence.

Choose computational methods and explanatory models independently. Support each answer with actual calculations or executed quantitative analysis. Define molecular states, units, energy references and conditions. Geometry, frequencies or connectivity evidence must support the claims that depend on them; no fixed search procedure or number of calculations is required.

# Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link reported quantities and claims to preserved inputs, native outputs and analysis artifacts. The existing record fields document provenance and earn no separate points. Use the supplied public inputs. Private evaluation files and other-mode or previous-run archives are not permitted inputs.
