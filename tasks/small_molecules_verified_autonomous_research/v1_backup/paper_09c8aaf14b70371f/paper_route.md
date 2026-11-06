# Private author route: chalcone reduction structure-property series

Scope version: chalcone-series-redox-20261012. The public task is a physical-organic property investigation, not a synthesis or thermal-isomerization mechanism task. User approval authorized this replacement; the author methods remain private.

The main paper p.2 section 2.3 reports Gaussian 16 B3LYP/6-311+G(2df,2p) optimizations and frequencies for neutral and reduced chalcones, in gas and IEF-PCM solvents. Tables 5-7 (pp.9-11) compare E/Z conformers and guide the subsequent representative E structures. SI pp.24-27 supplies one coordinate block per compound without complete state/solvent labels. The exact input route, grid and open-shell implementation are not supplied; implementation choices must be documented rather than attributed to the authors.

| Stage | Author calculation / source | Verification boundary |
|---|---|---|
| Identity and conformer attribution | Table 1; Tables 5-7; SI pp.1-3,24-27 | Verify full graphs and property conformer; compound 2 E1 minimizes G while E2 minimizes E. Do not guess which is the property reference. |
| Neutral orbital results | Table 4 p.7, Figs.11/13 pp.13-14 | ACN/DMSO 1-5, with 2 held until attribution; reproduce orbital eigenvalues, not absolute potentials. |
| Electron addition | Figs.11-12 pp.12-13 | Neutral orbitals plus anion spin plots in gas/ACN/DMSO; current required solution range ACN/DMSO. One-electron addition conserves atoms; doublet is the modeled odd-electron state. |
| Solvent comparison | Fig.14 p.14 | Compound 3 neutral DCM result in addition to ACN/DMSO. No reported DCM anion plot is a reference. |

Source LUMO eigenvalues (eV; source context, no new calibrated windows):

| Compound | Gas | ACN | DMSO |
|---|---:|---:|---:|
| 1 | -2.497 | -2.537 | -2.540 |
| 2 (attribution hold) | -2.427 | -2.493 | -2.496 |
| 3 | -2.507 | -2.538 | -2.540 |
| 4 | -2.426 | -2.470 | -2.473 |
| 5 | -2.133 | -2.293 | -2.298 |

The measured Epc values are in the public card and the Table 4 experimental columns. Fig.13 relates computed LUMO energies to experimental Epc: 3-5 form the fitted subset; 1/2 depart. Only three fitted points do not establish universal prediction or unique 2-prime-OH causation. Compound 1 versus 3 already demonstrates the boundary: nearly equal LUMO energies and distinctly different peak potentials. Compound-2-dependent acceptance targets are currently withheld explicitly in scoring_rules.json and qualification.json.

For 3 the DCM LUMO is -2.508 eV (Fig.14), higher than ACN -2.538 and DMSO -2.540 eV. Moving DCM to ACN/DMSO lowers the LUMO and shifts measured Epc from -2.019 to -1.859/-1.851 V. This resolves an ambiguous direction phrase in the design summary using the original values. Table 4 gives an ACN/DMSO LUMO difference of 0.005 eV for 5; the prose claim below 0.004 eV is not an acceptance threshold.

Figs.11-12 support the importance of the conjugated enone with aryl delocalization. Compare actual wavefunction-derived spatial evidence; no author atomic-spin percentages or numerical spatial-match windows exist. Figure contour values are plotting conventions, not charge fractions.

Reuse compatible validated 3/E geometry/frequency evidence before new work. The latest legacy audit, /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/verification/small_molecules_autonomous_research/paper_09c8aaf14b70371f/remaining24_20261012T134810Z_group_A/verification_report.md, is MISMATCH for the old full E/Z contract; it validates four endpoints but rejects the near-planar QST3 candidate as the wrong saddle. Retiring that question does not convert the old failure into PASS. New series results remain unverified. See evaluation/validation_plan.json and evaluation/qualification.json.

Do not expand verification or scoring to absolute reduction-potential cycles, electron-transfer kinetics, anion decomposition/proton transfer, causal energy decomposition, TD absorption/photodynamics, calculated NMR, other chalcone TSs or synthetic mechanisms. Author hypotheses about these processes are not computed references.
