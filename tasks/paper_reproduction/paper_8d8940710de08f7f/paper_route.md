# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to characterize the neutral conformational landscape of 4-amino-N-(naphthalen-2-yl)benzenesulfonamide (SNaft) and 4-amino-N-(anthracen-2-yl)benzenesulfonamide (SAntr). Its qualitative claim is that two V-like minima and one Z-like minimum occur along the C–S–N–C torsion, with the V-like structures favored and stabilized principally by intramolecular C–H···O interactions.

## 2. System and model boundary

The systems are neutral, singlet monomers. The three reported conformational minima are labelled V(+), V(−), and Z according to the C–S–N–C torsion. The SI reports equilibrium Cartesian geometries and Gibbs/electronic energies in Hartree for these systems; the main article discusses the torsional scans and structural interpretation. Solution context in the article is methanol for the relevant electronic-density analyses; Table S8 itself states that its geometries and energies were calculated in vacuo.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax C–S–N–C torsional scans and locate minima | SNaft and SAntr neutral monomers and torsion angle | ORCA 6.0.1 DFT | R2SCAN/def2-TZVP, def2/J, split-RI-J; C-PCM solvent when solvent was modelled | Candidate minimum structures | ev_doc_e60408ceaf14_000119_a2f28bf810e3 |
| 2 | Optimize stationary points | Scan minima | ORCA 6.0.1 | Same DFT level; neutral singlets | Equilibrium structures and energies | ev_doc_e60408ceaf14_000119_a2f28bf810e3 |
| 3 | Confirm minima | Optimized structures | ORCA vibrational analysis | Frequency analysis after every optimization | No imaginary frequencies for true minima | ev_doc_e60408ceaf14_000119_a2f28bf810e3 |
| 4 | Compare conformers and analyze interactions | Equilibrium structures/wavefunctions | DFT/QTAIM | ωB97M-V wavefunctions in methanol for density topology; QTAIM/Espinosa analysis | Relative conformer energies and C–H···O interaction descriptors | ev_doc_e60408ceaf14_000119_a2f28bf810e3; ev_doc_7b7892dba953_000027_67ad70a937ff |

## 4. Validation and analysis protocol

The authors identify three minima near torsions of approximately +50°, −50°, and 180°. Frequencies are used to distinguish minima from saddle points. Relative Gibbs energies are obtained by subtracting the lowest conformer for each molecule. The paper interprets the lower energy of V-like structures alongside QTAIM descriptors and Espinosa hydrogen-bond energies for the neutral V conformers.

## 5. Private reference results

Table S8 reports (Hartree) G(SNaft-V+) = −1275.93267041, G(SNaft-V−) = −1275.93248031, and G(SNaft-Z) = −1275.92853910; G(SAntr-V+) = −1429.49708929, G(SAntr-V−) = −1429.49781882, and G(SAntr-Z) = −1429.49376162. Relative values using the lowest conformer as zero are approximately SNaft: V+ 0.000, V− 0.119, Z 2.592 kcal/mol; SAntr: V− 0.000, V+ 0.458, Z 2.546 kcal/mol. The article reports neutral Z–V differences of 3.05 and 3.03 kcal/mol from the relaxed scans. Table S9 reports E_HB values 2.52 and 2.46 kcal/mol for SNaft V(+)/V(−), and 2.42 and 2.48 kcal/mol for SAntr V(+)/V(−), with H/rho 0.17 and |V|/G 0.79.

## 6. Limitations and interpretation boundaries

Table S8 is explicitly in vacuo, whereas parts of the article use continuum solvent. Relative energies depend on the chosen electronic-structure model, thermal convention, conformer starting structures, and whether additional low-energy minima are found. The benchmark therefore scores reproducibility against the reported neutral three-state set and requires the agent to state model and convergence choices; it does not treat the paper values as universal thermochemical truth.

## 7. Private source reconciliation (2026-09-16)

The Table S8 caption says in vacuo, but paired single points on all six literal SI coordinates reproduce its absolute electronic energies with CPCM(methanol) to within 4e-8 Hartree; the corresponding vacuum residuals are +0.028645 to +0.031931 Hartree. Together with the CPCM optimization route in main-text Section 2.8, this strongly supports a mislabeled environment in the SI caption. This is a documented computational inference, not an author-issued correction. Both environments and every residual are retained in the private verification record; matching single-point energies does not validate minima or Gibbs corrections. The public task does not impose vacuum or a new solvent constraint.

Connectivity-based signed C-S-N-C evaluation of the literal SNaft-Z source geometry gives -173.021759764 degrees. The former positive-only Z input region excluded the source itself. The same near-trans state identity is now represented by the union [-180,-140] and [140,180], preserving signed outputs and keeping the two V regions separate. No energy target, scoring rule, tolerance, molecular identity or scientific goal was changed.

Evidence and before/after hashes: `runs/hold_verification/group_5/santr_closure_20260916/paper_8d8940710de08f7f/source_review/source_boundary_correction.json`; paired calculations and original geometries are indexed in that run's `report/results.json`. These private verification artifacts must not be supplied to the evaluated agent.
