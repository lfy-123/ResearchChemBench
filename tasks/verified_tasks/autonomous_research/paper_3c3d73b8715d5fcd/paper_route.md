# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to explain Rh-catalyzed cycloisomerization of a model 1,7-allenene (1D), its [2+2] side reaction, and the preference of endo oxidative cyclometalation (OCM) over exo-OCM. The authors claim that endo-OCM initiates cycloisomerization and that the competing [2+2] and cycloisomerization channels have comparable barriers.

## 2. System and model boundary

The computed model is 1D, an O-tethered 1,7-allenene model with two methyl groups in the allene moiety, reacting with monomeric Rh species derived from [Rh(CO)2Cl]2. Energies are solution-phase Gibbs free energies at 298 K in 1,4-dioxane; CO uses an 8.5 mM standard state and other species 1 M.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate conformers and stationary-point guesses | 1D, catalyst, minima and TS guesses | CREST 2.12 with xTB 6.6.0 | GFN2-xTB/GBSA(toluene), 3 kcal/mol window | 3D starting structures | ev_doc_1226814998dd_000409_5358fe5b26ea |
| 2 | Optimize minima and transition states | 3D guesses | Gaussian 16 C.02, PW6B95-D3(BJ) | 6-311G(d,p), def2-TZVP/ECP for Rh, ultrafine grid | gas-phase optimized structures | ev_doc_1226814998dd_000409_5358fe5b26ea |
| 3 | Verify stationary points and obtain thermal terms | optimized structures | Gaussian frequency analysis | 298 K; TS has one imaginary frequency, minima none | Gibbs thermal corrections | ev_doc_1226814998dd_000415_4f7fe1677b19 |
| 4 | Add solvent contribution | optimized structures | Gaussian 16 C.02 SMD single points | 1,4-dioxane; PW6B95-D3(BJ), stated basis | solvation electronic energies | ev_doc_1226814998dd_000415_4f7fe1677b19 |
| 5 | Refine electronic energies | optimized structures | ORCA 5.0.4 | omegaB97M-V/def2-QZVP, TightSCF | high-level single-point energies | ev_doc_1226814998dd_000415_4f7fe1677b19 |
| 6 | Assemble profile and compare pathways | steps 3–5 | energy bookkeeping | Gsol = Ehigh + Gcorr_low + (Esolv_low−Egas_low), plus explicit standard-state corrections | free-energy profile and mechanistic comparison | ev_doc_1226814998dd_000053_e68d8e659e55 |

## 4. Validation and analysis protocol

The authors classify minima by zero imaginary frequencies and transition states by one imaginary frequency. They compare endo-OCM, exo-OCM, cycloisomerization and [2+2] pathways from a common catalyst/substrate reference and use the assembled solution Gibbs energies to identify the rate-determining event and product channels.

## 5. Private reference results

The paper reports an overall cycloisomerization activation free energy of 22.8 kcal/mol from INT11, an endo/exo-OCM transition-state difference of 7.5 kcal/mol, and an endo-OCM barrier of 12.9 kcal/mol from INT1. It reports 17.1 kcal/mol for the [2+2] reductive-elimination transition state, 6.0 kcal/mol for beta-H elimination, and 8.9 kcal/mol for the cycloisomerization reductive-elimination step.

## 6. Limitations and interpretation boundaries

The model is a simplified substrate and monomeric Rh representation rather than a full experimental catalyst ensemble. Conformational sampling and method sensitivity can affect dissociation and coordination barriers. The reported numbers are source-backed reference values for comparison, not universal experimental activation energies.

## Input transcription correction

Source correction 2026-09-15: the original public XYZ transcription crossed SI headings. 1D is the complete 24-atom C9H14O block on S46; [Rh(CO)2Cl]2 is the 12-atom C4O4Cl2Rh2 block spanning S44-S45. Public coordinates now match these source blocks. Old wrong-identity calculations cannot validate this corrected task. Gaussian PW6B95D3 implements PW6B95 with D3(BJ); the mixed basis is 6-311G(d,p) for all non-Rh atoms and def2-TZVP/ECP for Rh. Figure 1 scientific targets and tolerances are unchanged.

## Thermal-correction bookkeeping clarification (2026-09-25)

SI Table S2 labels TCG as a thermal correction to Gibbs energy, not the total low-level Gibbs energy. Therefore Gcorr_low is added once: Gsol = Ehigh + Gcorr_low + (ESMD_low − Egas_low), followed by the stated 298 K standard-state treatment (1 M species, 8.5 mM CO). Equivalently, if using the total low-level G, replace Gcorr_low by G_low − Egas_low. The old formula subtracted Egas_low twice when interpreting Gcorr as the SI correction; it is corrected here. Numerical targets and tolerances are unchanged. Shared installed ORCA 6.1.1 is user-approved for validation, with the source ORCA 5.0.4/default difference disclosed rather than claimed identical.
