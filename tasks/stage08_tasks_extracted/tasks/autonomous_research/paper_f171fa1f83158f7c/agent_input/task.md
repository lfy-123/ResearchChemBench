# Scientific objective

Determine the absolute configuration of clathriamine A (1) from independent computational ECD analysis of the supplied molecular model and measured solution spectrum. Generate and test your own plausible stereochemical explanations using calculations and validation. Report an assignment or a scientifically justified inconclusive result.

# Public inputs and scientific boundaries

The research object is the C22H20Br2N8 clathriamine A connectivity represented by `data/inputs/conformer_2.xyz` and `data/inputs/conformer_3.xyz`, each with charge +2 and singlet multiplicity. Treat the atom ordering and Cartesian coordinates in each file as the identity of public starting geometries A and B; independently determine and document the stereochemical identity rather than relying on a filename or comment. The solvent is methanol. `data/inputs/experimental_ecd_sign_anchors.json` gives four measured ECD sign anchors in nm for the natural product. You may generate stereochemical alternatives by an explicitly described atom-mapped transformation and may optimize, sample conformers, compute excited states and build broadened spectra. The scored endpoint is a validated ECD-based configuration conclusion and its limitations.

# Required scientific validation/investigation

State and justify the hypotheses you generate and test. Define a reproducible candidate-generation rule, preserve candidate identity and atom mapping, deduplicate candidates with a stated criterion, and record which candidates advance. For every advanced candidate, verify atom count, charge, multiplicity, connectivity and stereochemistry, validate optimized structures/frequencies or an honest alternative, calculate excited states covering 200–300 nm, and construct a population-weighted prediction. Compare each prediction with every experimental anchor and the broad pattern; include at least one method or conformer sensitivity check. Completion requires validated coverage of every advanced hypothesis and a conclusion whose sign/pattern is stable under the reported sensitivity checks. Stop when that stability is demonstrated and new candidates/sensitivity tests are unlikely to change the conclusion, or report a bounded inconclusive outcome with the untested space and stopping reason.

# Deliverables

Write `report/results.json` conforming to the local `submission_schema.json`. Include candidate identities and validation context, predicted spectral features, anchor-by-anchor comparison, final assignment/inconclusive status, uncertainty, sensitivity analysis and stopping rationale. Use the fields defined by the local schema, including its mode-specific requirements. Any failure or partial discovery must be represented truthfully rather than replaced by fabricated numeric values.
