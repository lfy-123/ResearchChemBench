# Scientific objective

Independently plan and execute a defensible electronic-structure calculation for neutral singlet compound 2a using the supplied structure. Determine the HOMO and LUMO energies, their gap, and the lowest reported vertical singlet excitation energy and wavelength. In the discussion, test the authors' qualitative proposal that the arene-fusion/orbital arrangement produces a stabilized acceptor orbital and that the lowest absorption is principally a frontier-orbital transition; do not assume that proposal is correct.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the arene-fusion pattern controls acceptor-orbital stabilization and the frontier-orbital gap. Their structure–property interpretation links the naphthyl C–B fusion in 2a to these electronic effects.

**Candidate route or mechanism.**
Test the proposed assignment of the lowest-energy singlet absorption as principally a HOMO→LUMO excitation, using the computed orbital character and contributions to assess that assignment.

**Discriminating evidence.**
The authors use ground-state DFT orbital energies and electron-density distributions together with TD-DFT vertical singlet energies, oscillator strengths, and orbital-configuration contributions. Relating the frontier gap to the lowest singlet excitation and inspecting the contributing orbitals provides evidence for assessing the proposed absorption origin.

# Public inputs and scientific boundaries

The object is C(1),B(3)-(naphthalene-1,8-diyl)-C(2)-phenyl-1,2-dicarba-closo-dodecaborane (2a), formula C18H20B10, charge 0, multiplicity 1. Use `data/inputs/2a.xyz` exactly as the starting ordered Cartesian structure and `data/inputs/system.json` for identity and boundary. The calculation concerns an isolated molecule; implicit solvent is optional, but solvent/model choices must be stated. Do not infer solid-state packing, experimental emission, or a different protonation/isotopologue. The measured quantities are orbital energies/gap and vertical singlet excitation energies, wavelengths, oscillator strengths, and dominant orbital contributions.

# Required scientific validation/investigation

Choose and disclose software, electronic-structure method, basis, solvent treatment, geometry protocol, and excited-state protocol. Optimize the ground state (or justify a fixed-geometry alternative), verify charge/multiplicity and absence of an obvious optimization failure, and establish that the reported excitation is a vertical singlet from the stated reference geometry. Deduplicate repeated states and identify the state by energy, wavelength, oscillator strength, and transition contributions rather than by an arbitrary internal label. Report convergence evidence and at least one sensitivity or uncertainty check. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include the structure identity, method, geometry/convergence evidence, orbital energies and gap, an array of singlet excitations with energy/wavelength/oscillator strength and contributions, the selected lowest-singlet record, validation checks, author-hypothesis assessment, conclusion. Include units for every numerical quantity and enough provenance to reproduce the calculation.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.

# Partial or unsuccessful submission

Use `status: "partial"` or `status: "bounded_failure"` when required calculations or analyses remain unavailable. Retain all actual partial results in their original fields. Include `failure` with a nonempty `reason`, a nonempty `missing_observables` array naming the unavailable result fields, and an `evidence` array of existing input, output or diagnostic paths (empty only if no artifact was produced). Explain which calculation failed or was not attempted; do not invent output files.

For these two statuses, the schema permits `null` for the specified unavailable calculated values, selected structures, state assignments or output paths. Keep the known molecular identities, charges, multiplicities, units and attempted methods. Report actual counts, including zero generated/validated candidates when appropriate. An unavailable frequency result is `null`, not zero imaginary modes or an empty list claiming a completed frequency analysis. A genuinely computed zero or an established empty imaginary-mode list remains valid evidence. A missing comparison is not a zero difference or zero RMSE.

Other statuses, and omission of status where the original schema permits it, retain the complete-result format. Passing this format check does not establish scientific completion: uncomputed endpoints receive no completion credit, and existing scientific rules still assess the actual evidence. This reporting branch does not change the scientific target, required successful investigation, or numerical acceptance criteria.
