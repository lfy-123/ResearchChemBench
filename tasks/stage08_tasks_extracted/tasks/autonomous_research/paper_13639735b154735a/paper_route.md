# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to support a synergistic dual-site mechanism for CO2 cycloaddition with epichlorohydrin (ECH) on HPILs-DVB-0.3. The authors identify epoxide ring opening by bromide as the rate-determining event and report an electronic barrier of 12 kcal mol-1; subsequent CO2 insertion is reported as a 1.37 kcal mol-1 activation event (main paper, Fig. 7c and discussion).

## 2. System and model boundary

The computational model is the neutral singlet 133-atom complex in SI Table S8 (in3), containing the imidazole/triazine/benzene catalyst fragment, bromide sites, ECH and the associated CO2/reactive components represented in the supplied coordinates. The authors model adsorption and the ECH ring-opening pathway with H, C, N, O, Cl and Br atoms.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize catalyst/adsorbate, reactants, intermediates, products and transition states | Model structures including in3 and TS1 | Gaussian16 DFT | B3LYP-D3(BJ)/6-31G(d), neutral singlet | Optimized geometries and electronic energies | ev_doc_27e0b7483446_000034_e687800c7438; ev_doc_27e0b7483446_000147_bdd50d104752; ev_doc_27e0b7483446_000156_2a179c28b62a |
| 2 | Validate stationary points | Optimized structures | Harmonic frequency analysis | Minima have zero imaginary frequencies; TS has one imaginary frequency along the expected coordinate | Frequencies and stationary-point assignment | ev_doc_27e0b7483446_000034_e687800c7438 |
| 3 | Verify key TS connectivity | Optimized TS structures | Intrinsic reaction coordinate calculation | IRC connects the intended neighboring states | Reaction-path connectivity | ev_doc_27e0b7483446_000034_e687800c7438 |
| 4 | Analyze energy profile and CO2 adsorption | Validated states | Electronic-energy comparisons | Compare elementary-step energies and adsorption geometries | Barriers, adsorption distances/angles, mechanistic interpretation | ev_doc_24eccd5c8b30_000158_2f5b5b6d1e5a; ev_doc_24eccd5c8b30_000163_5f7c0e6f9e32 |

## 4. Validation and analysis protocol

The authors require zero imaginary modes for minima, one imaginary mode for each transition state with the mode pointing along the intended reaction coordinate, and IRC connectivity for key transition states. The mechanism is interpreted using the relative electronic energies of ring opening, CO2 insertion and cyclization, together with the computed CO2 adsorption geometry and the experimental observation of high-selectivity cyclic-carbonate formation.

## 5. Private reference results

The main paper reports 12 kcal mol-1 for the ECH ring-opening electronic barrier and 1.37 kcal mol-1 for CO2 insertion. It identifies ring opening as rate determining. The reported CO2 adsorption distances are 3.11 Å (imidazole), 3.09 Å (triazine) and 3.24 Å (benzene); corresponding activated CO2 angles are 179.75°, 174.85° and 177.85°. These values are evaluator-private.

## 6. Limitations and interpretation boundaries

The model is a finite cluster representation of a heterogeneous polymer and therefore does not establish the full porous solid, pressure-dependent free energies or a unique global transition state. Electronic barriers should be compared within the submitted computational model and accompanied by method, stationary-point and connectivity diagnostics. Experimental conversion/selectivity is contextual validation, not a substitute for a validated molecular pathway.
