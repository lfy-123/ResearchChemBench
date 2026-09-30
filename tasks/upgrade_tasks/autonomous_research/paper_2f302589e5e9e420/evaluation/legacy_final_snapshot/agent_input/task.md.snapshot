# Scientific objective

Determine computationally whether adding the ortho-methoxy substituent in the supplied cured-epoxy model changes molecular polarity. Compare the neutral closed-shell fragments EPI1 (without the methoxy substituent) and EPI2 (with the ortho-methoxy substituent), and report their dipole moments, the percent change from EPI1 to EPI2, and hydroxyl-oxygen electrostatic-potential values if calculated. The scientific object is the isolated molecular fragments, not a bulk polymer dielectric simulation.

# Public inputs and scientific boundaries

Use `data/inputs/EPI1_start.xyz` and `data/inputs/EPI2_start.xyz`. Each XYZ file contains the complete atom list and starting Cartesian coordinates for the named neutral, closed-shell fragment; atom order is the identity key and must be preserved in reported outputs. The coordinates are deliberately displaced starting geometries derived from the SI coordinate tables. No paper or general-web lookup is needed. You may choose software, electronic-structure method, basis, dispersion treatment, conformer strategy, and ESP definition, but state them precisely. The measured quantities are dipole magnitude in Debye, EPI2-minus-EPI1 change and percentage relative to EPI1, and optionally hydroxyl-O ESP in kcal/mol with an explicit surface/point definition. Do not treat bulk Dk, water uptake, FTIR, or Tg as computed outputs.

This is an autonomous-research task. Use the authorized public inputs to investigate the stated scientific objective independently. Do not read hidden evaluator files, private reference calculations, the target paper or its SI, or import their answer structures, rankings or numerical results. Structures explicitly supplied as given objects are authorized for the properties requested here; independently generate any structure that the task asks you to find.

The primary percentage field is percent_change_ePI2_vs_EPI1 = 100*(mu_EPI2 - mu_EPI1)/mu_EPI1, with both dipole magnitudes in Debye. Retain the sign; a decrease is a negative change. An optional positive reduction percentage is a different derived quantity and cannot replace this field. ESP analysis is supplementary; omitting it requires no explanation and does not reduce the core score.

# Required scientific validation/investigation

For each fragment, perform at least one geometry optimization and demonstrate whether the reported structure is a minimum using a vibrational analysis or an equivalently justified stationary-point test. If multiple starting conformers are explored, retain a unique candidate identifier, generation rationale, energy, and validation evidence for every advanced candidate; deduplicate by connectivity and geometry. Compute the two dipoles on geometries that passed your stated validation, using a consistent protocol, and calculate the percent change explicitly. If a calculation fails or no minimum can be established, report that bounded failure with logs and the last validated result rather than inventing a value. Scientific completion requires validated dipoles for both fragments, a reproducible protocol and the signed percentage comparison.

# Deliverables

Submit `report/results.json` conforming to the submission schema. Include fragment identities, method and validation records, dipole values when available, the computed percentage change when both are available, any ESP values and definitions, a conclusion about the polarity change. Attach or reference output geometries, frequency/optimization evidence, and logs using paths relative to the submission root. A bounded-failure branch is valid only when it includes the failed stage, evidence, and the scientifically supported partial comparison.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
