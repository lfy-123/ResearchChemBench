# Scientific objective

For the neutral compound 3-(5-(butylthio)-1H-1,2,4-triazol-3-yl)-2-ethylimidazo[1,2-a]pyridine, independently determine a validated ground-state molecular structure and its HOMO, LUMO and frontier-orbital gap, then test agreement with the deposited single-crystal geometry. The scored object is the unique organic molecule in CCDC 2449676.

# Public inputs and scientific boundaries

Use `data/inputs/crystal_record.json` and the supplied immutable `data/inputs/ccdc_2449676.cif`. The CCDC record number is provenance only; CCDC database retrieval is not required or scored. The CIF must establish connectivity, atom identity, coordinates, formula C15H19N5S, neutral charge and crystal-reference metadata. The quantum system is one isolated neutral closed-shell molecule in its electronic ground state; no solvent, counterion, protein, periodic crystal, docking or biological inference is requested. Choose and disclose the computational model, conformer strategy and geometry-comparison metric; do not assume a paper-specific protocol.

# Required scientific validation/investigation

Read and verify the supplied CIF identity and coordinate completeness before calculation. Generate and deduplicate a finite set of chemically distinct conformers, documenting the generator, duplicate criterion and coverage; for a single-start calculation, report that limitation. Optimize each advanced conformer and perform a stationary-point test appropriate to the method, retaining the lowest validated minimum or reporting bounded failure. Compute HOMO, LUMO and gap for the selected minimum, with units and sign convention. Map the selected molecule to the crystal component and quantify geometry agreement. Completion requires either a validated minimum plus all requested observables and comparison, or a bounded-failure report containing attempted candidates, diagnostics and the next limiting step. Stop when the declared conformer-generation protocol is exhausted and every advanced candidate has either passed validation or been documented as failed; do not claim global conformational completeness beyond reported coverage.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method/software, input provenance, candidate coverage and deduplication, selected-candidate identity, minimum-validation evidence, HOMO/LUMO/gap, atom mapping, geometry comparison, conclusion and limitations. Numeric values must carry units and enough precision to reproduce the comparison. If the calculation cannot be completed, use the bounded-failure branch and provide truthful diagnostics rather than fabricated observables.
