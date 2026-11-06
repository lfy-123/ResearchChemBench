# Scientific question

Which molecular changes explain the supplied acid–base optical and NMR responses of dye 2a, and how specifically can the joint evidence identify the responsive species?

## Input files

- `data/inputs/parent_identity.json` supplies the neutral C30H20N6O4 molecular graph and atom mapping. Preserve its C30N6O4 heavy-atom skeleton.
- `data/inputs/observations.json` supplies aqueous absorption maxima at pH 2 and 14 and the aromatic-proton NMR signals adjacent to phenolic groups under nominal acid/neutral/base conditions, referenced to TMS in the DMSO comparison. These observations are known facts to explain.
- `data/inputs/problem_context.json` summarizes the problem, input limitations and available-resource boundary.

## Scope

Study reversible molecular acid–base response, allowing chemically admissible proton exchange and internal proton/bond rearrangement. Choose the responsive species and the comparisons needed to test their explanatory power. Map added, removed and relocated protons and state total charge, electron count and spin. Keep water optical response distinct from DMSO NMR and its reference. Synthesis, degradation, redox chemistry and sensor-device performance are outside the question.

## Required results

- Explain the absorption change with calculated dominant transition energies, intensities and electronic character in water. Report energies in eV or wavelengths in nm and define the solvent-response convention used.
- Determine the calculated acid-versus-neutral and base-versus-neutral changes for the mapped aromatic protons adjacent to phenolic groups. Report all corresponding proton shifts in ppm, the solvent/reference and any averaging convention, and assess their relation to the observations.
- Test whether a chemically admissible neutral internal proton/bond rearrangement can account for the principal switch without net proton exchange. Give discriminating computed evidence for the conclusion; the absence of a tested alternative is not evidence of exclusion.
- Give the responsive-species assignment supported jointly by the optical and local NMR evidence. Explain which functionality and proton/charge changes are identified and which site/population details remain unresolved, including any quantitative model–observation mismatch.

Different proton counts require a balanced proton reference for any population thermodynamics. A single matching peak cannot establish a unique protonation site. Evidence must support the claimed degree of identification, without a fixed candidate count, conformer count or control matrix.

## Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link actual model identities, native calculations and reproducible analyses to the final answers, retaining distinct physical states, solvents and reference conventions. Only final scientific results receive points. Use the supplied public inputs and tools/resources exposed by the runner; report partial or failed work honestly.
