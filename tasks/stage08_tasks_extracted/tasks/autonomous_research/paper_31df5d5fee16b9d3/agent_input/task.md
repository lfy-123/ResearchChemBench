# Scientific objective

Determine from first-principles or an equivalent independently justified atomistic calculation how the supplied bilayer V₂O₅·H₂O structure relaxes and what its Γ-point/Raman vibrational signatures imply about symmetry and the origin of hydrated-V₂O₅ bands. Generate and test your own plausible structural/vibrational explanations from your calculations.

# Public inputs and scientific boundaries

Use `data/inputs/v2o5_h2o_p1.json`, a neutral singlet periodic V₈O₂₅H₈ bilayer cell with explicit fractional coordinates. O* is the interlayer water oxygen and H(1)–H(8) are its water hydrogens. The physical boundary is the supplied periodic cell with its given composition and atom identities. Measure relaxed lattice lengths/angles, Γ-point frequencies, Raman activity/intensity where available, and mode composition. Any software/model may be chosen but must be disclosed. Comparison to experiment is limited to observed hydrated-V₂O₅ lattice and Raman features.

# Required scientific validation/investigation

Define at least two plausible explanations for prominent hydrated-V₂O₅ vibrational bands or apparent symmetry, then use the calculation to discriminate them. Relax the cell and validate atom count/composition, force/stress convergence, preservation of water connectivity, and treatment of imaginary modes. Compute and interpret Γ-point vibrations, using eigenvectors, projections, or Raman tensors to support assignments. Report the search/analysis coverage and stop after a converged relaxation and a checked vibrational analysis; if a requested observable cannot be computed, use the bounded-failure branch with diagnostics and a limitation statement. Completion requires an independent conclusion tied to reported evidence, not merely a method description.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. In the complete branch, include at least two hypotheses, each with its test and evidence-based result, method/settings, relaxed cell, convergence and chemical-integrity checks (including water connectivity and explicit imaginary-mode treatment), and at least three vibrational modes. Each mode must retain an input atom-label or chemically unique object identity and individually report eigenvector, projection, or Raman-tensor validation evidence; distinguish water and framework contributions. Include experimental comparison with uncertainty or measurement mismatch, discriminating conclusion, and limitations. Bounded failure requires the alternative branch fields and must not fabricate numerical results.
