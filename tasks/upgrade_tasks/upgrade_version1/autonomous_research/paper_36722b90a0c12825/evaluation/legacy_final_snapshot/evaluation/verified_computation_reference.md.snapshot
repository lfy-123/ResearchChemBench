# Verified computation reference — paper_36722b90a0c12825 (autonomous_research)

> Evaluator-private computation archive, not agent input or a scoring route. Reconciled 2026-09-18 from existing successful outputs; no new quantum calculation and no public-starter blind replay. The evaluator's scientific key points and conclusions remain the grading authority.

## Matched close/open calculation

The current primary comparison is the two chloride-complex conformers, each charge −1, singlet, B3LYP-D3BJ/6-31G(d), PCM acetone with the Gaussian UFF cavity, harmonic Gibbs free energy at 298.15 K and 1 atm. SI p. 16 prose specifies 298.15 K while table headings say 300 K; this task explicitly uses the archived 298.15 K route. The source's PCM-only and D3BJ columns are different protocols; their signs must not be mixed.

1. Preserve each named 101-atom complex and atom mapping; use the same charge/spin and chemical composition.
2. Run the completed close and open Gaussian Opt/Freq branches with `B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt=(Tight,MaxCycles=300) Freq SCRF=(PCM,Solvent=Acetone) NoSymm SCF=(XQC,MaxCycle=512)`.
3. Check normal termination, optimization completion and 297 real physical frequencies for each. Earlier wrong-charge or no-solvent attempts are not part of this successful chain.
4. Subtract the same-definition harmonic G values: ΔG = G(open)−G(close). Convert Hartree to eV once.

| Object | G / Eh | Physical modes | Imaginary modes |
|---|---:|---:|---:|
| close | −4269.381480 | 297 | 0 |
| open | −4269.344781 | 297 | 0 |

ΔG = 0.036699 Eh = **+0.9986306638456881 eV**, about **96.35 kJ/mol**. This supports a lower G for close under this specified protocol; it is **not near-degeneracy**. The historical report's “near-degeneracy” wording is superseded here without editing that raw report. Evaluator reference +0.997 eV and ±0.25 eV tolerance remain unchanged.

## Successful output anchors

- [close calculation directory](../../../../docs/verification/group_4/paper_36722b90a0c12825/hpc_runs/close_author_b3lyp_d3bj_pcm_acetone_optfreq_chargefix_retry1_hpc20_p6).
- [open calculation directory](../../../../docs/verification/group_4/paper_36722b90a0c12825/hpc_runs/open_author_b3lyp_d3bj_pcm_acetone_optfreq_chargefix_retry1_hpc20_p6).
- [Original parsed results](../../../../docs/verification/group_4/paper_36722b90a0c12825/report/results.json), retained as historical data, with the interpretation correction above.

These two branches demonstrate the requested conformer comparison. They are not a complete conformational ensemble or measured equilibrium kinetics. This is an archive statement, not a mandatory disclaimer for model submissions.

## Evidence scope review (2026-09-19)

The primary close/open comparison is supported. The current task also requires a successful comparable sensitivity check. A failed, wrong-charge or unfinished retry is not that check; reference coverage of this requirement remains pending unless a corresponding successful artifact is supplied. No new computation was run in this revision.
