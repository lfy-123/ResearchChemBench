# Private paper route

## 1. Scientific objective and author claim

The authors use quantum chemistry to explain photophysical differences across seven neutral, tetracoordinate boron(III) complexes BQ1–BQ7. Their claim is that halogen-dependent spin–orbit coupling changes the S1→T1 intersystem-crossing rate and therefore helps explain fluorescence-yield trends; iodine and bromine give the strongest heavy-atom effect.

## 2. System and model boundary

Each BQ complex contains BPh2 bound through N and O to one deprotonated 8-hydroxyquinoline ligand. BQ1 is unsubstituted; BQ2 is 5-Cl; BQ3 is 5,7-Cl2; BQ4 is 5,7-Br2; BQ5 is 5,7-I2; BQ6 is 5-Cl-7-I; BQ7 is 5,7-Cl2-2-Me. Monomers are treated in toluene PCM. A separate BQ7 stacked dimer calculation uses a crystal-derived ONIOM QM/MM model in water.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground state | BQ1–BQ7 monomers | DFT, Gaussian 16 | MPW1PW91; 6-31+G(d,p), LanL2DZ on I; PCM/toluene | S0 geometries | ev_doc_2f57598ccba9_000216_5819ab9c0aaf |
| 2 | Optimize excited states | S0 geometries | TD-DFT/TDA, Gaussian 16 | MPW1PW91; same mixed basis and PCM/toluene | S1, T1, T2 geometries and adiabatic energies | ev_doc_2f57598ccba9_000216_5819ab9c0aaf |
| 3 | Compute spin–orbit coupling | T1 geometries | SOMF/RI, ORCA | CAM-B3LYP; ZORA-def2-TZVP, SARC-ZORA-TZVP on I; RIJCOSX; PCM/toluene | S1/T1 SOC | ev_doc_2f57598ccba9_000229_e8adc764bc23 |
| 4 | Compute decay rates | excited geometries, frequencies, SOC | ORCA AH rate model and FCclasses3 | FC and HT terms; Cartesian TD treatment; Lorentzian HWHM 0.01 eV; PCM/toluene | kISC and kfl | ev_doc_2f57598ccba9_000229_e8adc764bc23 |
| 5 | Model aggregate | crystal BQ7 packing | multilayer ONIOM QM/MM, Gaussian 16 | BQ7 dimer QM, surrounding molecules UFF/Qeq MM; MPW1PW91/6-31+G(d,p), PCM/water | dimer S0/S1/T1 properties and SOC | ev_doc_2f57598ccba9_000229_e8adc764bc23 |

## 4. Validation and analysis protocol

The paper compares calculated absorption/emission quantities with experiment, reports S1/T1/T2 adiabatic energies, S1–T1 gaps, SOCs, FC and FC-HT ISC rates, fluorescence rates, and computes Φfl = kfl/(kfl+kISC). The interpretation emphasizes that S1 lies below T2 and above T1, and that SOC and energy gap jointly control ISC. Aggregate BQ7 is analyzed as a stacked dimer to rationalize its condensed-phase behavior.

## 5. Private reference results

Table 3 reports, for BQ1–BQ7, the numerical Ead(S1), Ead(T1), Ead(T2), ΔES–T, SOC, kISC (FC-HT and FC), kfl and calculated Φfl. Table S4 reports vertical absorption/emission energies, wavelengths, oscillator strengths and dominant H→L character. These values are evaluator-only.

## 6. Limitations and interpretation boundaries

The calculations are model-dependent and the authors note that ISC rates are likely underestimated when HT effects are neglected. Experimental agreement is described as qualitative/semi-quantitative. The benchmark therefore scores reproducible state definitions, validation provenance, trends and reported numerical observables separately, and accepts a scientifically justified bounded-failure report when software or excited-state convergence prevents a complete result.
