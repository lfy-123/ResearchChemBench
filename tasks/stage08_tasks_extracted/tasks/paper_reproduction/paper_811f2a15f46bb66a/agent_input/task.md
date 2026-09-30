# Scientific objective

Establish how one H atom changes hydrogen-incorporation energetics, oxygen-abstraction energetics, and H electronic character in bulk fluorite CeO2, CeO2 with one Ce replaced by Pr, and CeO2 with one Ce replaced by Gd. Independently formulate and discriminate plausible explanations for any composition-dependent behavior using computed energies, local structures, and charge analysis. Report E_H, E_Oabs before and after H, ΔE_Oabs, H Bader charge, local H coordination, and a supported conclusion.


## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that hydrogen incorporation and the resulting oxygen-abstraction response differ among undoped, Pr-substituted, and Gd-substituted ceria, with dopant-organized hydrogen incorporation affecting nearby oxygen stability.

**Candidate route or mechanism.**
Compare hydrogen in the stoichiometric lattice with hydrogen-containing oxygen-vacancy states, and examine whether the local hydrogen environment and electronic character are associated with facilitated oxygen removal, oxygen stabilization, or little change across the three compositions. The authors discuss a hydridic-like character for H in undoped ceria and a more protic-like character in the doped systems as candidate interpretations.

**Discriminating evidence.**
Use the common hydrogen-incorporation and oxygen-abstraction energies, especially the change in oxygen-abstraction energy upon adding H, together with optimized local H coordination, local structures, and H Bader charge. Candidate bonding or electronic interpretations can be supported further by charge or density based analysis when available.

# Public inputs and scientific boundaries

Use `data/inputs/structure_spec.json` and `reference_definitions.json`. Each host is a periodic 2x2x1 conventional fluorite cell (48 atoms, 16 cations and 32 O atoms) with a=5.41 Å; Pr or Gd replaces the cation at fractional supercell coordinate (0,0,0). Preserve composition and the named site in every derived state. Consider one H atom in the stoichiometric cell and one O vacancy in a separate H-free and H-containing family. Use isolated neutral H and O atoms as references, and state charge/multiplicity and all electronic-structure choices. No surfaces, solvent, finite-temperature correction, electrochemical potential, or external literature search is part of this task.

# Required scientific validation/investigation

Propose plausible competing explanations before selecting a conclusion, then generate a finite, explicitly described set of chemically distinct H placements and O-vacancy placements for each composition. Deduplicate by periodic structure and composition, relax retained candidates, and record convergence. Advance a candidate only when its geometry optimization and electronic calculation converge; report failed candidates. Select the lowest-energy converged candidate under your stated criteria, retain the candidate list and selection evidence, and distinguish computed findings from hypotheses. Compute all energies with the supplied definitions and common conventions. Validate atom counts, dopant identity, vacancy identity, H identity, charge analysis, and at least one sensitivity or limitation check. Complete when all three compositions have a converged host, selected H state, H-free vacancy state, H-containing vacancy state, isolated references, charge analysis, and a discriminating conclusion, or provide a bounded failure report. Stop after the declared candidate space is exhausted and no unreported candidate class remains; report coverage and limitations.

# Deliverables

Submit `report/results.json` and any supporting files. JSON must contain `status` (`complete` or `bounded_failure`), `hypotheses`, `systems` with one object for each named composition, candidate/validation records, energies in eV, ΔE_Oabs in eV, H charge in e, local geometry, `conclusion` plus `limitations`. A bounded failure must identify missing states and still report every successfully computed observable; do not fabricate numbers.
