# Private paper route

## 1. Scientific objective and author claim

The authors test whether Li/F co-substitution and subsequent Si4+ substitution in Fe3+-activated ZnAl2O4 modify local coordination and distort the Fe3+-site environment, providing a structural basis for relaxing forbidden Fe3+ transitions and enhancing NIR emission.

## 2. System and model boundary

The computational host is normal-spinel ZnAl2O4, with Fe3+ activation, represented by three 56-atom models: undoped ZAO (UC-1), one-Li/one-F co-doped ZAO (UC-2), and UC-2 further doped with one Si (UC-3). The paper states that the lowest-DFT-total-energy site occupation was selected. Reported local observables concern the atom at the substituted position.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Establish host and substituted models | ZnAl2O4 starting structure; one Li/one F, then one Si | DFT model construction; structures visualized in VESTA | 56 atoms per model; lowest-total-energy occupation selected | UC-1, UC-2, UC-3 | ev_doc_02434818493c_000953_04f8f030c442; ev_doc_a6eb284cc0e7_000087_d20e8b3ba8a2 |
| 2 | Relax atomic structures | Each model | VASP DFT structural relaxation | 500 eV cutoff; Gamma-centered 4x4x4 k mesh; SCF 1e-5 eV; conjugate-gradient relaxation; forces below 0.03 eV/A | relaxed structures | ev_doc_02434818493c_000214_10b875e54570 through ev_doc_02434818493c_000219_e992672ea397 |
| 3 | Extract local geometry | relaxed substituted-site environments | bond and angle measurement; VESTA visualization | substituted-site bond lengths and angles | Table S7 observables | ev_doc_02434818493c_000953_04f8f030c442; ev_doc_a6eb284cc0e7_000204_b5d085de285a |
| 4 | Interpret distortion | extracted geometry | comparison across UC-1 to UC-3 | shorter Li-O and Si-O; lengthened Al-F; altered O-Li-O and O-Al-F | structural rationale for reduced local symmetry | ev_doc_02434818493c_000961_27062a8838cb |

## 4. Validation and analysis protocol

The paper compares the substituted-site bond lengths and angles across the three models. It interprets shorter Li-O and Si-O distances, longer Al-F relative to Al-O, and changed O-Li-O/O-Al-F angles as lattice distortion and reduced local symmetry. The authors also relate this to increased Fe3+ occupancy in distorted octahedral sites and relaxed forbidden transitions. The reported calculation details do not identify functional, PAW dataset, spin setting, or Hubbard U; these are therefore not treated as mandatory reproduction parameters in the public task.

## 5. Private reference results

Table S7 gives: UC-1 Zn-O 1.98 A and O-Zn-O 109.47 degrees; UC-1 Al-O 1.91 A and O-Al-O 97.22 degrees; UC-2 Li-O 1.93 A and O-Li-O 113.93 degrees; UC-2 Al-F 2.09 A and O-Al-F 92.83 degrees; UC-3 Si-O 1.86 A and O-Si-O 114.14 degrees; UC-3 Li-O 1.94 A and O-Li-O 114.18 degrees; UC-3 Al-F 2.15 A and O-Al-F 89.52 degrees.

## 6. Limitations and interpretation boundaries

The source does not provide a ready-to-use coordinate file or all electronic-structure settings. Site selection and conformational/model sensitivity must be documented by the investigator. Geometry agreement alone supports the reported local-distortion interpretation; it does not prove optical intensities, defect concentrations, or experimental performance.
