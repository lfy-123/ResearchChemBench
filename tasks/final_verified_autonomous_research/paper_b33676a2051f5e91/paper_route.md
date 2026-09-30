# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to support selective oxidation of sec-butylbenzene. The authors claim that beta-scission of the alkoxy radical intermediate leading to acetophenone and an ethyl radical is more favorable than the competing cleavage leading to propiophenone and a methyl radical.

## 2. System and model boundary

The relevant model is the neutral doublet alkoxy radical labelled Int-3 in the SI and the neutral doublet transition state labelled TS-4b. The reported thermochemistry is for the isolated molecular species with implicit acetonitrile solvation; no explicit solvent, catalyst, oxygen, or counterion is included in these two structures.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground-state intermediates | Reactant/intermediate geometries | Gaussian 16 | BHandHLYP/aug-cc-pVDZ; SMD(acetonitrile) | Optimized minima | ev_doc_dfd058e5c120_000225_32a2a213ce20 |
| 2 | Optimize transition states | TS guesses | Gaussian 16 | BHandHLYP/aug-cc-pVDZ; SMD(acetonitrile) | TS with one imaginary mode | ev_doc_dfd058e5c120_000225_32a2a213ce20 |
| 3 | Frequency and thermochemistry validation | Optimized structures | Gaussian 16 | Zero imaginary frequencies for minima; one for TS | Thermal free-energy corrections | ev_doc_dfd058e5c120_000225_32a2a213ce20 |
| 4 | Confirm connectivity | Optimized TS | Gaussian 16 | Intrinsic reaction coordinate | Reactant/product connection | ev_doc_dfd058e5c120_000225_32a2a213ce20 |
| 5 | Compare pathways | Free energies of Int-3/TS-4a/TS-4b | Derived from steps 1–3 | ΔG‡ relative to Int-3 | Selectivity-supporting barriers | ev_doc_0661377fa5b3_000135_887350f93520 |

## 4. Validation and analysis protocol

The authors require frequency validation (zero imaginary modes for minima and one for a transition state) and IRC confirmation that the TS connects the intended reactant and products. They report the acetophenone-forming barrier as 9.07 kcal mol−1 and the competing propiophenone-forming barrier as 13.39 kcal mol−1. The broader mechanism also includes chlorine-radical HAT and oxygen chemistry, but those are outside this benchmark's scored calculation.

## 5. Private reference results

For the Int-3 → TS-4b beta-scission, the SI gives Int-3 electronic-plus-thermal-free-energy value −463.661084 Hartree and TS-4b value −463.646629 Hartree. The main text reports ΔG‡ = 9.07 kcal mol−1. The intended TS has exactly one imaginary frequency and Int-3 has zero.

## 6. Limitations and interpretation boundaries

This is a single-reaction model calculation and does not establish the full polymer-upcycling mechanism by itself. Barrier values depend on conformer, spin, solvation, thermal conventions, and numerical settings. The benchmark therefore scores structure/frequency validation and the reported barrier within an explicitly stated tolerance, while accepting a bounded-failure report when a validated TS cannot be located.
