# Scientific objective

Determine computationally how adsorption of neutral NiCp2 on a nine-Br Au(111) surface changes its molecular spin polarization. Propose and discriminate plausible adsorption arrangements and electronic explanations, then report a validated molecular magnetic moment for the best-supported state or a scientifically justified bounded failure.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json`. The molecule is neutral C10H10Ni, multiplicity 3, with two eta5-cyclopentadienyl rings. The periodic surface is an Au(111) slab with a=b=14.98 Å, gamma=60°, >10 Å vacuum, bottom two Au layers fixed, and nine Br atoms in quasi-(sqrt(3)x(sqrt(3))R30°) packing. No adsorption site, author route, target value, expected ordering or mechanism is supplied. You may choose software/model chemistry, but state it completely; do not consult the paper/SI or general web during the investigation.

# Required scientific validation/investigation

Define a finite candidate-generation rule covering at least three distinct local adsorption environments or orientations, retain unique candidate identity and construction parameters, and deduplicate after relaxation using heavy-atom RMSD plus site identity. Advance candidates only with spin-polarized SCF convergence and report maximum unconstrained force. Compare candidates using a stated physically meaningful criterion and support any mechanism claim with charge, spin-density, orbital or PDOS evidence. Stop when the planned candidate-generation rule is exhausted and every attempted candidate is converged or has a recorded failure; report coverage and limitations. A direct calculation is complete only when the selected state, moment extraction, convergence and an independent validation/restart or sensitivity check are documented.

# Deliverables

Submit `report/results.json` conforming to the schema. Include hypotheses, candidate records, selection rationale, method, convergence and validation evidence, selected molecular moment with sign and magnitude, optional local moments, conclusion and limitations. A bounded-failure branch must use status bounded_failure or partial, provide the schema's concrete failure_reason, report attempted coverage and per-candidate failure causes, and must not fabricate a successful result or selected moment.
