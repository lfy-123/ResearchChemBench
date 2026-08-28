# Private paper route

## 1. Scientific objective and author claim

The paper computes the mechanism of the Zn-catalyzed Cadiot–Chodkiewicz coupling of p-tolylacetylene (R1) with 1-bromo-2-phenylacetylene (R2) to form an unsymmetrical 1,3-diyne. Its central claim is that a redox-neutral Zn(II)/L-proline pathway is operative and that the computed free-energy span explains the need for 125 °C operation.

## 2. System and model boundary

The model reaction contains diethylzinc, L-proline, cesium carbonate base, R1, and R2 in ethanol. The reported cycle uses neutral Zn(II)[L-proline]2 (Int-1), a zinc-alkynyl intermediate (Int-2), an alkynyl-halide activation transition state (TS), and Int-3/product regeneration. The authors also examine and reject a Zn(0) redox-active alternative.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize reactants, intermediates, TS and product | Molecular structures for the Zn/proline coupling model | Gaussian 09 | B3LYP-D3; 6-31+G(d) for C,H,N,O; LANL2DZ ECP for Zn,Cs,Br; CPCM ethanol (ε=24.852); unconstrained optimization; 298.15 K | Optimized stationary points | ev_doc_dcc2978008ce_000028_39a486c78d0b; ev_doc_dcc2978008ce_000030_22df6580dc60 |
| 2 | Classify stationary points and obtain thermochemistry | Optimized structures | Gaussian 09 frequency analysis | Same level and solvent | Zero/one imaginary-frequency assignments, ZPVE and thermal Gibbs corrections | ev_doc_dcc2978008ce_000028_39a486c78d0b |
| 3 | Verify the reaction saddle point | Optimized TS | Gaussian 09 IRC | Berny TS search followed by IRC | Connectivity from TS toward Int-2 and Int-3 | ev_doc_dcc2978008ce_000028_39a486c78d0b |
| 4 | Build the free-energy profile and span | Gibbs energies for Int-1, Int-2, TS, Int-3, R1, R2, P and auxiliaries | Authors' energy accounting from Gaussian outputs | Reaction free energies at 298.15 K | Energy span and mechanistic interpretation | ev_doc_dcc2978008ce_000015_a1b21cb5ffca; ev_doc_dcc2978008ce_000058_ac47275d3118 |

## 4. Validation and analysis protocol

Minima were required to have no imaginary frequencies; the TS was required to have one and to pass IRC verification. The authors compared redox-active and redox-neutral formation pathways, examined alternative TS searches, and used the resulting span in an Eyring argument comparing 298.15 K with 398.15 K.

## 5. Private reference results

The SI reports ΔG‡/energy span = 29.2 kcal mol⁻¹. The paper reports Int-2 formation as 9.6 kcal mol⁻¹, Zn(0) precursor decomposition as 46.3 kcal mol⁻¹, cationic Zn(II)[L-proline]2 formation as 95.6 kcal mol⁻¹, and neutral active-catalyst formation as −98.5 kcal mol⁻¹. The authors report rate estimates of 2.4×10⁻9 s⁻¹ at 298.15 K and 7.9×10⁻4 s⁻¹ at 398.15 K.

## 6. Limitations and interpretation boundaries

These are gas/continuum-solvent DFT thermochemical models with finite conformer and pathway coverage. The source supports a mechanistic interpretation for the stated model system, not a universal claim for every Zn coupling. Numerical comparisons should state the method, standard-state convention, temperature, and whether the reported span is a barrier or an energy-span construction.
