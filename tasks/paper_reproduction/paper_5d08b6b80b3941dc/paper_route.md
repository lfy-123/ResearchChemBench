# Private paper route

## 1. Scientific objective and author claim

The paper evaluates whether radical chemistry can account for methane functionalization in concentrated sulfuric acid/oleum. The central computational claim is that hydrogen-atom transfer from methane to bisulfate radical, producing methyl radical and sulfuric acid, is a low-barrier elementary step and therefore supports a radical route to methanesulfonic acid.

## 2. System and model boundary

The computational model uses isolated molecular species embedded in an SMD continuum parameterized for 98% sulfuric acid. The directly relevant states are methane, HSO4•, HSO4•···CH4 reactant complex, the HAT transition structure, and the post-HAT methyl-radical/sulfuric-acid complex. Spin states and protonation are explicit; the surrounding acid is represented by the continuum and by the explicit H2SO4 partner used in the reported complexes.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate conformers/geometries | Molecular species and complexes | CREST/xTB followed by Gaussian 16 DFT | MN15/def2-SVP; SMD, 98% H2SO4, eps 98.0, radius 2.205 | Initial optimized structures | ev_doc_aff65376a94f_000095_8cfa5fb0d164 |
| 2 | Locate and optimize HAT TS | HSO4• + methane H-transfer guess | Gaussian 16 | MN15/def2-SVP(SMD), then reoptimization/refinement with MN15/def2-TZVPD(SMD) | TSR1 transition structure | ev_doc_aff65376a94f_000095_8cfa5fb0d164; ev_doc_287a677d0b28_000001_1fb36dae8a57 |
| 3 | Validate stationary points | Optimized reactant, TS, products | Gaussian 16 frequency/Hessian calculations | One imaginary mode for TS; minima without imaginary modes | Thermal corrections and mode validation | ev_doc_aff65376a94f_000095_8cfa5fb0d164 |
| 4 | Calculate energies | Validated structures | Gaussian 16 MN15 single points and composite comparison | def2-TZVPD(SMD); additional CBS-QB3 comparison | Electronic, enthalpy, and free energies | ev_doc_aff65376a94f_000095_8cfa5fb0d164; ev_doc_287a677d0b28_000006_edd302d38041 |
| 5 | Interpret mechanism | Relative state energies and barriers | Authors' comparison with closed-shell pathways | Radical HAT compared with protonation, hydride transfer, and C-H activation | Mechanistic conclusion | ev_doc_aff65376a94f_000231_4d46fb6d18ef; ev_doc_aff65376a94f_000286_4805573d884a; ev_doc_aff65376a94f_000287_e9690404d41f |

## 4. Validation and analysis protocol

The authors compare optimized stationary-point energies on the solution-phase surface, require a genuine first-order saddle for each transition structure, and inspect the imaginary mode to ensure it is the H-transfer coordinate. They compare the HAT barrier with alternative closed-shell pathways and use both DFT and CBS-QB3 analyses to assess robustness.

## 5. Private reference results

The SI tabulates the TSR1 free-energy barrier at the MN15/def2-TZVPD(SMD) level as 11.4 kcal/mol for the explicit sulfuric-acid complex, with an imaginary frequency of -1162.88 cm−1. The main text rounds the reported Gibbs barrier to 11 kcal/mol and describes the step as very low barrier. The paper also reports a second HAT step near 16 kcal/mol and a substantially higher hydride-transfer barrier.

## 6. Limitations and interpretation boundaries

The model is a continuum-solvent molecular-cluster approximation and does not establish the full speciation or kinetics of oleum. Conformer coverage, standard-state conventions, spin treatment, and method dependence can shift barriers. The benchmark evaluates the elementary stationary-point calculation and its mechanistic interpretation within the stated model, not experimental rate constants or a unique global mechanism.
