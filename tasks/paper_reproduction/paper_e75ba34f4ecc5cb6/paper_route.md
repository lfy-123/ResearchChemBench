# Private paper route

## 1. Scientific objective and author claim

The paper tests whether asymmetric alkylation of ether solvents changes K+-solvent interaction strength and electronic polarity, supporting a fluorine-free electrolyte design for potassium-ion batteries. The qualitative claim is that steric substitution reorganizes coordination and can weaken K+-solvent binding.

## 2. System and model boundary

The quantum-chemical systems are isolated neutral ether molecules and their singly coordinated K+ complexes: DEGDME, DPGDME, and two DPGMPE coordination conformations (DPGMPE-1 and DPGMPE-2). Molecules are singlet neutral states; K+ and each complex are singlets with charge +1. The reported binding energy is the electronic quantity Eb = Ecomplex − Esolvent − EK+ and is interpreted primarily as electrostatic ion–dipole interaction. No solvent continuum or thermal correction is reported.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize isolated solvent geometries representing coordination conformations | DEGDME, DPGDME, DPGMPE-1, DPGMPE-2 structures | Gaussian 16, B3LYP/6-31+G(d) | Full geometry optimization; neutral singlet | Optimized minima | ev_doc_c31aba2b707f_000078_f991d290051d, ev_doc_c31aba2b707f_000079_e151f4ce2ef7, ev_doc_c31aba2b707f_000080_432a1d7e9f11 |
| 2 | Optimize K+-solvent complexes | K+ plus each solvent | Gaussian 16, B3LYP/6-31+G(d) | Overall charge +1, singlet | Optimized binding configurations | ev_doc_25571081f510_000048_8e5a53be41a3, ev_doc_c31aba2b707f_000078_f991d290051d |
| 3 | Obtain consistent electronic energies and wavefunctions | Optimized complexes and isolated components | B3LYP/6-311++G(d,p) single points | Same geometries; component energies used in subtraction | Ecomplex, Esolvent, EK+ and wavefunctions | ev_doc_c31aba2b707f_000081_6aa01e939ca7, ev_doc_c31aba2b707f_000082_585a6bbae0d1, ev_doc_c31aba2b707f_000083_ca7322787595 |
| 4 | Calculate interaction and polarity observables | Single-point energies and wavefunctions | Binding-energy subtraction; Multiwfn analysis | Eb = Ecomplex − Esolvent − EK+; dipole from electronic structure | Eb and dipole moment | ev_doc_c31aba2b707f_000084_0ce4e7c06bec, ev_doc_c31aba2b707f_000088_1b075a709d5f, ev_doc_c31aba2b707f_000089_e38c8cde97e9, ev_doc_c31aba2b707f_000090_cd17ea90ad5e |

## 4. Validation and analysis protocol

The paper compares the four named configurations, uses optimized binding configurations (SI Fig. S1), applies the energy subtraction consistently, and interprets the sign and relative magnitude of Eb together with dipole moment and ESP. The main text reports the binding-energy sequence for all four configurations and says DPGMPE-2 has a substantially increased dipole moment despite weaker binding.

## 5. Private reference results

Binding energies reported in the main text are DEGDME −1.25 eV, DPGDME −1.36 eV, DPGMPE-1 −1.67 eV, and DPGMPE-2 −0.46 eV. The source reports a substantial dipole increase for DPGMPE-2 but the exact dipole values are graphical and are not used as scored numeric references in this package. The qualitative coordination interpretation is that DPGMPE-2 is sterically reconstructed and binds more weakly.

## 6. Limitations and interpretation boundaries

The source does not publish Cartesian starting coordinates or exact dipole numbers in the normalized text. DPGMPE has unspecified stereochemical composition and is treated here by connectivity and conformational identity, without stereochemical scoring. The benchmark therefore scores reproducible binding-energy statements and process/interpretation evidence, while requiring dipoles to be reported with method and units but treating them as an independently investigated observable rather than a hidden exact target.
