# Private paper route

## 1. Scientific objective and author claim

The paper uses computation to explain substituent-dependent optical properties of four triaryl-heptazine photocatalysts. The authors claim that the weak visible absorption is dominated by a symmetry-forbidden HOMO→LUMO excitation for dFHeptZ, dClHeptZ and dMeHeptZ, whereas dOMeHeptZ is dominated by HOMO−3→LUMO. The HOMO density is chiefly on the heptazine nitrogen core for dFHeptZ (and similarly dClHeptZ/dMeHeptZ); this does not describe their LUMO density, which extends across the molecule. dOMeHeptZ has HOMO density on its dimethoxyphenyl substituents (main PDF p3).

## 2. System and model boundary

The system is the neutral, closed-shell singlet molecule in acetonitrile, for each of 2,5,8-tris(2,4-disubstituted-phenyl)heptazine derivatives: dFHeptZ (2,4-F), dClHeptZ (2,4-Cl), dOMeHeptZ (2,4-OMe), and dMeHeptZ (2,4-Me). The calculations concern isolated-molecule ground-state minima and vertical singlet excitations; solvent is represented by IEFPCM acetonitrile. Experimental spectra are context, not computed observables.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground-state geometry | Each named heptazine | Gaussian 16 Rev. B.01 | B3LYP/6-311+G(d,p), charge 0, singlet | Optimized geometry | ev_doc_2b68f45a212f_000247_eb97a539c3c1; ev_doc_2b68f45a212f_000251_114fa7ca3032 |
| 2 | Verify a true minimum | Optimized geometry | Gaussian 16 frequency calculation | Same level; zero imaginary frequencies required | Frequency-validated minimum | ev_doc_2b68f45a212f_000247_eb97a539c3c1; ev_doc_2b68f45a212f_000257_81d2bdb3a80f |
| 3 | Calculate vertical UV-visible transitions | Validated optimized geometry | Gaussian 16 TD-DFT | TD-PBE0/6-311+G(d,p), IEFPCM acetonitrile, first 18 singlet states | Energy, wavelength, oscillator strength, major orbital contributions | ev_doc_2b68f45a212f_000249_f418ce718d65; ev_doc_2b68f45a212f_000267_cab8f82ada13 |
| 4 | Inspect frontier orbitals and interpret bands | PBE0 orbitals at the optimized B3LYP geometries and TD-DFT output | Gaussian 16/GaussView 6.1.1 | Same PBE0/6-311+G(d,p)/IEFPCM acetonitrile level as step 3 (SI S19); orbital isovalue 0.02; distinguish HOMO and LUMO localization | Localization and transition-character interpretation | ev_doc_2b68f45a212f_000287_b6ac20791ec1; ev_doc_b5d19aa5ec32_000047_466756b3a378 |

## 4. Validation and analysis protocol

For every molecule, verify formula/atom count, neutral singlet charge and multiplicity, optimization convergence, and absence of imaginary frequencies. Report the lowest-energy singlet transitions and the lowest-energy transition with non-negligible oscillator strength, retaining state identity and orbital contributions. Compare transition energies/wavelengths and oscillator strengths to the corresponding hidden SI table, and assess whether the visible-band orbital assignment and frontier-density localization are reproduced. Differences caused by independent conformers, software or method choices must be reported rather than silently treated as exact reproduction.

## 5. Private reference results

The SI tables S3a–S3d give 18 singlet transitions per molecule. The first state is at 420.56 nm for dFHeptZ (HOMO→LUMO, f=0), 427.97 nm for dClHeptZ (HOMO→LUMO, f=0), 407.35 nm for dOMeHeptZ (HOMO−3→LUMO, f=0.0001), and 411.62 nm for dMeHeptZ (HOMO→LUMO, f=0). The main paper reports core-localized HOMO density for dFHeptZ and analogous dClHeptZ/dMeHeptZ behavior, but substituent-localized HOMO density for dOMeHeptZ.

## 6. Limitations and interpretation boundaries

These are isolated-molecule vertical excitations and do not establish solid-state spectra, vibronic line shapes, aggregation, nonradiative rates, or catalytic performance. Orbital labels can change under near-degeneracy and different conformers; assignments should therefore be tied to the submitted calculation and stated analysis criterion.
