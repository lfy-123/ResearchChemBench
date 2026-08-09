# Stage02/Stage03 manual gold set (2026-08-10)

## Scope and decision rules

This gold set was created from the 76 papers that passed the historical Stage02
computational-content run and the 18 papers that subsequently passed the historical Stage03
software gate. Every passed paper was checked against its title, abstract/front matter, main-text
method evidence, all known SI text, and high-recall laboratory/software cue searches.

Stage02 `pure_computational` means that the current paper is original research, its primary
scientific contribution is a molecular/material computational workflow, and the current paper does
not report newly performed physical laboratory work. Reuse or fitting of experimental data from a
previous study is allowed and must not be confused with a current-author experiment.

Stage03 checks required scientific software against all three toolbox layers: predefined Actions,
documented native software, and task-specific Python. Visualization-only software is not a required
scientific engine. An exact private development build, locally modified engine, or unnamed core
runtime is not treated as its public upstream package.

## Stage02 gold labels (all 76 historical passes)

### In-scope pure computational-chemistry candidates (65)

`paper_023f8f2257c721dd`, `paper_0a59e211a25c4a1b`,
`paper_0e82d55e2c8fb3cd`, `paper_112230f9fed12763`,
`paper_2787202acb6aacf2`, `paper_27a191311c42f047`,
`paper_2bd6f5054aa589c3`, `paper_2f7d853847819e55`,
`paper_371f15fb65bd60c3`, `paper_37f7be2eeecd4088`,
`paper_41602c28cd56f3fc`, `paper_493ec44505ce0e5d`,
`paper_4a217ec2ed066e3f`, `paper_4ccc2ef5a8f6dc87`,
`paper_5093edce5947bdc1`, `paper_511cc19067df008b`,
`paper_57df85fa160273e8`, `paper_59d787fdcd19352b`,
`paper_5f0bb2df72cc3768`, `paper_6c26b11ef14b1e06`,
`paper_6de32578632df280`, `paper_726a75e9ac4eff5b`,
`paper_768e15849d5eff5d`,
`paper_781f3d8c77aa4102`, `paper_7970bfff30eb8db0`,
`paper_7a1f440fe7c68e38`, `paper_7b0ebf765f6a6694`,
`paper_80749f52dc2b07bd`,
`paper_83bcb87e982af6fa`, `paper_8404b4663ffbd741`,
`paper_965a2b6ac5174a7b`, `paper_97070aa2ed98af38`,
`paper_97cda0ac846b88c6`, `paper_9a3faa46869eca3c`,
`paper_9e5fb9643ff36dbe`, `paper_9f996b37f4bdb4ac`,
`paper_9fb8e33c60f60e90`, `paper_a2c99c3e95d8fbc8`,
`paper_a47b8a356658bbf4`, `paper_a649709e45bede0b`,
`paper_a94ab9737dd05015`, `paper_b1a6afa839978edb`,
`paper_b4fbe3f83f4f4e1a`, `paper_b975183360fa593f`,
`paper_ba65876100129429`, `paper_bcdc62f8a4ac3cfe`,
`paper_c4f073017ba1bba2`,
`paper_c59dab9c926a0fd3`, `paper_ca1d12b17e9e4e4b`,
`paper_ca32ee4f5baf90e2`, `paper_ca3a39c417bec4b6`,
`paper_cd30860da44e701d`,
`paper_cf0279fd0e9d131c`, `paper_d32c64f62f9a88c7`,
`paper_dea440679364ac58`,
`paper_e1be9a273ef02d41`, `paper_e1c7cc620647cd21`,
`paper_e300e76b3b6d1452`, `paper_e68148717191f0d6`,
`paper_e86c38ea6471168b`, `paper_f130c71a6b965644`,
`paper_f95d34466bfd9110`, `paper_fccb6813a9f5b43b`,
`paper_fec8743274f8d2a8`, `paper_ff8f1526222201cf`.

### Reject as out-of-scope computation (7)

These papers are computational, but their primary workflow is informatics, planning, enumeration, or generic
algorithm development rather than a molecular/material computational-chemistry workflow:

