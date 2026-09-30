# Private paper route

## 1. Scientific objective and author claim

The paper determines which low-lying electronic excitations of the 2-methyl-1-propenyl radical account for the 226–248 nm H-atom photofragment-yield feature, and connects the excited-state preparation to the observed H-loss dynamics. The authors assign the short-wavelength increase chiefly to D4 with 3s Rydberg character, while D3 (n→π*) may contribute near the broad feature around 240 nm.

## 2. System and model boundary

The species is the neutral doublet 2-methyl-1-propenyl radical, C4H7, represented by the CCSD/aug-cc-pVDZ ground-state geometry in SI Table S1. Vertical excitations from that ground-state geometry are considered; the spectroscopy calculation covers D1–D6, and NTO interpretation is a qualitative auxiliary analysis. The photodissociation discussion concerns H + C4H6 channels in the 226–248 nm window.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize the radical ground-state geometry | neutral C4H7 doublet | Gaussian 16 CCSD | aug-cc-pVDZ | optimized Cartesian geometry and energy | ev_doc_c4b3ffacf5ae_000196_8979fb9f7e8b; ev_doc_ca3e72be3209_000012_b9f9d70f8312 |
| 2 | Compute six vertical excited states | optimized geometry from step 1 | Gaussian 16 TDDFT and EOM-CCSD | CAM-B3LYP with d-aug/aug-cc-pVXZ variants; EOM-CCSD with d-aug-cc-pVXZ variants | VEE in nm and oscillator strengths for D1–D6 | ev_doc_c4b3ffacf5ae_000196_8979fb9f7e8b; ev_doc_ca3e72be3209_000024_8ace73923a44 |
| 3 | Interpret excitation character | radical and computed excited states | Gaussian 16 NTO analysis | CAM-B3LYP/6-31++G qualitative reference analysis | dominant NTO transitions and transition-dipole directions | ev_doc_ca3e72be3209_000197_2375b008d4bb; ev_doc_ca3e72be3209_000024_8ace73923a44 |
| 4 | Relate spectroscopy to dynamics | computed states plus PFY/TOF observations | comparison and mechanistic interpretation | 226–248 nm; translational-energy and angular-distribution evidence | assignment and internal-conversion/statistical-dissociation interpretation | ev_doc_c4b3ffacf5ae_000006_e78f1b0c7708; ev_doc_c4b3ffacf5ae_000010_958328a7d543; ev_doc_c4b3ffacf5ae_000393_10fa30e44674 |

## 4. Validation and analysis protocol

The authors compare excitation wavelengths and oscillator strengths across several electronic-structure/basis-set choices, inspect the dominant NTO character and transition-dipole orientation, and compare the resulting spectral locations/intensities with the PFY band. The dynamics interpretation is checked against the low-energy-peaked product translational-energy distributions, modest translational-energy fraction, and isotropic H-atom angular distribution.

## 5. Private reference results

SI Table S4 (SI page S3) reports these **CAM-B3LYP/6-31++G** values: D1 436.9 nm, f 0.002; D2 293.1 nm, 0.000; D3 249.7 nm, 0.003; D4 214.6 nm, 0.033; D5 201.1 nm, 0.000; D6 192.1 nm, 0.002. The distinct **EOM-CCSD/aug-cc-pVDZ** column is D1 421.0 nm, f 0.001; D2 270.6 nm, 0.000; D3 233.7 nm, 0.002; D4 204.3 nm, 0.033; D5 196.3 nm, 0.001; D6 182.6 nm, 0.004. Do not attribute the first method's column to the second method. The table also gives CAM-B3LYP/aug-cc-pVQZ, CAM-B3LYP/d-aug-cc-pVQZ, and additional EOM-CCSD basis-set columns. SI Table S5 identifies D3 as n→π*, D4 as n→3s Rydberg, and gives their transition-dipole directions. The paper reports a broad PFY feature near 240 nm with increased intensity below 228 nm, a translational-energy peak near 7 kcal mol−1, average translational-energy fraction 0.13–0.15, and an isotropic angular distribution. The favored ground-state H-loss product is methylenecyclopropane + H after internal conversion and isomerization.

## 6. Limitations and interpretation boundaries

The tabulated methods are not interchangeable benchmarks; state ordering and basis-set sensitivity must be reported. The PFY observes H-loss, not the total absorption, and the D3/D4 assignment is an interpretation rather than a uniquely measured electronic-state label. The public task therefore scores reproducible state observables and evidence-based interpretation, while allowing method choice and explicit limitations.
