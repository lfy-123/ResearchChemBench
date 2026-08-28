# Private paper route

## 1. Scientific objective and author claim

The paper tests whether lateral sliding of an A-type antiferromagnetic Fe5GeTe2 bilayer creates two switchable ferroelectric ferrimagnetic states, and quantifies the AB↔BA switching barrier, out-of-plane polarization, and net magnetic moment. The authors claim that the AC-centered slide breaks the combined spin/real-space symmetry, reverses polarization and moment without reversing the Néel vector, and produces a triply coupled metallic state.

## 2. System and model boundary

The modeled object is a periodic Fe5GeTe2 bilayer with 10 Fe, 2 Ge and 4 Te atoms, a=b=3.969 Å and c=37.538 Å, with approximately 18 Å vacuum. AB and BA are polar stackings; AC is the nonpolar intermediate. The magnetic reference is A-type AFM: each layer is ferromagnetic and the two layers are antiparallel.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax AB, BA and AC magnetic structures | SI crystallographic coordinates | VASP spin-polarized PBE/PAW | 500 eV; 9×9×1; DFT-D3 zero damping; dipole correction; energy 10^-6 eV; force 0.01 eV/Å; no Hubbard U; A-type AFM | relaxed geometries and energies | ev_doc_1e3795905288_000263_1992bfd61962; ev_doc_1e3795905288_000264_f8ec86686283; ev_doc_1e3795905288_000269_a490845f0976; ev_doc_f82f5ace4520_000018_2aff8b9e5bad; ev_doc_f82f5ace4520_000027_2378aa851ace |
| 2 | Determine switching path | relaxed AB and BA, AC-centered slide | VASP CL-NEB | climbing-image nudged elastic band | barrier per unit cell | ev_doc_1e3795905288_000102_5ec142204817; ev_doc_f82f5ace4520_000006_ |
| 3 | Compute polarization | relaxed polar structures | Berry-phase/electrostatic dipole evaluation in VASP | 15×15×1 for polarization; out-of-plane component | Pz in pC/m | ev_doc_1e3795905288_000111_726f98990016; ev_doc_1e3795905288_000265_777541da52bb; ev_doc_1e3795905288_000266_7ad349558146 |
| 4 | Compute ferrimagnetic moment | relaxed AB and BA | spin-polarized total/local moments | integrate spin DOS / sum moments per cell | net moment and sign reversal | ev_doc_1e3795905288_000126_17bbcd6ffcbf; ev_doc_b9dfdc04b808_000099_f901b094a840; ev_doc_b9dfdc04b808_000100_ac4637c3bfe4 |

## 4. Validation and analysis protocol

The paper compares competing FM and AFM orderings and reports AFM1/A-type AFM as favored for AB, BA and AC. It checks the AB/BA degeneracy and opposite signs of Pz and M, and uses the AC stacking as the low-energy switching intermediate. The authors also report denser k-point convergence for polarization and magnetic anisotropy, but transport calculations are outside this benchmark.

## 5. Private reference results

The published targets are: AB↔BA barrier 15.4 meV per unit cell; AB polarization magnitude 0.087 pC/m (opposite sign in BA); AB/BA net moment magnitude 0.19 μB per unit cell with opposite signs; AC net moment approximately zero. The SI gives AB local-moment sum -0.1943 μB, BA +0.1943 μB, and AC 0.

## 6. Limitations and interpretation boundaries

These are reference DFT results, not experimental observables. Metallic polarization is reported through the paper's classical dipole convention. Agreement is assessed with method-aware tolerances because independent pseudopotentials, relaxation thresholds, NEB images and polarization branch choices can shift values. The task does not score transport, Curie temperature, or discovery of other stackings.
