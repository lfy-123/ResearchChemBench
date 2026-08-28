# Private paper route

## 1. Scientific objective and author claim

The paper characterizes 1-phenyl-5-(m-tolyl)-1H-tetrazole and claims that its DFT electronic structure indicates comparatively high kinetic stability and limited chemical reactivity. The computationally testable core is the optimized isolated-molecule electronic structure, including the frontier-orbital gap and global conceptual-DFT descriptors.

## 2. System and model boundary

The system is neutral singlet C14H12N4, treated as one isolated molecule. The experimental comparison is to the molecular geometry from the SCXRD structure deposited as CCDC 2415253; the paper reports monoclinic P21/n crystallization and an XRD/DFT structural-overlay RMSD of 0.366 Å. The scored electronic quantities are properties of the optimized gas-phase molecular model, not crystal packing, solvent, protein binding, or biological efficacy.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize molecular geometry | Title compound geometry | Gaussian09, DFT | B3LYP/6-311++G(d,p); SCF RMS density 10^-6 a.u., energy 10^-8 Hartree; max force 1.5×10^-5 a.u., RMS force 1.0×10^-5 a.u. | Optimized structure | ev_doc_86774f5f3b37_000051_86bfb0db9393; ev_doc_86774f5f3b37_000052_5cd9a3d853b0; ev_doc_86774f5f3b37_000053_b5e056404b8a; ev_doc_86774f5f3b37_000054_05a524b02929; ev_doc_86774f5f3b37_000055_7e544eef5134; ev_doc_86774f5f3b37_000056_fb47c8399dcc; ev_doc_86774f5f3b37_000057_4f29a3bf5c0d; ev_doc_86774f5f3b37_000058_2114839a8e37; ev_doc_86774f5f3b37_000059_cf94f537df9f; ev_doc_86774f5f3b37_000060_0d84c03a20dc |
| 2 | Verify a minimum and obtain vibrational data | Optimized geometry | Gaussian09 frequency calculation at the same level | Require no imaginary frequencies | Validated minimum | ev_doc_86774f5f3b37_000061_2aef0a04cb10 |
| 3 | Extract frontier orbitals and conceptual-DFT descriptors | Validated minimum and orbital energies | Gaussian09 output analysis | ΔE, I, electron affinity, μ, χ, η, softness and electrophilicity computed from frontier orbital energies | Table of descriptors | ev_doc_86774f5f3b37_000132_e5e0947bd1dd; ev_doc_86774f5f3b37_000143_11111bda522f; ev_doc_86774f5f3b37_000144_30ea0f6fb093 |

## 4. Validation and analysis protocol

The authors checked that optimized structures were minima by frequency analysis and compared the optimized and XRD geometries by a structural overlay. They interpreted the large frontier-orbital gap as evidence for kinetic stability/limited reactivity and described the molecule as hard. The paper also reports MEP and QTAIM analyses, but those are outside this benchmark's scored core.

## 5. Private reference results

Table 7 reports EHOMO −1.707 eV, ELUMO −6.939 eV, ΔE 5.232 eV, ionization potential 1.707 eV, electron affinity 6.939 eV, chemical potential −4.323 eV, electronegativity 4.323 eV, hardness 2.616 eV, softness 0.382 eV−1, and electrophilicity 3.572 eV. The text rounds the gap to 5.23 eV and reports an XRD/DFT RMSD of 0.366 Å. These values are hidden from agents.

## 6. Limitations and interpretation boundaries

The source does not provide a machine-readable deposited CIF in the supplied snapshot, so the released task uses a connectivity-defined isolated molecule and asks agents to generate/validate their own geometry. Frontier-orbital values are method- and conformer-dependent; the paper's values are a single reported calculation and should not be interpreted as experimental observables or proof of biological activity. The source contains an internal inconsistency in the crystallographic CCDC number in one table versus the methods text; this benchmark does not depend on retrieving that record.
