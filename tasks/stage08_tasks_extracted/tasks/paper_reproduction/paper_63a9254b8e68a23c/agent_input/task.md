# Scientific objective

Determine the equilibrium inner radius and stable cross-sectional regime of the specified two-segment MoSSe/MoS2 nanoscroll from the public physical system, and independently identify which physical contributions control the result. The goal is a reproducible computational conclusion, including any competing explanation that your calculations discriminate.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that spontaneous curvature of the MoSSe segment drives scrolling, while the balance of bending and interlayer van der Waals contributions selects the equilibrium inner radius. Their continuum treatment targets the stable cross-sectional morphology of the ordered MoSSe/MoS2 ribbon.

**Candidate route or mechanism.**
A useful candidate treatment is a joined Archimedean spiral with the MoSSe segment leading into the inner turn and the MoS2 segment continuing outward. Compare complete-turn and incomplete-turn descriptions for the outer segment, with area conservation determining the outer radii and the energy evaluated relative to the spontaneously curved flat state.

**Discriminating evidence.**
Use total-energy comparisons and stationarity checks across positive inner radii, verify the angular-span regime and radius ordering, and test convergence under search or optimizer changes. Separate bending, intrasegment interlayer, and interface contributions so their relative control of the selected state can be assessed.

# Public inputs and scientific boundaries

The public input `data/inputs/system.json` defines an ordered free-standing ribbon with segment_1=MoSSe (100.0 nm, kappa=15.2 eV, C=0.018 A^-1) and segment_2=MoS2 (100.0 nm, kappa=11.6 eV, C=0), total length 200.0 nm. It supplies h1=6.329 A, h2=6.066 A, gamma1=0.0282 eV/A2, gamma2=0.0256 eV/A2, and interface gamma12=0.0288 eV/A2. Use joined Archimedean spiral segments, area conservation, and a positive common width W; state how W is handled. Energies use the spontaneously curved flat state as reference. The scored system is the isolated molecule; do not add a host or solvent. You may choose a continuum numerical method and may formulate alternative hypotheses, but may not use sources beyond the supplied public system.

# Required scientific validation/investigation

Plan and execute an independent numerical investigation over positive inner radii. Define the energy, geometry, and any regime-dependent treatment you use. Generate and compare at least two plausible explanations or model treatments for the stable morphology, then discriminate them with energy, stationarity, regime-consistency, and convergence evidence. Report candidate minima or bounded failure, search coverage, numerical resolution/termination, and sensitivity to a scientifically justified perturbation of method or parameter treatment. Completion requires a reproducible converged radius and a supported explanation, or a bounded-failure report with the explored domain and limitation. Stop when independent numerical checks agree within 0.01 nm and the selected state is demonstrably locally stable; do not stop merely after finding the first stationary point.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. Include the selected radius, regime, geometry, candidate/model comparison, validation evidence, search coverage, conclusion, and limitations. If the investigation cannot establish a stable state, use the bounded-failure branch and provide the required exploration and failure explanation.
