# Scientific objective

Determine the vertical lowest singlet excitation (S1) of neutral singlet benzoyl-PXX compound 1, and determine whether that excitation is dominated by a single HOMO-to-LUMO orbital transition. Report the S1 excitation energy in eV, the occupied and virtual orbital identifiers used for the dominant contribution, its percentage, and a conclusion about the computational optical assignment. In this reproduction mode, the authors' qualitative hypothesis is that the lowest-energy absorption band can be interpreted through an essentially HOMO-to-LUMO S1 excitation; test that hypothesis independently without assuming a numerical answer or the authors' software, model chemistry, or protocol.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose assigning the lowest-energy absorption band of compound 1 to a bright S1 excitation with π→π* and charge-transfer character.

**Candidate route or mechanism.**
Test a predominantly HOMO-to-LUMO excitation as the candidate electronic transition, with electron density displaced from the electron-rich side of the ribbon toward the ketone acceptor.

**Discriminating evidence.**
The authors use TD-DFT excitation energies and oscillator strengths, orbital-transition contributions, frontier-orbital profiles, and excited-state charge-density differences to examine this assignment. The orbital weights test single-pair dominance, while the spatial density changes test the proposed direction of charge transfer.

# Public inputs and scientific boundaries

The sole molecular input is `data/inputs/compound_1_start.xyz`: a 74-atom Cartesian geometry with formula C43H28O3, representing compound 1. Treat it as one neutral molecule with charge 0 and singlet multiplicity 1 in implicit dichloromethane. The research object is this molecule only; do not add a Lewis acid, counterion, solvent molecule, or alternate protonation state. The measured quantities are the lowest singlet vertical excitation energy and orbital-transition composition. You may re-optimize or validate the supplied geometry and may choose computational methods, basis sets, solvation treatment, and analysis software, but state those choices and their Experimental spectra are context only, not a substitute for the requested calculation.

This is a fixed-structure property track: the supplied coordinates are public inputs for the named property comparison, not a scored structure discovery answer. Do not claim that the input geometry itself was rediscovered; report any optimization or conformer search separately.

# Required scientific validation/investigation

First verify that the XYZ parses, has 74 coordinate rows, formula C43H28O3, and is chemically consistent with a neutral singlet. Use the supplied geometry for the primary ground-state and TD single-point calculation and document electronic convergence. Any optimized-geometry calculation is supplementary and does not replace the given-geometry result. Compute singlet excited states sufficiently to identify the lowest-energy S1 state, and inspect the orbital decomposition of that state. Report the dominant occupied-to-virtual transition and contribution percentage, with orbital indexing conventions. Scientific completion requires converged state calculations on the specified geometry, S1 and its orbital decomposition. If alternative conformers or methods are explored, report the explored set and use them as supplementary analysis rather than silently selecting a favorable result.

# Deliverables

Submit `report/results.json` conforming to the supplied schema. It must contain the input identity checks, computational protocol, convergence/validation evidence, S1 energy and units when obtained, orbital contribution details when obtained, a bounded-failure branch when either quantity is unavailable, and a concise final conclusion. Include paths to logs or output files if produced. Do not include the paper, SI, hidden reference values, or claims that cannot be traced to your calculations.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
