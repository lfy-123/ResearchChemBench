# Scientific objective

Independently determine how substitutions affect local geometry in Fe-activated ZnAl2O4, comparing three fixed-cell 56-atom periodic models. Establish an evidence-based local-structure conclusion with explicit site assignments, magnetic states and geometry comparisons for the defined fixed cells.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json` and `data/inputs/host_initial.cif`. The latter explicitly lists an unoptimized Zn8Al16O32 normal-spinel host (56 atoms, fixed cubic a=8.08 A); its P1 encoding lists all atoms once. Do not expand it a second time. This is a declared constructed benchmark model, not an exact ICSD export or experimental dilute-doping model.

Replace one Al by Fe in each state. UC-1 is the Fe-activated baseline, not Fe-free: Zn8FeAl15O32. UC-2 is LiZn7FeAl15FO31; UC-3 is LiSiZn6FeAl15FO31. Choose relative sites independently. Li/Si replace parent tetrahedral Zn; F replaces an anion O participating in Al/Fe-centered octahedra, not a "six-coordinate oxygen". Keep each state's exact 56-atom composition and total charge zero. UC-3 has formal ionic bookkeeping +2 and uses neutral-cell electronic compensation; do not add ionic defects or claim that this realizes a different ionic-compensation mechanism. Spin polarization and initial/final moments must be documented; nominal Fe3+ is not proof of its final oxidation state. Relax atomic positions only, at the fixed supplied cell.

No optimized doped coordinates, preferred occupation, numerical target or winner is supplied. Use only the public task files and allowed tools, not the paper/SI, published results or evaluator files. The model does not directly predict experimental phosphor efficiency.

This is an autonomous-research task. Use the authorized public inputs to investigate the stated scientific objective independently. Do not read hidden evaluator files, private reference calculations, the target paper or its SI, or import their answer structures, rankings or numerical results. Structures explicitly supplied as given objects are authorized for the properties requested here; independently generate any structure that the task asks you to find.

# Required scientific validation/investigation

Declare a finite set of relative substitution-site and magnetic hypotheses, deduplicate by stated symmetry/connectivity criteria, retain candidate IDs and explain candidate selection. Advanced candidates require a documented periodic method, electronic and force convergence, fixed-cell/composition checks, and final geometry artifacts. Compare only validated candidates; retain attempted candidates and limits rather than claiming an exhaustive or global-minimum search from one configuration. Complete reporting requires at least one validated candidate for each of UC-1/UC-2/UC-3 and explicit coverage; otherwise report bounded failure with attempts and scientific consequences.

Use the target-independent nominal first-shell algorithm in `system_spec.json`: all four O/F neighbors at parent tetrahedral centers, six at octahedral centers, every shell bond and all neighbor-pair angles. Retain atom IDs, periodic images, next-neighbor distance and any changed coordination. Compare complete label-specific distributions or declared summaries across states. Never select a bond or near-right angle because it matches a paper value. Separate calculated local distortion from uncomputed optical performance and from the real material's ionic compensation or dilute loading.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`, with state composition, total charge, fixed cell, candidate assignments, validated full-shell geometry, artifacts, coverage and a calculation-based conclusion. Include independent hypotheses, discrimination tests and outcomes; do not invent an autonomous discovery narrative.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
