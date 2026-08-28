# Private paper route

## 1. Scientific objective and author claim

The paper quantifies how hydration of the proton pathway changes chloride-ion permeation in the EcCLC homodimer. The authors claim that water in chain A lowers the PMF barriers for chloride leaving the central site, while chloride dissociation also widens and hydrates the proton pathway.

## 2. System and model boundary

The modeled system is EcCLC from PDB 1OTS in a 120 Å × 120 Å POPE bilayer, TIP3P water and 200 mM NaCl, with periodic 120 Å × 120 Å × 80 Å dimensions. Missing hydrogens were added; E113, H175, H281 and H284 in both chains, R417 in chain A, and E148 in both chains were protonated. Chain A is the water-containing proton pore and chain B the water-depleted comparison.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build and relax membrane system | PDB 1OTS | VMD/PSFGEN, CHARMM36 | POPE; TIP3P; 200 mM NaCl; 5000 minimization steps | solvated bilayer system | ev_doc_a50460585d15_000092_e9472315d74f; ev_doc_a50460585d15_000101_b1265eb0993b |
| 2 | Equilibrate protein/membrane/solution | built system | NAMD MD, NPT | 300 K, 1 atm Langevin piston, PME, 10 Å cutoff smoothed at 8 Å, 2 fs; 2 ns fixed-protein then 470 ns free | equilibrated trajectory; Cα RMSD stable in final 150 ns | ev_doc_a50460585d15_000101_b1265eb0993b |
| 3 | Generate transport paths | equilibrated chloride at S_cen | cv-SMD | Z coordinate referenced to protein Ca center; 10 kcal mol−1 Å−2 spring; 0.02 Å ps−1 in both directions; ~1.6 ns | starting structures along Z | ev_doc_a50460585d15_000136_2690317b8cc |
| 4 | Estimate chloride PMFs | SMD structures | NAMD ABF | 1 Å non-overlapping regions; ≥5 ns/region; 5 ns merge; six 0.2 ns samples; A −8.5 to 9.5 Å, B −5.5 to 6.5 Å; ≥95/65 ns total | PMFs and error bars | ev_doc_a50460585d15_000136_2690317b8cc; ev_doc_a50460585d15_000137_de780c52294c; ev_doc_a50460585d15_000138_3ae9129dcc59 |
| 5 | Test chloride effect on proton pore | chain-A equilibrated snapshots | SMD removal then MD | 250 ns from out state; independent 200 ns from up snapshot | chloride-free re-equilibrated trajectories | ev_doc_a50460585d15_000269_27146df0d9fa |
| 6 | Analyze structures | trajectories | HOLE and trajectory analysis | final 100 ns; five snapshots ≥10 ns apart | pore radius, water count, E148 states | ev_doc_a50460585d15_000300_34b315692259 |

## 4. Validation and analysis protocol

Equilibration was assessed by Cα backbone RMSD; PMF convergence was assessed from six independently merged PMF estimates and their error bars. Three PMF valleys near Z = −6, 0 and 4.5 Å were assigned to S_ext, S_cen and S_int. The paper compared water-containing and water-depleted chains and checked the chloride-free perturbation with RMSD. Structural analysis used the equilibrated final 100 ns and compared pore radius, water count and E148/F199/F357 behavior.

## 5. Private reference results

With pore water, the reported barriers from S_cen are 8.5 kcal/mol toward S_ext and 19.0 kcal/mol toward S_int. Without pore water they are 16 and 28 kcal/mol, respectively. Water therefore lowers both barriers. The water-containing PMF has three sites and S_cen is lowest. Chloride removal expands the proton pore and raises its water population from 9.3 ± 1.5 to 16.0 ± 2.4; the chloride-free E148 down state dominates (93.92% in the reported analysis), while the bound system is predominantly out. The reported water-chain formation rate is 4.18 ± 0.75 ns−1.

## 6. Limitations and interpretation boundaries

These are force-field PMFs for the specified protonation, membrane, salt and finite sampling protocol, not universal experimental barriers. Chain identity is a model condition, not an assertion that every EcCLC molecule has permanently hydrated or dehydrated pores. PMF uncertainty, conformational sampling and finite trajectory length must be reported; conclusions should be limited to the defined model and validation evidence.
