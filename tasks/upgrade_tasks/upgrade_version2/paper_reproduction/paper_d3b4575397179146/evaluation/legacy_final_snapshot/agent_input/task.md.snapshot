# Scientific objective

Independently plan and execute a computational test of the authors' qualitative explanation for the optical properties of the four explicitly identified triaryl-heptazines in `data/inputs/heptazines.json`. For each molecule, determine a validated neutral-singlet ground-state structure, vertical singlet excitations, oscillator strengths and dominant orbital contributions, then test whether the reported visible-band assignment and frontier-orbital localization are supported. The authors' qualitative hypothesis is that substituent-controlled frontier orbitals produce distinct weak visible transitions; independently test this hypothesis without assuming any numerical result or winning state.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that substituent-controlled frontier orbitals account for distinct weak visible transitions in this triaryl-heptazine series. Their interpretation distinguishes derivatives whose frontier density remains chiefly associated with the heptazine nitrogen core from a dimethoxy-substituted derivative in which the highest occupied density is shifted toward the aryl substituents. They further associate the relevant weak visible band with a frontier-orbital excitation for the fluoro-, chloro-, and methyl-substituted members, while proposing a lower occupied orbital to LUMO excitation for the dimethoxy member.

**Candidate route or mechanism.**
Test a substituent-dependent electronic-state assignment across the four molecules: compare core- versus aryl-localized HOMO/LUMO density, then examine whether the selected weak visible transition is dominated by HOMO→LUMO or instead by a lower occupied orbital→LUMO contribution. Treat these as candidate assignments to be checked on the independently obtained structures and excited states.

**Discriminating evidence.**
Use validated optimized neutral-singlet geometries, low-lying vertical singlet energies and wavelengths, oscillator strengths, dominant orbital contributions, and a reproducible orbital-density localization analysis. Compare the assignment and localization trends across all four compounds; the calculations should determine whether the proposed state character is supported.

# Public inputs and scientific boundaries

The four systems are identified by stable local IDs, complete names, formulas, SMILES, charge 0 and multiplicity 1 in the input JSON. Use those structures as the molecular identity; do not infer alternative protonation, connectivity or atom mapping. The physical system is an isolated molecule with implicit acetonitrile solvation. The measured quantities are ground-state minimum validation, vertical singlet excitation energies/wavelengths, oscillator strengths, dominant orbital transitions, and qualitative spatial localization of HOMO/LUMO (and any orbitals needed for the selected band). Solid-state packing, vibronic structure, fluorescence lifetimes, catalytic yields and reaction mechanisms are outside scope. The author route may be considered as a qualitative hypothesis, but paper-specific software, model chemistry, ordered protocol, numerical tables and answer-bearing orbital figures are not supplied.

# Required scientific validation/investigation

For all four named molecules, choose and document a defensible electronic-structure workflow. Generate or optimize at least one 3-D conformer per molecule, retain the conformer actually used, and report charge, multiplicity, convergence and whether a frequency analysis supports a minimum (or explicitly report a bounded failure). Calculate enough low-lying singlet states to cover the first visible/near-visible absorption and report state number, energy, wavelength, oscillator strength and dominant orbital contributions. Define visible as 380–700 nm and state how the band is selected when multiple states occur. Inspect orbital densities using a stated reproducible criterion and identify whether HOMO and LUMO density is primarily on the heptazine core or peripheral aryl substituents. Deduplicate equivalent states only when the submitted evidence explains the criterion. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include per-system structures and validation, transitions, orbital-localization observations, comparison to the qualitative hypothesis, computational provenance. Include enough evidence paths or excerpts from the agent's own outputs to make each object-specific claim auditable. Do not reproduce the paper or SI as a substitute for calculations.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
