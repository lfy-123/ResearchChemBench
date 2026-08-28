# Private paper route

## 1. Scientific objective and author claim

The paper asks why Rh-catalyzed keto-(5+2) cycloaddition of keto-vinylcyclopropane 1t is not observed, and contrasts it with carbonylation chemistry. The authors claim that a pathway involving VCP coordination/opening, keto coordination and subsequent C=O insertion is kinetically inaccessible; an alternative allylic-Rh/metallo-ene route is also rendered inaccessible by the uphill VCP opening and the high later barrier.

## 2. System and model boundary

The computed model is substrate 1t, the oxygen-bridged structural analog of the experimental keto-VCP, with a monomeric Rh species derived from [Rh(CO)2Cl]2. The paper considers the keto-(5+2) surface, an oxidative-cyclometalation alternative, and related CO-containing surfaces. Relative Gibbs energies are referenced to the separated catalyst/substrate (and CO where present), with CO at 6.2 mM and all other species at 1 M.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize stationary points | 1t, Rh complex, CO and pathway guesses | Gaussian 09 E.01, BMK/def2-SVP | gas phase; ultrafine grid (99 radial shells, 590 angular points) | optimized geometries | ev_doc_6e497549a572_000667_c997cf27d776 |
| 2 | Classify stationary points and obtain thermal terms | optimized structures | Gaussian 09 frequency analysis | intermediates and TSs checked by frequencies | TCGs and TS classifications | ev_doc_6e497549a572_000667_c997cf27d776 |
| 3 | Add solvent contribution | gas-phase optimized structures | Gaussian 09 SMD single point | mesitylene; same BMK/def2-SVP level | solvation-corrected energies | ev_doc_6e497549a572_000667_c997cf27d776 |
| 4 | Refine electronic energies | optimized geometries | ORCA 5.0.4 DLPNO-CCSD(T) | def2-TZVPP, def2-TZVPP/C, TightSCF, TightPNO | refined SPEs | ev_doc_6e497549a572_000667_c997cf27d776 |
| 5 | Assemble profile | SPEs, TCGs, standard-state terms | authors' energy bookkeeping | relative Gibbs energies and barriers | Figures 3, 4 and SI Tables S1–S2 | ev_doc_0f244575108c_000130_da29095c2d4f; ev_doc_6e497549a572_000710_8ec11d8981d6 |

## 4. Validation and analysis protocol

The authors optimized and frequency-checked intermediates and transition states, used the SI coordinate set for the stationary points, and compared alternative mechanistic surfaces. The principal analysis identified the highest kinetically relevant barrier and compared it with the competing CO-containing profile. The oxidative-cyclization route was separately assessed through TS-OC.

## 5. Private reference results

The source reports, for the keto-(5+2) surface, TS1 24.0, INT2 18.0, INT3 14.5, TS2 40.8, INT3′ 22.7, TS2′ 36.4, TS4 36.4 and TS-OC 44.6 kcal/mol relative Gibbs energies/barriers as identified in the paper discussion and Figure 3. The paper characterizes the overall metallo-ene barrier as 36.4 kcal/mol and the classical keto insertion barrier as 40.8 kcal/mol.

## 6. Limitations and interpretation boundaries

These are model-system free energies, not a direct rate measurement. Geometry/conformer completeness, functional and basis sensitivity, standard-state conventions, and the monomeric-Rh assumption limit quantitative transfer. The published surface does not establish that every conceivable mechanism has been searched; conclusions are bounded to the reported candidate surfaces.
