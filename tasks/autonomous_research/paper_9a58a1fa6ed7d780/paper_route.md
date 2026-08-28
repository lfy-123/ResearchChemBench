# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical calculations to explain how internal BN incorporation changes the electronic and excited-state structure of the doubly folded fluoranthene analogue BN-AkFlu (5a). The author claim is that internal BN doping narrows the frontier-orbital gap, produces a low-energy weakly allowed S1 transition and a stronger higher-energy absorption, and is consistent with red-shifted emission relative to the all-carbon analogue.

## 2. System and model boundary

The computed object is an isolated, neutral, singlet BN-AkFlu molecule (C22H15B2N2; 40 atoms) in the gas phase. The SI supplies its optimized S0 Cartesian geometry in Table S21. No crystal packing, solvent, vibronic structure, thermal averaging, or nonradiative dynamics are part of the electronic-structure calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain the reference ground-state structure | BN-AkFlu 5a | Gaussian 16 | B3LYP/6-311G(d,p), neutral singlet geometry optimization | optimized Cartesian coordinates | ev_doc_dc703d39e962_000062_6e8cf8ef6f97; ev_doc_dc703d39e962_000586_918a609fc651 |
| 2 | Calculate vertical singlet excitations and oscillator strengths | optimized isolated molecule | Gaussian 16 TD-DFT | B3LYP/6-311G(d,p), gas phase; states S1-S6 reported | excitation energies, wavelengths, oscillator strengths, orbital contributions | ev_doc_dc703d39e962_000517_f386227f50fd; ev_doc_dc703d39e962_000532_f36e26de8f28 |
| 3 | Characterize S0→Sn charge distributions | excited-state densities from step 2 | Multiwfn analysis of Gaussian output | hole/electron descriptors D, Sr, H, t, HDI, EDI | electron-hole metrics for S1-S4 | ev_doc_dc703d39e962_000520_69afce73eda1; ev_doc_dc703d39e962_000527_23dc99795f45 |
| 4 | Compare calculated spectrum with photophysical interpretation | calculated transitions and experimental spectra | authors' spectral plotting/interpretation | isolated-molecule spectrum; comparison to measured solution spectra | assignment of low-energy weak S1 and strong higher transition; red-shift interpretation | ev_doc_86934be038e1_000010_9e5f87e341f7; ev_doc_86934be038e1_000090_8880f0ce13c4 |

## 4. Validation and analysis protocol

The reported computational observables are checked against SI Tables S11 and S14: state identity, energy/wavelength, oscillator strength, dominant orbital contribution, and the six hole/electron descriptors. The spectrum is interpreted together with Figure S27 and the main-text discussion: S1 is weak, while the intense absorption near 350 nm is associated with a higher singlet transition. Experimental emission is a separate observable and is not treated as a direct vertical-excitation prediction.

## 5. Private reference results

For BN-AkFlu, Table S14 reports S1 2.1406 eV (579.20 nm, f=0.0080, HOMO→LUMO 98.8%), S2 2.8505 eV (434.95 nm, f=0.0001), S3 2.9880 eV (414.94 nm, f=0.0000), S4 3.4014 eV (364.50 nm, f=0.0000), S5 3.6113 eV (343.33 nm, f=1.8524), and S6 3.7197 eV (333.31 nm, f=0.0000). Table S11 reports for S1 D=0.001 Å, Sr=0.797, H=3.886 Å, t=-3.468 Å, HDI=5.14, EDI=4.98; S2 D=0.0, Sr=0.795, H=4.168 Å, t=-3.745 Å, HDI=4.53, EDI=4.73; S3 D=0.0, Sr=0.919, H=3.668 Å, t=-3.193 Å, HDI=4.83, EDI=4.60; S4 D=0.0, Sr=0.913, H=3.877 Å, t=-3.402 Å, HDI=4.53, EDI=4.44.

## 6. Limitations and interpretation boundaries

The SI does not state every Gaussian keyword, state-count request, convergence threshold, or whether TDA was used. Exact reproduction is therefore method-sensitive; evaluation rewards a transparent, independently justified route and comparison of reported observables, with bounded failure allowed when software or excited-state analysis is unavailable. Vertical gas-phase results do not by themselves establish solution emission maxima, solid-state packing, or causal nonradiative rates.
