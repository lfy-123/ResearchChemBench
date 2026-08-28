# Private paper route

## 1. Scientific objective and author claim

The paper studies the photophysical mechanism of cucurbit[8]uril/terpyridine-derivative host--guest systems. For the isolated G1 guest, the implemented calculation predicts the S1 fluorescence/emission wavelength and uses NTO/hole--electron analysis to characterize the transition. The authors interpret the G1 S1 transition as predominantly intramolecular charge transfer rather than a donor--acceptor transition between host and guest.

## 2. System and model boundary

G1 is the isolated cationic guest represented by the SI coordinate block `G1GS` (242 atoms). The reported isolated-guest optical calculation is distinct from the CB[8] host--guest complexes. The electronic state is a singlet cation; the public starting coordinates are the SI G1GS geometry.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax the ground state | SI G1GS coordinates | DFT in ORCA 5.0.1 | PBE0 with D3(BJ), old-SVP on H, old-TZVP on C/N/O, DKH; energy 10^-5 Ha, gradient 10^-4 Ha/Å, radial 10^-3 Å | S0 minimum | ev_doc_8e64b208457d_000005_6858e05fb5f0; ev_doc_a8b5b11efff9_000040_ |
| 2 | Relax the first excited singlet | optimized S0 | TDDFT/DFT in ORCA 5.0.1 | PBE0-D3(BJ), same mixed basis and DKH/TDA context; target S1 | S1 minimum | ev_doc_a8b5b11efff9_000040_; ev_doc_a8b5b11efff9_000075_ |
| 3 | Evaluate fluorescence | optimized S1 | TDDFT | S1-to-S0 vertical emission at the relaxed excited-state geometry | emission wavelength | ev_doc_a8b5b11efff9_000075_; ev_doc_a8b5b11efff9_000078_ |
| 4 | Check stationary points | S0 and S1 geometries | vibrational Hessian | no imaginary eigenvalues | minimum validation | ev_doc_a8b5b11efff9_000040_ |

## 4. Validation and analysis protocol

The authors verified optimized structures by vibrational analysis and required non-negative Hessian eigenvalues. They analyzed optical transitions with localized orbital/NTO representations and compared calculated absorption/emission values with experiment. The paper also compares PBE0-D3 with CAM-B3LYP in the discussion of optical transitions.

## 5. Private reference results

The paper's Table 1 reports an isolated G1 calculated photoluminescence value of 540.3 nm and a host--guest [CB[8]G1_2] calculated photoluminescence value of 566.1 nm. The surrounding text also discusses a 566 nm transition and assigns the isolated guest S1 transition mainly to charge transfer. These values are private evaluator references; they are intentionally absent from public inputs and task instructions.

## 6. Limitations and interpretation boundaries

The paper does not fully disambiguate every excited-state implementation detail in the prose, including the precise role of TDA during S1 optimization. The benchmark therefore evaluates a route-neutral independently chosen calculation and requires the Agent to disclose its actual method, convergence, state tracking and validation. Agreement with a reported wavelength is a test of reproducibility, not proof that a single functional uniquely establishes mechanism. NTO localization is interpreted qualitatively and must be reported with its orbital/state-selection evidence.
