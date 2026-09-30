# Scientific objective

Determine the relative electronic energies of the three supplied neutral-singlet di-ClPDI-Ph geometries (`crystal`, `(RRRR)-MM`, `(SSSS)-MM`) using the common fixed-geometry protocol defined below. Decide whether the three fixed-geometry electronic energies support an energetic preference among these labeled structures, while separating that bounded comparison from any claim about an exhaustive global minimum. The supplied geometries are the fixed objects to compare; do not treat an input or any source geometry as a result to copy.

# Public inputs and scientific boundaries

The public inputs are `data/inputs/crystal.xyz`, `rrrr.xyz`, and `ssss.xyz`. Each is a 138-atom Cartesian geometry in Å for the same neutral molecular composition C80H42Cl4N4O8, with charge 0 and multiplicity 1. Labels identify only the three starting structures and do not specify an expected ordering. Study the isolated molecule. Use wB97M-V/def2-TZVP with SMD dichloromethane (DCM) for the primary fixed-geometry single-point electronic energies. This is the common measurement protocol, not an expected ordering. Document grids, SCF convergence and numerical settings, and do not interpret this as a periodic-crystal lattice-energy calculation. Report electronic relative energies in kJ/mol using a clearly stated zero/reference.

This is an autonomous-research task on three explicitly supplied fixed geometries. Their identities are inputs; structure discovery is not scored. Do not use or retrieve the paper, SI, additional author structures, author hypotheses, published or hidden energy rankings, hidden reference values, or evaluator conclusions as inputs. Independently interpret your calculations within the public protocol.

# Required scientific validation/investigation

Validate atom count, elements, charge and multiplicity before calculation. Formulate and justify a computational route, then compute comparable single-point electronic energies for the three supplied labeled geometries (or, if you relax them, retain and report the fixed-input energies as the primary comparison and identify relaxation as a separate sensitivity check). Establish numerical SCF/energy convergence for each fixed geometry. Record the single-point calculation actually performed; optimization and frequency calculations are not prerequisites for this fixed-geometry task. Optimization and frequency calculations are optional, separate sensitivity analyses and must not replace the primary fixed-input energies. Report per-label outcomes and diagnostics. The investigation is complete when all three inputs have a documented outcome and the relative-energy table, ordering, validation evidence, uncertainty are supplied. If a calculation cannot be completed, provide the bounded-failure branch and explain what conclusion remains unsupported.

# Deliverables

Submit `report/results.json` conforming to the schema. Include per-structure identity and validation context, fixed-input electronic-energy outcomes, with any relaxed geometries reported separately, a relative-energy table, the `(RRRR)-MM` versus `(SSSS)-MM` difference if computable, ordering, conclusion. Include enough provenance to reproduce the chosen calculations.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
