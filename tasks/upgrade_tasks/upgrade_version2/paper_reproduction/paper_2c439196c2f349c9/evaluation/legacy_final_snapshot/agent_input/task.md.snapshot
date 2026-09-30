# Scientific objective

Determine the electronic structure of the isolated INP molecule, 2-((E)-(isobutylimino)methyl)-4-((E)-(4-nitrophenyl)diazenyl)phenol. Independently plan and execute a defensible quantum-chemical calculation to obtain a stationary-point geometry, HOMO energy, LUMO energy, and the HOMO-LUMO separation ΔE = E_LUMO − E_HOMO in eV. The authors qualitatively motivate this route as testing the donor/acceptor azo-Schiff-base electronic structure and its relation to nonlinear-optical behavior; test that motivation independently without assuming a published numerical outcome.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors treat INP as a donor–acceptor azo-Schiff-base chromophore: the phenolic hydroxyl is proposed as an electron donor and the nitro-substituted end as an electron acceptor, with the conjugated scaffold supporting intramolecular charge-transfer character. They relate the frontier-orbital separation to an insulator-like, limited-electronic-polarizability interpretation, while attributing the strong continuous-wave nonlinear-optical response mainly to thermal effects rather than purely electronic response.

**Candidate route or mechanism.**
The relevant candidate explanation is a delocalized donor-to-acceptor frontier electronic structure across the conjugated azo-Schiff-base framework, with the HOMO and LUMO sampling opposite donor/acceptor regions. Treat this as the proposed electronic-structure picture to examine, rather than as an established result.

**Discriminating evidence.**
Use the optimized neutral-singlet geometry and its frequency validation together with the computed HOMO and LUMO energies, their LUMO-minus-HOMO separation, and—where the chosen calculation provides it—the spatial character of the frontier orbitals. These observations can test the proposed donor–acceptor picture and the limited-polarizability interpretation, while keeping the conclusion confined to the isolated-molecule descriptor.

# Public inputs and scientific boundaries

Use `data/inputs/inp_molecule.json` as the complete molecular identity: it gives connectivity, formula, E configurations, charge 0, singlet multiplicity 1, and the isolated-molecule boundary. Do not add solvent, counterions, crystal packing, polymer, or an excited-state model. The scored observables for a completed calculation are the submitted HOMO and LUMO orbital energies in atomic units, their derived gap in eV, and the validation status of the optimized stationary point. A bounded-failure submission may truthfully leave unavailable numerical observables null and must document the attempted work and observed failure. The optical interpretation is a molecular orbital descriptor, not an experimental or solid-state band gap.

# Required scientific validation/investigation

Choose and document a reproducible electronic-structure method, geometry-search strategy, convergence settings, and software. Generate at least one chemically valid initial geometry, optimize it, and perform a vibrational/stationary-point check. Advance a geometry only if the optimization converges, the connectivity and charge/multiplicity remain those specified, and the reported frequency evidence supports a local minimum (or explicitly report bounded failure). Compute HOMO and LUMO on the validated geometry and independently recompute ΔE from the submitted orbital energies using 1 hartree = 27.2114 eV. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the molecular identity used, method/software and convergence provenance, optimized geometry or a path to it (or explicitly state that none was produced), frequency validation, HOMO/LUMO and derived gap when completed, calculation status, candidate records, and a conclusion linking the computed descriptor to the stated electronic-structure question. For bounded failure, do not fabricate numbers or structures: use null for unavailable frontier values and provide the failure reason, attempted steps. Numeric values must carry units and enough precision to reproduce the reported arithmetic.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
