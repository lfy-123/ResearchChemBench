# Stage06/07 v5 completed-artifact review (pre-Round-6 terminal results)

This note records the two scientifically approved artifacts that became
available in the earlier DeepSeek batch while the new Round-6 ten-paper batch
was still running. It is not used as a substitute for the required Round-6
sample; it documents what can already be checked without guessing.

## `paper_9ec8c4761c4f171b` — representative core subworkflow

The source/SI route contains a heterogeneous program: tautomer energetics,
18-molecule B3LYP-D3(BJ)/6-311+G* gas/CHCl3 geometry/frequency calculations,
TDDFT spectra, and non-QM branches. Stage06 explicitly attempted the full
program and recorded why it was not one coherent, feasible objective. It chose
the central HOMO/LUMO-to-experimental-optical-gap calibration branch for all 18
compounds. The source SI confirms coordinates for the 18 compounds and the
public inputs contain 36 geometry files plus the 18 experimental optical gaps.

Stage07 independently checked the paper claims and alternatives, preserved the
selected core, and recorded a representativeness audit. It repaired public
autonomous disclosure, route-map leakage, result bindings, and mode-specific
acceptance profiles. The published pair passed both the mechanical gate and the
published-bundle check. No current code or Prompt defect is indicated here.

## `paper_12c3b0b392f4dc14` — scientific approval, old mechanical block

Stage06 and Stage07 selected the closed DFT conformer/thermochemistry/FMO route
because the supplied snapshot lacked the CIF coordinates and full docking
protocol needed for other paper claims. Stage07's representativeness audit
states that the selected route covers the paper's stable-conformer and
HOMO/LUMO stability claims while honestly omitting crystal-packing, docking,
spectral, and biological branches. This is consistent with the v5 full-route
priority rule and is not a scientific rejection.

The old published attempt was blocked solely because Agent output used result
labels (`HOMO_energy`, `conformer_geometries`, etc.) as string
`required_deliverables`, which violated the Evaluator's typed artifact contract.
The current code replays this exact audited tree successfully after projecting
the labels to the declared submission files. This confirms a genuine generic
contract bug and its fix, not a paper-specific exception.

## Other old-batch failures

`paper_72c3e34e4e3814e2` and `paper_e256c53cbb43ab35` failed in the old Stage06B
converter before the latest prompt clarification (`d536bc0`) was present. They
remain useful negative fixtures, but cannot establish a post-fix common failure
until a new batch reaches terminal artifacts.

## Boundary for the next review

Round-6 currently has no terminal paper results. Once it does, each of its ten
papers must be checked against the paper/SI title, abstract, main figures/tables,
conclusion, selected full/core scope, input closure, software-gap registration,
Stage06B isolation, Stage07 scientific audit, and mechanical publication state.
Only a repeated post-fix transport failure should trigger another code change or
Stage07B consideration.
