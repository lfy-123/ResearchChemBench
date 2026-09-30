# Scientific objective

Determine whether substituent-dependent electronic tuning is observed for the two explicitly defined singlet fluorene anions in `data/inputs/system.json`. Independently plan and execute calculations that optimize each anion in a DMSO continuum, verify the optimized structures as minima, and report each Kohn–Sham HOMO energy in eV. The author hypothesis supplied for this reproduction task is that a 9-aryl fluorene anion has a fluorene-centered high-energy occupied orbital and that changing the para aryl substituent can tune that orbital; test this hypothesis without assuming a numerical result or a winning system.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the 9-aryl fluorene anion has a high-energy occupied orbital with substantial fluorene or benzylic character, and that a para electron-withdrawing substituent can stabilize this orbital through electronic communication with the aryl group.

**Candidate route or mechanism.**
For these isolated singlet anions, examine the candidate comparison between the unsubstituted 9-phenyl system (1a−) and the para-CF3 analogue (1e−), including whether their non-planar aryl/fluorene arrangements permit different frontier-orbital localization or energies. Treat the proposed substituent effect as a comparison hypothesis to test.

**Discriminating evidence.**
Use optimized, frequency-validated anion structures and compare their Kohn–Sham HOMO energies and orbital character or spatial distribution. Geometry/conformer sensitivity and consistent DMSO-continuum calculations for both systems provide evidence for or against the proposed tuning.

# Public inputs and scientific boundaries

The two objects are `1a_anion` (9-phenylfluoren-9-yl anion) and `1e_anion` (9-[4-(trifluoromethyl)phenyl]fluoren-9-yl anion), with explicit SMILES, charge −1, and singlet multiplicity in `data/inputs/system.json`. Use the isolated molecules, no counterion, and a DMSO continuum. The scored observable is the HOMO energy for each named object in eV; the validation observable is the presence or absence of imaginary harmonic frequencies at each optimized structure. You may choose software, electronic-structure method, basis, grid, SCF settings, conformer protocol, and solvation implementation, but must state them and preserve the same declared protocol for both systems. The paper and SI are not available as task inputs.

# Required scientific validation/investigation

Generate at least one chemically valid starting geometry per named anion and optimize both without imposing symmetry that changes the connectivity. If multiple conformers or starting orientations are explored, deduplicate by connectivity and a stated geometry criterion, report all retained starts and explain the selection of the final structure for each named object. Run a harmonic frequency calculation (or a clearly justified equivalent stationary-point test) on every reported final structure and identify any imaginary modes. Extract the HOMO from the same validated final wavefunction used for the reported structure. The direct calculation is complete when both named systems have either (a) a converged, validated minimum and a HOMO value with units or (b) a documented bounded failure with the attempted settings, last geometry/status, and failure cause.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include exactly one per-system record for each public ID, in the same order as `data/inputs/system.json`; the `id` field is the binding identity for each record. Include method and solvation details, geometry provenance, convergence status, frequency/minimum evidence, HOMO energy when available. Include a comparison statement describing the direction of the HOMO change only from the submitted values; when a bounded failure prevents a two-value comparison, state that the comparison is unavailable and why. Add a reproducibility note naming software/version and relevant numerical settings. A bounded-failure branch is acceptable only when its required evidence is supplied.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
