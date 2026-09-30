# Reference validation plan — EXPANDED REFERENCE PENDING

Personally read main PDF pp2–5 and visually checked Figs.2–3 on p3. The source isolated series preserves a complete P-centered Al12 shell and intact borane ligands; claims of shell retention additionally use orbital analysis. Figure 4/associated discussion distinguishes electronic-level shifts, fragment mixing and charge transfer.

Personally read the formal DOCX SI: Gaussian16/PBE0/def2-SVP, spin/site search, same-level frequency/ZPE and Hirshfeld/Multiwfn; VASP PBE-D3 and 300-K 10-ps AIMD are separate calculations. Figs S1–S4 show optimized structures, S6–S8 electronic evidence, S9 AIMD; no complete Cartesian table is present. The original missing-SI issue is resolved, but this is not an intact-endpoint validation.

## Reusable evidence and limits

The 2026-09-27 verification inventory recovered eight historical Gaussian PBE0/def2SVP n2 local-minimum candidates with 81 atoms and 237 positive frequencies. An independent supervisor parse checks raw log/input hashes, stationarity, the P-centered icosahedral Al12 adjacency and both element-labelled ligand graphs. The selected opposite-site neutral doublet and anion singlet retain the complete object; their electronic AEA is 3.9455364457428788 eV and ZPE-corrected AEA is 3.959169350252118 eV. These are historical baseline values, never expanded acceptance targets or tolerances. Native atom order differs from the public map; use the explicit graph mapping in task_provenance/historical_n2_reaudit.json. Other local minima include long Al-B contacts and require candidate-specific attachment interpretation. No global-minimum or shell-orbital claim follows. The later AR GFN2 reconstructed aggregate and unconverged PBEh-3c runs remain invalid intact endpoints, but do not erase the earlier valid Gaussian evidence. The full expanded reference remains pending.

## Explicit missing prerequisites

- The expanded n0/n1/n2 free, common-core constrained and vertical matrix remains incomplete.
- Same-geometry added-electron density, normalization/grid controls and diffuse-basis/state sensitivity remain unvalidated.
- Expanded uncertainty references and independent mode trials have not been calibrated; historical local minima do not prove a global minimum or superatomic shell character.

## Minimum pilot and release sequence

1. Developers may reuse the independently audited historical n2 free-minimum pair after checking raw hashes, native-to-public atom mapping, charge/spin and ligand attachment. Preserve failed and detached candidates. Evaluated agents must still establish their own authorized evidence.
2. Complete the missing n2 vertical-anion and same-geometry density pilot, with normalization/grid and diffuse-basis/state sensitivity; do not repeat equivalent Opt/Freq work merely because a later run failed.
3. Build and validate mapped n0/n1 free endpoints and the shared bare-neutral-core constrained series, then complete signed comparisons and independently calibrate uncertainty from actual method/numerical controls.

## Full expanded reference

Six validated free charge-state endpoints for completion; rigorously evidenced excluded n2 states can be documented in partial results, three vertical anion points, common-core electronic controls for every retained n/state, pairwise n1−n0/n2−n1 comparisons and shared-grid density/population analysis. Record candidate collapse without inventing distinct minima. Do not require full Al13/CAl12, graphene, AIMD or electrostatic embedding.

## Software and quantitative calibration

Allowed Gaussian/ORCA molecular engines plus supported density export/Multiwfn analysis can implement the pilot. PBE0/def2-SVP is a source baseline, not a verified diffuse-anion reference; calibrate a diffuse/basis sensitivity. xTB/CREST may generate starts but cannot substitute for intact DFT endpoints. Numerical uncertainty must be measured from converged raw calculations, model variation and geometry sensitivity. Paper numbers remain historical anchors only; there is no newly calibrated absolute tolerance, ranking or winner. Do not impose optional extensions as gates.

## Actual work in this upgrade

No new quantum, periodic or transport engine was launched. Local source reading, graph/stoichiometry checks and schema tests are development work. Preserve inputs, failed/restarted jobs, actual engine launches, CPU allocation and engine times when a future pilot is authorized and budgeted. Current scope is a development package, not a released benchmark or validated scientific reference.
