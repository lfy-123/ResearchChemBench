# Scientific objective

Independently plan and execute a calculation for one neutral triplet O2 molecule adsorbed upright at the fcc hollow site of the supplied Ag(111) slab. Determine the relaxed adsorption energy relative to the supplied isolated-O2 and clean-slab references, the O2 center-to-top-layer height, the net Bader charge received by O2, and its magnetic moment. The authors' qualitative hypothesis is that substrate electron transfer reduces O2 spin; test that hypothesis quantitatively while keeping your method choices independent.

# Public inputs and scientific boundaries

Use `data/inputs/adsorbate_ag111.vasp`, which explicitly contains 24 Ag atoms in six (111) layers in a 2×2 periodic cell, 15 Å of slab vacuum, and two O atoms upright over the fcc hollow. Use `data/inputs/isolated_o2.xyz` as the neutral triplet O2 reference. The manifest gives the charge, multiplicity, surface spacing, and atom identity. You must also construct a clean Ag slab with the same cell and a consistent isolated-O2 reference for the adsorption-energy difference. Only the single-molecule object is scored; monolayers, domain walls, and alternative sites are optional context and not scored.

# Required scientific validation/investigation

Choose and document a defensible electronic-structure method, relaxation criteria, spin treatment, periodic-boundary treatment, and charge/moment analysis. Demonstrate that the relaxed structure is a genuine stationary adsorption state and report the exact atom groups used for height, Bader charge, and moment. Check numerical stability by at least one explicit convergence or repeat comparison and report the observed change in each scored observable. The calculation is complete when the combined system, clean slab, and isolated molecule have converged energies and the analysis outputs are traceable to the same relaxed combined structure. Stop after those checks and a final interpretation; if a calculation cannot be completed, submit the bounded-failure branch with attempted setup, diagnostic evidence, and the limitation rather than fabricated values.

# Deliverables

Submit `report/results.json` conforming to the schema. Include method and validation provenance, all successful observables with units and object identity, or the bounded-failure branch. State whether the computed moment is reduced relative to the isolated-O2 reference and explain the scope of that conclusion. Include paths or hashes for key output files so the work is auditable.
