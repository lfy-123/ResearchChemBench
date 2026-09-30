# Scientific objective

Determine computationally how adsorption of neutral NiCp2 on a nine-Br Au(111) surface changes its molecular spin polarization. Propose and discriminate plausible adsorption arrangements and electronic explanations, then report a validated molecular magnetic moment for the best-supported state or a scientifically justified bounded failure.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that interaction with a sufficiently populated Br island can transfer charge to neutral NiCp2 and hybridize its frontier electronic states with the surface. In their interpretation, this interaction can remove one of the two frontier Ni 3d-derived unpaired-electron components, reducing the molecule's intrinsic spin polarization toward an effective S=1/2-like state.

**Candidate route or mechanism.**
Prioritize testing a bridge arrangement in which NiCp2 is initialized over the bridge between two adjacent Br atoms (the authors' conf3-type geometry), while retaining the molecule's orientation and the selected Br pair as explicit construction parameters. Treat this as a candidate explanation to compare against other allowed adsorption arrangements and orientations, not as an assumed outcome.

**Discriminating evidence.**
Distinguish the proposed charge-transfer/hybridization explanation using complementary charge analysis, molecular and atom-resolved spin density, and spin-resolved orbital or projected-density-of-states comparisons between the isolated molecule and adsorbed candidates. Examine whether frontier Ni 3d-derived states split or redistribute in a way consistent with the change in molecular moment.
# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json`. The scored system is one neutral C10H10Ni molecule, multiplicity 3, with two eta5-cyclopentadienyl rings adsorbed on a periodic 4x4 Au(111) slab with a=b=14.98 Å, gamma=60°, >10 Å vacuum, bottom two Au layers fixed, and nine Br atoms in quasi-(sqrt(3)x(sqrt(3))R30°) packing. Treat the isolated molecule, the Au slab and the Br-decorated slab as the stated system components; do not add a host or solvent. You may choose software/model chemistry, but state it completely.

# Required scientific validation/investigation

Define a finite candidate-generation rule covering at least three distinct local adsorption environments or orientations, retain unique candidate identity and construction parameters, and deduplicate after relaxation using heavy-atom RMSD plus site identity. Advance candidates only with spin-polarized SCF convergence and report maximum unconstrained force. Compare candidates using a stated physically meaningful criterion and support any mechanism claim with charge, spin-density, orbital or PDOS evidence. Stop when the planned candidate-generation rule is exhausted and every attempted candidate is converged or has a recorded failure; report coverage and limitations. A direct calculation is complete only when the selected state, moment extraction, convergence and an independent validation/restart or sensitivity check are documented.

# Deliverables

Submit `report/results.json` conforming to the schema. Include hypotheses, candidate records, selection rationale, method, convergence and validation evidence, selected molecular moment with sign and magnitude, optional local moments, conclusion and limitations. A bounded-failure branch must use status bounded_failure or partial, provide the schema's concrete failure_reason, report attempted coverage and per-candidate failure causes, and must not fabricate a successful result or selected moment.
