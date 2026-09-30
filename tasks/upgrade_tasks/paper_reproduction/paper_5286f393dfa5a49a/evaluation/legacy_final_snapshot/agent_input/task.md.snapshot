# Scientific objective

Determine the relative electronic energies of the three supplied neutral-singlet di-ClPDI-Ph geometries (`crystal`, `(RRRR)-MM`, `(SSSS)-MM`) using the common fixed-geometry protocol defined below. Test the author hypothesis that chiral side-chain organization can make one helical conformer lower in energy than its opposite; do not assume the winning conformer or any numerical result. The supplied geometries are the fixed objects to compare; do not treat an input or any source geometry as a result to copy.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that chiral side-chain organization selects the helical conformation of bay-fused tetrachlorinated diperylene diimide (di-ClPDI-Ph), producing a thermodynamic energy difference between the `(RRRR)-MM` and `(SSSS)-MM` structures.

**Candidate route or mechanism.**
The author route first optimized isolated-molecule conformations and then refined their electronic energies. This benchmark compares the supplied crystal, `(RRRR)-MM`, and `(SSSS)-MM` geometries as fixed objects using the public single-point protocol; it does not require repeating the author optimization stage. The authors' interpretation focuses on stereochemical induction linking side-chain configuration with preferred P or M helicity.

**Discriminating evidence.**
Compare converged fixed-input electronic energies under the public wB97M-V/def2-TZVP/SMD(DCM) protocol. Keep any optimization or alternative method as a separately labeled sensitivity analysis, and assess whether the conformer ordering and the chiral pair energy difference support the proposed stereochemical preference while accounting for method and structural sensitivities.

# Public inputs and scientific boundaries

The public inputs are `data/inputs/crystal.xyz`, `rrrr.xyz`, and `ssss.xyz`. Each is a 138-atom Cartesian geometry in Å for the same neutral molecular composition C80H42Cl4N4O8, with charge 0 and multiplicity 1. Labels identify only the three starting structures: the crystal-derived geometry, `(RRRR)-MM`, and `(SSSS)-MM`; they do not specify the answer. Study the isolated molecule. Use wB97M-V/def2-TZVP with SMD dichloromethane (DCM) for the primary fixed-geometry single-point electronic energies. This is the common measurement protocol, not an expected ordering. Document grids, SCF convergence and numerical settings, and do not interpret this as a periodic-crystal lattice-energy calculation. Report electronic relative energies in kJ/mol using a clearly stated zero/reference.

# Required scientific validation/investigation

Validate atom count, elements, charge and multiplicity before calculation. Compute comparable single-point electronic energies for the three supplied labeled geometries (or, if you relax them, retain and report the fixed-input energies as the primary comparison and identify relaxation as a separate sensitivity check). Establish numerical SCF/energy convergence for each fixed geometry. Record the single-point calculation actually performed; optimization and frequency calculations are not prerequisites for this fixed-geometry task. Optimization and frequency calculations are optional, separate sensitivity analyses and must not replace the primary fixed-input energies. Report per-label outcomes and diagnostics. The investigation is complete when all three inputs have a documented outcome and the relative-energy table, ordering, validation evidence, uncertainty are supplied. If a calculation cannot be completed, provide the bounded-failure branch and explain what conclusion remains unsupported.

# Deliverables

Submit `report/results.json` conforming to the schema. Include per-structure identity and validation context, fixed-input electronic-energy outcomes, with any relaxed geometries reported separately, a relative-energy table, the `(RRRR)-MM` versus `(SSSS)-MM` difference if computable, ordering, conclusion. Include enough provenance to reproduce the chosen calculations.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
