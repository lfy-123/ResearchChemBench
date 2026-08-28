# Private paper route

## 1. Scientific objective and author claim

The paper asks whether the face-centered-cubic (fcc) HoH3 phase, retained at ambient pressure after high-pressure synthesis, is thermodynamically metastable but dynamically persistent at experimentally relevant finite temperature. The authors claim that the cubic phase has a harmonic instability at 0 K, while anharmonic thermal motion stabilizes it at finite temperature and thereby helps explain ambient retention.

## 2. System and model boundary

The system is stoichiometric HoH3 in the cubic Fm-3m structure, with Ho on 4a, octahedral H on 4b, and tetrahedral H on 8c. The experimental ambient lattice parameter is 5.245(2) Å. The computational boundary is the 0-GPa crystal at 0 K in the harmonic approximation and at finite temperature in atomistic dynamics/temperature-renormalized lattice dynamics. The source also reports the Ho-H binary convex-hull context, but that thermodynamic calculation is not required for this task.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax the fcc-HoH3 structure and obtain forces | Fm-3m HoH3 cell | PAW DFT in VASP using PBE | 520 eV cutoff; Monkhorst-Pack spacing 2π×0.03 Å^-1; residual forces below 10^-5 eV Å^-1 | relaxed structure and energies/forces | ev_doc_1e04117422c9_000057_4f61fa6e1bee; ev_doc_1e04117422c9_000058_f10083ac3427; ev_doc_1e04117422c9_000060_a86f4cf40c9e |
| 2 | Test the harmonic limit | relaxed fcc-HoH3 | finite-displacement force constants with PHONOPY | 2×2×2 real-space supercell; 3×3×3 k-point mesh | harmonic phonon dispersion | ev_doc_1e04117422c9_000089_a2f11494d497 |
| 3 | Sample finite-temperature lattice dynamics | experimental-lattice fcc-HoH3 | Born-Oppenheimer AIMD in VASP with on-the-fly ML potentials and Nosé-Hoover thermostat | 128-atom 2×2×2 supercell; 300 K; 50 ps; 1 fs timestep; electronic force convergence 10^-3 eV Å^-1 | trajectory and energy time series | ev_doc_1e04117422c9_000089_a2f11494d497 |
| 4 | Extract thermal effective force constants and phonons | AIMD trajectory | TDEP | 300 K (and separately 50 K) | renormalized phonon dispersions | ev_doc_1e04117422c9_000089_a2f11494d497 |

## 4. Validation and analysis protocol

The authors compared the 0-K harmonic spectrum with finite-temperature TDEP spectra and inspected AIMD energy and atomic trajectories. Harmonic imaginary modes throughout the Brillouin zone were interpreted as 0-K dynamic instability. Absence of imaginary modes in the TDEP spectrum, together with no phase transition or structural collapse in the finite-temperature trajectory, was interpreted as finite-temperature dynamic stability. The SI captions describe approximately 40 ps trajectory displays, while the computational-details paragraph specifies 50 ps simulations.

## 5. Private reference results

The paper reports widespread imaginary modes for harmonic fcc-HoH3 at 0 GPa and 0 K. At 300 K, TDEP-renormalized phonons are fully real and the 50-ps AIMD trajectory shows no phase transition or structural collapse. The same qualitative finite-temperature stabilization is reported at 50 K. These are hidden reference results, not public task inputs.

## 6. Limitations and interpretation boundaries

Finite trajectory length, finite supercell, exchange-correlation and pseudopotential choices, and the distinction between absence of an observed event and proof of infinite-time stability limit the claim. A successful task result should therefore state finite-time dynamical persistence under the tested conditions, not absolute thermodynamic or kinetic stability. Harmonic imaginary modes are a local 0-K criterion and do not alone determine experimental recoverability.
