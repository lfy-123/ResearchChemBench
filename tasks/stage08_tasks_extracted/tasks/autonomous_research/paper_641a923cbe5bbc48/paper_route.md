# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to identify the resting conformer of cationic thiourea 7+ and to test whether its conformational preference is consistent with the mechanistic analogy to Takemoto's catalyst. The authors report isolated-cation free energies for Z,E, E,Z, and Z,Z, and also model their nitromethane adducts.

## 2. System and model boundary

The isolated species is the singly charged cation 7+ (45 atoms, charge +1, singlet). The three geometric labels are the authors' Z,Z; E,Z; and Z,E thiourea configurations. The SI also contains 7+--CH3NO2 complexes, but those are outside the public task's scored endpoint.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Compare isolated conformers | 7+ Z,Z, E,Z, Z,E geometries | Gaussian 16 geometry optimization | B3LYP/6-31G(d,p); also M06-2X/aug-cc-pVDZ | optimized geometries and electronic energies | ev_doc_970afd0219ff_000187_4bec7683d998; ev_doc_970afd0219ff_000189_2665727eef09 |
| 2 | Establish minima and thermochemistry | optimized isolated conformers | Gaussian 16 frequency calculation | same levels | frequencies, ZPE, enthalpy correction and entropy | ev_doc_970afd0219ff_000187_4bec7683d998; ev_doc_970afd0219ff_000189_2665727eef09 |
| 3 | Form relative free energies | electronic and thermal quantities | thermochemical assembly | report relative values in kcal mol-1 | conformer ordering and energy gaps | ev_doc_bf177dd573a3_000144_f706426a87f8 |
| 4 | Test substrate association | 7+ conformers plus nitromethane | optimization/frequencies at both levels | isolated complex comparison | adduct relative free energies | ev_doc_bf177dd573a3_000144_f706426a87f8; ev_doc_970afd0219ff_000029_f71fd3141a94 |

## 4. Validation and analysis protocol

Each optimized structure was checked as an energy minimum by requiring no imaginary frequencies. Free energies were compared after applying the reported zero-point, thermal and entropic corrections. The main-paper interpretation combines the conformer calculation with NOESY evidence and the adduct calculation: isolated-cation and substrate-bound preferences need not be identical.

## 5. Private reference results

At the B3LYP/6-31G(d,p) level, the paper states that Z,E is 10.2 kcal mol-1 lower than E,Z and 1.0 kcal mol-1 lower than Z,Z. Thus the isolated ordering is Z,E < Z,Z < E,Z. For the nitromethane adduct, Z,Z is reported lower than Z,E and E,Z by 6.5 and 9.6 kcal mol-1, respectively. The SI reports no imaginary frequencies for the three isolated conformers and gives raw energies, ZPE, thermal corrections and entropies.

## 6. Limitations and interpretation boundaries

These are gas-phase model calculations on a cation and do not by themselves establish solution populations or a complete catalytic mechanism. Relative free energies depend on conformer coverage, thermochemical conventions and model chemistry. The public task therefore scores the isolated conformer endpoint and requires explicit reporting of method, temperature/convention, convergence and limitations.
