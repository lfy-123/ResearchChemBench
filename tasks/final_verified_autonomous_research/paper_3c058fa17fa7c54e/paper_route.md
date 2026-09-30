# Private paper route

## 1. Scientific objective and author claim

The paper studies whether two anthracene-based σ-bond emitters, An-σ-Ph and An-σ-DA, have singlet/triplet energetics compatible with triplet–triplet annihilation (TTA) luminescence. The authors claim that TD-DFT energetics support TTA and that the σ-bond interrupts conjugation, enabling deep-blue emission.

## 2. System and model boundary

The systems are neutral closed-shell organic molecules: An-σ-Ph (C55H34F6; SI systematic name: 10,10′-((perfluoropropane-2,2-diyl)bis(4,1-phenylene))bis(9-phenylanthracene)) and An-σ-DA (C57H35F6NO; SI systematic name: 4-(10-(4-(1,1,1,3,3,3-hexafluoro-2-(4-(10-(4-methoxyphenyl)anthracen-9-yl)phenyl)propan-2-yl)phenyl)anthracen-9-yl)benzonitrile). Charge is 0 and the ground-state multiplicity is singlet. The computational boundary is isolated-molecule electronic structure; solvent, solid-state packing and device physics are outside the calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize molecular skeleton | An-σ-Ph and An-σ-DA structures | Gaussian 16, visualized in GaussView 6.0 | B3LYP/6-31G(d,p) | Optimized geometries and orbitals | ev_doc_8bd71de2ea67_000052_7946544193e8; ev_doc_c2000e587a02_000004_142fe1c58e4b |
| 2 | Compute lowest singlet and triplet levels | optimized geometries | time-dependent DFT | same 6-31G(d,p) basis; paper describes TD calculation but does not specify all keywords | S1 and T1 energies | ev_doc_8bd71de2ea67_000056_db3ff87425b3; ev_doc_c2000e587a02_000052_7946544193e8 |
| 3 | Interpret TTA energetics | computed S1/T1 | algebraic comparison | 2T1>S1 and S1−T1>0.5 eV | TTA/TADF interpretation | ev_doc_8bd71de2ea67_000056_db3ff87425b3; ev_doc_8bd71de2ea67_000135_e623fdf5645e |

## 4. Validation and analysis protocol

The paper reports optimized structures and frontier-orbital analysis, then compares the lowest singlet/triplet energies and applies the energetic inequalities. A defensible reproduction should document charge/multiplicity, geometry convergence and stationary-point evidence, identify the states and spin treatment used, report units and extraction procedure, and perform an explicit sensitivity/uncertainty discussion for unspecified TD-DFT settings. The paper also connects the energetic test with oxygen-sensitive delayed fluorescence and transient-PL observations, but those experiments are contextual rather than computational inputs.

## 5. Private reference results

The main paper PDF p.2, Figure 2 explicitly labels An-σ-Ph S1 = 3.1457 eV, T1/T2 = 1.7347 eV and ΔEST = 1.4110 eV; An-σ-DA S1/S2 = 2.9835 eV, T1 = 1.7284 eV and ΔEST = 1.2551 eV. These figure-labelled states define the private S1/T1 reference. For Ph, 2T1−S1 = 0.3237 eV; for DA, 0.4733 eV. Both satisfy the task's two energetic criteria.

Source correction (2026-09-23): p.4 prose reverses the Ph pair as 1.7347/3.1457 after naming S1/T1. Figure 2 directly resolves that ordering error and agrees with its labelled positive ΔEST, the DA state ordering and the proposed TTA energy diagram. This is a source-backed benchmark correction, not an author-issued corrigendum. The supplied SI p.2 confirms Gaussian 16 and B3LYP/6-31G(d,p), but its p.8 UV spectrum does not independently tabulate S1/T1. The original printed prose remains recorded here; no value is inferred by enforcing a universal S1>T1 rule.

Existing independent verification gives Ph S1/T1 = 3.0533/1.7386 eV and DA = 2.8270/1.7338 eV, with explicit singlet/triplet logs. These corroborate the state ordering and energetic criteria, not exact reproduction of Figure 2. The local ground-state optimization includes D3BJ, which the supplied SI does not specify; implementation/conformer differences remain disclosed. The energetic conditions support, but do not prove, the full photophysical mechanism. All numerical references remain private.

## 6. Limitations and interpretation boundaries

The paper omits some TD-DFT implementation details (for example number of roots, solvent treatment and exact keywords), and does not provide initial coordinate files. Reproduction therefore evaluates a transparent, independently chosen implementation against source-reported values with stated uncertainty; agreement is not evidence of unique conformer or unique method. The inequalities are energetic support, not a standalone proof of the full photophysical mechanism.
