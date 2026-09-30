# Private paper route

## 1. Scientific objective and author claim

The paper studies Li nucleation on Cu(111). Its computational claim is that the average Li adsorption strength becomes less favorable as first-layer coverage increases, helping explain the observed time-dependent decrease in the apparent deposition-rate coefficient. The authors compare an isolated Li atom with fcc-hollow Li adlayers, including a complete first layer.

## 2. System and model boundary

The author models use Cu(111) at a Cu lattice constant of 3.63 Å, five Cu layers and 15 Å vacuum, with the upper three Cu layers relaxed and the lower two fixed. The isolated-Li endpoint is one Li in p(5×5), θ=0.04; the full first-layer coverage in main-text Figure 6a uses p(2×2), with 20 Cu and 4 Li. Both use fcc-hollow adsorption. The public task also supplies a p(5×5), 25-Li full-layer representation; that supplied benchmark representation must not be misattributed to the author Figure 6a calculation. Each cell requires its own matching clean-slab reference; raw p2 energies must never be relabeled as p5 energies.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish clean Cu(111) slab and surface-energy convergence | Cu lattice and slab geometry | VASP periodic DFT | PBE, PAW, 500 eV, SCF 10^-6 eV, forces 10^-2 eV/Å, D3(BJ), Γ-centered 5×5×1 for p5 or 13×13×1 for p2, five layers, top three relaxed, 15 Å vacuum | Relaxed slab and surface energy | ev_doc_5cc5865526ad_000064_666bd989bfed; ev_doc_5cc5865526ad_000070_726a70cef845; ev_doc_5cc5865526ad_000075_fb65c83e9cfd; ev_doc_5cc5865526ad_000087_aa8dce122033 |
| 2 | Evaluate Li adsorption at coverages | Relaxed slab, fcc hollow sites, one Li/p5 or four Li/p2 in the author endpoint calculations | VASP periodic DFT | Isolated Li relaxed in z; coverage structures relaxed in all directions; same electronic settings | Total energies for clean, θ=0.04 and θ=1 systems | ev_doc_5cc5865526ad_000087_aa8dce122033; ev_doc_5cc5865526ad_000268_10f6e468e10a; ev_doc_5cc5865526ad_000272_9e977e3b0af1 |
| 3 | Convert total energies to average adsorption energy | E(nLi@surf), E(surf), E(Li) | E_ads=(E(nLi@surf)-E(surf)-nE(Li))/n | Energies extrapolated to 0 K | Endpoint adsorption energies and coverage trend | ev_doc_5cc5865526ad_000098_66fecde873d7; ev_doc_5cc5865526ad_000099_cc1776b7aca9 |

## 4. Validation and analysis protocol

The authors checked Cu(111) surface-energy convergence with slab thickness and reported a converged five-layer value. They checked adsorption-energy convergence with supercell size. For the first layer they sampled p(2×2) and p(3×3) coverages and included the p(5×5) isolated-atom reference; Figure 6 reports a monotonic weakening with coverage and a marked rise between θ=0.33 and 0.5.

## 5. Private reference results

The paper reports first-layer average adsorption energies of −2.63 eV at θ=0.04 and −2.05 eV at θ=1. It reports a general increase from more negative to less negative values with coverage, with a pronounced rise between θ=0.33 and 0.5. The clean Cu(111) surface energy is reported as 1.31 J/m².

## 6. Limitations and interpretation boundaries

These are idealized vacuum periodic-slab calculations, not explicit-electrolyte free energies or electrochemical potentials. Coverage is represented by ordered fcc-hollow adlayers and does not establish kinetics by itself. Numerical agreement is method- and geometry-dependent; the task evaluates the stated model boundary and requires the Agent to report convergence and residual uncertainty.

## Source/identity correction (2026-09-23)

Main-text pp.2–3 specify the cell-dependent k meshes, z-only relaxation of the isolated adsorbed Li, all-direction coverage relaxation and sigma→0 total energies. Figure 6a on p.6 assigns theta=1 to p(2×2), not p(5×5). The earlier route description conflated that author model with the supplied benchmark supercell. The isolated neutral Li atom is a doublet; this follows from its physical ground-state identity, whereas the source does not print a spin input line. No reference adsorption values, tolerances, scientific objective, coordinate files or evaluator rules were changed.

## Second-stage public geometry correction (2026-09-23)

A subsequent native-coordinate audit found that the public XYZ files, despite fcc labels, contained ABABA stacking and hcp-hollow Li (above the second, not third, Cu layer). The three slab XYZ files now use five-layer ABCAB fcc Cu at a=3.63 Å and Li above the third Cu layer. The manifest cell vectors now use the exact lattice-derived values instead of inconsistent rounded values. Atom counts, p5 coverage representations, all z starting values, goals and all evaluator files remain unchanged. The native author-route p2/p5 calculations already used correct ABC stacking and are not restarted. This correction supersedes the phase-one statement of unchanged coordinate files; both before snapshots are retained.
