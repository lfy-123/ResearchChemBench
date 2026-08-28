# Scientific objective

For the fixed neutral singlet molecule in `data/inputs/system.json`, independently compute and interpret its low-lying vertical singlet absorption in tetrahydrofuran. Test the authors' qualitative hypothesis that the lowest bright transition is dominated by donor-to-acceptor π–π* charge transfer involving the benzimidazole–cyanostilbene framework. The scored research object is the molecule, its validated ground-state conformer, states S1–S5, and the first absorption band; aggregation, solid-state packing, emission, and photoproducts are outside scope.

# Public inputs and scientific boundaries

Use the supplied isomeric SMILES, formula C19H15N3O3, neutral charge, singlet multiplicity, E alkene stereochemistry, and neutral 1H-benzimidazole tautomer exactly as specified. Generate 3D structures from this identity. Treat tetrahydrofuran as the bulk solvent using a continuum or another justified bulk-solvent model. The endpoint is vertical singlet excitation from the selected ground-state conformer; do not optimize an excited state. The public file contains no preselected conformer or transition data.

# Required scientific validation/investigation

Generate a finite, chemically distinct conformer set for the supplied identity, document the generation and deduplication criterion, optimize every advanced conformer, and retain the selected conformer only with an energy comparison and minimum/stability evidence (frequency or a justified alternative). Compute at least the first five singlet vertical states and report them as explicitly identified state records (`state`: 1 through 5, in ascending state order), with energies, wavelengths, oscillator strengths, and dominant orbital/configuration character. Validate the leading band by at least one independent numerical or model-sensitivity check and state whether state ordering is stable. The calculation is complete when one selected conformer has documented validation, all five states are available, the leading-band check is reported, and all requested fields are populated. Stop after the finite conformer set has been exhausted and the sensitivity check is complete; if a calculation fails, report the failed branch and scientifically bounded limitation rather than fabricating values.

# Deliverables

Submit `report/results.json` and `report/methods.md`. JSON must contain status, selected conformer identity and validation, a per-conformer evaluation array giving every advanced conformer's identity, relative energy, optimization outcome, and stability evidence, a five-or-more-state array with state number/energy/wavelength/oscillator strength/configuration, ground-state gap, sensitivity check, and a conclusion with limitations. If completion is bounded by a failed calculation, use the explicit bounded-failure branch in the schema and identify the missing observable.
