# Scientific objective

Determine, by an independently planned quantum-chemistry investigation, the total dipole-moment magnitude of the explicitly supplied 8OBAF acid and its explicitly supplied 1:1 8OBAF:CNPy hydrogen-bonded complex, and determine whether the supplied complex is more polar than the acid under the stated molecular model. The scored observables are the two dipole magnitudes in Debye and their difference, alongside the structures and validation evidence.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that incorporating 4-cyanopyridine through an O–H⋯N hydrogen bond increases the polarity of 8OBAF, because the cyano-bearing acceptor contributes a strong longitudinal dipole to the supramolecular complex.

**Candidate route or mechanism.**
The relevant comparison is between isolated 8OBAF and a 1:1 8OBAF:4-cyanopyridine hydrogen-bonded pair, with the acid hydroxyl proton directed toward pyridine nitrogen. Treat the proposed polarity increase as a hypothesis to test for the supplied pair.

**Discriminating evidence.**
Compare computed molecular dipole magnitudes for the isolated acid and hydrogen-bonded complex using validated optimized structures, while documenting the hydrogen-bond geometry, dipole extraction, and any conformer sensitivity. The molecular comparison bears on the proposed polarity explanation; bulk dielectric anisotropy is contextual rather than a computational target.

# Public inputs and scientific boundaries

Use only `data/inputs/molecular_systems.json`. It defines the connectivity, names, SMILES, neutral charge and singlet multiplicity of 8OBAF and 4-cyanopyridine, and defines the complex as a 1:1 noncovalent pair with the acid hydroxyl H directed toward pyridine N. Preserve connectivity and do not form a covalent bond. The model boundary is an isolated gas-phase molecule/complex; do not report bulk dielectric anisotropy as the computed dipole. You may generate 3-D geometries and choose computational software and model chemistry, but disclose them fully.

# Required scientific validation/investigation

Construct at least one acid geometry and at least one hydrogen-bonded complex geometry from the supplied identities. If multiple conformers or intermolecular arrangements are explored, retain unique candidate identities and state the deduplication criterion. Optimize the reported structures with a defensible method, verify convergence and a stationary point (frequency analysis or a clearly justified equivalent), and confirm charge/multiplicity and unchanged connectivity. Report hydrogen-bond geometry for the complex, dipole vector or magnitude extraction details, and any conformer sensitivity. A calculation is complete when both named systems have a converged, validated reported structure and dipole, or when a scientifically justified bounded failure is documented with the attempted scope and limitation. Stop after validation of the reported structures and after no unresolved identity, convergence or comparison issue remains; do not claim an exhaustive conformer search unless one was performed.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method, software, charge/multiplicity, structure representation or coordinates, validation evidence, per-system dipoles, the complex-minus-acid difference, and a concise conclusion about whether complexation increases polarity. If unable to obtain a validated result, use the failure branch and state the attempted investigation, reason and limitation rather than fabricating values.
