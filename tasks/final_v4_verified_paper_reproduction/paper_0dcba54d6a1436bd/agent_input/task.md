# Low-energy absorption of three substituted carbazole molecules

## Scientific question

How do NPCZCS, AQCZCS and PQCZCS differ in their low-energy vertical singlet excitations in dichloromethane, and how does the appended acceptor influence their electronic excitation character and absorption intensity distribution?

## Input files

`data/inputs/systems.json` defines the complete neutral Z molecular identities, formulas and singlet ground states. Retain all named alkyl substituents. The author baseline and comparison values for reproduction are disclosed below.

## Scope

Compare molecular absorption from physically justified relaxed ground-state geometries with a declared dichloromethane representation. Define S1 as the actual lowest singlet excited state and distinguish its vertical excitation energy from an orbital gap, a higher bright transition or an emission energy. A state index alone does not establish correspondence across models. Choose methods and explanatory tests independently. Restrict conclusions to these three molecules and solution absorption; aggregate, solid-state, emission-rate and device behavior are outside the question.

## Author baseline for reproduction

The source optimizes gas-phase ground states with B3LYP/6-31G(d,p), without symmetry constraints, and reports frequency checks with no imaginary modes (main p7). Its TD-DFT comparison uses Gaussian 09W, 6-31G(d,p) and PCM dichloromethane. B3LYP, CAM-B3LYP, M06, M06-2X, M06-HF and omegaB97XD are compared for NPCZCS/AQCZCS; the authors select M06 for subsequent analysis, including PQCZCS. Reproduce the disclosed structural and M06 excitation baseline, addressing the source functional-selection comparison where relevant to a claim about that selection. SI Tables S7–S9 give S1 energies/oscillator strengths of 2.9521 eV/0.4988 for NPCZCS, 2.5853 eV/0.1928 for AQCZCS and 2.4342 eV/0.0116 for PQCZCS. Tables S5/S6 instead list major bright transitions: 375.88 nm/0.8847 (NP, S2), 382.38 nm/1.0178 (AQ, S4), and 379.86 nm/1.0397 (PQ, S5); these are not S1 values. Main p8 and Figure5 interpret NP/AQ S1 NTO hole density on the carbazole–cyanostilbene region and particle density on the appended group as ICT, while PQ S1 is described as locally excited on phenanthraquinone. This distinction qualifies the broader ICT wording in the preceding discussion; assess it rather than assuming every low state is CT. Source ground-state HOMO–LUMO gaps are different observables from these excitation energies. NPCZCS has an unresolved internal source discrepancy: main physical p8 Figure5A labels HOMO −5.86 eV and LUMO −1.88 eV, whose arithmetic difference is 3.98 eV, but the same figure prints a 3.54 eV gap and main p7 also states 3.54 eV. Preserve both accounts without choosing a true value or silently correcting the source. These are orbital-gap source statements, not singlet excitation energies or mandatory numerical score targets. A transparent report of the conflict and independently supported results must not be penalized for missing either number; reporting the conflict alone does not replace the required molecular excitation investigation. Fixed-angle scans, ten-state windows, a common three-fragment partition and a mandatory second functional were V1 benchmark extensions, not a source reproduction protocol. Neither those extensions nor source numerical agreement alone establishes the broader solid-state emission mechanisms.

Reproduce this disclosed baseline or substantiate a physically applicable substitute and its consequences. Source values and assignments are comparison references; copied values alone earn no credit. Additional comparisons remain your choice.

## Required results

1. Report the S0→S1 vertical excitation energy in eV for each molecule and compare the three values under compatible definitions.
2. Establish for each molecule how the low-energy excitation relates to the stronger absorption transitions, using computed transition energies and intensities.
3. Determine the spatial character of the relevant low-energy singlet excitations, with state-resolved evidence and explicit treatment of any close-state mixing or reordering.
4. Explain how the acceptor-specific electronic structure connects the excitation character to the distinction between absorption onset and the dominant band. State the physical scope supported by that explanation.

## Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link the native inputs, outputs and analysis that support each final result. State identities, physical definitions, units, uncertainty and the limits of the modeled system. Unsupported guesses, copied observations and workflow completion earn no scientific points. Use only the supplied public inputs and available tools; general scientific/software documentation is allowed. The full target article/SI, private evaluation files and prior verification archives are not public resources. Any author baseline explicitly disclosed in this task is authorized.
