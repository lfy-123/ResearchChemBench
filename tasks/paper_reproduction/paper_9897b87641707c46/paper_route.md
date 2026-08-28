# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to explain why the bpy-UiO-FeH2 catalyst gives linear (anti-Markovnikov) hydroboration of styrene with HBpin, and to identify the turnover-limiting elementary step. The proposed cycle is dissociative loss of two THF ligands from octahedral (bpy)FeH2(THF)2, styrene coordination, competing 1,2/2,1 insertion into Fe–H, and sigma-bond metathesis with HBpin.

## 2. System and model boundary

The calculated model is a truncated molecular active site: a simplified 2,2'-bipyridyl ligand bound to Fe(II), with hydrides and, for the resting species, two axial THF ligands. Styrene and HBpin are explicit reactants; the UiO framework is not represented. The authors report unrestricted DFT, a quintet Fe(II) state as lowest among tested spin states, implicit toluene, and 333.15 K thermochemistry.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize stationary points | truncated Fe/bpy, styrene, HBpin and cycle structures | Gaussian 16, unrestricted B3LYP | GD3BJ dispersion; def2-SVP; IEFPCM/toluene; neutral, quintet | optimized minima and TS candidates | ev_doc_027b8abd2a51_000422_f0e313903ba2; ev_doc_027b8abd2a51_000433_87b23f5bdd1e |
| 2 | Classify stationary points | optimized structures | same level frequency calculations | minima have zero imaginary frequencies; TS have one imaginary frequency along the reaction coordinate | validated Hessians and thermal corrections | ev_doc_027b8abd2a51_000422_f0e313903ba2 |
| 3 | Refine electronic energies | optimized structures | single-point DFT | def2-TZVP refinement with IEFPCM/toluene | refined energies | ev_doc_027b8abd2a51_000422_f0e313903ba2 |
| 4 | Assemble free-energy profile | energies and thermal corrections | authors' thermochemical assembly | 333.15 K; relative to the dissociated tetrahedral FeH2 reference | ΔG for INT-1, insertion TS/INT, and metathesis TS/product branches | ev_doc_4c7bdca3a157_000205_4caddbdae68e |
| 5 | Interpret selectivity and rate control | profile for linear and branched branches | barrier and intermediate comparison | compare competing insertion and metathesis barriers | anti-Markovnikov branch and turnover-limiting step | ev_doc_4c7bdca3a157_000212_110d8e934cee; ev_doc_4c7bdca3a157_000218_5cb680c19d1d; ev_doc_4c7bdca3a157_000221_9f5e745f6092 |

## 4. Validation and analysis protocol

The paper validates every minimum by absence of imaginary frequencies and every transition state by exactly one imaginary frequency corresponding to the bond-making/bond-breaking event. The reported profile compares styrene coordination, both regioisomeric insertion branches, and the two subsequent HBpin sigma-bond-metathesis branches. Interpretation is restricted to the truncated molecular model and the reported solvent/temperature treatment; it is not a direct simulation of pore diffusion or the full MOF.

## 5. Private reference results

The paper reports ΔG(INT-1) = +14.7 kcal/mol, linear 1,2-insertion ΔG = −8.7 kcal/mol through an 8.4 kcal/mol barrier, branched 2,1-insertion ΔG = −8.0 kcal/mol through a 10.6 kcal/mol barrier, linear-branch metathesis barrier = 20.7 kcal/mol, and branched-branch metathesis barrier = 25.3 kcal/mol. It assigns the linear branch to the anti-Markovnikov product and identifies metathesis on the linear branch as turnover-limiting.

## 6. Limitations and interpretation boundaries

The SI gives a simplified bipyridyl model and stationary-point coordinate tables, but the normalized tables contain layout damage; the released task therefore supplies an unambiguous molecular definition rather than reproducing damaged result-bearing coordinates. Numerical agreement is judged against the paper's reported free energies, while alternative defensible computational protocols must report their method and uncertainty. The result is a model-level mechanistic test, not proof that every pore environment has identical energetics.
