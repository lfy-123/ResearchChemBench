# Scientific question

How do the molecular electronic properties of 2BT-TTA, 2BF-TTA and 2(C8Ph)-TTA differ, and what can those differences establish about their interaction with SWCNTs and the measured composite performance?

# Input files

- `data/inputs/2BT-TTA_identity.json`, `2BF-TTA_identity.json` and `2C8Ph-TTA_identity.json` provide complete mapped molecular graphs. Use neutral singlets: C26H12S6 (44 atoms), C26H12O2S4 (44 atoms) and C38H44S4 (86 atoms), respectively. Preserve both full octyl chains in 2(C8Ph)-TTA.
- `data/inputs/problem_context.json` gives film preparation, loading and power-factor observations, nanotube material specifications, a nominal electronic comparison reference and available-resource boundaries. The film measurements are given observations to interpret.

# Scope

Calculate isolated-molecule frontier orbital eigenvalues with a consistent vacuum energy reference; report HOMO, LUMO and LUMO−HOMO separation in eV and define the molecular geometry/state. Orbital eigenvalues, ionization energies, optical gaps and work functions are different observables. Relate molecular values to the supplied nominal nanotube reference only within its stated limitations.

The SWCNT sample is commercial XFS22 (>95% purity, 1–2 nm diameter, 5–30 micrometre length) with unspecified chirality and interface ensemble. A chosen microscopic tube is a model, not an identified experimental sample. No fixed chirality, adsorption model or film-transport simulation is required.

# Author baseline for reproduction

The reported baseline is Gaussian 09W B3LYP/6-31G(d) for the full isolated molecules (main pp.3–5; SI Tables S1–S3). Source HOMO/LUMO values are -5.04/-2.14 eV for 2BT-TTA, -5.00/-2.08 eV for 2BF-TTA and -4.99/-1.65 eV for 2(C8Ph)-TTA. Reproduce this disclosed baseline with actual calculations or justify a scientifically comparable implementation, and distinguish a reproduced stationary structure from an adequately validated minimum. The authors compare against a cited SWCNT level of -5.060 eV and propose an electronic/interfacial account of the film observations; critically assess that interpretation. A source value is a comparison reference, not evidence of execution.


# Required results

1. Report the molecular HOMO and LUMO eigenvalues and frontier gaps for all three complete molecules at your stated geometries. For this reproduction mode all six disclosed source eigenvalues are model-specific comparison evidence; assess their physical meaning and geometry dependence; explain the stationarity and applicability of the underlying geometries.
2. Determine how the HOMO, LUMO and gap of 2(C8Ph)-TTA compare with each heteroaryl derivative. Resolve the signs with internally consistent calculations and state the geometry and numerical dependence.
3. Assess what the level alignment permits about electron donation/acceptance and what remains undetermined about transferred charge or carrier type.
4. Relate the calculated molecular comparison to the supplied loading-dependent composite observations. Explain how far it can account for the performance contrast and which distinctions require information beyond molecular descriptors.

# Submission

Submit `report/results.json` and `report/report.md` using the existing schema and guide. Link every computed quantity and inference to genuine native outputs, defined objects and reproducible analysis. Geometry and state validation support those conclusions without independent process points.
