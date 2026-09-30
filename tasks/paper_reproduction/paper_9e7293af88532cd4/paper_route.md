# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to explain conversion of Mo(VI) oxido-hydroxylamido complex 1 to the Mo(II)-NO aqua complex 3. The authors claim an inner-sphere hydroxylamine route involving electron transfer, proton transfer, water coordination/dehydration, and subsequent oxidation; the calculated profile is intended to establish that the reaction proceeds through a reduced electronic surface.

## 2. System and model boundary

The modeled system is the isolated neutral singlet complex 1 and neutral singlet product 3, with hydroxylamine-derived atoms and the pidiox ligand retained explicitly. The reported thermochemistry is solution-phase Gibbs free energy at 298.15 K, with water represented by a continuum and explicit water association corrected from a 1 M to bulk-water standard state.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Locate stationary points for reactant, intermediates, TS1, TS2 and product | Table S6 Cartesian geometries and stated charge/multiplicity | Gaussian 16 C.01 geometry optimization | PBE0/def2-TZVP; def2 ECP for Mo; no symmetry constraints; IEF-PCM water | Optimized geometries | ev_doc_78639d795f95_000132_271170f29982; ev_doc_78639d795f95_000432_845d4deb3817 |
| 2 | Classify stationary points and obtain thermochemistry | Optimized structures | Gaussian 16 analytical frequencies | 298.15 K, 1 atm; harmonic corrections without scaling; minima NImag=0, TS NImag=1 | Sum of electronic and thermal free energies | ev_doc_78639d795f95_000138_21801bf54e09; ev_doc_78639d795f95_000139_c7df02bc914e |
| 3 | Verify TS connectivity | TS1 and TS2 structures | IRC calculations | PBE0/def2-TZVP/PCM(water) | Endpoint connectivity along both paths | ev_doc_78639d795f95_000432_845d4deb3817; ev_doc_b38e9ca4555a_000831_30d7d080e566 |
| 4 | Assemble profile | Free energies of stationary points | Algebraic thermochemistry | Reactant baseline; water association correction −RT ln(55.34)=−2.378 kcal mol−1 | Relative free-energy profile | ev_doc_78639d795f95_000139_c7df02bc914e; ev_doc_b38e9ca4555a_000852_a72cb6cd7bd3 |

## 4. Validation and analysis protocol

The authors inspect imaginary-frequency counts, use IRCs for TS1 and TS2, and interpret the profile together with experimental characterization. Their reported mechanistic interpretation is: NH2OH coordination gives Im1; electron transfer places TS1 on the reduced surface; TS2 couples proton transfer and water coordination; dehydration gives Im3; deprotonation gives Im4; NO/N2O-coupled oxidation gives Im5; water association gives product 3.

## 5. Private reference results

The reactant free energy in Table S6 is −859.262712 au. The product endpoint is the neutral Mo–NO aqua complex 3. The profile reports Im1 +8.7 kcal mol−1, reduced TS1 53.1 kcal mol−1 below Im1 on the common scale, Im2 approximately +12 kcal mol−1, TS2 a 15.6 kcal mol−1 barrier, Im3 approximately 9.5 kcal mol−1 below TS2, proton transfer Im3→Im4 −27.5 kcal mol−1, NO/N2O-coupled oxidation approximately thermoneutral, competing O2 oxidation +42.6 kcal mol−1, and final water association +1.6 kcal mol−1.

## 6. Limitations and interpretation boundaries

The numerical profile is model-dependent and contains mixed electronic surfaces and standard-state corrections. Formal oxidation-state assignments for nitrosyl chemistry are non-innocent; the paper describes the product as Mo(II)/NO+-leaning rather than uniquely ionic. The repaired benchmark validates complex1/product3 and scores only balanced Im5+water association; its declared source-recipe scalar is not a consistently corrected1M thermodynamic claim.


## 2026-09-26 source-backed task correction

Original complex1/product3 validation and the independent diagnostic remain required. Added completeIm5 and isolatedwater inputs make the scored final association atom balanced. The old unbalanced field is removed. Numeric reference1.6kcal/mol and tolerance8.0 are unchanged. SI S5 specifies1atm harmonic corrections, but S6/S7 calls the raw Gaussian sum1M. Therefore reproduce its exact recipe(raw deltaG minusRTln55.34) only as the source-recipe field and separately report raw1atm, consistentall-solute1M and bulk-water values. This correction does not establish the overall conversion or validate every proposed intermediate. The source is primary SI physicalS5-S7 andTableS6.
