# Private paper route

## 1. Scientific objective and author claim

The paper studies how O, S, and Se substitution in neutral 8-chalcogen-quinoline-BODIPY (8QBDY-X) changes excited-state intramolecular proton transfer (ESIPT). The author claim is that heavier chalcogens facilitate ESIPT and thereby tune fluorescence.

## 2. System and model boundary

The systems are neutral enol 8QBDY-O, 8QBDY-S, and 8QBDY-Se in the first singlet excited state, with proton transfer from X-H to the quinoline nitrogen giving the corresponding keto excited state. Solvent is represented as acetonitrile through CPCM in the authors' calculations.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize ground and first excited geometries | 8QBDY-X structures | Gaussian 16 DFT/TD-DFT | ωB97X-D/6-311G(d,p), CPCM acetonitrile | S0 and S1 enol/keto geometries | ev_doc_d25dd3ea0bfe_000033_0d6a956ecad8, ev_doc_d25dd3ea0bfe_000034_e60764ff498a |
| 2 | Establish ESIPT potential-energy profile and locate saddle point | optimized S1 enol geometry | relaxed PES scan followed by TS refinement | scan along X-H coordinate in S1 | TS and activation free energy | ev_doc_d25dd3ea0bfe_000035_a00e092e1956, ev_doc_d25dd3ea0bfe_000116_66662dceff68 |
| 3 | Validate stationary points and connectivity | optimized minima and TS | harmonic frequencies and IRC | minima: zero imaginary frequencies; TS: one imaginary frequency; forward/reverse IRC | validated ESIPT pathway | ev_doc_d25dd3ea0bfe_000049_6fbc2660a67d |
| 4 | Convert activation free energy to kinetics | validated S1 barrier | conventional transition-state theory | T = 298.15 K | k in s^-1 | ev_doc_d25dd3ea0bfe_000135_7971f62787a6, ev_doc_d25dd3ea0bfe_000139_f02b573e3300 |

## 4. Validation and analysis protocol

The authors verify minima and first-order saddle points by harmonic frequencies and verify that each TS connects the enol and keto minima by IRC in both directions. They compare the three chalcogen cases using the S1 ESIPT free-energy barrier and TST rate constant, and interpret the O→S→Se trend together with the calculated excited-state structures and fluorescence discussion.

## 5. Private reference results

For O, S, and Se respectively, the reported S1 ESIPT activation free energies are 13.54, 7.81, and 6.89 kcal mol^-1; the corresponding TST rates at 298.15 K are 7.39×10^2, 1.17×10^7, and 5.53×10^7 s^-1. The ordering is O > S > Se for barriers and O < S < Se for rates. These values are reported in Table 1 and its associated text (ev_doc_d25dd3ea0bfe_000121_4d764c388bca, ev_doc_d25dd3ea0bfe_000146_08aa923aed62, ev_doc_d25dd3ea0bfe_000149_b1e2c71911a1, ev_doc_d25dd3ea0bfe_000153_b1ebe01149a6, ev_doc_d25dd3ea0bfe_000155_c12232d9f15f).

## 6. Limitations and interpretation boundaries

These are single-level continuum-solvent calculations and TST estimates. The rate comparison is a comparison of computed S1 barriers and conventional-TST rates, not a claim that population kinetics, nonradiative decay, solvent dynamics, or excited-state lifetimes were fully simulated. The public task must not assume the authors' numerical protocol is uniquely optimal.
