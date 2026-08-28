# Scientific objective

Determine the equilibrium inner radius and stable cross-sectional regime of the specified two-segment MoSSe/MoS2 nanoscroll from the public physical system, and independently identify which physical contributions control the result. The goal is a reproducible computational conclusion, including any competing explanation that your calculations discriminate.

# Public inputs and scientific boundaries

The public input `data/inputs/system.json` defines an ordered free-standing ribbon with segment_1=MoSSe (100.0 nm, kappa=15.2 eV, C=0.018 A^-1) and segment_2=MoS2 (100.0 nm, kappa=11.6 eV, C=0), total length 200.0 nm. It supplies h1=6.329 A, h2=6.066 A, gamma1=0.0282 eV/A2, gamma2=0.0256 eV/A2, and interface gamma12=0.0288 eV/A2. Use joined Archimedean spiral segments, area conservation, and a positive common width W; state how W is handled. Energies use the spontaneously curved flat state as reference. You may choose a continuum numerical method and may formulate alternative hypotheses, but may not use the paper, SI, general web, or hidden reference values.

# Required scientific validation/investigation

Plan and execute an independent numerical investigation over positive inner radii. Define the energy, geometry, and any regime-dependent treatment you use. Generate and compare at least two plausible explanations or model treatments for the stable morphology, then discriminate them with energy, stationarity, regime-consistency, and convergence evidence. Report candidate minima or bounded failure, search coverage, numerical resolution/termination, and sensitivity to a scientifically justified perturbation of method or parameter treatment. Completion requires a reproducible converged radius and a supported explanation, or a bounded-failure report with the explored domain and limitation. Stop when independent numerical checks agree within 0.01 nm and the selected state is demonstrably locally stable; do not stop merely after finding the first stationary point.

# Deliverables

Submit `report/results.json` conforming to the schema. Include the selected radius, regime, geometry, candidate/model comparison, validation evidence, search coverage, conclusion, and limitations. If the investigation cannot establish a stable state, use the bounded-failure branch and provide the required exploration and failure explanation.
