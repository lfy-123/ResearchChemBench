# Scientific objective

Independently test the authors' qualitative hypothesis that the isolated neutral compound 3-(5-(butylthio)-1H-1,2,4-triazol-3-yl)-2-ethylimidazo[1,2-a]pyridine has a well-defined ground-state minimum whose geometry is broadly consistent with its deposited single-crystal geometry. Determine an optimized molecular structure, HOMO and LUMO energies and their gap, and a reproducible geometry comparison. The scored object is the unique organic molecule in CCDC 2449676, not a crystal packing model.

# Public inputs and scientific boundaries

Use `data/inputs/crystal_record.json` and the controlled CCDC connector for record 2449676. The record must establish connectivity, atom identity, coordinates, formula C15H19N5S, neutral charge and the crystal-reference metadata. The quantum system is one isolated neutral closed-shell molecule in its electronic ground state; no solvent, counterion, protein, periodic crystal, docking or biological inference is requested. You may generate conformers and choose computational methods, but must disclose them. Geometry comparison must use explicitly identified atom mapping and report bond lengths, bond angles and torsions or a clearly defined equivalent plus an overall deviation metric.

# Required scientific validation/investigation

Retrieve and verify the record identity and coordinate completeness before calculation. Generate and deduplicate a finite set of chemically distinct conformers, documenting the generator, duplicate criterion and coverage; for a direct single-start calculation, report that limitation explicitly. Optimize each advanced conformer and perform a stationary-point test appropriate to the method, retaining the lowest validated minimum or reporting bounded failure. Compute HOMO, LUMO and gap for the selected minimum, with units and sign convention. Map the selected molecule to the crystal component and quantify geometry agreement. Completion requires either a validated minimum plus all requested observables and comparison, or a bounded-failure report containing attempted candidates, diagnostics and the next limiting step. Stop when the declared conformer-generation protocol is exhausted and every advanced candidate has either passed validation or been documented as failed; do not claim global conformational completeness beyond the reported coverage.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method/software, input provenance, candidate coverage and deduplication, selected-candidate identity, minimum-validation evidence, HOMO/LUMO/gap, atom mapping, geometry comparison, conclusion and limitations. Numeric values must carry units and enough precision to reproduce the comparison. If the calculation cannot be completed, use the bounded-failure branch and provide truthful diagnostics rather than fabricated observables.
