# Private paper route

## 1. Scientific objective and author claim

The authors use electronic-structure calculations to compare folded (“close”) and unfolded (“open”) conformers of the E and Z forms of AB-mTTA-(1,3)Ph, with and without a chloride guest. Their claim is that open and folded conformers can be close in free energy, providing a conformational explanation for the similar chloride-binding strengths of the E and Z hosts.

## 2. System and model boundary

The modeled systems are the E- and Z-AB-mTTA-(1,3)Ph host and its chloride complex. The SI supplies Cartesian coordinates for close/open host and chloride-complex structures. The reported comparison is in acetone using PCM, with and without Grimme D3(BJ), and thermochemistry at approximately room temperature.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize candidate host and chloride-complex geometries | SI Cartesian structures for E/Z close/open forms | Gaussian 16 Rev. B.01; B3LYP | 6-31G*; D3(BJ); PCM acetone; UFF cavity radii; standard convergence | Relaxed structures and electronic energies | ev_doc_fefeaea453c5_000099_b4428ff0d59b; ev_doc_fefeaea453c5_000100_8089ae62aaa4; ev_doc_761758def1c3_000008_796b9348c627; ev_doc_761758def1c3_000009_c25022a54ecd |
| 2 | Validate stationary points and obtain thermochemistry | Optimized structures | Harmonic frequency calculation in Gaussian 16 | ZPE and thermal corrections; T=298.15 K (relative tables tabulated at 300 K) | Gibbs free energies; minima require no imaginary frequencies | ev_doc_fefeaea453c5_000101_21cf6c4e1c4a; ev_doc_fefeaea453c5_000102_897e22e6c4ed |
| 3 | Compare conformers | Relative energies of E/Z close/open chloride complexes | Relative-energy analysis | PCM and PCM+D3(BJ), acetone; energies in eV | Relative free-energy ordering and open/close separations | ev_doc_fefeaea453c5_000108_5c8fe830c772 |

## 4. Validation and analysis protocol

The authors optimized geometries, used harmonic frequencies for Gibbs corrections, and compared relative energies among close/open conformers. The chloride binding-energy workflow additionally uses relaxed host structures and counterpoise correction for BSSE. The conformer interpretation is limited by implicit solvation, dispersion-model dependence, and neglected conformational entropy beyond the harmonic treatment.

## 5. Private reference results

The hidden reference is Table S6: relative free DFT energies of chloride complexes in eV at T=300 K with acetone. For the E complex, the PCM+D3(BJ) close structure is the reference zero and the open structure is 0.9970 eV above it; the PCM column instead places open at zero and close at 0.0922 eV. The Z-complex close and open values are also tabulated (PCM: 0.7247 and 0.5971 eV; PCM+D3(BJ): 0.6518 and 1.4534 eV). These values are private and are not public task inputs.

## 6. Limitations and interpretation boundaries

Relative conformer energies depend strongly on dispersion and solvent treatment. A successful reproduction should report the actual method, convergence, frequency evidence, and any alternative conformers found; disagreement across defensible methods is a limitation, not evidence of a new experimental mechanism. The paper's qualitative “near-degeneracy” statement should not be generalized beyond the specified host, guest, solvent model, and conformer set.
