# Private paper route

## 1. Scientific objective and author claim

The paper studies Li nucleation on Cu(111). Its computational claim is that the average Li adsorption strength becomes less favorable as first-layer coverage increases, helping explain the observed time-dependent decrease in the apparent deposition-rate coefficient. The authors compare an isolated Li atom with fcc-hollow Li adlayers, including a complete first layer.

## 2. System and model boundary

The model is a periodic Cu(111) slab built from a Cu lattice constant of 3.63 Å, five Cu layers, p(5×5) lateral periodicity and 15 Å vacuum. The upper three Cu layers relax and the lower two are fixed. Li is referenced to a neutral isolated atom. The first-layer endpoint systems are one Li in the p(5×5) cell (θ=0.04) and a full fcc-hollow adlayer (θ=1).

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish clean Cu(111) slab and surface-energy convergence | Cu lattice and slab geometry | VASP periodic DFT | PBE, PAW, 500 eV, SCF 10^-6 eV, forces 10^-2 eV/Å, D3(BJ), Γ-centered 5×5×1, five layers, top three relaxed, 15 Å vacuum | Relaxed slab and surface energy | ev_doc_5cc5865526ad_000064_666bd989bfed; ev_doc_5cc5865526ad_000070_726a70cef845; ev_doc_5cc5865526ad_000075_fb65c83e9cfd; ev_doc_5cc5865526ad_000087_aa8dce122033 |
| 2 | Evaluate Li adsorption at coverages | Relaxed slab, fcc hollow sites, one or 25 Li atoms | VASP periodic DFT | Isolated Li relaxed in z; coverage structures relaxed in all directions; same electronic settings | Total energies for clean, θ=0.04 and θ=1 systems | ev_doc_5cc5865526ad_000087_aa8dce122033; ev_doc_5cc5865526ad_000268_10f6e468e10a; ev_doc_5cc5865526ad_000272_9e977e3b0af1 |
| 3 | Convert total energies to average adsorption energy | E(nLi@surf), E(surf), E(Li) | E_ads=(E(nLi@surf)-E(surf)-nE(Li))/n | Energies extrapolated to 0 K | Endpoint adsorption energies and coverage trend | ev_doc_5cc5865526ad_000098_66fecde873d7; ev_doc_5cc5865526ad_000099_cc1776b7aca9 |

## 4. Validation and analysis protocol

The authors checked Cu(111) surface-energy convergence with slab thickness and reported a converged five-layer value. They checked adsorption-energy convergence with supercell size. For the first layer they sampled p(2×2) and p(3×3) coverages and included the p(5×5) isolated-atom reference; Figure 6 reports a monotonic weakening with coverage and a marked rise between θ=0.33 and 0.5.

## 5. Private reference results

The paper reports first-layer average adsorption energies of −2.63 eV at θ=0.04 and −2.05 eV at θ=1. It reports a general increase from more negative to less negative values with coverage, with a pronounced rise between θ=0.33 and 0.5. The clean Cu(111) surface energy is reported as 1.31 J/m².

## 6. Limitations and interpretation boundaries

These are idealized vacuum periodic-slab calculations, not explicit-electrolyte free energies or electrochemical potentials. Coverage is represented by ordered fcc-hollow adlayers and does not establish kinetics by itself. Numerical agreement is method- and geometry-dependent; the task evaluates the stated model boundary and requires the Agent to report convergence and residual uncertainty.
