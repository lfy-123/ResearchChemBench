# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to explain ammonia oxidation by Ru-bda-Py. Its claim is that the rate-determining event in the bda catalyst is cleavage of the N–O interaction in singlet ^1TS3_bda, before diffusion-controlled NH3 attack; the reported Gibbs barrier is +6.2 kcal/mol.

## 2. System and model boundary

The system is the neutral singlet Ru-bda-Py ammonia-oxidation model in acetonitrile, with bda = 2,2′-bipyridine-6,6′-dicarboxylate and pyridine axial ligands. The evaluated pair is the singlet bda intermediate labelled 5_bda/S_bda and singlet TS3_bda in the SI coordinate table.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize stationary points | SI coordinate blocks for 5_bda and TS3_bda | Gaussian 16, B3LYP-D3(BJ) | SDD on Ru; 6-31G(d,p) on S,C,N,O,H; singlet, neutral | optimized geometries | ev_doc_d29674c1bddc_000540_d8dcc822e989; ev_doc_d29674c1bddc_000817_76da90988e7c |
| 2 | Classify stationary points and obtain thermal terms | optimized geometries | harmonic frequencies at same level | 298.15 K | minimum/TS classification and Gibbs corrections | ev_doc_d29674c1bddc_000540_d8dcc822e989 |
| 3 | Refine electronic energies | optimized geometries | B3LYP-D3(BJ)/def2-TZVP with SMD | acetonitrile | solvent electronic energies | ev_doc_d29674c1bddc_000540_d8dcc822e989 |
| 4 | Assemble electrochemical free-energy profile | frequency corrections and refined energies | authors’ thermochemical/electrochemical convention | 0.5 V vs Fc+/0; pH 15.1 | ΔG‡ for N–O cleavage | ev_doc_d29674c1bddc_000794_4ec8933c63c9; ev_doc_7419176c5781_000765_81f1905507d0 |

## 4. Validation and analysis protocol

The TS must have exactly one imaginary frequency and its displacement must involve breaking the N–O interaction of the bda intermediate. The reference free-energy profile is interpreted at 298.15 K, 0.5 V vs Fc+/0 and pH 15.1 in acetonitrile. The reported event is the rate-determining N–O cleavage; subsequent NH3 attack is described as diffusion-controlled.

## 5. Private reference results

The paper reports a +6.2 kcal/mol Gibbs free-energy barrier for N–O cleavage through ^1TS3_bda. The SI depicts this profile in Figure S55 and the structures in Table S21.

## 6. Limitations and interpretation boundaries

The supplied coordinates are finite starting geometries, not a guarantee that an independently optimized calculation reproduces the paper geometry. Solvent, thermal, spin, convergence and conformer choices can shift energies. Scoring therefore separates process validation from the final barrier and requires reporting the actual computational choices and failures.
