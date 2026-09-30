# Private paper route

## 1. Scientific objective and author claim

The paper explains the regioselectivity of Fe-catalyzed hydrodisilylation of 4-phenyl-1-butyne (2a) with 1,1,2,2-tetraphenyldisilane (1a) using L10·FeCl2. The authors claim that migratory insertion of the alkyne into an Fe–H species is regioselectivity-determining and that the OPQ ligand's chiral oxazoline/quinoline environment favors one approach.

## 2. System and model boundary

The modeled cycle contains the L10-supported iron hydride, alkyne 2a, dihydrodisilane 1a, alkenyl-iron intermediates, and competing migratory-insertion transition states. Fe(I) doublet, quartet, and sextet surfaces are considered; the reported comparison focuses on TS3A–D quartet structures and barriers relative to INT1A-sextet + 2a.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize stationary points | Catalyst, substrates, intermediates and TS guesses | Gaussian 09; M06L | SDD on Fe; 6-31G(d) on C,H,N,O,Si; gas phase; ultrafine grid | Optimized geometries and electronic energies | ev_doc_0208cf1c0355_001373_6e6e66864f04; ev_doc_0208cf1c0355_001375_efdbd95099a1 |
| 2 | Classify stationary points and obtain thermal terms | Optimized structures | Gaussian 09 frequency calculation at the optimization level | 298.15 K; TS requires one imaginary mode for the expected bond-making/breaking motion | Frequencies, Hcorr and Gcorr | ev_doc_0208cf1c0355_001373_6e6e66864f04; ev_doc_0208cf1c0355_001375_efdbd95099a1 |
| 3 | Add solvent electronic energy | Optimized geometries | M06L single point with IEFPCM(THF) | 6-311+G(d,p)-SDD; ultrafine grid | Hsol | ev_doc_0208cf1c0355_001375_efdbd95099a1; ev_doc_0208cf1c0355_001376_7fd2402cf060 |
| 4 | Assemble relative free energies | Hsol and thermal terms | Authors' 2/3 entropy adjustment | Reference INT1A-sextet + 2a; energies reported in kcal/mol | ΔGsol barriers for TS3A–D | ev_doc_0208cf1c0355_001376_7fd2402cf060; ev_doc_52d328a199b0_000107_9cb49f2d10e4 |

## 4. Validation and analysis protocol

The authors inspect imaginary frequencies to distinguish minima from transition states, compare spin surfaces, and analyze the four quartet migratory-insertion pathways. They interpret the barrier pattern together with steric/distortion analysis; TS3A-quartet has reported total catalyst-plus-substrate distortion energy of 34.2 kcal/mol. The reaction profile is used to explain the observed regioselective product formation and preservation of the Si–Si bond.

## 5. Private reference results

The reported quartet barriers relative to INT1A-sextet + 2a are TS3A 10.2, TS3B 12.4, TS3C 13.2, and TS3D 12.0 kcal/mol. The reported ordering is A < D < B < C. The paper states that TS3A is 2.2 kcal/mol below TS3B and assigns the selectivity to reduced steric distortion in the L10 environment.

## 6. Limitations and interpretation boundaries

These are single-geometry DFT stationary-point comparisons and do not establish a full kinetic model, explicit solvent dynamics, spin-crossing rate, or exhaustive conformational sampling. Barrier agreement is interpreted within the stated model and reference state; it is not a claim of experimental absolute-rate prediction.
