# Scientific objective

Using the supplied Fe(III)-peroxo 12-TMC plus DMA model, determine which chemically plausible elementary mechanism best accounts for N-demethylation on the modeled electronic potential-energy surface. Independently formulate and discriminate plausible routes without relying on an external paper or a preselected transition-state structure.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that N-demethylation may proceed through initial peroxide O–O homolysis to generate an Fe(IV)(oxo)(oxyl) species, followed by substrate hydrogen-atom transfer, and interpret this O–O-cleavage-first sequence as kinetically relevant relative to direct abstraction by the peroxo reactant.

**Candidate route or mechanism.**
Evaluate the proposed O–O-cleavage-first sequence, including the oxo/oxyl intermediate and subsequent DMA hydrogen-atom transfer, alongside a direct H-atom-abstraction route from the peroxo reactant. Treat both as candidate pathways whose stationary points, atom mapping, and connections must be established independently.

**Discriminating evidence.**
Use converged geometries, frequency analyses with a single event-associated imaginary mode for transition states, IRC or explicit endpoint following, connectivity and atom mapping, and electronic barrier comparisons from the common 1RC reference to distinguish the candidate routes. Spin-state and spin-density analysis may help interpret the proposed oxo/oxyl state.

# Public inputs and scientific boundaries

The file `data/inputs/1rc_dma.xyz` is a 67-atom Cartesian XYZ geometry containing the complete 1RC model: [Fe(III)(O2)(12-TMC)]+ with one DMA molecule. Its first line is the atom count and its comment identifies the source geometry. Treat the modeled complex as net charge +1 and sextet multiplicity (2S+1=6). Atom order is the order in the XYZ file; the two adjacent oxygen atoms bound to Fe are the peroxo O atoms, and the DMA fragment is the aniline-containing fragment separated from the metal complex in the supplied geometry. Do not alter connectivity, protonation, charge, multiplicity, or isotope identity without reporting the change and its scientific consequence. The scored system is the isolated molecule; do not add a host or solvent.

The research object is the electronic potential-energy surface of this fixed model. Report electronic energies relative to the supplied 1RC reference in kcal/mol, and state the electronic-structure method, solvent model, dispersion treatment, and geometry/frequency settings actually used. The endpoint is DMA N-demethylation represented by cleavage/transfer of one N–CH3 hydrogen-equivalent into the oxidant model; any proposed intermediate or product must retain atom mapping to the input and explicitly describe added or removed atoms. No product-side structure is supplied or assumed.

# Required scientific validation/investigation

Propose a finite, chemically justified candidate-generation strategy covering the distinct bond-change hypotheses you consider plausible. Generate and deduplicate candidate reactant complexes, intermediates, and transition states by connectivity, atom mapping, and geometry. Advance a candidate only after geometry convergence and frequency analysis; call it a transition state only with one reaction-coordinate imaginary mode involving the proposed event. Validate each claimed route by IRC in both directions or an equivalently explicit endpoint-following analysis, and retain endpoint structures and mapping. Compare all validated pathways from the same 1RC reference and distinguish a demonstrated pathway from an untested hypothesis.

The investigation is complete when every proposed route has either a validated stationary-point/connection set and barrier comparison, or a documented bounded failure. Stop when additional independently generated candidates repeatedly produce retained duplicates or fail for recorded reasons and no untested chemically distinct hypothesis remains within the stated scope. Report the candidate-generation scope, search coverage, deduplication, failed attempts, stopping reason, and limitations; do not invent a discovery story from an unvalidated calculation.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. Include all mode-appropriate required result keys, the proposed or recovered route set, candidate-by-candidate validation evidence, relative electronic energies/barriers with units, endpoint/connectivity evidence, the evidence-based mechanistic conclusion or route comparison, and limitations. If no route reaches validation, use the bounded-failure branch with the attempted candidates and evidence.
