# Scientific objective

Independently test the paper's qualitative hypothesis that changing proton source (acidic H3O+ versus alkaline H2O) and H* coverage changes the GC-DFT free-energy profile for HER on Au(111), with consequences for Volmer, Heyrovsky, and Tafel kinetics. Compute and compare reaction free energies and activation barriers for the declared states, without using paper/SI or general web content.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json`. The system is a 3-layer 3×3 Au(111) slab with 15 Å vacuum, bottom two layers fixed, nine top-layer sites; acidic solvent is H7O3+ and alkaline solvent H8O4; potentials are 0.000 and −0.826 V vs SHE; coverages are 0 and 7/9 ML (0 or 7 pre-adsorbed H). The measured objects are ΔG and G_a for each of Volmer, Heyrovsky, and Tafel in each medium/coverage. You may choose software and model chemistry, but state charge, multiplicity, constraints, solvation, and reference conventions. Do not claim exact author-structure reproduction.

# Required scientific validation/investigation

Generate at least one deduplicated initial and final state for every requested elementary step and medium/coverage, then optimize and validate each state. Advance a candidate only if forces/energy meet a stated criterion and connectivity is preserved. Locate and validate a TS or minimum-energy path; report endpoint continuity and an appropriate saddle/path diagnostic. Stop when all 12 step-condition combinations have a converged state/path or explicitly report bounded failure and the attempted coverage. Compare the four condition classes and test the stated hypothesis. Report sensitivity to at least one conformer or numerical choice and limitations.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include per-object identities, structures or hashes, ΔG/G_a with units and method, validation evidence, comparisons, conclusion, and truthful completion status. A bounded-failure branch must identify missing objects and attempted search coverage.
