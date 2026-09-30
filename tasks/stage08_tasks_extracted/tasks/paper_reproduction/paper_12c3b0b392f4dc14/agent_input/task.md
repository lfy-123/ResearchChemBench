# Scientific objective

For the neutral compound 3-(5-(butylthio)-1H-1,2,4-triazol-3-yl)-2-ethylimidazo[1,2-a]pyridine, independently determine a validated ground-state molecular structure and its HOMO, LUMO and frontier-orbital gap, then test agreement with the deposited single-crystal geometry. The scored object is the unique organic molecule in CCDC 2449676.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that a gas-phase DFT treatment of this isolated neutral heteroaromatic molecule yields a stable optimized ground-state structure broadly consistent with the deposited single-crystal geometry. They use the frontier-orbital gap as a qualitative descriptor associated with chemical stability.

**Candidate route or mechanism.**
For reproduction, examine a conformer-search-and-refinement route: generate candidate conformers with a molecular-mechanics search, optimize them in the neutral ground state with gas-phase DFT, and identify the lowest validated minimum using relative thermochemistry as a comparison aid. Use the optimized minimum for frontier-orbital analysis and comparison to the crystal component.

**Discriminating evidence.**
The relevant evidence is stationary-point validation by vibrational analysis, conformer coverage and relative energies or Gibbs energies, HOMO and LUMO energies with their gap, and mapped comparisons of bond lengths, bond angles and torsions between the optimized molecule and the deposited geometry. Treat the structural agreement and stability interpretation as qualitative, model-bounded claims.

# Public inputs and scientific boundaries

Use `data/inputs/crystal_record.json` and the controlled CCDC connector for record 2449676. The record must establish connectivity, atom identity, coordinates, formula C15H19N5S, neutral charge and crystal-reference metadata. The quantum system is one isolated neutral closed-shell molecule in its electronic ground state; no solvent, counterion, protein, periodic crystal, docking or biological inference is requested. Choose and disclose the computational model, conformer strategy and geometry-comparison metric; do not assume a paper-specific protocol.

# Required scientific validation/investigation

Retrieve and verify the record identity and coordinate completeness before calculation. Generate and deduplicate a finite set of chemically distinct conformers, documenting the generator, duplicate criterion and coverage; for a single-start calculation, report that limitation. Optimize each advanced conformer and perform a stationary-point test appropriate to the method, retaining the lowest validated minimum or reporting bounded failure. Compute HOMO, LUMO and gap for the selected minimum, with units and sign convention. Map the selected molecule to the crystal component and quantify geometry agreement. Completion requires either a validated minimum plus all requested observables and comparison, or a bounded-failure report containing attempted candidates, diagnostics and the next limiting step. Stop when the declared conformer-generation protocol is exhausted and every advanced candidate has either passed validation or been documented as failed; do not claim global conformational completeness beyond reported coverage.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method/software, input provenance, candidate coverage and deduplication, selected-candidate identity, minimum-validation evidence, HOMO/LUMO/gap, atom mapping, geometry comparison, conclusion and limitations. Numeric values must carry units and enough precision to reproduce the comparison. If the calculation cannot be completed, use the bounded-failure branch and provide truthful diagnostics rather than fabricated observables.
