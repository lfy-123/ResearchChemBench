# Scientific objective

Independently calculate the equilibrium inner radius of the specified two-segment MoSSe/MoS2 nanoscroll and test the authors' qualitative hypothesis that spontaneous curvature drives scrolling while bending and interlayer van der Waals energies select the final radius. Use the supplied continuum geometry and material data; do not use the paper or general web. Report the radius in nm, the selected complete/incomplete outer-segment regime, the energy-minimization or stationarity evidence, and the physical interpretation.

# Public inputs and scientific boundaries

The public input `data/inputs/system.json` defines segment_1 as MoSSe (100.0 nm, kappa=15.2 eV, C=0.018 A^-1) followed by segment_2 as MoS2 (100.0 nm, kappa=11.6 eV, C=0), total length 200.0 nm. It defines h1=6.329 A, h2=6.066 A, gamma1=0.0282 eV/A2, gamma2=0.0256 eV/A2, and interface gamma12=0.0288 eV/A2. Treat the ribbon as free-standing and its cross-section as two joined Archimedean spiral segments. Use area conservation to obtain each outer radius from the inner radius. Width W is positive and common to all terms; report its treatment because it cancels from the stationary radius. Energies are relative to the spontaneously curved flat-segment reference. No atomistic coordinates, stacking registry, thermal trajectory, or paper answer is part of this task.

# Required scientific validation/investigation

Write the total energy used, define every radius and angle, and search the physically admissible positive inner-radius domain. Evaluate both possible outer-segment regimes: complete turn (outer angular span at least 2pi) and incomplete turn (less than 2pi), using a source-independent consistent energy expression and selecting the lowest valid minimum. Demonstrate numerical convergence by changing the search resolution or optimizer settings and report the residual derivative/stationarity check or equivalent energy-bracket check. Validate that the selected configuration is a local minimum, that all radii are ordered, and that the reported regime agrees with its computed angle. Completion requires a converged radius, regime classification, and reproducible numerical validation. Stop when two independent numerical checks agree within 0.01 nm and the derivative/energy criterion is satisfied; if no physical minimum is found, submit the bounded-failure branch with the explored domain and reason.

# Deliverables

Submit `report/results.json` conforming to the schema. Include the numerical radius, regime, outer radii and angle, energy/stationarity validation, method summary, interpretation of the author hypothesis, and limitations. A bounded-failure submission must still include the explored domain, validation attempt, and scientifically specific failure reason.
