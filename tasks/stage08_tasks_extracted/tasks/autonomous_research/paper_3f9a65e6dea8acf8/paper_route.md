# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical calculations to characterize the electronic structure and global
reactivity of the synthesized 1,3,4-oxadiazole–1,2,3-triazole hybrids. For compound 10f, the
authors claim that its frontier-orbital descriptors identify it as especially soft/reactive and a
strong electron acceptor within the studied series.

## 2. System and model boundary

The target is compound 10f, 2-((5-(1-(3,4-dichlorophenyl)-5-methyl-1H-1,2,3-triazol-4-yl)-
1,3,4-oxadiazol-2-yl)thio)-N-(4-methoxyphenyl)acetamide, formula C20H16Cl2N6O3S. The
calculation concerns the isolated neutral molecule in its singlet electronic state. The reported
workflow uses gas-phase optimization/frequencies followed by a water-solvated single point; it
does not model protein binding, explicit solvent molecules, temperature-dependent populations,
or experimental biological activity.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate a stationary-point geometry | ChemBioDraw-derived 3-D structure of each synthesized compound | Gaussian 09 Rev. D.01, B3LYP | Gas phase; 6-31G(d); neutral, singlet; UltraFine grid (99 radial shells, 590 angular points); all structural parameters relaxed | Optimized geometry | ev_doc_765b85d96ff9_000329_12c056119761; ev_doc_765b85d96ff9_000340_0d24f9656630 |
| 2 | Verify the stationary point is a minimum | Optimized geometry from step 1 | Gaussian 09 vibrational frequency analysis | Same B3LYP/6-31G(d)/UltraFine setup | No imaginary frequencies | ev_doc_765b85d96ff9_000329_12c056119761; ev_doc_765b85d96ff9_000340_0d24f9656630 |
| 3 | Obtain frontier orbital energies in a biological-environment approximation | Step-1 geometry | Gaussian 09 single point | B3LYP/6-311+G(d,p), SMD water; neutral, singlet | HOMO and LUMO energies | ev_doc_765b85d96ff9_000337_76d1efce66d1; ev_doc_765b85d96ff9_000338_73dcd4e71949; ev_doc_765b85d96ff9_000339_efb2f2144aa1; ev_doc_765b85d96ff9_000340_0d24f9656630 |
| 4 | Calculate global descriptors | HOMO and LUMO energies | Algebraic post-processing using the paper's conceptual-DFT relations | ΔE = ELUMO − EHOMO; I = −EHOMO; A = −ELUMO; χ=(I+A)/2; η=(I−A)/2; s=1/(2η); μ=−χ; ω=μ²/(2η) | Gap, hardness, softness, electronegativity, chemical potential, electrophilicity and related indices | ev_doc_765b85d96ff9_000245_5d3f116c509a; ev_doc_765b85d96ff9_000254_8434c1991829; ev_doc_765b85d96ff9_000265_915871a75949 |

## 4. Validation and analysis protocol

The geometry is accepted as a minimum only if the frequency calculation contains no imaginary
frequencies. HOMO/LUMO identities must be taken from the same specified single-point wavefunction,
with units and sign convention stated. The reported descriptors must be recomputed from the
submitted orbital energies (or a reproducibly documented equivalent) and checked for internal
formula consistency. Interpretation is limited to comparison of electronic softness/reactivity;
it is not evidence of biological potency or binding affinity.

## 5. Private reference results

Table 6 reports for 10f: HOMO −5.63 eV, LUMO −2.34 eV, gap 3.29 eV, hardness 1.64 eV,
softness 0.60 eV−1, electronegativity 3.98 eV, chemical potential −3.98 eV, electrophilicity
4.82 eV, ΔNmax 2.42 eV, donating power 14.05 eV, accepting power 6.07 eV, and Δω −7.97 eV.
The paper describes the 10f gap/hardness/electrophilicity combination as indicating particularly
high reactivity/softness and electron-accepting ability. These values are private evaluator
references.

## 6. Limitations and interpretation boundaries

The source does not provide an input coordinate file or an atom-mapped structure. The public task
therefore supplies the unambiguous systematic identity and formula and requires the researcher to
document how a 3-D starting geometry was generated. Different conformer searches, software,
numerical settings, and orbital conventions can shift descriptors. No exact reproduction claim is
made for methods other than the reported route, and descriptor agreement must be interpreted within
the declared computational protocol and convergence/validation evidence.
