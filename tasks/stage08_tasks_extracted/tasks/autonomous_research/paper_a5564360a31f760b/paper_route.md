# Private paper route

## 1. Scientific objective and author claim

The paper uses calculations of the S1-to-S0 reorganization energy (λ), RMSD between relaxed excited- and ground-state geometries, and Huang–Rhys (HR) factors to explain the different fluorescence widths, Stokes shifts, and non-radiative rates of B←N-embedded isomers. The author claim is that the pyrazine-derived, para-oriented double-B←N compound p-2BN has stronger intramolecular charge transfer and a more rigid/conformationally stable structure than the pyrimidine-derived meta-oriented isomer m-2BN, producing smaller λ and RMSD; the dominant displacement patterns differ between backbone and side phenyl groups.

## 2. System and model boundary

The computational models replace the experimental octyl side chains by methyl groups. The two target molecules are the centrosymmetric pyrazine-derived p-2BN and the pyrimidine-derived m-2BN, both neutral singlets. The computed endpoint is the S1→S0 relaxation problem for isolated molecules; solvent, crystal packing, and aggregation are not part of the DFT model.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build the reduced molecular models | p-2BN and m-2BN structures; octyl groups replaced by methyl | Gaussian 16 | neutral, singlet | reduced molecular geometries | ev_doc_8d46deff894e_000036_f263da8ae1ed |
| 2 | Optimize and characterize electronic states | reduced structures | DFT geometry optimization and frequency calculations | PBE0/6-31G(d,p) for λ/RMSD analysis | relaxed S0 and S1 geometries, frequencies and normal modes | ev_doc_76d410568d6c_000075_5df47989acef; ev_doc_76d410568d6c_000116_01258835c62f |
| 3 | Quantify structural/electronic relaxation | S0/S1 geometries and energies | internal analysis of Gaussian outputs | S1→S0 reorganization-energy convention; RMSD after atom-consistent alignment | λ and RMSD | ev_doc_76d410568d6c_000116_01258835c62f |
| 4 | Resolve mode contributions | normal modes and state displacement data | Multiwfn 3.8 analysis/visualization | Huang–Rhys factors and mode ranking | HR factors and leading modes | ev_doc_8d46deff894e_000036_f263da8ae1ed; ev_doc_76d410568d6c_000112_ea460722b8ad |

The SI separately reports B3LYP/6-31G(d,p) geometry, HOMO/LUMO and ESP calculations and B3LYP/6-31G* TD calculations for transitions; those calculations are not the λ/RMSD target route.

## 4. Validation and analysis protocol

The authors compare the two isomers' λ and RMSD values, inspect the five modes with the largest λ contributions, and partition RMSD into backbone and side-group contributions. Their interpretation is that p-2BN and p-BN have mainly backbone-dominated leading vibrations, whereas m-2BN and m-BN have stronger side-phenyl contributions. The paper also relates lower λ/RMSD for the pyrazine-derived compounds to stronger ICT and lower non-radiative decay, while noting that side-group motion need not strongly broaden the backbone-controlled emission.

## 5. Private reference results

For the reduced-model comparison, the paper reports λ = 0.19 eV and RMSD = 0.0671 Å for p-2BN, and λ = 0.45 eV and RMSD = 0.4664 Å for m-2BN (Table 1; Fig. 5). It gives ranges across related compounds of 0.19 eV / 0.06–0.07 Å for pyrazine-derived compounds and 0.44–0.45 eV / 0.28–0.46 Å for pyrimidine-derived compounds. Leading modes are backbone-dominated for p-2BN and side-phenyl-dominated for m-2BN. The paper reports CT components of 56.8% (p-2BN) and 40.9% (m-2BN), and solution fluorescence λF of 638 and 447 nm, respectively, as contextual support rather than target outputs.

## 6. Limitations and interpretation boundaries

The source does not provide a machine-readable Cartesian input or complete computational output archive, and the paper's λ/HR implementation details are abbreviated. Results therefore require an explicit convention, atom mapping, geometry-alignment method, and uncertainty report. Agreement with the published values is a reproduction check, not proof that one model chemistry is uniquely correct. The isolated reduced molecules do not represent crystal packing, solvent relaxation, or the full octyl substituents.
