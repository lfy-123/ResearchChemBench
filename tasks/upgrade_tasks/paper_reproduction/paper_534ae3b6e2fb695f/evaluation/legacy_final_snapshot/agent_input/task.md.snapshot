# Scientific objective

Test the authors' multidescriptor reactivity hypothesis for ODA, 6FODA and PFMB toward TMC. Report the global nucleophilicity index, independently defined amine-local descriptors and optimized molecular geometry observables; analyze agreement or disagreement within the gas-phase model.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the three diamines share a common nucleophilic reactivity ordering toward TMC. They interpret local ionization based descriptors as the primary indicators, with electrostatic potential as complementary evidence.

**Candidate route or mechanism.**
The proposed comparison is direct amine attack at the TMC acyl chloride functionality, assessed through the electronic properties of the diamine nitrogen sites. The authors consider a multi-descriptor interpretation combining average local ionization energy or a related nucleophilicity index with electrostatic potential, frontier orbital information, and the conformational state of each diamine.

**Discriminating evidence.**
Compute and compare nitrogen mapped local descriptors, including local ionization or nucleophilicity measures and electrostatic potential, together with frontier orbital indicators where feasible. Use optimized isolated-molecule geometries and the specified inter-benzene dihedral definition; assess equivalent amine sites and conformational or method sensitivity to determine whether the descriptors support or conflict with the proposed ordering.

# Public inputs and scientific boundaries

Use `data/inputs/monomers.json` for the neutral singlet identities and atom-mapped graphs of ODA, 6FODA, PFMB and TMC, and `data/inputs/observable_definitions.json` for the measurement conventions. Generate conformers independently. Preserve connectivity/protonation; the two fluorinated diamines each have two CF3 groups. The comparison is isolated gas-phase diamines; TMC is the reaction-context partner, not a fourth member of their ranking. TMC optimization and a TMC inter-ring angle are not required.

The primary global index is `N_global = HOMO(diamine) - HOMO(TCE)`, in eV, using the declared fixed TCE reference of -9.1212 eV and comparable B3LYP/def2-TZVP HOMOs on B3LYP-D3BJ/def2-SVP stationary geometries. This is a common measurement scale, not a supplied molecular result or ranking. Other methods may inform exploration/sensitivity but must be reported separately. A local descriptor is a separate observable and cannot replace this index. Vertical charged electron-removal/addition probes are permitted for local descriptors at the neutral geometry; they do not change the neutral-singlet target identity.

Use only the public files and allowed tools, not paper/SI documents, web searches, optimized author coordinates, reference values or evaluator conclusions. Do not extrapolate this isolated-molecule comparison to computed membrane performance, solvent effects or experimental kinetic constants.

# Required scientific validation/investigation

Construct a finite, deduplicated conformer set for each diamine (or justify a single start), independently optimize the candidates and validate stationary geometry, connectivity and electronic convergence. Record candidate selection and any numerical-sensitivity results. For each selected validated geometry, report its neutral HOMO and global index on the defined scale, plus at least one consistently defined local descriptor at both mapped amine N sites, with units, formula, population/sampling convention and artifact evidence. Analyze equivalent-site asymmetry and conflicting descriptor rankings instead of silently exchanging scales.

Report the acute least-squares angle between the two mapped aromatic ring planes, plane-fit residuals, and all separately mapped continuous linker torsions. Use the supplied atom maps and sign convention; PFMB's central linker is the bond between mapped atoms 3 and 12. A four-atom torsion is not the ring-plane angle. Include final geometry and an output-index-to-map-ID mapping so every geometry observable can be independently re-extracted.

Completion requires all three diamines' validated observables and exactly one record per supplied molecule. TMC uses `context_only`; a failed diamine uses `bounded_failure` with attempted evidence and consequences. Report the ordering implied by each descriptor and the overall conclusion supported by those computed descriptors; do not fabricate missing quantities or claim an unperformed exhaustive search.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, including methods, conformer/validation evidence, identity-bound global and local quantities, mapped ring-plane angles and linker torsions, ordering. Cite final geometries, neutral/probe electronic outputs and extraction artifacts. These data, not a remembered ranking, must support the conclusion.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
