# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to rationalize the base-promoted remote migratory nucleophilic substitution of (Z)-(1-bromopenta-1,4-dien-1-yl)benzene (1a) by acetate. The authors claim that bromine enables an intramolecular hydrogen-migration manifold and that acetate addition/elimination through the path-b intermediate is kinetically preferred and gives thermodynamically stable 3a.

## 2. System and model boundary

The modeled species are neutral closed-shell organic intermediates/transition states together with acetate and bromide in implicit acetonitrile. The reported profile is a gas-phase electronic-energy plus thermal-correction treatment in which the zero of each path is its separated starting reference. It is not an explicit-solvent dynamics or rate prediction.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize stationary points | Structures for intermediates, TSs and products | Gaussian 16 | B3LYP-D3BJ/def2-SVP; SMD acetonitrile | Optimized geometries and frequencies | ev_doc_35d67f38b980_000210_b9d612e2e6b4; ev_doc_35d67f38b980_000211_d738cd1bdb7f |
| 2 | Refine energies | Optimized geometries | Gaussian 16 single point | M06-2X/ma-def2-TZVPP; SMD acetonitrile | Refined electronic energies | ev_doc_35d67f38b980_000212_2e4d6c96b9ca; ev_doc_35d67f38b980_000213_bf958f75df5a |
| 3 | Validate stationary points | Frequency output | Gaussian 16 | Minima: no imaginary modes; TS: exactly one | Stationary-point assignment | ev_doc_35d67f38b980_000215_a4d4faf9e719; ev_doc_35d67f38b980_000216_6f1a87368f98 |
| 4 | Build free-energy profile | Refined energies and thermal corrections | Authors' post-processing | Relative energies along paths | Path barriers and product energies | ev_doc_35d67f38b980_000217_7e696b0a3099; ev_doc_21cf77a2f292_000091_018a88870601 |

## 4. Validation and analysis protocol

The SI states that every optimized structure was frequency checked, with no imaginary frequencies for minima and exactly one imaginary frequency for transition states. The authors compare two hydrogen-migration/intermediate manifolds and report relative energies for intermediates, transition states and products. The interpretation is a kinetic/thermodynamic mechanistic rationale, not proof of an exclusive pathway.

## 5. Private reference results

The paper reports the path-b activation barrier as 25.9 kcal/mol and the relative free energy of 3a as -20.2 kcal/mol (the SI tabulation gives -20.23). It describes path a as having a 29.0 kcal/mol addition barrier and path b as the major pathway. The SI profile includes path-b intermediate relative energy -3.18 and TS relative energy 22.80 on its tabulated convention, while the main-text claim identifies the 25.9 kcal/mol barrier for the addition/elimination event.

## 6. Limitations and interpretation boundaries

The paper does not establish a unique global conformational ensemble, explicit solvent structure, standard-state convention beyond its own profile, or experimental rate constant. Energies from independently chosen conformers and methods are therefore compared as a mechanistic test within the stated model boundary, with conformer and method sensitivity reported as limitations.
