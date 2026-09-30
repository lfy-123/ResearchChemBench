# Scientific objective

Determine the relative electronic energies of the three supplied neutral-singlet di-ClPDI-Ph geometries (`crystal`, `(RRRR)-MM`, `(SSSS)-MM`) after independently choosing and documenting a defensible quantum-chemical workflow. Decide whether the three calculations support a thermodynamic preference among these labeled structures, while separating that bounded comparison from any claim about an exhaustive global minimum. The supplied geometries are the fixed objects to compare; do not treat an input or any source geometry as a result to copy.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that chiral side-chain organization selects the helical conformation of bay-fused tetrachlorinated diperylene diimide (di-ClPDI-Ph), producing a thermodynamic energy difference between the `(RRRR)-MM` and `(SSSS)-MM` structures.

**Candidate route or mechanism.**
The relevant comparison is among optimized isolated-molecule conformations corresponding to the supplied crystal, `(RRRR)-MM`, and `(SSSS)-MM` geometries. The authors' interpretation focuses on stereochemical induction linking side-chain configuration with preferred P or M helicity.

**Discriminating evidence.**
Compare converged electronic energies for the three conformations, with geometry optimization and stationarity or frequency diagnostics where feasible. Use a stated solvation treatment and electronic-structure method, and assess whether the conformer ordering and the chiral pair energy difference support the proposed stereochemical preference while accounting for method and structural sensitivities.

# Public inputs and scientific boundaries

The public inputs are `data/inputs/crystal.xyz`, `rrrr.xyz`, and `ssss.xyz`. Each is a 138-atom Cartesian geometry in Å for the same neutral molecular composition C80H42Cl4N4O8, with charge 0 and multiplicity 1. Labels identify only the three starting structures and do not specify an expected ordering. Study the isolated molecule. You may select an implicit solvent and electronic-structure method, but state them, and do not interpret this as a periodic-crystal lattice-energy calculation. Report electronic relative energies in kJ/mol using a clearly stated zero/reference.

# Required scientific validation/investigation

Validate atom count, elements, charge and multiplicity before calculation. Formulate and justify a computational route, then compute comparable single-point electronic energies for the three supplied labeled geometries (or, if you relax them, retain and report the fixed-input energies as the primary comparison and identify relaxation as a separate sensitivity check). Establish numerical convergence and, where feasible, stationary-point character using frequency or another explicit diagnostic; do not claim to have reproduced hidden optimized coordinates. Report per-label outcomes and diagnostics. The investigation is complete when all three inputs have a documented outcome and the relative-energy table, ordering, validation evidence, uncertainty and limitations are supplied. Stop after these three labeled structures have been treated; do not claim exhaustive conformer coverage. If a calculation cannot be completed, provide the bounded-failure branch and explain what conclusion remains unsupported.

# Deliverables

Submit `report/results.json` conforming to the schema. Include per-structure identity and validation context, optimized-geometry/energy outcomes, a relative-energy table, the `(RRRR)-MM` versus `(SSSS)-MM` difference if computable, ordering, conclusion, and limitations. Include enough provenance to reproduce the chosen calculations.
