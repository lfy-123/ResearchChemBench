# Scientific objective

Using the two explicitly defined zwitterionic amino-acid molecules AL and AB in water, investigate how their one-carbon difference changes conformational stability and molecular dipole moment. Identify and discriminate plausible compact and open conformational explanations from your calculations. The scored observables are the validated conformer set, within-molecule relative energies, geometry-based conformer descriptions, and dipole moments; battery-level performance is outside the research object.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the shorter-chain AL may favor a compact arrangement in which the terminal ammonium and carboxylate groups approach one another, whereas the longer-chain AB may favor a more extended arrangement that separates those groups. They associate the chain-length-dependent conformational difference with a difference in molecular dipole moment.

**Candidate route or mechanism.**
Compare compact, terminal-group-contact conformers of AL with open or extended backbone conformers, and compare the analogous compact and extended possibilities for AB. Treat these as candidate structural explanations to test for the isolated zwitterions in the stated aqueous environment.

**Discriminating evidence.**
Use a conformational survey followed by consistent aqueous geometry optimization, within-molecule relative energies, geometry-based compact/open descriptors, and dipole moments for validated candidates. Candidate-level convergence and stationary-point checks should establish whether the proposed structural comparison is supported.


# Public inputs and scientific boundaries

`data/inputs/molecular_system.json` uniquely defines AL as `[NH3+]CCC(=O)[O-]` and AB as `[NH3+]CCCC(=O)[O-]`; each is neutral overall, singlet, and modeled in water. The input does not prescribe a mechanism, winning conformer, software, model chemistry, or result direction. Define compact/open labels quantitatively if you use them, and state charge/protonation, solvent treatment, energy convention, and model limitations. Do not use the paper, SI, general web, or hidden reference values. Do not infer battery lifetime or electrode behavior from these molecule-only calculations.

# Required scientific validation/investigation

Plan and execute an independent conformer investigation for both named molecules. Generate multiple chemically plausible candidates, preserve candidate IDs and provenance, deduplicate with a stated geometry criterion, and optimize every retained candidate consistently in an aqueous model. Verify convergence and stationary-point quality (or report a candidate as failed), calculate dipoles with a stated convention, and define relative energies only within each molecule against its lowest validated candidate. Explain why the candidates cover the compact/open possibilities you considered, and report any alternative hypotheses that were tested and discriminated. Stop when repeated independent generation/seeding no longer adds a distinct validated conformer under your stated criterion, or when computational limits prevent that test; then report bounded failure with attempted candidates and coverage limitations. A complete result has at least one validated conformer for each molecule; otherwise use the bounded-failure branch without fabricating a preferred conformer.

# Deliverables

Submit `report/results.json` and `report/validation.json`. For a complete investigation, report a validated lowest-energy candidate for each molecule and the requested candidate energies and dipoles. If computational limits or failed optimizations prevent that outcome, submit `status: "bounded_failure"`, set unavailable selections/observables to JSON `null`, and include `failure_report` listing attempted candidates, failures and coverage limitations; do not fabricate a preferred conformer or numeric value. `validation.json` must document candidate generation, deduplication, optimization/convergence, stationary-point or failure checks, energy reference conventions, and stopping/coverage evidence. Include units and reproducibility information for every reported observable.
