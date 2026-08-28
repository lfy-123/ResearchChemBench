# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to explain the acidochromic response of the Schiff-base fluorophore HL. Its claim is that protonation at the azomethine nitrogen changes frontier-orbital localization, lowers the HOMO–LUMO gap, and thereby accounts for the red-shifted absorption/fluorescence observed after acid treatment.

## 2. System and model boundary

HL is (E)-2-(((9H-fluoren-9-ylidene)hydrazono)methyl)-5-methoxyphenol, formula C21H16N2O2. The comparison is between neutral singlet HL and its singly protonated singlet derivative, with the added proton on the azomethine N atom (the –N=CH– unit). The source describes isolated-molecule DFT calculations; solvent, counterion and explicit acid are not included in the electronic-structure model.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize neutral HL | SC-XRD-derived HL geometry | Gaussian 09W, DFT | B3LYP/6-31G(d) | optimized neutral geometry | ev_doc_a65085f6b591_000113_c12412f55ae7 |
| 2 | Analyze neutral frontier orbitals | optimized HL | Gaussian 09W FMO calculation | B3LYP/6-31G(d) | HOMO/LUMO localization and gap | ev_doc_a65085f6b591_000113_c12412f55ae7 |
| 3 | Optimize protonated HL | HL with azomethine-N proton | Gaussian 09W, DFT | B3LYP/6-31G(d) | optimized cation geometry | ev_doc_a65085f6b591_000186_d94e31df60fa |
| 4 | Analyze protonated frontier orbitals | optimized HL+H+ | Gaussian 09W FMO calculation | B3LYP/6-31G(d) | localization and gap | ev_doc_a65085f6b591_000186_d94e31df60fa |
| 5 | Interpret acid response | both FMO results | qualitative comparison with spectra | gap and orbital-density redistribution | reduced gap assigned as origin of red shift | ev_doc_a65085f6b591_000186_d94e31df60fa |

## 4. Validation and analysis protocol

The paper compares the two optimized species and inspects HOMO/LUMO density. Neutral HL is described as having HOMO density mainly on the fluorenone unit and a LUMO distributed over the molecular framework. After protonation, the azomethine region becomes more electron deficient, the LUMO is described as concentrating more on the benzene framework, and the optimized cation is more distorted. The computed gap change is used alongside the observed acid-induced red shift and fluorescence change.

## 5. Private reference results

The reported neutral HL HOMO–LUMO gap is 3.62 eV. The reported azomethine-N-protonated HL+H+ gap is 2.79 eV. The source interprets the decrease as supporting the acidochromic red shift. These values and the associated result-bearing interpretation are evaluator-private.

## 6. Limitations and interpretation boundaries

The comparison is a frontier-orbital explanation, not a directly calculated absorption spectrum or excited-state treatment. Gas-phase/isolated-molecule assumptions, conformational dependence, and the absence of an explicit acid counterion limit quantitative comparison to solution spectra. Orbital localization is qualitative and should not be treated as proof of a unique photophysical mechanism.
