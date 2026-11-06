# case_06 Private scoring guide

**Do not provide to ARCHE.** Paper: Construction of chiral nitrogen stereocenters via enantioselective C–H activation; DOI 10.1016/j.chempr.2025.102730.

Source locations: Main text p7–9 Fig.7–10. The main text and SI are located in 03_论文原文_仅供评测者/case_06/.

## Scoring items

|Item|Points|Scientific judgment|
|---|---:|---|
|ts_gap|10|Common-reference free-energy difference between C–H activation transition states|
|inversion_s|10|Inversion free-energy barrier of isolated S|
|inversion_p|10|Inversion free-energy barrier of isolated P|
|ts_direction|10|Independent direction of stereoselectivity|
|cmd_structure|10|Actual bond changes and configurational assignment in C–H activation|
|inversion_s_identity|10|Structural finding of configurational interconversion in S|
|inversion_p_identity|10|Structural finding of configurational interconversion in P|
|reactivity_conclusion|15|Final: different productive reactivity of the two configurations|
|configuration_conclusion|15|Final: configurational stability under separate conditions and the limits of DKR inference|

Whole-case success requires all required scientific items to pass; the 100-point scientific score only helps display partial completion. There are no process points.

## Item-by-item criteria

### r_ts_gap

Compare G(TS20-b)−G(TS20-a) for the complete Pd/L-pGlu/S system with the same composition and particle/proton inventory, and map the authors' a/b structures. This is a difference on a common-reference profile, not a difference between two separately defined local barriers. Use MeCN/SMD, thermal corrections at 363.15 K and the same charge/spin. The source does not specify the input charge/multiplicity; a neutral closed-shell Pd(II)/doubly deprotonated L-pGlu + neutral S system is a graph reconstruction that must be declared and supported. Once genuine relevant saddle points and reaction connectivity qualify, compare against 8.6±1.5 kcal/mol.

Numerical target: 8.6 ± 1.5 kcal/mol.

### r_inversion_s

Compare G(S inversion saddle point)−G(its connected isolated S/1b minimum) for the complete neutral molecule without Pd/ligand and with the same particle count; use MeCN/SMD and 353.15 K. A singlet is a graph-reconstruction assumption that must be supported. Use its own minimum and thermal corrections, genuinely relevant modes and connectivity; compare against 31.82±2.0 kcal/mol. Do not substitute the catalytic temperature of 363.15 K.

Numerical target: 31.82 ± 2.0 kcal/mol.

### r_inversion_p

Compare G(P inversion saddle point)−G(its connected isolated P/3ba minimum) for the complete neutral E-alkenylated molecule without Pd/ligand and with the same particle count; use n-octane/SMD and 398.15 K. A singlet is a graph-reconstruction assumption that must be supported. Use its own minimum/thermal corrections, genuinely relevant modes and connectivity; compare against 33.99±3.0 kcal/mol. Do not switch RRHO/qRRHO, the minimum or the temperature after the fact to approach the target.

Numerical target: 33.99 ± 3.0 kcal/mol.

### r_ts_direction

For the same mapped species, composition, state and MeCN/363.15 K conditions, actual calculations support G(TS20-a)<G(TS20-b). Assess the direction independently; an unmapped comparison or reversed direction fails. Passing the 8.6 numerical window is not a prerequisite.

### r_cmd_structure

Structures, relevant vibrations and connectivity evidence from actual calculations of both configurations support CMD: aryl C–H cleavage, H transfer to a ligand acceptor and C–Pd bond formation, while maintaining a consistent mapping of ligand chirality and seven-membered-ring configuration. A change in a single local signed volume around nearly coplanar nitrogen cannot directly replace a complete configurational assignment; a TS label alone does not pass. A complete catalytic cycle or fixed number of IRC points is not required.

### r_inversion_s_identity

Genuine S minima and inversion saddle points, relevant soft modes/paths or equivalent connectivity support interconversion of the two configurations of the same molecule, preserving composition and protonation, with a positive inversion free-energy barrier at 353.15 K/MeCN. Source coordinates, frequency signs or a statement that inversion is possible alone do not pass; this structural/qualitative result is independent of the 31.82 numerical window.

### r_inversion_p_identity

Genuine E-alkenylated P minima and inversion saddle points, relevant soft modes/paths or equivalent connectivity support interconversion of the two configurations of the same molecule without changing the E alkene or chemical composition, with a positive inversion free-energy barrier at 398.15 K/n-octane. Source coordinates or a statement that the product is stable alone are insufficient; this item does not require passing the 33.99 numerical window.

### r_reactivity_conclusion

In the final conclusion, connect the two validly mapped sets of reaction states and the lower TS20-a to its more favorable productive C–H activation, providing a computationally supported explanation of stereodifferentiation. The 8.6 numerical window need not be passed, but the direction and relevant reaction must be supported by actual results. Do not assert exactly zero reaction through the higher channel, an unmapped absolute configuration, rate control over the full cycle or an exact experimental endpoint ee. An equivalent mechanistic explanation supported by executed work is acceptable.

### r_configuration_conclusion

In the final conclusion, use the computed S/P inversions, their respective minima/solvents/temperatures and corresponding positive barriers to explain that configurational interconversion of the isolated molecules is limited by thermal activation, and relate this to the time courses and observed product stability within explicit bounds. Numerical ordering under separate conditions cannot establish kinetic ordering under identical conditions, rapid S interconversion at 363.15 K/MeCN/36 h or a closed quantitative DKR model. Genuine results for both molecules must support this scientific judgment; a P value outside its numerical window does not automatically invalidate it. Coordinated-state interconversion, a full cycle or exact ee is not required.

## Package changes and reference boundaries

On 2026-10-26, the user explicitly authorized changing only the P-inversion rule r_inversion_p from ±2.0 to ±3.0 kcal/mol around the unchanged target of 33.99 kcal/mol. The existing primary RRHO result of 36.59879981 kcal/mol differs by +2.60879981 kcal/mol and is inside the revised numerical window. This is a documented scoring amendment, not a new calculation or a change of thermochemical convention. Physical comparability and all structural, connectivity and evidence requirements still apply; no whole-case adjudication is inferred from this numerical comparison alone.

Historical records may contain remote /inspire paths, which are background indices only. Scoring in this package does not depend on access to them; historical acceptance status must not be treated as a result of this ARCHE evaluation.
