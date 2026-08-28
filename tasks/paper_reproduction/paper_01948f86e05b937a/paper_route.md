# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to test the mechanism of THF C–H borylation by an anionic iridium trisboryl catalyst and to explain α-regioselectivity. The authors claim that alkoxide enables the anionic trisboryl species, C–H oxidative addition is approximately turnover-limiting, and the subsequent α/β reductive-elimination barriers are slightly lower.

## 2. System and model boundary

The modeled system is the anionic Ir(III) trisboryl complex derived from ligand L8, THF as substrate/solvent, and the catalytic α and β THF-borylation pathways. The reported computations use singlet anionic complexes; Na+ is included in the optimized structures where present.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize minima and saddle points and verify stationary points | DFT starting geometries | ORCA 4.2.0 DFT | B3LYP-D3, def2-SVP, Def2-ECP for Ir, RIJCOSX/def2/J; harmonic frequencies | optimized geometries, frequencies, ZPE | ev_doc_8134a6395686_001069_459a57e6c548; ev_doc_8134a6395686_001155_c4071521459a |
| 2 | Refine electronic and solvation energies | optimized structures | ORCA single points/CPCM | B3LYP-D3/def2-TZVP, Def2-ECP, CPCM THF | E(SCF), solvation free energies | ev_doc_8134a6395686_001069_459a57e6c548 |
| 3 | Assemble free-energy profile | component energies and thermochemistry | paper protocol | 373.15 K; G=E(SCF)+ZPE−TS+Gsolv; −4.12 kcal/mol concentration correction for solvent-involving species | α/β activation free energies and profile interpretation | ev_doc_8134a6395686_001080_4730ce90cf48; ev_doc_8134a6395686_001151_f72b3a0e63d9 |

## 4. Validation and analysis protocol

Stationary points are checked by harmonic frequencies. Transition states must have one relevant imaginary mode connecting the stated reactant/product event; minima must have no imaginary frequencies. Energies are assembled consistently relative to complex 1 and compared across α and β channels. The paper additionally interprets the barrier ordering against the measured α-selectivity and KIE.

## 5. Private reference results

The paper reports approximately 29.3 kcal/mol for both α and β C–H oxidative addition, 27.4 kcal/mol for α C–B reductive elimination, and 28.0 kcal/mol for β C–B reductive elimination. Oxidative addition is interpreted as likely turnover-limiting; α-selectivity is experimentally observed and the small computed α/β oxidative-addition difference is not treated as quantitatively decisive.

## 6. Limitations and interpretation boundaries

The authors caution that DFT cannot reliably determine the magnitude or direction of the small α/β oxidative-addition ΔΔG‡. Free-energy values depend on conformational coverage, stationary-point verification, solvation and concentration conventions, and the chosen electronic-structure model.
