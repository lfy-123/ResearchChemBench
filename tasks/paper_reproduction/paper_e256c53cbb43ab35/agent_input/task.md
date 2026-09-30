# Scientific objective

Determine, by an independently planned and executed atomistic calculation, the average Li adsorption energy per Li atom for the two supplied Cu(111) first-layer systems: θ=0.04 (one Li in the p(5×5) cell) and θ=1 (the complete 25-site fcc-hollow adlayer). Test the authors' qualitative hypothesis that increasing Li coverage weakens adsorption because lateral adlayer interactions make adsorption less favorable. The measured quantity is E_ads=(E_system−E_clean−nE_Li)/n in eV per Li, using consistent total-energy references.

# Public inputs and scientific boundaries

All four XYZ files and system_manifest.json under data/inputs are public. They uniquely specify neutral Cu and Li composition, Cartesian coordinates in Å, the p(5×5) in-plane vectors, five Cu layers, 15 Å z vacuum to add/use, bottom two fixed and top three relaxable, fcc-hollow site identity, n=1 and n=25 coverage counts, a neutral isolated Li doublet reference. Do not impose a molecular singlet multiplicity on the periodic metallic slab; document its spin treatment separately. The object is a vacuum periodic slab; electrolyte, explicit potential, defects, steps, alloying, and second-layer Li are outside scope. Choose and justify the electronic-structure method and convergence settings independently; the paper's route is qualitative context only, not a required protocol or answer.

# Required scientific validation/investigation

Plan calculations for the clean slab, isolated Li, θ=0.04 and θ=1 systems, then relax and/or compute consistent energies as justified. Verify atom counts, periodic cell, fixed/relaxed-layer masks, fcc registry, charge and spin treatment. Demonstrate numerical convergence or quantify residual sensitivity for the principal energy difference. Compute both endpoint adsorption energies, their signed change E_ads(θ=1)−E_ads(θ=0.04), and state whether the hypothesis is supported. The calculation is complete when all four energies and validation diagnostics are available or a bounded failure report identifies the missing result and attempted checks. Stop after the defined endpoint systems have been treated and at least one convergence/sensitivity check or an explicit resource limitation has been documented; do not expand to other coverages unless used only as a clearly labelled optional check.

# Deliverables

Submit report/results.json conforming to submission_schema.json. Include method, per-system energies, endpoint adsorption energies with units, coverage trend, validation evidence, limitations, and a conclusion tied to the supplied objects. If computation cannot be completed, use the bounded-failure branch with attempted calculations, missing fields, diagnostics, and a scientifically honest limitation; do not fabricate values.