- `paper_7725c7b966d511fe`: structure-prediction-only DNA motif design.
- `paper_7f80c5b293552261`: similarity/template-based chemical-library enumeration.
- `paper_9307307a76677d97`: reaction-condition label ranking.
- `paper_94dcb91052f9b008`: carbohydrate-binding-pocket prediction and annotation.
- `paper_bedf255625361855`: synthesis planning and retrosynthesis prompting.
- `paper_cdbc6b1936a64a03`: quantum-hardware ansatz construction.
- `paper_e1572effc735ecbd`: biological-target prediction from signatures.

Notable boundary decisions:

- `paper_2787202acb6aacf2` models experiments reported by Conk et al.; it does not report a new
  laboratory experiment in the current work.
- `paper_83bcb87e982af6fa` and `paper_371f15fb65bd60c3` use an `EXPERIMENTAL SECTION` publisher
  heading, but the sections contain computational methods only.
- `paper_8404b4663ffbd741` explicitly takes measured spectra from a previous study; its current
  contribution is computational.
- `paper_e300e76b3b6d1452` derives rates from previously generated reaction-dynamics data and runs
  new DFT/RPMD calculations; no new physical measurement is reported in this paper.

### Reject as mixed computational/experimental (2)

- `paper_2b5f254d7a98422b`: current authors performed VtC-RIXS measurements at SwissFEL and also
  performed quantum-chemical calculations.
- `paper_66b56e627be8a80a`: current authors performed Langmuir, DSC, ITC, DLS, and SAXS experiments
  together with MD simulations.

### Reject as non-original article (2)

- `paper_8081455e98678826`: review article; it explicitly says that it highlights advances made
  since earlier reports.
- `paper_d0948819aaeabb4f`: commentary/research highlight describing work reported by another
  group in JACS, rather than an original computational study by the article authors.

## Stage03 gold labels (all 18 historical passes)

| Paper | Upstream eligible | Strict software result | Manual basis |
|---|---:|---|---|
| `paper_2b5f254d7a98422b` | no | not evaluated | Mixed experimental/computational paper. |
| `paper_2bd6f5054aa589c3` | yes | uncovered | Uses a development ORCA build based on ORCA 5; exact runtime is not the public ORCA entry. |
| `paper_371f15fb65bd60c3` | yes | covered | VASP and pymatgen are covered; described graph processing can use task-specific Python. |
| `paper_4a217ec2ed066e3f` | yes | covered | CP2K and Gaussian are covered; VMD is a configured native runtime. |
| `paper_511cc19067df008b` | yes | covered | ORCA is covered; RFT is a described analytic/mnemonic construction suitable for task-specific Python, not a missing program. |
| `paper_59d787fdcd19352b` | yes | covered | OpenMM, MDTraj, Packmol, OpenFF/GAFF workflow is covered. |
| `paper_6c26b11ef14b1e06` | yes | covered | ORCA and Gaussian workflow is covered. |
| `paper_726a75e9ac4eff5b` | yes | covered | VASP workflow is covered. |
| `paper_768e15849d5eff5d` | yes | covered | LAMMPS and Python/NumPy analysis are covered. |
| `paper_8081455e98678826` | no | not evaluated | Review article; Gaussian calculations in attached material do not make it original research. |
| `paper_83bcb87e982af6fa` | yes | covered | Packmol, LAMMPS, CP2K, and PLUMED are covered. |
| `paper_a649709e45bede0b` | yes | uncovered | Requires locally revised/development Gaussian variants not present in the frozen toolbox. |
| `paper_e1c7cc620647cd21` | yes | covered | VASP workflow is covered. |
| `paper_e300e76b3b6d1452` | yes | uncovered | Requires a new surface-RPMD implementation, not merely ordinary VASP. |
| `paper_e68148717191f0d6` | yes | covered | Gaussian/OpenMM/PLUMED are covered; the described PairFE-Net model workflow belongs to the task-specific Python layer. |
| `paper_e86c38ea6471168b` | yes | covered | ASE and GPAW workflow is covered. |
| `paper_f95d34466bfd9110` | yes | covered | VASP and Gaussian workflow is covered. |
| `paper_fccb6813a9f5b43b` | yes | covered | VASP and ASE workflow is covered. |

Expected strict result after Stage02 routing: 13 covered, 3 uncovered, and 2 papers removed upstream. This
gold set evaluates precision of accepted papers; a separate stratified rejected-paper sample is
still required to estimate recall.
