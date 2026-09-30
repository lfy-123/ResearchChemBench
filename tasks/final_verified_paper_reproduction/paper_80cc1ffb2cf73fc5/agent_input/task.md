# Scientific objective

For the supplied Z1 mHBDI system, report the calculated S0 anion and D0 neutral-radical structures or clearly identify the accepted input structures, harmonic normal modes, a scaled/convoluted vibronic peak representation, and a comparison with the 19,400–20,100 cm^-1 physical window. The public package supplies the measured black trace extracted from the published vector figure in `experimental_spectrum.csv`, with extraction limitations in its metadata. Compare relative prominent features using a declared peak-selection rule, recording the actual matched and unmatched peaks.

# Author-provided scientific guidance

Using the supplied 27-atom Cartesian structure of the singlet Z1 mHBDI anion, independently plan and perform calculations that test the authors' qualitative proposal that anion-to-neutral-core Franck–Condon activity explains prominent cryogenic action-spectrum structure near electron detachment. The author hypothesis is only that a low-energy neutral-core vibration may dominate the progression; do not assume its identity or the result.

# Public inputs and scientific boundaries

Public inputs are `data/inputs/z1_anion.xyz` (27 atoms, Angstrom coordinates, charge −1, singlet) and `data/inputs/problem_definition.json`, together with the experimental spectrum CSV and metadata. The neutral is the same nuclear connectivity after removal of one electron, with charge 0 and multiplicity 2. The research object is the isolated gas-phase Z1 system and the S0→D0 FC transition. The measured boundary is the action spectrum from 19,400 to 20,100 cm^-1, with features below and above the detachment threshold interpreted as bound and resonance channels. You may choose software, model chemistry, optimization strategy, frequency scaling, broadening and alignment, but must state them and their rationale. Do not use the paper, SI or general web during the investigation.

The supplied anion coordinates originate from a source-optimized structure and define the given initial-state object. They do not provide the neutral-radical geometry, normal modes, Franck–Condon factors or the dominant progression assignment to be determined.

# Required scientific validation/investigation

Establish atom count, charge, multiplicity and connectivity before calculation. Generate and retain an auditable anion minimum and a neutral-radical structure with the same connectivity; if optimization is not completed, identify the supplied geometry actually used. Validate each claimed minimum with a frequency calculation or an explicitly justified alternative, reporting imaginary frequencies and the mode convention. Compute or otherwise derive a finite, explicitly listed set of low-energy normal modes and FC transitions; deduplicate coincident peaks and state the peak-selection rule. Align spectra using a declared rule, compare the supplied experimental observations, retaining unmatched features and any unreliable matches, and identify the mode(s) whose displacement/intensity best support the progression.

Use the experimental lowest-resonance origin (19444 cm^-1) as the relative observed zero and your own calculated 0-0 transition as the relative calculated zero. Determine the required translation from your calculation; no author-computed translation is supplied. Compare the prominent spacings/features, not absolute detachment accuracy; this is the Z1-only comparison, not a two-isomer fit. Identify active modes by physical displacement/FC evidence rather than a mandatory integer index. Do not claim unavailable observations or fabricate error bars. An evidence-based disagreement is a legitimate submission, but is not automatically a successful reproduction of the reference interpretation.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include calculation provenance, input identity, structures or structure references, mode and peak tables, alignment, validation evidence, comparison metrics, a conclusion. A successful report must state whether the calculated spectrum supports the proposed FC explanation and which mode is most strongly implicated; a bounded-failure report must state exactly which validation or calculation was unavailable, what was completed, and why the conclusion is limited.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
