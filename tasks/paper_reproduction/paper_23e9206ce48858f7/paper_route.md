# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to test a selenium-radical/selenium-ion mechanism for electrochemical selenylation and cyclization of alkyne-modified O-methyltyrosine substrate 1a with diphenyl diselenide 2a, and to quantify the free-energy barriers for the three proposed elementary steps.

## 2. System and model boundary

The modeled chemical system is substrate 1a, diphenyl diselenide (PhSeSePh, 2a), the derived PhSe radical and PhSe− fragments, and intermediates/transition states along the pathway to cyclic selenium product 3. The reported energies are free energies at 298.15 K and 1 M; solvent treatment is THF with SMD for the refined energies.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize intermediates and TS structures | Stationary-point geometries for the pathway | Gaussian 16 Rev. A.03; B3LYP-D3 | BS-I: LANL2DZ/ECP for Se; 6-31G(d) for H,C,O,N | Optimized geometries and frequencies | ev_doc_6f7a20a08177_001865_d6e302c09962 |
| 2 | Characterize stationary points | Optimized structures | Gaussian frequency analysis | Minima: zero imaginary frequencies; TS: one imaginary frequency | Minima/TS assignment | ev_doc_6f7a20a08177_001865_d6e302c09962 |
| 3 | Verify TS connectivity | Each optimized TS | Gaussian IRC | IRC in both directions to connected minima | Connectivity assignment | ev_doc_6f7a20a08177_001865_d6e302c09962 |
| 4 | Refine energies in solvent | Optimized structures | B3LYP-D3 single points with SMD(THF) | BS-II: SDD/ECP for Se; 6-311++G(d,p) for H,C,O,N | Free energies at 1 M, 298.15 K | ev_doc_6f7a20a08177_001865_d6e302c09962 |
| 5 | Construct the pathway surface and extract barriers | Refined free energies | Relative free-energy analysis | Barriers measured from the preceding connected reactant/intermediate | TS1, TS2, TS3 activation barriers | ev_doc_28e08b89e0fe_000088_3f5a6fca5254; ev_doc_6f7a20a08177_001866_c067b553f025 |

## 4. Validation and analysis protocol

The authors required zero imaginary frequencies for minima, one imaginary frequency for each TS, and IRC connectivity. They interpreted the sequence as diselenide reduction to selenium radical/selenide, radical addition to the alkyne, oxidation to a carbocation, cyclization, and capture by PhSe−. The mechanism was discussed alongside radical-scavenger/trapping and electrochemical control experiments.

## 5. Private reference results

The reported activation barriers are 8.9 kcal/mol for TS1, 7.6 kcal/mol for TS2, and 6.2 kcal/mol for TS3. The paper assigns these to radical addition, carbocation cyclization, and selenide capture, respectively.

## 6. Limitations and interpretation boundaries

These are single-level DFT results with implicit solvent refinement and do not establish a unique real-time electrochemical trajectory. Barrier comparison is meaningful only for correctly identified connected stationary points and the stated thermodynamic standard state. Conformer and ion-pair choices can affect absolute values; failure to locate a TS should be reported as a bounded computational limitation rather than replaced by an invented value.
