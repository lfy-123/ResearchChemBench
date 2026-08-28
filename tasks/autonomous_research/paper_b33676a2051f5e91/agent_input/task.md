# Scientific objective

Determine computationally whether the supplied neutral alkoxy radical Int-3 has a kinetically accessible beta-scission channel to a ketone and alkyl radical, and quantify the activation free energy of the best-supported channel. Discover and discriminate plausible cleavage channels independently; do not assume any author mechanism or preferred product. The research object is the isolated molecular radical step, not polymer-scale conversion.

# Public inputs and scientific boundaries

`data/inputs/int3.xyz` is the SI-defined 24-atom Cartesian geometry of neutral doublet alkoxy radical Int-3. Preserve its atom identities, connectivity, charge and multiplicity. Products must be atom-balanced fragments formed by cleavage of the alkoxy radical; assign explicit structures, charge and spin for every reported channel. No transition-state geometry, product geometry, energy, reference value, method or paper route is public. Report energies in kcal mol−1 and state all method, solvent, thermal and spin choices.

# Required scientific validation/investigation

Propose a finite, chemically justified set of distinct beta-scission hypotheses, generate and deduplicate reactant conformers, products and TS guesses, and retain atom mapping for each candidate. Optimize candidates and validate every claimed minimum/TS by frequencies: zero imaginary modes for minima and exactly one for a TS. Show that each advanced TS connects the same reactant to its explicitly reported products using IRC, a relaxed path, or a justified equivalent. Compare validated channels on a common free-energy convention, identify the best-supported channel without relying on an unpublished target, and report search coverage and limitations. Completion requires at least one validated channel or a bounded-failure record with candidate-level outcomes; stop when the declared hypothesis/conformer/TS search is exhausted or further searches yield no distinct validated channel, and state the stopping basis.

# Deliverables

Submit `report/results.json` conforming to the schema. Include an array of candidate channels with structures/identities, validation evidence and energies, selected conclusion, method details, coverage and limitations. A bounded-failure branch must list attempted candidates and explain why no validated channel was obtained.
