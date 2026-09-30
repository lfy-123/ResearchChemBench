# Private paper route

## 1. Scientific objective and author claim

The paper evaluates protonation/deprotonation geometries of near-infrared probes A and B. For neutral probe A, the authors compare the OH···N and NH···O tautomeric arrangements and report that the NH···O form is more stable by 5.3 kcal mol⁻¹. This energetic ordering is used to interpret the pH-dependent conjugation/ESIPT picture.

## 2. System and model boundary

The benchmark system is neutral, singlet probe A in two tautomeric arrangements. The SI Tables S4 (pp. 24–25) and S6 (pp. 28–29) each provide 73-atom Cartesian geometries, C35H33N3O2, for A-OH···N and A-NH···O, respectively. The previous extraction omitted the two oxygen rows (16 and 17) from both tables; the public XYZ files now retain all rows in the original SI order. The authors treat the isolated molecule with implicit water solvation; no explicit solvent molecules are part of the reported geometry tables.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize each proposed tautomeric geometry | SI coordinate tables S4 and S6 | Gaussian 16 | APFD/6-311+G(d,p), PCM water, ultrafine grid, electronic accuracy 10⁻¹² | optimized structures and electronic energies | ev_doc_9f39b94ab5bf_000153_ec7bf3e701c6; ev_doc_9f39b94ab5bf_000154_646313264ef6; ev_doc_9f39b94ab5bf_000155_60ca75c65881 |
| 2 | Verify stationary points and obtain thermochemistry | optimized structures | Gaussian 16 frequency calculation | same solvation and electronic-structure settings | vibrational frequencies and thermochemical data; no imaginary frequencies | ev_doc_9f39b94ab5bf_000153_ec7bf3e701c6; ev_doc_9f39b94ab5bf_000154_646313264ef6; ev_doc_9f39b94ab5bf_000155_60ca75c65881 |
| 3 | Compare tautomer stabilities | validated results from steps 1–2 | energy subtraction | same energy convention for both states | relative stability difference | ev_doc_9f39b94ab5bf_000266_301cf171126b; ev_doc_9f39b94ab5bf_000267_85ef3f544910 |

## 4. Validation and analysis protocol

Each optimized structure must be a real minimum, assessed from the complete frequency calculation. The relative value is obtained by subtracting the lower-state energy from the higher-state energy and reporting the magnitude with the identity of the lower state. The authors' broader calculations also used TD-DFT for transitions, but that is outside this benchmark's scored endpoint.

## 5. Private reference results

For neutral probe A, A-NH···O is lower in energy than A-OH···N by 5.3 kcal mol⁻¹. The paper additionally reports the analogous B difference as 3.8 kcal mol⁻¹ and protonated OH···N versus NH···O differences of 6.4 and 5.9 kcal mol⁻¹, but those are not benchmark targets.

## 6. Limitations and interpretation boundaries

The benchmark tests a reported relative electronic/thermochemical calculation, not experimental pKa, fluorescence wavelengths, or a universal tautomer population. Different legitimate conformer searches, dispersion treatments, thermal conventions, or software can shift the value; submissions must state their convention and validation evidence. The hidden reference is the paper's stated comparison, not a newly recomputed value.
