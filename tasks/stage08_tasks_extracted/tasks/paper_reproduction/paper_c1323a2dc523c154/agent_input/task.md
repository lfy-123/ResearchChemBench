# Scientific objective

Independently compute and validate the nonresonant Pd 4d-to-2p X-ray emission spectrum of the neutral singlet Pd2Cl6 molecular unit. Determine the reproducible spectral features and infer, from transition- and orbital-level evidence, which electronic interactions produce them.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that several Pd–Cl-involving valence transitions can produce a broad lower-energy shoulder. Their interpretation links this to the chloride coordination symmetry and the number and energies of filled chloride valence orbitals available for mixing with Pd d orbitals.

**Candidate route or mechanism.**
Consider multiple occupied orbitals formed through chloride σ- and π-donation and Pd d mixing as candidate contributors distributed across the shoulder region. The authors invoke a D2h coordination environment, where inversion symmetry restricts dipole-allowed contributions; transition intensity may therefore depend on both Pd d character and donor-to-core transition dipole matrix elements.

**Discriminating evidence.**
Use relativistic DFT-based XES transition energies and intensities, broadened spectra, and donor-orbital analysis. Group transitions by spectral feature and examine their Pd d/Cl p composition and intensity contributions to test whether multiple Pd–Cl-mixed orbitals account for the shoulder.

# Public inputs and scientific boundaries

Use `data/inputs/pd2cl6_neutral_singlet.xyz`, an eight-atom fixed starting geometry containing two Pd and six Cl atoms. Treat it as total charge 0 and multiplicity 1. The research object is this isolated molecular unit; periodic packing, counterions, explicit solvent, thermal disorder, and experimental apparatus simulation are outside scope. Measure raw and, if used, calibrated transition energies, transition intensities, a normalized broadened spectrum spanning the complete main line and low-energy side, feature centers and relative intensities, and donor-orbital composition. Keep raw energies separate from any empirical or reference alignment.

# Required scientific validation/investigation

Select and justify an electronic-structure/XES approach suitable for Pd, including relativistic treatment, basis/ECP, charge, multiplicity, and intensity formalism. Validate the supplied geometry by optimization plus a minimum check, or demonstrate spectrum insensitivity between the fixed and independently optimized geometries. Report Pd–Pd and all six nearest Pd–Cl distances for the geometry used. Preserve a transition table with stable IDs, raw and aligned energies, intensities, donor-orbital identity, and quantitative or defensible qualitative Pd d/Cl p composition. Regenerate the plotted spectrum from that table with a declared kernel and width. Propose explanations for each resolved feature from the computed evidence, discriminate them using orbital composition and transition grouping, and test at least one sensitivity that could change feature identity or assignment.

Completion requires a converged and physically interpretable calculation, geometry validation, transition-resolved spectrum, resolved-feature inventory, evidence-based interaction assignments, and explicit uncertainty/limitations. Stop when further reasonable refinement does not change feature existence or assignments within the declared spectral resolution. If two materially different defensible calculation attempts fail to produce a usable spectrum, stop as a bounded failure and submit the attempts, diagnostics, partial geometry/transition evidence, and only conclusions supported by those partial results.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. It must identify the input, model, outcome status, geometry validation, transition provenance, spectrum construction, feature measurements, interaction assignments, sensitivity test, and limitations. A successful result includes the complete transition array and sampled normalized spectrum. A bounded failure includes attempted models, diagnostics, available geometry/transition evidence, and a truthful limitation conclusion without invented values.
