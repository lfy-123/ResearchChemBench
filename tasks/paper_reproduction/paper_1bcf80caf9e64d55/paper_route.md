# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to test a plausible PEt3-catalysed alkyne–ester stitching mechanism for substrate 1a and 4-fluorophenol 2a. The authors claim a zwitterion-mediated pathway in which phosphine adds to the alkyne, cyclization and alkoxide departure generate a stabilized cyclic intermediate, nucleophile capture and catalyst regeneration give the cyclopentenone, and this route is more favourable than their alternative alcohol-assisted migration route.

## 2. System and model boundary

The model is neutral, singlet PEt3 + diethyl 2-cinnamyl-2-(3-(4-nitrophenyl)prop-2-yn-1-yl)malonate (1a) + 4-fluorophenol (2a). The computational solvent boundary is fluorobenzene; the reported thermal reference is 383.15 K and relative Gibbs energies are referenced to infinitely separated reactants.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Find stationary points and conformers | PEt3, 1a, 2a and pathway structures | Gaussian 16 | ωB97XD/6-31G(d,p), neutral singlets; conformational searches, most stable conformers retained | Optimized minima and TS geometries | ev_doc_9f357a7b68a6_001546_1405b934f289 |
| 2 | Refine electronic energies | Optimized geometries | Gaussian 16 single points | ωB97XD/6-311+G(d,p), SMD fluorobenzene | Solvated electronic energies | ev_doc_9f357a7b68a6_001546_1405b934f289 |
| 3 | Add thermochemistry | Optimized geometries | Gaussian 16 frequencies | 383.15 K; ZPE and thermal corrections | Gibbs free energies | ev_doc_9f357a7b68a6_001546_1405b934f289 |
| 4 | Validate TSs and assemble profile | TSs and connected minima | Frequency/IRC and post-processing | Exactly one imaginary frequency; IRC connectivity; reference to separated reactants | ΔGrel profile | ev_doc_9f357a7b68a6_001546_1405b934f289; ev_doc_9f357a7b68a6_001552_3f7d9a656eae |

## 4. Validation and analysis protocol

The authors report one imaginary frequency for each TS and IRC confirmation. They compare pathway profiles and identify the largest barrier and thermodynamic direction. Figure S1 defines the pathway-A stationary-point sequence and SI text gives the numerical profile.

## 5. Private reference results

Pathway A relative Gibbs energies (kcal/mol), in the author sequence: TS1 18.9; TS2 8.2; 3 1.9; TS3 3.2; 6 -8.8; TS4 2.8; 7 -8.3; TS5 -0.9; 9 -24.7. The authors describe the initial step as rate determining and the overall reaction as thermodynamically favourable; pathway A is more favourable than pathway B.

## 6. Limitations and interpretation boundaries

These are single-level DFT estimates with gas-phase optimized geometries and implicit solvent single points. Conformer selection, standard-state conventions, IRC connectivity and model-chemistry sensitivity limit literal comparison to experiment. The paper calls the mechanism plausible, not uniquely proven.
