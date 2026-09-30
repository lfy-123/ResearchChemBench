# Scientific objective

Determine and validate the free-energy barrier for C-H activation of the supplied neutral closed-shell borylene complex, and characterize the connected C-H cleavage/B-H formation endpoint. Independently select plausible pathway representations and report what the calculation supports.

# Public inputs and scientific boundaries

Use `data/inputs/ncb_h_ch3_complex8.xyz`, a 92-atom Cartesian geometry of neutral singlet complex 8 (NCB(H)-CH3) from SI Figure S2. The boundary is an isolated molecular electronic-structure calculation beginning from this geometry. Choose and disclose model chemistry, thermal convention, and treatment of dispersion/solvation. The measured quantities are validated stationary-point frequencies, connectivity, and the free-energy barrier in kcal/mol.

# Required scientific validation/investigation

Propose and investigate plausible C-H activation pathway initializations, deduplicate equivalent stationary points, and advance only candidates with converged structures and chemically meaningful bond changes. Validate a selected TS by exactly one relevant imaginary frequency plus IRC, relaxed scan, or justified equivalent connectivity evidence. Report candidate coverage, discarded candidates and reasons, convergence, atom identities, uncertainty/sensitivity, and limitations. Completion is a validated pathway with sensitivity evidence, or a bounded failure report after the declared candidate generation and validation search is exhausted. In the bounded-failure branch, submit `status: "bounded_failure"`, set `barrier` to null, and report the attempted candidates and limitations without fabricated numerical or structure values. Stop at that point and do not claim an unvalidated mechanism.

# Deliverables

Write `report/results.json` conforming to the local `submission_schema.json`, including every schema-required field and the available candidate records, selected pathway if any, barrier and units if available, structures, frequencies, connectivity evidence, method/free-energy convention, sensitivity, coverage and conclusion.
