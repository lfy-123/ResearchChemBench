# Private paper route

## 1. Scientific objective and author claim

The authors use DFT and TD-DFT to connect twisting between the dibenzo[c,g]carbazole (DBC) core and the N-phenyl/para-aryl substituent to frontier-orbital localization and absorption/emission behavior for DBC-Ph and DBC-Nap. They claim moderately twisted geometries retain locally excited character with partial intramolecular charge transfer and red-shifted emission.

## 2. System and model boundary

The computational systems are neutral singlet DBC-Ph (7-([1,1'-biphenyl]-4-yl)-7H-dibenzo[c,g]carbazole) and DBC-Nap (7-(4-(naphthalen-1-yl)phenyl)-7H-dibenzo[c,g]carbazole), in implicit toluene. The reported states are the ground state S0 and first singlet S1; the reported observables are optimized-state dihedrals, vertical TD-DFT wavelengths, oscillator strengths, and orbital localization.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize S0 geometry | DBC-Ph or DBC-Nap structure | Gaussian 16 DFT | B3LYP/6-31+G(d,p), IEFPCM toluene | S0 optimized geometry and dihedrals | ev_doc_72617aa1e8c2_000195_3bc1118fe395; ev_doc_72617aa1e8c2_000196_907de06f6066 |
| 2 | Optimize S1 geometry | S0 geometry/first singlet state | Gaussian 16 excited-state DFT | B3LYP/6-31+G(d,p), IEFPCM toluene | S1 optimized geometry and dihedrals | ev_doc_72617aa1e8c2_000195_3bc1118fe395; ev_doc_72617aa1e8c2_000197_8b09862678ff |
| 3 | Compute absorption | S0 optimized geometry | Gaussian 16 TD-DFT | TD-B3LYP/6-31+G(d,p), IEFPCM toluene | singlet excitation wavelengths, oscillator strengths, configurations | ev_doc_72617aa1e8c2_000197_8b09862678ff; ev_doc_72617aa1e8c2_000260_224332d7ddda |
| 4 | Compute emission proxy | S1 optimized geometry | Gaussian 16 TD-DFT | TD-B3LYP/6-31+G(d,p), IEFPCM toluene | vertical transitions and oscillator strengths | ev_doc_72617aa1e8c2_000197_8b09862678ff; ev_doc_72617aa1e8c2_000260_224332d7ddda |
| 5 | Interpret structure–property relation | outputs of steps 1–4 | orbital population/visual analysis | HOMO/LUMO localization on DBC versus aryl units | LE/partial-CT interpretation | ev_doc_72617aa1e8c2_000268_8e41c7ffdeea; ev_doc_72617aa1e8c2_000284_4fa23bd7e1e3 |

## 4. Validation and analysis protocol

The reported S0 dihedrals were compared across compounds and against the DBC-Nap X-ray structure. TD-DFT spectra were compared with the experimental UV-vis/PL trends and the computed tables. Orbital distributions were used to distinguish DBC-localized HOMO character from aryl-extended LUMO character.

## 5. Private reference results

Main-paper Table 2 reports S0 J1/J2 dihedrals for DBC-Ph and DBC-Nap; SI Tables S5 and S7 report five S0 and five S1 transitions, wavelengths, oscillator strengths, and dominant configurations for each. These values are evaluator-only and are not public inputs.

## 6. Limitations and interpretation boundaries

Implicit solvent and a single functional/basis set do not establish quantitative experimental accuracy. Vertical transitions are not complete vibronic spectra, and orbital population partitions are model-dependent. The benchmark scores the stated calculated observables and qualitative localization, not a universal photophysical mechanism.
