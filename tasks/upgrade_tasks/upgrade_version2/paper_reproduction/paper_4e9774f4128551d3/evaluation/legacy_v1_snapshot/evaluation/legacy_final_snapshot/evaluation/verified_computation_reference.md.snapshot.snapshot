# Verified computation reference — paper_4e9774f4128551d3 (paper_reproduction)

## Release reconciliation (2026-09-15)

Evaluator-private provenance only. Scoring remains based on the task's intermediate key points and final conclusions. No new quantum calculation was run. Historical verification files under `docs/verification` are read-only.

## Paper basis and input correction

The [SI](../../../../papers/paper_4e9774f4128551d3/documents/supplementary_001.pdf), PDF p. 71, gives the B3LYP-D3 gas Opt/Freq → larger-basis PCM methanol route, dielectric 32.63, and ΔG(sol)=2.3171919 kcal/mol. Tables S35 (PDF pp. 71–73) and S36 (PDF pp. 73–75) provide the two 53-atom structures.

The 2026-09-15 audit found a residual extraction error in **the autonomous package only**: S20 atom rows 40–43 had displaced coordinate tokens. These four rows were corrected directly from SI Table S36 (PDF p. 74); they now agree with the already-correct reproduction package and successful recovered-S20 historical input. No atom identity, stereochemistry, scientific target, charge, multiplicity or tolerance is changed. The prior malformed autonomous file is recoverable from the Git baseline. The reproduction input needed no coordinate change.

This is the approved fixed-structure thermochemistry track, not a task to discover the endpoint structures. Coordinates are authorized input for this property comparison; author energy/ordering results remain private. The autonomous task's contradictory generic ban on its own supplied geometries was clarified without adding author-route information.

## Actual successful calculation chain

1. Use the SI-derived named structure 50 and the recovered, correctly extracted S20, both neutral singlets (53 atoms). After the four-row correction, the public geometries and historical optimization input distance matrices match at printed precision. Raw input/output atom order is retained.
2. Gaussian B3LYP/6-31G(d,p), EmpiricalDispersion=GD3, Opt=(CalcFC,MaxCycles=300), Freq, NoSymm, SCF=(Tight,XQC,MaxCycle=512), Int=UltraFine in gas phase. Each log records optimization completion, normal termination and 153 positive vibrational modes.
3. On each corresponding optimized geometry, Gaussian B3LYP-D3/6-311++G(d,p), IEF-PCM methanol with explicit Eps=32.63 single point. Both logs terminate normally. Pair-distance comparison confirms each SP uses its matched optimized geometry exactly at printed precision; energy and thermal correction are not taken from different structures.
4. Extract G(sol)=E_PCM-SP + gas-phase thermal correction to Gibbs at 298.15 K (Gaussian default pressure convention). Calculate ΔG(sol)=[G(S20)−G(50)] × 627.5094740631 kcal mol⁻¹ Eh⁻¹. No extra unrecorded 1 M correction is invented.
5. Compare the signed thermodynamic difference with the existing 2.3171919 ±1.0 kcal/mol evaluator rule; do not infer a reaction barrier, rate, yield or population.

## Actual energies

| Structure | PCM E / Eh | Thermal G correction / Eh | Combined G / Eh | Frequencies | Imaginary |
|---|---:|---:|---:|---:|---:|
| 50 | -1006.18906600 | 0.416764 | -1005.77230200 | 153 | 0 |
| S20 | -1006.18535194 | 0.417259 | -1005.76809294 | 153 | 0 |

ΔG(sol) = 2.641225027 kcal/mol (approximately 2.641225 in the historical summary). Its difference from the unchanged paper target is 0.324033127 kcal/mol, inside ±1.0. Structure 50 is thermodynamically lower in this model; no kinetic claim follows.

## Raw successful output anchors

- 50: [Opt/Freq](../../../../docs/verification/group_2/paper_4e9774f4128551d3/provenance/qzcli_hpc/author_structure_50_b3lypd3_631gdp_optfreq_hpc20_20260905T233554Z/stdout.log); [matched PCM single point](../../../../docs/verification/group_2/paper_4e9774f4128551d3/provenance/qzcli_hpc/author_structure_50_si_eps3263_pcm_sp_hpc20_20260910T123350Z/stdout.log). Input decks and geometry sections in these exact logs identify the successful chain.
- S20: [Opt/Freq](../../../../docs/verification/group_2/paper_4e9774f4128551d3/provenance/qzcli_hpc/author_structure_S20_si_s36_recovered_optfreq_hpc20_20260910T110100Z/stdout.log); [matched PCM single point](../../../../docs/verification/group_2/paper_4e9774f4128551d3/provenance/qzcli_hpc/author_structure_S20_si_eps3263_pcm_sp_hpc20_20260910T123359Z/stdout.log). Input decks and geometry sections in these exact logs identify the successful chain.

## Historical status and exclusions

The historical `independent_author_route_results_20260914.json` correctly retained an unclosed identity/evaluator-audit flag. This audit explicitly checks the input identity, matched optimized-to-SP geometry, 153-mode stationarity, arithmetic and existing numeric rule. It does not change that historical flag or reinterpret an inventory-only report as a scientific PASS.

Earlier malformed-S20 calculations and alternate PCM settings remain in the group archive but are not used in this primary chain. The valid chain supports the current named-pair thermochemistry target after the autonomous input repair. It is not evidence of blind structure discovery, a global conformer search or a unique prediction at every possible method/solvent.
