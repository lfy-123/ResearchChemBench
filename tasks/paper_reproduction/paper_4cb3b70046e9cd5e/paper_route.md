# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to explain why bulk reaction of styrene oxide with 2,6-dimethylaniline (DMeA) in ethanol favors alcoholysis over aminolysis. The authors claim that a proton-assisted bulk pathway gives a lower IM1→TS1 activation free energy for ethanol attack than for DMeA attack, and that this difference explains the bulk chemoselectivity.

## 2. System and model boundary

The modeled bulk system contains styrene oxide, DMeA, ethanol and a proton; GO is represented only through proton catalysis, not as an explicit cluster. Gibbs free energies are referenced to the corresponding reactants. The competing channels are nucleophilic opening at the phenyl-substituted epoxide carbon by DMeA (aminolysis) or ethanol (alcoholysis).

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build and optimize bulk reactants, IM1, TS1 and IM2 for both channels | Styrene oxide, DMeA, ethanol and proton; starting geometries in SI | Gaussian 16 DFT | M06-2X/6-31G(d), SMD ethanol | Optimized stationary-point geometries and thermochemistry | ev_doc_25661d3e9dc8_000048_737bbe15d050; ev_doc_25661d3e9dc8_000050_f457cb090ebb |
| 2 | Refine energies/free energies | Optimized geometries from step 1 | Gaussian 16 single points | M06-2X/6-311+G(d,p), SMD ethanol | Refined Gibbs free energies relative to reactants | ev_doc_25661d3e9dc8_000048_737bbe15d050; ev_doc_25661d3e9dc8_000049_e818ebe5863e; ev_doc_25661d3e9dc8_000050_f457cb090ebb |
| 3 | Compare the rate-determining barriers | IM1 and TS1 free energies for each channel | Algebraic analysis | ΔG‡ = G(TS1) − G(IM1); compare channels | Bulk aminolysis and alcoholysis barriers and ΔΔG‡ | ev_doc_4ed8c271866e_000040_bf3dd22df108; ev_doc_4ed8c271866e_000042_748295b18038; ev_doc_4ed8c271866e_000044_e4e9b5865274; ev_doc_4ed8c271866e_000046_4acdb8b88531 |

## 4. Validation and analysis protocol

The authors analyze the IM1→TS1 step as rate determining. A valid TS must have one imaginary frequency for the nucleophilic ring-opening coordinate; optimized intermediates must have no imaginary frequencies. The authors also compare the alternative aminolysis regiochannel in SI Figure S10 and identify attack at the carbon attached to phenyl as the lower aminolysis route.

## 5. Private reference results

For bulk, the paper reports ΔG‡(aminolysis) = 47.5 kJ mol−1 and ΔG‡(alcoholysis) = 43.4 kJ mol−1, so alcoholysis is lower by 4.1 kJ mol−1. The corresponding bulk IM1 free energies are −418.6 and −450.3 kJ mol−1, and TS1 free energies are −371.1 and −406.9 kJ mol−1, respectively.

## 6. Limitations and interpretation boundaries

These are model-system free energies, not a direct kinetic measurement. The bulk proton model omits explicit GO and does not establish all possible solvent configurations or conformers. Reported chemoselectivity is interpreted through the modeled barrier ordering within this specified model boundary.
