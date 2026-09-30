# Scientific objective

Independently determine the isolated-molecule vertical emission wavelengths for the lowest singlet excited state S1→S0 and lowest triplet excited state T1→S0 of neutral mononuclear copper(I) complex 2, [CuI(L)(PPh3)2], with L = 2-phenyl-5-(4-pyridyl)-1,3,4-oxadiazole. Use the crystallographic complex as the starting molecular identity, omit the co-crystallized methanol, and independently choose and justify the computational route. Do not assume that a solid-state emission maximum equals an isolated-molecule vertical emission.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the emissive lowest singlet and triplet states have mixed metal/halide-to-ligand charge-transfer ((M+X)LCT) character, with Cu(I) and iodide donor contributions and ligand-centered acceptor character.

**Candidate route or mechanism.**
The authors considered relaxation of the lowest singlet and triplet excited states of the isolated neutral complex from the crystallographic molecular structure, followed by assigning each emissive state through its electronic transition character. The candidate state change is donor-to-ligand charge transfer involving the Cu/I unit and the oxadiazole-pyridyl ligand.

**Discriminating evidence.**
Use optimized S1 and T1 geometries, state tracking, and orbital or transition-density analysis such as NTOs to distinguish mixed Cu/iodide-to-ligand charge transfer from alternative localization. Compare the resulting vertical emission energies with the state assignments while treating solid-state emission only as context.

# Public inputs and scientific boundaries

The public input `data/inputs/complex_2_record.json` identifies CCDC record 2498911 (DOI 10.5517/ccdc.csd.cc2pwb1z), formula C49H40CuIN3OP2·CH4O, and the neutral complex unit [CuI(L)(PPh3)2]. Retrieve that record through the allowed CCDC/CSD connector, select one complex molecule, remove methanol, and retain the stated connectivity, charge 0, and S0 multiplicity 1. S1 means the lowest singlet excited state and T1 the lowest triplet excited state of that isolated molecule. The scored observables are the two vertical emission wavelengths in nm, calculated from optimized excited-state structures and identified transitions. Crystal packing, solvent environment, and the experimental solid-state peak are contextual only and are not the computational endpoint.

# Required scientific validation/investigation

Generate and retain a documented S0 structure, an S1 structure, and a T1 structure. Verify that each optimized structure is a stationary minimum or otherwise report the failed optimization and the best converged state with diagnostics. Track the intended S1 and T1 states from the initial excitation through optimization; report state identity, spin, and any root/state crossings. For each state, provide an orbital or transition-density analysis (NTOs or a justified equivalent) that identifies donor and acceptor regions and explicitly discusses Cu, I, ligand, and phosphine contributions. Compute the two vertical emission energies/wavelengths at the reported state geometries, state the exact method/basis/relativistic treatment/solvation and conversion used, and provide reproducibility artifacts or logs sufficient to audit the values. Independently check sensitivity or numerical stability enough to identify whether the reported assignment or wavelengths are fragile. The calculation is complete when both endpoints have converged structures, state tracking, vertical wavelengths, and character evidence, or when a bounded failure report documents which endpoint could not be obtained, why, what alternatives were attempted, and the resulting limitation. Stop after the stated route and any pre-declared sensitivity checks are exhausted; do not continue an unbounded method or conformer search. If multiple starting conformers are used, deduplicate them by a stated structural criterion and report coverage and selection rationale.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus the listed structure, analysis, and provenance files. The JSON must include the two wavelength values when available, explicit state/geometry validation, charge and multiplicity, state-character evidence, method details, and a conclusion. A bounded-failure branch is valid only if it names the missing endpoint and includes diagnostics, attempted alternatives, and limitations. Include no claims of agreement based solely on the experimental solid-state spectrum.
