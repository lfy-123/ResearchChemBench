# Scientific objective

Using the supplied 27-atom Cartesian structure of the singlet Z1 mHBDI anion, independently determine whether an anion-to-neutral-core Franck–Condon calculation can account for prominent cryogenic action-spectrum structure near electron detachment. Report the calculated S0 anion and D0 neutral-radical structures or clearly identify the accepted input structures, harmonic normal modes, a scaled/convoluted vibronic peak representation, and a comparison with the 19,400–20,100 cm^-1 physical window. Compare observations available from the supplied inputs without inventing observed peak positions; if pointwise observations cannot be extracted, report that limitation and compare calculated coverage and relative progression qualitatively. Formulate and discriminate plausible explanations for any agreement or mismatch, generating and testing your own pathways or explanations.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that anion-to-neutral-core Franck–Condon activity can account for prominent near-detachment structure, with a low-energy vibration of the neutral core potentially dominating the observed progression. Their interpretation concerns threshold-near bound and resonance behavior, but does not establish a unique microscopic explanation for every feature.

**Candidate route or mechanism.**
Treat the S0 anion to D0 neutral-radical change as the candidate structural pathway and test whether displacement along a low-energy in-plane bending coordinate can produce a strong vibronic progression. Consider the possibility that the same FC pathway explains only the prominent structure while additional bands arise from other structural or electronic contributions.

**Discriminating evidence.**
Use optimized or accepted anion and neutral structures with harmonic-frequency validation, then evaluate mode displacements, FC transition intensities, and a declared scaled/convoluted spectrum across the stated window. Distinguish the candidate explanation from alternatives by checking peak coverage, relative progression, and the stability of the mode assignment under reasonable alignment, scaling, broadening, or structural choices.

# Public inputs and scientific boundaries

Public inputs are `data/inputs/z1_anion.xyz` (27 atoms, Angstrom coordinates, charge −1, singlet) and `data/inputs/problem_definition.json`. The neutral is the same nuclear connectivity after removal of one electron, with charge 0 and multiplicity 2. The scored system is the isolated gas-phase Z1 molecule; do not add a host or solvent. The scored transition is S0 anion → D0 neutral radical, and the action-spectrum window is 19,400–20,100 cm^-1, including bound and resonance channels relative to electron detachment. You may choose software, model chemistry, optimization strategy, frequency scaling, broadening and alignment, but must state them and their rationale. Use the supplied public inputs and your declared computational methods during the investigation.

# Required scientific validation/investigation

Establish atom count, charge, multiplicity and connectivity before calculation. Generate and retain an auditable anion minimum and a neutral-radical structure with the same connectivity; if optimization is not completed, report the starting-geometry limitation. Validate each claimed minimum with a frequency calculation or an explicitly justified alternative, reporting imaginary frequencies and the mode convention. Generate a finite, explicitly listed set of low-energy normal modes and FC transitions; deduplicate coincident peaks and state the peak-selection rule. Compare available observations or explain why pointwise matches cannot be extracted, and propose and discriminate at least two plausible causes for agreement or mismatch using your computed evidence. Stop when the stated spectral window has been searched, the selected explanation and peak/mode assignment are validated by the reported evidence, and additional candidates or alternate settings no longer change the conclusion; if this cannot be achieved, provide a bounded-failure report with coverage and the next discriminating calculation.

# Deliverables

Write `report/results.json` conforming to the local `submission_schema.json`. Include calculation provenance, input identity, structures or structure references, mode and peak tables, alignment, validation evidence, compared hypotheses, a conclusion and limitations. A successful report must state the best-supported explanation and mode/peak evidence; a bounded-failure report must state exactly which validation or calculation was unavailable, what was completed, and why the conclusion is limited. Include every result key required by the local schema and do not require mode-specific keys that the local schema does not define. Include every result key required by the local schema and do not require mode-specific keys that the local schema does not define.
