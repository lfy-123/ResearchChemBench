# Iridium nitrato molecular structure and IR

## Scientific question

What nitrate coordination and molecular bonding description can explain the IR observations of neutral singlet IrCl2(NO3)(PPh3)2, and which band interpretations remain unresolved?

## Input files

- `data/inputs/complex_specification.json` defines the full 75-atom composition, charge, spin and intact ligand identities; it leaves metal coordination and ligand placement to be investigated.
- `data/inputs/experimental_ir.json` provides unassigned KBr band positions (cm^-1), qualitative strengths and two differing accounts of a high-frequency feature. These are given observations to explain.

## Scope

Study the full isolated molecular complex and distinguish that environment from the KBr measurement. Choose and justify molecular models and calculations. Keep molecular coordination, individual mode assignments and solid-state conclusions separate. The required question is molecular structure/vibrational interpretation; it does not require a formation mechanism, electrochemistry, CO/NO chemistry, an exhaustive candidate search or a global IR-only uniqueness proof.

## Required results

1. Determine the nitrate coordination and relative donor arrangement supported by your model, with mapped bond lengths in Å and angles in degrees.
2. Explain how the intranitrate bond pattern relates to its stretching motions. Report calculated frequencies in cm^-1, IR intensities with their units, and the physical mode assignments; distinguish raw and any corrected frequencies.
3. Interpret the calculated mode character near each supplied 1261, 1223 and 802 cm^-1 observation. Explain the supported correspondence and mismatches without treating nearest-frequency coincidence as an assignment.
4. Assess the high-frequency observations at 1532 and 1561 cm^-1 using actual mode character and activity, keeping their differing reported status visible.
5. State what these comparisons establish about the measured spectrum and what remains unresolved when moving from an isolated molecule to KBr.

## Author baseline for reproduction

The source uses Gaussian09/WebMO B3LYP/LANL2DZ optimization and IR for the full complex (main p7). Reproduce that molecular baseline or justify a comparable implementation. Crystallography assigns eta2 nitrate and approximately trans chlorides; crystal Ir–O distances are 2.173(2)/2.174(2) Å, the bite angle is 60.02(9)°, and N–O distances are 1.294/1.291/1.209 Å (main pp3–4, Fig4/Table2; SI pp15–16). These are disclosed experimental references, not your computed outputs.

The printed calculated nitrate bands are 1541, 1102 and 926 cm^-1. The source mentions frequency correction but does not disclose an unambiguous numerical factor. Keep raw calculation and printed reference distinct and do not fit a factor to force agreement. The detailed band list and discussion differ at 1561/1532 cm^-1. Known crystal coordination does not make IR alone unique. Extra coordination-isomer searches are optional extensions, not author requirements.

## Submission

Submit `report/results.json` and `report/report.md` following `submission_guide.md` and `submission_schema.json`. Support final answers with inspectable native calculations and reproducible analyses. Final scientific results total 100 points; research-process completion carries no independent points. Use supplied inputs and available tools; general scientific/software documentation is allowed. Private evaluator files, prior verification archives and undisclosed target-paper answers are not public resources.
