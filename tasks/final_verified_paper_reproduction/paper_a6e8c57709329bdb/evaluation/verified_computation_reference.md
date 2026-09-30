# Verified computation reference — paper_a6e8c57709329bdb (paper_reproduction)

> Evaluator-private computation archive, not agent input or a scoring route. Reconciled 2026-09-18 from existing successful outputs; no new quantum calculation and no public-starter blind replay. The evaluator's scientific key points and conclusions remain the grading authority.

## Correct-object successful chain

This replaces the older wrong-regioisomer archive, retained only in Git history. The object is HL, C20H22N4O6, 52 atoms, neutral singlet, two E imines. On each ring OH is ortho and OMe para to the imine attachment. The archived graph is `COc1ccc(/C=N/NC(=O)CCC(=O)N/N=C/c2ccc(OC)cc2O)c(O)c1`. Formula alone was not used to validate identity.

1. Recover the named graph from main Scheme 1 / SI Fig. S17. Generate candidates from that identity; the preparation archive records 62 embeddings, 21 MMFF-deduplicated representatives and one DFT candidate. No paper endpoint was used to infer an alternative regioisomer.
2. Run Gaussian 16 C.01, gas B3LYP/6-31G(d,p), neutral singlet, `Opt=(Tight,CalcFC,MaxCycles=240) Freq Int=UltraFine SCF=(Tight,XQC,MaxCycle=512) NoSymm Temperature=298.15 Pop=Full`. [Actual input](../../../../docs/verification/group_1/paper_a6e8c57709329bdb/provenance/qzcli_hpc/hl_orthoOH_paraOMe_B3LYP631Gdp_20260916/repair_20260916T071832Z/input.com) and [Successful Opt/Freq log](../../../../docs/verification/group_1/paper_a6e8c57709329bdb/provenance/qzcli_hpc/hl_orthoOH_paraOMe_B3LYP631Gdp_20260916/repair_20260916T071832Z/gaussian.log) are the primary execution evidence.
3. Verify the optimized graph and both imine dihedrals (−179.9723°, 179.8522°). The log records normal termination, completed optimization and 150 positive modes (minimum 3.5593 cm⁻¹). Electronic energy is −1445.72650236 Eh.
4. Extract occupied/unoccupied frontier energies from this same successful branch; compute their difference using the same Hartree/eV conversion. Analyze its final checkpoint with native Multiwfn Mulliken MO populations, including AO overlap, not squared coefficients alone. One-based orbitals 109/110 are HOMO/LUMO.

| Observable | Existing computed value |
|---|---:|
| HOMO | −5.21635046991403 eV |
| LUMO | −1.562399649864471 eV |
| Gap | 3.653950820049559 eV |
| Aromatic/azomethine HOMO population | 67.35879% |
| Aromatic/azomethine LUMO population | 77.81639% |
| Saturated-bridge HOMO / LUMO population | 0.28872% / 1.34287% |

The saturated methylene bridge is a weak LUMO participant, not the dominant LUMO region. The primary orbital population resides on aromatic/azomethine fragments. These calculations support the specified molecular frontier-orbital comparison, not an optical excitation or metal-binding calculation.

## Atom groups and reproducible extraction

One-based Gaussian atom groups are: aromatic/azomethine π = 3,4,5,6,7,8,17,18,19,20,21,22,25,26,28,30,34,35,36,43,44,45,49,52; hydrazide/carbonyl = 9,10,11,14,15,16,37,42; saturated bridge = 12,13,38,39,40,41; phenol/methoxy substituents = 1,2,23,24,27,29,31,32,33,46,47,48,50,51. Sum the printed atomic Mulliken contributions within each group separately for orbitals 109 and 110.

[Optimized structure](../../../../docs/verification/group_1/paper_a6e8c57709329bdb/artifacts/source_hl_closure_20260916/optimized_hl.xyz) · [Final wavefunction](../../../../docs/verification/group_1/paper_a6e8c57709329bdb/artifacts/source_hl_closure_20260916/wavefunction.fchk) · [Native orbital-population output](../../../../docs/verification/group_1/paper_a6e8c57709329bdb/artifacts/source_hl_closure_20260916/frontier_mulliken.out) · [Analysis invocation](../../../../docs/verification/group_1/paper_a6e8c57709329bdb/artifacts/source_hl_closure_20260916/frontier_mulliken.json) · [Independent raw-evidence extraction](../../../../docs/verification/group_1/paper_a6e8c57709329bdb/provenance/source_hl_raw_evidence_20260916.json).

Main p. 7 gives the B3LYP/6-31G(d,p) route. Historical verification may start from author information; no independent discovery from current public inputs is claimed here. No evaluator target was used as a computed value, and no target/tolerance was changed in this archival repair.
