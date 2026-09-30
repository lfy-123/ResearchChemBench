# Private paper route

## 1. Scientific objective and author claim

The paper tests whether small uniaxial distortions along the interlayer direction can account for the unusually small electronic gap observed for K0.5WTe2. The author claim is that both signs of a 2% distortion reduce the calculated gap; −2% makes the material metallic and +2% produces a zero-gap semimetal, with tensile strain introducing Te-derived states at the Fermi energy.

## 2. System and model boundary

The system is K0.5WTe2 represented by the P21/m crystallographic model (formula-cell contents K2W4Te8, Z=2; cell a=7.29743 Å, b=17.2594 Å, c=7.24144 Å, beta=119.1069°). The strain is applied to the b lattice vector, identified by the paper as the interlayer direction. The electronic observable is the fundamental band-gap character and band dispersion near the Fermi level.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize the crystallographic model | K0.5WTe2 P21/m structure | DFT in ABINIT | PAW; PBE; vdW-DFT-D3; plane-wave cutoff 26 Ha; 4x2x4 k mesh; Methfessel–Paxton occupations | relaxed geometry | ev_doc_3832331917ee_000564_2a949767d9c8; ev_doc_3832331917ee_000570_67aa9d48e963; ev_doc_3832331917ee_000571_a8b2feed6437 |
| 2 | Generate distorted cells | relaxed geometry | scale b lattice vector | −2% and +2% uniaxial strain along b; internal fractional coordinates retained for the illustrated local distortion | compressed and tensile structures | ev_doc_3832331917ee_000435_9bd55664ec91; ev_doc_3832331917ee_000454_cc1ca0f85f50 |
| 3 | Determine electronic structure | each strained structure | self-consistent DFT and band-structure calculation in ABINIT | same K model chemistry and 4x2x4 sampling; literature special-point path | band plots and gap character | ev_doc_3832331917ee_000564_2a949767d9c8; ev_doc_3832331917ee_000570_67aa9d48e963; ev_doc_3832331917ee_000571_a8b2feed6437 |

## 4. Validation and analysis protocol

The relaxed structure was used before electronic calculations. The paper compared the unstrained, −2%, and +2% cases and inspected bands close to the Fermi level, including their orbital character. It interpreted a Fermi-level crossing as metallic, a touching with no finite separation as a zero-gap semimetal, and a finite indirect separation as semiconducting. The strain comparison was used as a structural-distortion explanation for disorder-sensitive small gaps, not as a prediction of a unique experimental strain state.

## 5. Private reference results

The unstrained K0.5WTe2 calculation is semiconducting with an indirect DFT gap in the paper's reported 0.35–0.4 eV range for the intercalated compounds. At −2% b-axis strain the bands cross the Fermi level and the material is metallic. At +2% b-axis strain the gap closes to a zero-gap semimetal; the paper attributes the newly appearing near-Fermi unoccupied states to Te orbitals and reports a more dramatic change in the highest-occupied-band curvature than for compression. No exact strained numerical gap is stated in the text.

## 6. Limitations and interpretation boundaries

The paper does not provide tabulated numerical strained gaps, so the fair hidden target is qualitative classification and source-supported band/orbital interpretation. DFT gap magnitudes are method-dependent and the paper itself notes the usual gap error. The crystallographic coordinates are experimental and the calculated relaxed geometry is not reproduced as a hidden structure; submissions must report their own relaxation and convergence evidence.
