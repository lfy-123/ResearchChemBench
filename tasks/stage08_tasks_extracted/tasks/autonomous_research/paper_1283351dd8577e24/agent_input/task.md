# Scientific objective

For neutral enol 7,9-bis(4-nitrophenyl)-10-hydroxybenzo[h]quinoline (1NO2), independently determine whether the lowest singlet excited-state landscape along the hydroxy O–H distance supports an intact-hydrogen-bond basin, proton transfer, or another outcome, and discriminate plausible electronic/structural explanations with validated computation.

# Public inputs and scientific boundaries

Use `data/inputs/molecular_identity.json` and `data/inputs/problem_boundary.json`. The object is the neutral, closed-shell enol molecule specified there. The solvent boundary is dichloromethane and the reaction coordinate is the distance from the hydroxy oxygen to its attached hydrogen, in Å. Investigate S0 and the lowest singlet excited state S1 of the isolated molecule. You may construct 3-D coordinates and computational models independently. Do not treat a failed optimization as a numerical result.

# Required scientific validation/investigation

Propose plausible competing explanations for the excited-state profile before selecting one, then generate and retain at least two chemically distinct starting conformers by varying the two aryl/backbone torsions. Preserve atom mapping and optimization outcomes, and advance a conformer only after checking connectivity, charge, multiplicity, convergence and (where applicable) vibrational stability. Obtain an S1 O–H profile with enough points to establish the local shape and the direction toward proton transfer; state the sampled range and spacing and explain any adaptive refinement. For every profile point report constrained O–H distance, relative energy, state definition, convergence status and geometry identifier. Validate the selected basin or alternative outcome against neighboring points and at least one independent check, and use geometry plus orbital/density/transition evidence to discriminate the proposed explanations. The investigation is complete when candidate coverage, a converged profile covering intact and transfer-side regions, validation, and a conclusion are documented. Stop when further refinement changes the reported conclusion within the stated uncertainty, or stop earlier only with a scientifically justified failure/coverage limitation; report the coverage and unresolved ambiguity.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include hypotheses, candidate/conformer table, profile points, basin/barrier or alternative-outcome analysis, validation evidence, electronic interpretation, software/method details, uncertainties, and a conclusion. A bounded-failure branch is allowed only when attempted work, diagnostics, achieved coverage and limitations are present; do not invent missing energies or structures.
