# Private paper route

## 1. Scientific objective and author claim

The paper studies whether substitution changes the geometry and electronic structure of polysubstituted hydrazones. For representative HPY 10a, the authors claim that the central hydrazone-linked pyrrole/pyridine framework is nearly coplanar while the aryl substituents are twisted out of that plane; this geometry is used to explain weak substituent effects on solution photophysics.

## 2. System and model boundary

The target is neutral, closed-shell HPY 10a in dichloromethane continuum. The molecule is ethyl (E)-6-(2-((3-(ethoxycarbonyl)-4,5-diphenyl-1H-pyrrol-2-yl)methylene)hydrazineyl)-5-isocyano-2-methyl-4-phenylnicotinate. The reported computational object is its optimized ground-state geometry, harmonic frequencies, three substituent dihedrals, and frontier orbital energies.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Find low-energy structure | HPY 10a molecular structure | ORCA GOAT | Global optimizer; solvent model as used for subsequent calculations | Candidate minimum geometry | ev_doc_8f60930f2164_000259_6d67b72e6174 |
| 2 | Optimize ground-state geometry | GOAT geometry | ORCA 6.0 DFT | B3LYP-D3BJ/def2-TZVP with def2/J and def2-TZVP/C; CPCM dichloromethane, Gaussian charges, vdW cavity | Optimized neutral singlet geometry | ev_doc_8f60930f2164_000259_6d67b72e6174 |
| 3 | Verify a true minimum | Optimized geometry | ORCA analytical frequencies | Same model boundary | No imaginary modes | ev_doc_8f60930f2164_000259_6d67b72e6174 |
| 4 | Extract structural/electronic observables | Frequency-validated geometry | Geometry/FMO analysis; Multiwfn 3.8 used for excited-state/FMO analysis | Dihedrals θ1–θ3 defined in SI Table S4; HOMO/LUMO in eV | θ1=35°, θ2=61°, θ3=60°; HOMO=-5.75 eV; LUMO=-1.97 eV | ev_doc_2304218d8c89_000309_b69755d8e427 |

## 4. Validation and analysis protocol

The authors optimized all compounds and computed analytical frequencies; absence of imaginary modes was taken as confirmation of true minima. They compared the resulting dihedrals across HPY/TBPY series. The main text interprets the central hydrazone and pyrrole/pyridine segments as coplanar, with substituent-dependent but generally substantial twisting. FMO distributions were used to support a push-pull/charge-transfer interpretation.

## 5. Private reference results

For 10a, SI Table S4 reports θ1=35°, θ2=61°, θ3=60°, HOMO=-5.75 eV and LUMO=-1.97 eV. The source says the central hydrazone and azine segments are completely coplanar and that substituents are out of plane; the 10a first transitions have holes mainly on pyrrole and electrons on pyridine (main-text IFCT discussion).

## 6. Limitations and interpretation boundaries

The source does not provide Cartesian coordinates, atom numbering diagrams for every θ label, or a uniquely machine-readable public structure file. The public task therefore uses the full systematic compound name plus formula and requires the Agent to document atom selections for θ1–θ3. Numerical comparison is to the SI's rounded degree/eV values and is not a claim of method-independent exactness. No excited-state, solvent-spectrum, or experimental-structure reproduction is scored.
