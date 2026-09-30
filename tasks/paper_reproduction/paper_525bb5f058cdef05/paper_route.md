# Private paper route

## 1. Scientific objective and author claim

The paper asks how reduced field strength changes proton-transfer kinetics from hydrated hydronium to benzene. The authors claim that hydration, reaction-complex stability, and internal proton-transfer barriers make the observed rate depart from the collision/association limit, especially for benzene.

## 2. System and model boundary

The modeled system is gas-phase benzene with H3O+ and H3O+(H2O), including protonated benzene and water-containing adducts. H3O+(H2O)2 is present as a hydration/dehydration reservoir; main PDF p8 explicitly excludes its direct reaction with the analytes from the modeled network, consistent with SI PDF p8, Fig. S3. The public task additionally asks for an n=2 candidate/status; a source-route reproduction must disclose this scope gap and must not relabel the 19-atom n=1 complex as n=2. The paper treats one literature-supported protonation site and one selected conformer per reaction complex. The kinetic boundary includes association, dissociation, hydration/dehydration, proton transfer, pressure dependence, and numerical population propagation; it excludes tunnelling corrections.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build and optimize species | Reactants, products, complexes | ORCA DFT | ωB97X-D3(BJ)/def2-TZVPP; one protonation site; one lowest-energy complex conformer | Geometries, frequencies, thermochemistry, electrostatic properties | ev_doc_e182a747c6b2_000163_5e6cecf61815; ev_doc_4a7e2fa70661_000120_8fa8190a94db |
| 2 | Refine energies and check reference character | Optimized structures | ORCA DLPNO-CCSD(T) | def2-TZVPP; T1 diagnostics reported below 0.0156 closed-shell and 0.0221 open-shell | Refined electronic energies and diagnostics | ev_doc_e182a747c6b2_000163_5e6cecf61815 |
| 3 | Locate tight proton-transfer path | Optimized reactant/product endpoints | ORCA climbing-image NEB then TS optimization | Highest NEB image used as TS guess; one imaginary mode required | MEP, TS geometry and frequency | ev_doc_e182a747c6b2_000168_59cbb380c5f0 |
| 4 | Model field-dependent kinetics | Thermochemistry, TS, mobilities | SACM/TST with Lindemann-Hinshelwood and coupled rate equations | Ion-induced-dipole or ion-dipole capture; effective temperature and collision frequency; numerical propagation | Rate coefficients and ion populations versus field/effective temperature | ev_doc_4a7e2fa70661_000243_30ae1640cf62; ev_doc_e182a747c6b2_000168_59cbb380c5f0 |

## 4. Validation and analysis protocol

The authors validate single-reference behavior with T1 diagnostics, validate transition states by one imaginary frequency associated with proton transfer, and compare modeled rates/populations with experimental trends over reduced field strength. Their conclusions emphasize qualitative agreement, order-of-magnitude behavior, hydration suppression of proton transfer, and stable adduct accumulation.

## 5. Private reference results

The paper reports that bare hydronium proton transfer to benzene is strongly exergonic and approaches the association limit, whereas hydrated hydronium is slowed by ligand switching, stable complexes, and internal barriers. Benzene is less efficiently protonated than toluene or p-xylene by hydrates; larger hydrates are not efficiently protonating. The modeled benzene rate shows a depression in the intermediate effective-temperature region and lies below the association-limit rate when hydrated ions dominate. Exact plotted/table rate values are intentionally private.

## 6. Limitations and interpretation boundaries

The paper uses one conformer per complex, omits tunnelling, uses a simplified SACM/TST kinetic treatment rather than a master equation, and notes uncertainty from hydration and experimental transfer efficiencies. These limitations make qualitative mechanistic and trend validation more defensible than exact numerical reproduction.
