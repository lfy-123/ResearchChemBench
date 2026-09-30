# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to explain the strong ortho regioselectivity in the phosphoric-acid-catalyzed intramolecular cyclodehydration of substrate 1a. The authors claim that catalyst organization and simultaneous activation of the ketone and phenolic OH favor the cyclization transition state leading to the 4-hydroxybenzofuran pathway over the competing para pathway.

## 2. System and model boundary

The modeled system is neutral, singlet substrate 1a, 1-(3-hydroxyphenoxy)propan-2-one, associated with one equivalent of bis(p-nitrophenyl) phosphate in implicit toluene at 298.15 K. The mechanistic comparison concerns the first intramolecular Friedel–Crafts cyclization, not the later dehydration steps. The paper labels the productive and competing cyclization transition structures TS1 and TS1′ and the common catalyst-bound precursor INT1.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain stationary-point geometries | Catalyst-bound substrate and candidate pathway structures | Gaussian 16 geometry optimization | B3LYP-D3/6-31+G(d), ultrafine grid, SMD(toluene), 298.15 K | Optimized INT/TS structures | ev_doc_6f9e4d0f8641_001314_fabedf206958 |
| 2 | Classify stationary points and obtain thermochemistry | Optimized structures | Gaussian 16 harmonic frequencies; IRC for TSs | Same level and solvent; TSs required to connect the relevant minima | Gibbs free energies and TS connectivity | ev_doc_6f9e4d0f8641_001314_fabedf206958 |
| 3 | Refine electronic energies | Frequency/IRC-validated structures | Gaussian 16 single points | B3LYP-D3/6-311+G(d,p), ultrafine grid, SMD(toluene), 298.15 K | Refined energies | ev_doc_6f9e4d0f8641_001314_fabedf206958; ev_doc_6f9e4d0f8641_001320_6db4847e2947 |
| 4 | Compare regioselective barriers | Validated TS1, TS1′ and common reference | Relative free-energy analysis | Barrier difference referenced to the same catalyst-bound precursor | ΔΔG‡ and mechanistic interpretation | ev_doc_99072196e953_000094_5bb2b58ab294 |

## 4. Validation and analysis protocol

The authors identify minima by the absence of imaginary frequencies and transition structures by one imaginary frequency; IRC traces are used to connect each transition structure to the appropriate local minima. The comparison is kinetic: the two cyclization transition structures are compared relative to the same catalyst-bound reference, and the lower barrier is interpreted as the favored regiochannel. The authors also inspect catalyst–substrate hydrogen-bonding geometry in the transition structures.

## 5. Private reference results

The SI reports a negative imaginary frequency for TS1 and provides the stationary-point coordinates and energies in Section 12. The main paper reports that TS1′ is higher than TS1 by ΔΔG‡ = +7.6 kcal/mol, and attributes this to dual carbonyl/phenolic-OH activation in the lower transition structure versus carbonyl activation alone in the competing structure. The paper connects this calculated preference with the experimentally observed >99:1 ratio for 2a over 2a′ under the stated catalytic conditions.

## 6. Limitations and interpretation boundaries

The result is a single-level implicit-solvent DFT model and does not establish a universally complete reaction mechanism. It addresses the relative first cyclization barriers for the defined substrate/catalyst system. Conformer coverage, anharmonic effects, explicit solvent, catalyst aggregation and kinetic prefactors are outside the source-backed claim unless independently investigated and reported as limitations.

## 7. Primary quantitative protocol and optional controls (2026-09-27)

SI Section 9 (PDF p59) defines the B3LYP-D3/6-311+G(d,p)//B3LYP-D3/6-31+G(d), ultrafine-grid, SMD(toluene) protocol. For an unambiguous primary comparison the benchmark states the verified implementation: zero-damped D3 (Gaussian GD3), 298.15 K/1 atm, and G = E_high + (G_low - E_low) with unscaled harmonic low-level corrections. These implementation details are not a claim that the SI spells out every default. SI Table S5 (PDF p61) reports additional functionals with different quantitative gaps. The existing 7.6 +/- 1.5 reference applies to the primary protocol, not to all alternative methods. The actual verified gap of +7.528199785 kcal/mol supports this protocol. Optional controls remain allowed and unpenalized; their values must not be substituted for the required primary comparison. No TS geometry, barrier, ranking or private verification artifact was added to agent inputs.
