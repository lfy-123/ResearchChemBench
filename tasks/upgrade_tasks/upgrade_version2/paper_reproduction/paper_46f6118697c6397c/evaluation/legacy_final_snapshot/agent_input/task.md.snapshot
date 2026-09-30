# Scientific objective

For the fixed neutral tetra(triflate) derivative identified below (compound 2), compute the dominant singlet vertical UV-vis excitation and its oscillator strength in a dichloromethane continuum. The research object is the complete molecule and its electronic excited states, not the crystal packing or an experimental spectrum.

# Author-provided scientific guidance

Independently plan and execute a computational test of the authors' qualitative proposal that boron substitution controls the N6-centred pi electronic system in boron-bridged hexazenes. Use the authors' qualitative route as a hypothesis to test, but choose and justify your own software, model chemistry, geometry protocol and state-selection procedure.

# Public inputs and scientific boundaries

Use `data/inputs/ccdc_record.json` and the supplied immutable CCDC file `data/inputs/ccdc_2512981.cif` directly. The CCDC record number is provenance only; CCDC database retrieval is not required or scored. The declared target is compound 2, the neutral tetra(triflate) boron-bridged B2N6 hexazene with formula C18H14B2F12N6O12S4, charge 0 and singlet multiplicity 1. Before calculation, verify the CIF's internal archive ID, formula, element set, occupancy, cell, connectivity, B2N6 core and all four B-O-SO2CF3 substituents. Select one complete crystallographic compound-2 component, resolve symmetry and any crystallographic disorder deterministically, remove only noncovalently associated crystallographic solvent if present, and preserve all four triflate substituents. Do not delete triflate groups, edit elements or invent hydrogens to simplify the target. If a complete chemically consistent component cannot be recovered, preserve the raw file and report a bounded identity/preprocessing failure. The target endpoint is a vertical singlet excitation energy (eV) and oscillator strength from the optimized ground-state molecule with dichloromethane represented by a stated continuum or equivalent solvation treatment. Crystal packing, emission, electrochemistry and experimental wavelengths are outside the scored endpoint. Do not use the paper, SI or general web as a computational answer source.

# Required scientific validation/investigation

Report the complete independent route and software/model choices. Establish that the complete compound-2 molecular identity, charge and multiplicity are correct; show optimization convergence and state whether a frequency/Hessian check was performed. Generate enough low-lying singlet states to identify the state carrying the dominant oscillator strength in the near-UV/visible state list, retain its state index, energy, wavelength if available, oscillator strength and principal orbital-transition character, and show the neighboring states or another reproducible basis for calling it dominant. The calculation is complete when the optimized structure passes the stated convergence test and the reported state list is sufficient to make the dominant-state selection reproducible. Report the disorder treatment and the conformers or starting structures actually used.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. It must contain either a completed result with identity, route, convergence, state evidence, dominant excitation, or a truthful bounded-failure branch with stage-specific diagnostics and no fabricated endpoint values. Include provenance for the supplied CIF and deterministic preprocessing.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
