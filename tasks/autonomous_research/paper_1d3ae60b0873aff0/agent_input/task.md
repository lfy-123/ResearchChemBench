# Scientific objective

Determine, from independent computation on the supplied Fe(III)Cl@TCPP cluster, whether its paramagnetic electronic structure can account for the ligand-nucleus 1H and 13C NMR observables associated with Fe@PCN-224 and what local Fe coordination geometry is supported. Formulate the interpretation from the data and calculations rather than relying on an author route or claimed mechanism.

# Public inputs and scientific boundaries

`data/inputs/feiii_cl_tcpp.xyz` is the 86-atom Fe(III)Cl@TCPP Cartesian model from SI Table S14, with fixed atom order, charge -4 and multiplicity 6. The boundary is the isolated cluster, excluding periodic-MOF and solvent effects. The measurement boundary is ligand 1H/13C MAS NMR site shifts and Fe coordination distances; their numerical observations are withheld. Evaluate and identify the three aromatic proton environments (beta, meta, ortho) and eight carbon environments (alpha, beta, meso, ipso, ortho, meta, para, carboxylate carbon) using an explicit atom/site mapping.

# Required scientific validation/investigation

Plan and execute an independent route for geometry, electronic/EPR parameters and isotropic shifts, or justify a valid alternative. Validate charge, spin, convergence, minimum character (or report failure), temperature, site averaging and provenance. Report separate 1H and 13C fit metrics and Fe--N/Fe--Cl distances, and state what the computed evidence does and does not establish about coordination. Completion requires the requested observables or a bounded-failure report containing completed partial results, diagnostics and a concrete reason to stop; stop when the selected route is complete and limitations/sensitivity are documented.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, with provenance, validation, per-site predictions, fit metrics, structural distances, an independently reasoned conclusion and limitations. Do not claim experimental values were computed; distinguish calculated quantities from withheld measurements.
